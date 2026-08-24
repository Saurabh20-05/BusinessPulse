function StatCard({ label, value, icon: Icon, accent = "primary" }) {
  const accentColors = {
    primary: "bg-primary-50 text-primary-600",
    green: "bg-emerald-50 text-emerald-600",
    amber: "bg-amber-50 text-amber-600",
    rose: "bg-rose-50 text-rose-600",
  };

  return (
    <div className="flex items-center justify-between rounded-lg border border-slate-200 bg-white p-3 shadow-card">
      <div className="min-w-0">
        <p className="text-[11px] font-medium text-slate-500">{label}</p>

        <p className="mt-0.5 text-base font-semibold text-slate-900 truncate">
          {value}
        </p>
      </div>

      {Icon && (
        <div
          className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${accentColors[accent]}`}
        >
          <Icon size={16} />
        </div>
      )}
    </div>
  );
}

export default StatCard;
