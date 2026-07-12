from __future__ import annotations

from schiphol_ops.models import Direction, Flight

_HEADERS = {
    Direction.DEPARTURE: ("FLIGHT", "DESTINATION", "GATE", "SCHEDULED", "STATUS"),
    Direction.ARRIVAL: ("FLIGHT", "ORIGIN", "GATE", "SCHEDULED", "STATUS"),
}

_TITLES = {
    Direction.DEPARTURE: "DEPARTURES — Schiphol (AMS)",
    Direction.ARRIVAL: "ARRIVALS — Schiphol (AMS)",
}

EMPTY_MESSAGE = "No flights match the given filters."


def _rows(flights: list[Flight]) -> list[tuple[str, ...]]:
    return [
        (
            flight.number,
            flight.city,
            flight.gate,
            flight.scheduled.strftime("%H:%M"),
            flight.display_status,
        )
        for flight in flights
    ]


def _render_table(headers: tuple[str, ...], rows: list[tuple[str, ...]]) -> str:
    widths = [len(header) for header in headers]
    for row in rows:
        widths = [max(width, len(cell)) for width, cell in zip(widths, row)]
    lines = ["    ".join(header.ljust(width) for header, width in zip(headers, widths)).rstrip()]
    for row in rows:
        lines.append("    ".join(cell.ljust(width) for cell, width in zip(row, widths)).rstrip())
    return "\n".join(lines)


def _footer(flights: list[Flight]) -> str:
    delayed = sum(1 for f in flights if f.is_delayed)
    cancelled = sum(1 for f in flights if f.is_cancelled)
    noun = "flight" if len(flights) == 1 else "flights"
    return f"Showing {len(flights)} {noun} — {delayed} delayed, {cancelled} cancelled"


def render_board(flights: list[Flight], direction: Direction) -> str:
    if not flights:
        return EMPTY_MESSAGE
    table = _render_table(_HEADERS[direction], _rows(flights))
    return f"{_TITLES[direction]}\n\n{table}\n\n{_footer(flights)}"


def render_detail(flight: Flight) -> str:
    city_label = "Destination" if flight.direction is Direction.DEPARTURE else "Origin"
    fields = [
        ("Flight", f"{flight.number} ({flight.airline_name})"),
        ("Type", flight.direction.capitalize()),
        (city_label, flight.city),
        ("Terminal", flight.terminal),
        ("Gate", flight.gate),
        ("Scheduled", flight.scheduled.strftime("%H:%M")),
        ("Status", flight.display_status),
    ]
    width = max(len(label) for label, _ in fields)
    return "\n".join(f"{label.ljust(width)}  {value}" for label, value in fields)
