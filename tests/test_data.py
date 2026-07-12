from __future__ import annotations

from datetime import time
from pathlib import Path

import pytest

from schiphol_ops.data import load_flights, load_gates, parse_time
from schiphol_ops.models import Status


def test_parse_time():
    assert parse_time("06:25") == time(6, 25)
    assert parse_time("23:05") == time(23, 5)


def test_load_flights_sorts_by_scheduled_time(fixtures_dir):
    flights = load_flights(fixtures_dir / "flights.json")
    assert [f.number for f in flights[:3]] == ["KL1001", "HV5821", "KL0643"]


def test_load_flights_parses_fields(fixtures_dir):
    flights = load_flights(fixtures_dir / "flights.json")
    delayed = next(f for f in flights if f.number == "KL0643")
    assert delayed.status is Status.DELAYED
    assert delayed.delay_minutes == 25
    assert delayed.scheduled == time(7, 10)


def test_load_flights_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_flights(Path("/nonexistent/flights.json"))


def test_load_gates(fixtures_dir):
    gates = load_gates(fixtures_dir / "gates.json")
    assert len(gates) == 7
    wide_bodies = {g.code for g in gates if g.wide_body}
    assert wide_bodies == {"E18", "E19"}
