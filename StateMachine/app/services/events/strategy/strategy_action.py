from abc import ABC, abstractmethod

from app.exceptions.exceptions import StrategyNotFoundError


class StrategyAction(ABC):
    _registry = {}
    @classmethod
    def register(cls, name):
        def decorator(subclass):
            cls._registry[name] = subclass
            return subclass
        return decorator

    @classmethod
    def exists(cls, name: str) -> bool:
        return name in cls._registry

    @classmethod
    def get(cls, name):
        try:
            return cls._registry[name]
        except KeyError:
            raise StrategyNotFoundError(name)

    @abstractmethod
    async def execute(self, metadata:dict, order_id:str, service):
        raise NotImplementedError

    @property
    def registry(self):
        return self._registry