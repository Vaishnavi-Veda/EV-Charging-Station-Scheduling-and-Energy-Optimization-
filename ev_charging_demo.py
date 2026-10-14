"""Demo entry point for the EV Charging Station Scheduling project."""
from ev_charging import ChargingStation, EVChargingScheduler, EVRequest


def print_result(title, result):
    print("\n" + title)
    print("=" * len(title))
    for item in result.schedules:
        print(
            f"{item.vehicle_id}: {item.station_id} | "
            f"slot {item.start_slot}-{item.end_slot} | "
            f"{item.energy_delivered_kwh} kWh | cost {item.cost:.2f}"
        )
    print(f"Total energy: {result.total_energy_kwh} kWh")
    print(f"Total cost: {result.total_cost:.2f}")
    print("Rejected:", ", ".join(result.rejected_vehicle_ids) or "None")


def main():
    stations = [
        ChargingStation("CS-01", power_kwh_per_slot=20, cost_per_slot=6.0),
        ChargingStation("CS-02", power_kwh_per_slot=30, cost_per_slot=8.0),
        ChargingStation("CS-03", power_kwh_per_slot=15, cost_per_slot=4.0),
    ]
    requests = [
        EVRequest("EV-101", 0, 4, 40, priority=3),
        EVRequest("EV-102", 0, 3, 30, priority=2),
        EVRequest("EV-103", 1, 5, 50, priority=4),
        EVRequest("EV-104", 2, 6, 35, priority=1),
        EVRequest("EV-105", 3, 7, 60, priority=5),
        EVRequest("EV-106", 4, 8, 25, priority=2),
    ]

    scheduler = EVChargingScheduler(stations)
    print_result("GREEDY SCHEDULE", scheduler.schedule_greedy(requests))
    print_result("DYNAMIC PROGRAMMING SCHEDULE", scheduler.schedule_dynamic_programming(requests))


if __name__ == "__main__":
    main()
