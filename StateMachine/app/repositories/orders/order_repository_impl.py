from datetime import datetime

from app.repositories.orders.order_repository_abstract import OrderRepository
from bson import ObjectId
from bson.errors import InvalidId
from app.mappers.orders.order_mapper_impl import OrderMapper
from app.config.database_config import db
from app.models import Order
from app.exceptions.exceptions import InvalidOrderIdError


class OrderRepositoryImpl(OrderRepository):

    def __init__(self, mapper: OrderMapper):
        self.mapper = mapper

    async def create(self, data: Order) -> Order:
        doc = self.mapper.to_mongo(data)
        result = await db["orders"].insert_one(doc)
        data.id = str(result.inserted_id)
        return data

    async def list(self) -> list[Order | None]:
        cursor = db["orders"].find({})
        documents = await cursor.to_list(length=None)
        return [self.mapper.from_mongo(doc) for doc in documents if doc]

    async def get_by_id(self, order_id: str) -> Order | None:
        try:
            doc = await db["orders"].find_one({"_id": ObjectId(order_id)})
            return self.mapper.from_mongo(doc) if doc else None
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
