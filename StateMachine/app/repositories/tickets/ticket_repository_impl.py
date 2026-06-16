from app.repositories.tickets.ticket_repository_abstract import TicketRepository
from app.models.ticket import Ticket
from app.config.database_config import db
from app.mappers.tickets.ticket_mapper_abstract import TicketMapper


class TicketRepositoryImpl(TicketRepository):

    def __init__(self, mapper: TicketMapper):
        self.mapper = mapper


    async def get_by_order_id(self, order_id: str) -> Ticket | None:
        document = await db["tickets"].find_one({"order_id": order_id})
        return self.mapper.from_mongo(document) if document else None

    async def create_ticket(self, ticket: Ticket) -> Ticket| None:
        doc = self.mapper.to_mongo(ticket)
        result = await db["tickets"].insert_one(doc)
        ticket.id = str(result.inserted_id)
        return ticket

    async def get_all_tickets(self) -> list[Ticket]:
        cursor = db["tickets"].find()
        tickets = []
        async for document in cursor:
            tickets.append(self.mapper.from_mongo(document))
        return tickets
