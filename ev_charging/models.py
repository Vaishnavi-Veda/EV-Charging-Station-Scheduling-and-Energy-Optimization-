from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EVRequest:
    vehicle_id: str
    arrival_slot: int
    departure_slot: int
    energy_needed_kwh: float
    priority: int = 1

    def __post_init__(self) -> None:
        if not self.vehicle_id:
            raise ValueError("vehicle_id is required")
        if self.departure_slot <= self.arrival_slot:
            raise ValueError("departure_slot must be greater than arrival_slot")
        if self.energy_needed_kwh <= 0:
            raise ValueError("energy_needed_kwh must be positive")
        if self.priority <= 0:
            raise ValueError("priority must be positive")


@dataclass(frozen=True)
class ChargingStation:
    station_id: str
    power_kwh_per_slot: float
    cost_per_slot: float

    def __post_init__(self) -> None:
        if not self.station_id:
            raise ValueError("station_id is required")
        if self.power_kwh_per_slot <= 0:
            raise ValueError("power_kwh_per_slot must be positive")
        if self.cost_per_slot < 0:
            raise ValueError("cost_per_slot must be non-negative")
