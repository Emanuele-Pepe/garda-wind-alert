from pathlib import Path

import pytest

from garda_wind_alert.config import load_config

ROOT = Path(__file__).resolve().parents[1]


def test_loads_repo_config():
    cfg = load_config(ROOT / "config.yaml")
    assert [s.name for s in cfg.spots] == ["Malcesine", "Torbole"]
    assert cfg.days_ahead == [1, 2]
    assert cfg.data_path == Path("data/forecasts.csv")


def test_rejects_inverted_window(tmp_path):
    bad = tmp_path / "c.yaml"
    bad.write_text(
        """
days_ahead: [1]
model: best_match
data_path: data/f.csv
spots:
  - {name: X, wind_name: Y, latitude: 0, longitude: 0, start_hour: 15, end_hour: 12,
     dir_from: 0, dir_to: 90, min_speed_kn: 10, min_hours: 1}
"""
    )
    with pytest.raises(ValueError):
        load_config(bad)


def test_rejects_missing_key(tmp_path):
    bad = tmp_path / "c.yaml"
    bad.write_text("days_ahead: [1]\nmodel: best_match\nspots: []\n")
    with pytest.raises(ValueError):
        load_config(bad)
