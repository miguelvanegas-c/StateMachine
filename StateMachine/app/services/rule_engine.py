from app.models.condition_node import ConditionNode
from app.models.group_node import GroupNode

import logging

logger = logging.getLogger(__name__)

class RuleEngine:

    condition_evaluators = {
        "=": lambda field_value, value: field_value == value,
        "!=": lambda field_value, value: field_value != value,
        ">": lambda field_value, value: field_value > value,
        "<": lambda field_value, value: field_value < value,
        ">=": lambda field_value, value: field_value >= value,
        "<=": lambda field_value, value: field_value <= value,
    }

    group_evaluators = {
        "AND": lambda results: all(results),
        "OR": lambda results: any(results),
    }

    def evaluate_tree(self, tree: GroupNode | ConditionNode, metadata: dict):

        if tree.type == "CONDITION":
            condition_evaluator = self.condition_evaluators.get(tree.operator)
            field_value = metadata.get(tree.field)
            condition = condition_evaluator(field_value, tree.value)
            return condition

        evaluator = self.group_evaluators.get(tree.operator)
        results = [self.evaluate_tree(child, metadata) for child in tree.children]
        return evaluator(results)