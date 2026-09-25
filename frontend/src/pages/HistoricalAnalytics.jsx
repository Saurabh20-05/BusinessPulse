// import { useEffect, useState } from "react";
// import { useTranslation } from "react-i18next";

// import ChartCard from "../components/ChartCard";
// import Loader from "../components/Loader";
// import CustomTooltip from "../components/CustomTooltip";

// import {
//   ResponsiveContainer,
//   LineChart,
//   Line,
//   BarChart,
//   Bar,
//   PieChart,
//   Pie,
//   Cell,
//   ScatterChart,
//   Scatter,
//   XAxis,
//   YAxis,
//   CartesianGrid,
//   Tooltip,
//   Legend,
// } from "recharts";

// import {
//   getMonthlyRevenue,
//   getMonthlyOrders,
//   getRevenueByCategory,
//   getHistoricalTopCategories,
//   getPaymentDistribution,
//   getCustomersByState,
//   getReviewDistribution,
//   getPriceDistribution,
//   getRevenueVsOrders,
//   getCorrelationHeatmap,
// } from "../services/api";

// const PIE_COLORS = [
//   "#2563eb",
//   "#60a5fa",
//   "#93c5fd",
//   "#1d4ed8",
//   "#3b82f6",
//   "#bfdbfe",
// ];

// function HistoricalAnalytics() {

//   const { t } = useTranslation();
//   const [historicalData, setHistoricalData] = useState(null);
//   const [error, setError] = useState(null);
//   const [datasetId, setDatasetId] = useState("olist");

//   useEffect(() => {

//     const savedDataset = localStorage.getItem("selected_dataset");

// if (savedDataset) {
//   setDatasetId(savedDataset);
// }
//     // Load all historical data needed by the charts
//     Promise.all([
//       getMonthlyRevenue(datasetId),
//       getMonthlyOrders(datasetId),
//       getRevenueByCategory(datasetId),
//       getHistoricalTopCategories(datasetId),
//       getPaymentDistribution(datasetId),
//       getCustomersByState(datasetId),
//       getReviewDistribution(datasetId),
//       getPriceDistribution(datasetId),
//       getRevenueVsOrders(datasetId),
//       getCorrelationHeatmap(datasetId),
//     ])
//       .then(
//         ([
//           monthlyRevenue,
//           monthlyOrders,
//           revenueByCategory,
//           topCategories,
//           paymentDistribution,
//           customersByState,
//           reviewDistribution,
//           priceDistribution,
//           revenueVsOrders,
//           correlationHeatmap,
//         ]) => {
//           // Keep all chart data together for the dashboard
//           setHistoricalData({
//             monthly_revenue: monthlyRevenue,
//             monthly_orders: monthlyOrders,
//             revenue_by_category: revenueByCategory,
//             top_categories: topCategories,
//             payment_distribution: paymentDistribution,
//             customers_by_state: customersByState,
//             review_distribution: reviewDistribution,
//             price_distribution: priceDistribution,
//             revenue_vs_orders: revenueVsOrders,
//             correlation_heatmap: correlationHeatmap,
//           });
//         },
//       )
//       .catch(() => {
//         setError(t("failedToLoadHistoricalData"));
//       });
//   }, [datasetId]);

//   if (error) {
//     return <p className="text-sm text-rose-600">{error}</p>;
//   }

//   if (!historicalData) {
//     return <Loader label={t("loadingHistoricalData")} />;
//   }

//   // Show only the top categories in the pie chart
//   const topRevenueCategories = historicalData.revenue_by_category.slice(0, 6);

//   return (
//     <div className="grid grid-cols-1 xl:grid-cols-2 gap-4 fade-in">
//       <ChartCard
//   title={t("monthlyRevenue")}
//   description={t("monthlyRevenueDescription")}
// >
//         <ResponsiveContainer width="100%" height={260}>
//           <LineChart data={historicalData.monthly_revenue}>
//             <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

