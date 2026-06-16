import { api } from "./api";

export const stateService = {

  async getState(name: string) {
    const response = await api.get(`/states/${name}`);
    return response.data.data;
  }

}