from abc import ABC, abstractmethod
from typing import Dict
from fastapi import WebSocket
from app.schemas.order_schemas import OrderOut

class ConnectionManager(ABC):
    """Contrato base para gestores de conexiones WebSocket."""


    @abstractmethod
    async def connect(self, order_id: str, websocket: WebSocket) -> None:
        """Acepta y registra una nueva conexión WebSocket para una orden."""
        pass

    @abstractmethod
    def disconnect(self, order_id: str) -> None:
        """Elimina la conexión asociada a una orden."""
        pass

    @abstractmethod
    async def send_update(self, order_id: str, order_out: OrderOut) -> None:
        """Envía una actualización (OrderOut) al cliente conectado a la orden."""
        pass