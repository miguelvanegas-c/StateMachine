from abc import ABC, abstractmethod

from app.models.ticket import Ticket


class TicketRepository(ABC):

    @abstractmethod
    async def get_by_order_id(self, order_id: str) -> Ticket | None:
        raise NotImplementedError

    @abstractmethod
    async def create_ticket(self, ticket:Ticket) -> Ticket:
        raise NotImplementedError

    @abstractmethod
    async def get_all_tickets(self) -> list[Ticket]:
        raise NotImplementedError