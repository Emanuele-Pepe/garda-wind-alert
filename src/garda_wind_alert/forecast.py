"""Fetch and parse hourly wind forecasts from Open-Meteo (free, no API key).

Docs: https://open-meteo.com/en/docs
Request params you need: latitude, longitude,
  hourly=wind_speed_10m,wind_gusts_10m,wind_direction_10m,
  wind_speed_unit=kn, timezone=Europe/Rome, forecast_days, models.

Response shape (trimmed):
  {"hourly": {"time": ["2026-09-26T00:00", ...],
              "wind_speed_10m": [3.1, ...],
              "wind_gusts_10m": [5.4, ...],
              "wind_direction_10m": [350, ...]}}
Values can be null.
"""

from dataclasses import dataclass
from datetime import datetime

from garda_wind_alert.config import Spot

API_URL = "https://api.open-meteo.com/v1/forecast"


@dataclass(frozen=True)
class HourlyPoint:
    time: datetime  # naive, local time (Europe/Rome)
    speed_kn: float
    gust_kn: float
    direction_deg: float


def fetch_raw(spot: Spot, model: str, forecast_days: int, timeout: float = 20) -> dict:
    """Call the API and return the JSON payload. Raise on HTTP errors."""
    raise NotImplementedError


def parse_hourly(payload: dict) -> list[HourlyPoint]:
    """Turn the payload into HourlyPoints, skipping hours with any null value."""
    raise NotImplementedError
