---
name: jira
description: Work with Jira tickets from the terminal using acli (Atlassian CLI). Use when the user mentions a ticket key (e.g. OPS-3), asks to pull ticket context, list their tickets, comment on a ticket, or transition a ticket's status.
---

# Jira via acli

Interact with Jira work items using `acli`. Never ask the user to open a browser for something these commands can do.

## Fetch a ticket (do this first)

When the user references a ticket key, pull the full ticket and treat it as the source of truth for scope and acceptance criteria:

```bash
acli jira workitem view <KEY> --json --fields '*all'
```

From the JSON, extract and echo back before planning:
1. **Summary** — what is being asked
2. **Type** — Bug (reproduce first!) or Story (implement ACs)
3. **Description** — repro steps for bugs, user story for features
4. **Acceptance criteria** — each bullet becomes a test later

## Recipes

| Action | Command |
|--------|---------|
| My open tickets | `acli jira workitem search --jql "assignee = currentUser() AND resolution = Unresolved"` |
| All tickets in a project | `acli jira workitem search --jql "project = <KEY> ORDER BY created ASC"` |
| View ticket (full JSON) | `acli jira workitem view <KEY> --json --fields '*all'` |
| View ticket (readable) | `acli jira workitem view <KEY>` |
| Assign to me | `acli jira workitem assign --key <KEY> --assignee "@me"` |
| Add a comment | `acli jira workitem comment create --key <KEY> --body "..."` |
| Transition status | `acli jira workitem transition --key <KEY> --status "In Progress"` |

## Workflow rituals

- When starting work on a ticket: assign it to yourself and transition it to **In Progress**.
- When the PR is open: comment on the ticket with the PR URL, then transition to **In Review** (or the closest status the project has — list options with `acli jira workitem transition --key <KEY>` if a status name is rejected).
- Multi-line comment bodies: write the text to a temp file and pass it with `--body "$(cat file.md)"`.

## Failure modes

- `acli` not authenticated → tell the user to run `acli jira auth login` themselves; do not attempt interactive login from the agent.
- Ticket key not found → the user may be in the wrong Jira project; ask which project their workshop tickets were seeded into (see `my-tickets.md` in the repo root if present).
- Jira unreachable → fall back to the matching markdown ticket in `docs/workshop/exercises/` and say you did so.
