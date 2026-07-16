from __future__ import annotations

import time
from datetime import datetime

from alarm.models import Alarm
from alarm.storage import delete_alarm, load_alarms

POLL_INTERVAL_SECONDS = 5


def next_alarm(alarms: list[Alarm]) -> Alarm | None:
    if not alarms:
        return None
    return min(alarms, key=lambda a: a.time)


def ring(alarm: Alarm) -> None:
    print("\a")
    print(f"ALARM! [{alarm.id}] {alarm.time.strftime('%Y-%m-%d %H:%M')}")


def run() -> None:
    print("Scheduler started. Waiting for alarms... (Ctrl+C to stop)")
    try:
        while True:
            alarm = next_alarm(load_alarms())

            if alarm is None:
                time.sleep(POLL_INTERVAL_SECONDS)
                continue

            wait_seconds = (alarm.time - datetime.now()).total_seconds()
            if wait_seconds > 0:
                time.sleep(wait_seconds)

            ring(alarm)
            delete_alarm(alarm.id)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")
