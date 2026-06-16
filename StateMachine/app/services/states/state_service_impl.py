from typing import List

from app.models import Order
from app.exceptions.exceptions import NoStateError, EventInvalidError
from app.models.state import State
from app.repositories.states.state_repository_abstract import StateRepository
from app.services.states.state_service_abstract import StateService
from app.services.events.event_service_abstract import EventService


class StateServiceImpl(StateService):
    def __init__(self, repository:StateRepository, event_service: EventService):
        self.repository = repository
        self.event_service = event_service

    async def event_handler(self, order_id:str, state:str, event: str, metadata: dict) -> str:
        state = await self.get_by_name(state)
        event = event.upper()
        if not(event in state.events):
            raise EventInvalidError(event = event, state = state.name)
        return await self.event_service.handle(order_id = order_id, event_name = event, metadata = metadata)


    async def get_by_name(self, state_name:str) -> State:
        state_name = state_name.upper()
        state = await self.repository.get_by_name(state_name)
        if state is None:
            raise NoStateError(state_name)
        return state

