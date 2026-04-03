import { Routes, Route, Link, Navigate } from "react-router-dom";
import { Card } from "../shared/ui/Card";
import { useAuth } from "../features/auth/auth";

function AdminHome() {
  return (
    <div className="page">
      <div className="pageHeader">
        <h1 className="h1">Admin</h1>
        <div className="subtle">Admin and moderator area backed by API RBAC.</div>
      </div>

      <div className="gridCards">
        <Card>
          <div className="sectionTitle">Admin Actions</div>
          <div className="muted small">
            This page is visible only when the current session has moderator or admin access.
          </div>
        </Card>
      </div>
    </div>
  );
}

function AdminRuns() {
  return (
    <div className="page">
      <h1 className="h1">Admin / Runs</h1>
      <div className="subtle">Protected workspace for reviewing runs.</div>
    </div>
  );
}

export function AdminPage() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <div className="state"><div className="stateTitle">Checking access</div><div className="stateBody">Loading your session...</div></div>;
  }

  if (!user || (user.role !== "admin" && user.role !== "moderator")) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="page">
      <div className="adminNav">
        <Link to="/admin">Overview</Link>
        <Link to="/admin/runs">Runs</Link>
      </div>

      <Routes>
        <Route index element={<AdminHome />} />
        <Route path="runs" element={<AdminRuns />} />
      </Routes>
    </div>
  );
}
