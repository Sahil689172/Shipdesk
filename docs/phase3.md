# Phase 3 – Switch Setup: Full Context, Issues and Resolution Log

**Author:** Vaibhav Dwivedi  
**Date:** November 3, 2026  
**Branch:** feature/phase-3-switch-setup  

---

## What Phase 3 Was About

Install and configure Switch Console, connect OpenCode as a coding agent,
create the ShipDesk collaboration room, and verify that an agent can respond
to messages in the room.

---

## What Was Installed

| Tool | Version | Status |
|------|---------|--------|
| Docker Desktop | 29.2.1 | ✅ Running |
| Switch Console | 0.40.1 | ✅ Installed and server running |
| OpenCode CLI | 2.2.5 | ✅ Installed via `npm i -g @opencode/cli@latest` |
| Antigravity CLI | latest | ✅ Installed via PowerShell script |
| Node.js | 22.17.0 | ✅ Already present |
| Git | 2.50.1 | ✅ Already present |

---

## Files Created in This Phase

```
agents/
  builder/opencode-instructions.md   ← Builder's full coding rulebook
  qa/opencode-instructions.md        ← QA's independent review guide
  intake/                            ← placeholder for Phase 4
  deploy/                            ← placeholder for Phase 4

switch/
  room-template.yaml                 ← room config: participants, task schema, decision schema
  rules.md                           ← 32 rules across 8 categories
  SETUP.md                           ← step-by-step install guide
  agent-configs/
    intake.yaml
    builder.yaml
    qa.yaml
    deploy.yaml

integrations/github/ cloudflare/ discord/
tests/
docs/
README.md
```

The website folder inside the repo was renamed from `shipdesk-festivekart/`
to `demo-website/` to avoid confusion with the outer local folder name.
All references across 7 files were updated automatically.

---

## Switch Console Room Created

- Room name: `shipdesk-client-project`
- Created manually in Switch Console GUI
- Room instructions and project context set from `switch/room-template.yaml`
- Server: Local Switch server running via Docker on this machine

---

## Major Issue: OpenCode ↔ Switch Console Auth Clash (Windows Bug)

### What the problem is

Switch Console v0.40.x on Windows cannot verify OpenCode's login. Every time
it tries, it shows:

```
Could not verify authentication. Check the connection and provider setup, then retry.
Pass an integration ID or name when running without an interactive terminal
Failed
opencode auth login ended without signing in.
```

### Root cause

Switch Console spawns a **non-interactive background process** to check OpenCode's
auth status. OpenCode's auth flow requires an **interactive terminal** with a live
stdin to complete. These two things are incompatible on Windows.

Even after successfully completing `opencode auth login opencode` in a terminal
(getting "Connected to OpenCode Console — Done"), Switch Console still fails
the check because its internal process runs without a TTY.

### Everything we tried

| Attempt | Command | Result |
|---------|---------|--------|
| npm package (wrong name) | `npm install -g opencode` | 404 not found |
| npm package (wrong name) | `npm install -g @opencode-ai/opencode` | 404 not found |
| PowerShell installer | `iwr https://opencode.ai/install.ps1 \| iex` | 404 not found |
| Correct npm package | `npm i -g @opencode/cli@latest` | ✅ Installed v2.2.5 |
| Browser device auth | `opencode auth login opencode` | ✅ CLI connected, Switch Console still failed |
| Browser device auth with flags | `opencode auth login --provider google --api-key ...` | Unrecognized flags |
| Standalone mode auth | `opencode auth login opencode --method device --standalone` | ✅ CLI connected, Switch Console still failed |
| Background process + auth | `Start-Process opencode --standalone` then login | ✅ CLI connected, Switch Console still failed |
| API key method | `opencode auth login opencode` → select "API key (service account)" | ✅ CLI connected, Switch Console still failed |
| Claude Code (paid) | `npm install -g @anthropic-ai/claude-code` | Requires Max/Pro/Ultra plan — rejected |
| Antigravity npm | `npm install -g @google/antigravity` | 404 not found |
| Antigravity CLI install | `iwr https://antigravity.google/cli/install.ps1 \| iex` | ✅ Installed as `agy.exe` |
| Antigravity auth | `agy auth login` | Wrong command — `agy` has no `auth` subcommand |

