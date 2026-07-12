from __future__ import annotations

from datetime import time
from pathlib import Path

import pytest

from schiphol_ops.models import Direction, Flight, Status

FIXTURES = Path(__file__).parent / "fixtures"


def make_flight(**overrides) -> Flight:
    defaults = dict(
        number="KL1001",
        airline="KL",
        direction=Direction.DEPARTURE,
        city="London (LHR)",
        terminal="D",
        gate="D04",
        scheduled=time(6, 25),
        delay_minutes=0,
        status=Status.ON_TIME,
    )
    defaults.update(overrides)
    return Flight(**defaults)


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES


@pytest.fixture
def sample_flights() -> list[Flight]:
    return [
        make_flight(),
        make_flight(
            number="HV5821",
            airline="HV",
            city="Barcelona (BCN)",
            terminal="H",
            gate="H01",
            scheduled=time(6, 40),
            status=Status.DEPARTED,
        ),
        make_flight(
            number="KL0643",
            airline="KL",
            city="New York (JFK)",
            terminal="E",
            gate="E18",
            scheduled=time(7, 10),
            delay_minutes=25,
            status=Status.DELAYED,
        ),
        make_flight(
            number="KL1002",
            direction=Direction.ARRIVAL,
            city="London (LHR)",
            gate="D02",
            scheduled=time(9, 5),
            status=Status.LANDED,
        ),
        make_flight(
            number="DL0046",
            airline="DL",
            direction=Direction.ARRIVAL,
            city="New York (JFK)",
            terminal="E",
            gate="E19",
            scheduled=time(7, 25),
            status=Status.LANDED,
        ),
    ]


@pytest.fixture
def cli_data(monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the CLI at the small fixture dataset."""
    monkeypatch.setenv("SCHIPHOL_OPS_DATA", str(FIXTURES))
    return FIXTURES
