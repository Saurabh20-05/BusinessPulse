// import { useEffect, useState } from "react";

// import CustomTooltip from "../components/CustomTooltip";
// import ChartCard from "../components/ChartCard";
// import Loader from "../components/Loader";

// import {
//   ResponsiveContainer,
//   LineChart,
//   Line,
//   XAxis,
//   YAxis,
//   CartesianGrid,
//   Tooltip,
// } from "recharts";

// import {
//   getRevenueForecast,
//   getOrdersForecast,
//   getCustomersForecast,
// } from "../services/api";

// // function ForecastChart({ historical, predicted }) {
// //   if (!historical || historical.length === 0) {
// //     return (
// //       <p className="text-sm text-gray-500">
// //         Not enough historical data available for forecasting.
// //       </p>
// //     );
// //   }

// //   const lastPoint = historical[historical.length - 1];

// //   // Connect the actual line to the start of the forecast
// //   const chartData = [
// //     ...historical.map((item) => ({
// //       month: item.month,
// //       actual: item.value,
// //       forecast: null,
// //     })),

// //     {
// //       month: lastPoint.month,
// //       actual: lastPoint.value,
// //       forecast: lastPoint.value,
// //     },

// //     ...predicted.map((item) => ({
// //       month: item.month,
// //       actual: null,
// //       forecast: item.value,
// //     })),
// //   ];

// //   return (
// //     <ResponsiveContainer width="100%" height={260}>
// //       <LineChart
// //         data={chartData}
// //         margin={{
// //           top: 10,
// //           right: 20,
// //           left: 20,
// //           bottom: 10,
// //         }}
// //       >
// //         <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

// //         <XAxis
// //           dataKey="month"
// //           axisLine={{
// //             stroke: "#374151",
// //             strokeWidth: 1.5,
// //           }}
// //           tickLine={false}
// //           tick={{ fontSize: 11 }}
// //         />

// //         <YAxis
// //           axisLine={{
// //             stroke: "#374151",
// //             strokeWidth: 1.5,
// //           }}
// //           tickLine={false}
// //           tick={{ fontSize: 11 }}
// //         />

// //         <Tooltip content={<CustomTooltip />} />

// //         <Line
// //           type="monotone"
// //           dataKey="actual"
// //           stroke="#2563eb"
// //           strokeWidth={2}
// //         />

// //         <Line
// //           type="monotone"
// //           dataKey="forecast"
// //           stroke="#ea580c"
// //           strokeWidth={2.5}
// //           strokeDasharray="5 5"
// //         />
// //       </LineChart>
// //     </ResponsiveContainer>
// //   );
// // }

// function ForecastChart({ historical, predicted }) {
//   if (!historical || historical.length === 0) {
//     return (
//       <p className="text-sm text-gray-500">
//         Not enough historical data available for forecasting.
//       </p>
//     );
//   }

//   const chartData = historical.map((item, index) => ({
//     month: item.month,
//     actual: item.value,
//     forecast: index === historical.length - 1 ? item.value : null,
//   }));

//   predicted.forEach((item) => {
//     chartData.push({
//       month: item.month,
//       actual: null,
//       forecast: item.value,
//     });
//   });

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

// function ForecastPredictions() {
//   const [forecastData, setForecastData] = useState(null);
//   const [error, setError] = useState(null);
//   const [datasetId, setDatasetId] = useState("olist");

//   useEffect(() => {
//     const savedDataset = localStorage.getItem("selected_dataset");

//     if (savedDataset) {
//       setDatasetId(savedDataset);
//     }
//   }, []);

//   useEffect(() => {
//     // Load all three forecasts together
//     Promise.all([
//       getRevenueForecast(datasetId),
//       getOrdersForecast(datasetId),
//       getCustomersForecast(datasetId),
//     ])

//       .then(([revenue, orders, customers]) => {
//         // Keep each forecast ready for its corresponding chart
//         setForecastData({
//           revenue,
//           orders,
//           customers,
//         });
//       })

//       .catch(() => {
//         setError("Failed to load forecast data.");
//       });
//   }, [datasetId]);

//   if (error) {
//     return <p className="text-sm text-rose-600">{error}</p>;
//   }

//   if (!forecastData) {
//     return <Loader label="Loading forecast data..." />;
//   }

