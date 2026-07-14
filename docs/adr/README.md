# Architecture Decision Records

Short, append-only notes on the decisions we made and the trade-offs we accepted. New records get the next sequential number; accepted records are never edited in spirit - if a decision changes, write a new ADR that **supersedes** the old one and flip only the old record's Status line.

Format: [Nygard-style](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) - Status / Context / Decision / Consequences. Keep it under a page. The **adr skill** ([`.github/skills/adr/`](../../.github/skills/adr/SKILL.md)) walks agents through writing one.

Both engineers and agents should read this index before making non-trivial changes. If your change contradicts a record here, write a new ADR first.

## Index

| #     | Title                                                                                     | Status   |
| ----- | ----------------------------------------------------------------------------------------- | -------- |
| [0001](./0001-python-stdlib-only.md)                | Python 3.11+ with stdlib only at runtime            | Accepted |
| [0002](./0002-module-split.md)                      | One module per responsibility                        | Accepted |
| [0003](./0003-json-seed-data.md)                    | JSON files as the only data source                   | Accepted |
| [0004](./0004-layered-copilot-instructions.md)      | Layered Copilot instructions                         | Accepted |
| [0005](./0005-jira-keyed-git-workflow.md)           | Jira-keyed branches, commits, and PR titles          | Accepted |
| [0006](./0006-subcommand-cli.md)                    | Single binary with argparse subcommands              | Accepted |
| [0007](./0007-repo-shipped-agent-skills.md)         | Ship team rituals as agent skills in the repo        | Accepted |
| [0008](./0008-city-filter-word-boundary-matching.md) | City filter uses case-insensitive word-boundary matching | Accepted |
