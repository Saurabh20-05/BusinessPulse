// import { useEffect, useState } from "react";
// import { useNavigate } from "react-router-dom";

// import ChartCard from "../components/ChartCard";
// import Loader from "../components/Loader";
// import PageHeader from "../components/PageHeader";

// import { getCurrentUser, getMyDatasets } from "../services/api";

// function Profile() {
//   const navigate = useNavigate();

//   const [user, setUser] = useState(null);
//   const [datasets, setDatasets] = useState([]);
//   const [error, setError] = useState(null);

//   const selectedDataset = localStorage.getItem("selected_dataset") || "olist";

//   const selectedDatasetName =
//     selectedDataset === "olist"
//       ? "Olist Dataset"
//       : datasets.find((dataset) => dataset.dataset_id === selectedDataset)
//           ?.filename || "Custom Dataset";

//   useEffect(() => {
//     Promise.all([getCurrentUser(), getMyDatasets()])
//       .then(([userData, datasetData]) => {
//         const datasetList = Array.isArray(datasetData)
//           ? datasetData
//           : datasetData?.datasets || datasetData?.data || [];

//         setUser(userData);
//         setDatasets(datasetList);
//       })
//       .catch(() => {
//         setError("Failed to load profile information.");
//       });
//   }, []);

//   if (error) {
//     return <p className="text-sm text-rose-600">{error}</p>;
//   }

//   if (!user) {
//     return <Loader label="Loading profile..." />;
//   }

//   return (
//     <div className="min-h-screen bg-slate-200">
//       <div className="max-w-7xl mx-auto px-6 py-8 fade-in space-y-5">
//         <PageHeader
//           title="Profile"
//           subtitle="Manage your account and BusinessPulse activity."
//         />

//         <ChartCard title="Profile" description="Your BusinessPulse account.">
//           <div className="flex items-center gap-4">
//             <div className="w-14 h-14 rounded-full bg-primary-50 text-primary-700 flex items-center justify-center text-xl font-semibold">
//               {user.name?.charAt(0)?.toUpperCase() ||
//                 user.email?.charAt(0)?.toUpperCase()}
//             </div>

//             <div>
//               <h2 className="text-lg font-semibold text-slate-800">
//                 {user.name}
//               </h2>

//               <p className="text-sm text-slate-500">{user.email}</p>

//               <p className="mt-1 text-xs text-slate-400">BusinessPulse User</p>
//             </div>
//           </div>
//         </ChartCard>

//         <ChartCard
//           title="Personal Information"
//           description="Your account details."
//         >
//           <div className="grid gap-4 sm:grid-cols-2">
//             <div>
//               <p className="text-xs text-slate-500">Full Name</p>

//               <p className="mt-1 text-sm font-medium text-slate-800">
//                 {user.name}
//               </p>
//             </div>

//             <div>
//               <p className="text-xs text-slate-500">Email Address</p>

//               <p className="mt-1 text-sm font-medium text-slate-800">
//                 {user.email}
//               </p>
//             </div>

//             <div>
//               <p className="text-xs text-slate-500">Account Status</p>

//               <p className="mt-1 text-sm font-medium text-emerald-600">
//                 Active
//               </p>
//             </div>
//           </div>
//         </ChartCard>

//         <ChartCard
//           title="Your Data"
//           description="Your datasets and current data source."
//         >
//           <div className="grid gap-4 sm:grid-cols-2">
//             <div>
//               <p className="text-xs text-slate-500">Uploaded Datasets</p>

//               <p className="mt-1 text-xl font-semibold text-slate-800">
//                 {datasets.length}
//               </p>
//             </div>

//             <div>
//               <p className="text-xs text-slate-500">Current Dataset</p>

//               <p className="mt-1 text-sm font-medium text-slate-800">
//                 {selectedDatasetName}
//               </p>
//             </div>
//           </div>
//         </ChartCard>

//         <ChartCard
//           title="Quick Actions"
//           description="Jump to the parts of BusinessPulse you use most."
//         >
//           <div className="flex flex-wrap gap-3">
//             <button
//               onClick={() => navigate("/dataset")}
//               className="rounded-lg border border-slate-400 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
//             >
//               Manage Datasets
//             </button>

