# 0005 — Jira-keyed branches, commits, and PR titles

## Status

Accepted — 2026-06-22

## Context

The workshop's core loop is Jira → code → PR, and the artifacts should be traceable in both directions: from a ticket to the code that closed it, and from a diff back to why it exists. Participants each seed tickets into their own Jira project, so ticket keys differ per person (OPS-1 for one, WS-1 for another).

## Decision

We will key every git artifact to the ticket: branches are `<ticket-key>-<slug>` (lowercase), commit messages are conventional-commit titles carrying the key (`fix: … (OPS-1)`), and PR titles are `<KEY>: <summary>` with a `Closes <KEY>` line in the body per the PR template. Alternatives: free-form branch names (rejected: untraceable in a room of 20 forks), and hard Jira/GitHub automation via webhooks (rejected: needs admin on both sides; the naming convention gives 90% of the traceability for none of the setup).

## Consequences

`git log --oneline` reads as a ticket history, and reviewers can pull ticket context for any PR with one `acli` command. The convention is enforced socially and by the agent instructions, not by tooling — a wrong branch name is a review remark, not a blocked push.
