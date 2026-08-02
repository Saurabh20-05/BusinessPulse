import axios from "axios";




const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
});


export const getDashboardSummary = () => {
  return api.get("/dashboard").then((response) => response.data);
};




export const getHistoricalAnalytics = () => {
  return api.get("/historical").then((response) => response.data);
};





export const getCurrentDashboard = () => {
  return api.get("/current").then((response) => response.data);
};





export const getForecastOverview = () => {
  return api.get("/forecast").then((response) => response.data);
};



export default api;
