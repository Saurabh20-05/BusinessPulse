



import {
  BarChart3,
  Activity,
  TrendingUp,
} from "lucide-react";






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
    
    
    
    <aside className="hidden lg:block w-72 shrink-0">
      
      
      
      
      <div className="sticky top-28 rounded-2xl border border-slate-200 bg-white p-5 shadow-md">
        
        
        <p className="mb-4 text-sm font-bold uppercase tracking-wide text-slate-400">
          Dashboard
        </p>



        <nav className="flex flex-col gap-3">
          {sidebarItems.map((item) => {
            const Icon = item.icon;

            
            
            return (
              
              
              
              <button
                key={item.key}
                onClick={() => onSelect(item.key)}
                className={`flex items-center gap-4 rounded-xl border-2 px-4 py-4 text-left text-base font-semibold transition-all duration-200 ${
                  activeTab === item.key
                    ? "border-primary-600 bg-primary-600 text-white shadow-md"
                    : "border-slate-300 bg-white text-slate-700 hover:bg-slate-100 hover:border-slate-400"
                }`}
              >
                <Icon size={20} />
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