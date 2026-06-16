from abc import ABC, abstractmethod

from app.models.state import State
from app.schemas.state_schemas import StateOut


class StateMapper(ABC):
    @abstractmethod
    def from_mongo(self, doc: dict) -> State:
        pass

    @abstractmethod
    def to_mongo(self, order: State) -> dict:
        pass

    @abstractmethod
    def to_state_out(self, state: State) -> StateOut:
        pass