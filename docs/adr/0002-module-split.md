# 0002 — One module per responsibility

## Status

Accepted — 2026-06-15

## Context

The demo repo for the original talk squeezed everything into three files. This codebase is deliberately bigger, and multiple people (and agents) will change it concurrently during the workshop. Unclear module boundaries are the main way agent-generated diffs sprawl.

## Decision

We will split `src/schiphol_ops/` by responsibility: `cli.py` (argparse and *all* printing), `models.py` (frozen dataclasses and enums), `data.py` (loading and parsing seed data), `filters.py` (flight selection), `board.py` (board and detail rendering), `gates.py` (occupancy and conflicts), `stats.py` (aggregates). Everything outside `cli.py` is pure: functions take values and return values, never print. The alternative — grouping by feature (one module per subcommand) — was rejected because subcommands share filtering and rendering, and duplication across them is exactly the kind of drift agents amplify.

## Consequences

A ticket usually names its home module, so plans stay small and diffs stay local. Pure functions make the test suite fast and subprocess-free. The cost is that a new subcommand touches two files (`cli.py` plus its logic module); we accept that as the price of testability.
