# 0006 — Single binary with argparse subcommands

## Status

Accepted — 2026-06-29

## Context

The demo repo's CLI printed one board and took three flags; this codebase covers five views of the operation (departures, arrivals, gates, stats, search) and tickets will keep adding more. Cramming views into flags on one command (`--mode gates --conflicts`) turns the flag namespace into a minefield where every new option must be checked against every mode.

## Decision

We will expose one `schiphol-ops` binary with argparse subparsers, one subcommand per view, each owning its flags. Shared flag groups (the board filters) are attached by a helper so `departures` and `arrivals` stay consistent. Alternatives: multiple entry points per view (rejected: five console scripts to install and document), `click`/`typer` command groups (rejected by ADR-0001's no-dependency rule — argparse subparsers do the same job with more ceremony but zero installs).

## Consequences

New capability = new subcommand with a private flag namespace, which keeps feature tickets independent of each other — important when twenty people implement different tickets against the same `main`. `cli.py` grows a parser-builder and a dispatch block per subcommand; that boilerplate is accepted as the cost of argparse.
