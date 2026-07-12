from __future__ import annotations

from datetime import time

from schiphol_ops.gates import (
    find_conflicts,
    occupancies_by_gate,
    occupancy_for,
    render_conflicts,
    render_gates,
)
from schiphol_ops.models import Direction, Gate, Status

from tests.conftest import make_flight


def test_departure_occupies_gate_before_pushback():
    flight = make_flight(scheduled=time(10, 0))
    slot = occupancy_for(flight)
    assert slot.window == "09:15–10:10"


def test_arrival_occupies_gate_for_deboarding():
    flight = make_flight(direction=Direction.ARRIVAL, scheduled=time(10, 0))
    slot = occupancy_for(flight)
    assert slot.window == "09:55–10:40"


def test_delay_shifts_the_occupancy_window():
    flight = make_flight(scheduled=time(10, 0), delay_minutes=30, status=Status.DELAYED)
    slot = occupancy_for(flight)
    assert slot.window == "09:45–10:40"


def test_cancelled_flights_do_not_occupy_gates():
    flight = make_flight(status=Status.CANCELLED)
    assert occupancies_by_gate([flight]) == {}


def test_overlapping_flights_at_same_gate_conflict():
    flights = [
        make_flight(number="HV6011", gate="H04", scheduled=time(14, 20)),
        make_flight(number="HV6923", gate="H04", scheduled=time(15, 0)),
    ]
    conflicts = find_conflicts(flights)
    assert len(conflicts) == 1
    assert conflicts[0].gate == "H04"
    assert conflicts[0].first.flight.number == "HV6011"
    assert conflicts[0].second.flight.number == "HV6923"


def test_back_to_back_flights_do_not_conflict():
    # First window ends 10:10, second starts 10:10 — a legal tight turnaround.
    flights = [
        make_flight(number="KL0001", gate="D04", scheduled=time(10, 0)),
        make_flight(number="KL0002", gate="D04", scheduled=time(10, 55)),
    ]
    assert find_conflicts(flights) == []


def test_same_window_different_gates_do_not_conflict():
    flights = [
        make_flight(number="KL0001", gate="D04", scheduled=time(10, 0)),
        make_flight(number="KL0002", gate="D07", scheduled=time(10, 0)),
    ]
    assert find_conflicts(flights) == []


def test_render_conflicts_reports_the_overlap():
    flights = [
        make_flight(number="HV6011", gate="H04", scheduled=time(14, 20)),
        make_flight(number="HV6923", gate="H04", scheduled=time(15, 0)),
    ]
    output = render_conflicts(find_conflicts(flights))
    assert "1 gate conflict detected" in output
    assert "H04: HV6011" in output
    assert "during 14:15–14:30" in output


def test_render_conflicts_when_all_clear():
    assert render_conflicts([]) == "No gate conflicts detected."


def test_render_gates_lists_free_and_occupied():
    gates = [
        Gate(code="D04", pier="D", schengen=False, wide_body=False),
        Gate(code="D07", pier="D", schengen=False, wide_body=False),
    ]
    output = render_gates([make_flight()], gates)
    assert "D04 (non-schengen)" in output
    assert "KL1001" in output
    assert "free all day" in output


def test_render_gates_filters_by_pier():
    gates = [
        Gate(code="D04", pier="D", schengen=False, wide_body=False),
        Gate(code="E18", pier="E", schengen=False, wide_body=True),
    ]
    output = render_gates([], gates, pier="e")
    assert "E18" in output
    assert "D04" not in output
