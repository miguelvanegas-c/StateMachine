from typing import Dict
from fastapi import WebSocket, WebSocketDisconnect

from app.models.order import Order


class ConnectionManager:

    def __init__(self):
        self.active_connections: Dict[str, list[WebSocket]] = {}

    async def connect(self, order_id: str, websocket: WebSocket):
        await websocket.accept()
        if order_id not in self.active_connections:
            self.active_connections[order_id] = []
        self.active_connections[order_id].append(websocket)

    def disconnect(self, order_id: str, websocket: WebSocket):
        connections = self.active_connections.get(order_id, [])
        if websocket in connections:
            connections.remove(websocket)
        if not connections:
            self.active_connections.pop(order_id, None)

    async def send_update(self, order_id: str, order: Order):
        connections = self.active_connections.get(order_id, [])
        disconnected = []
        for websocket in connections:
            try:
                await websocket.send_json(self._to_dict(order))
            except WebSocketDisconnect:
                disconnected.append(websocket)
        for websocket in disconnected:
            self.disconnect(order_id, websocket)

    def _to_dict(self, order: Order) -> dict:
        return {
            "id": order.id,
            "products_id": order.products_id,
            "amount": order.amount,
            "state": order.state,
            "created_at": str(order.created_at),
            "updated_at": str(order.updated_at),
            "transitions": [
                {
                    "event": t.get("event"),
                    "new_state": t.get("new_state"),
                    "timestamp": str(t.get("timestamp")),
                }
                for t in order.transitions
            ],
        }