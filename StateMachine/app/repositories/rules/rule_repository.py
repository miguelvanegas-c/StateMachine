
from abc import ABC, abstractmethod

from app.models.rule import Rule


class RuleRepository(ABC):
    
    @abstractmethod
    async def create(self, data: Rule) -> Rule:
        raise NotImplementedError


    @abstractmethod
    async def get_by_event_name_and_name(self, event_name: str, name: str) -> Rule | None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_event_name(self, event_name: str) -> list[Rule]:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, rule: Rule) -> Rule:
        raise NotImplementedError
