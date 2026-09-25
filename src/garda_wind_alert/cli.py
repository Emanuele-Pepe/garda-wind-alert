"""Entry point: `uv run garda-wind-alert [--config config.yaml] [--dry-run] [--always-send]`.

Flow:
  1. load config
  2. target days = today (Europe/Rome) + each of days_ahead
  3. for each spot: fetch -> parse -> append to CSV -> evaluate each target day
  4. format report, print it
  5. unless --dry-run: send email if any verdict is GO (or --always-send)
Return 0 on success, non-zero on failure (so GitHub Actions shows a red run).
"""


def main(argv: list[str] | None = None) -> int:
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
