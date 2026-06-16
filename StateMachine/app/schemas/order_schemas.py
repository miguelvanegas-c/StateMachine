# app/schemas/order_schemas.py
from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.models import Transition


class OrderBase(BaseModel):
    pass

class OrderCreate(OrderBase):
    products_id: list[str] = Field(..., min_length=1)
    amount: float = Field(..., gt=0)

class OrderUpdate(OrderBase):
    id: str
    event_type: str
    metadata: dict


class OrderOut(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    products_id: list[str]
    amount: float
    state: str
    created_at: datetime
    updated_at: datetime
    transitions: list[Transition]

