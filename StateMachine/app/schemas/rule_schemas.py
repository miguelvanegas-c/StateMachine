from typing import Union

from pydantic import BaseModel, Field

from app.models.group_node import GroupNode

class RuleBase(BaseModel):
    name: str = Field(..., min_length=1)
    event_name: str = Field(..., min_length=1)
    tree: GroupNode
    action: str = Field(..., min_length=1)

class RuleCreate(RuleBase):
    pass
    


class RuleUpdate(RuleBase):
    pass


class RuleOut(RuleBase):
    pass