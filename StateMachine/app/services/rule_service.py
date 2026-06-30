
from datetime import datetime

from app.services.rule_engine import RuleEngine
from app.services.action_service import ActionService
from app.repositories.rules.rule_repository import RuleRepository
from app.exceptions.exceptions import InvalidTypeConditionException, EventNotExistError, RuleExistError, RuleNotExistError
from app.schemas.node_schemas import ConditionNodeSchema, GroupNodeSchema
from app.models.rule import Rule
from app.schemas.rule_schemas import RuleCreate
from app.services.events import EVENTS
class RuleService:

    def __init__(self, repository: RuleRepository, action_service: ActionService, rule_engine: RuleEngine):
        self.repository = repository
        self.action_service = action_service
        self.rule_engine = rule_engine

    async def execute_rules(self, event_name: str, order, metadata: dict):
        rules = await self.get_rules_by_event_name(event_name)
        for rule in rules:
            if rule.active:
                flag = self.rule_engine.evaluate_tree(rule.tree, metadata)
                if flag:
                    await self.action_service.execute_action(rule.action, order, metadata)

    async def create_rule(self, rule_create: RuleCreate) -> Rule:
        event_name= rule_create.event_name.upper()
        name = rule_create.name.upper()
        action = rule_create.action.upper()
        self.validate_conditions(rule_create.tree)
        await self.validate_rule(event_name,name)
        self.action_service.validate_action(action)
        rule = Rule.create_new(
            name=name,
            event_name=event_name, 
            tree=rule_create.tree,
            action=action  
        )
        return await self.repository.create(rule)
    
    async def update_rule(self, event_name: str, name: str) -> Rule:
        event_name = event_name.upper()
        name = name.upper()
        rule = await self.get_rule_by_event_name_and_name(event_name, name)
        rule.active = not rule.active
        rule.updated_at = datetime.now()
        return await self.repository.update(rule)

    
    async def get_rule_by_event_name_and_name(self, event_name: str, name: str) -> Rule:
        event_name = event_name.upper()
        name = name.upper()
        rule = await self.repository.get_by_event_name_and_name(event_name, name)
        if not rule:
            raise RuleNotExistError(event_name,name)
        return rule


    async def get_rules_by_event_name(self, event_name: str) -> list[Rule]:
        event_name = event_name.upper()
        rules = await self.repository.get_by_event_name(event_name)
        if len(rules) == 0:
            raise RuleNotExistError(event_name)
        return rules


    async def validate_rule(self, event_name: str, name: str) -> None:
        try:
            EVENTS(event_name)
            rule = await self.repository.get_by_event_name_and_name(event_name, name)
            if rule:
                raise RuleExistError(event_name,name)   
        except ValueError:
            raise EventNotExistError(event_name)


    def validate_conditions(self, node: GroupNodeSchema | ConditionNodeSchema) -> None:
        if node.type == "CONDITION":
            tipo_esperado = str if node.value_type == "string" else float
            if not isinstance(node.value, tipo_esperado):
                raise InvalidTypeConditionException(node.field, node.value_type)
            return
        for child in node.children:
            self.validate_conditions(child)

   
        
        