//             <XAxis
//               dataKey="month"
//               axisLine={{
//                 stroke: "#374151",
//                 strokeWidth: 1.5,
//               }}
//               tickLine={false}
//               tick={{ fontSize: 12 }}
//             />

//             <YAxis
//               axisLine={{
//                 stroke: "#374151",
//                 strokeWidth: 1.5,
//               }}
//               tickLine={false}
//               tick={{ fontSize: 12 }}
//             />

//             <Tooltip content={<CustomTooltip />} />

//             <Line
//               type="monotone"
//               dataKey="revenue"
//               stroke="#2563eb"
//               strokeWidth={2}
//             />
//           </LineChart>
//         </ResponsiveContainer>
//       </ChartCard>

//       <ChartCard
//   title={t("monthlyOrders")}
//   description={t("monthlyOrdersDescription")}
// >
//         <ResponsiveContainer width="100%" height={240}>
//           <BarChart data={historicalData.monthly_orders}>
//             <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

//             <XAxis
//               dataKey="month"
//               axisLine={{
//                 stroke: "#374151",
//                 strokeWidth: 1.5,
//               }}
//               tickLine={false}
//               tick={{ fontSize: 12 }}
//             />

//             <YAxis
//               axisLine={{
//                 stroke: "#374151",
//                 strokeWidth: 1.5,
//               }}
//               tickLine={false}
//               tick={{ fontSize: 12 }}
//             />

//             <Tooltip content={<CustomTooltip />} />

//             <Bar dataKey="orders" fill="#2563eb" />
//           </BarChart>
//         </ResponsiveContainer>
//       </ChartCard>

//       <ChartCard
//   title={t("topCategories")}
//   description={t("topCategoriesDescription")}
// >
//         <ResponsiveContainer width="100%" height={260}>
//           <BarChart
//             data={historicalData.top_categories}
//             layout="vertical"
//             margin={{
//               top: 10,
//               right: 20,
//               left: 40,
//               bottom: 10,
//             }}
//             barCategoryGap={14}
//           >
//             <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

//             <XAxis
//               type="number"
//               axisLine={{
//                 stroke: "#374151",
//                 strokeWidth: 1.5,
//               }}
//               tickLine={false}
//               tick={{ fontSize: 12 }}
//             />

//             <YAxis
//               dataKey="category"
//               type="category"
//               width={140}
//               axisLine={{
//                 stroke: "#374151",
//                 strokeWidth: 1.5,
//               }}
//               tickLine={false}
//               tick={{ fontSize: 12 }}
//             />

//             <Tooltip cursor={{ fill: "#eff6ff" }} content={<CustomTooltip />} />

//             <Bar
//               dataKey="revenue"
//               fill="#2563eb"
//               radius={[0, 8, 8, 0]}
//               barSize={18}
//             />
//           </BarChart>
//         </ResponsiveContainer>
//       </ChartCard>

//       <ChartCard
//   title={t("revenueByCategory")}
//   description={t("revenueByCategoryDescription")}
// >
//         <ResponsiveContainer width="100%" height={260}>
//           <PieChart>
//             <Pie
//               data={topRevenueCategories}
//               dataKey="revenue"
//               nameKey="category"
//               cx="50%"
//               cy="45%"
//               innerRadius={55}
//               outerRadius={110}
//               paddingAngle={3}
//               label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
//             >
//               {topRevenueCategories.map((_, index) => (
//                 <Cell
//                   key={index}
//                   fill={PIE_COLORS[index % PIE_COLORS.length]}
//                 />
//               ))}
//             </Pie>

//             <Tooltip content={<CustomTooltip />} />
//           </PieChart>
//         </ResponsiveContainer>
//       </ChartCard>

//       <ChartCard
//         title="Customers by State"
//         description="Customer distribution by state."
//       >
//         <ResponsiveContainer width="100%" height={240}>
//           <BarChart data={historicalData.customers_by_state}>
//             <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

