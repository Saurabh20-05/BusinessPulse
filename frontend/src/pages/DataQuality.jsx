// import { useEffect, useState } from "react";

// import ChartCard from "../components/ChartCard";
// import Loader from "../components/Loader";
// import PageHeader from "../components/PageHeader";

// import { getDataQuality, getMyDatasets } from "../services/api";

// function getStatusText(status) {
//   if (status === "good") {
//     return "Good";
//   }

//   if (status === "warning") {
//     return "Worth Checking";
//   }

//   return "Needs Review";
// }

// function getScoreStyle(score) {
//   if (score >= 90) {
//     return "text-emerald-600";
//   }

//   if (score >= 70) {
//     return "text-amber-500";
//   }

//   return "text-rose-600";
// }

// function DataQuality() {
//   const [qualityData, setQualityData] = useState(null);
//   const [error, setError] = useState(null);
//   const [datasetId, setDatasetId] = useState(
//     () => localStorage.getItem("selected_dataset") || "olist",
//   );
//   const [datasetName, setDatasetName] = useState("Olist Dataset");

//   useEffect(() => {
//     const savedDataset = localStorage.getItem("selected_dataset") || "olist";

//     setDatasetId(savedDataset);

//     if (savedDataset === "olist") {
//       setDatasetName("Olist Dataset");
//       return;
//     }

//     getMyDatasets()
//       .then((datasets) => {
//         const selected = datasets.find(
//           (dataset) => dataset.dataset_id === savedDataset,
//         );

//         setDatasetName(selected?.filename || "Custom Dataset");
//       })
//       .catch(() => {
//         setDatasetName("Custom Dataset");
//       });
//   }, []);

//   useEffect(() => {
//     setQualityData(null);
//     setError(null);

//     getDataQuality(datasetId)
//       .then((data) => {
//         setQualityData(data);
//       })
//       .catch(() => {
//         setError("Failed to load data quality information.");
//       });
//   }, [datasetId]);

//   if (error) {
//     return <p className="text-sm text-rose-600">{error}</p>;
//   }

//   if (!qualityData) {
//     return <Loader label="Loading data quality..." />;
//   }

//   const { quality_score, summary, checks, columns } = qualityData;

//   const checkCards = [
//     {
//       label: "Missing Values",
//       value: checks.missing_values.count,
//       percentage: checks.missing_values.percentage,
//       status: checks.missing_values.status,
//     },
//     {
//       label: "Duplicate Rows",
//       value: checks.duplicate_rows.count,
//       percentage: checks.duplicate_rows.percentage,
//       status: checks.duplicate_rows.status,
//     },
//     {
//       label: "Invalid Dates",
//       value: checks.invalid_dates.count,
//       percentage: checks.invalid_dates.percentage,
//       status: checks.invalid_dates.status,
//     },
//     {
//       label: "Negative Values",
//       value: checks.negative_values.count,
//       percentage: checks.negative_values.percentage,
//       status: checks.negative_values.status,
//     },
//   ];

//   return (
//     <div className="min-h-screen bg-slate-200">
//       <div className="max-w-7xl mx-auto px-6 py-8 fade-in space-y-5">
//         <PageHeader
//           title="Data Quality"
//           subtitle="Review your data for missing, duplicate, or invalid values."
//         />

//         <div className="bg-white rounded-xl shadow-sm p-4 flex items-center justify-between">
//           <span className="text-sm text-slate-500">Data Source</span>

//           <span className="px-4 py-2 rounded-full bg-blue-50 text-blue-600 text-sm font-medium">
//             {datasetName}
//           </span>
//         </div>

//         <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
//           <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
//             <p className="text-xs text-slate-500">Total Rows</p>

//             <p className="mt-1 text-xl font-semibold text-slate-800">
//               {summary.rows.toLocaleString()}
//             </p>
//           </div>

//           <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
//             <p className="text-xs text-slate-500">Total Columns</p>

//             <p className="mt-1 text-xl font-semibold text-slate-800">
//               {summary.columns.toLocaleString()}
//             </p>
//           </div>

