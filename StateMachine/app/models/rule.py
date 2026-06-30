

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Rule:
    id: Optional[str] = None
    name: str = ""
    latest_version: Optional[str] = ""
    