from datetime import datetime
from app.mappers.transitions.transition_mapper_abstract import TransitionMapper
from app.models.transition import Transition


class TransitionMapperImpl(TransitionMapper):
    def from_mongo(self, doc: dict) -> Transition:
        return Transition(
            event=doc.get("event", ""),
            new_state=doc.get("new_state", ""),
            timestamp= doc.get("timestamp", ""),
        )

    def to_mongo(self, transition: Transition) -> dict:
        return {
            "event": transition.event,
            "new_state": transition.new_state,
            "timestamp": transition.timestamp
        }

    def to_dict(self, transition: Transition) -> dict:
        return {
            "event": transition.event,
            "new_state": transition.new_state,
            "timestamp": str(transition.timestamp) if transition.timestamp else None
        }