//             <XAxis
//               dataKey="state"
//               axisLine={{
//                 stroke: "#374151",
//                 strokeWidth: 1.5,
//               }}
//               tickLine={false}
//               tick={{ fontSize: 12 }}
//             />

//             <YAxis
//               axisLine={{
//                 stroke: "#374151",
//                 strokeWidth: 1.5,
//               }}
//               tickLine={false}
//               tick={{ fontSize: 12 }}
//             />

//             <Tooltip content={<CustomTooltip />} />

//             <Bar dataKey="customers" fill="#60a5fa" />
//           </BarChart>
//         </ResponsiveContainer>
//       </ChartCard>

//       <ChartCard title="Review Scores" description="Review score distribution.">
//         <ResponsiveContainer width="100%" height={240}>
//           <BarChart data={historicalData.review_distribution}>
//             <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

//             <XAxis
//               dataKey="score"
//               axisLine={{
//                 stroke: "#374151",
//                 strokeWidth: 1.5,
//               }}
//               tickLine={false}
//               tick={{ fontSize: 12 }}
//             />

//             <YAxis
//               axisLine={{
//                 stroke: "#374151",
//                 strokeWidth: 1.5,
//               }}
//               tickLine={false}
//               tick={{ fontSize: 12 }}
//             />

//             <Tooltip content={<CustomTooltip />} />

//             <Bar dataKey="count" fill="#2563eb" />
//           </BarChart>
//         </ResponsiveContainer>
//       </ChartCard>

//       <ChartCard
//         title="Payment Methods"
//         description="Payment method distribution."
//       >
//         <ResponsiveContainer width="100%" height={240}>
//           <PieChart>
//             <Pie
//               data={historicalData.payment_distribution}
//               dataKey="count"
//               nameKey="payment_type"
//               cx="50%"
//               cy="50%"
//               innerRadius={45}
//               outerRadius={80}
//               paddingAngle={3}
//             >
//               {historicalData.payment_distribution.map((_, index) => (
//                 <Cell
//                   key={index}
//                   fill={PIE_COLORS[index % PIE_COLORS.length]}
//                 />
//               ))}
//             </Pie>

//             <Tooltip content={<CustomTooltip />} />

//             <Legend verticalAlign="bottom" height={36} />
//           </PieChart>
//         </ResponsiveContainer>
//       </ChartCard>

//       <ChartCard
//         title="Price Distribution"
//         description="Product price distribution."
//       >
//         <ResponsiveContainer width="100%" height={240}>
//           <BarChart data={historicalData.price_distribution}>
//             <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

//             <XAxis
//               dataKey="range"
//               axisLine={{
//                 stroke: "#374151",
//                 strokeWidth: 1.5,
//               }}
//               tickLine={false}
//               tick={{ fontSize: 12 }}
//             />

//             <YAxis
//               axisLine={{
//                 stroke: "#374151",
//                 strokeWidth: 1.5,
//               }}
//               tickLine={false}
//               tick={{ fontSize: 12 }}
//             />

//             <Tooltip content={<CustomTooltip />} />

//             <Bar dataKey="count" fill="#93c5fd" />
//           </BarChart>
//         </ResponsiveContainer>
//       </ChartCard>

//       <ChartCard
//         title="Revenue vs Orders"
//         description="Revenue compared with orders."
//         className="xl:col-span-2"
//       >
//         <ResponsiveContainer width="100%" height={240}>
//           <ScatterChart>
//             <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

//             <XAxis
//               type="number"
//               dataKey="orders"
//               name="Orders"
//               tick={{ fontSize: 13 }}
//             />

//             <YAxis
//               type="number"
//               dataKey="revenue"
//               name="Revenue"
//               tick={{ fontSize: 13 }}
//             />

//             <Tooltip content={<CustomTooltip />} />

//             <Scatter
//               name="Revenue vs Orders"
//               data={historicalData.revenue_vs_orders}
//               fill="#2563eb"
//             />
//           </ScatterChart>
//         </ResponsiveContainer>
//       </ChartCard>

