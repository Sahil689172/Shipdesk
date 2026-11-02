# SHIPDESK | PROJECT PLAN

SHIPDESK

AI-Powered Client Request, Website Development
and Deployment Desk

Detailed Project Plan and Phase-wise Implementation Guide

Hackathon: Flip the Switch
Target Track: Track 01 – Best Business Workflow
Team: The Beatles
Event dates: 4–7 November 2026

Project planning document

# Document Information

| Item | Details |

| --- | --- |

| Project name | ShipDesk |

| Project category | AI-powered business workflow / website maintenance automation |

| Primary hackathon track | Track 01 – Best Business Workflow |

| Team | The Beatles (four-person team) |

| Primary communication interface | Discord |

| Collaboration and orchestration | Switch |

| Coding agent | OpenCode |

| Repository and change management | GitHub |

| Preview and production hosting | Cloudflare Pages |

| Document purpose | Define the project scope, architecture, phases, deliverables, testing and hackathon alignment. |

# Table of Contents

1. Executive Summary

2. Problem Statement and Proposed Solution

3. Goals, Scope and Success Criteria

4. End-to-End Product Workflow

5. System Architecture and Technology Stack

6. Agent Responsibilities and Interaction

7. Phase-wise Development Plan

8. Four-Day Hackathon Execution Schedule

9. Team Roles and Responsibilities

10. Security, Permissions and Approval Controls

11. Testing and Acceptance Criteria

12. Hackathon Requirement Alignment

13. Risks, Dependencies and Scope Control

14. Final Submission Checklist

# 1. Executive Summary

ShipDesk is an AI-powered client request desk that allows a non-technical website owner to request website changes using plain English in a Discord channel. A coordinated team of specialised AI agents converts the request into a structured task, modifies the website code, reviews the change, prepares a preview, collects authenticated client approval and ships the approved change to the existing production website.

Switch is the collaboration and orchestration layer. It connects people and agents in a shared room containing messages, instructions, roles, tasks, decisions and history. OpenCode performs repository-level coding work. GitHub manages branches and pull requests. Cloudflare Pages hosts preview and production deployments.

Core promise: A client can request a website update in natural language, review the proposed result and approve its release without manually editing code or managing Git operations.

Important design principle: ShipDesk is not intended to be a generic chatbot. Its value is completing a real, auditable business workflow from request to production deployment.

# 2. Problem Statement and Proposed Solution

## 2.1 Problem statement

Small businesses and independent website owners often depend on a developer for routine website changes such as updating headlines, adding promotional banners, changing product information or fixing layout issues. The client may not understand source code, Git branches, pull requests, testing or deployment. The developer must interpret the request, implement it, verify it and publish it. This creates communication overhead and delays.

## 2.2 Proposed solution

ShipDesk provides a conversational interface in Discord backed by a Switch room. The client describes the desired change. The Intake Agent turns the request into clear acceptance criteria. The Builder Agent edits the website repository and opens a pull request. The QA Agent independently checks the code and preview. The client reviews the preview and explicitly approves or rejects it. The Deploy Agent verifies the required approvals and commit identity before allowing the pull request to be merged into the protected production branch.

## 2.3 Example client request

Client message in Discord:

"Please change the homepage headline to
'Big Diwali Sale – 40% OFF', add a festive
promotional banner and make sure it works
on mobile. Do not disturb the existing layout."

## 2.4 Expected result

A structured task is created with requirements and acceptance criteria.

The Builder Agent modifies the existing website repository.

A GitHub pull request and preview URL are produced.

The QA Agent reports evidence-based pass/fail results.

The client approval is authenticated and recorded.

The Deploy Agent validates the approvals and approved commit.

The production website is updated after the approved merge.

The final result and deployment status are reported in the Switch room and Discord.

# 3. Goals, Scope and Success Criteria

## 3.1 Primary goals

Allow non-technical clients to request website changes through Discord.

Use Switch as the central collaboration environment for humans and agents.

Use an existing coding agent, OpenCode, to make real repository changes.

Separate implementation, quality assurance and deployment responsibilities.

Provide a preview environment before production release.

Require authenticated client approval and successful QA before deployment.

Maintain a traceable history of requests, tasks, decisions, pull requests and deployments.

## 3.2 In-scope features for the hackathon

One demonstration website (FestiveKart) built with HTML, CSS and JavaScript.

