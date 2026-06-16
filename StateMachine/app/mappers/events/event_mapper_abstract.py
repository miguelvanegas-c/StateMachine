
from abc import ABC, abstractmethod
from app.models.event import Event
from app.schemas.event_schemas import EventOut


class EventMapper(ABC):
    @abstractmethod
    def from_mongo(self, doc: dict) -> Event:
        pass

    @abstractmethod
    def to_mongo(self, order: Event) -> dict:
        pass

    @abstractmethod
    def to_event_out(self, event: Event) -> EventOut:
        pass