# Exercise 5 — Export flight data for the daily ops report

**Type:** Story
**Priority:** Medium
**Components:** schiphol-ops · CLI
**Difficulty:** ★★★ · ~45 min
**Skills in play:** adr ⭐, jira, github

## Description

As an ops analyst, I want to export (filtered) flight data to a machine-readable file, so I can build the daily punctuality report in a spreadsheet instead of copy-pasting board text.

Every evening the analyst pastes terminal output into Excel and hand-fixes the columns. We want a first-class `export` subcommand instead.

**This ticket requires an ADR before implementation.** Exporting introduces real decisions this codebase hasn't made yet — which formats to support, exact column/field layout, where the code lives in the module split, stdout vs file semantics. Capture the decision as `docs/adr/0008-…` (use the **adr skill**), get it agreed, then build exactly what the ADR says.

## Acceptance criteria

- [ ] ADR-0008 exists, follows the house template, is listed in the ADR index, and covers: supported formats, field layout, module placement, and output destination semantics — including at least one rejected alternative per decision.
- [ ] `schiphol-ops export --format csv` and `--format json` work; the format flag is required and validated by argparse.
- [ ] Every exported record carries at least: flight number, airline, direction, city, terminal, gate, scheduled time, delay minutes, status.
- [ ] `--out FILE` writes to the given path; without `--out`, the export goes to stdout (so it pipes).
- [ ] Export honors the board filters (`--terminal`, `--status`, `--airline`) and a `--direction departures|arrivals` selector; no filters = the whole dataset.
- [ ] Runtime stays stdlib-only (`csv`, `json` modules).
- [ ] Tests cover both formats, filtered export, and the file-writing path (use `tmp_path`).

## Notes

- Write the ADR, show it, *then* code. PRs where the ADR appeared after the implementation diff will be sent back on review — that ordering is the exercise.
- Rendering stays in `board.py`; export is a different concern (the ADR should say where it lives).