One GitHub repository connected to Cloudflare Pages.

One Switch room connected to Discord.

Four specialised agents: Intake, Builder, QA and Deploy.

Git feature branches and pull requests.

Preview deployment for pull requests.

QA feedback and Builder retry loop.

Authenticated client approval and approval record.

Deploy Agent validation and production merge.

Deployment status notification.

## 3.3 Out of scope for the initial version

Supporting every website framework and arbitrary customer repository.

A full commercial multi-tenant SaaS dashboard.

Training a custom foundation model.

Autonomous production deployment without human approval.

Unrestricted access to customer repositories or hosting accounts.

Complex billing, subscriptions and enterprise identity management.

Large-scale production monitoring and guaranteed uptime.

## 3.4 Definition of success

The minimum successful product demonstration is one complete change cycle: a client sends a request in Discord; the request is handled in a Switch room; the Builder creates a pull request; QA reviews it; the client approves the matching commit; the Deploy Agent validates the approval; and the existing production website is updated through the normal GitHub-to-Cloudflare deployment pipeline.

# 4. End-to-End Product Workflow

## 4.1 High-level workflow

EXISTING LIVE WEBSITE
        |
        v
CLIENT SENDS REQUEST IN DISCORD
        |
        v
SWITCH ROOM
(messages, roles, rules, tasks, decisions, history)
        |
        v
INTAKE AGENT
(structures request and creates task)
        |
        v
BUILDER AGENT - OPENCODE
(edits repository, creates branch and pull request)
        |
        v
QA AGENT - OPENCODE
(reviews diff, runs checks and inspects preview)
        |
        +---- QA FAIL ----> BUILDER FIXES AND RESUBMITS
        |
        v
PREVIEW URL SHARED WITH CLIENT
        |
        +---- CLIENT REJECTS ----> BUILDER REVISES
        |
        v
CLIENT APPROVAL RECORDED
        |
        v
DEPLOY AGENT VALIDATES:
QA PASS + CLIENT IDENTITY + APPROVAL + COMMIT SHA
        |
        v
APPROVED PULL REQUEST MERGED TO PROTECTED MAIN
        |
        v
CLOUDFLARE PAGES PRODUCTION DEPLOYMENT
        |
        v
UPDATED LIVE WEBSITE + COMPLETION NOTICE

## 4.2 Detailed workflow stages

| Stage | Description |

| --- | --- |

| 1. Request | Client posts a plain-English request in the designated Discord channel. |

| 2. Intake | Intake Agent checks whether the request is understandable and in scope. It asks clarifying questions if needed. |

| 3. Task creation | Intake Agent creates a Switch task with a task ID, requirements, acceptance criteria and priority. |

| 4. Assignment | Builder Agent is assigned the task and receives the relevant repository and project context. |

| 5. Implementation | Builder creates a feature branch, edits files, runs checks, commits and pushes the branch. |

| 6. Pull request | Builder opens a PR and shares its URL, changed files, commit SHA and summary in the room. |

| 7. QA | QA reviews the diff, runs available checks, inspects the preview and maps results to acceptance criteria. |

| 8. QA failure loop | If QA fails, the report is sent to Builder. The next commit must be reviewed again. |

| 9. Preview | After QA passes, the preview URL and QA evidence are shared with the client. |

| 10. Client decision | An authenticated client approves or rejects the exact preview/commit. The decision is recorded. |

| 11. Deployment validation | Deploy Agent checks the PR, latest commit, QA result, client identity, approval and deployment state. |

| 12. Merge and release | Deploy Agent merges the approved PR through the protected workflow. Cloudflare Pages deploys the production branch. |

| 13. Completion | The room receives the deployment result, production URL and task completion status. |

# 5. System Architecture and Technology Stack

## 5.1 Architecture overview

CLIENT / HUMAN TEAM
       |
       v
DISCORD CHANNEL
       |
       v
SWITCH COLLABORATION BRIDGE
       |
       v
SWITCH ROOM
  | messages
  | instructions and rules
  | roles and agent identities
  | tasks and decisions
  | shared history
       |
       +------ Intake Agent (custom Python/Node)
       |
       +------ Builder Agent (OpenCode)
       |
       +------ QA Agent (OpenCode, separate model/config)
       |
       +------ Deploy Agent (custom Python/Node)
                       |
                       v
              GITHUB REPOSITORY
              branches / commits / PRs
                       |
                       v
              CLOUDFLARE PAGES
              preview and production

