# Setup — do this before the workshop

Everything below takes ~20 minutes. If you arrive with `./scripts/check-setup.sh` all green, you'll spend the workshop building instead of installing. Bring your questions to the first half hour — that block exists for setup stragglers.

## 1. Prerequisites

| Tool | What | Check |
|------|------|-------|
| IDE + Copilot | Your favorite IDE with the GitHub Copilot extension, **agent mode** available (VS Code, JetBrains, Neovim, …), signed in with an active Copilot subscription. Repo agent skills require a recent version — update your extension. | Copilot Chat opens and answers |
| Python | 3.11 or newer | `python3 --version` |
| git | any recent | `git --version` |
| GitHub CLI | [cli.github.com](https://cli.github.com) | `gh --version` |
| Atlassian CLI | [acli](https://developer.atlassian.com/cloud/acli/guides/install-acli/) — the `acli` binary | `acli --version` |
| Jira | A Jira Cloud site where **you can create a project** (a free personal site from [atlassian.com/try](https://www.atlassian.com/try) is perfect). No shared board is provided — everyone brings their own. | you can log in |

No Jira available at all? Everything also works with GitHub Issues on your fork — noted per step below.

## 2. Fork and clone

```bash
gh auth login                      # if you haven't already; pick HTTPS + browser
gh repo fork scholtenmartijn/schiphol-cop-workshop --clone
cd schiphol-cop-workshop
```

You'll do all work on **your fork** and open PRs against your fork's own `main`.

## 3. Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest                             # expect: all green
schiphol-ops departures            # expect: a departures board
```

Yes, the suite is green — the workshop bugs are *behavioral*. The tickets tell you how to see them.

## 4. Jira login

```bash
acli jira auth login               # follow the prompts (site URL + API token)
acli jira workitem search --jql "project is not empty" # any output = you're in
```

Create (or pick) a project for the workshop tickets — a throwaway **team-managed** project with key `OPS` is ideal. You can do that in the Jira UI in ~30 seconds.

## 5. Seed your tickets

```bash
./scripts/seed-jira.sh --project OPS
```

This creates the eight workshop tickets in *your* project and writes `my-tickets.md` mapping each exercise to your ticket keys. Verify:

```bash
acli jira workitem search --jql "project = OPS ORDER BY created ASC"
```

**Fallback without Jira:** `./scripts/seed-github-issues.sh` creates the same tickets as issues on your fork.

## 6. Self-check

```bash
./scripts/check-setup.sh
```

All green? You're done. Anything red tells you which step above to revisit.

## 7. After the workshop — clean up

- Delete the workshop project (or tickets) from your Jira site — it's your site, keep it tidy.
- Keep the fork if you want to reference it; otherwise `gh repo delete <you>/schiphol-cop-workshop`.
