# schiphol-cop-workshop

Hands-on workshop repository for the **Schiphol GitHub Copilot Community of Practice**: *from Jira ticket to pull request without leaving your IDE*. The sequel to the ["Jira to PR" talk](https://github.com/scholtenmartijn/schiphol-cop-demo) — this time, you drive.

You'll work on **`schiphol-ops`**, a Python CLI for Schiphol airside operations, fixing real (planted) bugs and shipping features the way the tickets describe them — with GitHub Copilot in agent mode, `acli` for Jira, and `gh` for GitHub.

## Start here

1. **[Setup](docs/workshop/00-setup.md)** — fork, clone, venv, `gh`/`acli` login, seed your tickets. *Do this before the workshop.*
2. **[Participant guide](docs/workshop/01-participant-guide.md)** — the Jira → PR loop you'll repeat all afternoon.
3. **[Exercises](docs/workshop/exercises/README.md)** — 3 bugs, 3 features, 2 stretch goals.

## Agenda (≈4 hours)

| Time | Block |
|------|-------|
| 0:00 | Welcome — Copilot customization: instructions, AGENTS.md, and **skills** |
| 0:20 | Setup clinic — everyone to a green `check-setup.sh` |
| 0:50 | Guided: Exercise 1 together, the full Jira → PR loop |
| 1:20 | Self-paced: Exercises 2–4 |
| 2:20 | Break + demo: the **adr skill** (intro to Exercise 5) |
| 2:35 | Self-paced: Exercises 5–6, stretch goals |
| 3:30 | Show & tell, retro, Q&A |
| 3:55 | Cleanup — your Jira project, your fork |

## The app

```
$ schiphol-ops departures --terminal D
DEPARTURES — Schiphol (AMS)

FLIGHT    DESTINATION         GATE    SCHEDULED    STATUS
KL1001    London (LHR)        D04     06:25        Departed
BA0431    London (LHR)        D59     09:40        Departed
KL1027    Manchester (MAN)    D07     13:20        Delayed +20m
...
```

```bash
schiphol-ops departures [--terminal D] [--status delayed] [--airline KL] [--destination CITY]
schiphol-ops arrivals   [--terminal E] [--status expected] [--airline KL] [--origin CITY]
schiphol-ops gates      [--pier F] [--conflicts]
schiphol-ops stats      [--by airline|terminal]
schiphol-ops search KL1001
```

Python 3.11+, stdlib only, `pytest` for tests. Install: `pip install -e ".[dev]"`.

> **Note:** the test suite is green, and yet this codebase ships three real bugs. The tickets know where. That's the exercise.

## Repo map

```
src/schiphol_ops/        the CLI (cli / models / data / filters / board / gates / stats)
data/                    one operational day: flights.json, gates.json
tests/                   pytest suite + small fixture dataset
docs/adr/                architecture decision records — agents read these first
docs/workshop/           setup, participant guide, exercises, facilitator material
scripts/                 check-setup.sh, seed-jira.sh, seed-github-issues.sh
.github/
  copilot-instructions.md    repo-wide Copilot behavior
  instructions/              per-path conventions (Python, tests)
  skills/                    ⭐ agent skills: jira, github, adr
AGENTS.md                agent-mode tool rules and the change ritual
```

## For facilitators

Runbook, per-exercise solutions, and the slide outline live in [`docs/workshop/facilitator/`](docs/workshop/facilitator/). Participants: reading the solutions ahead of time only ruins your own afternoon 🙂

## License / provenance

Flight data is fictional; any resemblance to actual delays at gate F07 is entirely intentional.
