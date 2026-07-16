from datetime import datetime

from alarm import cli


class FixedDateTime(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 7, 16, 12, 0, 0)


def test_parse_time_rolls_to_tomorrow_if_already_passed_today(monkeypatch):
    monkeypatch.setattr(cli, "datetime", FixedDateTime)
    assert cli.parse_time("09:00") == datetime(2026, 7, 17, 9, 0)


def test_parse_time_stays_today_if_still_upcoming(monkeypatch):
    monkeypatch.setattr(cli, "datetime", FixedDateTime)
    assert cli.parse_time("15:30") == datetime(2026, 7, 16, 15, 30)
