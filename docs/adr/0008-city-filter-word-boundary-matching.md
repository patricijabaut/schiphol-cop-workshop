# 0008 - City filter uses case-insensitive word-boundary matching

## Status

Accepted - 2026-07-14

## Context

`by_city` in `filters.py` is used for both `--destination` (departures) and `--origin` (arrivals). The original implementation required an exact, case-sensitive match against the stored city string (e.g. `"London (LHR)"`). Users do not know the stored format, and a city like London maps to multiple airport codes (LHR, LTN), so an exact match missed most real-world queries. Bug VQ-2262.

## Decision

We will use `re.compile(r"\b" + re.escape(city), re.IGNORECASE)` — a case-insensitive regex anchored at a word boundary — as the match strategy in `by_city`.

Alternatives considered:

- **Exact match** (`f.city == city`): The broken status quo. Requires the user to know the exact stored string including airport code.
- **Plain substring** (`city.lower() in f.city.lower()`): Simpler, but matches mid-word — `"lon"` would return Barcelona (`barce**lon**a`) alongside London flights, producing confusing results.
- **Word-boundary regex** (chosen): `\b` anchors the search to the start of a word, so `"lon"` matches `"London (LHR)"` but not `"Barcelona (BCN)"`. `re.escape` handles parentheses in inputs like `"London (LHR)"`. `re.IGNORECASE` removes case sensitivity. The only added dependency is `re`, which is stdlib.

## Consequences

- `--destination london`, `--destination lon`, and `--destination "London (LHR)"` all return the expected flights.
- Searching by airport code alone (e.g. `--destination lhr`) will also match because `(` is not a word character, so `\b` fires before `L` in `(LHR)`. This is acceptable behaviour.
- `re.compile` adds minor overhead per filter call; negligible for the data sizes this CLI handles.
- The filter remains a pure function; no new runtime dependencies.
