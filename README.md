# Smart Parking System in Python

A comprehensive, object-oriented simulation of a smart parking lot system. This project demonstrates core OOP principles to manage a parking facility that can accommodate various vehicle types with different-sized parking spots, calculate parking fees, and handle a mock payment process.

---

## 🌟 Features

* **Object-Oriented Design**: Built with a clear, modular structure using classes for `Vehicle`, `ParkingSpot`, `ParkingLot`, and `Payment`.
* **Multiple Vehicle Types**: Supports different types of vehicles, including `Bike`, `Car`, `SUV`, and `Truck`, each with unique properties and parking fees.
* **Variable Spot Sizes**: The parking lot consists of spots of various sizes (`S`, `M`, `L`, `XL`) to efficiently accommodate different vehicles.
* **Smart Spot Allocation**: The system intelligently assigns the smallest possible spot that can fit an incoming vehicle. For example, a `Bike` can park in an `S`, `M`, `L`, or `XL` spot, but the system will prioritize an available `S` spot first.
* **Fee Calculation**: Automatically calculates the parking fee based on the vehicle type and the duration of parking (in hours).
* **Mock Payment Gateway**: Simulates a payment process with options for Cash, Card, or UPI.

---

## 📂 Project Structure

The project is organized into logical modules for better readability and maintenance:

```
smart-parking-system/
├── main.py             # Main script to run the simulation
├── vehicles.py         # Contains the base Vehicle class and its subclasses (Bike, Car, etc.)
├── parking_system.py   # Core logic for ParkingSpot and ParkingLot
└── payment_gateway.py  # A simple mock payment processing module
```

---

## ⚙️ How It Works

1.  **Initialization**: The `main.py` script initializes a `ParkingLot` and populates it with a random assortment of parking spots (`S`, `M`, `L`, `XL`).
2.  **Vehicle Classes**: The `vehicles.py` module defines a base `Vehicle` class with common attributes like `plate` and `owner_name`. Subclasses like `Car` and `Truck` inherit from `Vehicle` and add specific attributes (e.g., `seats`, `max_load_capacity`).
3.  **Parking Logic**:
    * When a vehicle needs to be parked, the `park_vehicle()` method in `ParkingLot` determines the minimum required spot size.
    * It then iterates through the available spots, starting from the smallest suitable size, and assigns the vehicle to the first empty spot it finds.
4.  **Unparking and Payment**:
    * The `unpark_vehicle()` method searches for a vehicle by its license plate.
    * Once found, it calculates the total cost based on the vehicle's hourly fee and the duration of the stay.
    * The vehicle is removed from the spot, making it available again.
    * Finally, the `Payment` class is used to simulate the payment transaction.

---

## 🚀 How to Run

1.  **Prerequisites**:
    * Python 3.6 or higher.

2.  **Clone the repository**:
    ```bash
    git clone [https://github.com/your-username/smart-parking-system.git](https://github.com/your-username/smart-parking-system.git)
    ```

3.  **Navigate to the project directory**:
    ```bash
    cd smart-parking-system
    ```

4.  **Run the main script**:
    ```bash
    python main.py
    ```

---

## 📋 Example Output

Running `main.py` will produce an output similar to this, showing the status of all parking spots, the cost calculation for an unparked vehicle, and the payment confirmation.

```
------------------------------
Size: S
------------------------------
Size: S
Slot Status:
	License: B101
	Plate: TS07AB1234
	Owner Name: Rahul Kumar
	Helmet Required: True
Size: S
Slot Status:
	License: B102
	Plate: TS08BC2345
	Owner Name: Suresh Singh
	Helmet Required: False
...
(output continues for all spots)
...
------------------------------
==============================
Cost: 400
==============================
Payment Method:
1. Cash
2. Card
3. UPI
Choose payment method: 2
Paid 400 through Card
==============================
          Thank You
==============================
```

---

<!--
## 🛠️ Future Improvements

This project serves as a strong foundation. Here are some potential features to add:

* **Database Integration**: Store parking data, vehicle logs, and transactions in a database like SQLite or PostgreSQL.
* **GUI/Web Interface**: Build a graphical user interface using Tkinter, or a web interface using Flask/Django to visualize the parking lot and interact with the system.
* **Real-time Availability**: Implement a system to track spot availability in real-time.
* **Error Handling**: Improve error handling for cases like a full parking lot or an invalid license plate.
* **Unit Testing**: Add unit tests to ensure the reliability of each module.
-->
