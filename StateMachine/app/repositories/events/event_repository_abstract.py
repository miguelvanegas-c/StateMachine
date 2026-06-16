from abc import ABC, abstractmethod

from app.models.event import Event
from app.models.rule import Rule


class EventRepository(ABC):

    @abstractmethod
    async def get_by_name(self, name: str) -> Event| None:
        pass

    @abstractmethod
    async def get_all(self) -> list[Event]|None:
        pass

    @abstractmethod
    async def add_new_rule(self, event_name:str, expected_version:float, rule:Rule) -> bool:
        pass