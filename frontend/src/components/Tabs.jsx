



function Tabs({ tabs, activeTab, onSelect }) {
  
  
  
  
  
  
  return (
    
    <div className="mb-4 flex gap-2 overflow-x-auto pb-2 lg:hidden">
      
      
      {tabs.map((tabItem) => (
        
        
        
        
        
        <button
          key={tabItem.key}
          onClick={() => onSelect(tabItem.key)}
          className={`whitespace-nowrap rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
            activeTab === tabItem.key
              ? "bg-primary-600 text-white"
              : "border border-slate-200 bg-white text-slate-600"
          }`}
        >
          {tabItem.label}
        </button>
      
      
      
      ))}
    </div>
  );
}

export default Tabs;