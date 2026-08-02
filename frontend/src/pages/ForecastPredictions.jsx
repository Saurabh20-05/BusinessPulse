import { useEffect, useState } from "react";
import { Legend } from "recharts";
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


import { getForecastOverview } from "../services/api";










function ForecastChart({ historical, predicted }) {
  const lastPoint = historical[historical.length - 1];

  const chartData = [
    ...historical.map((item) => ({
      month: item.month,
      actual: item.value,
      forecast: null,
    })),

    {
      month: lastPoint.month,
      actual: lastPoint.value,
      forecast: lastPoint.value,
    },

    ...predicted.map((item) => ({
      month: item.month,
      actual: null,
      forecast: item.value,
    })),
  ];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart
  data={chartData}
  margin={{
    top: 20,
    right: 25,
    left: 30,
    bottom: 20,
  }}
>
        <CartesianGrid
    stroke="#d9dee8"
    strokeDasharray="3 3"
/>
        <XAxis
    dataKey="month"
    axisLine={{ stroke: "#374151", strokeWidth: 1.5 }}
    tickLine={false}
    tick={{ fontSize:12 }}
/>
        <YAxis
    axisLine={{ stroke: "#374151", strokeWidth: 1.5 }}
    tickLine={false}
    tick={{ fontSize: 12 }}
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
          strokeWidth={3}
          strokeDasharray="5 5"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}




function ForecastPredictions() {
  const [forecastData, setForecastData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getForecastOverview()
      .then((response) => {
        setForecastData(response);
      })
      .catch(() => {
        setError("Failed to load forecast data.");
      });
  }, []);

  if (error) {
    return <p className="text-sm text-rose-600">{error}</p>;
  }

  if (!forecastData) {
    return <Loader label="Loading forecast data..." />;
  }

  return (
    <div className="grid gap-5 fade-in">
      <ChartCard
        title="Revenue Forecast"
        description="Revenue forecast for the next 4 months."
      >

        <ForecastChart
  historical={forecastData.revenue.historical}
  predicted={forecastData.revenue.predicted}
/>


      </ChartCard>

      <ChartCard
        title="Order Forecast"
        description="Order forecast for the next 4 months."
      >


        <ForecastChart
  historical={forecastData.orders.historical}
  predicted={forecastData.orders.predicted}
/>


      </ChartCard>

      <ChartCard
        title="Customer Forecast"
        description="Customer forecast for the next 4 months."
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