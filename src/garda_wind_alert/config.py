"""Load config.yaml into typed objects."""

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Spot:
    name: str
    wind_name: str
    latitude: float
    longitude: float
    start_hour: int  # inclusive, local time
    end_hour: int  # exclusive, local time
    dir_from: float  # degrees the wind comes FROM; range may wrap around 0
    dir_to: float
    min_speed_kn: float
    min_hours: int


@dataclass(frozen=True)
class Config:
    spots: list[Spot]
    days_ahead: list[int]
    model: str
    data_path: Path


def load_config(path: str | Path) -> Config:
    """Read the YAML file and return a Config.

    Fail loudly (ValueError) on missing keys or on start_hour >= end_hour.
    """
    raw = yaml.safe_load(Path(path).read_text())
    try:
        spots = [Spot(**s) for s in raw["spots"]]
        config = Config(
            spots=spots,
            days_ahead=raw["days_ahead"],
            model=raw["model"],
            data_path=Path(raw["data_path"]),
        )
    except (KeyError, TypeError) as e:
        raise ValueError(f"Invalid config {path}: {e}") from e
    for s in spots:
        if s.start_hour >= s.end_hour:
            raise ValueError(f"Spot {s.name}: start_hour must be before end_hour")
    return config
