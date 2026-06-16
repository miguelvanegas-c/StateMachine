import { api } from "./api";
import type { Event, NewRule } from "../models/event";

export const eventService = {
  async getAll(): Promise<Event[]> {
    const response = await api.get("/events");
    return response.data.data;
  },

  async getByName(name: string): Promise<Event> {
    const response = await api.get(`/events/${name}`);
    return response.data.data;
  },

  // Añadir una regla a un evento existente
  async addRule(eventName: string, rule: NewRule): Promise<Event> {
    const response = await api.put("/events/rule", {
      event_name: eventName,
      rule: rule
    });
    return response.data.data;
  }
};