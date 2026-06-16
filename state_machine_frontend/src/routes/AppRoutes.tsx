import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import { DashboardLayout } from "../components/layout/DashboardLayout";
import { OrdersPage } from "../pages/OrdersPage";
import { TicketsPage } from "../pages/TicketsPage";
import { EventsPage } from "../pages/EventsPage";
import { ErrorProvider } from "../context/ErrorContext";

export const AppRoutes = () => {

  return (
    <ErrorProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<DashboardLayout />}>
            <Route path="/orders" element={<OrdersPage />} />
            <Route path="/tickets" element={<TicketsPage />} />
            <Route path="/events" element={<EventsPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/orders" />} />
        </Routes>
      </BrowserRouter>
    </ErrorProvider>
  );
};
