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
    # 1. points on the right day, inside the time window
    window = [
        p for p in points if p.time.date() == day and spot.start_hour <= p.time.hour < spot.end_hour
    ]

    # 2. hours with the right direction AND enough speed
    good = [
        p
        for p in window
        if direction_in_range(p.direction_deg, spot.dir_from, spot.dir_to)
        and p.speed_kn >= spot.min_speed_kn
    ]

    # 3. maxima over the whole window, 0 if the window is empty
    max_speed = max((p.speed_kn for p in window), default=0)
    max_gust = max((p.gust_kn for p in window), default=0)

    # 4. build the verdict
    return DayVerdict(
        spot=spot.name,
        wind_name=spot.wind_name,
        day=day,
        go=len(good) >= spot.min_hours,
        good_hours=len(good),
        max_speed_kn=max_speed,
        max_gust_kn=max_gust,
    )
