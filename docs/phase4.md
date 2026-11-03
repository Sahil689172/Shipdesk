# Phase 4 – Build and Configure the Four Agents

**Date:** November 4, 2026  
**Branch:** `feature/phase-4-agents`

---

## What Phase 4 Delivers

Four specialised agents with clear responsibilities, structured handoffs,
and controlled tool access. Two agents (Intake, Deploy) are custom Python
implementations. Two (Builder, QA) are configured through OpenCode with
instruction files created in Phase 3.

---

## Agent Summary

| Agent | Implementation | Role | Repository Access |
|-------|---------------|------|-------------------|
| **Intake** | Custom Python (`agents/intake/`) | Parse client requests → structured tasks | None |
| **Builder** | OpenCode + `opencode-instructions.md` | Edit code, create branch, open PR | Read + write (feature branches only) |
| **QA** | OpenCode + `opencode-instructions.md` | Independent review, preview inspection | Read-only |
| **Deploy** | Custom Python (`agents/deploy/`) | Validate conditions, merge PR, monitor deploy | Merge-only (scoped token) |

---

## Files Created in Phase 4

### Schemas (`agents/schemas/`)
| File | Purpose |
|------|---------|
| `task.json` | Intake → Builder task structure |
| `implementation_report.json` | Builder → QA PR report structure |
| `qa_report.json` | QA → Room review result (tied to commit SHA) |
| `approval_record.json` | Client → Deploy authenticated approval record |
| `README.md` | Schema documentation and usage |

### Intake Agent (`agents/intake/`)
| File | Purpose |
|------|---------|
| `__init__.py` | Package init |
| `prompts.py` | LLM system prompt, task extraction prompt, clarification prompt |
| `main.py` | SSE listener, LLM interaction, task creation, room posting |

### Deploy Agent (`agents/deploy/`)
| File | Purpose |
|------|---------|
| `__init__.py` | Package init |
| `approval.py` | 9-check validation: QA pass, commit SHA match, client identity, approval binding, PR state, stale commit detection |
| `github_merge.py` | GitHub PR inspection and squash merge via scoped token |
| `main.py` | SSE listener, validation, merge, Cloudflare monitoring, deployment report |

### Integration Configs (`integrations/`)
| File | Purpose |
|------|---------|
| `github/config.example.json` | GitHub token scopes, branch naming, PR template |
| `cloudflare/config.example.json` | Cloudflare Pages project, build settings, deployment monitoring |
| `discord/config.example.json` | Discord bridge config, identity mapping (for Phase 5) |

### Root Files
| File | Purpose |
|------|---------|
| `.env.example` | Environment variable template for all agents |
| `requirements.txt` | Python dependencies (requests, jsonschema, python-dotenv) |

---

## Handoff Contract

```
Client Message
      ↓
Intake Agent ──→ task.json ──→ Builder Agent
                                    ↓
                    implementation_report.json
                                    ↓
                              QA Agent
                                    ↓
                            qa_report.json
                                    ↓
                          Client Review
                                    ↓
                        approval_record.json
                                    ↓
                            Deploy Agent
                                    ↓
                      Merge PR → Cloudflare → Report
```

Every handoff includes the task ID and relevant artifact identifiers.
QA reports and approval records are bound to the full commit SHA.

---

## Deploy Agent Validation Checklist

The Deploy Agent runs 9 checks before merging. ALL must pass:

1. QA report exists with verdict `QA_PASS`
2. QA report commit SHA matches current PR HEAD
3. Client approval decision exists
4. Approval commit SHA matches current PR HEAD
5. Approval PR number matches the PR being merged
6. Approval was submitted by an authenticated client identity
7. Approval timestamp is after the QA pass timestamp
8. PR is currently open (not merged or closed)
9. No new commits were pushed after approval was recorded

If any check fails, the deployment is blocked and the reason is reported.

---

## How to Run

### Setup
```bash
# From the repository root
cp .env.example .env
# Fill in your LLM API key, GitHub token, Switch API key, etc.

pip install -r requirements.txt
```

### Start the Intake Agent
```bash
python -m agents.intake.main
```
Listens for client messages in the Switch room, converts them to tasks,
and assigns them to the Builder Agent.

### Start the Deploy Agent
```bash
python -m agents.deploy.main
```
Listens for deployment requests, validates all conditions, merges approved
PRs, and monitors the Cloudflare Pages deployment.

### Builder and QA Agents
These run through OpenCode with the instruction files at:
- `agents/builder/opencode-instructions.md`
- `agents/qa/opencode-instructions.md`

Connect them to the Switch room per the Phase 3 setup guide.

---

## Phase 4 Exit Criteria

| Criterion | Status |
|-----------|--------|
| Four named agents with distinct responsibilities | ✅ |
| Task and handoff schemas defined | ✅ |
| Agent instructions and configuration | ✅ |
| Deploy Agent validation logic (9 checks) | ✅ |
| Integration config templates | ✅ |
| .env.example with all required variables | ✅ |
| requirements.txt for Python dependencies | ✅ |

**Testing note:** Each agent should be tested individually against the
Switch room before the full chain is tested in Phase 6. See the test
matrix in `plan.md` Section 11 for test cases.

---

## Security Notes

- The Deploy Agent uses a **scoped GitHub token** with merge-only permissions.
- Builder and QA agents use **separate tokens** — Builder can push to feature
  branches but cannot merge. QA is read-only.
- Client approval requires `client_id` from an authenticated source, not a
  Discord display name.
- All tokens, API keys, and secrets go in `.env` (gitignored). Never in code,
  commits, or room messages.
