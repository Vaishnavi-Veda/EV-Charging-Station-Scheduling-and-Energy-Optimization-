class Vehicle:
    def __init__(self, license_number, plate_number, owner_name, vehicle_type):
        self.license_number = license_number
        self.plate_number = plate_number
        self.owner_name = owner_name
        self.vehicle_type = vehicle_type


class ParkingSlot:
    def __init__(self, slot_id, size, vehicle=None):
        self.slot_id = slot_id
        self.size = size
        self.vehicle = vehicle
        self.is_occupied = vehicle is not None

    def park_vehicle(self, vehicle):
        if self.is_occupied:
            raise ValueError("Cannot park in an occupied slot")
        self.vehicle = vehicle
        self.is_occupied = True

    def remove_vehicle(self):
        if not self.is_occupied:
            raise ValueError("Cannot remove a vehicle from an empty slot")
        vehicle = self.vehicle
        self.vehicle = None
        self.is_occupied = False
        return vehicle


class ParkingService:
    def __init__(self):
        self._slots = []

    def add_slot(self, slot):
        self._slots.append(slot)

    def total_slots(self):
        return len(self._slots)

    def find_available_slot(self, size):
        for slot in self._slots:
            if slot.size == size and not slot.is_occupied:
                return slot
        return None

    def park_vehicle(self, vehicle, size):
        slot = self.find_available_slot(size)
        if slot is None:
            return None
        slot.park_vehicle(vehicle)
        return slot

    def get_occupied_slots(self):
        return [slot for slot in self._slots if slot.is_occupied]

    def get_available_slots(self):
        return [slot for slot in self._slots if not slot.is_occupied]

    def remove_vehicle(self, slot_id):
        for slot in self._slots:
            if slot.slot_id == slot_id:
                return slot.remove_vehicle()
        raise ValueError(f"Slot {slot_id} not found")


class PaymentService:
    def process_payment(self, amount, method):
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero")

        normalized = str(method).lower()
        if normalized not in {"cash", "card", "upi"}:
            raise ValueError("Unsupported payment method")

        return f"Paid {amount:.2f} through {normalized.title()}"
