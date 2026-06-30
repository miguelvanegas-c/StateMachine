from __future__ import annotations

import asyncio

from app.services.rule_service import RuleService
from app.models.rule import Rule
from app.models import order
from app.schemas.rule_schemas import RuleCreate, RuleOut, RuleUpdate
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.dependencies.dependencies import get_rule_service 
from app.schemas.response_schemas import APIResponse
from app.services.order_service import OrderService

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


@router.put("")
async def update_rule(
    rule_update: RuleUpdate,
    service: RuleService = Depends(get_rule_service),
) -> APIResponse:
    rule = await service.update_rule(rule_update)
    return APIResponse(message="Rule updated", status_code=200, data=to_rule_out(rule))



def to_rule_out(rule: Rule) -> RuleOut:
    return RuleOut(
        name=rule.name,
        event_name=rule.event_name,
        tree=rule.tree,
        action=rule.action,
    )