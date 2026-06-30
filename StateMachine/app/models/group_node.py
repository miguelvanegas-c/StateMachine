from __future__ import annotations  
from typing import Literal
from dataclasses import dataclass, field
from app.schemas.node_schemas import GroupNodeSchema
from app.models.condition_node import ConditionNode

@dataclass(slots=True)
class GroupNode:
    type: str
    operator: str
    children: list[ConditionNode | GroupNode] = field(default_factory=list)

    @staticmethod
    def create_new(group_node_schema: GroupNodeSchema) -> GroupNode:
        children = []
        for child in group_node_schema.children:
            if child.type == "CONDITION":
                children.append(ConditionNode(
                    type=child.type,
                    field=child.field,
                    operator=child.operator,
                    value=child.value,
                    value_type=child.value_type
                ))
            elif child.type == "GROUP":
                children.append(GroupNode.create_new(child))
        return GroupNode(
            type=group_node_schema.type,
            operator=group_node_schema.operator,
            children=children
        )