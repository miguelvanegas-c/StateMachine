from app.mappers.tickets.ticket_mapper_abstract import TicketMapper
from app.models.ticket import Ticket
from bson import ObjectId

from app.schemas.ticket_schemas import TicketOut


class TicketMapperImpl(TicketMapper):

    def from_mongo(self, ticket: dict) -> Ticket:
        return Ticket(
            id= str(ticket["_id"]),
            order_id=ticket.get("order_id", ""),
            message=ticket.get("message", ""),
            created_at=ticket.get("created_at", None),
        )

    def to_mongo(self, ticket: Ticket) -> dict:
        doc ={
            "order_id": ticket.order_id,
            "message": ticket.message,
            "created_at": ticket.created_at,
        }
        if ticket.id:
            doc["_id"] = ObjectId(ticket.id)
        return doc

    def to_ticket_out(self, ticket: Ticket) -> TicketOut:
        return TicketOut(
            order_id=ticket.order_id,
            message=ticket.message,
            created_at=ticket.created_at
        )