//             <button
//               onClick={() => navigate("/dashboard")}
//               className="rounded-lg border border-slate-400 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
//             >
//               Dashboard
//             </button>

//             <button
//               onClick={() => navigate("/insights")}
//               className="rounded-lg border border-slate-400 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
//             >
//               Insights
//             </button>
//           </div>
//         </ChartCard>
//       </div>
//     </div>
//   );
// }

// export default Profile;



import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

import ChartCard from "../components/ChartCard";
import Loader from "../components/Loader";
import PageHeader from "../components/PageHeader";

import { getCurrentUser, getMyDatasets } from "../services/api";

function Profile() {
  const navigate = useNavigate();
  const { t } = useTranslation();

  const [user, setUser] = useState(null);
  const [datasets, setDatasets] = useState([]);
  const [error, setError] = useState(null);

  const selectedDataset = localStorage.getItem("selected_dataset") || "olist";

  const selectedDatasetName =
    selectedDataset === "olist"
      ? t("olistDataset")
      : datasets.find((dataset) => dataset.dataset_id === selectedDataset)
          ?.filename || t("customDataset");

  useEffect(() => {
    Promise.all([getCurrentUser(), getMyDatasets()])
      .then(([userData, datasetData]) => {
        const datasetList = Array.isArray(datasetData)
          ? datasetData
          : datasetData?.datasets || datasetData?.data || [];

        setUser(userData);
        setDatasets(datasetList);
      })
      .catch(() => {
        setError(t("failedToLoadProfile"));
      });
  }, [t]);

  if (error) {
    return <p className="text-sm text-rose-600">{error}</p>;
  }

  if (!user) {
    return <Loader label={t("loadingProfile")} />;
  }

  return (
    <div className="min-h-screen bg-slate-200">
      <div className="max-w-7xl mx-auto px-6 py-8 fade-in space-y-5">
        <PageHeader
          title={t("profile")}
          subtitle={t("profileSubtitle")}
        />

        <ChartCard
          title={t("profile")}
          description={t("profileCardDescription")}
        >
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 rounded-full bg-primary-50 text-primary-700 flex items-center justify-center text-xl font-semibold">
              {user.name?.charAt(0)?.toUpperCase() ||
                user.email?.charAt(0)?.toUpperCase()}
            </div>

            <div>
              <h2 className="text-lg font-semibold text-slate-800">
                {user.name}
              </h2>

              <p className="text-sm text-slate-500">{user.email}</p>

              <p className="mt-1 text-xs text-slate-400">
                {t("businessPulseUser")}
              </p>
            </div>
          </div>
        </ChartCard>

        <ChartCard
          title={t("personalInformation")}
          description={t("accountDetails")}
        >
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <p className="text-xs text-slate-500">
                {t("fullName")}
              </p>

              <p className="mt-1 text-sm font-medium text-slate-800">
                {user.name}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-500">
                {t("emailAddress")}
              </p>

              <p className="mt-1 text-sm font-medium text-slate-800">
                {user.email}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-500">
                {t("accountStatus")}
              </p>

              <p className="mt-1 text-sm font-medium text-emerald-600">
                {t("active")}
              </p>
            </div>
          </div>
        </ChartCard>

        <ChartCard
          title={t("yourData")}
          description={t("yourDataDescription")}
        >
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <p className="text-xs text-slate-500">
                {t("uploadedDatasets")}
              </p>

              <p className="mt-1 text-xl font-semibold text-slate-800">
                {datasets.length}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-500">
                {t("currentDataset")}
              </p>

              <p className="mt-1 text-sm font-medium text-slate-800">
                {selectedDatasetName}
              </p>
            </div>
          </div>
        </ChartCard>

        <ChartCard
          title={t("quickActions")}
          description={t("quickActionsDescription")}
        >
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => navigate("/dataset")}
              className="rounded-lg border border-slate-400 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
            >
              {t("manageDatasets")}
            </button>

            <button
              onClick={() => navigate("/dashboard")}
              className="rounded-lg border border-slate-400 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
            >
              {t("dashboard")}
            </button>

            <button
              onClick={() => navigate("/insights")}
              className="rounded-lg border border-slate-400 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
            >
              {t("insights")}
            </button>
          </div>
        </ChartCard>
      </div>
    </div>
  );
}

export default Profile;