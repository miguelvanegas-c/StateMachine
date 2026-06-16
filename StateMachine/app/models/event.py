from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from app.models.rule import Rule


@dataclass(slots=True)
class Event:
    id: str
    event_name: str = ""
    next_state_name: str = ""
    rules: List[Rule] = field(default_factory=list)
    version: int = 0


