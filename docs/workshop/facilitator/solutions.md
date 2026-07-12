# Solutions — facilitator eyes only

Root cause, expected diff shape, and graded hints per exercise. The three bugs were seeded deliberately; the shipped test suite is green because its coverage holes were placed exactly around them (that's a talking point, not an accident).

## Exercise 1 — destination filter

**Seeded bug** — `src/schiphol_ops/filters.py`, `by_city()`:

```python
return [f for f in flights if f.city == city]   # exact, case-sensitive
```

**Expected fix** (one line + tests):

```python
needle = city.lower()
return [f for f in flights if needle in f.city.lower()]
```

`by_city` already backs both `--destination` and `--origin` via `apply_filters`, so the third AC is free — good participants will *verify* that rather than assume it.

**Verification:** `departures --destination london` → 4 flights (KL1001, U28874, BA0431, BA0443); `arrivals --origin york` → 2.

**What Copilot typically does:** nails it. Occasionally over-engineers (normalizing accents, regex). Push-back practice: "simplest thing that satisfies the ACs."

**Hints, graded:** ① "Which module owns *selection*?" ② "Compare what the board prints with what you typed — exactly." ③ "Look at `by_city` in filters.py."

## Exercise 2 — stats

**Seeded bug** — `src/schiphol_ops/stats.py`, `summarize()`, two intertwined mistakes:

```python
on_time = len(flights) - len(delayed)                    # cancelled counted as on time
avg_delay = round(sum(f.delay_minutes for f in flights) / len(flights))  # ÷ all flights
```

**Expected fix:**

```python
on_time = len(flights) - len(delayed) - len(cancelled)
avg_delay = round(sum(f.delay_minutes for f in delayed) / len(delayed)) if delayed else 0
```

**Verification:** `schiphol-ops stats` → `55 flights — 43 on time, 9 delayed, 3 cancelled, avg delay 40m, on-time 83%` (buggy: 46 / 7m / 88%).

**Why the suite was green:** the shipped avg-delay test uses a fixture where *every* flight is delayed (÷all == ÷delayed), and the on-time test has no cancelled flights. Worth showing at the wrap-up — tests can be green and wrong.

**What Copilot typically does:** finds both once it *reads* `summarize()`, but often fixes only the average if the prompt only mentioned the average — the ticket names both symptoms for exactly that reason. Watch for agents "fixing" `on_time_pct` instead (the ticket's Note forbids it).

**Hints:** ① "Do the three buckets add up to the total?" ② "What set is the average divided over?" ③ "Two bugs, one function, `stats.py`."

## Exercise 3 — gate conflicts

**Seeded bug** — `src/schiphol_ops/gates.py`, `find_conflicts()` compares only *adjacent* occupancies after sorting by start:

```python
for current, following in zip(slots, slots[1:]):
    if _overlaps(current, following):
```

KL0661 (18:20–19:15) swallows DL0047 (18:25–19:10); the adjacent pair DL0047→KL0685 doesn't overlap (19:10 vs 19:10), so KL0661 vs KL0685 (19:10–19:15) is never compared.

**Expected fix** — all pairs per gate (n² is fine at this scale; sorted-sweep with max-end also acceptable and worth praising):

```python
for i, current in enumerate(slots):
    for later in slots[i + 1:]:
        if _overlaps(current, later):
```

**Verification:** `gates --conflicts` → **3** conflicts, including `F07: KL0661 … overlaps KL0685 … during 19:10–19:15`. Back-to-back test (`test_back_to_back_flights_do_not_conflict`) must stay green — `_overlaps` uses strict `<` and must keep doing so.

**What Copilot typically does:** the classic failure is "fixing" `_overlaps` to `<=`, which flags legal back-to-back turnarounds — the existing test catches it; let participants discover that red test rather than pre-warning. Regression test needs *three* flights where the middle doesn't overlap the last (mirror the F07 data).

**Hints:** ① "Reproduce with `gates --pier F` and draw the three windows on paper." ② "Which *pairs* does the loop actually compare?" ③ "`zip(slots, slots[1:])` — what pair is missing?"

## Exercise 4 — `--sort`

No bug; clean feature. Expected shape: a pure `sort_flights(flights, order)` in `filters.py`; `cli.py` gains `--sort` (`choices=["time", "destination", "delay"]`, `default="time"`) on both board subparsers via `_add_board_arguments`. Delay order: `sorted(..., key=lambda f: (-f.delay_minutes, f.scheduled, f.number))`. Watch for: sorting inside `board.py` (ADR-0002 violation — send it back), and missing the "non-delayed keep time order" tail of the delay AC.

## Exercise 5 — export + ADR-0008

The deliverable is the **ordering**: ADR first, agreed, then code. There's no single right ADR — CSV+JSON per the ticket, but module placement (`export.py` vs extending `board.py` — `export.py` is the defensible one per ADR-0002), stdout semantics, and column layout are theirs to decide *and defend*. Two participants with different ADR-0008s is a feature; compare them at show & tell.

Implementation notes: `csv` module with `DictWriter`, `json.dumps` with a list of dicts; `--out` writes via `Path.write_text` / file handle, default stdout keeps it pipeable. Tests: `tmp_path` for the file path, `capsys` for stdout. Common miss: forgetting `--direction` filtering or leaking `print` into the export module.

If someone edits ADR index/README sloppily, the adr skill's step 4 is the reference.

## Exercise 6 — delay-report

Clean feature + the acli round-trip. Expected shape: a pure `render_delay_report(flights, top)` (new `report.py` or alongside board rendering — either defensible), `delay-report` subparser with `--top` (default 5, `type=int`). Ordering: delay desc; totals line covers *all* delayed flights even when the table is truncated (the AC people miss). Uses `summarize()` — participants who skipped Exercise 2 get funny totals; the ticket tells them to note it in the PR, check they did.

The ⭐ AC is the `acli jira workitem comment create` step — physically check a few tickets for the comment during the block; it's the most-skipped step of the day.

## Stretch A — gate suggestions

Builds on the Ex-3 fix. Sound approach: for each conflict, take the later occupancy, scan gates (same pier first, then all) filtered by schengen/wide-body compatibility, and test the window against every occupancy at the candidate gate using the same `_overlaps`. `argparse` dependency check: `parser.error` when `--suggest` without `--conflicts`. No-gate case must be explicit output, not silence.

## Stretch B — peer review

Nothing to solve — check reviews are substantive (AC coverage, missing regression test, ADR conflicts) and that at least one received remark turned into a pushed commit. Harvest the best Copilot-review miss for the retro.

## Meta: if someone asks "were the bugs planted?"

Yes — and the honest answer is the best slide of the day: each bug is a real-world mistake pattern (exact-match filter, wrong denominator + wrong bucket, adjacent-only interval check), and the tests were written around them the way real coverage holes happen: happy paths only.
