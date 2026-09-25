// import { useEffect, useState } from "react";

// import { getBusinessInsights, getKPIs } from "../services/api";

// function Insights() {
//   const [selectedDataset, setSelectedDataset] = useState("olist");
//   const [insights, setInsights] = useState([]);
//   const [kpis, setKpis] = useState(null);

//   useEffect(() => {
//     const savedDataset = localStorage.getItem("selected_dataset") || "olist";

//     setSelectedDataset(savedDataset);

//     const loadInsights = async () => {
//       try {
//         const response = await getBusinessInsights(savedDataset);

//         setInsights(response.data.insights || []);

//         const kpiData = await getKPIs(savedDataset);

//         setKpis(kpiData);
//       } catch (error) {
//         console.error("Failed to load business insights:", error);

//         setInsights([]);
//       }
//     };

//     loadInsights();
//   }, []);

//   return (
//     <div className="fade-in bg-slate-200 px-6 py-6 lg:px-8">
//       <div className="mx-auto max-w-7xl">
//         <div className="mb-6">
//           <p className="text-sm font-semibold uppercase tracking-widest text-primary-600">
//             Business Intelligence
//           </p>

//           <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">
//             Business Insights
//           </h1>

//           <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
//             Discover key patterns, trends, and opportunities from your business
//             data.
//           </p>
//         </div>

//         <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-700">
//           <span className="h-2 w-2 rounded-full bg-emerald-500" />
//           Dataset:{" "}
//           {selectedDataset === "olist" ? "Olist Dataset" : "Custom Dataset"}
//         </div>

//         {kpis && (
//           <div className="mb-6 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
//             <div className="rounded-2xl border border-slate-300 bg-white p-5 shadow-card">
//               <p className="text-sm font-medium text-slate-500">
//                 Total Revenue
//               </p>

//               <p className="mt-2 text-2xl font-bold text-slate-900">
//                 {Number(kpis.total_revenue || 0).toLocaleString()}
//               </p>
//             </div>

//             <div className="rounded-2xl border border-slate-300 bg-white p-5 shadow-card">
//               <p className="text-sm font-medium text-slate-500">Total Orders</p>

//               <p className="mt-2 text-2xl font-bold text-slate-900">
//                 {Number(kpis.total_orders || 0).toLocaleString()}
//               </p>
//             </div>

//             <div className="rounded-2xl border border-slate-300 bg-white p-5 shadow-card">
//               <p className="text-sm font-medium text-slate-500">
//                 Total Customers
//               </p>

//               <p className="mt-2 text-2xl font-bold text-slate-900">
//                 {Number(kpis.total_customers || 0).toLocaleString()}
//               </p>
//             </div>

//             <div className="rounded-2xl border border-slate-300 bg-white p-5 shadow-card">
//               <p className="text-sm font-medium text-slate-500">
//                 Average Review
//               </p>

//               <p className="mt-2 text-2xl font-bold text-slate-900">
//                 {Number(kpis.avg_review_score || 0).toFixed(1)}
//                 <span className="ml-1 text-base font-medium text-slate-500">
//                   / 5
//                 </span>
//               </p>
//             </div>
//           </div>
//         )}

//         {insights.length > 0 ? (
//           <div className="border-t border-slate-300 pt-6">
//             <div className="mb-4">
//               <h2 className="text-xl font-semibold uppercase tracking-wide text-slate-900">
//                 Key Findings
//               </h2>

//               <p className="mt-1 text-sm text-slate-500">
//                 Important patterns identified from the selected dataset.
//               </p>
//             </div>

//             <div className="grid gap-5 md:grid-cols-2">
//               {insights.map((insight, index) => (
//                 <div
//                   key={`${insight.type}-${index}`}
//                   className={`rounded-2xl border p-6 shadow-card transition-shadow hover:shadow-lg ${
//                     insight.type === "recommendation"
//                       ? "border-primary-200 bg-primary-50"
//                       : insight.type === "interpretation"
//                         ? "border-slate-300 bg-slate-50 md:col-span-2"
//                         : insight.type === "alert"
//                           ? insight.title === "Revenue Growth Alert"
//                             ? "border-emerald-200 bg-emerald-50"
//                             : "border-amber-200 bg-amber-50"
//                           : insight.type === "opportunity"
//                             ? "border-emerald-200 bg-emerald-50"
//                             : "border-slate-300 bg-white"
//                   }`}
//                 >
//                   <div className="min-w-0">
//                     <p
//                       className={`text-base font-semibold uppercase tracking-wide ${
//                         insight.type === "recommendation"
//                           ? "text-primary-700"
//                           : insight.type === "alert"
//                             ? insight.title === "Revenue Growth Alert"
//                               ? "text-emerald-700"
//                               : "text-amber-700"
//                             : insight.type === "opportunity"
//                               ? "text-emerald-700"
//                               : insight.type === "interpretation"
//                                 ? "text-slate-700"
//                                 : "text-primary-600"
//                       }`}
//                     >
//                       {insight.title}
//                     </p>

