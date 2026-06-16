from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Rule:
    meta_data_key: str
    value: Any
    operator: str = ""
    actions: list[str] = field(default_factory=list)




