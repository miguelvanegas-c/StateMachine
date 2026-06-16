from abc import ABC, abstractmethod
from typing import List

from app.models import Rule, Order


class RuleEngine(ABC):
    @abstractmethod
    async def evaluate(self, rules: List[Rule], metadata: dict, order_id:str):
        raise NotImplementedError

