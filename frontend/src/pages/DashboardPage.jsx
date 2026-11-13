import { useEffect, useState } from 'react';

import KpiChart from '../components/KpiChart';
import StatCard from '../components/StatCard';
import DataTable from '../components/DataTable';
import { fetchDashboardExport, fetchDashboardSummary, fetchForecasts, fetchInventory, fetchShortages, fetchSuppliers, readApiError } from '../services/api';

export default function DashboardPage() {
  const [summary, setSummary] = useState({});
  const [inventory, setInventory] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [forecasts, setForecasts] = useState([]);
  const [shortages, setShortages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  const loadData = async () => {
    setLoading(true);
    setErrorMessage('');

    try {
      const [summaryResponse, inventoryResponse, supplierResponse, forecastResponse, shortageResponse] = await Promise.all([
        fetchDashboardSummary(),
        fetchInventory(),
        fetchSuppliers(),
        fetchForecasts(),
        fetchShortages(),
      ]);

      setSummary(summaryResponse.data || {});
      setInventory(Array.isArray(inventoryResponse.data) ? inventoryResponse.data.slice(0, 6) : []);
      setSuppliers(Array.isArray(supplierResponse.data) ? supplierResponse.data.slice(0, 6) : []);
      setForecasts(Array.isArray(forecastResponse.data) ? forecastResponse.data.slice(0, 6) : []);
      setShortages(Array.isArray(shortageResponse.data) ? shortageResponse.data : []);
    } catch (error) {
      setErrorMessage(readApiError(error));
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      const response = await fetchDashboardExport();
      const blob = new Blob([response.data], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'supply_chain_dashboard_export.csv';
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch (error) {
      setErrorMessage(readApiError(error));
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const inventoryColumns = [
    { key: 'sku_id', label: 'SKU' },
    { key: 'location_id', label: 'Location' },
    { key: 'on_hand_quantity', label: 'On Hand' },
    { key: 'safety_stock', label: 'Safety' },
  ];

  const forecastColumns = [
    { key: 'sku_id', label: 'SKU' },
    { key: 'location_id', label: 'Location' },
    { key: 'week_start', label: 'Week' },
    { key: 'forecast_units', label: 'Forecast' },
  ];

  const shortageColumns = [
    { key: 'sku_id', label: 'SKU' },
    { key: 'location_id', label: 'Location' },
    { key: 'projected_shortage_units', label: 'Shortage' },
    { key: 'severity', label: 'Severity' },
  ];

  const supplierColumns = [
    { key: 'supplier_id', label: 'Supplier' },
    { key: 'name', label: 'Name' },
    { key: 'country', label: 'Country' },
    { key: 'rating', label: 'Rating' },
    { key: 'capacity_units', label: 'Capacity' },
  ];

  const chartData = ['high', 'medium', 'low'].map((severity) => ({
    name: `${severity[0].toUpperCase()}${severity.slice(1)} Risk`,
    value: shortages.filter((shortage) => shortage.severity === severity).length,
  }));

  if (loading) {
    return <div className="container py-5"><div className="text-center">Loading dashboard...</div></div>;
  }

  return (
    <div className="container py-4">
      <div className="d-flex align-items-center justify-content-between mb-4">
        <div>
          <p className="text-uppercase small text-primary mb-1">Operations overview</p>
          <h2 className="mb-0">Demand & inventory dashboard</h2>
        </div>
        <div className="d-flex gap-2">
          <button className="btn btn-outline-secondary" onClick={loadData} type="button">Refresh data</button>
          <button className="btn btn-primary" onClick={handleExport} type="button">Export CSV</button>
        </div>
      </div>

      {errorMessage ? (
        <div className="alert alert-warning" role="alert">
          {errorMessage}
        </div>
      ) : null}

      <div className="row g-4 mb-4">
        <StatCard title="SKUs" value={summary.total_skus ?? 0} accent="primary" />
        <StatCard title="Locations" value={summary.total_locations ?? 0} accent="success" />
        <StatCard title="Suppliers" value={summary.total_suppliers ?? 0} accent="warning" />
        <StatCard title="Shortages" value={summary.projected_shortages ?? 0} accent="danger" />
      </div>

      <div className="row g-4 mb-4">
        <div className="col-lg-8">
          <KpiChart data={chartData} />
        </div>
        <div className="col-lg-4">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <h5 className="card-title mb-3">Operational snapshot</h5>
              <ul className="list-group list-group-flush">
                <li className="list-group-item px-0"><strong>{summary.total_inventory_records ?? 0}</strong> inventory records</li>
                <li className="list-group-item px-0"><strong>{summary.open_purchase_orders ?? 0}</strong> open purchase orders</li>
                <li className="list-group-item px-0"><strong>{summary.at_risk_locations ?? 0}</strong> at-risk locations</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div className="row g-4">
        <div className="col-lg-6">
          <DataTable title="Inventory" columns={inventoryColumns} rows={inventory} />
        </div>
        <div className="col-lg-6">
          <DataTable title="Suppliers" columns={supplierColumns} rows={suppliers} />
        </div>
        <div className="col-lg-6">
          <DataTable title="Forecasts" columns={forecastColumns} rows={forecasts} />
        </div>
        <div className="col-lg-12">
          <DataTable title="Projected shortages" columns={shortageColumns} rows={shortages} />
        </div>
      </div>
    </div>
  );
}
