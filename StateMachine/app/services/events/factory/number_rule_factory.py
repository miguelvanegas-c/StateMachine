from typing import Any

from app.models import Rule
from app.exceptions.exceptions import StrategyNotFoundError, OperatorNotFoundError
from app.services.events.factory.rule_factory import RuleFactory
from app.services.events.strategy.strategy_action import StrategyAction


@RuleFactory.register('NUMBER')
class NumberRuleFactory(RuleFactory):

    def __init__(self) -> None:
        self.operators ={
            "equal to": "==",
            "greater than": ">",
            "less than": "<",
            "less than or equal to": "<=",
            "greater than or equal to": ">="
        }
    async def create_new_rule(self, meta_data_key:str, value: Any, operator: str, actions:list[str])-> Rule:
        for a in actions:
            if not StrategyAction.exists(a):
                raise StrategyNotFoundError(a)
        operator_value = self.validate_operator(operator=operator)
        try:
            result_value = float(value)
        except ValueError:
            raise ValueError(f"The value {value} is not a valid number")

        return Rule(
            meta_data_key=meta_data_key,
            value=result_value,
            operator=operator_value,
            actions=actions
        )

    def validate_operator(self, operator:str) -> str:
        try:
            return self.operators[operator]
        except KeyError:
            raise OperatorNotFoundError(operator)



