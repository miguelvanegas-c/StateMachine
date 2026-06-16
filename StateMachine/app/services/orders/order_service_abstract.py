from abc import ABC, abstractmethod

from app.schemas.order_schemas import OrderCreate, OrderUpdate
from app.models import Order


class OrderService(ABC):
    @abstractmethod
    async def create_order(self, data: OrderCreate) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def list_orders(self) -> list[Order]:
        raise NotImplementedError

    @abstractmethod
    async def get_order(self, order_id: str) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def update_order(self, order_update:OrderUpdate) -> Order :
        raise NotImplementedError