//           <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
//             <p className="text-xs text-slate-500">Missing Values</p>

//             <p className="mt-1 text-xl font-semibold text-slate-800">
//               {summary.missing_values.toLocaleString()}
//             </p>
//           </div>

//           <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
//             <p className="text-xs text-slate-500">Duplicate Rows</p>

//             <p className="mt-1 text-xl font-semibold text-slate-800">
//               {summary.duplicate_rows.toLocaleString()}
//             </p>
//           </div>
//         </div>

//         <ChartCard
//           title="Data Quality Score"
//           description="A quick look at how clean and reliable your data is."
//         >
//           <div className="flex flex-col items-center justify-center py-5">
//             <div className="relative flex items-center justify-center w-28 h-28 rounded-full border-8 border-slate-100">
//               <span
//                 className={`text-4xl font-bold ${getScoreStyle(quality_score)}`}
//               >
//                 {quality_score}
//               </span>
//             </div>

//             <p
//               className={`mt-3 text-base font-semibold ${getScoreStyle(
//                 quality_score,
//               )}`}
//             >
//               {quality_score >= 90
//                 ? "Excellent"
//                 : quality_score >= 70
//                   ? "Good"
//                   : "Needs Review"}
//             </p>

//             <p className="mt-1 text-sm text-slate-500">out of 100</p>

//             <p className="mt-3 text-sm text-slate-500">
//               {quality_score >= 90
//                 ? "Your data looks clean and ready to use."
//                 : quality_score >= 70
//                   ? "Your data looks good, with a few things worth checking."
//                   : "There are a few data issues that should be reviewed."}
//             </p>
//           </div>
//         </ChartCard>

//         <ChartCard
//           title="Quality Checks"
//           description="A quick check for common data problems."
//         >
//           <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
//             {checkCards.map((check) => (
//               <div
//                 key={check.label}
//                 className="border border-slate-100 rounded-lg p-4"
//               >
//                 <div className="flex items-center justify-between">
//                   <p className="text-sm font-medium text-slate-700">
//                     {check.label}
//                   </p>

//                   <span
//                     className={`w-2.5 h-2.5 rounded-full ${
//                       check.status === "good"
//                         ? "bg-emerald-500"
//                         : check.status === "warning"
//                           ? "bg-amber-500"
//                           : "bg-rose-500"
//                     }`}
//                   />
//                 </div>

//                 <p className="mt-4 text-2xl font-semibold text-slate-800">
//                   {check.value.toLocaleString()}
//                 </p>

//                 <p className="mt-1 text-xs text-slate-500">
//                   {check.percentage}% of data
//                 </p>

//                 <p
//                   className={`mt-2 text-xs font-medium ${
//                     check.status === "good"
//                       ? "text-emerald-600"
//                       : check.status === "warning"
//                         ? "text-amber-600"
//                         : "text-rose-600"
//                   }`}
//                 >
//                   {getStatusText(check.status)}
//                 </p>
//               </div>
//             ))}
//           </div>
//         </ChartCard>

//         <ChartCard
//           title="Column Quality"
//           description="See how each column looks at a glance."
//         >
//           <div className="overflow-x-auto">
//             <table className="w-full text-sm">
//               <thead>
//                 <tr className="border-b border-slate-200 text-left">
//                   <th className="px-3 py-3 font-medium text-slate-600">
//                     Column
//                   </th>

//                   <th className="px-3 py-3 font-medium text-slate-600">Type</th>

//                   <th className="px-3 py-3 font-medium text-slate-600 text-right">
//                     Missing
//                   </th>

//                   <th className="px-3 py-3 font-medium text-slate-600 text-right">
//                     Unique
//                   </th>
//                 </tr>
//               </thead>

//               <tbody>
//                 {columns.map((column) => (
//                   <tr
//                     key={column.name}
//                     className="border-b border-slate-100 hover:bg-slate-50"
//                   >
//                     <td className="px-3 py-3 text-slate-700">{column.name}</td>

