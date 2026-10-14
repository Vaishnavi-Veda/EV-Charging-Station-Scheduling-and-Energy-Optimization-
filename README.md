# EV Charging Station Scheduling and Energy Optimization

This project schedules electric vehicles across charging stations with limited capacity. Each request includes an arrival time, a departure deadline, required energy, and a priority.

## Frontend

Open `index.html` in a browser to use the interactive scheduler. Add or remove charging stations and requests, load sample data, and compare the greedy and dynamic programming schedules.

## Python demo

Run the command-line scheduling demo with Python 3.10 or later:

```bash
python ev_charging_demo.py
```

The `ev_charging` package provides validated models for charging stations and EV requests, plus greedy and dynamic programming scheduling algorithms.

## Tests

Run the test suite with pytest:

```bash
pytest -q
```

## Project structure

```text
ev_charging/
  __init__.py
  models.py
  scheduler.py
tests/
  test_ev_charging.py
app.js
ev_charging_demo.py
index.html
styles.css
```