## 5.2 Technology stack

| Technology | Purpose |

| --- | --- |

| Switch Console | Runs and manages the Switch collaboration environment; hosts rooms and agent participation. |

| Docker Desktop / Docker Engine | Runs the local Switch infrastructure and supporting containers. |

| Discord | Client-facing and team communication interface. |

| OpenCode | Existing coding agent used by Builder and QA. |

| LLM providers | Provide model inference for OpenCode and custom agents. Select currently available free-tier models and verify limits. |

| Python or Node.js | Used to implement Intake and Deploy agents using the documented Switch agent protocol. |

| Git and GitHub | Version control, feature branches, commits, pull requests and permission controls. |

| Cloudflare Pages | Hosts the live demonstration site and pull-request previews. |

| Playwright or browser testing tool | Optional automated browser checks for desktop and mobile layouts. |

| OBS Studio | Records the final demonstration video. |

| Dev.to or Hashnode | Optional blog publication for the Best Blog side competition. |

## 5.3 Website hosting model

The project begins with a simple website already deployed to Cloudflare Pages and connected to GitHub. The production branch (normally main) represents the live website. The Builder Agent works on a separate feature branch. A pull request triggers a preview deployment. The client reviews that preview. After approval, the PR is merged into the protected production branch, which triggers the production deployment.

Important: The website does not need to be an existing third-party commercial website. The team can build and deploy its own demonstration website first. This gives the team permission and control over the repository and hosting configuration.

## 5.4 Suggested repository structure

ShipDesk/
|
|-- agents/
|   |-- intake/
|   |   |-- main.py
|   |   |-- prompts.py
|   |   |-- task_schema.py
|   |
|   |-- builder/
|   |   |-- opencode-instructions.md
|   |
|   |-- qa/
|   |   |-- opencode-instructions.md
|   |
|   |-- deploy/
|       |-- main.py
|       |-- approval.py
|       |-- github_merge.py
|
|-- switch/
|   |-- room-template.yaml
|   |-- rules.md
|   |-- agent-configs/
|
|-- integrations/
|   |-- github/
|   |-- cloudflare/
|   |-- discord/
|
|-- demo-website/
|   |-- index.html
|   |-- style.css
|   |-- script.js
|   |-- assets/
|
|-- tests/
|-- docs/
|-- .env.example
|-- README.md
|-- requirements.txt

# 6. Agent Responsibilities and Interaction

## 6.1 Intake Agent

Implementation: Custom Python or Node.js agent using an LLM and the Switch agent protocol.

Responsibilities:

Receive client requests from the Switch room.

Identify requested pages, components and changes.

Detect ambiguity and ask the client for clarification.

Convert the request into structured requirements.

Create a Switch task with acceptance criteria and priority.

Assign the task to Builder and post a concise summary.

Expected output: Task ID, title, requirements, acceptance criteria, scope, priority and status.

## 6.2 Builder Agent

Implementation: OpenCode with a coding model and controlled access to the demo repository.

Responsibilities:

Read the assigned task and repository instructions.

Inspect the existing project before editing.

Create a uniquely named feature branch.

Modify only files needed for the request.

Run build, lint or basic tests available for the project.

Commit and push the branch.

Open a pull request with summary, changed files and test results.

Report the PR URL and commit SHA to the Switch room.

Expected output: Feature branch, code changes, commit SHA, pull request URL and implementation summary.

## 6.3 QA Agent

Implementation: A separate OpenCode agent configuration, preferably using a different model from Builder.

Responsibilities:

Read the task and acceptance criteria.

Inspect the PR diff independently.

Check for unintended changes and obvious regressions.

Run available automated tests.

Open the preview URL and inspect relevant pages.

Check desktop and mobile layouts where feasible.

Record evidence and map each criterion to pass/fail.

Return precise findings to Builder or report QA pass.

Expected output: Structured QA report with PR number, commit SHA, criterion results, test evidence, defects and final pass/fail status.

## 6.4 Deploy Agent

Implementation: Custom Python or Node.js agent with narrowly scoped GitHub permissions.

Responsibilities:

Receive a deployment request after QA and client review.

Read the authoritative QA result.

Verify the client is authenticated and authorised.

