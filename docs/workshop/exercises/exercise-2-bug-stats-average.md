# Exercise 2 — Operations summary reports impossible numbers

**Type:** Bug
**Priority:** Highest
**Components:** schiphol-ops · stats
**Difficulty:** ★★☆ · ~30 min
**Skills in play:** jira, github

## Description

The duty manager uses `schiphol-ops stats` for the morning briefing and stopped trusting it today:

```
$ schiphol-ops stats
OPERATIONS SUMMARY — Schiphol (AMS)

Overall: 55 flights — 46 on time, 9 delayed, 3 cancelled, avg delay 7m, on-time 88%
```

Two things can't be right:

1. **Average delay of 7 minutes?** Check the boards: the nine delayed flights are carrying delays of 15 up to 95 minutes (`schiphol-ops departures --status delayed` and `schiphol-ops arrivals --status delayed`). The real average across delayed flights is around 40 minutes. It looks like the average is being spread across *all* flights instead of the delayed ones.
2. **46 + 9 + 3 = 58, but there are 55 flights.** The three cancelled flights are apparently *also* being counted as "on time". A cancelled flight is many things, but not on time.

The same wrong numbers show up in every `--by airline` / `--by terminal` breakdown.

## Steps to reproduce

1. `schiphol-ops stats` — note `46 on time` and `avg delay 7m`.
2. `schiphol-ops departures --status delayed` and `schiphol-ops arrivals --status delayed` — add up the delays yourself: 9 flights, average ≈ 40m.
3. Note that on time (46) + delayed (9) + cancelled (3) exceeds the total (55).

## Acceptance criteria

- [ ] Average delay is computed across **delayed flights only**; with no delayed flights it reports `0m`.
- [ ] Cancelled flights are excluded from the on-time count: the buckets on time + delayed + cancelled add up to the total.
- [ ] With the shipped dataset, `schiphol-ops stats` reports `43 on time`, `avg delay 40m`, `on-time 83%`.
- [ ] Regression tests cover a mixed set (on-time + delayed + cancelled) for both the average and the bucket counts.

## Notes

- The on-time percentage is defined over operated flights (total minus cancelled) — that part is believed correct; don't change its definition, make its inputs right.
- Existing tests are green, so whatever you add must expose the current behavior before your fix.
