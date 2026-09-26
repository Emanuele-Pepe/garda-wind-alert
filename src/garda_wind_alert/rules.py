"""Decide whether a day is worth driving to the lake. Pure functions, no I/O."""

from dataclasses import dataclass
from datetime import date

from garda_wind_alert.config import Spot
from garda_wind_alert.forecast import HourlyPoint


@dataclass(frozen=True)
class DayVerdict:
    spot: str
    wind_name: str
    day: date
    go: bool
    good_hours: int  # hours in the window meeting direction AND speed
    max_speed_kn: float  # max mean speed inside the window (0 if no data)
    max_gust_kn: float  # max gust inside the window (0 if no data)


def direction_in_range(deg: float, dir_from: float, dir_to: float) -> bool:
    """True if deg is inside [dir_from, dir_to], handling wrap-around (e.g. 330 -> 30)."""
    deg = deg % 360

    if dir_from <= dir_to:
        return dir_from <= deg <= dir_to
    else:
        return deg >= dir_from or deg <= dir_to


def evaluate_day(points: list[HourlyPoint], spot: Spot, day: date) -> DayVerdict:
    """Look only at points on `day` with start_hour <= hour < end_hour.

    go = good_hours >= spot.min_hours.
    """
    raise NotImplementedError