Verify approval is for the exact PR and commit SHA.

Check that the PR remains open and has not changed since approval.

Check required branch protections and merge conditions.

Merge only when every condition passes.

Monitor the deployment result and notify the room.

Expected output: Deployment decision, merge result, deployment status and production URL.

## 6.5 Agent handoff contract

Agents should exchange structured, task-linked information rather than relying only on conversational statements. Every handoff should include the task ID and relevant artifact identifiers.

| Handoff | Required information |

| --- | --- |

| Intake → Builder | Task ID, requirements, acceptance criteria, repository identifier, priority and any clarifications. |

| Builder → QA | Task ID, PR number and URL, branch, commit SHA, changed files, build/test results and preview URL if available. |

| QA → Builder (failure) | Task ID, reviewed commit SHA, failed criteria, reproduction steps, evidence and requested corrections. |

| QA → Client | Task ID, PR number, reviewed commit SHA, preview URL, QA result and known limitations. |

| Client → Deploy | Authenticated approval or rejection tied to the task, PR and commit SHA. |

| Deploy → Room | Validation result, merge result, deployment status, production URL and any failure details. |

# 7. Phase-wise Development Plan

The project should be built incrementally. Each phase has a concrete output and an exit criterion. The team should not proceed to complex multi-agent automation until the preceding infrastructure has been tested.

# Phase 1 – Build and Deploy the Demonstration Website

Objective: Create a small but realistic website that acts as the client’s existing production website and gives the Builder Agent a controlled repository to modify.

## What to build

Create a fictional e-commerce brand called FestiveKart.

Use plain HTML, CSS and JavaScript to keep the codebase easy for a coding agent to understand.

Include a navbar, hero headline, product cards, pricing/deals section, promotional banner area, about section and footer.

Make the site responsive on desktop and mobile.

Use assets that the team is allowed to use.

## Implementation steps

Create a GitHub repository named shipdesk-festivekart.

Create index.html, style.css, script.js and an assets directory.

Implement the initial website and test it locally.

Push the code to GitHub.

Create a Cloudflare Pages project and connect the GitHub repository.

Deploy the production branch and record the public URL.

Confirm that a commit to the production branch triggers a new production deployment.

## Deliverables

- FestiveKart website source code.

- GitHub repository.

- Public production URL.

- Responsive layout and working navigation.

## Exit criteria

A public website is live and the team can update it through a normal GitHub commit and deployment.

## Important considerations

Keep the initial website small; complex components increase the chance of coding-agent errors.

Do not use a third-party website without permission. The team-owned demo website is the safest option.

# Phase 2 – GitHub Workflow, Pull Requests and Preview Deployments

Objective: Establish the safe code-delivery path that the Builder, QA and Deploy agents will use.

## What to build

A protected production branch named main.

Feature branches for individual client requests.

Pull requests as the review and approval unit.

Preview deployments for pull requests.

Automated production deployment after an approved merge.

## Implementation steps

Configure Cloudflare Pages to build from the GitHub production branch.

Enable pull-request preview deployments and verify the generated preview URL.

Define a branch naming convention such as feature/SD-001-diwali-banner.

Create a test feature branch manually and make a small website change.

Open a pull request and confirm that a preview deployment is produced.

Protect main and configure required checks or review conditions where available.

Merge the test PR manually and confirm the production URL updates.

## Deliverables

- Verified GitHub-to-Cloudflare integration.

- Feature branch and pull-request process.

- Working preview URL for a PR.

- Working production deployment from main.

- Documented repository permissions.

## Exit criteria

A manually created pull request produces a preview, and merging it updates the existing production website.

## Important considerations

The Builder should not have permission to merge into main.

Preview and production URLs must be clearly distinguished.

The exact Cloudflare preview behaviour depends on the Pages project and Git integration settings; test it before building automation.

# Phase 3 – Install and Configure Switch

Objective: Set up Switch as the central collaboration environment and prove that an existing AI agent can join and work in a room.

## What to build

Switch Console and its local server.

Docker Desktop or Docker Engine.

One working OpenCode agent.

A ShipDesk room with project instructions and initial roles.

## Implementation steps

Install Docker and confirm the Docker engine is running.

Download and install the official Switch Console release for the team's operating system.

Start the local Switch server using the official quickstart.

Follow the official provider onboarding steps to connect OpenCode.

