import { BarChart3, Activity, TrendingUp } from "lucide-react";

const sidebarItems = [
  {
    key: "historical",
    label: "Historical Analytics",
    icon: BarChart3,
  },
  {
    key: "current",
    label: "Current Dashboard",
    icon: Activity,
  },
  {
    key: "forecast",
    label: "Forecast & Predictions",
    icon: TrendingUp,
  },
];

function Sidebar({ activeTab, onSelect }) {
  return (
    <aside className="hidden lg:block w-60 shrink-0">
      <div className="sticky top-24 rounded-xl border border-slate-200 bg-white p-4 shadow-md">
        <p className="mb-3 text-xs font-bold uppercase tracking-wide text-slate-400">
          Dashboard
        </p>

        <nav className="flex flex-col gap-2">
          {sidebarItems.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.key}
                onClick={() => onSelect(item.key)}
                className={`flex items-center gap-3 rounded-lg border px-3 py-3 text-left text-sm font-semibold transition-all duration-200 ${
                  activeTab === item.key
                    ? "border-primary-600 bg-primary-600 text-white shadow-md"
                    : "border-slate-300 bg-white text-slate-700 hover:bg-slate-100 hover:border-slate-400"
                }`}
              >
                <Icon size={18} />

                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}

export default Sidebar;
