from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .models import ChargingStation, EVRequest


@dataclass(frozen=True)
class ScheduledSession:
    vehicle_id: str
    station_id: str
    start_slot: int
    end_slot: int
    energy_delivered_kwh: float
    cost: float


@dataclass
class ScheduleResult:
    schedules: List[ScheduledSession] = field(default_factory=list)
    total_energy_kwh: float = 0.0
    total_cost: float = 0.0
    rejected_vehicle_ids: List[str] = field(default_factory=list)


class EVChargingScheduler:
    def __init__(self, stations: List[ChargingStation]):
        self.stations = list(stations)

    def schedule_greedy(self, requests: List[EVRequest]) -> ScheduleResult:
        schedules: List[ScheduledSession] = []
        rejected: List[str] = []
        station_usage = {station.station_id: [] for station in self.stations}

        for request in sorted(
            requests,
            key=lambda req: (
                req.departure_slot,
                req.priority,
                req.energy_needed_kwh,
                req.arrival_slot,
            ),
            reverse=False,
        ):
            assigned = False
            for station in self.stations:
                duration = request.departure_slot - request.arrival_slot
                energy_capacity = station.power_kwh_per_slot * max(duration, 1)
                if request.energy_needed_kwh > energy_capacity:
                    continue
                conflicts = False
                for occupied_start, occupied_end in station_usage[station.station_id]:
                    if not (request.departure_slot <= occupied_start or request.arrival_slot >= occupied_end):
                        conflicts = True
                        break
                if conflicts:
                    continue

                start_slot = request.arrival_slot
                end_slot = request.departure_slot
                cost = (end_slot - start_slot) * station.cost_per_slot
                schedules.append(
                    ScheduledSession(
                        vehicle_id=request.vehicle_id,
                        station_id=station.station_id,
                        start_slot=start_slot,
                        end_slot=end_slot,
                        energy_delivered_kwh=min(request.energy_needed_kwh, energy_capacity),
                        cost=cost,
                    )
                )
                station_usage[station.station_id].append((start_slot, end_slot))
                assigned = True
                break

            if not assigned:
                rejected.append(request.vehicle_id)

        total_energy = sum(session.energy_delivered_kwh for session in schedules)
        total_cost = sum(session.cost for session in schedules)
        return ScheduleResult(
            schedules=schedules,
            total_energy_kwh=total_energy,
            total_cost=total_cost,
            rejected_vehicle_ids=rejected,
        )

    def schedule_dynamic_programming(self, requests: List[EVRequest]) -> ScheduleResult:
        feasible: List[tuple[EVRequest, ChargingStation]] = []
        for request in requests:
            for station in self.stations:
                duration = max(1, request.departure_slot - request.arrival_slot)
                if request.energy_needed_kwh <= station.power_kwh_per_slot * duration:
                    feasible.append((request, station))

        if not feasible:
            return ScheduleResult(rejected_vehicle_ids=[request.vehicle_id for request in requests])

        candidates: List[ScheduledSession] = []
        for request, station in feasible:
            duration = request.departure_slot - request.arrival_slot
            cost = duration * station.cost_per_slot
            candidates.append(
                ScheduledSession(
                    vehicle_id=request.vehicle_id,
                    station_id=station.station_id,
                    start_slot=request.arrival_slot,
                    end_slot=request.departure_slot,
                    energy_delivered_kwh=request.energy_needed_kwh,
                    cost=cost,
                )
            )

        candidates.sort(key=lambda session: (session.end_slot, session.start_slot))
        memo: List[tuple[float, List[ScheduledSession]]] = [(0.0, []) for _ in range(len(candidates) + 1)]
        for idx in range(1, len(candidates) + 1):
            prev_idx = idx - 1
            total_value = candidates[idx - 1].energy_delivered_kwh * max(1, candidates[idx - 1].cost / max(1.0, candidates[idx - 1].end_slot - candidates[idx - 1].start_slot + 1))
            while prev_idx > 0 and candidates[prev_idx - 1].end_slot > candidates[idx - 1].start_slot:
                prev_idx -= 1
            best_without = memo[idx - 1][0]
            best_with = memo[prev_idx][0] + total_value
            if best_with > best_without:
                memo[idx] = (best_with, memo[prev_idx][1] + [candidates[idx - 1]])
            else:
                memo[idx] = (best_without, memo[idx - 1][1])
        selected = memo[-1][1]
        seen = set()
        schedules = []
        for session in selected:
            if session.vehicle_id in seen:
                continue
            seen.add(session.vehicle_id)
            schedules.append(session)

        total_energy = sum(session.energy_delivered_kwh for session in schedules)
        total_cost = sum(session.cost for session in schedules)
        rejected = [request.vehicle_id for request in requests if request.vehicle_id not in seen]
        return ScheduleResult(
            schedules=schedules,
            total_energy_kwh=total_energy,
            total_cost=total_cost,
            rejected_vehicle_ids=rejected,
        )
