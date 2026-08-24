import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
});

//   JWT Authentication

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    // Attach the token to requests when the user is logged in

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

//   Handle Authentication Errors

api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Clear the old token and send the user back to login
      localStorage.removeItem("access_token");

      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  },
);

//   Current Dashboard

export const getKPIs = () =>
  api.get("/current/kpis").then((response) => response.data);

export const getRecentOrders = () =>
  api.get("/current/recent-orders").then((response) => response.data);

export const getCurrentTopCategories = () =>
  api.get("/current/top-categories").then((response) => response.data);

//   Historical Analytics

export const getMonthlyRevenue = () =>
  api.get("/historical/monthly-revenue").then((response) => response.data);

export const getMonthlyOrders = () =>
  api.get("/historical/monthly-orders").then((response) => response.data);

export const getRevenueByCategory = () =>
  api.get("/historical/revenue-by-category").then((response) => response.data);

export const getHistoricalTopCategories = () =>
  api.get("/historical/top-categories").then((response) => response.data);

export const getPaymentDistribution = () =>
  api.get("/historical/payment-distribution").then((response) => response.data);

export const getCustomersByState = () =>
  api.get("/historical/customers-by-state").then((response) => response.data);

export const getReviewDistribution = () =>
  api.get("/historical/review-distribution").then((response) => response.data);

export const getPriceDistribution = () =>
  api.get("/historical/price-distribution").then((response) => response.data);

export const getRevenueVsOrders = () =>
  api.get("/historical/revenue-vs-orders").then((response) => response.data);

export const getCorrelationHeatmap = () =>
  api.get("/historical/correlation-heatmap").then((response) => response.data);

//   Forecast

export const getRevenueForecast = () =>
  api.get("/forecast/revenue").then((response) => response.data);

export const getOrdersForecast = () =>
  api.get("/forecast/orders").then((response) => response.data);

export const getCustomersForecast = () =>
  api.get("/forecast/customers").then((response) => response.data);

//   Authentication

export const signupUser = (userData) =>
  api.post("/auth/signup", userData).then((response) => response.data);

export const loginUser = (credentials) =>
  api.post("/auth/login", credentials).then((response) => response.data);

export const getCurrentUser = () =>
  api.get("/auth/me").then((response) => response.data);

export default api;