//       <ChartCard
//         title="Correlation Heatmap"
//         description="Correlation between business metrics."
//       >
//         {(() => {
//           const labels = historicalData.correlation_heatmap.labels;

//           const matrix = historicalData.correlation_heatmap.matrix;

//           const values = {};

//           // Turn the matrix into values we can look up for each cell
//           matrix.forEach((item) => {
//             values[`${item.y}-${item.x}`] = item.value;
//           });

//           return (
//             <div className="overflow-x-auto">
//               <table className="w-full border border-slate-300 text-sm text-center">
//                 <thead>
//                   <tr>
//                     <th className="border p-2"></th>

//                     {labels.map((label) => (
//                       <th key={label} className="border p-2">
//                         {label}
//                       </th>
//                     ))}
//                   </tr>
//                 </thead>

//                 <tbody>
//                   {labels.map((row) => (
//                     <tr key={row}>
//                       <th className="border p-2">{row}</th>

//                       {labels.map((column) => (
//                         <td key={column} className="border p-2">
//                           {(values[`${row}-${column}`] ?? 0).toFixed(2)}
//                         </td>
//                       ))}
//                     </tr>
//                   ))}
//                 </tbody>
//               </table>
//             </div>
//           );
//         })()}
//       </ChartCard>
//     </div>
//   );
// }

// export default HistoricalAnalytics;











import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import ChartCard from "../components/ChartCard";
import Loader from "../components/Loader";
import CustomTooltip from "../components/CustomTooltip";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

import {
  getMonthlyRevenue,
  getMonthlyOrders,
  getRevenueByCategory,
  getHistoricalTopCategories,
  getPaymentDistribution,
  getCustomersByState,
  getReviewDistribution,
  getPriceDistribution,
  getRevenueVsOrders,
  getCorrelationHeatmap,
} from "../services/api";

const PIE_COLORS = [
  "#2563eb",
  "#60a5fa",
  "#93c5fd",
  "#1d4ed8",
  "#3b82f6",
  "#bfdbfe",
];

