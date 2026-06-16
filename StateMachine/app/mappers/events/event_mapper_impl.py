# app/mappers/events/event_mapper_impl.py
from bson import ObjectId
from app.mappers.events.event_mapper_abstract import EventMapper
from app.models.event import Event
from app.mappers.rules.rule_mapper_abstract import RuleMapper
from app.schemas.event_schemas import EventOut


class EventMapperImpl(EventMapper):

    def __init__(self, rule_mapper: RuleMapper):
        self.rule_mapper = rule_mapper


    def from_mongo(self, doc: dict) -> Event:
        rules = [self.rule_mapper.from_mongo(r) for r in doc.get("rules", [])]
        return Event(
            id=str(doc["_id"]),
            event_name=doc.get("event_name", ""),
            next_state_name=doc.get("next_state_name", ""),
            rules=rules,
            version=doc.get("version", 0),
        )

    def to_mongo(self, event: Event) -> dict:
        doc = {
            "event_name": event.event_name,
            "next_state_name": event.next_state_name,
            "rules": [self.rule_mapper.to_mongo(r) for r in event.rules],
            "version": event.version
        }
        if event.id:
            doc["_id"] = ObjectId(event.id)
        return doc

    def to_event_out(self, event: Event) -> EventOut:
        return EventOut(
            event_name=event.event_name,
            next_state_name=event.next_state_name,
            rules=event.rules
        )