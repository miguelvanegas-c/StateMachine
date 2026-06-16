from abc import ABC, abstractmethod

from app.models.order import Order



class OrderRepository(ABC):
    @abstractmethod
    async def create(self, data: Order) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> list[Order]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, order_id: str) -> Order | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, order_id: str, expected_version: float, new_state: str, event:str) -> bool:
        raise NotImplementedError



