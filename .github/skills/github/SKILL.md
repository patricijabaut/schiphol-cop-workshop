---
name: github
description: Branch, commit, and open pull requests with the gh CLI following this repo's conventions. Use when work on a ticket is implemented and tested, or when the user asks to create a branch, open/inspect a PR, or check PR status.
---

# GitHub via gh

Ship reviewed work from ticket to pull request without leaving the terminal.

## Preconditions — check before opening a PR

1. `pytest` is green.
2. The manual repro/demo command from the ticket shows the intended behavior.
3. `git diff` has been shown to and confirmed by the user.
4. You are NOT on `main` (create the branch first if needed).

## Branch → commit → PR

```bash
# 1. Branch from main, named after the ticket
git checkout -b <ticket-key>-<slug>        # e.g. ops-1-destination-filter

# 2. Stage and commit with a conventional title + ticket key
git add -A
git commit -m "fix: match destination filter case-insensitively (OPS-1)"

# 3. Push and open the PR
git push -u origin <branch>
gh pr create --title "OPS-1: Destination filter misses every flight" --body-file /tmp/pr-body.md
```

Commit types: `feat:` new behavior · `fix:` bug fix · `test:` tests only · `docs:` docs/ADRs · `chore:` plumbing.

## PR body

Follow [`.github/pull_request_template.md`](../../pull_request_template.md): a `Closes <KEY>` line, a 1-2 sentence summary, the ticket's acceptance criteria as checked boxes, and a test plan (pytest + the manual command you ran). Write the body to a temp file and pass `--body-file` — don't fight shell quoting.

## Inspecting

| Action | Command |
|--------|---------|
| PR status of current branch | `gh pr status` |
| View a PR | `gh pr view <number>` (add `--web` to open the browser) |
| PR diff | `gh pr diff <number>` |
| List open PRs | `gh pr list` |
| Check CI | `gh pr checks <number>` |

## Rules

- One ticket = one branch = one PR. Don't bundle tickets.
- Never `git push --force`. Never commit directly to `main`.
- Never merge or close a PR unless the user explicitly asks.
- `gh` not authenticated → tell the user to run `gh auth login` themselves.
