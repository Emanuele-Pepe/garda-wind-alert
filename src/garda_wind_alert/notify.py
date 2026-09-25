"""Build the report and send it by email (Gmail SMTP with an app password)."""

from garda_wind_alert.rules import DayVerdict


def format_report(verdicts: list[DayVerdict]) -> tuple[str, str]:
    """Return (subject, body).

    Subject lists the GO days, e.g. "GO: Torbole Ora sat 27/09"
    or "No wind: next 2 days" when nothing qualifies.
    Body: one line per verdict with good hours, max speed and max gust.
    """
    raise NotImplementedError


def send_email(subject: str, body: str) -> None:
    """Send via SMTP_SSL. Read SMTP_HOST (default smtp.gmail.com), SMTP_PORT (default 465),
    SMTP_USER, SMTP_PASSWORD, ALERT_TO from environment variables. Never hardcode secrets."""
    raise NotImplementedError
