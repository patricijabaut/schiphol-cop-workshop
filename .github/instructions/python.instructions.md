---
applyTo: "**/*.py"
---

# Python conventions

## Language level
- Target Python 3.11+. Use modern syntax: `X | None`, `list[int]`, `StrEnum`, and `from __future__ import annotations` at the top of every module.
- Type hints are required on every public function and dataclass field.

## Structure
- Domain models live in `models.py` as `@dataclass(frozen=True)`. Do not add ORM or pydantic.
- Pure functions everywhere except the CLI: `filters.py`, `board.py`, `gates.py`, and `stats.py` return values, never print.
- All `print` lives in `cli.py` (and `__main__.py`). Libraries return strings; the CLI prints them.
- Argparse only — no `click`, `typer`, or other CLI libs.

## Style
- Functions short, single-purpose. No unnecessary classes.
- Comments are rare: only when the *why* is non-obvious. Don't restate the code.
- No `print` debugging left behind. No commented-out code.
- Imports: stdlib, then first-party (`from schiphol_ops...`), separated by a blank line. No wildcard imports.

## Errors
- Raise built-in exceptions (`ValueError`, `FileNotFoundError`) with a clear message. Do not invent exception hierarchies for this codebase.
- Validate user-facing CLI input via argparse `choices=`/`type=` rather than handwritten checks.
- A lookup miss is not an error: return `None` or an empty list and let the CLI decide what to print and which exit code to use.
