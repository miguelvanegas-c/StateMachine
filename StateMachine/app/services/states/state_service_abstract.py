from abc import ABC, abstractmethod
from typing import List

from app.models import Order
from app.models.state import State


class StateService(ABC):
    @abstractmethod
    async def event_handler(self, order_id: str, state: str, event: str, metadata:dict) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, state_name: str) -> State:
        raise NotImplementedError