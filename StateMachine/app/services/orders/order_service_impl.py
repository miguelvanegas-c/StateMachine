
from app.services.orders.order_service_abstract import OrderService


from app.repositories.orders.order_repository_abstract import OrderRepository

from app.schemas.order_schemas import OrderCreate, OrderUpdate
from app.models import Order
from app.exceptions.exceptions import NoOrderException, ConcurrentModificationException
from app.services.states.state_service_abstract import StateService
from app.services.events.ws.connection_manager_abstract import ConnectionManager
import logging
logger = logging.getLogger(__name__)

class OrderServiceImpl(OrderService):
    def __init__(self, repository: OrderRepository, state_service: StateService, websocket_manager:ConnectionManager):
        self.repository: OrderRepository = repository
        self.state_service: StateService = state_service
        self.websocket_manager = websocket_manager

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
        
        logger.info(f"Updating order {order_update.id} with event {order_update.event_type}")
        order = await self.get_order(order_update.id)
        logger.debug(f"Order {order_update.id} current state: {order.state}, version: {order.version}")
        new_state = await self.state_service.event_handler(order_id = order_update.id, state = order.state, event = order_update.event_type, metadata = order_update.metadata)
        logger.info(f"New state for order {order_update.id}: {new_state}")
        result = await self.repository.update(order_id = order_update.id, expected_version = order.version, new_state = new_state, event = order_update.event_type)
        if not result:
            logger.warning(f"Concurrent modification for order {order_update.id}, expected version {order.version}")
            raise ConcurrentModificationException()
        logger.info(f"Order {order_update.id} updated successfully")
        new_order = await self.get_order(order_update.id)
        await self.websocket_manager.send_update(order_update.id, new_order)
        logger.debug(f"WebSocket update sent for order {order_update.id}")
        return new_order



