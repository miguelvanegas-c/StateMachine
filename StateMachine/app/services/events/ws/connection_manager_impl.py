# websocket_manager.py
from typing import Dict
from fastapi import WebSocket, WebSocketDisconnect
from app.schemas.order_schemas import OrderOut
from app.services.events.ws.connection_manager_abstract import ConnectionManager
from app.mappers.orders.order_mapper_abstract import OrderMapper

class ConnectionManagerImpl(ConnectionManager):

    def __init__(self, mapper:OrderMapper):
        self.mapper = mapper
        self.active_connections: Dict[str, WebSocket] = {}  

    async def connect(self, order_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[order_id] = websocket

    def disconnect(self, order_id: str):
        if order_id in self.active_connections:
            del self.active_connections[order_id]

    async def send_update(self, order_id: str, order_out: OrderOut):
        ws = self.active_connections.get(order_id)
        if ws:
            try:
                await ws.send_json(self.mapper.to_dict(order_out))
            except WebSocketDisconnect:
                self.disconnect(order_id)

