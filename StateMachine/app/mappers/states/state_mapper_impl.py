from app.mappers.states.state_mapper_abstract import StateMapper
from app.models.state import State
from bson import ObjectId

from app.schemas.state_schemas import StateOut


class StateMapperImpl(StateMapper):

    def from_mongo(self, state: dict) -> State:
        return State(
            id= str(state["_id"]),
            events=state.get("events", []),
            name=state.get("name", ""),
        )

    def to_mongo(self, state: State) -> dict:
        doc ={
            "name": state.name,
            "events": state.events
        }
        if state.id:
            doc["_id"] = ObjectId(state.id)
        return doc

    def to_state_out(self, state: State) -> StateOut:
        return StateOut(
            name=state.name,
            events=state.events
        )