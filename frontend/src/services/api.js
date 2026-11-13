import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api',
  timeout: 10000,
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.message || error.message || 'The API request failed.';
    return Promise.reject(new Error(message));
  },
);

export const readApiError = (error) => {
  if (!error) return 'Unable to load the dashboard data.';
  return error.message || 'Unable to load the dashboard data.';
};

export const fetchDashboardSummary = () => api.get('/dashboard/summary');
export const fetchDashboardExport = () => api.get('/dashboard/export', { responseType: 'blob' });
export const fetchInventory = () => api.get('/inventory');
export const fetchSuppliers = () => api.get('/suppliers');
export const fetchForecasts = () => api.get('/forecasts');
export const fetchPurchaseOrders = () => api.get('/purchase-orders');
export const fetchShortages = () => api.get('/shortages');
export const fetchMitigation = () => api.get('/mitigation');

export default api;
