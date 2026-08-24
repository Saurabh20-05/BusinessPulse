import { useState } from "react";

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
  const [activeTab, setActiveTab] = useState("historical");

  const currentTab = dashboardTabs.find((tab) => tab.key === activeTab);

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
