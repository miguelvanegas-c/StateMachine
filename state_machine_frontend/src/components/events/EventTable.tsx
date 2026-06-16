import { useState } from "react";
import type { Event } from "../../models/event";
import { AddRuleModal } from "./AddRuleModal";

interface Props {
  events: Event[];
  onRefresh: () => void;
}

export const EventTable = ({ events, onRefresh }: Props) => {
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);

  return (
    <>
      <table>
        <thead>
          <tr>
            <th>Event Name</th>
            <th>Next State</th>
            <th>Rules</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {events.map((event) => (
            <tr key={event.id}>
              <td>{event.event_name}</td>
              <td>{event.next_state_name}</td>
              <td>
                <ul>
                  {event.rules.map((rule, idx) => (
                    <li key={idx}>
                      {rule.meta_data_key} {rule.operator} {rule.value} → actions: {rule.actions.join(", ")}
                    </li>
                  ))}
                </ul>
              </td>
              <td>
                <button onClick={() => setSelectedEvent(event)}>Add Rule</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {selectedEvent && (
        <AddRuleModal
          event={selectedEvent}
          onClose={() => setSelectedEvent(null)}
          onSuccess={onRefresh}
        />
      )}
    </>
  );
};