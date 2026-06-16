import { useState } from "react";
import { Modal } from "../common/Modal";
import { eventService } from "../../services/eventService";
import type { Event, NewRule } from "../../models/event";

interface Props {
  event: Event;
  onClose: () => void;
  onSuccess: () => void;
}

const OPERATORS = [
  "equal to",
  "greater than",
  "less than",
  "less than or equal to",
  "greater than or equal to"
];

const RULE_TYPES = ["NUMBER"];

const AVAILABLE_ACTIONS = ["TICKET"];

export const AddRuleModal = ({ event, onClose, onSuccess }: Props) => {
  const [ruleType, setRuleType] = useState(RULE_TYPES[0]);
  const [metaDataKey, setMetaDataKey] = useState("");
  const [value, setValue] = useState<string>("");
  const [operator, setOperator] = useState(OPERATORS[0]);
  const [selectedActions, setSelectedActions] = useState<string[]>([]);

  const toggleAction = (action: string) => {
    setSelectedActions(prev =>
      prev.includes(action) ? prev.filter(a => a !== action) : [...prev, action]
    );
  };

  const handleSubmit = async () => {
    const rule: NewRule = {
      rule_type: ruleType,
      meta_data_key: metaDataKey,
      value: isNaN(Number(value)) ? value : Number(value),
      operator: operator,
      actions: selectedActions  // Aquí solo podrá ir "TICKET" si se selecciona
    };

    await eventService.addRule(event.event_name, rule);
    onSuccess();
    onClose();
  };

  return (
    <Modal>
      <h2>Add Rule to Event: {event.event_name}</h2>
      <div style={{ marginBottom: "10px" }}>
        <label>Rule Type:</label>
        <select value={ruleType} onChange={(e) => setRuleType(e.target.value)}>
          {RULE_TYPES.map(type => <option key={type}>{type}</option>)}
        </select>
      </div>
      <div style={{ marginBottom: "10px" }}>
        <label>Metadata Key:</label>
        <input type="text" value={metaDataKey} onChange={(e) => setMetaDataKey(e.target.value)} />
      </div>
      <div style={{ marginBottom: "10px" }}>
        <label>Operator:</label>
        <select value={operator} onChange={(e) => setOperator(e.target.value)}>
          {OPERATORS.map(op => <option key={op}>{op}</option>)}
        </select>
      </div>
      <div style={{ marginBottom: "10px" }}>
        <label>Value:</label>
        <input type="text" value={value} onChange={(e) => setValue(e.target.value)} />
      </div>
      <div style={{ marginBottom: "10px" }}>
        <label>Actions:</label>
        <div>
          {AVAILABLE_ACTIONS.map(action => (
            <label key={action} style={{ marginRight: "10px" }}>
              <input
                type="checkbox"
                checked={selectedActions.includes(action)}
                onChange={() => toggleAction(action)}
              />
              {action}
            </label>
          ))}
        </div>
      </div>
      <button onClick={handleSubmit}>Save Rule</button>
      <button onClick={onClose}>Cancel</button>
    </Modal>
  );
};