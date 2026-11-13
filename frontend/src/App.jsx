import { Link, Route, Routes } from 'react-router-dom';

import DashboardPage from './pages/DashboardPage';

export default function App() {
  return (
    <>
      <nav className="navbar navbar-expand-lg bg-body-tertiary border-bottom">
        <div className="container">
          <span className="navbar-brand mb-0 h1">SCIO</span>
          <div className="navbar-nav">
            <Link className="nav-link" to="/">Overview</Link>
            <Link className="nav-link" to="/inventory">Inventory</Link>
          </div>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/inventory" element={<DashboardPage />} />
      </Routes>
    </>
  );
}
