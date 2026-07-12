from __future__ import annotations

from dataclasses import dataclass
from datetime import time
from enum import StrEnum

AIRLINE_NAMES = {
    "AF": "Air France",
    "BA": "British Airways",
    "DL": "Delta Air Lines",
    "EI": "Aer Lingus",
    "EK": "Emirates",
    "HV": "Transavia",
    "KL": "KLM",
    "LH": "Lufthansa",
    "LX": "SWISS",
    "SK": "SAS",
    "SQ": "Singapore Airlines",
    "TK": "Turkish Airlines",
    "U2": "easyJet",
    "VY": "Vueling",
}


class Direction(StrEnum):
    DEPARTURE = "departure"
    ARRIVAL = "arrival"


class Status(StrEnum):
    ON_TIME = "on-time"
    BOARDING = "boarding"
    GATE_CLOSED = "gate-closed"
    DEPARTED = "departed"
    EXPECTED = "expected"
    LANDED = "landed"
    DELAYED = "delayed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class Flight:
    number: str
    airline: str
    direction: Direction
    city: str
    terminal: str
    gate: str
    scheduled: time
    delay_minutes: int
    status: Status

    @property
    def airline_name(self) -> str:
        return AIRLINE_NAMES.get(self.airline, self.airline)

    @property
    def is_delayed(self) -> bool:
        return self.status is Status.DELAYED

    @property
    def is_cancelled(self) -> bool:
        return self.status is Status.CANCELLED

    @property
    def display_status(self) -> str:
        if self.status is Status.DELAYED:
            return f"Delayed +{self.delay_minutes}m"
        return self.status.replace("-", " ").capitalize()


@dataclass(frozen=True)
class Gate:
    code: str
    pier: str
    schengen: bool
    wide_body: bool


def minutes_since_midnight(value: time) -> int:
    return value.hour * 60 + value.minute


def format_minutes(minutes: int) -> str:
    return f"{(minutes // 60) % 24:02d}:{minutes % 60:02d}"
