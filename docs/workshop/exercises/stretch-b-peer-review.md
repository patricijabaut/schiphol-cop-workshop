# Stretch B — Review a neighbour's PR from the terminal

**Type:** Task
**Priority:** Low
**Components:** workflow
**Difficulty:** ★★☆ stretch · ~25 min
**Skills in play:** github ⭐

## Description

You've been opening PRs all afternoon; now sit on the other side. Pair up with a neighbour and review one of their open PRs on **their fork** — entirely from your terminal and IDE, with Copilot as your co-reviewer.

## Steps

1. `gh pr list --repo <neighbour>/schiphol-cop-workshop` — pick an open PR.
2. Pull the diff: `gh pr diff <number> --repo <neighbour>/schiphol-cop-workshop`.
3. Feed the diff and the corresponding exercise ticket to Copilot and ask for a review: does the change meet every acceptance criterion? Is there a regression test? Would the diff survive the ADRs?
4. Verify at least one Copilot finding yourself before repeating it — you sign the review, not the model.
5. Submit it: `gh pr review <number> --repo <neighbour>/... --comment --body-file review.md` (or `--approve` if it's genuinely clean).
6. Swap roles: address the review you received on your own PR and push the fix-up.

## Acceptance criteria

- [ ] A review with at least two substantive remarks (AC coverage, missing test, ADR conflict, naming — not typos) is posted on a neighbour's PR via `gh`.
- [ ] At least one remark you received on your own PR is addressed with a pushed commit.

## Notes

- Review tone: you're colleagues at the same airport tomorrow. Be specific, be kind.
- If Copilot's review contradicts an ADR or invents an acceptance criterion, that's worth calling out during the wrap-up — bring it.
