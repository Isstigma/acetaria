import { Routes, Route, Link } from "react-router-dom";
import { Card } from "../shared/ui/Card";

function AdminHome() {
  return (
    <div className="page">
      <div className="pageHeader">
        <h1 className="h1">Admin</h1>
        <div className="subtle">Stubbed structure (visuals minimal). Auth/RBAC not implemented.</div>
      </div>

      <div className="gridCards">
        <Card>
          <div className="sectionTitle">Admin Actions (Placeholders)</div>
          <div className="muted small">
            Backend admin endpoints exist and return dummy success responses.
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
      <div className="subtle">Placeholder page.</div>
    </div>
  );
}

export function AdminPage() {
  return (
    <div className="page">
      <div className="adminNav">
        <Link to="/admin">Overview</Link>
        <Link to="/admin/runs">Runs</Link>
      </div>

      <Routes>
        <Route path="/" element={<AdminHome />} />
        <Route path="runs" element={<AdminRuns />} />
      </Routes>
    </div>
  );
}
