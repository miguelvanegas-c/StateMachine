from __future__ import annotations

from dataclasses import dataclass, field
from typing import List




@dataclass(slots=True)
class State:
    id: str
    name: str = ""
    events: List[str] = field(default_factory=list)



