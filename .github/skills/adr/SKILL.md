---
name: adr
description: Write or supersede an Architecture Decision Record in docs/adr/ using this repo's Nygard-style template. Use when a change involves a technical decision or trade-off (new module, new output format, new dependency, changed convention), when a planned change contradicts an existing ADR, or when the user asks to document a decision.
---

# Architecture Decision Records

Capture one decision per record in `docs/adr/`, before the code that implements it.

## When an ADR is required

- Adding a module, subcommand, output format, or dependency — anything a future reader will ask "why is it like this?" about.
- Any change that contradicts an accepted ADR. Never silently break a recorded decision: write a new ADR that **supersedes** it first.
- A ticket explicitly asks for one.

Not required for: bug fixes that restore intended behavior, refactors within an existing decision, or test-only changes.

## Procedure

1. Read `docs/adr/README.md` and skim existing records so the new one doesn't contradict or duplicate them.
2. Take the next free sequential number (`ls docs/adr/` — records are `NNNN-kebab-case-title.md`).
3. Write the record using the template below. Keep it under a page. Present it to the user for approval **before** implementing the decision.
4. Add a row to the index table in `docs/adr/README.md`.
5. If the record supersedes an older one, set the old record's Status to `Superseded by [NNNN](./NNNN-….md)` — that status line is the only edit ever allowed to an accepted record.
6. Commit ADR and implementation together on the ticket branch (`docs: add ADR-NNNN … (<KEY>)` if committed separately).

## Template

```markdown
# NNNN — <Short imperative title>

## Status

Accepted — <YYYY-MM-DD>

## Context

<What situation forces a decision? 2-5 sentences of facts, no solution talk.>

## Decision

<The decision, stated actively: "We will …". Name the alternatives considered
and in one line each why they lost.>

## Consequences

<What becomes easier, what becomes harder, what debt is accepted. Include the
negative consequences — an ADR with no downsides hasn't been thought through.>
```

## Style

- Facts and trade-offs, not advocacy. The losing options were not stupid; say what they'd have been good at.
- Write for a reader two years from now who has none of today's context.
- One decision per record. Two decisions = two ADRs.
