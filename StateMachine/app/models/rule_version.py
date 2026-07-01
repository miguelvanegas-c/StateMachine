# app/models/rule.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

<<<<<<< HEAD
from app.schemas.node_schemas import ConditionNodeSchema, GroupNodeSchema
from app.models.condition_node import ConditionNode
=======
from app.schemas.node_schemas import  GroupNodeSchema
>>>>>>> rama-temporal
from app.models.group_node import GroupNode


@dataclass(slots=True)
class RuleVersion:
    id: Optional[str] = None
    name: str = ""
    event_name: str = ""
    tree: GroupNode = None
    action: str = ""
<<<<<<< HEAD
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    rule_id: Optional[str] = None

=======
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
>>>>>>> rama-temporal

    @staticmethod
    def create_new(event_name: str, tree: GroupNodeSchema, action:str, name: str) -> RuleVersion:
            now = datetime.now()
            return RuleVersion(
                event_name=event_name,
                tree= GroupNode.create_new(tree),
                action=action,
                name=name,
<<<<<<< HEAD
                active=True,
                created_at=now,
                updated_at=now
=======
                created_at=now,
                updated_at=now,
>>>>>>> rama-temporal
            )