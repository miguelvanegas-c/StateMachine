from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class StateBase(BaseModel):
    name: str = ""
    events: List[str]


class StateOut(StateBase):
    pass