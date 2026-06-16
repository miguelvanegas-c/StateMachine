import { useState } from "react";
import { orderService } from "../../services/orderService";

interface Props {
  onSuccess: () => void;
}

export const CreateOrderForm = ({ onSuccess }: Props) => {

  const [amount, setAmount] = useState<number>(0);

  const [products, setProducts] = useState("");

  const handleCreate = async () => {

    const productsArray = products
      .split(",")
      .map((p) => p.trim());

    await orderService.create({
      products_id: productsArray,
      amount: amount
    });

    onSuccess();

    setAmount(0);
    setProducts("");
  };

  return (
    <div>

      <h2>Create Order</h2>

      <input
        placeholder="Products (p1,p2,p3)"
        value={products}
        onChange={(e) =>
          setProducts(e.target.value)
        }
      />

      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) =>
          setAmount(Number(e.target.value))
        }
      />

      <button onClick={handleCreate}>
        Create Order
      </button>

    </div>
  );
};