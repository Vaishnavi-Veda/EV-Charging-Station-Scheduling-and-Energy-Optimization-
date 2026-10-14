import pytest

from models import Vehicle, ParkingSlot


def test_vehicle_creation():
    vehicle = Vehicle(
        "B101",
        "TS07AB1234",
        "Rahul Kumar",
        "Car"
    )

    assert vehicle.license_number == "B101"
    assert vehicle.plate_number == "TS07AB1234"
    assert vehicle.owner_name == "Rahul Kumar"
    assert vehicle.vehicle_type == "Car"


def test_parking_slot_creation():
    slot = ParkingSlot("S01", "S")

    assert slot.slot_id == "S01"
    assert slot.size == "S"
    assert slot.vehicle is None
    assert slot.is_occupied is False


def test_park_vehicle():
    vehicle = Vehicle(
        "B101",
        "TS07AB1234",
        "Rahul Kumar",
        "Car"
    )

    slot = ParkingSlot("S01", "S")

    slot.park_vehicle(vehicle)

    assert slot.vehicle == vehicle
    assert slot.is_occupied is True


def test_remove_vehicle():
    vehicle = Vehicle(
        "B101",
        "TS07AB1234",
        "Rahul Kumar",
        "Car"
    )

    slot = ParkingSlot("S01", "S")
    slot.park_vehicle(vehicle)

    removed = slot.remove_vehicle()

    assert removed == vehicle
    assert slot.vehicle is None
    assert slot.is_occupied is False


def test_cannot_park_in_occupied_slot():
    vehicle1 = Vehicle(
        "B101",
        "TS07AB1234",
        "Rahul Kumar",
        "Car"
    )

    vehicle2 = Vehicle(
        "B102",
        "TS08BC2345",
        "Suresh Singh",
        "Car"
    )

    slot = ParkingSlot("S01", "S")

    slot.park_vehicle(vehicle1)

    with pytest.raises(ValueError):
        slot.park_vehicle(vehicle2)


def test_cannot_remove_from_empty_slot():
    slot = ParkingSlot("S01", "S")

    with pytest.raises(ValueError):
        slot.remove_vehicle()