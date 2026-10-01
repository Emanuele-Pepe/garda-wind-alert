from garda_wind_alert import cli

EMPTY_PAYLOAD = {
    "hourly": {"time": [], "wind_speed_10m": [], "wind_gusts_10m": [], "wind_direction_10m": []}
}


def patch_io(monkeypatch) -> list:
    """Replace network, CSV and email with fakes. Return the list of sent emails."""
    sent = []
    monkeypatch.setattr(cli, "fetch_raw", lambda spot, model, days: EMPTY_PAYLOAD)
    monkeypatch.setattr(cli, "append_forecast", lambda *args: None)
    monkeypatch.setattr(cli, "send_email", lambda subject, body: sent.append(subject))
    return sent


def test_no_email_when_no_go(monkeypatch):
    sent = patch_io(monkeypatch)
    exit_code = cli.main([])
    assert exit_code == 0
    assert sent == []


def test_always_send_sends_email(monkeypatch):
    sent = patch_io(monkeypatch)
    exit_code = cli.main(["--always-send"])
    assert exit_code == 0
    assert len(sent)==1
    assert str(sent[0]).startswith("No wind")   