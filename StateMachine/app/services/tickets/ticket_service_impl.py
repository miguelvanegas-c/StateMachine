from app.services.tickets.ticket_service_abstract import TicketService
from app.models.ticket import Ticket
from app.exceptions.exceptions import TicketNotExistError
from app.repositories.tickets.ticket_repository_abstract import TicketRepository


class TicketServiceImpl(TicketService):

    def __init__(self, repository: TicketRepository) -> None:
        self.repository = repository

    async def get_ticket(self, order_id:str) -> Ticket:
        ticket = await self.repository.get_by_order_id(order_id)
        if ticket is None:
            raise TicketNotExistError(order_id)
        return ticket

    async def create_ticket(self, order_id:str, message:str) -> Ticket:
        ticket = Ticket.create(order_id=order_id, message=message)
        new_ticket = await self.repository.create_ticket(ticket)
        return new_ticket

    async def get_all_tickets(self) -> list[Ticket]:
        tickets = await self.repository.get_all_tickets()
        if not tickets:
            raise TicketNotExistError("No tickets found")
        return tickets