//                     <td className="px-3 py-3 text-slate-500 capitalize">
//                       {column.type}
//                     </td>

//                     <td className="px-3 py-3 text-right text-slate-700">
//                       {column.missing.toLocaleString()}
//                     </td>

//                     <td className="px-3 py-3 text-right text-slate-700">
//                       {column.unique.toLocaleString()}
//                     </td>
//                   </tr>
//                 ))}
//               </tbody>
//             </table>
//           </div>
//         </ChartCard>
//       </div>
//     </div>
//   );
// }

// export default DataQuality;





import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import ChartCard from "../components/ChartCard";
import Loader from "../components/Loader";
import PageHeader from "../components/PageHeader";

import { getDataQuality, getMyDatasets } from "../services/api";

function getStatusText(status, t) {
  if (status === "good") {
    return t("good");
  }

  if (status === "warning") {
    return t("worthChecking");
  }

  return t("needsReview");
}

function getScoreStyle(score) {
  if (score >= 90) {
    return "text-emerald-600";
  }

  if (score >= 70) {
    return "text-amber-500";
  }

  return "text-rose-600";
}

function DataQuality() {
  const { t } = useTranslation();

  const [qualityData, setQualityData] = useState(null);
  const [error, setError] = useState(null);
  const [datasetId, setDatasetId] = useState(
    () => localStorage.getItem("selected_dataset") || "olist",
  );
  const [datasetName, setDatasetName] = useState("Olist Dataset");

  useEffect(() => {
    const savedDataset = localStorage.getItem("selected_dataset") || "olist";

    setDatasetId(savedDataset);

    if (savedDataset === "olist") {
      setDatasetName(t("olistDataset"));
      return;
    }

    getMyDatasets()
      .then((datasets) => {
        const selected = datasets.find(
          (dataset) => dataset.dataset_id === savedDataset,
        );

        setDatasetName(selected?.filename || t("customDataset"));
      })
      .catch(() => {
        setDatasetName(t("customDataset"));
      });
  }, [t]);

  useEffect(() => {
    setQualityData(null);
    setError(null);

    getDataQuality(datasetId)
      .then((data) => {
        setQualityData(data);
      })
      .catch(() => {
        setError(t("failedToLoadDataQuality"));
      });
  }, [datasetId, t]);

  if (error) {
    return <p className="text-sm text-rose-600">{error}</p>;
  }

  if (!qualityData) {
    return <Loader label={t("loadingDataQuality")} />;
  }

  const { quality_score, summary, checks, columns } = qualityData;

  const checkCards = [
    {
      label: t("missingValues"),
      value: checks.missing_values.count,
      percentage: checks.missing_values.percentage,
      status: checks.missing_values.status,
    },
    {
      label: t("duplicateRows"),
      value: checks.duplicate_rows.count,
      percentage: checks.duplicate_rows.percentage,
      status: checks.duplicate_rows.status,
    },
    {
      label: t("invalidDates"),
      value: checks.invalid_dates.count,
      percentage: checks.invalid_dates.percentage,
      status: checks.invalid_dates.status,
    },
    {
      label: t("negativeValues"),
      value: checks.negative_values.count,
      percentage: checks.negative_values.percentage,
      status: checks.negative_values.status,
    },
  ];

  return (
    <div className="min-h-screen bg-slate-200">
      <div className="w-full px-6 py-5 fade-in space-y-5">
        <PageHeader
          title={t("dataQuality")}
          subtitle={t("dataQualityPageSubtitle")}
        />

        <div className="bg-white rounded-xl shadow-sm p-4 flex items-center justify-between">
          <span className="text-sm text-slate-500">
            {t("dataSource")}
          </span>

          <span className="px-4 py-2 rounded-full bg-blue-50 text-blue-600 text-sm font-medium">
            {datasetName}
          </span>
        </div>

        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
            <p className="text-xs text-slate-500">{t("totalRows")}</p>

            <p className="mt-1 text-xl font-semibold text-slate-800">
              {summary.rows.toLocaleString()}
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
            <p className="text-xs text-slate-500">{t("totalColumns")}</p>

            <p className="mt-1 text-xl font-semibold text-slate-800">
              {summary.columns.toLocaleString()}
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
            <p className="text-xs text-slate-500">{t("missingValues")}</p>

            <p className="mt-1 text-xl font-semibold text-slate-800">
              {summary.missing_values.toLocaleString()}
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
            <p className="text-xs text-slate-500">{t("duplicateRows")}</p>

            <p className="mt-1 text-xl font-semibold text-slate-800">
              {summary.duplicate_rows.toLocaleString()}
            </p>
          </div>
        </div>

        <ChartCard
          title={t("dataQualityScore")}
          description={t("dataQualityScoreDescription")}
        >
          <div className="flex flex-col items-center justify-center py-5">
            <div className="relative flex items-center justify-center w-28 h-28 rounded-full border-8 border-slate-100">
              <span
                className={`text-4xl font-bold ${getScoreStyle(quality_score)}`}
              >
                {quality_score}
              </span>
            </div>

            <p
              className={`mt-3 text-base font-semibold ${getScoreStyle(
                quality_score,
              )}`}
            >
              {quality_score >= 90
                ? t("excellent")
                : quality_score >= 70
                  ? t("good")
                  : t("needsReview")}
            </p>

            <p className="mt-1 text-sm text-slate-500">
              {t("outOf100")}
            </p>

            <p className="mt-3 text-sm text-slate-500">
              {quality_score >= 90
                ? t("qualityExcellentMessage")
                : quality_score >= 70
                  ? t("qualityGoodMessage")
                  : t("qualityNeedsReviewMessage")}
            </p>
          </div>
        </ChartCard>

        <ChartCard
          title={t("qualityChecks")}
          description={t("qualityChecksDescription")}
        >
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {checkCards.map((check) => (
              <div
                key={check.label}
                className="border border-slate-100 rounded-lg p-4"
              >
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-slate-700">
                    {check.label}
                  </p>

                  <span
                    className={`w-2.5 h-2.5 rounded-full ${
                      check.status === "good"
                        ? "bg-emerald-500"
                        : check.status === "warning"
                          ? "bg-amber-500"
                          : "bg-rose-500"
                    }`}
                  />
                </div>

                <p className="mt-4 text-2xl font-semibold text-slate-800">
                  {check.value.toLocaleString()}
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  {check.percentage}% {t("ofData")}
                </p>

                <p
                  className={`mt-2 text-xs font-medium ${
                    check.status === "good"
                      ? "text-emerald-600"
                      : check.status === "warning"
                        ? "text-amber-600"
                        : "text-rose-600"
                  }`}
                >
                  {getStatusText(check.status, t)}
                </p>
              </div>
            ))}
          </div>
        </ChartCard>

        <ChartCard
          title={t("columnQuality")}
          description={t("columnQualityDescription")}
        >
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-left">
                  <th className="px-3 py-3 font-medium text-slate-600">
                    {t("column")}
                  </th>

                  <th className="px-3 py-3 font-medium text-slate-600">
                    {t("type")}
                  </th>

                  <th className="px-3 py-3 font-medium text-slate-600 text-right">
                    {t("missing")}
                  </th>

                  <th className="px-3 py-3 font-medium text-slate-600 text-right">
                    {t("unique")}
                  </th>
                </tr>
              </thead>

              <tbody>
                {columns.map((column) => (
                  <tr
                    key={column.name}
                    className="border-b border-slate-100 hover:bg-slate-50"
                  >
                    <td className="px-3 py-3 text-slate-700">
                      {column.name}
                    </td>

                    <td className="px-3 py-3 text-slate-500 capitalize">
                      {column.type}
                    </td>

                    <td className="px-3 py-3 text-right text-slate-700">
                      {column.missing.toLocaleString()}
                    </td>

                    <td className="px-3 py-3 text-right text-slate-700">
                      {column.unique.toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </ChartCard>
      </div>
    </div>
  );
}

export default DataQuality;