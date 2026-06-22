from app.exceptions.exceptions import EventNotExistError, NoStateError
from app.services.transitions import TRANSITIONS
from app.models import Order
from app.services.event_service import EventService

class StateMachineService():
    def __init__(self, event_service: EventService):
        self.event_service = event_service

    async def process_event(self, order:Order, event_name:str, metadata:dict) -> str:
        transitions = self.get_transitions(state = order.state)
        next_state = self.get_next_state(event_name = event_name, transitions = transitions)
        await self.event_service.hand_event(order = order, event_name = event_name, metadata = metadata)
        return next_state
    
    def get_transitions(self, state:str):
        transitions = TRANSITIONS.get(state)
        if transitions is None:
            raise NoStateError(state)
        return transitions   

    def get_next_state(self, event_name:str, transitions:dict):
        next_state = transitions.get(event_name)
        if next_state is None:
            raise EventNotExistError(event_name)
        return next_state