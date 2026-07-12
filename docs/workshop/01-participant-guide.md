# Participant guide — the Jira → PR loop

You'll run the same loop for every exercise. It's the loop from the talk, but this time *you're* driving. The point of the afternoon is not the Python — it's making this loop feel boring by the third repetition.

## The loop

```
ticket → context → plan → implement → verify → review → PR → close the loop
```

### 1. Pull the ticket

Open Copilot Chat in **agent mode** at the repo root and start from the ticket, not from the code:

> Pick up OPS-3 for me.

The repo's **jira skill** teaches the agent to fetch it with `acli jira workitem view OPS-3 --json --fields '*all'`, read the acceptance criteria, assign it to you, and move it to In Progress. If it doesn't reach for `acli`, nudge it: *"use the jira skill."*

You never open a browser. The ticket comes to you.

### 2. Reproduce (bug tickets)

Before any plan: make the agent run the repro command from the ticket and show you the wrong output. A bug you haven't seen is a bug you can't confirm fixed. For feature tickets, run the closest existing command instead so you know the "before".

### 3. Plan — and push back

Ask for a plan before code. Read it critically. **Push back on at least one thing, every time** — scope, approach, test strategy, anything. Two reasons: half of all agent failures are visible in the plan (cheaper to fix there than in a 400-line diff), and the habit of pushing back is the skill this workshop actually teaches. Then, and only then: go.

The plan should reference the ADRs (`docs/adr/`). If it proposes something an ADR forbids — a new dependency, printing outside `cli.py` — that's your first push-back.

### 4. Implement

Let the agent edit. Resist grabbing the keyboard when it stumbles; describe what's wrong instead and let it correct itself. You're reviewing intent, not typing speed.

### 5. Verify

```bash
pytest                       # green, including the NEW tests
schiphol-ops <repro command> # the ticket's command now shows the right thing
```

Bugs need a **regression test that fails on the old code** — ask the agent to prove that ("stash the fix and show the test failing" is a fair demand). Features need a test per acceptance criterion.

### 6. Review the diff

```bash
git diff
```

Walk through every hunk. You are the reviewer of record — anything you don't understand, you ask about *now*, not after merge. Watch for: drive-by refactors nobody ordered, deleted comments, test assertions weakened to pass.

### 7. Open the PR

The **github skill** covers this: branch `<ticket-key>-<slug>`, conventional commit with the key, `gh pr create` against **your fork's** `main` with the template body — `Closes` line, summary, checked-off ACs, test plan.

### 8. Close the loop

Comment the PR link on the Jira ticket and transition it (the jira skill knows how). Ticket read, code written, tests green, PR open, ticket updated — and you never left the terminal.

## Working with the repo's guardrails

This repo instructs your agent in four layers — worth reading once, since building this structure for your own repos is the take-home:

| Layer | File(s) | When it loads |
|-------|---------|---------------|
| Repo instructions | `.github/copilot-instructions.md` | every session |
| Path instructions | `.github/instructions/*.instructions.md` | when matching files are touched |
| Agent rules | `AGENTS.md` | agent-mode sessions |
| **Skills** | `.github/skills/{jira,github,adr}/SKILL.md` | on demand, when the task matches the skill's description |

Skills are the new part: procedures with a trigger description, loaded only when relevant. Say *"comment on the ticket"* and watch the jira skill wake up. Exercise 5 makes the adr skill earn its keep.

## Anti-patterns (a.k.a. how to have a bad afternoon)

- **Copy-pasting code between browser and IDE.** Give the agent the ticket key; context transfer is its job.
- **Accepting the first plan silently.** The plan is a draft, and you're the senior engineer in the pair. Act like it.
- **"It compiles, ship it."** Run the repro. Read the diff. The suite was green while three bugs sat in this codebase — let that sink in.
- **Fixing the data.** If editing `data/flights.json` makes the ticket "pass", you've falsified the evidence, not fixed the bug.
- **Bundling tickets.** One ticket, one branch, one PR. Reviewable beats impressive.

## Stuck?

1. Re-read the ticket — the answer is usually in the ACs or Notes.
2. Ask the agent to explain the failing behavior before asking it to fix it.
3. Wave. The host and floaters are there for exactly this.
