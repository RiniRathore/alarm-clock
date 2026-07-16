from __future__ import annotations

import json
import os
from pathlib import Path

from alarm.models import Alarm

DEFAULT_PATH = Path("alarms.json")


def load_alarms(path: Path = DEFAULT_PATH) -> list[Alarm]:
    path = Path(path)
    if not path.exists():
        return []
    with open(path, "r") as f:
        data = json.load(f)
    return [Alarm.from_dict(d) for d in data]


def save_alarms(alarms: list[Alarm], path: Path = DEFAULT_PATH) -> None:
    path = Path(path)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with open(tmp_path, "w") as f:
        json.dump([a.to_dict() for a in alarms], f, indent=2)
    os.replace(tmp_path, path)


def add_alarm(alarm: Alarm, path: Path = DEFAULT_PATH) -> None:
    alarms = load_alarms(path)
    alarms.append(alarm)
    save_alarms(alarms, path)


def delete_alarm(alarm_id: int, path: Path = DEFAULT_PATH) -> None:
    alarms = load_alarms(path)
    alarms = [a for a in alarms if a.id != alarm_id]
    save_alarms(alarms, path)
