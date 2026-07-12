# Exercises

Six tickets plus two stretch goals. Each file is the source of truth for a Jira ticket — `scripts/seed-jira.sh` creates them in your own Jira project (or `scripts/seed-github-issues.sh` creates them as GitHub issues on your fork). After seeding, `my-tickets.md` in the repo root maps each exercise to *your* ticket key.

Work them in order — Exercise 1 is the guided warm-up, and 2–4 can be done in any order after that. Every exercise follows the same loop, described in the [participant guide](../01-participant-guide.md).

| # | Ticket | Type | Difficulty | Est. | Skills in play |
|---|--------|------|------------|------|----------------|
| 1 | [Destination filter misses every flight](./exercise-1-bug-destination-filter.md) | Bug | ★☆☆ | 20 min | jira, github |
| 2 | [Operations summary reports impossible numbers](./exercise-2-bug-stats-average.md) | Bug | ★★☆ | 30 min | jira, github |
| 3 | [Gate conflict check misses a double-booking on F07](./exercise-3-bug-gate-conflicts.md) | Bug | ★★★ | 40 min | jira, github |
| 4 | [Sort the boards by destination or delay](./exercise-4-feature-sort-flag.md) | Story | ★★☆ | 30 min | jira, github |
| 5 | [Export flight data for the daily ops report](./exercise-5-feature-export.md) | Story | ★★★ | 45 min | **adr** ⭐, jira, github |
| 6 | [Delay report that posts back to Jira](./exercise-6-feature-delay-report.md) | Story | ★★☆ | 35 min | **jira** ⭐, github |
| A | [Suggest a free gate for conflicted flights](./stretch-a-gate-suggestions.md) | Story | ★★★ stretch | 45 min | jira, github |
| B | [Review a neighbour's PR from the terminal](./stretch-b-peer-review.md) | Task | ★★☆ stretch | 25 min | **github** ⭐ |

Ground rules:

- **One ticket = one branch = one PR** against your own fork's `main`.
- **Bugs:** reproduce before fixing, and ship a regression test that fails on the old code.
- **Features:** every acceptance-criterion bullet gets a test.
- The test suite is green when you clone — the bugs are real behavior, not red tests. Trust the tickets, not the suite.