Create a room named shipdesk-client-project.

Add a concise room description and shared project instructions.

Send a test message and confirm that the OpenCode agent responds in the room.

Read the official agent protocol and room documentation before implementing custom agents.

## Deliverables

- Switch Console installed and running.

- Docker runtime working.

- OpenCode connected as an agent.

- ShipDesk room created.

- Successful test conversation in the room.

## Exit criteria

A human can send a message in the Switch room and receive a response from the connected OpenCode agent.

## Important considerations

Switch provides collaboration infrastructure; it does not provide the coding agent or model itself.

Use the current official Switch documentation and release instructions. Do not assume configuration keys or protocol fields from examples without checking the installed version.

# Phase 4 – Build and Configure the Four Agents

Objective: Create specialised agents with clear responsibilities, structured handoffs and controlled tool access.

## What to build

Intake Agent implemented as a custom protocol-compatible agent.

Builder Agent configured through OpenCode.

QA Agent configured independently, preferably with a different model.

Deploy Agent implemented as a custom protocol-compatible agent.

## Implementation steps

Define JSON schemas for tasks, implementation reports, QA results and approval records.

Implement Intake so it can clarify requests, create structured tasks and assign Builder.

Configure Builder with repository instructions, branch naming, allowed tools and PR requirements.

Configure QA with independent review instructions and read-only repository access.

Implement QA reporting tied to the exact commit SHA.

Implement Deploy with read/merge permissions only as needed and no general-purpose unrestricted access.

Connect custom agents through the documented Switch agent protocol.

Test each agent individually before testing the full chain.

## Deliverables

- Four named agents with distinct responsibilities.

- Task and handoff schemas.

- Agent instructions and configuration.

- A test task that produces a PR and QA report.

- Deploy Agent validation logic tested without production merging.

## Exit criteria

The agents can participate in the Switch room and complete a manually initiated task-to-PR-to-QA workflow.

## Important considerations

Do not create custom agents as standalone Discord bots that bypass Switch.

Use the exact protocol and event/message format documented by Switch.

A separate model does not guarantee independent QA; also give QA a separate role, read-only access and explicit review criteria.

# Phase 5 – Connect Discord to Switch

Objective: Make Discord the client-facing interface while preserving Switch as the shared collaboration room and workflow environment.

## What to build

A Discord server for ShipDesk.

A designated client request channel.

The supported Switch Discord bridge or integration.

Human and agent identities visible in the connected room.

## Implementation steps

Create a Discord server named ShipDesk Workspace.

Create an initial channel such as #client-requests.

Follow the official Switch collaboration bridge instructions to connect Discord.

Map the designated Discord channel to the ShipDesk Switch room.

Verify that client messages arrive in the room and agent responses appear back in the channel.

Test mentions, replies and thread behaviour supported by the bridge.

Restrict who can submit requests and who is recognised as the client approver.

## Deliverables

- Discord server and channel.

- Working Discord-to-Switch bridge.

- Verified human-to-agent communication.

- Authenticated client identity/role mapping.

## Exit criteria

A client can submit a request in Discord and the Intake Agent can respond through the connected Switch room.

## Important considerations

Use the official supported bridge rather than building a separate bot that duplicates Switch functionality.

A Discord display name or typed message saying 'approved' is not sufficient authentication for production deployment.

# Phase 6 – Integrate the End-to-End Workflow

Objective: Connect the agents, GitHub, preview hosting and approval process so a Discord request can result in an approved production update.

## What to build

Automated request-to-task creation.

Builder-to-QA handoff.

QA failure and retry loop.

Preview URL delivery.

Authenticated client approval.

Deploy validation and controlled merge.

Production deployment notification.

## Implementation steps

Connect Intake task creation to the Builder assignment.

Pass task ID, repository details and acceptance criteria to Builder.

Have Builder create a feature branch, commit changes and open a PR.

Capture PR number, branch, commit SHA and preview URL.

Assign QA and require its report to identify the exact commit reviewed.

If QA fails, send evidence and corrections to Builder and require a new review.

If QA passes, send the preview URL and report to the authenticated client.

Record client approval or rejection as a Switch decision and in a machine-verifiable approval record.

Bind approval to task ID, PR number and commit SHA.

Have Deploy re-check all conditions immediately before merge.

Merge through the protected GitHub workflow and monitor Cloudflare deployment.

