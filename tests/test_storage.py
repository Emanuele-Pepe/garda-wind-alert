import csv
from datetime import datetime

from garda_wind_alert.storage import COLUMNS, append_forecast
from tests.conftest import point


def test_append_creates_file_with_header_then_appends(tmp_path, ora_spot):
    path = tmp_path / "data" / "forecasts.csv"
    run_at = datetime(2026, 9, 26, 6, 15)
    pts = [point("2026-09-27T13:00", 13, 200), point("2026-09-27T14:00", 15, 190)]

    append_forecast(path, run_at, ora_spot, "best_match", pts)
    append_forecast(path, run_at, ora_spot, "best_match", pts[:1])

    with path.open() as f:
        rows = list(csv.reader(f))
    assert rows[0] == COLUMNS
    assert len(rows) == 1 + 3  # header written once
    assert rows[1][1] == "Torbole"
    assert rows[1][2] == "best_match"
