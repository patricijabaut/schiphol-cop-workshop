# Exercise 6 — Delay report that posts back to Jira

**Type:** Story
**Priority:** Medium
**Components:** schiphol-ops · CLI
**Difficulty:** ★★☆ · ~35 min
**Skills in play:** jira ⭐, github

## Description

As a duty manager, I want a ready-to-paste Markdown report of the worst delays, so I can drop the current situation into tickets and chat channels without retyping numbers.

The output should be a self-contained Markdown snippet — and to prove it works, the last step of this ticket is posting the generated report back onto **this very Jira ticket** as a comment, straight from the terminal.

Expected shape:

```markdown
## Delay report — Schiphol (AMS)

| Flight | Type      | City                | Scheduled | Delay |
|--------|-----------|---------------------|-----------|-------|
| KL0757 | Departure | Sao Paulo (GRU)     | 14:05     | +95m  |
| KL1602 | Arrival   | Rome (FCO)          | 17:35     | +55m  |
...

9 delayed flights in total, average delay 40m.
```

## Acceptance criteria

- [ ] `schiphol-ops delay-report` prints a Markdown table of the most-delayed flights across departures **and** arrivals, largest delay first.
- [ ] `--top N` limits the table (default 5); the closing line always reports the totals across **all** delayed flights.
- [ ] Cancelled flights never appear in the report.
- [ ] With no delayed flights, the command prints `No delays to report. 🎉` and exits 0.
- [ ] Tests cover the ordering, the `--top` limit, and the no-delays case.
- [ ] **The loop is closed:** the generated report is posted as a comment on this ticket via `acli jira workitem comment create`, and the PR description mentions that this was done.

## Notes

- The totals line should use the (fixed) stats logic from Exercise 2 — if you haven't done Exercise 2, the averages will look funny; that's fine, note it in the PR.
- Markdown assembly is rendering: it belongs next to (not inside) the board rendering, per ADR-0002.
