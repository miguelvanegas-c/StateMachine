from app.services.events.event_service_abstract import EventService
from app.exceptions.exceptions import EventNotExistError, ConcurrentModificationException
from app.repositories.events.event_repository_abstract import EventRepository
from app.services.events.rule_engine_abstract import RuleEngine
from app.models import Event
from app.schemas.event_schemas import EventUpdate
from app.services.events.factory.rule_factory import RuleFactory
from app.services.events.factory.number_rule_factory import NumberRuleFactory

class EventServiceImpl(EventService):

    def __init__(self, repository:EventRepository, rule_engine: RuleEngine):
        self.repository = repository
        self.rule_engine = rule_engine

    async def handle(self, order_id:str, event_name:str, metadata:dict) -> str:
        event = await self.get_by_name(event_name)
        await self.rule_engine.evaluate(rules = event.rules,metadata=metadata, order_id = order_id)
        return event.next_state_name

    async def get_by_name(self, event_name:str) -> Event:
        event = await self.repository.get_by_name(event_name.upper())
        if event is None:
            raise EventNotExistError(event_name)
        return event

    async def get_all(self) -> list[Event]:
        events = await self.repository.get_all()
        if events is None:
            raise EventNotExistError(None)
        return events

    async def add_rule(self, event_update: EventUpdate) -> Event:
        event = await self.get_by_name(event_update.event_name)
        rule_factory = RuleFactory.get(event_update.rule.rule_type)
        rule_factory_instance = rule_factory()
        new_rule = await rule_factory_instance.create_new_rule(
            meta_data_key=event_update.rule.meta_data_key,
            value=event_update.rule.value,
            operator=event_update.rule.operator,
            actions=event_update.rule.actions
                                                )
        condition = await self.repository.add_new_rule(event_update.event_name.upper(), event.version, new_rule)
        if not condition:
            raise ConcurrentModificationException()
        return await self.get_by_name(event_update.event_name)

