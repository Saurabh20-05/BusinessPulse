function Tabs({ tabs, activeTab, onSelect }) {
  return (
    <div className="mb-3 flex gap-2 overflow-x-auto pb-1 lg:hidden">
      {tabs.map((tabItem) => (
        <button
          key={tabItem.key}
          onClick={() => onSelect(tabItem.key)}
          className={`whitespace-nowrap rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
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
