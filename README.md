# ShipDesk

**AI-Powered Client Request, Website Development and Deployment Desk**

> Hackathon: Flip the Switch · Track 01 – Best Business Workflow
> Team: The Beatles · Event: 4–7 November 2026

---

## What is ShipDesk?

ShipDesk lets a non-technical website owner request changes to their live
website using plain English in Discord. A team of four specialised AI agents
converts the request into a structured task, edits the code, reviews it,
collects an authenticated approval and ships the change to production –
all without the client touching Git or code.

**Core promise:** One Discord message → reviewed, approved, live on production.

---

## How it Works

```
Client message in Discord
        ↓
Intake Agent  →  structures request into a Switch task
        ↓
Builder Agent →  creates branch, edits code, opens PR
        ↓
QA Agent      →  independently reviews PR + preview URL
        ↓
Client        →  reviews preview, approves or rejects
        ↓
Deploy Agent  →  validates all conditions, merges PR
        ↓
Cloudflare Pages → production deployment
        ↓
Updated live website + completion notice in room
```

---

## Repository Structure

```
Shipdesk/
│
├── agents/
│   ├── intake/                  # Intake Agent (Python/Node – Phase 4)
│   ├── builder/
│   │   └── opencode-instructions.md   # Builder's OpenCode system prompt
│   ├── qa/
│   │   └── opencode-instructions.md   # QA's OpenCode system prompt
│   └── deploy/                  # Deploy Agent (Python/Node – Phase 4)
│
├── switch/
│   ├── room-template.yaml       # Switch room config (participants, schema)
│   ├── rules.md                 # 32 room rules across 8 categories
│   ├── SETUP.md                 # Step-by-step Phase 3 setup guide
│   └── agent-configs/
│       ├── intake.yaml          # Intake Agent Switch config
│       ├── builder.yaml         # Builder Agent Switch config
│       ├── qa.yaml              # QA Agent Switch config
│       └── deploy.yaml          # Deploy Agent Switch config
│
├── integrations/
│   ├── github/                  # GitHub token config (Phase 4)
│   ├── cloudflare/              # Cloudflare Pages config (Phase 4)
│   └── discord/                 # Discord bridge config (Phase 5)
│
├── demo-website/        # Demo website (FestiveKart)
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   ├── DESIGN.md
│   └── assets/
│       ├── images/banners/
│       ├── images/products/
│       └── images/brand/
│
├── tests/                       # Test scripts (Phase 7)
├── docs/                        # Architecture diagrams (Phase 8)
├── plan.md                      # Full project plan
└── README.md
```

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Switch (SandboxAQ) | Collaboration room, agent orchestration, shared history |
| OpenCode | Builder and QA coding agents |
| Discord | Client-facing interface |
| GitHub | Version control, branches, pull requests |
| Cloudflare Pages | Preview and production hosting |
| Python / Node.js | Intake and Deploy custom agents (Phase 4) |
| Docker Desktop | Runs the local Switch server |

---

## Phase Progress

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Build and deploy the FestiveKart demo website | ✅ Complete |
| 2 | GitHub workflow, pull requests and preview deployments | ✅ Complete |
| 3 | Install and configure Switch | ✅ Structure complete – follow `switch/SETUP.md` |
| 4 | Build and configure the four agents | 🔲 Next |
| 5 | Connect Discord to Switch | 🔲 Pending |
| 6 | Integrate the end-to-end workflow | 🔲 Pending |
| 7 | Security, testing and reliability | 🔲 Pending |
| 8 | Documentation, demo video and submission | 🔲 Pending |

---

## Getting Started (Phase 3)

Follow the step-by-step guide: [`switch/SETUP.md`](switch/SETUP.md)

**Short version:**
1. Install Docker Desktop and confirm it is running.
2. Download Switch Console from the [Switch GitHub releases](https://github.com/sandbox-quantum/switch/releases/latest).
3. Open Switch Console – it starts the local server automatically.
4. Connect OpenCode (Builder) and OpenCode (QA, different model) to the room.
5. Create room `shipdesk-client-project` using `switch/room-template.yaml`.
6. Send a test message and confirm both agents respond.

---

## Demo Website

FestiveKart is live at: **[update after Cloudflare deployment]**

It is the target website that ShipDesk manages. All agent changes go through
a PR → preview → approval → production pipeline on this site.

---

## Team

**The Beatles** – four-person hackathon team.

---

## License

See individual component licenses. Switch is Apache 2.0 + Commons Clause.
Project code is owned by the team.
