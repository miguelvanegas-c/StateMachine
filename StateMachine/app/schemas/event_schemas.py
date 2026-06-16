from __future__ import annotations

from dataclasses import field
from typing import Any

from pydantic import BaseModel, Field

from app.models import Rule


class EventBase(BaseModel):
    event_name: str = Field(default="", min_length=1)

class EventUpdate(EventBase):
    rule: NewRule

class EventOut(EventBase):
    next_state_name: str = Field(default="", min_length=1)
    rules: list[Rule] = Field(default_factory=dict)

class NewRule(BaseModel):
    rule_type:str = Field(default="")
    meta_data_key: str
    value: Any
    operator: str = ""
    actions: list[str] = field(default_factory=list)