# websocket_manager.py
from typing import Dict
from fastapi import WebSocket, WebSocketDisconnect
from app.models.order import Order



class ConnectionManager():

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}  

    async def connect(self, order_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[order_id] = websocket

    def disconnect(self, order_id: str):
        if order_id in self.active_connections:
            del self.active_connections[order_id]

    async def send_update(self, order_id: str, order: Order):
        ws = self.active_connections.get(order_id)
        if ws:
            try:
                order_out = self.to_orders_out(order)
                await ws.send_json(order_out)
            except WebSocketDisconnect:
                self.disconnect(order_id)

    def to_orders_out(self, order: Order) -> dict:
        return {
            "id": order.id,
            "products_id": order.products_id,
            "amount": order.amount,
            "state": order.state,
            "created_at": str(order.created_at),
            "updated_at": str(order.updated_at),    
            "transitions": [{
                "event": t.get("event"),
                "new_state": t.get("new_state"),
                "timestamp": str(t.get("timestamp"))
            } for t in order.transitions]
        }