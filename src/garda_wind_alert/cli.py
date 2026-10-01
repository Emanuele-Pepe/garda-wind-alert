"""Entry point: `uv run garda-wind-alert [--config config.yaml] [--dry-run] [--always-send]`.

Flow:
  1. load config
  2. target days = today (Europe/Rome) + each of days_ahead
  3. for each spot: fetch -> parse -> append to CSV -> evaluate each target day
  4. format report, print it
  5. unless --dry-run: send email if any verdict is GO (or --always-send)
Return 0 on success, non-zero on failure (so GitHub Actions shows a red run).
"""

import argparse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from garda_wind_alert.config import load_config
from garda_wind_alert.forecast import fetch_raw, parse_hourly
from garda_wind_alert.notify import format_report, send_email
from garda_wind_alert.rules import evaluate_day
from garda_wind_alert.storage import append_forecast

TZ = ZoneInfo("Europe/Rome")


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lake Garda wind alert")
    parser.add_argument("--config", default="config.yaml", help="Path to the YAML config")
    parser.add_argument("--dry-run", action="store_true", help="Print only: no CSV, no email")
    parser.add_argument("--always-send", action="store_true", help="Email even with no GO day")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    cfg = load_config(args.config)

    now = datetime.now(TZ)
    target_days = [now.date() + timedelta(days=d) for d in cfg.days_ahead]
    forecast_days = max(cfg.days_ahead) + 1

    verdicts = []
    for spot in cfg.spots:
        points = parse_hourly(fetch_raw(spot, cfg.model, forecast_days))
        if not args.dry_run:
            append_forecast(cfg.data_path, now, spot, cfg.model, points)
        for day in target_days:
            verdicts.append(evaluate_day(points, spot, day))

    subject, body = format_report(verdicts)
    print(subject)
    print()
    print(body)

    if args.dry_run:
        return 0
    if any(v.go for v in verdicts) or args.always_send:
        send_email(subject, body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
