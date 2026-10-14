import pytest  # type: ignore[import-not-found]

from models import Vehicle, ParkingSlot
from services import ParkingService, PaymentService


def create_vehicle():
    return Vehicle(
        "B101",
        "TS07AB1234",
        "Rahul Kumar",
        "Car"
    )


def test_add_parking_slot():
    service = ParkingService()

    slot = ParkingSlot("S01", "S")

    service.add_slot(slot)

    assert service.total_slots() == 1


def test_find_available_slot():
    service = ParkingService()

    slot = ParkingSlot("S01", "S")
    service.add_slot(slot)

    result = service.find_available_slot("S")

    assert result == slot


def test_park_vehicle():
    service = ParkingService()

    slot = ParkingSlot("S01", "S")
    service.add_slot(slot)

    vehicle = create_vehicle()

    result = service.park_vehicle(vehicle, "S")

    assert result == slot
    assert slot.is_occupied is True


def test_no_available_slot():
    service = ParkingService()

    slot = ParkingSlot("S01", "S")
    service.add_slot(slot)

    vehicle = create_vehicle()

    service.park_vehicle(vehicle, "S")

    second_vehicle = Vehicle(
        "B102",
        "TS08BC2345",
        "Suresh Singh",
        "Car"
    )

    result = service.park_vehicle(second_vehicle, "S")

    assert result is None


def test_occupied_slots():
    service = ParkingService()

    slot1 = ParkingSlot("S01", "S")
    slot2 = ParkingSlot("S02", "S")

    service.add_slot(slot1)
    service.add_slot(slot2)

    vehicle = create_vehicle()

    service.park_vehicle(vehicle, "S")

    occupied = service.get_occupied_slots()

    assert len(occupied) == 1
    assert occupied[0] == slot1


def test_available_slots():
    service = ParkingService()

    slot1 = ParkingSlot("S01", "S")
    slot2 = ParkingSlot("S02", "S")

    service.add_slot(slot1)
    service.add_slot(slot2)

    vehicle = create_vehicle()

    service.park_vehicle(vehicle, "S")

    available = service.get_available_slots()

    assert len(available) == 1
    assert available[0] == slot2


def test_remove_vehicle():
    service = ParkingService()

    slot = ParkingSlot("S01", "S")
    service.add_slot(slot)

    vehicle = create_vehicle()

    service.park_vehicle(vehicle, "S")

    removed = service.remove_vehicle("S01")

    assert removed == vehicle
    assert slot.is_occupied is False


def test_payment_cash():
    payment = PaymentService()

    result = payment.process_payment(400, "cash")

    assert result == "Paid 400.00 through Cash"


def test_payment_card():
    payment = PaymentService()

    result = payment.process_payment(400, "card")

    assert result == "Paid 400.00 through Card"


def test_payment_upi():
    payment = PaymentService()

    result = payment.process_payment(400, "upi")

    assert result == "Paid 400.00 through Upi"


def test_invalid_payment_method():
    payment = PaymentService()

    with pytest.raises(ValueError):
        payment.process_payment(400, "bitcoin")


def test_invalid_payment_amount():
    payment = PaymentService()

    with pytest.raises(ValueError):
        payment.process_payment(0, "cash")