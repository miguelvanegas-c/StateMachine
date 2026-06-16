# Services (excluding rule engine)
from app.services.orders.order_service_abstract import OrderService
from app.services.orders.order_service_impl import OrderServiceImpl
from app.services.events.event_service_abstract import EventService
from app.services.events.event_service_impl import EventServiceImpl
from app.services.states.state_service_abstract import StateService
from app.services.states.state_service_impl import StateServiceImpl
from app.services.tickets.ticket_service_abstract import TicketService
from app.services.tickets.ticket_service_impl import TicketServiceImpl

# Repositories
from app.repositories.orders.order_repository_abstract import OrderRepository
from app.repositories.orders.order_repository_impl import OrderRepositoryImpl
from app.repositories.events.event_repository_abstract import EventRepository
from app.repositories.events.event_repository_impl import EventRepositoryImpl
from app.repositories.states.state_repository_abstract import StateRepository
from app.repositories.states.state_repository_impl import StateRepositoryImpl
from app.repositories.tickets.ticket_repository_abstract import TicketRepository
from app.repositories.tickets.ticket_repository_impl import TicketRepositoryImpl

# Mappers
from app.mappers.orders.order_mapper_abstract import OrderMapper
from app.mappers.orders.order_mapper_impl import OrderMapperImpl
from app.mappers.states.state_mapper_abstract import StateMapper
from app.mappers.states.state_mapper_impl import StateMapperImpl
from app.mappers.rules.rule_mapper_abstract import RuleMapper
from app.mappers.rules.rule_mapper_impl import RuleMapperImpl
from app.mappers.events.event_mapper_abstract import EventMapper
from app.mappers.events.event_mapper_impl import EventMapperImpl
from app.mappers.transitions.transition_mapper_abstract import TransitionMapper
from app.mappers.transitions.transition_mapper_impl import TransitionMapperImpl
from app.mappers.tickets.ticket_mapper_abstract import TicketMapper
from app.mappers.tickets.ticket_mapper_impl import TicketMapperImpl

# Rule Engine
from app.services.events.rule_engine_abstract import RuleEngine
from app.services.events.rule_engine_impl import RuleEngineImpl

from functools import lru_cache
from fastapi import Depends


#websocket manager
from app.services.events.ws.connection_manager_abstract import ConnectionManager
from app.services.events.ws.connection_manager_impl import ConnectionManagerImpl

#websocket manager instance
@lru_cache
def get_connection_manager() -> ConnectionManager:
    return ConnectionManagerImpl(mapper=get_order_mapper())

# mappers

@lru_cache
def get_ticket_mapper() -> TicketMapper:
    return TicketMapperImpl()


@lru_cache
def get_rule_mapper() -> RuleMapper:
    return RuleMapperImpl()


@lru_cache
def get_transition_mapper() -> TransitionMapper:
    return TransitionMapperImpl()


@lru_cache
def get_state_mapper() -> StateMapper:
    return StateMapperImpl()


@lru_cache
def get_event_mapper() -> EventMapper:
    return EventMapperImpl(rule_mapper=get_rule_mapper())


@lru_cache
def get_order_mapper() -> OrderMapper:
    return OrderMapperImpl(transition_mapper=get_transition_mapper())



@lru_cache
def get_ticket_repository() -> TicketRepository:
    return TicketRepositoryImpl(mapper=get_ticket_mapper())

# repositories

@lru_cache
def get_state_repository() -> StateRepository:
    return StateRepositoryImpl(mapper=get_state_mapper())


@lru_cache
def get_event_repository() -> EventRepository:
    return EventRepositoryImpl(mapper=get_event_mapper())


@lru_cache
def get_order_repository() -> OrderRepository:
    return OrderRepositoryImpl(mapper=get_order_mapper())

# services

@lru_cache
def get_ticket_service() -> TicketService:
    return TicketServiceImpl(repository=get_ticket_repository())


@lru_cache
def get_rule_engine() -> RuleEngine:
    return RuleEngineImpl(services={"TICKET": get_ticket_service()})


@lru_cache
def get_event_service() -> EventService:
    return EventServiceImpl(
        repository=get_event_repository(),
        rule_engine=get_rule_engine(),
    )


@lru_cache
def get_state_service() -> StateService:
    return StateServiceImpl(
        repository=get_state_repository(),
        event_service=get_event_service(),
    )


@lru_cache
def get_order_service() -> OrderService:
    return OrderServiceImpl(
        websocket_manager=get_connection_manager(),
        repository=get_order_repository(),
        state_service=get_state_service(),
    )


