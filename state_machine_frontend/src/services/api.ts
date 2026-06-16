import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000/api/v1"
});

// Callback set by the app once the error context is ready
let _onError: ((msg: string) => void) | null = null;

export const setErrorHandler = (handler: (msg: string) => void) => {
  _onError = handler;
};

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const data = error?.response?.data;

    // Most handlers send { success: false, message: "..." }
    // HTTPException / ValueError / generic send { error: "..." }
    const message: string =
      data?.message ||
      data?.error ||
      error?.message ||
      "Ocurrió un error inesperado";

    if (_onError) _onError(message);

    return Promise.reject(error);
  }
);
