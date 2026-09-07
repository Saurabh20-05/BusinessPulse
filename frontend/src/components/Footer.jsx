function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-white">
      <div className="flex items-center justify-between px-6 py-4">
        {/* Left */}
        <div>
          <p className="text-sm font-semibold text-slate-900">
            BusinessPulse
          </p>

          <p className="mt-0.5 text-xs text-slate-500">
            Business Analytics & Forecasting Platform
          </p>
        </div>

        {/* Right */}
        <div className="text-right">
          <p className="text-xs text-slate-500">
            Analyze · Monitor · Forecast
          </p>

          <p className="mt-0.5 text-xs text-slate-400">
            © {new Date().getFullYear()} BusinessPulse
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;