from abc import ABC, abstractmethod
from typing import List

from app.models.state import State


class StateRepository(ABC):

    @abstractmethod
    async def get_by_name(self, name: str) -> State | None:
        raise NotImplementedError

