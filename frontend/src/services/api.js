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

// Handle authentication errors

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

export const getKPIs = (datasetId = "olist") =>
  api
    .get("/current/kpis", {
      params: { dataset_id: datasetId },
    })
    .then((response) => response.data);

export const getRecentOrders = (datasetId = "olist") =>
  api
    .get("/current/recent-orders", {
      params: { dataset_id: datasetId },
    })
    .then((response) => response.data);

export const getCurrentTopCategories = (datasetId = "olist") =>
  api
    .get("/current/top-categories", {
      params: { dataset_id: datasetId },
    })
    .then((response) => response.data);

//   Historical Analytics

export const getMonthlyRevenue = (datasetId = "olist") =>
  api
    .get("/historical/monthly-revenue", {
      params: {
        dataset_id: datasetId,
      },
    })
    .then((response) => response.data);

export const getMonthlyOrders = (datasetId = "olist") =>
  api
    .get("/historical/monthly-orders", {
      params: {
        dataset_id: datasetId,
      },
    })
    .then((response) => response.data);

export const getRevenueByCategory = (datasetId = "olist") =>
  api
    .get("/historical/revenue-by-category", {
      params: {
        dataset_id: datasetId,
      },
    })
    .then((response) => response.data);

export const getHistoricalTopCategories = (datasetId = "olist") =>
  api
    .get("/historical/top-categories", {
      params: {
        dataset_id: datasetId,
      },
    })
    .then((response) => response.data);

export const getPaymentDistribution = (datasetId = "olist") =>
  api
    .get("/historical/payment-distribution", {
      params: {
        dataset_id: datasetId,
      },
    })
    .then((response) => response.data);

export const getCustomersByState = (datasetId = "olist") =>
  api
    .get("/historical/customers-by-state", {
      params: { dataset_id: datasetId },
    })
    .then((response) => response.data);

export const getReviewDistribution = (datasetId = "olist") =>
  api
    .get("/historical/review-distribution", {
      params: { dataset_id: datasetId },
    })
    .then((response) => response.data);

export const getPriceDistribution = (datasetId = "olist") =>
  api
    .get("/historical/price-distribution", {
      params: { dataset_id: datasetId },
    })
    .then((response) => response.data);

export const getRevenueVsOrders = (datasetId = "olist") =>
  api
    .get("/historical/revenue-vs-orders", {
      params: { dataset_id: datasetId },
    })
    .then((response) => response.data);

export const getCorrelationHeatmap = (datasetId = "olist") =>
  api
    .get("/historical/correlation-heatmap", {
      params: { dataset_id: datasetId },
    })
    .then((response) => response.data);

//   Forecast

export const getRevenueForecast = (datasetId = "olist") =>
  api
    .get("/forecast/revenue", {
      params: { dataset_id: datasetId },
    })
    .then((response) => response.data);

export const getOrdersForecast = (datasetId = "olist") =>
  api
    .get("/forecast/orders", {
      params: { dataset_id: datasetId },
    })
    .then((response) => response.data);

export const getCustomersForecast = (datasetId = "olist") =>
  api
    .get("/forecast/customers", {
      params: { dataset_id: datasetId },
    })
    .then((response) => response.data);

//   Authentication

export const signupUser = (userData) =>
  api.post("/auth/signup", userData).then((response) => response.data);

export const loginUser = (credentials) =>
  api.post("/auth/login", credentials).then((response) => response.data);

export const getCurrentUser = () =>
  api.get("/auth/me").then((response) => response.data);

// Dataset management
export const uploadDataset = (file) => {
  const formData = new FormData();

  formData.append("file", file);

  return api.post("/dataset/upload", formData);
};

export const configureDataset = (datasetId, mapping) => {
  return api.post("/dataset/configure", {
    dataset_id: datasetId,
    mapping,
  });
};

export const getMyDatasets = () => {
  return api.get("/dataset");
};

export const deleteDataset = (datasetId) => {
  return api.delete(`/dataset/${datasetId}`);
};

export const previewDataset = (datasetId) => {
  return api.get(`/dataset/${datasetId}/preview`);
};

// Business insights
export const getBusinessInsights = (datasetId = "olist") => {
  return api.get("/insights", {
    params: {
      dataset_id: datasetId,
    },
  });
};

// Data quality
export const getDataQuality = (datasetId = "olist") =>
  api
    .get("/data-quality", {
      params: {
        dataset_id: datasetId,
      },
    })
    .then((response) => response.data);

export default api;
