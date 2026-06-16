from abc import ABC, abstractmethod

from app.models.ticket import Ticket
from app.schemas.ticket_schemas import TicketOut


class TicketMapper(ABC):
    @abstractmethod
    def from_mongo(self, doc: dict) -> Ticket:
        pass

    @abstractmethod
    def to_mongo(self, ticket: Ticket) -> dict:
        pass

    def to_ticket_out(self, ticket: Ticket) -> TicketOut:
        pass