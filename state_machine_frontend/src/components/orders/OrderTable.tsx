import type { Order } from "../../models/order";
import { useState } from "react";

import { OrderEditModal }
  from "./OrderEditModal";

import { OrderViewModal }
  from "./OrderViewModal";

interface Props {
  orders: Order[];
  onRefresh: () => void;
}

export const OrderTable = ({
  orders,
  onRefresh
}: Props) => {

  const [
    selectedOrderId,

    setSelectedOrderId

  ] = useState<
    string | null
  >(null);

  const [
    viewOrderId,

    setViewOrderId

  ] = useState<
    string | null
  >(null);

  return (

    <>

      <table>

        <thead>

          <tr>

            <th>ID</th>

            <th>State</th>

            <th>Amount</th>

            <th>Actions</th>

          </tr>

        </thead>

        <tbody>

          {orders.map(
            (order) => (

            <tr key={order.id}>

              <td>
                {order.id}
              </td>

              <td>
                {order.state}
              </td>

              <td>
                {order.amount}
              </td>

              <td>

                <button
                  onClick={() =>
                    setSelectedOrderId(
                      order.id
                    )
                  }
                >
                  Edit
                </button>

                {" "}

                <button
                  onClick={() =>
                    setViewOrderId(
                      order.id
                    )
                  }
                >
                  View
                </button>

              </td>

            </tr>

          ))}

        </tbody>

      </table>

      {/* Modal Edit */}

      {selectedOrderId && (

        <OrderEditModal

          orderId={
            selectedOrderId
          }

          onClose={() =>
            setSelectedOrderId(
              null
            )
          }

          onSuccess={
            onRefresh
          }

        />

      )}

      {/* Modal View */}

      {viewOrderId && (

        <OrderViewModal

          orderId={
            viewOrderId
          }

          onClose={() =>
            setViewOrderId(
              null
            )
          }

        />

      )}

    </>

  );
};