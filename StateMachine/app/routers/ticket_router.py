from fastapi import APIRouter, Depends

from app.schemas.response_schemas import APIResponse
from app.services.tickets.ticket_service_abstract import TicketService
from app.dependencies.dependencies import get_ticket_service, get_ticket_mapper
from app.mappers.tickets.ticket_mapper_abstract import TicketMapper

router = APIRouter(prefix="/api/v1/tickets", tags=["tickets"])

@router.get("/{order_id}")
async def get_ticket(order_id:str, service: TicketService = Depends(get_ticket_service), mapper: TicketMapper = Depends(get_ticket_mapper)) -> APIResponse:
    ticket = await service.get_ticket(order_id)
    ticket_out = mapper.to_ticket_out(ticket)
    return APIResponse(message="States retrieved successfully", data=ticket_out, status_code=200)

@router.get("")
async def get_all_tickets(service: TicketService = Depends(get_ticket_service), mapper: TicketMapper = Depends(get_ticket_mapper)) -> APIResponse:
    tickets = await service.get_all_tickets()
    tickets_out = [mapper.to_ticket_out(ticket) for ticket in tickets]
    return APIResponse(message="States retrieved successfully", data=tickets_out, status_code=200)

