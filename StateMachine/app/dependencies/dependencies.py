# Services (excluding rule engine)
from app.services.order_service import OrderService
from app.services.event_service import EventService
from app.services.connection_manager import ConnectionManager
from app.services.state_machine_service import StateMachineService

# Repositories
from app.repositories.orders.order_repository_abstract import OrderRepository
from app.repositories.orders.order_repository_mongo import OrderRepositoryMongo
from app.repositories.tickets.ticket_repository_abstract import TicketRepository
from app.repositories.tickets.ticket_repository_mongo import TicketRepositoryMongo


from functools import lru_cache



#websocket manager
from app.services.connection_manager import ConnectionManager

#websocket manager instance
@lru_cache
def get_connection_manager() -> ConnectionManager:
    return ConnectionManager()


@lru_cache
def get_ticket_repository() -> TicketRepository:
    return TicketRepositoryMongo()

# repositories


@lru_cache
def get_order_repository() -> OrderRepository:
    return OrderRepositoryMongo()

# services

@lru_cache
def get_event_service() -> EventService:
    return EventService(
        ticket_repository=get_ticket_repository(),
    )

@lru_cache
def get_state_machine_service() -> StateMachineService:
    return StateMachineService(
        event_service=get_event_service(),
    )

@lru_cache
def get_order_service() -> OrderService:
    return OrderService(
        websocket_manager=get_connection_manager(),
        repository=get_order_repository(),
        state_machine_service=get_state_machine_service(),
    )


