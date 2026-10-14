from ev_charging import ChargingStation, EVChargingScheduler, EVRequest


def sample():
    stations = [
        ChargingStation("A", 20, 5),
        ChargingStation("B", 30, 7),
    ]
    requests = [
        EVRequest("EV1", 0, 3, 40, 2),
        EVRequest("EV2", 1, 4, 30, 3),
        EVRequest("EV3", 3, 6, 20, 1),
    ]
    return stations, requests


def test_greedy_assigns_requests():
    stations, requests = sample()
    result = EVChargingScheduler(stations).schedule_greedy(requests)
    assert result.schedules
    assert result.total_energy_kwh > 0


def test_dynamic_programming_assigns_requests():
    stations, requests = sample()
    result = EVChargingScheduler(stations).schedule_dynamic_programming(requests)
    assert result.schedules
    assert len({s.vehicle_id for s in result.schedules}) == len(result.schedules)


def test_invalid_request_rejected_at_model_level():
    try:
        EVRequest("BAD", 4, 3, 20)
    except ValueError:
        assert True
    else:
        assert False
