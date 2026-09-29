from datetime import datetime

import pytest
import requests

from garda_wind_alert import forecast
from garda_wind_alert.forecast import fetch_raw, parse_hourly

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


class FakeResponse:
    """Stands in for requests.Response: only the two methods fetch_raw uses."""

    def __init__(self, payload: dict, status: int = 200):
        self.payload = payload
        self.status = status

    def raise_for_status(self) -> None:
        if self.status >= 400:
            raise requests.HTTPError(f"HTTP {self.status}")

    def json(self) -> dict:
        return self.payload


def test_fetch_raw_sends_expected_params(monkeypatch, ora_spot):
    calls = {}

    def fake_get(url, params, timeout):
        calls.update(url=url, params=params, timeout=timeout)
        return FakeResponse({"hourly": {}})

    monkeypatch.setattr(forecast.requests, "get", fake_get)

    result = fetch_raw(ora_spot, "best_match", 3)

    assert result == {"hourly": {}}
    assert calls["params"]["latitude"] == ora_spot.latitude
    assert calls["params"]["wind_speed_unit"] == "kn"
    assert calls["params"]["timezone"] == "Europe/Rome"
    assert calls["params"]["forecast_days"] == 3
    assert calls["timeout"] > 0


def test_fetch_raw_raises_on_http_error(monkeypatch, ora_spot):
    def fake_get(url, params, timeout):
        return FakeResponse({}, status=500)

    monkeypatch.setattr(forecast.requests, "get", fake_get)

    with pytest.raises(requests.HTTPError):
        fetch_raw(ora_spot, "best_match", 3)
