#!/usr/bin/env python3
"""
ShipDesk Intake Agent

Receives client change requests from a Switch room, converts them into
structured tasks using an LLM, asks clarifying questions when needed,
and assigns confirmed tasks to the Builder Agent.

Usage:
    python -m agents.intake.main

Requires environment variables — see .env.example at the project root.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from typing import Any

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
LOG = logging.getLogger("intake")

SWITCH_API_URL = os.getenv("SWITCH_API_URL", "http://localhost:8080/api")
SWITCH_API_KEY = os.getenv("SWITCH_API_KEY", "")
ROOM_ID = os.getenv("SWITCH_ROOM_ID", "shipdesk-client-project")

LLM_API_URL = os.getenv("LLM_API_URL", "https://api.openai.com/v1/chat/completions")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

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
        json={"text": text, "agent": "intake"},
        headers={"Authorization": f"Bearer {SWITCH_API_KEY}"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def post_task(task: dict[str, Any]) -> dict[str, Any]:
    """Create a structured task in the Switch room."""
    payload = {
        "agent": "intake",
        "type": "task",
        "title": task["title"],
        "content": json.dumps(task, indent=2),
        "metadata": {
            "task_id": task["task_id"],
            "priority": task["priority"],
            "status": task["status"],
            "assigned_to": task.get("assigned_to", "builder"),
        },
    }
    resp = requests.post(
        f"{SWITCH_API_URL}/rooms/{ROOM_ID}/tasks",
        json=payload,
        headers={"Authorization": f"Bearer {SWITCH_API_KEY}"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def get_room_history(limit: int = 100) -> list[dict[str, Any]]:
    """Fetch recent room messages/tasks to determine the next task ID."""
    resp = requests.get(
        f"{SWITCH_API_URL}/rooms/{ROOM_ID}/messages",
        params={"limit": limit},
        headers={"Authorization": f"Bearer {SWITCH_API_KEY}"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("messages", data) if isinstance(data, dict) else data


# ---------------------------------------------------------------------------
# Task ID management
# ---------------------------------------------------------------------------
def get_next_task_id() -> str:
    """Scan room history for existing SD-NNN IDs and return the next one."""
    highest = 0
    try:
        history = get_room_history(limit=200)
    except Exception as exc:
        LOG.warning("Could not fetch room history for task ID: %s", exc)
        history = []

    for entry in history:
        text = ""
        if isinstance(entry, dict):
            text = entry.get("text", "") or entry.get("content", "") or ""
        elif isinstance(entry, str):
            text = entry

        matches = re.findall(r"SD-(\d{3,})", text)
        for m in matches:
            highest = max(highest, int(m))

    return f"SD-{highest + 1:03d}"


# ---------------------------------------------------------------------------
# LLM interaction
# ---------------------------------------------------------------------------
def llm_complete(system_prompt: str, user_prompt: str) -> str:
    """Call an OpenAI-compatible chat completion endpoint."""
    resp = requests.post(
        LLM_API_URL,
        json={
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        },
        headers={"Authorization": f"Bearer {LLM_API_KEY}"},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


# ---------------------------------------------------------------------------
# Request processing
# ---------------------------------------------------------------------------
def process_client_message(
    client_message: str,
    client_id: str,
    clarifications: list[dict[str, str]] | None = None,
) -> dict[str, Any] | None:
    """
    Send the client message to the LLM and parse the response.

    Returns a task dict if the request is clear, or None if clarification
    is needed (in which case a question is posted to the room).
    """
    from agents.intake.prompts import SYSTEM_PROMPT, TASK_EXTRACTION_PROMPT

    clarification_text = (
        json.dumps(clarifications, indent=2) if clarifications else "None"
    )

    user_prompt = TASK_EXTRACTION_PROMPT.format(
        client_message=client_message,
        client_id=client_id,
        clarifications=clarification_text,
    )

    raw = llm_complete(SYSTEM_PROMPT, user_prompt)
    raw = raw.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        LOG.error("LLM returned non-JSON: %s", raw[:200])
        post_message(
            "I had trouble processing that request. Could you rephrase it?\n\n"
            "For example: 'Change the hero headline to say Big Diwali Sale — 40% OFF'"
        )
        return None

    # Check if clarification is needed
    if result.get("needs_clarification"):
        question = result.get("question", "Could you provide more detail?")
        post_message(f"📋 Clarification needed: {question}")
        return None

    # Populate task with metadata
    task_id = get_next_task_id()
    now = datetime.now(timezone.utc).isoformat()

    task = {
        "task_id": result.get("task_id", task_id),
        "title": result.get("title", "Untitled task"),
        "requested_by": client_id,
        "priority": result.get("priority", "medium"),
        "status": "open",
        "scope": result.get("scope", []),
        "out_of_scope": result.get("out_of_scope", []),
        "requirements": result.get("requirements", []),
        "acceptance_criteria": result.get("acceptance_criteria", []),
        "clarifications": clarifications or [],
        "assigned_to": "builder",
        "created_at": now,
        "updated_at": now,
    }

    return task


def create_and_assign_task(task: dict[str, Any]) -> None:
    """Post the task to the Switch room and notify the Builder Agent."""
    post_task(task)

    summary = (
        f"📋 TASK CREATED\n"
        f"Task ID:              {task['task_id']}\n"
        f"Title:                {task['title']}\n"
        f"Requested by:         {task['requested_by']}\n"
        f"Priority:             {task['priority']}\n"
        f"Scope:                {', '.join(task['scope'])}\n"
        f"Out of scope:         {', '.join(task['out_of_scope']) or 'none'}\n\n"
        f"Requirements:\n"
        + "\n".join(f"  - {r}" for r in task["requirements"])
        + "\n\nAcceptance criteria:\n"
        + "\n".join(f"  - [ ] {c}" for c in task["acceptance_criteria"])
        + f"\n\nAssigned to: Builder Agent\nStatus: open"
    )
    post_message(summary)


# ---------------------------------------------------------------------------
# Main event loop (SSE listener)
# ---------------------------------------------------------------------------
def listen() -> None:
    """
    Listen for new messages in the Switch room via Server-Sent Events.

    When a client message arrives, process it through the LLM and either
    ask a clarifying question or create a structured task.
    """
    LOG.info("Intake Agent starting — room: %s", ROOM_ID)

    url = f"{SWITCH_API_URL}/rooms/{ROOM_ID}/events"
    headers = {
        "Authorization": f"Bearer {SWITCH_API_KEY}",
        "Accept": "text/event-stream",
    }

    pending_clarifications: dict[str, list[dict[str, str]]] = {}

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

                # Only process client messages (not our own agent messages)
                if event.get("agent") == "intake":
                    continue
                if event.get("type") not in ("message", "client_message"):
                    continue

                text = event.get("text", "")
                client_id = event.get("author", event.get("client_id", "unknown"))

                LOG.info("Received message from %s: %s", client_id, text[:80])

                clarifications = pending_clarifications.pop(client_id, [])
                task = process_client_message(text, client_id, clarifications)

                if task:
                    create_and_assign_task(task)
                    LOG.info("Task %s created and assigned to Builder", task["task_id"])

    except requests.exceptions.ConnectionError:
        LOG.error("Cannot connect to Switch server at %s", SWITCH_API_URL)
        LOG.error("Make sure Switch Console is running. See switch/SETUP.md")
        sys.exit(1)
    except KeyboardInterrupt:
        LOG.info("Shutting down Intake Agent")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if not LLM_API_KEY:
        LOG.error("LLM_API_KEY is not set. Copy .env.example to .env and fill in values.")
        sys.exit(1)

    LOG.info("LLM model: %s", LLM_MODEL)
    LOG.info("Switch API: %s", SWITCH_API_URL)

    listen()
