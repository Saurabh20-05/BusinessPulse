import { Link } from "react-router-dom";

import { BarChart3, Activity, TrendingUp } from "lucide-react";

function Home() {
  return (
    <div className="fade-in bg-slate-200">
      
      {/* Hero Section */}

      <section className="max-w-6xl mx-auto px-6 pt-14 pb-14 text-center">
        <h1 className="text-4xl sm:text-5xl font-bold text-slate-900">
          BusinessPulse
        </h1>

        <p className="mt-5 text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
          Explore a company's past performance, understand its current state,
          and predict future business trends
        </p>

        <div className="mt-7">
          <Link
            to="/dashboard"
            className="inline-block px-7 py-3 text-lg bg-primary-600 text-white rounded-xl hover:bg-primary-700 transition"
          >
            View Dashboard
          </Link>
        </div>
      </section>

      {/* Feature Cards */}

      <section className="max-w-6xl mx-auto px-6 pb-12">
        <div className="grid sm:grid-cols-3 gap-5">
          {/* Historical Analytics */}

          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-md hover:shadow-xl transition duration-300">
            <div className="w-11 h-11 rounded-lg bg-primary-50 flex items-center justify-center text-primary-600 mb-4">
              <BarChart3 size={24} />
            </div>

            <h3 className="text-lg font-bold text-slate-900">
              Historical Analytics
            </h3>

            <p className="mt-2 text-sm text-slate-600 leading-relaxed">
              View sales, orders and customer data using different charts.
            </p>
          </div>

          {/* Current Dashboard */}

          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-md hover:shadow-xl transition duration-300">
            <div className="w-11 h-11 rounded-lg bg-primary-50 flex items-center justify-center text-primary-600 mb-4">
              <Activity size={24} />
            </div>

            <h3 className="text-lg font-bold text-slate-900">
              Current Dashboard
            </h3>

            <p className="mt-2 text-sm text-slate-600 leading-relaxed">
              View important business information like revenue, customers and
              orders.
            </p>
          </div>

          {/* Forecast */}

          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-md hover:shadow-xl transition duration-300">
            <div className="w-11 h-11 rounded-lg bg-primary-50 flex items-center justify-center text-primary-600 mb-4">
              <TrendingUp size={24} />
            </div>

            <h3 className="text-lg font-bold text-slate-900">
              Forecast & Predictions
            </h3>

            <p className="mt-2 text-sm text-slate-600 leading-relaxed">
              Predict future revenue, orders and customers using machine
              learning.
            </p>
          </div>
        </div>
      </section>

      {/* About Project */}

      <section className="max-w-3xl mx-auto px-6 pb-12 text-center">
        <h2 className="text-2xl font-semibold text-slate-900">About Project</h2>

        <p className="mt-3 text-base text-slate-600 leading-relaxed">
          BusinessPulse is a business analytics dashboard developed using
          FastAPI, React, and the Olist Brazilian E-commerce dataset. It
          analyzes historical business data, visualizes key performance metrics,
          and predicts future sales trends using machine learning.
        </p>
      </section>
    </div>
  );
}

export default Home;
