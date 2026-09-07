import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getMyDatasets } from "../services/api";

import Sidebar from "../components/Sidebar";
import Tabs from "../components/Tabs";
import PageHeader from "../components/PageHeader";

import HistoricalAnalytics from "./HistoricalAnalytics";
import CurrentDashboard from "./CurrentDashboard";
import ForecastPredictions from "./ForecastPredictions";

const dashboardTabs = [
  {
    key: "historical",
    label: "Historical Analytics",
    subtitle: "Analyze historical sales, orders, and customer trends.",
  },
  {
    key: "current",
    label: "Current Dashboard",
    subtitle: "Monitor important business KPIs in real time.",
  },
  {
    key: "forecast",
    label: "Forecast & Predictions",
    subtitle: "Predict future sales, orders, and business growth.",
  },
];

function Dashboard() {

    const [selectedDatasetName, setSelectedDatasetName] =
    useState("Olist Dataset");

      useEffect(() => {
    const loadSelectedDataset = async () => {
      const savedDataset = localStorage.getItem("selected_dataset");

      if (!savedDataset || savedDataset === "olist") {
        setSelectedDatasetName("Olist Dataset");
        return;
      }

      try {
        const response = await getMyDatasets();

        const selected = response.data.find(
          (dataset) => dataset.dataset_id === savedDataset
        );

        if (selected) {
          setSelectedDatasetName(selected.filename);
        } else {
          setSelectedDatasetName("Custom Dataset");
        }
      } catch (error) {
        console.error(
          "Failed to load selected dataset:",
          error
        );

        setSelectedDatasetName("Custom Dataset");
      }
    };

    loadSelectedDataset();
  }, []);


  const [searchParams] = useSearchParams();

  const initialTab = searchParams.get("tab");

  const [activeTab, setActiveTab] = useState(
    dashboardTabs.some((tab) => tab.key === initialTab)
      ? initialTab
      : "historical"
  );

  const currentTab = dashboardTabs.find(
    (tab) => tab.key === activeTab
  );

  return (
    <div className="bg-slate-200 min-h-screen">
      <div className="w-full px-6 py-6 flex gap-6">
        <Sidebar activeTab={activeTab} onSelect={setActiveTab} />

        <main className="flex-1 min-w-0">
          <Tabs
            tabs={dashboardTabs}
            activeTab={activeTab}
            onSelect={setActiveTab}
          />

          <PageHeader title={currentTab.label} subtitle={currentTab.subtitle} />

                    <div className="mb-5 flex items-center justify-between rounded-xl border border-slate-200 bg-white px-4 py-3 shadow-sm">
            <span className="text-sm font-medium text-slate-500">
              Data Source
            </span>

            <span className="rounded-full bg-primary-50 px-3 py-1 text-sm font-semibold text-primary-600">
              {selectedDatasetName}
            </span>
          </div>

          {/* Show only the section selected by the user */}
          {activeTab === "historical" && <HistoricalAnalytics />}

          {activeTab === "current" && <CurrentDashboard />}

          {activeTab === "forecast" && <ForecastPredictions />}
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
