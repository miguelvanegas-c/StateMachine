
from typing import Literal
from typing import Union 
from pydantic import BaseModel, Field


class ConditionNodeSchema(BaseModel):
    type: Literal["CONDITION"]
    value_type: Literal["string", "float"]
    field: str
    operator: Literal["=", "!=", ">", "<", ">=", "<="]
    value: str | float


class GroupNodeSchema(BaseModel):
    type: Literal["GROUP"]
    operator: Literal["AND", "OR"]
    children: list[Union["ConditionNodeSchema", "GroupNodeSchema"]] = Field(..., min_length=2)

GroupNodeSchema.model_rebuild()