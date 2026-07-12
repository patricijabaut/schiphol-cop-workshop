# Slide outline — intro talk (≈20 min) + adr-skill demo interstitial

Builds on the deck from the 15-min talk (`schiphol-cop-demo/presentation/`); slides 1–4 can be lifted from it almost unchanged, then the new material starts.

## Part 1 — Welcome (slides 1–4, ~5 min)

1. **Title** — *Jira → PR: this time you drive.* Name, handle, the workshop repo URL big.
2. **Last time, in 15 minutes** — one slide recap of the talk: the live demo GIF/screenshot, "ticket read, code written, tests green, PR open — never left the window."
3. **Today's contract** — agenda table (from README). You will: fix 3 real bugs, ship 2–3 features, open PRs from your terminal, and steal this repo's structure for your own team.
4. **The cast** — Copilot agent mode (any IDE) + `acli` + `gh` + a ~600-line Python CLI called `schiphol-ops`. Nobody needs to be a Python expert; the agent writes Python, you supervise engineering.

## Part 2 — How a repo steers an agent (slides 5–9, ~10 min) ← the new depth

5. **The problem** — an agent with no context is a very fast intern on their first day, forever. Prompting harder doesn't scale; *the repo itself* must carry the context.
6. **Four layers** — diagram of this repo:
   - `.github/copilot-instructions.md` — always on: policy ("plan first", "stdlib only", git rules)
   - `.github/instructions/*.instructions.md` — per-path: Python style loads for `.py`, test style for `tests/`
   - `AGENTS.md` — agent mode: allowed tools + the 8-step ritual
   - `.github/skills/` — on demand: procedures with trigger descriptions
   Each rule lives in exactly one layer (ADR-0004).
7. **Skills, up close** — anatomy of `SKILL.md`: frontmatter `name` + `description` (the *trigger*), body (the *procedure*). Show the jira skill: "you say 'pick up OPS-3', the description matches, the recipe loads." Key line: skills are **versioned with the code** — a broken recipe is a bug you fix by PR (ADR-0007).
8. **The three skills you'll use today** — jira (ticket in/out of the terminal), github (branch → templated PR), adr (decide before you code). Exercise 5 will refuse to let you code before the ADR exists — on purpose.
9. **ADRs in 60 seconds** — Status/Context/Decision/Consequences, append-only, supersede-don't-edit. "The agent reads `docs/adr/` before planning — so your past decisions steer today's diff."

## Part 3 — Launch (slides 10–12, ~5 min)

10. **The loop you'll repeat** — the 8 steps from the participant guide, one line each. Highlight step 3: *push back on every plan, every time* — that's the skill being trained.
11. **Ground rules** — one ticket = one branch = one PR (on your fork). Bugs: reproduce first, regression test that fails on old code. The suite is green *and* the code has 3 bugs — trust tickets, not tests.
12. **Go** — `./scripts/check-setup.sh` on screen; green → start the participant guide; red → hands up, floaters incoming.

## Interstitial deck — adr-skill demo (2:20, 2-3 slides or just live terminal)

- **Why stop and write?** The expensive agent failure isn't wrong code, it's right code implementing an undecided thing. ADR = the pushback artifact.
- **Live**: "Implement OPS-5" → plan halts at "ADR-0008 required" → adr skill drafts → you tighten the Consequences live → *don't* implement (that's their afternoon).
- **Take-home line**: "Instructions tell the agent how to behave. Skills tell it how *we* do things. ADRs tell it what we've already decided. All three are just files in the repo — start Monday."

## Wrap-up prompts (no slides needed, 3:30)

- Show 2–3 PRs: a regression test, two competing ADR-0008s, a delay-report comment on a Jira ticket.
- Retro: where did pushback win? where did the agent surprise you? which file do you copy into your repo on Monday?
- Cleanup slide: delete Jira project, optionally the fork; links to demo repo + this repo.
