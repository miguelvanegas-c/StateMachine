from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.schemas.node_schemas import GroupNodeSchema
from app.models.group_node import GroupNode


@dataclass(slots=True)
class RuleVersion:
    id: Optional[str] = None
    name: str = ""
    event_name: str = ""
    tree: GroupNode = None
    action: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def create_new(event_name: str, tree: GroupNodeSchema, action: str, name: str) -> RuleVersion:
        now = datetime.now()
        return RuleVersion(
            event_name=event_name,
            tree=GroupNode.create_new(tree),
            action=action,
            name=name,
            created_at=now,
            updated_at=now
        )