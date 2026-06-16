import { useOrders } from "../hooks/useOrders";
import { OrderTable } from "../components/orders/OrderTable";
import { CreateOrderForm } from "../components/orders/CreateOrderForm";

export const OrdersPage = () => {

  const { orders, refreshOrders } = useOrders();

  return (
    <div>

      <h1>Orders</h1>

      <CreateOrderForm
        onSuccess={refreshOrders}
      />

      <OrderTable
        orders={orders}
        onRefresh={refreshOrders}
      />

    </div>
  );
};