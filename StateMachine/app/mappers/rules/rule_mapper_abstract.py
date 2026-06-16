# app/mappers/rules/rule_mapper_abstract.py
from abc import ABC, abstractmethod
from app.models.rule import Rule

class RuleMapper(ABC):
    @abstractmethod
    def from_mongo(self, doc: dict) -> Rule:
        pass

    @abstractmethod
    def to_mongo(self, rule: Rule) -> dict:
        pass