"""Build the report and send it by email (Gmail SMTP with an app password)."""

import os
import smtplib
from email.message import EmailMessage

from garda_wind_alert.rules import DayVerdict


def format_report(verdicts: list[DayVerdict]) -> tuple[str, str]:
    go = [v for v in verdicts if v.go]

    if go:
        labels = [f"{v.spot} {v.wind_name} {v.day:%a %d/%m}" for v in go]
        subject = "GO: " + ", ".join(labels)
    else:
        n_days = len({v.day for v in verdicts})
        subject = f"No wind: next {n_days} days"

    lines = [
        f"{'✅' if v.go else '❌'} {v.day:%a %d/%m}  {v.spot} ({v.wind_name}): "
        f"{v.good_hours} good h, max {v.max_speed_kn:.0f} kn, gust {v.max_gust_kn:.0f} kn"
        for v in verdicts
    ]
    body = "\n".join(lines)
    return subject, body


def send_email(subject: str, body: str) -> None:
    """Send via SMTP_SSL. Read SMTP_HOST (default smtp.gmail.com), SMTP_PORT (default 465),
    SMTP_USER, SMTP_PASSWORD, ALERT_TO from environment variables."""
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "465"))
    user = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASSWORD"]
    to = os.environ["ALERT_TO"]

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to
    msg.set_content(body)

    with smtplib.SMTP_SSL(host, port, timeout=30) as server:
        server.login(user, password)
        server.send_message(msg)
