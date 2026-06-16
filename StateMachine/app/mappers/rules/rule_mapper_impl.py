# app/mappers/rules/rule_mapper_impl.py
from app.mappers.rules.rule_mapper_abstract import RuleMapper
from app.models.rule import Rule

class RuleMapperImpl(RuleMapper):
    def from_mongo(self, doc: dict) -> Rule:
        return Rule(
            meta_data_key=doc.get("meta_data_key", ""),
            value=doc.get("value", ""),
            operator=doc.get("operator", ""),
            actions=doc.get("actions", []),
        )

    def to_mongo(self, rule: Rule) -> dict:
        return {
            "meta_data_key": rule.meta_data_key,
            "value": rule.value,
            "operator": rule.operator,
            "actions": rule.actions,
        }