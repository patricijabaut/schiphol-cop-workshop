# AGENTS.md — agent-mode rules for this repo

This file is read by Copilot (and other agent-mode tools) at the start of a session. It defines which CLIs the agent may call and the ritual every change follows. Repo-wide behavior lives in [`.github/copilot-instructions.md`](./.github/copilot-instructions.md); per-path conventions in [`.github/instructions/`](./.github/instructions/); tool recipes in the skills under [`.github/skills/`](./.github/skills/).

## Allowed tools

The agent may invoke these without asking:

| Tool     | What for                                                            |
| -------- | ------------------------------------------------------------------- |
| `git`    | Read state, branch, stage, commit. Never `push --force`.            |
| `gh`     | Open and inspect PRs and issues — follow the **github** skill.      |
| `acli`   | Read, comment on, and transition Jira tickets — follow the **jira** skill. |
| `pytest` | Run the test suite.                                                 |
| `python` | Run the CLI for smoke checks and bug repros.                        |
| `pip`    | Only with `-e ".[dev]"` against this repo. No global installs.      |

Ask first before:

- Any `gh` action that merges or closes PRs, or deletes anything
- Any `git` command that rewrites history (`rebase`, `reset --hard`, `push --force`)
- Any `acli` action that creates or deletes projects, or bulk-edits tickets
- Installing anything outside the dev extra

## The ritual

Every ticket follows this loop:

1. **Read context** — pull the ticket via the **jira** skill; skim [`docs/adr/`](./docs/adr/) for decisions that bound the change.
2. **Reproduce** (bug tickets) — run the repro command from the ticket and confirm the broken behavior before touching code.
3. **Plan** — produce a plan grounded in the ticket and the ADRs. Surface assumptions. Wait for the user's go-ahead. If the change needs a decision or contradicts an ADR, write the ADR first via the **adr** skill.
4. **Implement** — edit existing files where possible; match the module split (`cli` / `models` / `data` / `filters` / `board` / `gates` / `stats`).
5. **Test** — run `pytest`. Bug fixes get a regression test; features get a test per acceptance criterion. Re-run the ticket's repro/demo command.
6. **Diff review** — show `git diff` and walk through it before staging.
7. **PR** — branch, commit, and open the PR via the **github** skill.
8. **Close the loop** — comment the PR link on the Jira ticket and transition it.

## Branch naming

`<ticket-key>-<slug>`, lowercase — for example `ops-1-destination-filter`.

## Python environment

The system Python may be externally managed. Always use a venv:

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
```

If `.venv` already exists, just activate it: `source .venv/bin/activate`.

## Data

Seed data lives in `data/flights.json` and `data/gates.json`; tests use the smaller set in `tests/fixtures/` via the `SCHIPHOL_OPS_DATA` environment variable. Don't edit seed data to make a bug disappear — fix the code.
