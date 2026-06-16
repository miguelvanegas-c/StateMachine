from typing import List
from app.services.events.rule_engine_abstract import RuleEngine
from simpleeval import SimpleEval
from app.models import Rule
from app.services.events.strategy.strategy_action import StrategyAction
import logging
from app.services.events.strategy.ticket_strategy import TicketStrategy


logger = logging.getLogger(__name__)


class RuleEngineImpl(RuleEngine):

    def __init__(self, services:dict) -> None:
        self.services = services

    async def evaluate(self, rules:List[Rule], metadata:dict, order_id:str):
        simple_eval = SimpleEval()
        for rule in rules:
            try:
                value = metadata[rule.meta_data_key]
            except KeyError:
                logger.warning(f"Metadata key {rule.meta_data_key} not found in metadata. Skipping rule.")
                continue
            operator = rule.operator
            value_to_operate = rule.value
            actions = rule.actions
            condition = simple_eval.eval(f"{value} {operator} {value_to_operate}")
            await self.execute_action(actions=actions, metadata=metadata, order_id=order_id, condition=condition)


    async def execute_action(self, actions:list[str], metadata:dict, order_id:str, condition:bool):
        if condition:
            for action in actions:
                strategy = StrategyAction.get(action)
                strategy_instance = strategy()
                await strategy_instance.execute(metadata=metadata, order_id=order_id, service=self.services[action])