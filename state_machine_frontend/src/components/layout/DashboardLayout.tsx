import { useEffect } from "react";
import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { ErrorModal } from "../common/ErrorModal";
import { useError } from "../../context/ErrorContext";
import { setErrorHandler } from "../../services/api";

export const DashboardLayout = () => {
  const { showError } = useError();

  useEffect(() => {
    setErrorHandler(showError);
  }, [showError]);

  return (
    <div className="dashboard-container">
      <Sidebar />
      <main className="dashboard-content">
        <Outlet />
      </main>
      <ErrorModal />
    </div>
  );
};
