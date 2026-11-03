"""
GitHub PR merge logic for the ShipDesk Deploy Agent.

Uses a scoped GitHub token with merge-only permissions to merge an
approved pull request into the protected main branch.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

import requests

LOG = logging.getLogger("deploy.github")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "Sahil689172/Shipdesk")
GITHUB_API = "https://api.github.com"


# ---------------------------------------------------------------------------
# PR inspection
# ---------------------------------------------------------------------------
def get_pr_info(pr_number: int) -> dict[str, Any]:
    """Fetch PR metadata: state, head SHA, branch name, mergeable status."""
    url = f"{GITHUB_API}/repos/{GITHUB_REPO}/pulls/{pr_number}"
    resp = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def get_pr_commits(pr_number: int) -> list[dict[str, Any]]:
    """Fetch the list of commits on the PR branch."""
    url = f"{GITHUB_API}/repos/{GITHUB_REPO}/pulls/{pr_number}/commits"
    resp = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# PR merge
# ---------------------------------------------------------------------------
def merge_pr(
    pr_number: int,
    commit_sha: str,
    commit_message_title: str,
    commit_message_body: str = "",
) -> dict[str, Any]:
    """
    Merge an approved PR using a squash merge.

    Returns the API response containing the merge commit SHA, or raises
    an exception with the failure reason.
    """
    url = f"{GITHUB_API}/repos/{GITHUB_REPO}/pulls/{pr_number}/merge"

    full_message = commit_message_title
    if commit_message_body:
        full_message += "\n\n" + commit_message_body

    payload = {
        "commit_title": f"Merge PR #{pr_number}: {commit_message_title}",
        "commit_message": f"Approved commit: {commit_sha}\n{commit_message_body}",
        "merge_method": "squash",
    }

    resp = requests.put(
        url,
        json=payload,
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        },
        timeout=30,
    )

    if resp.status_code == 200:
        result = resp.json()
        LOG.info("PR #%d merged successfully. SHA: %s", pr_number, result.get("sha", ""))
        return result
    else:
        error_detail = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text
        LOG.error("Merge failed for PR #%d: %s", pr_number, error_detail)
        raise RuntimeError(f"GitHub merge failed: {error_detail}")


# ---------------------------------------------------------------------------
# Branch protection check (informational)
# ---------------------------------------------------------------------------
def check_branch_protection() -> dict[str, Any] | None:
    """
    Check if main branch has protection rules configured.

    Returns None if no protection is configured (informational only —
    the merge itself will fail if protections block it).
    """
    url = f"{GITHUB_API}/repos/{GITHUB_REPO}/branches/main/protection"
    resp = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        },
        timeout=15,
    )
    if resp.status_code == 404:
        LOG.warning("Branch main has no protection rules configured.")
        return None
    resp.raise_for_status()
    return resp.json()
