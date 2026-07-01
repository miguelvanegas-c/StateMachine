from __future__ import annotations

import asyncio

from app.services.rule_service import RuleService
from app.models.rule_version import RuleVersion
from app.schemas.rule_schemas import RuleCreate, RuleOut
from fastapi import APIRouter, Depends
from dataclasses import asdict
from app.dependencies.dependencies import get_rule_service 
from app.schemas.response_schemas import APIResponse


router = APIRouter(prefix="/api/v1/rules", tags=["Rules"])


@router.post("", status_code=201)
async def create_rule(
    create_rule_schema: RuleCreate,
    service: RuleService = Depends(get_rule_service),
) -> APIResponse:
    rule = await service.create_rule(create_rule_schema)
    return APIResponse(message="Rule created", status_code=201, data=to_rule_out(rule))


@router.get("", status_code=200)
async def get_rule(
    event_name: str,
    name: str ,
    service: RuleService = Depends(get_rule_service),
) -> APIResponse:
    rule = await service.get_rule_by_event_name_and_name(event_name = event_name, name = name)
    return APIResponse(message="Rule found", status_code=200, data=to_rule_out(rule))

@router.get("/history", status_code=200)
async def get_rule_history(
    event_name: str,
    name: str ,
    service: RuleService = Depends(get_rule_service),
) -> APIResponse:
    rule_history = await service.get_rule_history(event_name = event_name, name = name)
    return APIResponse(message="Rule history found", status_code=200, data=[to_rule_out(rule) for rule in rule_history])

@router.patch("")
async def update_rule(
    rule_create: RuleCreate ,
    service: RuleService = Depends(get_rule_service),
    
) -> APIResponse:
    rule = await service.update_rule(rule_create)
    return APIResponse(message="Rule updated", status_code=200, data=to_rule_out(rule))


def to_rule_out(rule: RuleVersion) -> RuleOut:
    return RuleOut(
        name=rule.name,
        event_name=rule.event_name,
        tree=asdict(rule.tree),
        action=rule.action
    )