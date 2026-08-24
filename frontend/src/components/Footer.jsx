function Footer() {
  return (
    <footer className="border-t border-blue-200 bg-white">
      <div className="flex items-center justify-between px-8 py-5">
        <span className="text-base font-semibold">
          BusinessPulse &copy; {new Date().getFullYear()}
        </span>

        <p className="text-sm text-slate-400">
          Business Analytics Dashboard using the Olist Brazilian E-commerce
          Dataset
        </p>
      </div>
    </footer>
  );
}

export default Footer;
