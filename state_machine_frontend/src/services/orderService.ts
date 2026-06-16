import { api } from "./api";

export const orderService = {

  async getAll() {
    const response = await api.get("/orders");
    return response.data.data;
  },

  async getById(id: string) {
    const response = await api.get(`/orders/${id}`);
    return response.data.data;
  },

  async update(payload: {
    id: string;
    event_type: string;
    metadata: object;
  }) {
    const response = await api.put("/orders", payload);
    return response.data.data;
  },
  
  async create(order: {
    products_id: string[];
    amount: number;
  }) {

  const response = await api.post(
    "/orders",
    order
  );

  return response.data.data;
  }
}