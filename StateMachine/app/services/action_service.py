


from app.repositories.tickets.ticket_repository_abstract import TicketRepository
from app.exceptions.exceptions import ActionNotExistError
from app.models.ticket import Ticket
import logging

logger = logging.getLogger(__name__)
class ActionService:

    def __init__(self,ticket_repository: TicketRepository):
        self.ticket_repository = ticket_repository
        self.actions: dict[str, callable] = {
            "TICKET": self.ticket_action
        }

    def validate_action(self, action:str):
       if action not in self.actions:
            raise ActionNotExistError(action)
    
    async def execute_action(self, action:str, order, metadata:dict):
        self.validate_action(action)
        action_function = self.actions[action]
        await action_function(order, metadata)

    async def ticket_action(self, order, metadata:dict):
        logger.info(f"Executing ticket action for order {order.id} with metadata: {metadata}")
        ticket = Ticket(
            order_id=order.id,
            message= "funciono",    
        )
        await self.ticket_repository.create_ticket(ticket)

    