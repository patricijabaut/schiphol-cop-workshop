# Exercise 4 — Sort the boards by destination or delay

**Type:** Story
**Priority:** Medium
**Components:** schiphol-ops · CLI
**Difficulty:** ★★☆ · ~30 min
**Skills in play:** jira, github

## Description

As a gate-ops coordinator, I want to sort the departures and arrivals boards by destination or by delay, so I can find a city quickly during disruptions and see the worst-hit flights at the top instead of scanning a time-ordered list.

Today both boards always print in scheduled-time order. During this morning's fog window the coordinator was reading 30 rows top to bottom looking for the biggest delays.

## Acceptance criteria

- [ ] `departures` and `arrivals` both accept `--sort` with choices `time`, `destination`, and `delay`; invalid values are rejected by argparse with exit code 2.
- [ ] `--sort time` (and no `--sort` at all) keeps today's behavior: ascending by scheduled time.
- [ ] `--sort destination` orders alphabetically by the board's destination/origin column (case-insensitive).
- [ ] `--sort delay` orders by delay minutes, largest first; flights without delay follow, in scheduled-time order.
- [ ] `--sort` combines with the existing filters (`--terminal`, `--status`, `--airline`, `--destination`/`--origin`).
- [ ] Tests cover each sort order and at least one combination with a filter.

## Notes

- Sorting is flight *selection/ordering* logic — it belongs in `filters.py` (or a sibling pure function), not in `board.py` rendering and not inline in `cli.py` (see ADR-0002).
- The flag applies to boards only; `gates`, `stats`, and `search` are out of scope.
