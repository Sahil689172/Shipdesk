#!/usr/bin/env python3
"""
ShipDesk Deploy Agent

The final gatekeeper. Validates that all deployment conditions are met
(QA pass, client identity, approval bound to exact commit SHA), merges
the approved PR, and reports the deployment result to the Switch room.

Usage:
    python -m agents.deploy.main

Requires environment variables — see .env.example at the project root.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any

import requests

from agents.deploy.approval import validate_deployment
from agents.deploy.github_merge import get_pr_info, merge_pr

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
LOG = logging.getLogger("deploy")

SWITCH_API_URL = os.getenv("SWITCH_API_URL", "http://localhost:8080/api")
SWITCH_API_KEY = os.getenv("SWITCH_API_KEY", "")
ROOM_ID = os.getenv("SWITCH_ROOM_ID", "shipdesk-client-project")

CLOUDFLARE_API_URL = os.getenv("CLOUDFLARE_API_URL", "https://api.cloudflare.com/client/v4")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
CLOUDFLARE_PROJECT_NAME = os.getenv("CLOUDFLARE_PROJECT_NAME", "shipdesk-festivekart")

# Comma-separated list of authenticated client IDs who can approve
AUTHENTICATED_CLIENT_IDS = [
    cid.strip()
    for cid in os.getenv("AUTHENTICATED_CLIENT_IDS", "").split(",")
    if cid.strip()
]

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# ---------------------------------------------------------------------------
# Switch room interaction
# ---------------------------------------------------------------------------
def post_message(text: str) -> dict[str, Any]:
    """Post a message to the Switch room."""
    resp = requests.post(
        f"{SWITCH_API_URL}/rooms/{ROOM_ID}/messages",
        json={"text": text, "agent": "deploy"},
        headers={"Authorization": f"Bearer {SWITCH_API_KEY}"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def fetch_qa_report(task_id: str) -> dict[str, Any] | None:
    """Find the latest QA report for this task in the room history."""
    resp = requests.get(
        f"{SWITCH_API_URL}/rooms/{ROOM_ID}/messages",
        params={"limit": 200},
        headers={"Authorization": f"Bearer {SWITCH_API_KEY}"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    messages = data.get("messages", data) if isinstance(data, dict) else data

    for msg in reversed(messages):
        if not isinstance(msg, dict):
            continue
        text = msg.get("text", "") or msg.get("content", "")
        if "QA REPORT" in text and task_id in text:
            # Try to parse the structured report from the message
            try:
                # Look for JSON embedded in the message
                json_start = text.find("{")
                json_end = text.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    return json.loads(text[json_start:json_end])
            except json.JSONDecodeError:
                pass
            # Fall back to constructing a minimal record from the text
            if "QA PASS" in text:
                return {"verdict": "QA_PASS", "posted_at": msg.get("timestamp", "")}
    return None


def fetch_approval_record(task_id: str) -> dict[str, Any] | None:
    """Find the client approval record for this task."""
    resp = requests.get(
        f"{SWITCH_API_URL}/rooms/{ROOM_ID}/decisions",
        params={"task_id": task_id},
        headers={"Authorization": f"Bearer {SWITCH_API_KEY}"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    decisions = data.get("decisions", data) if isinstance(data, dict) else data

    for decision in reversed(decisions):
        if not isinstance(decision, dict):
            continue
        if decision.get("task_id") == task_id and decision.get("type") == "client_approval":
            return decision
    return None


# ---------------------------------------------------------------------------
# Cloudflare deployment monitoring
# ---------------------------------------------------------------------------
def check_cloudflare_deployment(max_retries: int = 12, interval: int = 15) -> dict[str, Any]:
    """
    Poll Cloudflare Pages for the latest deployment status.

    Returns a dict with status, URL, and deployment ID.
    Retries every 15 seconds for up to 3 minutes.
    """
    if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ACCOUNT_ID:
        return {"status": "unknown", "url": "", "deploy_id": "",
                "note": "Cloudflare credentials not configured"}

    url = (
        f"{CLOUDFLARE_API_URL}/accounts/{CLOUDFLARE_ACCOUNT_ID}/"
        f"pages/projects/{CLOUDFLARE_PROJECT_NAME}/deployments"
    )

    for attempt in range(max_retries):
        try:
            resp = requests.get(
                url,
                params={"per_page": 1, "sort": "created_on:desc"},
                headers={"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"},
                timeout=15,
            )
            resp.raise_for_status()
            deployments = resp.json().get("result", [])

            if not deployments:
                time.sleep(interval)
                continue

            latest = deployments[0]
            status = latest.get("latest_stage", {}).get("status", "unknown")
            deploy_url = latest.get("url", "")
            deploy_id = latest.get("id", "")

            if status in ("success", "failure"):
                return {
                    "status": "success" if status == "success" else "failed",
                    "url": f"https://{deploy_url}" if deploy_url else "",
                    "deploy_id": deploy_id,
                }

            LOG.info("Cloudflare deployment in progress (attempt %d/%d): %s",
                      attempt + 1, max_retries, status)
            time.sleep(interval)

        except requests.RequestException as exc:
            LOG.warning("Cloudflare API error (attempt %d): %s", attempt + 1, exc)
            time.sleep(interval)

    return {"status": "timeout", "url": "", "deploy_id": "",
            "note": "Deployment status check timed out after 3 minutes"}


# ---------------------------------------------------------------------------
# Main deployment handler
# ---------------------------------------------------------------------------
def handle_deployment_request(
    task_id: str,
    pr_number: int,
) -> dict[str, Any]:
    """
    Process a deployment request: validate, merge, monitor, report.

    Returns a dict with the deployment result for logging.
    """
    LOG.info("Deployment request received — Task: %s, PR: #%d", task_id, pr_number)

    # Step 1: Fetch PR info from GitHub
    try:
        pr_info = get_pr_info(pr_number)
    except requests.RequestException as exc:
        LOG.error("Failed to fetch PR #%d: %s", pr_number, exc)
        post_message(
            f"❌ DEPLOYMENT BLOCKED\nTask ID: {task_id}\nPR: #{pr_number}\n"
            f"Reason: Could not fetch PR information from GitHub.\nError: {exc}"
        )
        return {"result": "failed", "reason": "Could not fetch PR info"}

    pr_head_sha = pr_info.get("head", {}).get("sha", "")
    pr_state = pr_info.get("state", "unknown")
    pr_title = pr_info.get("title", "")

    LOG.info("PR #%d — state: %s, HEAD: %s", pr_number, pr_state, pr_head_sha[:8])

    # Step 2: Fetch QA report and client approval from the room
    qa_report = fetch_qa_report(task_id)
    approval_record = fetch_approval_record(task_id)

    # Step 3: Run all validation checks
    validation = validate_deployment(
        qa_report=qa_report,
        approval_record=approval_record,
        pr_head_sha=pr_head_sha,
        pr_number=pr_number,
        pr_state=pr_state,
        authenticated_client_ids=AUTHENTICATED_CLIENT_IDS,
    )

    if not validation.passed:
        post_message(
            f"❌ DEPLOYMENT BLOCKED\n"
            f"Task ID: {task_id}\n"
            f"PR: #{pr_number}\n\n"
            f"{validation.summary()}"
        )
        return {"result": "blocked", "reasons": validation.failed_checks}

    LOG.info("All deployment conditions passed for Task %s, PR #%d", task_id, pr_number)

    # Step 4: Merge the PR
    post_message(
        f"✅ All checks passed. Merging PR #{pr_number} for Task {task_id}..."
    )

    try:
        merge_result = merge_pr(
            pr_number=pr_number,
            commit_sha=pr_head_sha,
            commit_message_title=pr_title,
            commit_message_body=f"Task: {task_id}\nApproved commit: {pr_head_sha}",
        )
    except RuntimeError as exc:
        post_message(
            f"❌ MERGE FAILED\nTask ID: {task_id}\nPR: #{pr_number}\nError: {exc}"
        )
        return {"result": "failed", "reason": str(exc)}

    merge_sha = merge_result.get("sha", "")
    merge_ts = datetime.now(timezone.utc).isoformat()

    # Step 5: Monitor Cloudflare deployment
    post_message(f"PR #{pr_number} merged. Waiting for Cloudflare Pages deployment...")

    deploy_info = check_cloudflare_deployment()
    deploy_status = deploy_info.get("status", "unknown")
    production_url = deploy_info.get("url", "")

    # Step 6: Report final result
    if deploy_status == "success":
        result_text = "DEPLOYED"
        icon = "🚀"
    elif deploy_status == "failed":
        result_text = "FAILED"
        icon = "❌"
    else:
        result_text = "TIMEOUT"
        icon = "⏳"

    report = (
        f"{icon} DEPLOYMENT REPORT\n"
        f"Task ID:           {task_id}\n"
        f"PR Number:         #{pr_number}\n"
        f"Merged commit SHA: {merge_sha[:8] if merge_sha else 'unknown'}\n"
        f"Merge timestamp:   {merge_ts}\n\n"
        f"Cloudflare deployment:\n"
        f"- Status:         {deploy_status}\n"
        f"- Production URL:  {production_url or 'not available'}\n"
        f"- Deploy ID:      {deploy_info.get('deploy_id', 'n/a')}\n\n"
        f"RESULT: {result_text}"
    )

    if deploy_status != "success" and deploy_info.get("note"):
        report += f"\nNote: {deploy_info['note']}"

    post_message(report)
    LOG.info("Deployment complete — Task %s, Result: %s", task_id, result_text)

    return {
        "result": result_text.lower(),
        "merge_sha": merge_sha,
        "deploy_status": deploy_status,
        "production_url": production_url,
    }


# ---------------------------------------------------------------------------
# Event listener (SSE)
# ---------------------------------------------------------------------------
def listen() -> None:
    """Listen for deployment requests in the Switch room via SSE."""
    LOG.info("Deploy Agent starting — room: %s", ROOM_ID)

    url = f"{SWITCH_API_URL}/rooms/{ROOM_ID}/events"
    headers = {
        "Authorization": f"Bearer {SWITCH_API_KEY}",
        "Accept": "text/event-stream",
    }

    try:
        with requests.get(url, headers=headers, stream=True, timeout=300) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue

                try:
                    event = json.loads(line[6:])
                except json.JSONDecodeError:
                    continue

                # Only process deployment requests
                if event.get("agent") == "deploy":
                    continue
                if event.get("type") not in ("message", "deployment_request"):
                    continue

                text = event.get("text", "")
                task_id = event.get("task_id", "")
                pr_number = event.get("pr_number")

                if not pr_number:
                    # Try to parse PR number from message text
                    import re
                    match = re.search(r"PR\s*#?(\d+)", text)
                    if match:
                        pr_number = int(match.group(1))

                if task_id and pr_number:
                    handle_deployment_request(task_id, int(pr_number))

    except requests.exceptions.ConnectionError:
        LOG.error("Cannot connect to Switch server at %s", SWITCH_API_URL)
        LOG.error("Make sure Switch Console is running. See switch/SETUP.md")
        sys.exit(1)
    except KeyboardInterrupt:
        LOG.info("Shutting down Deploy Agent")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if not os.getenv("GITHUB_TOKEN"):
        LOG.error("GITHUB_TOKEN is not set. Copy .env.example to .env and fill in values.")
        sys.exit(1)

    LOG.info("Deploy Agent ready")
    LOG.info("GitHub repo: %s", os.getenv("GITHUB_REPO", "Sahil689172/Shipdesk"))
    LOG.info("Switch API: %s", SWITCH_API_URL)
    LOG.info("Authenticated clients: %s", AUTHENTICATED_CLIENT_IDS or "(none configured)")

    listen()
