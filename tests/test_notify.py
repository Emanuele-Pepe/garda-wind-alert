from datetime import date

from garda_wind_alert.notify import format_report
from garda_wind_alert.rules import DayVerdict


def verdict(spot: str, day: date, go: bool) -> DayVerdict:
    """Small helper so each test only specifies what it cares about."""
    return DayVerdict(
        spot=spot,
        wind_name="Ora",
        day=day,
        go=go,
        good_hours=3 if go else 0,
        max_speed_kn=16.4,
        max_gust_kn=22.0,
    )


def test_subject_lists_go_days():
    verdicts = [
        verdict("Torbole", date(2026, 9, 28), go=True),
        verdict("Torbole", date(2026, 9, 29), go=False),
    ]
    subject, _ = format_report(verdicts)
    assert subject == "GO: Torbole Ora Mon 28/09"


def test_subject_when_no_wind():
    verdicts = [
        verdict("Torbole", date(2026, 9, 28), go=False),
        verdict("Torbole", date(2026, 9, 29), go=False),
        verdict("Malcesine", date(2026, 9, 28), go=False),
        verdict("Malcesine", date(2026, 9, 29), go=False),
    ]
    subject, _ = format_report(verdicts)
    assert subject == "No wind: next 2 days"


def test_body_has_one_line_per_verdict():
    verdicts = [
        verdict("Torbole", date(2026, 9, 28), go=False),
        verdict("Torbole", date(2026, 9, 29), go=True),
        verdict("Malcesine", date(2026, 9, 28), go=False),
    ]
    _, body = format_report(verdicts)

    assert len(body.splitlines()) == 3
    assert "16 kn" in body.splitlines()[0]
