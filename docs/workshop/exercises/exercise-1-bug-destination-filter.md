# Exercise 1 — Destination filter misses every flight

**Type:** Bug
**Priority:** High
**Components:** schiphol-ops · filters
**Difficulty:** ★☆☆ warmup · ~20 min
**Skills in play:** jira, github

## Description

Passenger services tried to pull up this morning's London departures for a stranded group and got nothing:

```
$ schiphol-ops departures --destination london
No flights match the given filters.
```

That's wrong — the full board clearly shows London flights (KL1001, U28874, BA0431, BA0443). Even `--destination London` with a capital L finds nothing. The only thing that works is typing the exact board entry including the airport code:

```
$ schiphol-ops departures --destination "London (LHR)"
```

…which nobody knows by heart, and which still misses the easyJet flight to Luton because that one is listed as `London (LTN)`.

## Steps to reproduce

1. `schiphol-ops departures` — note the four London flights on the board.
2. `schiphol-ops departures --destination london` — expected those four flights, got `No flights match the given filters.`

## Acceptance criteria

- [ ] `schiphol-ops departures --destination london` lists all four London flights, regardless of the casing typed by the user.
- [ ] Partial names match: `--destination lon` and `--destination "New York"` both work (substring match against the board entry).
- [ ] The same fix applies to `schiphol-ops arrivals --origin <city>` — origin and destination share one code path.
- [ ] A regression test covers case-insensitive and partial matching, so this can't come back.

## Notes

- Exact full-string input like `"London (LHR)"` must keep working.
- Reproduce the bug before fixing it, and re-run the repro afterwards.
