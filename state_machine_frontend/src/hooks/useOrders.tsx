import { useEffect, useState } from "react";
import { orderService } from "../services/orderService.ts";
import type { Order } from "../models/order";

export const useOrders = () => {

  const [orders, setOrders] = useState<Order[]>([]);

  const fetchOrders = async () => {
    const data = await orderService.getAll();
    setOrders(data);
  }

  useEffect(() => {
    fetchOrders();
  }, []);

  return {
    orders,
    refreshOrders: fetchOrders
  }
}