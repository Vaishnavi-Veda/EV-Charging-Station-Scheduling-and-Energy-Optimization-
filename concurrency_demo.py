from models import ParkingSlot, Vehicle
from services import ParkingService


def main() -> None:
    parking = ParkingService()

    # Create 5 parking slots
    for number in range(1, 6):
        parking.add_slot(
            ParkingSlot(f"S{number:02d}", "S")
        )

    # Create 10 vehicles
    vehicles = [
        Vehicle(
            license_number=f"L{number}",
            plate_number=f"TS07AB{number:04d}",
            owner_name=f"Owner {number}",
            vehicle_type="Car",
        )
        for number in range(1, 11)
    ]

    print("=" * 60)
    print("CONCURRENT SMART PARKING TEST")
    print("=" * 60)
    print(f"Vehicles requesting parking : {len(vehicles)}")
    print("Available slots             : 5")
    print()

    results = parking.park_vehicle_concurrently(vehicles, "S")

    for result in results:
        print(
            f"{result['vehicle']:12} | "
            f"{result['status']:7} | "
            f"{result['slot']}"
        )

    parked = sum(
        1 for result in results
        if result["status"] == "Parked"
    )

    failed = len(results) - parked

    print()
    print("-" * 60)
    print(f"Successfully parked : {parked}")
    print(f"Parking failed      : {failed}")
    print(f"Occupancy rate      : {parking.occupancy_rate():.2f}%")
    print("=" * 60)


if __name__ == "__main__":
    main()