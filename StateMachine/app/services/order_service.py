

from app.services.state_machine_service import StateMachineService
from app.repositories.orders.order_repository_abstract import OrderRepository

from app.schemas.order_schemas import OrderCreate, OrderUpdate
from app.models import Order
from app.exceptions.exceptions import NoOrderException, ConcurrentModificationException
from app.services.connection_manager import ConnectionManager



class OrderService():
    def __init__(self, repository: OrderRepository, state_machine_service: StateMachineService, websocket_manager:ConnectionManager):
        self.repository: OrderRepository = repository
        self.state_machine_service: StateMachineService = state_machine_service
        self.websocket_manager: ConnectionManager = websocket_manager

    async def create_order(self, data: OrderCreate) -> Order:
        new_order = Order.create_new(products_id=data.products_id, amount=data.amount)
        return await self.repository.create(new_order)

    async def list_orders(self) -> list[Order]:
        orders = await self.repository.list()
        if orders is None or len(orders) == 0:
            raise NoOrderException(None)
        return orders

    async def get_order(self, order_id: str) -> Order:
        order = await self.repository.get_by_id(order_id)
        if order is None:
            raise NoOrderException(order_id)
        return order

    async def update_order(self, order_update: OrderUpdate) -> Order:
        order = await self.get_order(order_update.id)
        new_state = await self.state_machine_service.process_event(order = order, event_name = order_update.event_type, metadata = order_update.metadata)
        result = await self.repository.update(order_id = order_update.id, expected_version = order.version, new_state = new_state, event = order_update.event_type)
        if not result:
            raise ConcurrentModificationException()
        new_order = await self.get_order(order_update.id)
        await self.websocket_manager.send_update(order_update.id, new_order)
        return new_order



