from abc import ABC, abstractmethod

from app.models.ticket import Ticket


class TicketService(ABC):

    @abstractmethod
    async def get_ticket(self, order_id:str) -> Ticket:
        pass

    @abstractmethod
    async def create_ticket(self, order_id:str, message:str) -> Ticket:
        pass

    @abstractmethod
    async def get_all_tickets(self) -> list[Ticket]:
        pass