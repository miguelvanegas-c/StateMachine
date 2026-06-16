import { useTickets } from "../hooks/useTickets";
import { TicketTable } from "../components/tickets/TicketTable";

export const TicketsPage = () => {

  const {
    tickets
  } = useTickets();

  return (

    <div>

      <h1>Tickets</h1>

      <TicketTable
        tickets={tickets}
      />

    </div>

  );
};