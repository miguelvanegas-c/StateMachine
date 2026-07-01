from functools import lru_cache


from app.repositories.rules.rule_repository import RuleRepository
from app.repositories.rules.rule_repository_mongo import RuleRepositoryMongo
from app.services.rule_engine import RuleEngine
from app.services.action_service import ActionService
from app.repositories.rules_version.rule_version_repository import RuleVersionRepository
from app.repositories.rules_version.rule_version_repository_mongo import RuleVersionRepositoryMongo
from app.repositories.orders.order_repository_abstract import OrderRepository
from app.repositories.orders.order_repository_mongo import OrderRepositoryMongo
from app.repositories.tickets.ticket_repository_abstract import TicketRepository
from app.repositories.tickets.ticket_repository_mongo import TicketRepositoryMongo
from app.services.connection_manager import ConnectionManager
from app.services.event_service import EventService
from app.services.order_service import OrderService
from app.services.state_machine_service import StateMachineService
from app.services.rule_service import RuleService


# --- Singletons (stateful, safe to cache) ---

@lru_cache
def get_connection_manager() -> ConnectionManager:
    return ConnectionManager()


# --- Repositories ---

def get_order_repository() -> OrderRepository:
    return OrderRepositoryMongo()

def get_ticket_repository() -> TicketRepository:
    return TicketRepositoryMongo()

def get_rule_version_repository() -> RuleVersionRepository:
    return RuleVersionRepositoryMongo()

def get_rule_repository() -> RuleRepository:
    return RuleRepositoryMongo()

# --- Services ---

def get_event_service() -> EventService:
    return EventService(
        ticket_repository=get_ticket_repository(),
        rule_service=get_rule_service()
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

def get_rule_service() -> RuleService:
    return RuleService(
        rule_version_repository=get_rule_version_repository(),
        rule_repository=get_rule_repository(),
        action_service=get_action_service(),
        rule_engine=get_rule_engine()
    )

def get_action_service() -> 'ActionService':
    return ActionService(
        ticket_repository=get_ticket_repository()
    )

def get_rule_engine() -> 'RuleEngine':
    return RuleEngine()