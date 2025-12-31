import { createBrowserRouter } from "react-router-dom";
import { AppLayout } from "./layout/AppLayout";
import { HomePage } from "../pages/HomePage";
import { AdminPage } from "../pages/AdminPage";
import { HsrPage } from "../features/hsr/pages/HsrPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: "hsr", element: <HsrPage /> },
      { path: "admin/*", element: <AdminPage /> }
    ]
  }
]);
