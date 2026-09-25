import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getMyDatasets } from "../services/api";
import { useTranslation } from "react-i18next";

import Sidebar from "../components/Sidebar";
import Tabs from "../components/Tabs";
import PageHeader from "../components/PageHeader";

import HistoricalAnalytics from "./HistoricalAnalytics";
import CurrentDashboard from "./CurrentDashboard";
import ForecastPredictions from "./ForecastPredictions";

function Dashboard() {
  const { t } = useTranslation();

  const dashboardTabs = [
    {
      key: "historical",
      label: t("historicalAnalytics"),
      subtitle: t("historicalAnalyticsSubtitle"),
    },
    {
      key: "current",
      label: t("currentDashboard"),
      subtitle: t("currentDashboardSubtitle"),
    },
    {
      key: "forecast",
      label: t("forecastPredictions"),
      subtitle: t("forecastPredictionsSubtitle"),
    },
  ];

  const [selectedDatasetName, setSelectedDatasetName] =
    useState(t("olistDataset"));

  useEffect(() => {
    const loadSelectedDataset = async () => {
      const savedDataset = localStorage.getItem("selected_dataset");

      if (!savedDataset || savedDataset === "olist") {
        setSelectedDatasetName(t("olistDataset"));
        return;
      }

      try {
        const response = await getMyDatasets();

        const selected = response.data.find(
          (dataset) => dataset.dataset_id === savedDataset,
        );

        if (selected) {
          setSelectedDatasetName(selected.filename);
        } else {
          setSelectedDatasetName(t("customDataset"));
        }
      } catch (error) {
        console.error("Failed to load selected dataset:", error);

        setSelectedDatasetName(t("customDataset"));
      }
    };

    loadSelectedDataset();
  }, [t]);

  const [searchParams] = useSearchParams();

  const initialTab = searchParams.get("tab");

  const [activeTab, setActiveTab] = useState(
    dashboardTabs.some((tab) => tab.key === initialTab)
      ? initialTab
      : "historical",
  );

  const currentTab = dashboardTabs.find(
    (tab) => tab.key === activeTab,
  );

  return (
    <div className="min-h-screen bg-slate-200">
      <div className="flex w-full gap-6 px-6 py-6">
        <Sidebar
          activeTab={activeTab}
          onSelect={setActiveTab}
        />

        <main className="min-w-0 flex-1">
          <Tabs
            tabs={dashboardTabs}
            activeTab={activeTab}
            onSelect={setActiveTab}
          />

          <PageHeader
            title={currentTab.label}
            subtitle={currentTab.subtitle}
          />

          <div className="mb-5 flex items-center justify-between rounded-xl border border-slate-200 bg-white px-4 py-3 shadow-sm">
            <span className="text-sm font-medium text-slate-500">
              {t("dataSource")}
            </span>

            <span className="rounded-full bg-primary-50 px-3 py-1 text-sm font-semibold text-primary-600">
              {selectedDatasetName}
            </span>
          </div>

          {/* Show only the section selected by the user */}
          {activeTab === "historical" && (
            <HistoricalAnalytics />
          )}

          {activeTab === "current" && (
            <CurrentDashboard />
          )}

          {activeTab === "forecast" && (
            <ForecastPredictions />
          )}
        </main>
      </div>
    </div>
  );
}

export default Dashboard;