//   return (
//     <div className="grid gap-4 fade-in">
//       {/* Revenue Forecast */}

//       <ChartCard
//         title="Revenue Forecast"
//         description="Revenue forecast for the next 4 months."
//       >
//         <ForecastChart
//           historical={forecastData.revenue.historical}
//           predicted={forecastData.revenue.predicted}
//         />
//       </ChartCard>

//       {/* Order Forecast */}

//       <ChartCard
//         title="Order Forecast"
//         description="Order forecast for the next 4 months."
//       >
//         <ForecastChart
//           historical={forecastData.orders.historical}
//           predicted={forecastData.orders.predicted}
//         />
//       </ChartCard>

//       {/* Customer Forecast */}

//       <ChartCard
//         title="Customer Satisfaction Forecast"
//         description="Average customer review score forecast for the next 4 months"
//       >
//         <ForecastChart
//           historical={forecastData.customers.historical}
//           predicted={forecastData.customers.predicted}
//         />
//       </ChartCard>
//     </div>
//   );
// }

// export default ForecastPredictions;

// import { useEffect, useState } from "react";
// import { useTranslation } from "react-i18next";

// import CustomTooltip from "../components/CustomTooltip";
// import ChartCard from "../components/ChartCard";
// import Loader from "../components/Loader";

// import {
//   ResponsiveContainer,
//   LineChart,
//   Line,
//   XAxis,
//   YAxis,
//   CartesianGrid,
//   Tooltip,
// } from "recharts";

// import {
//   getRevenueForecast,
//   getOrdersForecast,
//   getCustomersForecast,
// } from "../services/api";

// function ForecastChart({ historical, predicted, notEnoughDataMessage }) {
//   if (!historical || historical.length === 0) {
//     return (
//       <p className="text-sm text-gray-500">
//         {notEnoughDataMessage}
//       </p>
//     );
//   }

//   const chartData = historical.map((item, index) => ({
//     month: item.month,
//     actual: item.value,
//     forecast: index === historical.length - 1 ? item.value : null,
//   }));

//   predicted.forEach((item) => {
//     chartData.push({
//       month: item.month,
//       actual: null,
//       forecast: item.value,
//     });
//   });

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

// function ForecastPredictions() {
//   const { t } = useTranslation();

//   const [forecastData, setForecastData] = useState(null);
//   const [error, setError] = useState(null);
//   const [datasetId, setDatasetId] = useState("olist");

//   useEffect(() => {
//     const savedDataset = localStorage.getItem("selected_dataset");

//     if (savedDataset) {
//       setDatasetId(savedDataset);
//     }
//   }, []);

//   useEffect(() => {
//     // Load all three forecasts together
//     Promise.all([
//       getRevenueForecast(datasetId),
//       getOrdersForecast(datasetId),
//       getCustomersForecast(datasetId),
//     ])
//       .then(([revenue, orders, customers]) => {
//         // Keep each forecast ready for its corresponding chart
//         setForecastData({
//           revenue,
//           orders,
//           customers,
//         });
//       })
//       .catch(() => {
//         setError(t("failedToLoadForecastData"));
//       });
//   }, [datasetId, t]);

//   if (error) {
//     return <p className="text-sm text-rose-600">{error}</p>;
//   }

//   if (!forecastData) {
//     return <Loader label={t("loadingForecastData")} />;
//   }

//   return (
//     <div className="grid gap-4 fade-in">
//       {/* Revenue Forecast */}

//       <ChartCard
//         title={t("revenueForecast")}
//         description={t("revenueForecastDescription")}
//       >
//         <ForecastChart
//           historical={forecastData.revenue.historical}
//           predicted={forecastData.revenue.predicted}
//           notEnoughDataMessage={t("notEnoughHistoricalData")}
//         />
//       </ChartCard>

//       {/* Order Forecast */}

//       <ChartCard
//         title={t("orderForecast")}
//         description={t("orderForecastDescription")}
//       >
//         <ForecastChart
//           historical={forecastData.orders.historical}
//           predicted={forecastData.orders.predicted}
//           notEnoughDataMessage={t("notEnoughHistoricalData")}
//         />
//       </ChartCard>

//       {/* Customer Forecast */}

