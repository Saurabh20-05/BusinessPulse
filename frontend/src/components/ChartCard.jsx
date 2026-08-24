function ChartCard({ title, description, children, className = "" }) {
  return (
    <div
      className={`bg-white rounded-xl border border-slate-200 p-4 shadow-md hover:shadow-xl transition-all duration-300 ${className}`}
    >
      <h3 className="text-base font-bold text-slate-900">{title}</h3>

      {description && (
        <p className="mt-1 mb-4 text-xs text-slate-500">{description}</p>
      )}

      <div className={description ? "" : "mt-4"}>{children}</div>
    </div>
  );
}

export default ChartCard;
