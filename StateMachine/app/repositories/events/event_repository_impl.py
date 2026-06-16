from app.repositories.events.event_repository_abstract import EventRepository
from app.models.event import Event
from app.config.database_config import db
from app.mappers.events.event_mapper_abstract import EventMapper
from app.models.rule import Rule



class EventRepositoryImpl(EventRepository):

    def __init__(self, mapper: EventMapper):
        self.mapper = mapper

    async def get_by_name(self, name: str) -> Event | None:
        document = await db["events"].find_one({"event_name": name})
        return self.mapper.from_mongo(document) if document else None

    async def get_all(self) -> list[Event]| None:
        cursor = db["events"].find({})
        documents = await cursor.to_list(length=None)
        return [self.mapper.from_mongo(doc) for doc in documents if doc]

    async def add_new_rule(self, event_name:str, expected_version:int, rule:Rule) -> bool:
        result = await db["events"].update_one(
            {
                "event_name": event_name,
                "version": expected_version
            },
            {
                "$inc": {"version": 1},
                "$push": {
                    "rules": {
                        "meta_data_key": rule.meta_data_key,
                        "value": rule.value,
                        "operator": rule.operator,
                        "actions": rule.actions
                    }
                }
            }
        )
        return result.modified_count == 1