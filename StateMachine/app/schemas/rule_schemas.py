# app/schemas/rule_schemas.py
from typing import Any
from pydantic import BaseModel, Field

from app.schemas.node_schemas import GroupNodeSchema


class RuleBase(BaseModel):
    name: str = Field(..., min_length=1)
    event_name: str = Field(..., min_length=1)
    tree: GroupNodeSchema
    action: str = Field(..., min_length=1)


class RuleCreate(RuleBase):
    pass


class RuleOut(BaseModel):
    name: str
    event_name: str
    tree: dict[str, Any]
    action: str
    active: bool