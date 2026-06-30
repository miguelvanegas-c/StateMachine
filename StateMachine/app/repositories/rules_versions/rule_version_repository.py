from abc import ABC, abstractmethod

from app.models.rule import RuleVersion



class RuleVersionRepository(ABC):
    @abstractmethod
    async def create(self, data: RuleVersion) -> RuleVersion:
        raise NotImplementedError


    @abstractmethod
    async def get_by_event_name_and_name(self, event_name: str, name: str) -> RuleVersion | None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_event_name(self, event_name: str) -> list[RuleVersion]:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, rule: RuleVersion) -> RuleVersion:
        raise NotImplementedError


   