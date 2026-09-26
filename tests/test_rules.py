from datetime import date

import pytest

from garda_wind_alert.rules import direction_in_range, evaluate_day
from tests.conftest import point

DAY = date(2026, 9, 27)


@pytest.mark.parametrize(
    ("deg", "expected"),
    [(180, True), (160, True), (230, True), (159, False), (231, False), (0, False)],
)
def test_direction_simple_range(deg, expected):
    assert direction_in_range(deg, 160, 230) is expected


def test_direction_360_equals_north():
    assert direction_in_range(360, 0, 30) is True


@pytest.mark.parametrize(
    ("deg", "expected"),
    [
        (350, True),
        (0, True),
        (360, True),
        (15, True),
        (330, True),
        (30, True),
        (90, False),
        (329, False),
        (31, False),
    ],
)
def test_direction_wraps_around_north(deg, expected):
    assert direction_in_range(deg, 330, 30) is expected


def test_ora_go_when_enough_good_hours(ora_spot):
    points = [
        point("2026-09-27T13:00", 13, 200),
        point("2026-09-27T14:00", 16, 190, gust=22),
        point("2026-09-27T15:00", 11, 190),  # too light
    ]
    v = evaluate_day(points, ora_spot, DAY)
    assert v.go is True
    assert v.good_hours == 2
    assert v.max_speed_kn == 16
    assert v.max_gust_kn == 22
    assert (v.spot, v.wind_name, v.day) == ("Torbole", "Ora", DAY)


def test_no_go_when_wrong_direction(ora_spot):
    points = [point(f"2026-09-27T{h}:00", 18, 20) for h in range(12, 19)]  # strong but northerly
    v = evaluate_day(points, ora_spot, DAY)
    assert v.go is False
    assert v.good_hours == 0


def test_hours_outside_window_are_ignored(ora_spot):
    points = [
        point("2026-09-27T11:00", 20, 200),  # before window
        point("2026-09-27T12:00", 20, 200),  # first hour, inclusive
        point("2026-09-27T19:00", 20, 200),  # end hour, exclusive
    ]
    v = evaluate_day(points, ora_spot, DAY)
    assert v.good_hours == 1
    assert v.go is False


def test_other_days_are_ignored(peler_spot):
    points = [
        point("2026-09-26T07:00", 20, 0),
        point("2026-09-26T08:00", 20, 0),
        point("2026-09-27T07:00", 20, 350),
        point("2026-09-27T08:00", 20, 10),
    ]
    v = evaluate_day(points, peler_spot, DAY)
    assert v.good_hours == 2
    assert v.go is True


def test_no_data_for_day(peler_spot):
    v = evaluate_day([], peler_spot, DAY)
    assert v.go is False
    assert v.good_hours == 0
    assert v.max_speed_kn == 0
    assert v.max_gust_kn == 0
