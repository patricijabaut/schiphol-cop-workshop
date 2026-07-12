from __future__ import annotations

from datetime import time

from schiphol_ops.board import EMPTY_MESSAGE, render_board, render_detail
from schiphol_ops.filters import by_direction
from schiphol_ops.models import Direction, Status

from tests.conftest import make_flight


def test_departures_board_has_title_and_headers(sample_flights):
    output = render_board(by_direction(sample_flights, Direction.DEPARTURE), Direction.DEPARTURE)
    assert output.startswith("DEPARTURES — Schiphol (AMS)")
    assert "DESTINATION" in output
    assert "KL1001" in output
    assert "KL1002" not in output


def test_arrivals_board_uses_origin_header(sample_flights):
    output = render_board(by_direction(sample_flights, Direction.ARRIVAL), Direction.ARRIVAL)
    assert output.startswith("ARRIVALS — Schiphol (AMS)")
    assert "ORIGIN" in output


def test_empty_board_prints_friendly_message():
    assert render_board([], Direction.DEPARTURE) == EMPTY_MESSAGE


def test_delayed_flight_shows_delay_minutes():
    flight = make_flight(delay_minutes=25, status=Status.DELAYED)
    output = render_board([flight], Direction.DEPARTURE)
    assert "Delayed +25m" in output


def test_footer_counts_delays_and_cancellations(sample_flights):
    output = render_board(sample_flights, Direction.DEPARTURE)
    assert output.endswith("Showing 5 flights — 1 delayed, 0 cancelled")


def test_footer_uses_singular_for_one_flight():
    output = render_board([make_flight()], Direction.DEPARTURE)
    assert "Showing 1 flight —" in output


def test_render_detail_for_departure():
    flight = make_flight(scheduled=time(6, 25))
    output = render_detail(flight)
    assert "KL1001 (KLM)" in output
    assert "Destination" in output
    assert "London (LHR)" in output
    assert "06:25" in output


def test_render_detail_for_arrival():
    flight = make_flight(direction=Direction.ARRIVAL, status=Status.LANDED)
    output = render_detail(flight)
    assert "Origin" in output
    assert "Landed" in output
