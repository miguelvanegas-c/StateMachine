import type { Ticket } from "../../models/ticket";

interface Props {
  tickets: Ticket[];
}

export const TicketTable = ({
  tickets
}: Props) => {

  return (

    <table>

      <thead>

        <tr>
          <th>Order ID</th>
          <th>Message</th>
          <th>Created At</th>
        </tr>

      </thead>

      <tbody>

        {tickets.map((ticket) => (

          <tr key={ticket.id}>

            <td>{ticket.order_id}</td>

            <td>{ticket.message}</td>

            <td>{ticket.created_at}</td>

          </tr>

        ))}

      </tbody>

    </table>

  );
};