Report the final production URL and deployment status in the room.

## Deliverables

- Connected request-to-deployment workflow.

- QA retry loop.

- Preview and approval process.

- Commit-bound approval record.

- Deploy Agent validation and merge.

- Final deployment notification.

## Exit criteria

One Discord request can update the existing production website without a human manually editing files or merging the pull request.

## Important considerations

The client must approve the exact version they previewed.

Any new commit after QA or client approval invalidates the old approval and requires re-review.

Use GitHub branch protection and token permissions as enforcement; Switch room rules alone are not a security boundary.

Do not allow the Builder to merge or deploy directly.

# Phase 7 – Security, Testing and Reliability

Objective: Prove that the workflow handles errors, rejects unauthorised actions and protects the production website.

## What to build

Happy-path tests.

QA failure and retry tests.

Client rejection tests.

Unauthorised approval tests.

Stale commit and duplicate deployment tests.

Deployment failure reporting.

## Implementation steps

Test a valid client request from Discord through production deployment.

Introduce a deliberate visual or functional defect and confirm QA rejects it.

Confirm Builder receives QA feedback and creates a new commit.

Reject a preview as the client and confirm deployment is blocked.

Attempt approval from an unauthorised Discord user and confirm it is rejected.

Change the PR after approval and confirm stale QA/client approval is invalidated.

Submit the same deployment request twice and confirm the operation is idempotent.

Simulate a failed deployment and verify the room receives an accurate failure status.

Review all API tokens, secrets and repository permissions.

## Deliverables

- Test results and evidence.

- Permission matrix.

- Verified approval validation.

- Verified retry and rejection paths.

- Documented limitations and recovery process.

## Exit criteria

The team can demonstrate both a successful release and at least one safely blocked or rejected release.

## Important considerations

Keep production credentials out of prompts, source code and Discord messages.

Use minimum required token permissions and rotate any exposed credentials.

Do not claim rollback or monitoring capabilities unless they are implemented and tested.

# Phase 8 – Documentation, Demo and Submission

Objective: Package the working product so judges can understand, run and evaluate the workflow.

## What to build

Project README.

Architecture and workflow diagrams.

Setup instructions.

Screenshots and demo video.

Clear explanation of Switch usage.

Submission to the selected hackathon track.

## Implementation steps

Write the problem statement and product overview.

Explain why Switch is central to the project and how the room, roles, rules, tasks, decisions and history are used.

Document each agent's responsibilities and handoff contracts.

Document installation, configuration and environment variables without exposing secrets.

Add screenshots of the Switch room, Discord workflow, PR, QA report, preview and production site.

Record a three-to-five-minute end-to-end demonstration.

Test setup instructions on a clean environment if time allows.

Submit the project before the official deadline.

## Deliverables

- Complete README.

- Architecture diagram.

- Setup and usage guide.

- Demo video.

- Screenshots and evidence.

- Final hackathon submission.

## Exit criteria

A reviewer can understand the product, see Switch being used meaningfully and watch a complete real website change being shipped.

## Important considerations

The organisers' exact submission form, team rules, project eligibility and deadlines should be checked on the official event page.

Do not present planned features as completed features in the README or demo.

# 8. Four-Day Hackathon Execution Schedule

| Period | Priority and expected outcome |

| --- | --- |

| Before event | Prepare FestiveKart website, GitHub repository, hosting, developer tools and technical familiarity. Do not assume the hackathon workflow may be pre-built; follow event rules. |

| Day 1 – Nov 4 | Verify website and preview deployments; install/start Switch; connect OpenCode; create the room; prove one agent responds. |

| Day 2 – Nov 5 | Implement Intake; configure Builder and QA; build task and handoff schemas; produce a real PR and QA report. |

| Day 3 – Nov 6 | Connect Discord bridge; implement client approval; complete Deploy Agent; merge approved PR; verify production deployment. |

| Day 4 – Nov 7 | Run end-to-end and failure tests; fix critical bugs; finalise README and video; submit before the official deadline. |

# 9. Team Roles and Responsibilities

Suggested ownership for a four-person team. Team members should coordinate interfaces and help with integration rather than working in isolation.

Shared responsibility: All four members should understand the complete request-to-production workflow and participate in integration testing and the final demonstration.

# 10. Security, Permissions and Approval Controls