//                     <p className="mt-3 text-sm leading-6 text-slate-600">
//                       {insight.message}
//                     </p>
//                   </div>
//                 </div>
//               ))}
//             </div>
//           </div>
//         ) : (
//           <div className="rounded-2xl border border-slate-300 bg-white p-8 shadow-card">
//             <p className="text-sm text-slate-500">
//               No insights are available for this dataset.
//             </p>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }

// export default Insights;

import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { getBusinessInsights, getKPIs } from "../services/api";

function Insights() {
  const { t } = useTranslation();

  const [selectedDataset, setSelectedDataset] = useState("olist");
  const [insights, setInsights] = useState([]);
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    const savedDataset = localStorage.getItem("selected_dataset") || "olist";

    setSelectedDataset(savedDataset);

    const loadInsights = async () => {
      try {
        const response = await getBusinessInsights(savedDataset);

        setInsights(response.data.insights || []);

        const kpiData = await getKPIs(savedDataset);

        setKpis(kpiData);
      } catch (error) {
        console.error("Failed to load business insights:", error);

        setInsights([]);
      }
    };

    loadInsights();
  }, []);

  const getInsightTitle = (insight) => {
    if (insight.title_key) {
      return t(insight.title_key);
    }

    return insight.title;
  };

  const getInsightMessage = (insight) => {
    if (insight.type === "interpretation" && insight.message_parts) {
      return insight.message_parts
        .map((part) => {
          return t(part.message_key, part.params || {});
        })
        .join(" ");
    }

    if (insight.message_key) {
      return t(insight.message_key, insight.params || {});
    }

    return insight.message;
  };

  return (
    <div className="fade-in bg-slate-200 px-6 py-4">
      <div className="w-full">
        <div className="mb-6">
          <p className="text-sm font-semibold uppercase tracking-widest text-primary-600">
            {/* {t("businessIntelligence")} */}
          </p>

          <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">
            {t("businessInsights")}
          </h1>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
            {t("businessInsightsPageDescription")}
          </p>
        </div>

        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-700">
          <span className="h-2 w-2 rounded-full bg-emerald-500" />
          {t("dataSource")}:{" "}
          {selectedDataset === "olist" ? t("olistDataset") : t("customDataset")}
        </div>

        {kpis && (
          <div className="mb-6 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            <div className="rounded-2xl border border-slate-300 bg-white p-5 shadow-card">
              <p className="text-sm font-medium text-slate-500">
                {t("totalRevenue")}
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {Number(kpis.total_revenue || 0).toLocaleString()}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-300 bg-white p-5 shadow-card">
              <p className="text-sm font-medium text-slate-500">
                {t("totalOrders")}
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {Number(kpis.total_orders || 0).toLocaleString()}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-300 bg-white p-5 shadow-card">
              <p className="text-sm font-medium text-slate-500">
                {t("totalCustomers")}
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {Number(kpis.total_customers || 0).toLocaleString()}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-300 bg-white p-5 shadow-card">
              <p className="text-sm font-medium text-slate-500">
                {t("averageReview")}
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {Number(kpis.avg_review_score || 0).toFixed(1)}

                <span className="ml-1 text-base font-medium text-slate-500">
                  / 5
                </span>
              </p>
            </div>
          </div>
        )}

        {insights.length > 0 ? (
          <div className="border-t border-slate-300 pt-6">
            <div className="mb-4">
              <h2 className="text-xl font-semibold uppercase tracking-wide text-slate-900">
                {t("keyFindings")}
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                {t("keyFindingsDescription")}
              </p>
            </div>

            <div className="grid gap-5 md:grid-cols-2">
              {insights.map((insight, index) => (
                <div
                  key={`${insight.type}-${index}`}
                  className={`rounded-2xl border p-6 shadow-card transition-shadow hover:shadow-lg ${
                    insight.type === "recommendation"
                      ? "border-primary-200 bg-primary-50"
                      : insight.type === "interpretation"
                        ? "border-slate-300 bg-slate-50 md:col-span-2"
                        : insight.type === "alert"
                          ? insight.title_key === "revenueGrowthAlertTitle"
                            ? "border-emerald-200 bg-emerald-50"
                            : "border-amber-200 bg-amber-50"
                          : insight.type === "opportunity"
                            ? "border-emerald-200 bg-emerald-50"
                            : "border-slate-300 bg-white"
                  }`}
                >
                  <div className="min-w-0">
                    <p
                      className={`text-base font-semibold uppercase tracking-wide ${
                        insight.type === "recommendation"
                          ? "text-primary-700"
                          : insight.type === "alert"
                            ? insight.title_key === "revenueGrowthAlertTitle"
                              ? "text-emerald-700"
                              : "text-amber-700"
                            : insight.type === "opportunity"
                              ? "text-emerald-700"
                              : insight.type === "interpretation"
                                ? "text-slate-700"
                                : "text-primary-600"
                      }`}
                    >
                      {getInsightTitle(insight)}
                    </p>

                    <p className="mt-3 text-sm leading-6 text-slate-600">
                      {getInsightMessage(insight)}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="rounded-2xl border border-slate-300 bg-white p-8 shadow-card">
            <p className="text-sm text-slate-500">{t("noInsightsAvailable")}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Insights;
