# Phase 3 – Switch Setup Guide

Step-by-step instructions to install Switch Console, connect OpenCode
and create the ShipDesk room. Follow every step in order.

---

## Prerequisites

| Requirement | Check |
|-------------|-------|
| Windows 10/11, macOS 12+, or Ubuntu 20.04+ | |
| 8 GB RAM minimum | |
| Docker Desktop installed and running | |
| Git installed | |
| OpenCode installed (`npm install -g opencode` or see opencode docs) | |
| A free LLM API key (Gemini free tier, OpenAI, Anthropic, or Ollama local) | |

---

## Step 1 – Install Docker Desktop

Docker is required to run the Switch server locally.

1. Go to [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Download the installer for your OS.
3. Run the installer and follow the prompts.
4. After install, open Docker Desktop and wait for the engine to show **Running**.
5. Verify in terminal:
   ```powershell
   docker --version
   docker ps
   ```
   Both commands should return output without errors.

> **Windows note:** Docker Desktop on Windows requires WSL 2.
> If prompted, follow the WSL 2 installation steps Docker shows you.

---

## Step 2 – Install Switch Console

Switch Console is the desktop app that runs and manages your Switch server
and lets you create rooms, add agents and connect chat platforms.

1. Go to [https://github.com/sandbox-quantum/switch/releases/latest](https://github.com/sandbox-quantum/switch/releases/latest)
2. Download the installer for your platform:

   | Platform | File to download |
   |----------|-----------------|
   | Windows | `Switch-Console-Setup-x.x.x.exe` |
   | macOS Apple Silicon | `Switch-Console-x.x.x-arm64.dmg` |
   | macOS Intel | `Switch-Console-x.x.x-x64.dmg` |
   | Linux x64 | `Switch-Console-x.x.x-x64.AppImage` or `.deb` |

3. Run the installer.
4. Open **Switch Console** – it will start the local Switch server automatically
   using Docker.
5. On first run, Switch Console shows the **switch-buddy** agent – your
   built-in assistant. It can create agents and rooms for you.
6. Switch Console will ask about telemetry. Disable it if you prefer.

> **Windows / Linux note:** These builds are currently labeled early access.
> The server itself (running on Linux inside Docker) is the primary deployment path.

---

## Step 3 – Connect OpenCode to the Switch Docs MCP Server

This lets OpenCode read the Switch documentation and help you configure things.

In your terminal, run:

```powershell
opencode mcp add
```

When prompted for the MCP server URL, enter:

```
https://docs.switchagents.ai/mcp
```

Now when you run OpenCode, it can answer questions about Switch setup by
reading the official docs directly.

---

## Step 4 – Configure OpenCode for the Builder Agent

Builder uses OpenCode with access to the repo. Set up its configuration:

1. Copy `agents/builder/opencode-instructions.md` – this is Builder's system
   prompt file.
2. In OpenCode's config, set:
   - Instructions file: `agents/builder/opencode-instructions.md`
   - Working directory: `demo-website/`
   - Model: your chosen provider (Gemini, Claude, GPT-4o, etc.)
3. Give Builder a GitHub token with these permissions only:
   - `contents: write` (for pushing branches)
   - `pull-requests: write` (for opening PRs)
   - `pull-requests: read`
   - **No** `merge` permission on main

---

## Step 5 – Configure OpenCode for the QA Agent

QA uses a **separate** OpenCode instance with a **different model** from Builder.
Using the same model risks QA simply agreeing with Builder. Independence matters.

1. Copy `agents/qa/opencode-instructions.md` – this is QA's system prompt file.
2. In OpenCode's config for the QA instance, set:
   - Instructions file: `agents/qa/opencode-instructions.md`
   - Working directory: `demo-website/`
   - Model: a different model than Builder's (e.g. if Builder uses Claude,
     QA uses Gemini, or vice versa)
3. Give QA a GitHub token with read-only PR permissions only:
   - `pull-requests: read`
   - `contents: read`
   - **No** write permissions

---

## Step 6 – Create the ShipDesk Room in Switch Console

1. Open Switch Console.
2. Click **New Room**.
3. Name it: `shipdesk-client-project`
4. Description: paste the description from `switch/room-template.yaml`.
5. In the **Instructions** field, paste the full `instructions` block from
   `switch/room-template.yaml`.
6. Add participants:
   - Add your Builder OpenCode agent (name: `builder`)
   - Add your QA OpenCode agent (name: `qa`)
   - Add yourself as `team`
   - (Intake and Deploy agents will be added in Phase 4)
7. Click **Create Room**.

---

## Step 7 – Send a Test Message

1. In the `shipdesk-client-project` room, send this message:

   ```
   @builder Hello! Please confirm you can read the repository and
   tell me how many sections are in the current index.html.
   ```

2. Wait for Builder to respond. A correct response lists the sections
   (header, category nav, hero carousel, featured products, etc.).

3. If Builder responds correctly: **Phase 3 is complete.**

4. If Builder does not respond or gives an error:
   - Check Docker Desktop is running
   - Check Switch Console shows the server as active
   - Check Builder's OpenCode config points to the right working directory
   - Check the API key is valid

---

## Step 8 – Verify QA Independence

Send a second test:

```
@qa Hello! Without looking at any Builder reports, please tell me
the file name and line count of style.css in the repository.
```

QA should respond with the correct file name and an approximate line count
by reading the file directly – not by referencing any Builder message.

---

## Exit Criteria for Phase 3

- [ ] Docker Desktop is installed and running
- [ ] Switch Console is installed and the local server is active
- [ ] OpenCode (Builder) is connected to the room and responds to messages
- [ ] OpenCode (QA) is connected with a different model and responds independently
- [ ] Room `shipdesk-client-project` exists with the project instructions loaded
- [ ] Builder can read files from `demo-website/`
- [ ] QA can read files from `demo-website/`

Once all boxes are checked, proceed to **Phase 4 – Build the Four Agents**.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Docker Desktop won't start | Enable WSL 2 on Windows; enable virtualisation in BIOS |
| Switch Console can't connect to server | Restart Docker Desktop; restart Switch Console |
| OpenCode doesn't respond in room | Check API key in OpenCode config; check model name is valid |
| Builder can't read repo files | Check working directory path in OpenCode config |
| Preview URL not generated | Check Cloudflare Pages PR preview is enabled (Phase 2 step) |
