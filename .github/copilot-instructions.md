# Copilot — repository instructions

These instructions apply to every Copilot session in this repo. They describe how Copilot should collaborate on changes, regardless of language or folder.

## What this repo is

`schiphol-ops` — a Schiphol airside operations CLI (departures, arrivals, gates, stats, search). It is the hands-on codebase for the **"Jira to PR" workshop** at the Schiphol GitHub Copilot Community of Practice. Participants pull a ticket from Jira, implement it with Copilot, and open a PR — end to end from the IDE.

## How to work

- **Plan before code.** Start every non-trivial change with a plan. Read the plan back to the user before editing files. Tighten the plan instead of arguing with a 400-line diff.
- **Pull ticket context first.** When the user references a Jira ticket, use the **jira skill** (`.github/skills/jira/`) to fetch it via `acli` and treat the ticket JSON as the source of truth for scope and acceptance criteria.
- **Read the ADRs first.** Skim [`docs/adr/`](../docs/adr/) before non-trivial work. If your change contradicts an existing ADR, use the **adr skill** (`.github/skills/adr/`) to write a superseding record *before* writing code.
- **Reproduce before fixing.** For bug tickets, run the repro command from the ticket and confirm the broken behavior before touching code. After the fix, run it again and add a regression test that would have caught the bug.
- **Edit existing files** instead of creating new ones unless a new module is genuinely warranted. Match the module split: `cli.py` (argparse + print), `models.py` (dataclasses), `data.py` (loading), `filters.py` (selection), `board.py` (rendering), `gates.py` (occupancy), `stats.py` (aggregates).
- **Keep the runtime stdlib-only.** No new runtime dependencies without explicit approval. `pytest` is the only allowed dev dependency.
- **Be terse.** Short replies, short comments, no narration.

## Git & PR policy

Branching, commits, and PRs follow the **github skill** (`.github/skills/github/`). In short:

- Branch from `main`, named `<ticket-key>-<slug>` (e.g. `ops-1-destination-filter`).
- Conventional commit titles: `feat: …`, `fix: …`, `docs: …`, `test: …`, `chore: …` — with the ticket key in the message.
- PR title: `<TICKET-KEY>: <short summary>`. PR body follows [`.github/pull_request_template.md`](./pull_request_template.md).
- Run `pytest` and confirm green before opening a PR.
- Never `git push --force`. Never commit secrets, credentials, or `.env` files.

## Safety

- Do not bypass branch protection (`gh pr merge --admin`, `--force`, etc.).
- Do not run destructive `git` commands (`reset --hard`, `clean -fdx`) without explicit confirmation.
- If a tool is missing on the host, surface it — do not silently install global packages.
