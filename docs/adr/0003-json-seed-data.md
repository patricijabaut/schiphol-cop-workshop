# 0003 — JSON files as the only data source

## Status

Accepted — 2026-06-15

## Context

The CLI needs a full day of plausible Schiphol flight and gate data. A real API (Schiphol publishes one) requires keys, network, and rate limits — all workshop hazards. A database adds setup and hides the data from casual reading.

## Decision

We will ship the dataset as `data/flights.json` and `data/gates.json`, loaded by `data.py` at each invocation, with the `SCHIPHOL_OPS_DATA` environment variable overriding the directory (tests point it at `tests/fixtures/`). Times are `"HH:MM"` strings describing one operational day. Alternatives: the live Schiphol API (rejected: network + auth in a room with 20 laptops), SQLite (rejected: obscures the data and invites schema tickets we don't want).

## Consequences

The whole world state is two human-readable files — participants can open them to check what a command *should* print, which is exactly how bug tickets here are verified. Deterministic data means deterministic outputs. The single-day model can't express date rollovers; if a ticket ever needs real timestamps, that supersedes this record.
