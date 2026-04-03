import { Outlet } from "react-router-dom";
import { TopBar } from "./TopBar";

export function AppLayout() {
  return (
    <div className="appRoot">
      <TopBar />
      <div className="appContainer">
        <Outlet />
      </div>
    </div>
  );
}
