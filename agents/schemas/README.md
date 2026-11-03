# ShipDesk Agent Schemas

JSON Schema definitions for the structured data exchanged between agents.

Every agent handoff uses one of these schemas. Agents must validate their
output against the relevant schema before posting to the Switch room.

## Schemas

| File | From → To | Description |
|------|-----------|-------------|
| `task.json` | Intake → Builder | Structured task with requirements, acceptance criteria, scope |
| `implementation_report.json` | Builder → QA | PR URL, commit SHA, files changed, self-check results |
| `qa_report.json` | QA → Room/Client | Independent review results tied to exact commit SHA, verdict |
| `approval_record.json` | Client → Deploy | Authenticated approval bound to task ID, PR number, commit SHA |

## Usage

```python
import json
from jsonschema import validate

with open("agents/schemas/task.json") as f:
    task_schema = json.load(f)

validate(instance=my_task_dict, schema=task_schema)
```

## Design principles

- **Commit SHA binding**: QA reports and approval records both reference the
  full 40-character commit SHA. A new commit invalidates the previous report
  or approval.
- **No free-text verdicts**: Acceptance criteria results are `pass` or `fail`
  with evidence strings — "looks good" is rejected.
- **Authenticated identity**: Approval records require `client_id` from an
  authenticated source, not a Discord display name.
- **Additional properties disabled**: Schemas reject unknown fields to catch
  accidental drift between agent versions.
