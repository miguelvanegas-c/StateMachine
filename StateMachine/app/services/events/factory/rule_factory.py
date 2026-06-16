from abc import ABC, abstractmethod
from typing import Any

from app.models import Rule
from app.exceptions.exceptions import FactoryNotFoundError


class RuleFactory(ABC):
    _registry = {}
    @classmethod
    def register(cls, name):
        def decorator(subclass):
            cls._registry[name] = subclass
            return subclass
        return decorator

    @classmethod
    def get(cls, name):
        try:
            return cls._registry[name]
        except KeyError:
            raise FactoryNotFoundError(name)

    @abstractmethod
    async def create_new_rule(self, meta_data_key:str, value: Any, operator: str, actions:list[str]) -> Rule:
        raise NotImplementedError