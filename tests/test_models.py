from datetime import datetime

from alarm.models import Alarm


def test_alarm_round_trips_through_dict():
    alarm = Alarm(id=1, time=datetime(2026, 7, 16, 9, 0))
    restored = Alarm.from_dict(alarm.to_dict())
    assert restored == alarm
