from typing import List

from app.repositories.states.state_repository_abstract import StateRepository
from app.models.state import State
from app.config.database_config import db
from app.mappers.states.state_mapper_abstract import StateMapper


class StateRepositoryImpl(StateRepository):

    def __init__(self, mapper: StateMapper):
        self.mapper = mapper


    async def get_by_name(self, name: str) -> State | None:
        document = await db["states"].find_one({"name": name})
        return self.mapper.from_mongo(document) if document else None


