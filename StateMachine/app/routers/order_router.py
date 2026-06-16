from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.dependencies import get_order_service, get_order_mapper, get_connection_manager
from app.services.orders.order_service_abstract import OrderService
from app.schemas.order_schemas import OrderCreate, OrderOut, OrderUpdate
from app.schemas.response_schemas import APIResponse
from app.models import Order, Transition
from app.mappers.orders.order_mapper_abstract import OrderMapper
from app.services.events.ws.connection_manager_abstract import ConnectionManager
from fastapi import WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.post("")
async def create_order(create_order_schema: OrderCreate, service: OrderService = Depends(get_order_service), mapper:OrderMapper = Depends(get_order_mapper)) -> APIResponse:
    order = await service.create_order(create_order_schema)
    order_out = mapper.to_order_out(order)
    response = APIResponse(message= "Order created", status_code= 201, data=order_out)
    return response

@router.get("")
async def list_orders(service: OrderService = Depends(get_order_service), mapper:OrderMapper = Depends(get_order_mapper)) -> APIResponse:
    orders = await service.list_orders()
    orders_out = [mapper.to_order_out(order) for order in orders]
    response = APIResponse(message= "Orders", status_code= 200, data=orders_out)
    return response

@router.get("/{order_id}")
async def get_order(order_id: str, service: OrderService = Depends(get_order_service), mapper:OrderMapper = Depends(get_order_mapper)) -> APIResponse:
    order = await service.get_order(order_id)
    order_out = mapper.to_order_out(order)
    response = APIResponse(message= "Order found", status_code= 200, data=order_out)
    return response


@router.put("")
async def update_order(order_update: OrderUpdate, service: OrderService = Depends(get_order_service), mapper:OrderMapper = Depends(get_order_mapper)):
    order = await service.update_order(order_update)
    order_out = mapper.to_order_out(order)
    response = APIResponse(message= "Order updated", status_code= 200, data=order_out)
    return response

import asyncio

@router.websocket("/ws/{order_id}")
async def order_websocket(websocket: WebSocket, order_id: str, manager: ConnectionManager = Depends(get_connection_manager)):
    await manager.connect(order_id, websocket)
    try:
        await asyncio.Future() 
    except WebSocketDisconnect:
        manager.disconnect(order_id)


