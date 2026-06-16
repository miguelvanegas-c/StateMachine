import { useEffect, useState } from "react";
import { orderService } from "../../services/orderService";
import { stateService } from "../../services/stateService";
import type { Order } from "../../models/order";
import { MetadataFields } from "./MetadataFields";
import { Modal } from "../common/Modal";

interface Props {
  orderId: string;
  onClose: () => void;
  onSuccess: () => void;
}

interface MetadataField {
  key: string;
  value: string;
}

export const OrderEditModal = ({
  orderId,
  onClose,
  onSuccess
}: Props) => {

  const [order, setOrder] = useState<Order | null>(null);
  const [events, setEvents] = useState<string[]>([]);
  const [selectedEvent, setSelectedEvent] = useState("");
  const [metadataFields, setMetadataFields] = useState<MetadataField[]>([
                                                                          {
                                                                            key: "",
                                                                            value: ""
                                                                          }
                                                                        ]);
  const fetchFreshOrder =
    async () => {
    const freshOrder =
      await orderService.getById(
        orderId
      );
    setOrder(freshOrder);
    const state =
      await stateService.getState(
        freshOrder.state
      );
    setEvents(state.events);
  };

  useEffect(() => {
    fetchFreshOrder();
  }, []);

  const addMetadataField =
    () => {
    setMetadataFields([
      ...metadataFields,

      {
        key: "",
        value: ""
      }
    ]);
  };

  const updateMetadataField = (
    index: number,
    field:
      "key" | "value",
    value: string
  ) => {
    const updated =
      [...metadataFields];
    updated[index][field] =
      value;
    setMetadataFields(updated);
  };

  const removeMetadataField = (
    index: number
  ) => {
    setMetadataFields(
      metadataFields.filter(
        (_, i) => i !== index
      )
    );
  };

  const handleSubmit =
    async () => {
    const metadata:
      Record<string, unknown> = {};
    metadataFields.forEach(
      (field) => {
      if (
        field.key.trim() === ""
      ) return;
      let parsedValue:
        unknown =
          field.value;
      if (
        !isNaN(
          Number(field.value)
        )
      ) {
        parsedValue =
          Number(field.value);
      }
      else if (
        field.value
          .toLowerCase()
          === "true"
      ) {
        parsedValue = true;
      }
      else if (
        field.value
          .toLowerCase()
          === "false"
      ) {
        parsedValue = false;
      }
      metadata[
        field.key
      ] = parsedValue;
    });

    await orderService.update({
      id: orderId,
      event_type:
        selectedEvent,
      metadata: metadata
    });
    onSuccess();
    onClose();
  };

  return (
    <Modal>
      <h2>Edit Order</h2>
      <p>
        Current state:
        {order?.state}
      </p>
      <select
        onChange={(e) =>
          setSelectedEvent(
            e.target.value
          )
        }
      >
        <option>
          Select event
        </option>
        {events.map(
          (event) => (
          <option
            key={event}
            value={event}
          >
            {event}
          </option>
        ))}
      </select>
      <MetadataFields
        metadataFields={
          metadataFields
        }
        onAdd={
          addMetadataField
        }
        onRemove={
          removeMetadataField
        }
        onUpdate={
          updateMetadataField
        }
      />
      <br />
      <button
        onClick={
          handleSubmit
        }
      >
        Start Event
      </button>
      <button
        onClick={onClose}
      >
        Cancel
      </button>
    </Modal>
  );
};