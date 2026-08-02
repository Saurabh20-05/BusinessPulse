


function CustomTooltip({ active, payload, label }) {

    if (!active || !payload?.length) return null;


    return (
    
    <div className="rounded-xl border border-slate-200 bg-white px-4 py-3 shadow-lg">
      
      
      <p className="mb-2 text-sm font-semibold text-slate-700">
        {label}
      </p>

      
      
      {payload.map((item) => (
        
        
        <div key={item.dataKey} className="flex items-center justify-between gap-8 py-1 text-sm" >
            
            
            
            <div className="flex items-center gap-2">
                <span
                className="h-3 w-3 rounded-full"
                style={{ backgroundColor: item.color }}
                />

            
                <span className="text-slate-600">
                {item.name}
                </span>
          
            </div>



            <span className="font-semibold text-slate-900">
              {Number(item.value).toLocaleString()}
            </span>


        </div>
     
     ))}
    
    
    </div>
  );
}

export default CustomTooltip;