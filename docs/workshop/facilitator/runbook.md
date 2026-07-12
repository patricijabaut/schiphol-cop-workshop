# Facilitator runbook

Host script for the 3.5–4 h workshop, ~20 participants. Companion files: [solutions.md](./solutions.md) (root causes, expected diffs, hints) and [slides-outline.md](./slides-outline.md) (intro deck).

## Before the day

- [ ] Announce [00-setup.md](../00-setup.md) to participants **at least a week ahead** — the Jira-site requirement ("a Jira Cloud site where you can create a project") is the one people discover too late.
- [ ] Recruit 1–2 floaters if possible; 20 people : 1 host is thin during self-paced blocks.
- [ ] Rehearse Exercise 1 end-to-end on a fresh fork, and the adr-skill demo for the 2:20 slot.
- [ ] Your own machine: fork cloned, venv green, `acli` + `gh` authenticated, tickets seeded in a demo project, `check-setup.sh` green.
- [ ] Room: projector tested with your terminal font size, wifi checked against Jira Cloud and GitHub.
- [ ] Have the markdown tickets open in a tab — they're the universal fallback when someone's Jira misbehaves.

## Timeline

### 0:00–0:20 — Welcome & talk: how this repo steers an agent

Deck from [slides-outline.md](./slides-outline.md). Core message: the demo talk showed the loop working; today everyone runs it, and the new depth is **how a repo teaches Copilot to behave** — four layers: repo instructions → path instructions → AGENTS.md → skills. Skills are the star: procedures with trigger descriptions, loaded on demand, versioned with the code (show ADR-0007 as the "why").

### 0:20–0:50 — Setup clinic

Everyone runs `./scripts/check-setup.sh`; put the fix-it order on screen (fork/clone → venv → gh → acli → seed). Floaters chase red ✗ lines. **Checkpoint 0:50: everyone has a green check or is consciously on the GitHub-issues fallback.** Fast finishers: point them at the participant guide and `docs/adr/`.

### 0:50–1:20 — Guided Exercise 1 (you drive, on screen)

Full loop, out loud, deliberately imperfect:

1. "Pick up <your OPS-1 key>" in Copilot Chat — let the **jira skill** fetch it; show the skill file afterwards so people see why that worked.
2. Reproduce: `schiphol-ops departures --destination london` → nothing. React like it's real.
3. Ask for a plan. **Push back on something visibly**, even if the plan is fine — narrate why that habit matters.
4. Implement, `pytest`, re-run repro (4 London flights now), demand the regression test *fail on the old code* (agent stashes fix, shows red, unstashes).
5. `git diff` walk-through, then the **github skill**: branch, commit, `gh pr create` on your fork. Comment the PR on the ticket, transition it.
6. The closer, same as the talk: *"Ticket read. Code written. Tests green. PR open, ticket updated — I never left the terminal."*

### 1:20–2:20 — Self-paced: Exercises 2–4

Announce: 2 and 3 are the bugs (do at least one), 4 is the feature breather; order free after that. Circulate — the [solutions](./solutions.md) hints are graded so you can unblock without spoiling. **Checkpoint 2:20: everyone has ≥1 merged-or-open PR; most have 2.** Anyone still fighting setup: pair them with a neighbour rather than losing them to config.

### 2:20–2:35 — Break + demo: the adr skill

Short, on screen, while people refill coffee: "Implement <OPS-5 key>" → watch the plan *stop* at "this needs ADR-0008 first" → let the adr skill draft it → tighten one sentence of the Consequences section live (ADRs are arguments, not paperwork). Don't finish the implementation — that's their Exercise 5.

### 2:35–3:30 — Self-paced: Exercises 5–6 + stretch

5 exercises the adr skill, 6 closes the Jira loop (the comment lands on **their** ticket — do a table-check that people actually run the `acli` comment step, it's the AC everyone forgets). Fast people: stretch A (builds on their Ex-3 fix) or stretch B (pairs, needs two open PRs — seed the pairing yourself).

### 3:30–3:55 — Show & tell + retro

Pick 2–3 PRs on the projector — ideally: one clean regression test (Ex 2/3), one ADR-0008 (compare two participants' different-but-valid decisions if you can — that's the best ADR teaching moment of the day), one delay-report comment sitting on a Jira ticket. Retro prompts: *Where did you push back on a plan and win? Where did the agent surprise you — both directions? Which skill would you copy into your team's repo on Monday?*

### 3:55–4:00 — Cleanup & close

- Jira: delete the workshop project (or bulk-delete tickets) — their site, their mess.
- Fork: keep as reference or `gh repo delete`.
- Take-home: the four-layer instruction structure and the three skills are MIT-licensed-in-spirit — copy them into your own repos and adapt.

## Checkpoints at a glance

| Time | Everyone should have |
|------|----------------------|
| 0:50 | green `check-setup.sh` (or conscious gh-issues fallback) |
| 1:20 | seen the full loop once, tickets seeded |
| 2:20 | ≥1 PR open on their fork |
| 3:30 | ≥2–3 PRs; Ex-5 people have an ADR-0008 |

## Recovery moves

| Symptom | Move |
|---------|------|
| Participant's Jira/acli won't cooperate | `./scripts/seed-github-issues.sh` on their fork; tickets are identical. Don't debug Jira for >5 min. |
| Copilot rate-limited / licence issues | Pair them with a neighbour — driver/navigator; swap on the next exercise. |
| Agent's plan is bad on stage | Say so and redo it — "that's the lesson" (it genuinely is). |
| Agent "fixes" a bug by editing `data/flights.json` | Point at AGENTS.md's last line on stage — best unplanned teaching moment available. |
| Tests fail after an implement step | Read the failure with the room. Ask Copilot to fix. Resist typing. |
| `gh pr create` flakes | `git push` and use the PR-URL hint from the push output in the browser; keep moving. |
| Someone finishes everything | Stretch A/B, then deputize them as a floater — teaching it is the best rep. |
| Wifi dies | Boards, gates, stats all work offline; Jira steps fall back to the markdown tickets; PRs queue up until it's back. |

## Room defaults worth saying out loud

- Terminal font ≥ 18 pt when anything is on the projector, yours included.
- "Wave, don't sink" — nobody should be stuck >10 minutes without a human.
- PRs stay open on forks; nothing merges to the upstream repo today.
