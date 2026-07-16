from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Alarm:
    id: int
    time: datetime

    def to_dict(self) -> dict:
        return {"id": self.id, "time": self.time.isoformat()}

    @classmethod
    def from_dict(cls, data: dict) -> "Alarm":
        return cls(id=data["id"], time=datetime.fromisoformat(data["time"]))
