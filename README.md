# garda-wind-alert

Every morning a GitHub Action checks the 2-day wind forecast for two Lake Garda spots
and emails me when it looks sailable:

| Spot | Wind | Window | Direction | Threshold |
|---|---|---|---|---|
| Malcesine | Peler (N, morning) | 05–11 | 330°–30° | ≥ 14 kn for ≥ 2 h |
| Torbole | Ora (S, afternoon) | 12–19 | 160°–230° | ≥ 12 kn for ≥ 2 h |

Every forecast is also logged to `data/forecasts.csv`, to later compare with measured wind.

## Definition of Done (v1)

- [ ] All tests in `tests/` pass; I added tests for `format_report` and `cli.main` (with `fetch_raw` mocked)
- [ ] `ruff check` and `ruff format --check` clean, CI green
- [ ] `uv run garda-wind-alert --dry-run` prints a real report locally
- [ ] Scheduled workflow ran **7 days in a row** without failures, CSV growing
- [ ] Screenshot of a real alert email below
- [ ] "Known limits" section filled with what I actually observed

Anything else goes to [ROADMAP.md](ROADMAP.md).

## Run locally

```bash
uv sync
uv run pytest
uv run garda-wind-alert --dry-run
```

To send email, set `SMTP_USER`, `SMTP_PASSWORD` (Gmail app password) and `ALERT_TO`.
In GitHub: Settings → Secrets and variables → Actions.

## Screenshot

_TODO_

## Known limits

- Ora and Peler are thermal/local winds; global and regional models tend to underestimate them.
  The thresholds are calibrated by feel, not validated. _To fill after one week of use._

## Data

Forecasts: [Open-Meteo](https://open-meteo.com/) (CC BY 4.0).
