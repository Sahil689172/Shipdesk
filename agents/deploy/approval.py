"""
Approval validation logic for the ShipDesk Deploy Agent.

Every deployment must pass ALL checks before the PR is merged.
A single failure blocks the deployment and reports the reason.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

LOG = logging.getLogger("deploy.approval")


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------
@dataclass
class ValidationResult:
    """Outcome of the full pre-deployment validation."""

    passed: bool
    failed_checks: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)
    approval_record: dict[str, Any] | None = None

    def summary(self) -> str:
        """Human-readable summary for the room."""
        if self.passed:
            return "All deployment conditions passed."
        lines = ["DEPLOYMENT BLOCKED — the following conditions failed:"]
        for check in self.failed_checks:
            lines.append(f"  ✗ {check}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Individual check functions
# ---------------------------------------------------------------------------
def check_qa_report(qa_report: dict[str, Any] | None) -> tuple[bool, str]:
    """Check 1: A QA report exists with verdict QA_PASS."""
    if qa_report is None:
        return False, "No QA report found for this task."
    if qa_report.get("verdict") != "QA_PASS":
        return False, f"QA verdict is '{qa_report.get('verdict')}', not 'QA_PASS'."
    return True, "QA report exists with QA_PASS verdict."


def check_qa_commit_matches(
    qa_report: dict[str, Any], pr_head_sha: str
) -> tuple[bool, str]:
    """Check 2: QA report commit SHA matches the current PR HEAD."""
    reviewed_sha = qa_report.get("reviewed_commit_sha", "")
    if reviewed_sha != pr_head_sha:
        return (
            False,
            f"QA reviewed commit {reviewed_sha[:8]} but PR HEAD is {pr_head_sha[:8]}. "
            "A new commit was pushed after QA review.",
        )
    return True, f"QA report covers current HEAD {pr_head_sha[:8]}."


def check_client_approval(approval_record: dict[str, Any] | None) -> tuple[bool, str]:
    """Check 3: A client approval decision exists."""
    if approval_record is None:
        return False, "No client approval found for this task."
    if not approval_record.get("client_approval"):
        return False, "Client has rejected this change. Deployment is blocked."
    return True, "Client approval exists."


def check_approval_commit_matches(
    approval_record: dict[str, Any], pr_head_sha: str
) -> tuple[bool, str]:
    """Check 4: Client approval references the same commit SHA as PR HEAD."""
    approved_sha = approval_record.get("commit_sha", "")
    if approved_sha != pr_head_sha:
        return (
            False,
            f"Client approved commit {approved_sha[:8]} but PR HEAD is {pr_head_sha[:8]}. "
            "A new commit was pushed after client approval.",
        )
    return True, f"Approval matches current HEAD {pr_head_sha[:8]}."


def check_approval_pr_matches(
    approval_record: dict[str, Any], pr_number: int
) -> tuple[bool, str]:
    """Check 5: Approval PR number matches the PR being merged."""
    approved_pr = approval_record.get("pull_request_number", 0)
    if approved_pr != pr_number:
        return (
            False,
            f"Approval references PR #{approved_pr} but we are merging PR #{pr_number}.",
        )
    return True, f"Approval references PR #{pr_number}."


def check_client_authenticated(
    approval_record: dict[str, Any], authenticated_client_ids: list[str]
) -> tuple[bool, str]:
    """Check 6: The approval was submitted by an authenticated client."""
    client_id = approval_record.get("client_id", "")
    if not client_id:
        return False, "Approval has no client_id — cannot verify identity."
    if authenticated_client_ids and client_id not in authenticated_client_ids:
        return (
            False,
            f"Client '{client_id}' is not in the authorised client list.",
        )
    return True, f"Client '{client_id}' is authenticated and authorised."


def check_approval_after_qa(
    approval_record: dict[str, Any], qa_report: dict[str, Any]
) -> tuple[bool, str]:
    """Check 7: Approval timestamp is after the QA pass timestamp."""
    approval_ts = approval_record.get("approval_timestamp", "")
    qa_ts = qa_report.get("posted_at", "")

    if not approval_ts or not qa_ts:
        return False, "Missing timestamps — cannot verify approval order."

    try:
        approval_dt = datetime.fromisoformat(approval_ts.replace("Z", "+00:00"))
        qa_dt = datetime.fromisoformat(qa_ts.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return False, "Invalid timestamp format in approval or QA report."

    if approval_dt < qa_dt:
        return False, "Client approved before QA passed. Approval is stale."

    return True, "Approval was recorded after QA pass."


def check_pr_open(pr_state: str) -> tuple[bool, str]:
    """Check 8: The PR is currently open."""
    if pr_state != "open":
        return False, f"PR state is '{pr_state}', not 'open'."
    return True, "PR is open."


def check_no_new_commits(
    approval_record: dict[str, Any], pr_head_sha: str
) -> tuple[bool, str]:
    """Check 9: No new commits were pushed after the approval was recorded."""
    approved_sha = approval_record.get("commit_sha", "")
    if approved_sha != pr_head_sha:
        return (
            False,
            f"New commit detected after approval. Approved {approved_sha[:8]}, "
            f"current {pr_head_sha[:8]}.",
        )
    return True, "No new commits since approval."


# ---------------------------------------------------------------------------
# Full validation
# ---------------------------------------------------------------------------
def validate_deployment(
    qa_report: dict[str, Any] | None,
    approval_record: dict[str, Any] | None,
    pr_head_sha: str,
    pr_number: int,
    pr_state: str,
    authenticated_client_ids: list[str],
) -> ValidationResult:
    """
    Run all pre-deployment checks.

    All must pass. A single failure blocks the merge.
    Returns a ValidationResult with the outcome.
    """
    result = ValidationResult(passed=True)

    checks = [
        ("QA report exists with QA_PASS", lambda: check_qa_report(qa_report)),
        ("QA commit SHA matches PR HEAD", lambda: check_qa_commit_matches(
            qa_report or {}, pr_head_sha)),
        ("Client approval exists", lambda: check_client_approval(approval_record)),
        ("Approval commit SHA matches PR HEAD", lambda: check_approval_commit_matches(
            approval_record or {}, pr_head_sha)),
        ("Approval PR number matches", lambda: check_approval_pr_matches(
            approval_record or {}, pr_number)),
        ("Client is authenticated", lambda: check_client_authenticated(
            approval_record or {}, authenticated_client_ids)),
        ("Approval is after QA pass", lambda: check_approval_after_qa(
            approval_record or {}, qa_report or {})),
        ("PR is currently open", lambda: check_pr_open(pr_state)),
        ("No new commits after approval", lambda: check_no_new_commits(
            approval_record or {}, pr_head_sha)),
    ]

    for check_name, check_fn in checks:
        passed, message = check_fn()
        result.details[check_name] = {"passed": passed, "message": message}
        if not passed:
            result.failed_checks.append(f"{check_name}: {message}")
            result.passed = False
            LOG.warning("CHECK FAILED: %s — %s", check_name, message)

    return result
