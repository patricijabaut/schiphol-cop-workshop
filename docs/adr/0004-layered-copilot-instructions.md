# 0004 — Layered Copilot instructions

## Status

Accepted — 2026-06-22

## Context

Copilot reads guidance from several places, and it's tempting to dump everything into one giant file. One file means Python style rules pollute a docs-only session, and repo policy gets lost between lint rules. The workshop also needs to *demonstrate* how the layers compose, since that's a teaching goal.

## Decision

We will layer instructions by scope: [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md) for repo-wide collaboration policy (always loaded), [`.github/instructions/*.instructions.md`](../../.github/instructions/) with `applyTo` globs for per-path conventions (Python style, test style), [`AGENTS.md`](../../AGENTS.md) for agent-mode tool permissions and the change ritual, and [`.github/skills/`](../../.github/skills/) for on-demand procedures (see ADR-0007). Each rule lives in exactly one layer. The alternative — a single instructions file — was rejected as unscalable and pedagogically useless.

## Consequences

Rules load only where they apply, and finding the right home for a new rule is mechanical: policy → repo instructions, style → path instructions, permissions/ritual → AGENTS.md, procedure → a skill. The cost is four places to look; the index in the README and cross-links between the files mitigate that.