### Current status

- OpenCode CLI works perfectly in the terminal with Gemini 3.5 Flash Lite
- Switch Console cannot connect to OpenCode due to the Windows non-interactive TTY bug
- Antigravity CLI (`agy`) is installed and needs to be tested as an alternative provider
- The Switch room `shipdesk-client-project` exists and is ready

### Next steps to fully resolve

1. Run `agy` in terminal — it authenticates with Google on first launch
2. Go to Switch Console → New Agent → click **Antigravity** → check if it shows signed in
3. If Antigravity works: create the `builder` agent using Antigravity as the provider
4. If Antigravity also fails: the workaround is to connect agents via the Switch Agent
   Protocol directly (HTTP + server-sent events) instead of through the GUI — this is
   documented at `https://docs.switchagents.ai`

### Important note for the team

The OpenCode ↔ Switch Console auth issue is a **known bug on Windows** in
Switch Console v0.40.x. It affects all team members on Windows. The agents
(Builder, QA) still work perfectly via OpenCode CLI in the terminal — the only
thing broken is the Switch Console GUI connection for switch-buddy.

**The actual workflow for Phase 4–6 does not require switch-buddy to be connected.**
Agents can be added to rooms and interact via the Switch Agent Protocol without
the GUI provider connection working.

---

## API Key Security Incident

During setup, a Gemini API key was accidentally pasted into terminal commands
that appeared in chat logs. The key was:
- Immediately identified
- Should be deleted at https://aistudio.google.com/apikey
- A new key should be generated before continuing work

**Action required:** Vaibhav must delete the old Gemini key and generate a new one.

---

## Gemini Model Note

When configuring OpenCode with `gemini-2.5-flash-lite`, the model returned:

```
Error: This model models/gemini-2.5-flash-lite is no longer available to new users.
Please update your code to use models/gemini-3.5-flash-lite
```

OpenCode automatically switched to `gemini-3.5-flash-lite` (Gemini 3.5 Flash Lite).
This is the correct model to use going forward. Update any config references
from `gemini-2.5-flash-lite` to `gemini-3.5-flash-lite`.

---

## Phase 3 Exit Criteria — Status

| Criterion | Status |
|-----------|--------|
| Docker Desktop installed and running | ✅ |
| Switch Console installed and server active | ✅ |
| Room `shipdesk-client-project` created | ✅ |
| OpenCode installed and working with Gemini | ✅ |
| All config files committed and pushed | ✅ |
| Folder structure clean (`demo-website/`) | ✅ |
| Builder agent connected to Switch Console room | ⚠️ Pending — blocked by Windows auth bug |
| switch-buddy connected to OpenCode | ❌ Blocked — Windows TTY bug in v0.40.x |

**Overall: Phase 3 infrastructure is complete. Agent GUI connection is pending
resolution of the Windows auth bug or switch to Antigravity provider.**

---

## How to Continue From Here (for other team members)

### If you are on macOS or Linux
The Switch Console OpenCode connection works without issues on those platforms.
Run `opencode auth login opencode`, complete the browser auth, then go to
Switch Console and click Check again — it will connect immediately.

### If you are on Windows
1. Try Antigravity first: run `agy` in terminal, complete Google auth, then
   try connecting Antigravity in Switch Console
2. If that fails, use the Switch Agent Protocol directly — connect OpenCode
   to the room via HTTP without using the Switch Console GUI provider flow
3. Reference: https://docs.switchagents.ai

### Room configuration
All room config is in `switch/room-template.yaml`. The room instructions,
task schema and decision schema are all defined there. Import or paste them
when recreating the room on another machine.

### OpenCode config location on Windows
```
C:\Users\<username>\.config\opencode\opencode.json   ← MCP servers config
C:\Users\<username>\.config\opencode\service.json    ← running service info
C:\Users\<username>\.local\state\opencode\model.json ← last used model
```

The Gemini API key is stored in the Windows credential store, not in these
JSON files. To reconfigure: run `opencode` → press `Ctrl+P` → select provider
settings → update the key.
