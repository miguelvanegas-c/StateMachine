import { useEffect, useState } from "react";
import { orderService } from "../../services/orderService";
import { createOrderSocket } from "../../services/orderSocketService";
import type { Order } from "../../models/order";
import { Modal } from "../common/Modal";
import { TransitionDiagram } from "./TransitionDiagram";

interface Props {
  orderId: string;
  onClose: () => void;
}

export const OrderViewModal = ({ orderId, onClose }: Props) => {
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);

  // 1. Cargar el estado inicial mediante HTTP
  useEffect(() => {
    let isMounted = true;

    const fetchInitialOrder = async () => {
      try {
        const data = await orderService.getById(orderId);
        if (isMounted) {
          setOrder(data);
          setLoading(false);
        }
      } catch (error) {
        console.error("Error fetching order:", error);
        if (isMounted) setLoading(false);
      }
    };

    fetchInitialOrder();

    return () => {
      isMounted = false;
    };
  }, [orderId]);

  // 2. Conectar WebSocket para recibir actualizaciones
  useEffect(() => {
    // Esperar a tener el pedido inicial antes de conectar (opcional, pero puede evitar condiciones de carrera)
    // En realidad podemos conectar aunque order aún sea null, pero el socket enviará el estado actual al conectar?
    // Depende del backend. Para mayor seguridad, conectamos inmediatamente.
    const socket = createOrderSocket(orderId);

    socket.onopen = () => {
      console.log("WebSocket conectado para orden", orderId);
    };

    socket.onmessage = (event) => {
      try {
        const updatedOrder = JSON.parse(event.data);
        setOrder(updatedOrder); // Reemplazamos con la orden actualizada
      } catch (error) {
        console.error("Error parsing WebSocket message", error);
      }
    };

    socket.onerror = (error) => {
      console.error("WebSocket error", error);
    };

    socket.onclose = () => {
      console.log("WebSocket cerrado para orden", orderId);
    };

    return () => {
      socket.close();
    };
  }, [orderId]);

  if (loading || !order) {
    return (
      <Modal>
        <p>Cargando orden...</p>
      </Modal>
    );
  }

  return (
    <Modal>
      <h2>Monitor de Orden</h2>
      <p>
        Estado actual: <strong>{order.state}</strong>
      </p>
      <br />
      <TransitionDiagram transitions={order.transitions} />
      <br />
      <button onClick={onClose}>Cerrar</button>
    </Modal>
  );
};