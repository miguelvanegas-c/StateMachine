import { useEvents } from "../hooks/useEvents";
import { EventTable } from "../components/events/EventTable";

export const EventsPage = () => {
  const { events, refreshEvents, loading } = useEvents();

  if (loading) return <div>Loading events...</div>;

  return (
    <div>
      <h1>Events</h1>
      <EventTable events={events} onRefresh={refreshEvents} />
    </div>
  );
};