ShipDesk can modify and publish a live website. Therefore, it must treat repository permissions, client identity and approval validation as security-critical.

## 10.1 Permission matrix

| Actor | Allowed actions | Restricted actions |

| --- | --- | --- |

| Client | Submit requests; review preview; approve or reject | Cannot directly merge or deploy |

| Intake Agent | Read request; create task; ask questions; assign work | Cannot modify repository or deploy |

| Builder Agent | Read repository; create feature branch; commit and push branch; open PR | Cannot merge to production or change deployment credentials |

| QA Agent | Read repository and PR; run tests; inspect preview; publish QA result | Cannot write or merge production code |

| Deploy Agent | Read approval records; verify status; merge approved PR using limited permission | Cannot bypass required checks or approve on behalf of client |

| Human maintainer | Manage configuration and intervene in failures | Must follow documented release controls |

## 10.2 Mandatory deployment conditions

DEPLOYMENT IS ALLOWED ONLY IF:

1. The PR is open and targets the protected production branch.
2. QA has passed for the latest commit SHA.
3. The client is authenticated and authorised.
4. Client approval refers to the same task, PR and commit SHA.
5. No new commit has been added after approval.
6. Required GitHub checks and branch protections pass.
7. The task has not already been deployed.

Otherwise:
BLOCK DEPLOYMENT AND REPORT THE REASON.

## 10.3 Approval record

{
  "task_id": "SD-001",
  "pull_request_number": 12,
  "commit_sha": "full-commit-sha",
  "qa_status": "passed",
  "qa_commit_sha": "full-commit-sha",
  "client_id": "authenticated-client-id",
  "client_approval": true,
  "approval_timestamp": "ISO-8601 timestamp",
  "deployment_status": "pending"
}

The record above is illustrative. The implementation must use authenticated identities, durable storage and server-side validation. A plain Discord message, username or agent-generated claim is not by itself sufficient proof of approval.

# 11. Testing and Acceptance Criteria

| Test case | Test action | Expected result |

| --- | --- | --- |

| Valid request | Client submits a clear change request. | Intake creates a task with correct requirements. |

| Ambiguous request | Client omits important details. | Intake asks a clarifying question; no coding begins prematurely. |

| Builder success | Builder receives a valid task. | Feature branch and PR are created; commit SHA is reported. |

| Builder failure | Build or validation fails. | Builder reports the failure; QA/deploy cannot treat it as a pass. |

| QA rejection | A deliberate defect is introduced. | QA reports the defect and sends it back to Builder. |

| QA pass | All acceptance criteria pass. | QA report is tied to the reviewed commit SHA. |

| Client rejection | Client rejects preview. | Task returns for revision; Deploy is blocked. |

| Unauthorised approval | Non-client user attempts approval. | Approval is rejected and recorded. |

| Stale approval | A new commit is pushed after approval. | Previous QA and client approvals are invalidated. |

| Duplicate deploy | Same task is submitted for deployment twice. | Second attempt does not create an unintended second merge/deployment. |

| Production release | All checks and approvals pass. | PR merges and Cloudflare production deployment completes. |

| Deployment failure | Hosting deployment fails. | Failure is reported; task is not falsely marked complete. |

# 12. Hackathon Requirement Alignment

The project is designed for Track 01 – Best Business Workflow because it helps a business owner and AI agents complete a practical business task: changing and publishing a website.

| Hackathon expectation | How ShipDesk addresses it |

| --- | --- |

| Use an existing AI agent | OpenCode is connected as the Builder and QA coding agent. |

| Connect through Switch | Switch Console and the documented agent protocol connect agents to a shared room. |

| Use a team communication platform | Discord is the client-facing chat interface connected through the Switch bridge. |

| Human and agent collaboration | The client submits requirements and approves the exact preview/commit; agents perform specialised work. |

| Complete real work | The system modifies a repository, creates a PR, tests the change and updates a live website. |

| Use Switch meaningfully | Room context, instructions, roles, tasks, decisions, history and agent handoffs coordinate the workflow. |

Track recommendation: Track 01 – Best Business Workflow. ShipDesk is a practical workflow for website owners and small businesses.

Judging emphasis: Demonstrate that Switch is central to the collaboration and task lifecycle. Do not use Switch only as a message relay or decorative chat interface.

## 12.1 Optional side competitions

