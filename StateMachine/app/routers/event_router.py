from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends


from app.dependencies.dependencies import get_event_service, get_event_mapper
from app.services.events.event_service_abstract import EventService
from app.schemas.response_schemas import APIResponse
from app.schemas.event_schemas import EventUpdate
from app.mappers.events.event_mapper_abstract import EventMapper

router = APIRouter(prefix="/api/v1/events", tags=["events"])

@router.get("/{event_name}")
async def get_event(event_name:str, service: EventService = Depends(get_event_service), mapper: EventMapper = Depends(get_event_mapper)) -> APIResponse:
    event = await service.get_by_name(event_name)
    event_out = mapper.to_event_out(event)
    return APIResponse(message="Events retrieved successfully", data=event_out, status_code=200)

@router.get("")
async def get_all_events(service: EventService = Depends(get_event_service), mapper: EventMapper = Depends(get_event_mapper)) -> APIResponse:
    events = await service.get_all()
    events_out = [mapper.to_event_out(event) for event in events]
    return APIResponse(message="Events retrieved successfully", data=events_out, status_code=200)

@router.put("/rule")
async def add_rule(event_update: EventUpdate, service:EventService = Depends(get_event_service), mapper: EventMapper = Depends(get_event_mapper)) -> APIResponse:
    event = await service.add_rule(event_update)
    event_out = mapper.to_event_out(event)
    return APIResponse(message="Rule added successfully", data=event_out, status_code=200)


