from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Ticket:
    id: Optional[str] = None
    order_id: str = None
    message: str = None
    created_at: Optional[datetime] = None

    @staticmethod
    def create(order_id:str, message:str) -> 'Ticket':
        return Ticket(
            order_id = order_id,
            message=message,
            created_at = datetime.now()
        )


