from enum import Enum
from typing import Set

from app.services.transitions import TRANSITIONS

def generate_event_enum(transitions: dict) -> type:
    events: Set[str] = set()
    for state_events in transitions.values():
        events.update(state_events.keys())
    return Enum(
        'OrderEvent', 
        {event: event for event in sorted(events)},
        module=__name__
    )

EVENTS = generate_event_enum(TRANSITIONS)
