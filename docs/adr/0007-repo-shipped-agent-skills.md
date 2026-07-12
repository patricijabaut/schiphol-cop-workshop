# 0007 — Ship team rituals as agent skills in the repo

## Status

Accepted — 2026-07-05

## Context

Three procedures recur in every ticket here: pulling Jira context with `acli`, opening PRs with `gh`, and recording decisions as ADRs. Stuffing their full command recipes into `copilot-instructions.md` loads them into every session whether needed or not, and personal skills on each laptop would drift apart across twenty participants within an hour.

## Decision

We will ship the three procedures as agent skills in `.github/skills/` (`jira`, `github`, `adr`), one folder per skill with a `SKILL.md` whose frontmatter `description` tells the agent when to load it. The always-on instruction layers (ADR-0004) *reference* the skills instead of duplicating their content. The alternative — per-user skills in home directories — was rejected because the repo is the only artifact everyone reliably shares; versioning the skills with the code means a PR can fix a broken recipe for everyone at once.

## Consequences

Recipes load on demand, keeping the always-on context small, and every participant runs the same procedures — which makes workshop debugging tractable ("read what the skill told it to do"). The skills are code now: wrong recipes are bugs, fixable by PR. Cost: agents or IDE versions without skill support fall back to the cross-references in AGENTS.md, which cover the same ground more tersely.
