# Stretch A — Suggest a free gate for conflicted flights

**Type:** Story
**Priority:** Low
**Components:** schiphol-ops · gates
**Difficulty:** ★★★ stretch · ~45 min
**Skills in play:** jira, github, (adr if you decide the rules deserve one)

## Description

As a ramp planner, when `gates --conflicts` flags a double-booking, I want the tool to propose a free, compatible gate for the later flight, so resolving a conflict is one decision instead of a manual search across the pier.

## Acceptance criteria

- [ ] `schiphol-ops gates --conflicts --suggest` appends a suggestion per conflict: a gate that is **free for the later flight's entire occupancy window**.
- [ ] Suggested gates are compatible: same schengen classification as the conflicted gate, and wide-body capable if the original gate was.
- [ ] Gates on the same pier are preferred; if none is free there, any compatible gate qualifies.
- [ ] If no compatible free gate exists, say so explicitly for that conflict.
- [ ] `--suggest` without `--conflicts` is rejected by argparse.
- [ ] Tests cover: a suggestion on the same pier, a fallback to another pier, and the no-gate-available case.

## Notes

- Requires a working Exercise 3 fix — suggestions built on a conflict list that misses conflicts would be actively dangerous. Say so in the PR if you stacked the branches.
- "Free" means: no occupancy overlap with any flight at the candidate gate, using the same overlap rule the conflict check uses.
