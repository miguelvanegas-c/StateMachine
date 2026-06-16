# app/mappers/transitions/transition_mapper_abstract.py
from abc import ABC, abstractmethod
from app.models.transition import Transition

class TransitionMapper(ABC):
    @abstractmethod
    def from_mongo(self, doc: dict) -> Transition:
        pass

    @abstractmethod
    def to_mongo(self, transition: Transition) -> dict:
        pass

    @abstractmethod
    def to_dict(self, transition: Transition) -> dict:
        pass