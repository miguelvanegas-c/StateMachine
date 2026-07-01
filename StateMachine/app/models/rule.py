
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass(slots=True)
class Rule:
    id: Optional[str] = None
    name: str = ""
    event_name: str = ""
    actual_version: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def create_new(name: str, event_name: str) -> 'Rule':
        now = datetime.now()
        return Rule(
            name=name,
            event_name=event_name,
            created_at=now,
            updated_at=now
        )