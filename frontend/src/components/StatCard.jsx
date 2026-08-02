function StatCard({
  label,
  value,
  icon: Icon,
  accent = "primary",
}) {
  const accentColors = {
    primary: "bg-primary-50 text-primary-600",
    green: "bg-emerald-50 text-emerald-600",
    amber: "bg-amber-50 text-amber-600",
    rose: "bg-rose-50 text-rose-600",
  };




  return (
    
    
    <div className="flex items-center justify-between rounded-xl border border-slate-200 bg-white p-5 shadow-card">
      
      
      <div>
        
        
        <p className="text-xs font-medium text-slate-500">
          {label}
        </p>

        
        <p className="mt-1.5 text-xl font-semibold text-slate-900">
          {value}
        </p>
      
      
      </div>

      
      
      
      {Icon && (
        
        <div
          className={`flex h-10 w-10 items-center justify-center rounded-lg ${accentColors[accent]}`}
        >
          <Icon size={19} />
        </div>
      
      )}
    
    
    </div>
  );
}

export default StatCard;