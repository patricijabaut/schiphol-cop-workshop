from __future__ import annotations

from schiphol_ops.filters import (
    apply_filters,
    by_airline,
    by_city,
    by_direction,
    by_status,
    by_terminal,
    find_flight,
)
from schiphol_ops.models import Direction, Status

from tests.conftest import make_flight


def test_by_direction_splits_departures_and_arrivals(sample_flights):
    departures = by_direction(sample_flights, Direction.DEPARTURE)
    arrivals = by_direction(sample_flights, Direction.ARRIVAL)
    assert {f.number for f in departures} == {"KL1001", "HV5821", "KL0643"}
    assert {f.number for f in arrivals} == {"KL1002", "DL0046"}


def test_by_terminal_is_case_insensitive_on_input(sample_flights):
    assert [f.number for f in by_terminal(sample_flights, "e")] == ["KL0643", "DL0046"]


def test_by_status(sample_flights):
    delayed = by_status(sample_flights, Status.DELAYED)
    assert [f.number for f in delayed] == ["KL0643"]


def test_by_airline_is_case_insensitive_on_input(sample_flights):
    assert {f.number for f in by_airline(sample_flights, "kl")} == {
        "KL1001",
        "KL0643",
        "KL1002",
    }


def test_by_city_matches_the_board_entry(sample_flights):
    matches = by_city(sample_flights, "London (LHR)")
    assert {f.number for f in matches} == {"KL1001", "KL1002"}


def test_by_city_no_match_returns_empty_list(sample_flights):
    assert by_city(sample_flights, "Atlantis (ATL)") == []


# Regression tests for VQ-2262: city filter was exact-match only
def test_by_city_is_case_insensitive(sample_flights):
    # "london" (lowercase) should match flights with city "London (LHR)"
    matches = by_city(sample_flights, "london")
    assert {f.number for f in matches} == {"KL1001", "KL1002"}


def test_by_city_matches_partial_name(sample_flights):
    # "lon" should match all London flights regardless of airport code suffix
    matches = by_city(sample_flights, "lon")
    assert {f.number for f in matches} == {"KL1001", "KL1002"}


def test_by_city_filters_arrivals_by_origin(sample_flights):
    # --origin on arrivals uses the same code path; "new york" should find DL0046
    matches = apply_filters(sample_flights, direction=Direction.ARRIVAL, city="new york")
    assert {f.number for f in matches} == {"DL0046"}


def test_by_city_wrong_airport_code_does_not_match(sample_flights):
    # A city with a different airport code suffix must not match another airport
    assert by_city(sample_flights, "London (GHE)") == []


def test_apply_filters_combines_criteria(sample_flights):
    result = apply_filters(
        sample_flights,
        direction=Direction.DEPARTURE,
        terminal="E",
        airline="KL",
    )
    assert [f.number for f in result] == ["KL0643"]


def test_apply_filters_without_criteria_returns_everything(sample_flights):
    assert apply_filters(sample_flights) == sample_flights


def test_find_flight_ignores_case_and_spaces(sample_flights):
    assert find_flight(sample_flights, "kl 1001") == sample_flights[0]


def test_find_flight_returns_none_for_unknown_number(sample_flights):
    assert find_flight(sample_flights, "XX9999") is None


def test_terminal_filter_on_flight_with_delay():
    flight = make_flight(terminal="F", gate="F07", delay_minutes=30, status=Status.DELAYED)
    assert by_terminal([flight], "F") == [flight]
