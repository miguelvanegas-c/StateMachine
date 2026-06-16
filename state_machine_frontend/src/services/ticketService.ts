import { api } from "./api";
import type { Ticket } from "../models/ticket";

export const ticketService = {

  async getAll(): Promise<Ticket[]> {

    const response = await api.get(
      "/tickets"
    );

    /*
      FastAPI devuelve:
      {
        message: ...
        status_code: ...
        data: [...]
      }
    */

    return response.data.data;
  }

};