Best Blog: publish a technical article describing the problem, architecture, Switch integration, implementation and lessons learned.

Code with Wispr: use Wispr Flow for prompts, instructions and documentation during development, then submit the required usage scorecard.

Best Core Contribution: separately select an issue labelled hackathon, request assignment and submit a meaningful pull request. A ShipDesk product feature does not automatically count as a core contribution.

Eligibility note: The project team should verify the official rules for multiple track entries, separate project submissions and team eligibility directly with the organisers.

# 13. Risks, Dependencies and Scope Control

| Risk | Priority | Mitigation |

| --- | --- | --- |

| Switch setup takes longer than expected | High | Start with the official quickstart and one OpenCode agent before custom agent work. |

| Custom agent protocol integration is misunderstood | High | Read current protocol docs and examples; implement one custom agent first. |

| OpenCode model/API limits | Medium | Test provider quotas early and keep a fallback model/provider configuration. |

| Builder makes incorrect edits | High | Use a small website, clear acceptance criteria, feature branches and QA. |

| QA misses a defect | High | Combine diff review, automated checks and preview inspection; report limitations honestly. |

| Discord identity is not securely mapped | High | Use authenticated client identity and server-side role mapping; do not trust display names. |

| Approval becomes stale after a new commit | High | Bind approvals to full commit SHA and invalidate them when code changes. |

| Deploy Agent has excessive permissions | High | Use minimum required GitHub permissions and protected branch rules. |

| Preview deployment is unavailable or misconfigured | Medium | Verify Cloudflare PR preview behaviour in Phase 2 before agent automation. |

| Four-day scope becomes too large | High | Prioritise one website, one Discord room, four agents and one complete request-to-production path. |

## 13.1 Minimum viable product versus stretch goals

| MVP – Must complete | Stretch goals – Only after MVP works |

| --- | --- |

| One deployed demo website | Support multiple client websites |

| One Switch room connected to Discord | Separate room per client/project |

| Intake, Builder, QA and Deploy responsibilities | Additional project manager or security agent |

| GitHub branch and PR creation | Automated changelog and release notes |

| QA result and preview URL | Visual before/after comparison |

| Authenticated client approval | Client-facing dashboard |

| Approval-gated production merge | Rollback automation |

| Completion notification | Analytics and usage reporting |

# 14. Final Submission Checklist

- FestiveKart is deployed and accessible through a public URL.

- The website source is available in the team's GitHub repository.

- GitHub pull requests create preview deployments.

- Merging an approved PR updates production.

- Switch Console is installed and running.

- OpenCode is connected to Switch.

- The ShipDesk room contains instructions and configured agent identities.

- Discord is connected through the supported Switch bridge.

- Intake Agent creates structured tasks.

- Builder Agent creates a branch, commits changes and opens a PR.

- QA Agent reviews the correct commit and reports evidence.

- QA failure returns work to Builder.

- The client can inspect a preview and approve or reject it.

- Client approval is authenticated and recorded.

- Deploy Agent verifies QA, client approval and commit identity.

- Builder cannot merge into production.

- Approved PR merges and production deployment is verified.

- Failure and rejection paths are demonstrated.

- README explains the problem, architecture, Switch usage and setup.

- Demo video shows the complete workflow.

- All secrets are excluded from source code and public documentation.

- The final submission follows the current official hackathon rules.

# Conclusion

ShipDesk is designed to demonstrate how existing AI agents can become productive teammates in a real business workflow. A client describes a website change in Discord; Switch provides the shared collaboration environment; specialised agents handle intake, implementation, review and deployment; GitHub manages the code lifecycle; and Cloudflare Pages publishes the approved result.

The project's strongest demonstration is a complete, verifiable request-to-production cycle on a website that the team owns and controls. The team should prioritise a reliable end-to-end workflow, meaningful Switch usage, authenticated human approval and clear evidence over adding many optional features.

# Reference Links

Switch documentation: https://docs.switchagents.ai/

Switch GitHub repository: https://github.com/sandbox-quantum/switch

Flip the Switch Hackathon resources: https://www.wemakedevs.org/hackathons/switch/resources

OpenCode: https://opencode.ai/

Cloudflare Pages documentation: https://developers.cloudflare.com/pages/

GitHub pull requests documentation: https://docs.github.com/en/pull-requests

Docker Desktop: https://www.docker.com/products/docker-desktop/
