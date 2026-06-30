from app.services.rule_service import RuleService
from app.models import Order, Ticket
from app.repositories.tickets.ticket_repository_abstract import TicketRepository

class EventService():

    def __init__(self, ticket_repository:TicketRepository, rule_service:RuleService):
        self.ticket_repository = ticket_repository
        self.rule_service = rule_service
        self.handler: dict[str, callable] = {
            "PAYMENTFAILED": self.handle_payment_failed
        }

    async def handle_event(self, order:Order, event_name:str, metadata:dict):
        handler = self.handler.get(event_name)
        if handler:
            await handler(order = order, metadata = metadata)
        await self.rule_service.execute_rules(event_name = event_name, order = order, metadata = metadata)    
    

    async def handle_payment_failed(self, order:Order, metadata:dict):
        if order.amount > 1000:
            ticket = Ticket.create(order_id = order.id, message = f"Payment failed for order {order.id} with amount {order.amount}")
            await self.ticket_repository.create_ticket(ticket)



