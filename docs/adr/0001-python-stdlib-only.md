# 0001 — Python 3.11+ with stdlib only at runtime

## Status

Accepted — 2026-06-15

## Context

`schiphol-ops` is a workshop codebase: ~20 people clone it onto laptops we don't control, on corporate networks where package installs are slow or blocked. Every runtime dependency multiplies setup failures. The domain (filtering lists, formatting tables, small aggregates) needs nothing the standard library doesn't provide.

## Decision

We will target Python 3.11+ and keep the runtime dependency list empty. `pytest` is the only allowed dev dependency. Alternatives considered: `rich` would give prettier tables but adds an install and tempts feature creep in rendering; `pydantic` would give validated models but the JSON schema is ours and trivial; `click`/`typer` lose to argparse per the same logic (see ADR-0006).

## Consequences

Setup is `python -m venv` + one editable install, and it works offline once cloned. Table rendering, time math, and JSON parsing are hand-rolled, which costs some code but makes every behavior traceable — useful in a workshop where participants read unfamiliar code under time pressure. If a ticket genuinely needs a runtime dependency, that's a new ADR superseding this one.
