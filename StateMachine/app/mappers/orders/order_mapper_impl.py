# app/mappers/order_mapper_impl.py
from bson import ObjectId
from app.mappers.orders.order_mapper_abstract import OrderMapper
from app.models.order import Order
from app.mappers.transitions.transition_mapper_abstract import TransitionMapper
from app.schemas.order_schemas import OrderOut


class OrderMapperImpl(OrderMapper):

    def __init__(self, transition_mapper: TransitionMapper) -> None:
        self.transition_mapper = transition_mapper


    def from_mongo(self, doc: dict) -> Order:
        transitions = [self.transition_mapper.from_mongo(t) for t in doc.get("transitions", [])]
        return Order(
            id=str(doc["_id"]),
            products_id=doc.get("products_id", []),
            amount=doc.get("amount", 0.0),
            state=doc.get("state", ""),
            transitions=transitions,
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at"),
            version=doc.get("version", 0.0),
        )

    def to_mongo(self, order: Order) -> dict:
        doc = {
            "products_id": order.products_id,
            "amount": order.amount,
            "state": order.state,
            "transitions": [self.transition_mapper.to_mongo(t) for t in order.transitions],
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "version": order.version,
        }
        if order.id:
            doc["_id"] = ObjectId(order.id)
        return doc

    def to_order_out(self, order: Order) -> OrderOut:
        return OrderOut(
            id=order.id,
            products_id=order.products_id,
            amount=order.amount,
            state=order.state,
            created_at=order.created_at,
            updated_at=order.updated_at,
            transitions=order.transitions,
        )
    def to_dict(self, order: OrderOut) -> dict:
        return {
            "id": order.id,
            "products_id": order.products_id,
            "amount": order.amount,
            "state": order.state,
            "created_at": str(order.created_at) if order.created_at else None,
            "updated_at": str(order.updated_at) if order.updated_at else None,
            "transitions": [self.transition_mapper.to_dict(t) for t in order.transitions],
        }