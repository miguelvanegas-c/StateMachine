from app.repositories.tickets.ticket_repository_abstract import TicketRepository
from app.models.ticket import Ticket
from app.config.database_config import db


class TicketRepositoryMongo(TicketRepository):

    
    async def create_ticket(self, ticket: Ticket) -> Ticket| None:
        doc = self.to_doc(ticket)
        result = await db["tickets"].insert_one(doc)
        ticket.id = str(result.inserted_id)
        return ticket

    def to_doc(self, ticket: Ticket) -> dict:
        return {
            "order_id": ticket.order_id,
            "message": ticket.message,
            "created_at": ticket.created_at.isoformat() if ticket.created_at else None,
        }
