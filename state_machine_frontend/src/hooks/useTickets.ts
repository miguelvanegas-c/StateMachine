import { useEffect, useState } from "react";

import type { Ticket } from "../models/ticket";
import { ticketService } from "../services/ticketService";

export const useTickets = () => {

  const [tickets, setTickets] =
    useState<Ticket[]>([]);

  const fetchTickets = async () => {

    try {

      const data =
        await ticketService.getAll();

      setTickets(data);

    } catch (error) {

      console.error(
        "Error fetching tickets",
        error
      );
    }
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  return {
    tickets,
    refreshTickets: fetchTickets
  };
};