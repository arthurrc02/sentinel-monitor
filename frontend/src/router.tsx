import { Route, Routes } from "react-router-dom";

import { ComputerDetailPage } from "./pages/ComputerDetailPage";
import { DashboardPage } from "./pages/DashboardPage";

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/computers/:id" element={<ComputerDetailPage />} />
    </Routes>
  );
}
