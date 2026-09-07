import { useEffect, useState } from "react";

import CustomTooltip from "../components/CustomTooltip";
import ChartCard from "../components/ChartCard";
import Loader from "../components/Loader";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

import {
  getRevenueForecast,
  getOrdersForecast,
  getCustomersForecast,
} from "../services/api";

// function ForecastChart({ historical, predicted }) {
//   if (!historical || historical.length === 0) {
//     return (
//       <p className="text-sm text-gray-500">
//         Not enough historical data available for forecasting.
//       </p>
//     );
//   }

//   const lastPoint = historical[historical.length - 1];

//   // Connect the actual line to the start of the forecast
//   const chartData = [
//     ...historical.map((item) => ({
//       month: item.month,
//       actual: item.value,
//       forecast: null,
//     })),

//     {
//       month: lastPoint.month,
//       actual: lastPoint.value,
//       forecast: lastPoint.value,
//     },

//     ...predicted.map((item) => ({
//       month: item.month,
//       actual: null,
//       forecast: item.value,
//     })),
//   ];

//   return (
//     <ResponsiveContainer width="100%" height={260}>
//       <LineChart
//         data={chartData}
//         margin={{
//           top: 10,
//           right: 20,
//           left: 20,
//           bottom: 10,
//         }}
//       >
//         <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

//         <XAxis
//           dataKey="month"
//           axisLine={{
//             stroke: "#374151",
//             strokeWidth: 1.5,
//           }}
//           tickLine={false}
//           tick={{ fontSize: 11 }}
//         />

//         <YAxis
//           axisLine={{
//             stroke: "#374151",
//             strokeWidth: 1.5,
//           }}
//           tickLine={false}
//           tick={{ fontSize: 11 }}
//         />

//         <Tooltip content={<CustomTooltip />} />

//         <Line
//           type="monotone"
//           dataKey="actual"
//           stroke="#2563eb"
//           strokeWidth={2}
//         />

//         <Line
//           type="monotone"
//           dataKey="forecast"
//           stroke="#ea580c"
//           strokeWidth={2.5}
//           strokeDasharray="5 5"
//         />
//       </LineChart>
//     </ResponsiveContainer>
//   );
// }

function ForecastChart({ historical, predicted }) {
  if (!historical || historical.length === 0) {
    return (
      <p className="text-sm text-gray-500">
        Not enough historical data available for forecasting.
      </p>
    );
  }

  const chartData = historical.map((item, index) => ({
    month: item.month,
    actual: item.value,
    forecast: index === historical.length - 1 ? item.value : null,
  }));

  predicted.forEach((item) => {
    chartData.push({
      month: item.month,
      actual: null,
      forecast: item.value,
    });
  });

  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart
        data={chartData}
        margin={{
          top: 10,
          right: 20,
          left: 20,
          bottom: 10,
        }}
      >
        <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

        <XAxis
          dataKey="month"
          axisLine={{
            stroke: "#374151",
            strokeWidth: 1.5,
          }}
          tickLine={false}
          tick={{ fontSize: 11 }}
        />

        <YAxis
          axisLine={{
            stroke: "#374151",
            strokeWidth: 1.5,
          }}
          tickLine={false}
          tick={{ fontSize: 11 }}
        />

        <Tooltip content={<CustomTooltip />} />

        <Line
          type="monotone"
          dataKey="actual"
          stroke="#2563eb"
          strokeWidth={2}
        />

        <Line
          type="monotone"
          dataKey="forecast"
          stroke="#ea580c"
          strokeWidth={2.5}
          strokeDasharray="5 5"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

function ForecastPredictions() {
  const [forecastData, setForecastData] = useState(null);
  const [error, setError] = useState(null);
  const [datasetId, setDatasetId] = useState("olist");

  useEffect(() => {
    const savedDataset = localStorage.getItem("selected_dataset");

    if (savedDataset) {
      setDatasetId(savedDataset);
    }
  }, []);

  useEffect(() => {
    // Load all three forecasts together
    Promise.all([
      getRevenueForecast(datasetId),
      getOrdersForecast(datasetId),
      getCustomersForecast(datasetId),
    ])

      .then(([revenue, orders, customers]) => {
        // Keep each forecast ready for its corresponding chart
        setForecastData({
          revenue,
          orders,
          customers,
        });
      })

      .catch(() => {
        setError("Failed to load forecast data.");
      });
  }, [datasetId]);

  if (error) {
    return <p className="text-sm text-rose-600">{error}</p>;
  }

  if (!forecastData) {
    return <Loader label="Loading forecast data..." />;
  }

  return (
    <div className="grid gap-4 fade-in">
      {/* Revenue Forecast */}

      <ChartCard
        title="Revenue Forecast"
        description="Revenue forecast for the next 4 months."
      >
        <ForecastChart
          historical={forecastData.revenue.historical}
          predicted={forecastData.revenue.predicted}
        />
      </ChartCard>

      {/* Order Forecast */}

      <ChartCard
        title="Order Forecast"
        description="Order forecast for the next 4 months."
      >
        <ForecastChart
          historical={forecastData.orders.historical}
          predicted={forecastData.orders.predicted}
        />
      </ChartCard>

      {/* Customer Forecast */}

      <ChartCard
        title="Customer Satisfaction Forecast"
        description="Average customer review score forecast for the next 4 months"
      >
        <ForecastChart
          historical={forecastData.customers.historical}
          predicted={forecastData.customers.predicted}
        />
      </ChartCard>
    </div>
  );
}

export default ForecastPredictions;
