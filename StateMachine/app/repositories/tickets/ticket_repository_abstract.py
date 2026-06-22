from abc import ABC, abstractmethod

from app.models.ticket import Ticket


class TicketRepository(ABC):

    @abstractmethod
    async def create_ticket(self, ticket:Ticket) -> Ticket:
        raise NotImplementedError
