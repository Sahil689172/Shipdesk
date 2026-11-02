# ShipDesk – Switch Room Rules

These rules govern every participant (human and agent) inside the
`shipdesk-client-project` Switch room. All agents must read and follow
these rules before acting. Rules are enforced by the Deploy Agent and
the team; violations block deployment.

---

## 1. Identity and Access

| Rule | Detail |
|------|--------|
| R-01 | Only authenticated team members and the designated client account may post in this room. |
| R-02 | Agents must identify themselves by their assigned role name in every handoff message. |
| R-03 | A Discord display name or casual message saying "approved" does not count as an authenticated approval. Approval must be recorded as a Switch decision tied to a task ID, PR number and commit SHA. |
| R-04 | No team member may impersonate the client or submit an approval on the client's behalf. |

---

## 2. Task Lifecycle

| Rule | Detail |
|------|--------|
| R-05 | Every piece of work must have a task created by Intake before Builder starts. No task = no branch = no PR. |
| R-06 | Task IDs follow the format `SD-NNN` (e.g. `SD-001`). Intake assigns these sequentially. |
| R-07 | A task must move through statuses in order: `open → in_progress → in_review → awaiting_approval → approved → deployed`. Skipping a status requires an explicit team override with a written reason. |
| R-08 | Only Intake may create tasks. Only the client or team may cancel a task. |

---

## 3. Builder Rules

| Rule | Detail |
|------|--------|
| R-09 | Builder must create a new feature branch for every task. Branch name format: `feature/SD-NNN-short-description`. |
| R-10 | Builder must only modify files relevant to the task scope defined by Intake. Changes outside scope require a new task. |
| R-11 | Builder must NOT merge any branch into `main` directly. All merges go through a pull request reviewed by QA and approved by the client. |
| R-12 | Every PR message from Builder must include: task ID, branch name, commit SHA, list of changed files, summary of changes and preview URL (once available). |
| R-13 | If QA returns a failure report, Builder must address every listed issue in a new commit. A new commit resets QA review; the old QA report is invalidated. |

---

## 4. QA Rules

| Rule | Detail |
|------|--------|
| R-14 | QA must review the PR independently. QA must not reuse Builder's context, test results or self-reported checks. |
| R-15 | Every QA report must reference the exact commit SHA being reviewed. A report without a commit SHA is invalid. |
| R-16 | QA must map each acceptance criterion from the task to a pass or fail result with evidence (screenshot reference, test output or specific observation). |
| R-17 | QA must check both desktop (1280px) and mobile (375px) layouts for any UI change. |
| R-18 | QA must explicitly state the final verdict: `QA PASS` or `QA FAIL`. No ambiguous language. |
| R-19 | QA must not approve a commit it did not review. If Builder pushes a new commit after QA's review, QA must re-review the new commit. |

---

## 5. Client Approval Rules

| Rule | Detail |
|------|--------|
| R-20 | The client must review the preview URL before approving. Approval without a viewed preview is not valid. |
| R-21 | Approval must be submitted as a Switch decision containing: task ID, PR number, commit SHA, preview URL, decision (approved/rejected), client identifier and timestamp. |
| R-22 | Approval is tied to a specific commit SHA. If Builder pushes a new commit after the client approved, the approval is invalidated and the client must re-review. |
| R-23 | The client may reject at any point before Deploy merges. A rejection sends the task back to Builder with written feedback. |

---

## 6. Deploy Rules

| Rule | Detail |
|------|--------|
| R-24 | Deploy must validate ALL of the following before merging: QA status = PASS, client decision = approved, PR is still open, PR commit SHA matches the approved SHA, approval timestamp is after the latest QA pass. |
| R-25 | Deploy must abort and report failure if any condition in R-24 is not met. |
| R-26 | Deploy must NOT have general write access to the repository. It holds a scoped token with merge-only permission on PRs that have passed all checks. |
| R-27 | After merging, Deploy must monitor the Cloudflare Pages deployment and report the final production URL and deployment status in the room. |
| R-28 | Deploy must not retry a failed deployment automatically. It must report the failure and wait for a team decision. |

---

## 7. Security Rules

| Rule | Detail |
|------|--------|
| R-29 | No agent or human may post API keys, tokens, passwords or secrets in the room. Use environment variables only. |
| R-30 | No agent may execute arbitrary shell commands on a production system. All changes go through Git and the PR process. |
| R-31 | The `main` branch is protected. Direct pushes are forbidden for all agents and all team members except in a declared emergency override with a written justification. |
| R-32 | All deployment decisions and their reasons are recorded permanently in the room history. Records must not be deleted. |

---

## 8. Escalation

If an agent is stuck, blocked or encounters an unexpected condition it cannot
resolve, it must post a clear `BLOCKED:` message in the room with the task ID,
the blocking condition and what it needs to proceed. A human team member must
then intervene.

---

*These rules are the enforcement layer. The room-template.yaml is the
configuration layer. Both must be consistent with each other.*
