from datetime import datetime

from garda_wind_alert.forecast import parse_hourly

PAYLOAD = {
    "hourly": {
        "time": ["2026-09-27T13:00", "2026-09-27T14:00", "2026-09-27T15:00"],
        "wind_speed_10m": [12.5, None, 15.0],
        "wind_gusts_10m": [18.0, 20.0, 22.1],
        "wind_direction_10m": [200, 190, 185],
    }
}


def test_parse_hourly_skips_nulls_and_parses_times():
    points = parse_hourly(PAYLOAD)
    assert len(points) == 2
    assert points[0].time == datetime(2026, 9, 27, 13)
    assert points[0].speed_kn == 12.5
    assert points[1].gust_kn == 22.1
    assert points[1].direction_deg == 185


def test_parse_hourly_empty():
    empty = {
        "hourly": {"time": [], "wind_speed_10m": [], "wind_gusts_10m": [], "wind_direction_10m": []}
    }
    assert parse_hourly(empty) == []

def test_parse_hourly_skips_null_direction():
    payload = {
        "hourly": {
            "time": ["2026-09-27T13:00", "2026-09-27T14:00"],
            "wind_speed_10m": [12.0, 13.0],
            "wind_gusts_10m": [18.0, 19.0],
            "wind_direction_10m": [None, 200],
        }
    }
    points = parse_hourly(payload)
    assert len(points) == 1
    assert points[0].direction_deg == 200
