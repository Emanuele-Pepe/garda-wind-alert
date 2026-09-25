"""Append every forecast to a CSV. This log is the dataset for project 3
(forecast vs. measured wind), so never drop columns once it has data."""

from datetime import datetime
from pathlib import Path

from garda_wind_alert.config import Spot
from garda_wind_alert.forecast import HourlyPoint

COLUMNS = ["run_at", "spot", "model", "time", "speed_kn", "gust_kn", "direction_deg"]


def append_forecast(
    path: Path, run_at: datetime, spot: Spot, model: str, points: list[HourlyPoint]
) -> None:
    """Append one row per point. Create the file (and parent dir) with header if missing."""
    raise NotImplementedError
