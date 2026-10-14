from payment_gateway import Payment
from vehicles import Bike, Car, SUV, Truck
from parking_system import ParkingLot, ParkingSpot
import random

# Program Initialization

NO_OF_PARKING_SPOTS = 20

# 1. Create Parking Lot
lot = ParkingLot("CityMall Parking")

# 2. Add Parking Spots
# Adding parking spots
for _ in range(NO_OF_PARKING_SPOTS):
    lot.add_spot(ParkingSpot(random.choice(ParkingSpot.sizes)))

# 3. Vehicles
bikes = [
    Bike("B101", "TS07AB1234", "Rahul Kumar", True),
    Bike("B102", "TS08BC2345", "Suresh Singh", False),
    Bike("B103", "TS09CD3456", "Kavya Reddy", True),
    Bike("B104", "TS10DE4567", "Amit Sharma", False)
]

cars = [
    Car("C201", "TS05EF5678", "Priya Sharma", 5),
    Car("C202", "TS12FG6789", "Deepak Gupta", 4),
    Car("C203", "TS04GH7890", "Sneha Patel", 7),
    Car("C204", "TS13IJ9012", "Rohan Mehta", 5)
]

suvs = [
    SUV("S301", "TS09KL9012", "Anjali Rao", True),
    SUV("S302", "TS11MN0123", "Vikram Verma", False),
    SUV("S303", "TS08OP1234", "Neha Joshi", True),
]

trucks = [
    Truck("T401", "TS15QR4455", "Ravi Prasad", 12),
    Truck("T402", "TS06RS5566", "Manoj Kumar", 16.5),
    Truck("T403", "TS10ST6677", "Sunita Yadav", 10),
    Truck("T404", "TS07UV7788", "Balaji Naidu", 20)
]

# 4. Parking Vehicles
# Bikes
for i in range(2):
    lot.park_vehicle(bikes[i])

# Cars
for i in range(3):
    lot.park_vehicle(cars[i])

# SUVs
for i in range(2):
    lot.park_vehicle(suvs[i])

# Trucks
for i in range(3):
    lot.park_vehicle(trucks[i])

# 5. Testing
lot.show_spots()

cost, vehicle = lot.unpark_vehicle("TS15QR4455", hours=4)
print('='*30)
print(f'Cost: {cost}')
print('='*30)

payment = Payment()
payment.process_payment(cost)

print('='*30)
print('Thank You'.center(30))
print('='*30)