//       <ChartCard
//         title={t("customerSatisfactionForecast")}
//         description={t("customerSatisfactionForecastDescription")}
//       >
//         <ForecastChart
//           historical={forecastData.customers.historical}
//           predicted={forecastData.customers.predicted}
//           notEnoughDataMessage={t("notEnoughHistoricalData")}
//         />
//       </ChartCard>
//     </div>
//   );
// }

// export default ForecastPredictions;

import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

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

const formatMonth = (value) => {
  if (!value) return "";

  const [year, month] = value.split("-");

  if (!year || !month) return value;

  return `${month}/${year.slice(-2)}`;
};

function ForecastChart({
  historical,
  predicted,
  notEnoughDataMessage,
  predictionType,
  t,
  i18n,
}) {
  if (!historical || historical.length === 0) {
    return <p className="text-sm text-slate-500">{notEnoughDataMessage}</p>;
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
    <ResponsiveContainer width="100%" height={300}>
      <LineChart
        data={chartData}
        margin={{
          top: 10,
          right: 20,
          left: 25,
          bottom: 10,
        }}
      >
        <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

        <XAxis
          dataKey="month"
          tickFormatter={formatMonth}
          axisLine={{
            stroke: "#374151",
            strokeWidth: 1.5,
          }}
          tickLine={false}
          tick={{ fontSize: 11 }}
        />

        <YAxis
          width={55}
          domain={predictionType === "customers" ? [3, 5.5] : ["auto", "auto"]}
          axisLine={{
            stroke: "#374151",
            strokeWidth: 1.5,
          }}
          tickLine={false}
          tick={{ fontSize: 11 }}
          label={({ viewBox }) => {
            const { x, y, height } = viewBox;
            const centerY = y + height / 2;
            const labelX = x - 18;

            return (
              <text
                x={labelX}
                y={centerY}
                transform={`rotate(-90 ${labelX} ${centerY})`}
                textAnchor="middle"
                dominantBaseline="middle"
                fill="#737373"
                fontSize={14}
              >
                {predictionType === "customers"
                  ? t("reviewScore")
                  : predictionType === "revenue"
                    ? t("revenue")
                    : t("orders")}
              </text>
            );
          }}
        />

        <Tooltip content={<CustomTooltip />} />

        <Line
          type="monotone"
          dataKey="actual"
          stroke="#2563eb"
          strokeWidth={2}
          dot={{ r: 4 }}
          activeDot={{ r: 6 }}
          name="Actual"
        />

        <Line
          type="monotone"
          dataKey="forecast"
          stroke="#ea580c"
          strokeWidth={2.5}
          strokeDasharray="5 5"
          dot={{ r: 4 }}
          activeDot={{ r: 6 }}
          name={t("forecast")}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

function ForecastPredictions() {
  const { t, i18n } = useTranslation();

  const [datasetId, setDatasetId] = useState("olist");

  const [predictionType, setPredictionType] = useState("revenue");

  const [selectedModel, setSelectedModel] = useState("linear");

  const [forecastData, setForecastData] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const savedDataset = localStorage.getItem("selected_dataset");

    if (savedDataset) {
      setDatasetId(savedDataset);
    }
  }, []);

  const predictionOptions = [
    {
      value: "revenue",
      label: t("revenue"),
    },
    {
      value: "orders",
      label: t("orders"),
    },
    {
      value: "customers",
      label: t("customerSatisfaction"),
    },
  ];

  const modelOptions = [
    {
      value: "linear",
      label: t("linearRegression"),
    },
    {
      value: "random_forest",
      label: t("randomForestRegression"),
    },
    {
      value: "polynomial",
      label: t("polynomialRegression"),
    },
  ];

  const getForecast = async () => {
    setLoading(true);
    setError(null);
    setForecastData(null);

    try {
      let response;

      if (predictionType === "revenue") {
        response = await getRevenueForecast(datasetId, selectedModel);
      } else if (predictionType === "orders") {
        response = await getOrdersForecast(datasetId, selectedModel);
      } else {
        response = await getCustomersForecast(datasetId, selectedModel);
      }

      setForecastData(response);
    } catch (error) {
      console.error("Failed to generate forecast:", error);

      setError(error.response?.data?.detail || t("failedToLoadForecastData"));
    } finally {
      setLoading(false);
    }
  };

  const getPredictionTitle = () => {
    if (predictionType === "revenue") {
      return t("revenueForecast");
    }

    if (predictionType === "orders") {
      return t("orderForecast");
    }

    return t("customerSatisfactionForecast");
  };

  const getPredictionDescription = () => {
    if (predictionType === "revenue") {
      return t("revenueForecastDescription");
    }

    if (predictionType === "orders") {
      return t("orderForecastDescription");
    }

    return t("customerSatisfactionForecastDescription");
  };

  if (loading) {
    return <Loader label={t("loadingForecastData")} />;
  }

  return (
    <div className="grid gap-5 fade-in">
      {/* Forecast Controls */}

      <ChartCard
        title={t("forecastControls")}
        description={t("forecastControlsDescription")}
      >
        <div className="grid gap-5 md:grid-cols-3">
          <div>
            <label
              htmlFor="predictionType"
              className="mb-2 block text-sm font-semibold text-slate-700"
            >
              {t("predictionType")}
            </label>

            <select
              id="predictionType"
              value={predictionType}
              onChange={(event) => {
                setPredictionType(event.target.value);
                setForecastData(null);
                setError(null);
              }}
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-700 outline-none transition focus:border-primary-500 focus:ring-2 focus:ring-primary-100"
            >
              {predictionOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label
              htmlFor="forecastModel"
              className="mb-2 block text-sm font-semibold text-slate-700"
            >
              {t("selectModel")}
            </label>

            <select
              id="forecastModel"
              value={selectedModel}
              onChange={(event) => {
                setSelectedModel(event.target.value);
                setForecastData(null);
                setError(null);
              }}
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-700 outline-none transition focus:border-primary-500 focus:ring-2 focus:ring-primary-100"
            >
              {modelOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-end">
            <button
              type="button"
              onClick={getForecast}
              className="w-full rounded-lg bg-primary-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-primary-700"
            >
              {t("generateForecast")}
            </button>
          </div>
        </div>

        {error && (
          <div className="mt-5 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
            {error}
          </div>
        )}
      </ChartCard>

      {forecastData && (
        <>
          {/* Selected Model */}

          <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-card">
              <p className="text-sm font-medium text-slate-500">
                {t("predictionType")}
              </p>

              <p className="mt-2 text-lg font-semibold text-slate-900">
                {getPredictionTitle()}
              </p>
            </div>

            <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-card">
              <p className="text-sm font-medium text-slate-500">
                {t("modelUsed")}
              </p>

              <p className="mt-2 text-lg font-semibold text-primary-600">
                {forecastData.model_used}
              </p>
            </div>
          </div>

          {/* Model Performance */}

          <ChartCard
            title={t("modelPerformance")}
            description={t("modelPerformanceDescription")}
          >
            <div className="grid gap-4 sm:grid-cols-3">
              <div className="rounded-xl border border-slate-200 bg-slate-50 p-5">
                <p className="text-sm font-medium text-slate-500">MAE</p>

                <p className="mt-2 text-2xl font-bold text-slate-900">
                  {forecastData.metrics.mae}
                </p>

                <p className="mt-1 text-xs text-slate-400">
                  {t("meanAbsoluteError")}
                </p>
              </div>

              <div className="rounded-xl border border-slate-200 bg-slate-50 p-5">
                <p className="text-sm font-medium text-slate-500">RMSE</p>

                <p className="mt-2 text-2xl font-bold text-slate-900">
                  {forecastData.metrics.rmse}
                </p>

                <p className="mt-1 text-xs text-slate-400">
                  {t("rootMeanSquaredError")}
                </p>
              </div>

              <div className="rounded-xl border border-slate-200 bg-slate-50 p-5">
                <p className="text-sm font-medium text-slate-500">R²</p>

                <p className="mt-2 text-2xl font-bold text-slate-900">
                  {forecastData.metrics.r2}
                </p>

                <p className="mt-1 text-xs text-slate-400">
                  {t("coefficientOfDetermination")}
                </p>
              </div>
            </div>
          </ChartCard>

          {/* Forecast Chart */}

          <ChartCard
            title={getPredictionTitle()}
            description={getPredictionDescription()}
          >
            <ForecastChart
              historical={forecastData.historical}
              predicted={forecastData.predicted}
              notEnoughDataMessage={t("notEnoughHistoricalData")}
              predictionType={predictionType}
              t={t}
              i18n={i18n}
            />
          </ChartCard>
        </>
      )}
    </div>
  );
}

export default ForecastPredictions;
