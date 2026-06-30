from app.exceptions.exceptions import EventNotExistError, NoStateError
from app.services.transitions import TRANSITIONS
from app.models import Order
from app.services.event_service import EventService

class StateMachineService():
    def __init__(self, event_service: EventService):
        self.event_service = event_service

    async def process_event(self, order:Order, event_name:str, metadata:dict) -> str:
        next_state = self.transition_lookup(state = order.state, event_name = event_name)
        await self.event_service.handle_event(order = order, event_name = event_name, metadata = metadata)
        return next_state
    
    def transition_lookup(self, state:str, event_name:str) -> dict:
        transitions = TRANSITIONS.get(state)
        if transitions is None:
            raise NoStateError(state)
        next_state = transitions.get(event_name)
        if next_state is None:
            raise EventNotExistError(event_name)
        return next_state 

    
        