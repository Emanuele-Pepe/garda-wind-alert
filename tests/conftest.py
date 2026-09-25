from datetime import datetime

import pytest

from garda_wind_alert.config import Spot
from garda_wind_alert.forecast import HourlyPoint


@pytest.fixture
def ora_spot() -> Spot:
    return Spot(
        name="Torbole",
        wind_name="Ora",
        latitude=45.871,
        longitude=10.874,
        start_hour=12,
        end_hour=19,
        dir_from=160,
        dir_to=230,
        min_speed_kn=12,
        min_hours=2,
    )


@pytest.fixture
def peler_spot() -> Spot:
    return Spot(
        name="Malcesine",
        wind_name="Peler",
        latitude=45.764,
        longitude=10.809,
        start_hour=5,
        end_hour=11,
        dir_from=330,
        dir_to=30,
        min_speed_kn=14,
        min_hours=2,
    )


def point(iso: str, speed: float, direction: float, gust: float | None = None) -> HourlyPoint:
    return HourlyPoint(
        time=datetime.fromisoformat(iso),
        speed_kn=speed,
        gust_kn=gust if gust is not None else speed + 4,
        direction_deg=direction,
    )
