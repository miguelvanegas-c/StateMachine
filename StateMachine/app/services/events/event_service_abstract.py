from abc import ABC, abstractmethod

from app.models import Event
from app.schemas.event_schemas import  EventUpdate


class EventService(ABC):
    @abstractmethod
    async def handle(self, order_id:str, event_name:str, metadata:dict) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self,event_name:str) -> Event:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[Event]:
        raise NotImplementedError

    @abstractmethod
    async def add_rule(self, new_rule: EventUpdate) -> Event:
        raise NotImplementedError