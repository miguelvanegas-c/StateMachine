import { useEffect, useState, useRef } from "react";
import type { Order } from "../models/order";
import { createOrderSocket } from "../services/orderSocketService";

export const useOrderSocket = (orderId: string) => {
  const [order, setOrder] = useState<Order | null>(null);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Si ya hay un socket para este orderId, no crear otro
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      return;
    }

    console.log("🟢 Creando WebSocket para", orderId);
    const socket = createOrderSocket(orderId);
    socketRef.current = socket;

    socket.onopen = () => console.log("🔌 WebSocket abierto");
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setOrder(data);
    };
    socket.onerror = (error) => console.error("❌ Error WS", error);
    socket.onclose = () => console.log("🔌 WebSocket cerrado");

    // Cleanup: cerrar el socket solo si el componente se desmonta
    return () => {
      console.log("🧹 Desmontando componente, cerrando socket");
      if (socketRef.current) {
        socketRef.current.close();
        socketRef.current = null;
      }
    };
  }, [orderId]); // Solo se ejecuta si cambia orderId

  return order;
};