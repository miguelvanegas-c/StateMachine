from app.services.events.strategy.strategy_action import StrategyAction
from app.services.tickets.ticket_service_abstract import TicketService


@StrategyAction.register("TICKET")
class TicketStrategy(StrategyAction):
    async def execute(self, metadata:dict, order_id:str, service:TicketService):
        message =f"ticket for a support review, order id {order_id}"
        await service.create_ticket(order_id=order_id, message=message)

        


