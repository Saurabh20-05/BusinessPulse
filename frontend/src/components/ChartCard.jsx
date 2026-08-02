function ChartCard({
  title,
  description,
  children,
  className = "",
}) {
 
 
  return (
    
    
    <div className={`bg-white rounded-2xl border border-slate-200 p-6 shadow-md hover:shadow-xl transition-all duration-300 ${className}`}>
      
      
      <h3 className="text-lg font-bold text-slate-900">
        {title}
      </h3>




      {description && (
        <p className="mt-1 mb-5 text-sm text-slate-500">
          {description}
        </p>
      )}



      <div className={description ? "" : "mt-5"}>
        {children}
      </div>
 
 
    </div>
 
);
}

export default ChartCard;