function HistoricalAnalytics() {
  const { t } = useTranslation();

  const [historicalData, setHistoricalData] = useState(null);
  const [error, setError] = useState(null);
  const [datasetId, setDatasetId] = useState("olist");

  useEffect(() => {
    const savedDataset = localStorage.getItem("selected_dataset");

    if (savedDataset) {
      setDatasetId(savedDataset);
    }

    // Load all historical data needed by the charts
    Promise.all([
      getMonthlyRevenue(datasetId),
      getMonthlyOrders(datasetId),
      getRevenueByCategory(datasetId),
      getHistoricalTopCategories(datasetId),
      getPaymentDistribution(datasetId),
      getCustomersByState(datasetId),
      getReviewDistribution(datasetId),
      getPriceDistribution(datasetId),
      getRevenueVsOrders(datasetId),
      getCorrelationHeatmap(datasetId),
    ])
      .then(
        ([
          monthlyRevenue,
          monthlyOrders,
          revenueByCategory,
          topCategories,
          paymentDistribution,
          customersByState,
          reviewDistribution,
          priceDistribution,
          revenueVsOrders,
          correlationHeatmap,
        ]) => {
          // Keep all chart data together for the dashboard
          setHistoricalData({
            monthly_revenue: monthlyRevenue,
            monthly_orders: monthlyOrders,
            revenue_by_category: revenueByCategory,
            top_categories: topCategories,
            payment_distribution: paymentDistribution,
            customers_by_state: customersByState,
            review_distribution: reviewDistribution,
            price_distribution: priceDistribution,
            revenue_vs_orders: revenueVsOrders,
            correlation_heatmap: correlationHeatmap,
          });
        },
      )
      .catch(() => {
        setError(t("failedToLoadHistoricalData"));
      });
  }, [datasetId, t]);

  if (error) {
    return <p className="text-sm text-rose-600">{error}</p>;
  }

  if (!historicalData) {
    return <Loader label={t("loadingHistoricalData")} />;
  }

  // Show only the top categories in the pie chart
  const topRevenueCategories = historicalData.revenue_by_category.slice(0, 6);

  return (
    <div className="grid grid-cols-1 xl:grid-cols-2 gap-4 fade-in">
      <ChartCard
        title={t("monthlyRevenue")}
        description={t("monthlyRevenueDescription")}
      >
        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={historicalData.monthly_revenue}>
            <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

            <XAxis
              dataKey="month"
              axisLine={{
                stroke: "#374151",
                strokeWidth: 1.5,
              }}
              tickLine={false}
              tick={{ fontSize: 12 }}
            />

            <YAxis
              axisLine={{
                stroke: "#374151",
                strokeWidth: 1.5,
              }}
              tickLine={false}
              tick={{ fontSize: 12 }}
            />

            <Tooltip content={<CustomTooltip />} />

            <Line
              type="monotone"
              dataKey="revenue"
              stroke="#2563eb"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard
        title={t("monthlyOrders")}
        description={t("monthlyOrdersDescription")}
      >
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={historicalData.monthly_orders}>
            <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

            <XAxis
              dataKey="month"
              axisLine={{
                stroke: "#374151",
                strokeWidth: 1.5,
              }}
              tickLine={false}
              tick={{ fontSize: 12 }}
            />

            <YAxis
              axisLine={{
                stroke: "#374151",
                strokeWidth: 1.5,
              }}
              tickLine={false}
              tick={{ fontSize: 12 }}
            />

            <Tooltip content={<CustomTooltip />} />

            <Bar dataKey="orders" fill="#2563eb" />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard
        title={t("topCategories")}
        description={t("topCategoriesDescription")}
      >
        <ResponsiveContainer width="100%" height={260}>
          <BarChart
            data={historicalData.top_categories}
            layout="vertical"
            margin={{
              top: 10,
              right: 20,
              left: 40,
              bottom: 10,
            }}
            barCategoryGap={14}
          >
            <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

            <XAxis
              type="number"
              axisLine={{
                stroke: "#374151",
                strokeWidth: 1.5,
              }}
              tickLine={false}
              tick={{ fontSize: 12 }}
            />

            <YAxis
              dataKey="category"
              type="category"
              width={140}
              axisLine={{
                stroke: "#374151",
                strokeWidth: 1.5,
              }}
              tickLine={false}
              tick={{ fontSize: 12 }}
            />

            <Tooltip
              cursor={{ fill: "#eff6ff" }}
              content={<CustomTooltip />}
            />

            <Bar
              dataKey="revenue"
              fill="#2563eb"
              radius={[0, 8, 8, 0]}
              barSize={18}
            />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard
        title={t("revenueByCategory")}
        description={t("revenueByCategoryDescription")}
      >
        <ResponsiveContainer width="100%" height={260}>
          <PieChart>
            <Pie
              data={topRevenueCategories}
              dataKey="revenue"
              nameKey="category"
              cx="50%"
              cy="45%"
              innerRadius={55}
              outerRadius={110}
              paddingAngle={3}
              label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
            >
              {topRevenueCategories.map((_, index) => (
                <Cell
                  key={index}
                  fill={PIE_COLORS[index % PIE_COLORS.length]}
                />
              ))}
            </Pie>

            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard
        title={t("customersByState")}
        description={t("customersByStateDescription")}
      >
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={historicalData.customers_by_state}>
            <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

            <XAxis
              dataKey="state"
              axisLine={{
                stroke: "#374151",
                strokeWidth: 1.5,
              }}
              tickLine={false}
              tick={{ fontSize: 12 }}
            />

            <YAxis
              axisLine={{
                stroke: "#374151",
                strokeWidth: 1.5,
              }}
              tickLine={false}
              tick={{ fontSize: 12 }}
            />

            <Tooltip content={<CustomTooltip />} />

            <Bar dataKey="customers" fill="#60a5fa" />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard
        title={t("reviewScores")}
        description={t("reviewScoresDescription")}
      >
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={historicalData.review_distribution}>
            <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

            <XAxis
              dataKey="score"
              axisLine={{
                stroke: "#374151",
                strokeWidth: 1.5,
              }}
              tickLine={false}
              tick={{ fontSize: 12 }}
            />

            <YAxis
              axisLine={{
                stroke: "#374151",
                strokeWidth: 1.5,
              }}
              tickLine={false}
              tick={{ fontSize: 12 }}
            />

            <Tooltip content={<CustomTooltip />} />

            <Bar dataKey="count" fill="#2563eb" />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard
        title={t("paymentMethods")}
        description={t("paymentMethodsDescription")}
      >
        <ResponsiveContainer width="100%" height={240}>
          <PieChart>
            <Pie
              data={historicalData.payment_distribution}
              dataKey="count"
              nameKey="payment_type"
              cx="50%"
              cy="50%"
              innerRadius={45}
              outerRadius={80}
              paddingAngle={3}
            >
              {historicalData.payment_distribution.map((_, index) => (
                <Cell
                  key={index}
                  fill={PIE_COLORS[index % PIE_COLORS.length]}
                />
              ))}
            </Pie>

            <Tooltip content={<CustomTooltip />} />

            <Legend verticalAlign="bottom" height={36} />
          </PieChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard
        title={t("priceDistribution")}
        description={t("priceDistributionDescription")}
      >
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={historicalData.price_distribution}>
            <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

            <XAxis
              dataKey="range"
              axisLine={{
                stroke: "#374151",
                strokeWidth: 1.5,
              }}
              tickLine={false}
              tick={{ fontSize: 12 }}
            />

            <YAxis
              axisLine={{
                stroke: "#374151",
                strokeWidth: 1.5,
              }}
              tickLine={false}
              tick={{ fontSize: 12 }}
            />

            <Tooltip content={<CustomTooltip />} />

            <Bar dataKey="count" fill="#93c5fd" />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard
        title={t("revenueVsOrders")}
        description={t("revenueVsOrdersDescription")}
        className="xl:col-span-2"
      >
        <ResponsiveContainer width="100%" height={240}>
          <ScatterChart>
            <CartesianGrid stroke="#d9dee8" strokeDasharray="3 3" />

            <XAxis
              type="number"
              dataKey="orders"
              name={t("orders")}
              tick={{ fontSize: 13 }}
            />

            <YAxis
              type="number"
              dataKey="revenue"
              name={t("revenue")}
              tick={{ fontSize: 13 }}
            />

            <Tooltip content={<CustomTooltip />} />

            <Scatter
              name={t("revenueVsOrders")}
              data={historicalData.revenue_vs_orders}
              fill="#2563eb"
            />
          </ScatterChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard
        title={t("correlationHeatmap")}
        description={t("correlationHeatmapDescription")}
      >
        {(() => {
          const labels = historicalData.correlation_heatmap.labels;

          const matrix = historicalData.correlation_heatmap.matrix;

          const values = {};

          // Turn the matrix into values we can look up for each cell
          matrix.forEach((item) => {
            values[`${item.y}-${item.x}`] = item.value;
          });

          return (
            <div className="overflow-x-auto">
              <table className="w-full border border-slate-300 text-sm text-center">
                <thead>
                  <tr>
                    <th className="border p-2"></th>

                    {labels.map((label) => (
                      <th key={label} className="border p-2">
                        {label}
                      </th>
                    ))}
                  </tr>
                </thead>

                <tbody>
                  {labels.map((row) => (
                    <tr key={row}>
                      <th className="border p-2">{row}</th>

                      {labels.map((column) => (
                        <td key={column} className="border p-2">
                          {(values[`${row}-${column}`] ?? 0).toFixed(2)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
        })()}
      </ChartCard>
    </div>
  );
}

export default HistoricalAnalytics;