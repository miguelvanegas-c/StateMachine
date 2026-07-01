

from app.exceptions.exceptions import InvalidOrderIdError
from app.models.condition_node import ConditionNode
from app.models.group_node import GroupNode
from app.models.rule_version import RuleVersion
from app.repositories.rules_version.rule_version_repository import RuleVersionRepository
from bson import ObjectId
from bson.errors import InvalidId
from app.config.database_config import db

class RuleVersionRepositoryMongo(RuleVersionRepository):
    async def create(self, data: RuleVersion) -> RuleVersion:
        doc = self.to_doc(data)
        result = await db["rules_versions"].insert_one(doc)
        data.id = str(result.inserted_id)
        return data
    
    
    async def get_by_event_name_and_name(self, event_name: str, name: str) -> RuleVersion | None:
        doc = await db["rules_versions"].find_one({"event_name": event_name, "name": name})
        if doc:
            return self.from_doc(doc)
        return None
    
    async def get_by_event_name(self, event_name: str) -> list[RuleVersion]:
        cursor = db["rules_versions"].find({"event_name": event_name})
        documents = await cursor.to_list(length=None)
        return [self.from_doc(doc) for doc in documents if doc]
    
    async def update(self, rule: RuleVersion) -> RuleVersion:
        await db["rules_versions"].update_one(
            {"event_name": rule.event_name, "name": rule.name},
            {"$set": {"active": rule.active, "updated_at": rule.updated_at}}
        )
        return rule
    
    async def get_by_id(self, id: str) -> RuleVersion | None:
        try:
            doc = await db["rules_versions"].find_one({"_id": ObjectId(id)})
            return self.from_doc(doc) if doc else None
        except InvalidId as e:
            raise InvalidOrderIdError(f"Invalid rule version ID: {id}")
        
    async def get_all_by_event_name_and_name(self, event_name: str, name: str) -> list[RuleVersion]:
        cursor = db["rules_versions"].find({"event_name": event_name, "name": name})
        documents = await cursor.to_list(length=None)
        return [self.from_doc(doc) for doc in documents if doc]

    def to_doc(self, rule: RuleVersion) -> dict:
        return {
            "name": rule.name,
            "event_name": rule.event_name,
            "action": rule.action,
            "tree": self.group_node_to_doc(rule.tree),
            "created_at": rule.created_at,
            "updated_at": rule.updated_at
        }
    
    def group_node_to_doc(self, group_node: GroupNode) -> dict:
        return {
            "type": group_node.type,
            "operator": group_node.operator,
            "children": [self.group_node_to_doc(child) if isinstance(child, GroupNode) else self.condition_node_to_doc(child) for child in group_node.children]
        }
    
    def condition_node_to_doc(self, condition_node) -> dict:
        return {
            "type": condition_node.type,
            "field": condition_node.field,
            "operator": condition_node.operator,
            "value": condition_node.value,
            "value_type": condition_node.value_type
        }
    
    def from_doc(self, doc: dict) -> RuleVersion:
        return RuleVersion(
            id=str(doc["_id"]),
            name=doc["name"],
            event_name=doc["event_name"],
            action=doc["action"],
            tree=self.group_node_from_doc(doc["tree"]),
            created_at=doc["created_at"],
            updated_at=doc["updated_at"]
        )
    
    def group_node_from_doc(self, doc: dict) -> GroupNode:
        children = []
        for child in doc["children"]:
            if child["type"] == "CONDITION":
                children.append(self.condition_node_from_doc(child))
            elif child["type"] == "GROUP":
                children.append(self.group_node_from_doc(child))
        return GroupNode(
            type=doc["type"],
            operator=doc["operator"],
            children=children
        )
    

    def condition_node_from_doc(self, doc: dict) -> ConditionNode:
        return ConditionNode(
            type=doc["type"],
            field=doc["field"],
            operator=doc["operator"],
            value=doc["value"],
            value_type=doc["value_type"]
        )