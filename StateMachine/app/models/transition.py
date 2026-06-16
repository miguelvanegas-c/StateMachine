# app/models/transition.py
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(slots=True)
class Transition:
    event: str
    new_state: str
    timestamp: datetime = field(default_factory=datetime.now)

