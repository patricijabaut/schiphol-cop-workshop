---
applyTo: "tests/**"
---

# Test conventions

- Plain `pytest` functions — no test classes, no unittest.
- Test names describe the behavior, not the function: `test_back_to_back_flights_do_not_conflict`, not `test_find_conflicts_2`.
- Build flights with the `make_flight(**overrides)` factory from `tests/conftest.py` instead of hand-writing `Flight(...)` literals.
- CLI tests call `main([...])` directly and use the `cli_data` fixture (which points `SCHIPHOL_OPS_DATA` at `tests/fixtures/`) plus `capsys`. Never invoke a subprocess.
- Every bug fix gets a regression test that fails on the old code. Name it after the behavior, and reference the ticket key in a short comment.
- Every acceptance-criterion bullet in a feature ticket gets at least one test.
- Assert on observable behavior (returned strings, exit codes, counts) — not on internal call order or private helpers.
