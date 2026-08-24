function PageHeader({ title, subtitle }) {
  return (
    <div className="mb-5">
      <h1 className="text-3xl font-bold text-slate-900">{title}</h1>

      {subtitle && <p className="mt-1 text-base text-slate-600">{subtitle}</p>}
    </div>
  );
}

export default PageHeader;
