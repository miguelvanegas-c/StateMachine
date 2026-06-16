from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends


from app.dependencies.dependencies import get_state_service, get_state_mapper
from app.services.states.state_service_abstract import StateService
from app.schemas.response_schemas import APIResponse
from app.mappers.states.state_mapper_abstract import StateMapper

router = APIRouter(prefix="/api/v1/states", tags=["States"])

@router.get("/{state_name}")
async def get_state(state_name:str, service: StateService = Depends(get_state_service), mapper: StateMapper = Depends(get_state_mapper)) -> APIResponse:
    state = await service.get_by_name(state_name)
    state_out = mapper.to_state_out(state)
    return APIResponse(message="States retrieved successfully", data=state_out, status_code=200)


