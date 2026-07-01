
from datetime import datetime

from app.repositories.rules.rule_repository import RuleRepository
from app.services.rule_engine import RuleEngine
from app.services.action_service import ActionService
<<<<<<< HEAD
from app.repositories.rules.rule_repository import RuleVersionRepository
from app.exceptions.exceptions import InvalidTypeConditionException, EventNotExistError, RuleExistError, RuleNotExistError
from app.schemas.node_schemas import ConditionNodeSchema, GroupNodeSchema
from app.models.rule import RuleVersion
=======
from app.repositories.rules_version.rule_version_repository import RuleVersionRepository
from app.exceptions.exceptions import InvalidTypeConditionException, EventNotExistError, RuleExistError, RuleNotExistError
from app.schemas.node_schemas import ConditionNodeSchema, GroupNodeSchema
from app.models.rule_version import RuleVersion
from app.models.rule import Rule
>>>>>>> rama-temporal
from app.schemas.rule_schemas import RuleCreate
from app.services.events import EVENTS

class RuleService:

<<<<<<< HEAD
    def __init__(self, repository: RuleVersionRepository, action_service: ActionService, rule_engine: RuleEngine):
        self.repository = repository
=======
    def __init__(self,rule_repository:RuleRepository, rule_version_repository: RuleVersionRepository, action_service: ActionService, rule_engine: RuleEngine):
        self.rule_version_repository = rule_version_repository
        self.rule_repository = rule_repository
>>>>>>> rama-temporal
        self.action_service = action_service
        self.rule_engine = rule_engine


    async def execute_rules(self, event_name: str, order, metadata: dict):
        rules = await self.get_rules_by_event_name(event_name)
        metadata["amount"]= order.amount
        for rule in rules:
            flag = self.rule_engine.evaluate_tree(rule.tree, metadata)
            if flag:   
                await self.action_service.execute_action(rule.action, order, metadata)

<<<<<<< HEAD
=======

>>>>>>> rama-temporal
    async def create_rule(self, rule_create: RuleCreate) -> RuleVersion:
        event_name= rule_create.event_name.upper()
        name = rule_create.name.upper()
        action = rule_create.action.upper()
        self.validate_conditions(rule_create.tree)
        await self.validate_rule(event_name,name)
        self.action_service.validate_action(action)
<<<<<<< HEAD
        rule = RuleVersion.create_new(
=======
        rule = Rule.create_new(name=name, event_name=event_name)
        rule_version = RuleVersion.create_new(
>>>>>>> rama-temporal
            name=name,
            event_name=event_name, 
            tree=rule_create.tree,
            action=action  
        )
        new_rule_version = await self.rule_version_repository.create(rule_version)
        rule.actual_version = new_rule_version.id
        await self.rule_repository.create(rule)
        return new_rule_version
    
    async def update_rule(self, event_name: str, name: str, rule_create: RuleCreate) -> RuleVersion:
        event_name = event_name.upper()
        name = name.upper()
<<<<<<< HEAD
        rule = await self.get_rule_by_event_name_and_name(event_name, name)
        new_rule = RuleVersion.create_new(
            name=name,
            event_name=event_name,
            tree=rule_create.tree,
            action=rule_create.action.upper()
        )

        rule.active = not rule.active
=======
        rule = await self.rule_repository.get_by_event_name_and_name(event_name, name)
        rule_version = RuleVersion.create_new(
            name=name,
            event_name=event_name, 
            tree=rule_create.tree,
            action=rule_create.action  
        )
        new_rule_version = await self.rule_version_repository.create(rule_version)
>>>>>>> rama-temporal
        rule.updated_at = datetime.now()
        rule.actual_version = new_rule_version.id
        await self.rule_repository.update(rule)
        return new_rule_version

<<<<<<< HEAD
    
    async def get_rule_by_event_name_and_name(self, event_name: str, name: str) -> RuleVersion:
=======

    async def get_rule_history(self, event_name: str, name: str) -> list[RuleVersion]:
>>>>>>> rama-temporal
        event_name = event_name.upper()
        name = name.upper()
        rules = await self.rule_version_repository.get_all_by_event_name_and_name(event_name, name)
        if rules is None or len(rules) == 0:
            raise RuleNotExistError(event_name,name)
        return rules
    
    async def get_rule_by_event_name_and_name(self, event_name: str, name: str) -> RuleVersion:
        event_name = event_name.upper()
        name = name.upper()
        rule = await self.rule_repository.get_by_event_name_and_name(event_name, name)
        if not rule:
            raise RuleNotExistError(event_name,name)
        return await self.rule_version_repository.get_by_id(rule.actual_version) 
        


    async def get_rules_by_event_name(self, event_name: str) -> list[RuleVersion]:
        event_name = event_name.upper()
        rules = await self.rule_repository.get_by_event_name(event_name)
        if len(rules) == 0:
            raise RuleNotExistError(event_name)
        return [await self.rule_version_repository.get_by_id(rule.actual_version) for rule in rules]


    async def validate_rule(self, event_name: str, name: str) -> None:
        try:
            EVENTS(event_name)
            rule = await self.rule_repository.get_by_event_name_and_name(event_name, name)
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

   
        
        
