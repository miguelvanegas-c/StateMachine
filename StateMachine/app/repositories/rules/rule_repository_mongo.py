

from app.models.rule import Rule
from app.repositories.rules.rule_repository import RuleRepository
from app.models.condition_node import ConditionNode
from app.models.group_node import GroupNode
from app.models.rule_version import RuleVersion

from app.config.database_config import db

class RuleRepositoryMongo(RuleRepository):
    async def create(self, data: Rule) -> Rule:
        doc = self.to_doc(data)
        result = await db["rules"].insert_one(doc)
        data.id = str(result.inserted_id)
        return data
    
    
    async def get_by_event_name_and_name(self, event_name: str, name: str) -> Rule | None:
        doc = await db["rules"].find_one({"event_name": event_name, "name": name})
        if doc:
            return self.from_doc(doc)
        return None
    
    async def get_by_event_name(self, event_name: str) -> list[Rule]:
        cursor = db["rules"].find({"event_name": event_name})
        documents = await cursor.to_list(length=None)
        return [self.from_doc(doc) for doc in documents if doc]
    
    async def update(self, rule: Rule) -> Rule:
        await db["rules"].update_one(
            {"event_name": rule.event_name, "name": rule.name},
            {"$set": {"actual_version": rule.actual_version, "updated_at": rule.updated_at}}
        )
        return rule
    
    def to_doc(self, rule: Rule) -> dict:
        return {
            "name": rule.name,
            "event_name": rule.event_name,
            "actual_version": rule.actual_version,
            "created_at": rule.created_at,
            "updated_at": rule.updated_at,
        }
    
    def from_doc(self, doc: dict) -> Rule:
        return Rule(
            id=str(doc["_id"]),
            name=doc["name"],
            event_name=doc["event_name"],
            actual_version=doc.get("actual_version"),
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at"),
        )