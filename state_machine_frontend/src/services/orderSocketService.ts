export const createOrderSocket = (
  orderId: string
) => {

  return new WebSocket(
    `ws://localhost:8000/api/v1/orders/ws/${orderId}`
  );
};