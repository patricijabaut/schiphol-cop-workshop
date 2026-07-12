# Exercise 3 — Gate conflict check misses a double-booking on F07

**Type:** Bug
**Priority:** Highest
**Components:** schiphol-ops · gates
**Difficulty:** ★★★ · ~40 min
**Skills in play:** jira, github

## Description

Ramp operations counted **three** aircraft assigned to gate F07 in tonight's 18:20–20:05 window, but the conflict check only reports one clash there:

```
$ schiphol-ops gates --conflicts
2 gate conflicts detected

F07: KL0661 (18:20–19:15) overlaps DL0047 (18:25–19:10) during 18:25–19:10
H04: HV6011 (13:35–14:30) overlaps HV6923 (14:15–15:10) during 14:15–14:30
```

Look at F07 yourself:

```
$ schiphol-ops gates --pier F
...
F07 (non-schengen, wide-body)
    18:20–19:15  KL0661  Houston (IAH)
    18:25–19:10  DL0047  New York (JFK)
    19:10–20:05  KL0685  Mexico City (MEX)
```

KL0661's window (18:20–19:15) overlaps KL0685's (19:10–20:05) by five minutes — that's a second conflict on F07, and it's silently missing from the report. If ops had trusted the tool tonight, two aircraft would have been taxiing to the same gate.

It smells like the check only compares *neighbouring* occupancies once they're sorted by start time, so a long occupancy that swallows a later one never gets compared against it.

## Steps to reproduce

1. `schiphol-ops gates --pier F` — F07 shows three occupancies; note KL0661 vs KL0685 overlap 19:10–19:15.
2. `schiphol-ops gates --conflicts` — only the KL0661/DL0047 pair is reported for F07. Expected the KL0661/KL0685 pair as well (3 conflicts in total).

## Acceptance criteria

- [ ] Every overlapping **pair** of occupancies at a gate is reported, not just adjacent ones: with the shipped dataset, `gates --conflicts` reports 3 conflicts, including `F07: KL0661 … overlaps KL0685 … during 19:10–19:15`.
- [ ] Back-to-back occupancies (one ends exactly when the next starts) still do **not** count as conflicts.
- [ ] A regression test covers three overlapping occupancies at one gate where the middle one does not overlap the last one.

## Notes

- Reproduce first. Ask your agent to explain *why* the current algorithm misses the pair before letting it fix anything.
- Existing conflict tests only use two flights per gate — that's why the suite is green. Your regression test closes that hole.
