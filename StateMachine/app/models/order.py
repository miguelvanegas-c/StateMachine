# app/models/order_schemas.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.models.transition import Transition


@dataclass(slots=True)
class Order:
    id: Optional[str] = None
    products_id: list[str] | None = None
    amount: float = 0.0
    state: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    transitions: list[Transition] = field(default_factory=list)
    version: int = 0

    @staticmethod
    def create_new(products_id:list[str], amount:float) -> Order:
        now = datetime.now()
        return Order(
            products_id=products_id,
            amount=amount,
            state="PENDING",
            version=0,
            transitions=[Transition(event="CREATE", new_state="PENDING", timestamp=now)],
            created_at=now,
            updated_at=now,
        )