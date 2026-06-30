
from dataclasses import dataclass


@dataclass(slots=True)
class ConditionNode:
    type: str 
    value_type: str
    field: str
    operator: str
    value: str | float

   
