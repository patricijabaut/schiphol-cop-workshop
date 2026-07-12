from __future__ import annotations

import json
import os
from datetime import time
from pathlib import Path

from schiphol_ops.models import Direction, Flight, Gate, Status

DATA_DIR_ENV = "SCHIPHOL_OPS_DATA"


def data_dir() -> Path:
    """Resolve the data directory: env override first, then the repo's data/."""
    override = os.environ.get(DATA_DIR_ENV)
    if override:
        return Path(override)
    return Path(__file__).resolve().parents[2] / "data"


def parse_time(value: str) -> time:
    hours, _, minutes = value.partition(":")
    return time(int(hours), int(minutes))


def _flight_from_record(record: dict) -> Flight:
    status = Status(record["status"])
    delay = int(record.get("delay_minutes", 0))
    if status is Status.DELAYED and delay <= 0:
        raise ValueError(f"flight {record['number']} is delayed but has no delay_minutes")
    return Flight(
        number=record["number"],
        airline=record["airline"],
        direction=Direction(record["direction"]),
        city=record["city"],
        terminal=record["terminal"],
        gate=record["gate"],
        scheduled=parse_time(record["scheduled"]),
        delay_minutes=delay,
        status=status,
    )


def load_flights(path: Path | None = None) -> list[Flight]:
    source = path if path is not None else data_dir() / "flights.json"
    if not source.exists():
        raise FileNotFoundError(f"flight data not found: {source}")
    records = json.loads(source.read_text(encoding="utf-8"))
    flights = [_flight_from_record(record) for record in records]
    return sorted(flights, key=lambda f: (f.scheduled, f.number))


def load_gates(path: Path | None = None) -> list[Gate]:
    source = path if path is not None else data_dir() / "gates.json"
    if not source.exists():
        raise FileNotFoundError(f"gate data not found: {source}")
    records = json.loads(source.read_text(encoding="utf-8"))
    return [
        Gate(
            code=record["code"],
            pier=record["pier"],
            schengen=bool(record["schengen"]),
            wide_body=bool(record["wide_body"]),
        )
        for record in records
    ]
