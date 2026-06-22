from functools import lru_cache

from app.repositories.orders.order_repository_abstract import OrderRepository
from app.repositories.orders.order_repository_mongo import OrderRepositoryMongo
from app.repositories.tickets.ticket_repository_abstract import TicketRepository
from app.repositories.tickets.ticket_repository_mongo import TicketRepositoryMongo
from app.services.connection_manager import ConnectionManager
from app.services.event_service import EventService
from app.services.order_service import OrderService
from app.services.state_machine_service import StateMachineService


# --- Singletons (stateful, safe to cache) ---

@lru_cache
def get_connection_manager() -> ConnectionManager:
    return ConnectionManager()


# --- Repositories ---

def get_order_repository() -> OrderRepository:
    return OrderRepositoryMongo()

def get_ticket_repository() -> TicketRepository:
    return TicketRepositoryMongo()


# --- Services ---

def get_event_service() -> EventService:
    return EventService(
        ticket_repository=get_ticket_repository(),
    )

def get_state_machine_service() -> StateMachineService:
    return StateMachineService(
        event_service=get_event_service(),
    )

def get_order_service() -> OrderService:
    return OrderService(
        repository=get_order_repository(),
        state_machine_service=get_state_machine_service(),
        websocket_manager=get_connection_manager(),
    )