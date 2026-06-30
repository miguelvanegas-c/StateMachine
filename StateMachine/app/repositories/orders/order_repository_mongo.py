from datetime import datetime

from app.repositories.orders.order_repository_abstract import OrderRepository
from bson import ObjectId
from bson.errors import InvalidId
from app.config.database_config import db
from app.models import Order
from app.exceptions.exceptions import InvalidOrderIdError


class OrderRepositoryMongo(OrderRepository):


    async def create(self, data: Order) -> Order:
        doc = self.to_doc(data)
        result = await db["orders"].insert_one(doc)
        data.id = str(result.inserted_id)
        return data

    async def list(self) -> list[Order | None]:
        cursor = db["orders"].find({})
        documents = await cursor.to_list(length=None)
        return [self.from_doc(doc) for doc in documents if doc]

    async def get_by_id(self, order_id: str) -> Order | None:
        try:
            doc = await db["orders"].find_one({"_id": ObjectId(order_id)})
            return self.from_doc(doc) if doc else None
        except InvalidId as e:
            raise InvalidOrderIdError(f"Invalid order ID: {order_id}")

    async def update(self, order_id: str, expected_version: float, new_state: str, event:str) -> bool:
        result = await db["orders"].update_one(
            {
                "_id": ObjectId(order_id),
                "version": expected_version
            },
            {
                "$set": {
                    "state": new_state,
                    "updated_at": datetime.now()
                },
                "$inc": {"version": 1},
                "$push": {
                "transitions": {
                    "event": event,
                    "new_state": new_state.upper(),
                    "timestamp": datetime.now()
                }
        }
            }
        )
        return result.modified_count == 1


    def to_doc(self, order: Order) -> dict:
        return {
            "products_id": order.products_id,
            "amount": order.amount,
            "state": order.state,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "version": order.version,
            "transitions": [self.transition_to_doc(transition) for transition in order.transitions]
        }
    
    def transition_to_doc(self, transition) -> dict:
        return {
            "event": transition.event,
            "new_state": transition.new_state,
            "timestamp": transition.timestamp
        }
    def from_doc(self, doc: dict) -> Order:
        return Order(
            id=str(doc["_id"]),
            products_id=doc["products_id"],
            amount=doc["amount"],
            state=doc["state"],
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
            version=doc.get("version", 0),
            transitions=[self.transition_from_doc(transition) for transition in doc.get("transitions", [])]
        )
    def transition_from_doc(self, doc: dict):
        return {
            "event": doc["event"],
            "new_state": doc["new_state"],
            "timestamp": doc["timestamp"]
        }