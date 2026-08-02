

function PageHeader({ title, subtitle }) {
  
  return (
    
    
    <div className="mb-8">
      
      
      <h1 className="text-4xl font-bold text-slate-900">
        {title}
      </h1>

      {subtitle && (
        <p className="mt-2 text-lg text-slate-600">
          {subtitle}
        </p>
      )}
    
    
    </div>
  

  );
}

export default PageHeader;