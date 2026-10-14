# EV Charging Station Scheduling Using Greedy and Dynamic Programming

This is an extended version of the original **Smart Parking System** project. All original project files are retained, while a new EV charging scheduling module has been added.

## Real-world problem

EV charging stations have limited chargers while vehicles arrive with different arrival times, departure deadlines, energy requirements, and priority levels. This project schedules vehicles so that charger capacity is used efficiently.

## Algorithms implemented

### 1. Greedy Algorithm
The greedy scheduler sorts requests using earliest departure time, priority, energy demand, and arrival time. It assigns each request to the earliest available feasible charger.

### 2. Dynamic Programming
The DP scheduler uses **Weighted Interval Scheduling**. Each feasible charging session receives a value based on `priority × energy needed`, and the algorithm selects non-overlapping sessions that maximize the total value.

## New files

```text
ev_charging/
  __init__.py
  models.py
  scheduler.py
ev_charging_demo.py
tests/test_ev_charging.py
EV_PROJECT_README.md
```

## Existing files retained

The original parking system, vehicle classes, services, payment gateway, datasets, performance tests, concurrency demo, HTML coverage files, and original tests remain in the project.

## Run EV demo

```bash
python ev_charging_demo.py
```

## Run tests

```bash
pytest -q
```

## Main concepts demonstrated

- Greedy scheduling
- Dynamic Programming / Weighted Interval Scheduling
- Object-Oriented Programming
- Data classes
- Validation and exception handling
- Multiple charging stations
- Time-window constraints
- Priority-based scheduling
- Energy and charging-cost calculation
- Unit testing

## Suggested project title

**EV Charging Station Scheduling and Energy Optimization Using Greedy and Dynamic Programming Algorithms**
