# app/mappers/events/event_mapper_abstract.py
from abc import ABC, abstractmethod
from app.models.order import Order
from app.schemas.order_schemas import OrderOut


class OrderMapper(ABC):
    @abstractmethod
    def from_mongo(self, doc: dict) -> Order:
        pass

    @abstractmethod
    def to_mongo(self, event: Order) -> dict:
        pass

    @abstractmethod
    def to_order_out(self, order: Order) -> OrderOut:
        pass
    
    @abstractmethod
    def to_dict(self, order: OrderOut) -> dict:
        pass