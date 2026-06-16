from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field



class TicketBase(BaseModel):
    order_id: str = Field(default="", min_length=1)
    message: str = Field(default="", min_length=1)
    created_at: datetime


class TicketOut(TicketBase):
    pass
