import { Link } from "react-router-dom";

import {
  BarChart3,
  Gauge,
  Lightbulb,
  TrendingUp,
} from "lucide-react";

function Home() {
  return (
    <div className="fade-in bg-slate-200">
      {/* Hero Section */}

      <section className="max-w-6xl mx-auto px-6 pt-20 pb-16 text-center">
        <p className="text-sm font-semibold uppercase tracking-widest text-primary-600">
          Business Analytics Platform
        </p>

        <h1 className="mt-4 text-5xl sm:text-6xl font-bold tracking-tight text-slate-900">
          Turn Business Data Into
          <span className="block text-primary-600">Better Decisions</span>
        </h1>

        <p className="mt-6 max-w-2xl mx-auto text-lg text-slate-600 leading-relaxed">
          Analyze your business data, track performance, identify data issues,
          and uncover insights to make better decisions.
        </p>

        <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
          <Link
            to="/dashboard"
            className="inline-block rounded-xl bg-primary-600 px-7 py-3 text-lg font-medium text-white shadow-sm transition hover:bg-primary-700"
          >
            Explore Dashboard
          </Link>

          <Link
            to="/dataset"
            className="inline-block rounded-xl border border-slate-300 bg-white px-7 py-3 text-lg font-medium text-slate-700 transition hover:bg-slate-50"
          >
            Upload Dataset
          </Link>
        </div>
      </section>

      {/* Feature Cards */}

      <section className="max-w-6xl mx-auto px-6 pb-16">
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <Link
            to="/dashboard?tab=historical"
            className="group block rounded-2xl border border-slate-200 bg-white p-6 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition group-hover:bg-primary-600 group-hover:text-white">
              <BarChart3 size={25} />
            </div>

            <p className="mt-5 text-xs font-semibold uppercase tracking-wider text-primary-600">
              Analyze
            </p>

            <h3 className="mt-2 text-xl font-bold text-slate-900">
              Business Analytics
            </h3>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              Explore revenue, orders, customers, categories, payments, and
              reviews.
            </p>

            <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
              Explore Analytics →
            </p>
          </Link>

          <Link
            to="/dashboard?tab=current"
            className="group block rounded-2xl border border-slate-200 bg-white p-6 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition group-hover:bg-primary-600 group-hover:text-white">
              <Gauge size={25} />
            </div>

            <p className="mt-5 text-xs font-semibold uppercase tracking-wider text-primary-600">
              Monitor
            </p>

            <h3 className="mt-2 text-xl font-bold text-slate-900">
              Current Dashboard
            </h3>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              Track your most important business metrics in one place.
            </p>

            <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
              View Dashboard →
            </p>
          </Link>

          <Link
            to="/insights"
            className="group block rounded-2xl border border-slate-200 bg-white p-6 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition group-hover:bg-primary-600 group-hover:text-white">
              <Lightbulb size={25} />
            </div>

            <p className="mt-5 text-xs font-semibold uppercase tracking-wider text-primary-600">
              Understand
            </p>

            <h3 className="mt-2 text-xl font-bold text-slate-900">
              Business Insights
            </h3>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              Get clear insights from your data and identify important trends.
            </p>

            <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
              View Insights →
            </p>
          </Link>

          <Link
            to="/dashboard?tab=forecast"
            className="group block rounded-2xl border border-slate-200 bg-white p-6 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition group-hover:bg-primary-600 group-hover:text-white">
              <TrendingUp size={25} />
            </div>

            <p className="mt-5 text-xs font-semibold uppercase tracking-wider text-primary-600">
              Forecast
            </p>

            <h3 className="mt-2 text-xl font-bold text-slate-900">
              Future Predictions
            </h3>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              Use machine learning to estimate future business performance.
            </p>

            <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
              View Forecast →
            </p>
          </Link>
        </div>
      </section>

      <section className="max-w-6xl mx-auto px-6 pb-16">
        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-md">
          <div className="flex items-center justify-between gap-8">
            <div>
              <p className="text-sm font-semibold uppercase tracking-widest text-primary-600">
                Data Quality
              </p>

              <h2 className="mt-3 text-3xl font-bold text-slate-900">
                Know Your Data Before You Analyze It
              </h2>

              <p className="mt-4 max-w-xl text-base leading-7 text-slate-600">
                Check your dataset for missing values, duplicates, invalid
                dates, and other common data issues before relying on your
                analysis.
              </p>
            </div>

            <div className="flex justify-start md:justify-end">
              <Link
                to="/data-quality"
                className="rounded-xl border border-slate-300 bg-white px-6 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
              >
                Check Data Quality →
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* About Project */}

      <section className="max-w-5xl mx-auto px-6 pb-16 text-center">
        <p className="text-sm font-semibold uppercase tracking-widest text-primary-600">
          One Platform. Complete Insight.
        </p>

        <h2 className="mt-3 text-3xl font-bold text-slate-900">
          From Data to Decisions
        </h2>

        <p className="mx-auto mt-4 max-w-3xl text-base leading-7 text-slate-600">
          BusinessPulse brings your business data into one place so you can
          understand performance, monitor key metrics, check data quality,
          discover useful insights, and plan ahead with forecasts.
        </p>
      </section>

      {/* How It Works */}

      <section className="max-w-6xl mx-auto px-6 pb-20">
        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-md">
          <div className="text-center">
            <p className="text-sm font-semibold uppercase tracking-widest text-primary-600">
              Simple Workflow
            </p>

            <h2 className="mt-3 text-3xl font-bold text-slate-900">
              How BusinessPulse Works
            </h2>

            <p className="mx-auto mt-3 max-w-2xl text-sm leading-6 text-slate-600">
              Bring your business data into the platform and turn it into
              meaningful insights in a few simple steps.
            </p>
          </div>

          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-50 text-lg font-bold text-primary-600">
                1
              </div>

              <h3 className="mt-4 font-semibold text-slate-900">Upload Data</h3>

              <p className="mt-2 text-sm leading-6 text-slate-600">
                Upload your business or sales data as a CSV file.
              </p>
            </div>

            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-50 text-lg font-bold text-primary-600">
                2
              </div>

              <h3 className="mt-4 font-semibold text-slate-900">Map Columns</h3>

              <p className="mt-2 text-sm leading-6 text-slate-600">
                Match your dataset columns with the fields used by
                BusinessPulse.
              </p>
            </div>

            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-50 text-lg font-bold text-primary-600">
                3
              </div>

              <h3 className="mt-4 font-semibold text-slate-900">Check Data</h3>

              <p className="mt-2 text-sm leading-6 text-slate-600">
                Review missing, duplicate, and invalid values before analyzing.
              </p>
            </div>

            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-50 text-lg font-bold text-primary-600">
                4
              </div>

              <h3 className="mt-4 font-semibold text-slate-900">Analyze</h3>

              <p className="mt-2 text-sm leading-6 text-slate-600">
                Explore performance, insights, and forecasts from your data.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Final Call To Action */}

      <section className="max-w-6xl mx-auto px-6 pb-20">
        <div className="rounded-2xl bg-primary-600 px-8 py-12 text-center shadow-lg">
          <p className="text-sm font-semibold uppercase tracking-widest text-primary-100">
            Ready to Get Started?
          </p>

          <h2 className="mt-3 text-3xl font-bold text-white">
            Start Exploring Your Business Data
          </h2>

          <p className="mx-auto mt-4 max-w-2xl text-sm leading-6 text-primary-100">
            Upload your dataset and use BusinessPulse to understand performance,
            discover insights, and plan ahead.
          </p>

          <div className="mt-7">
            <Link
              to="/dataset"
              className="inline-block rounded-xl bg-white px-6 py-3 text-sm font-semibold text-primary-700 transition hover:bg-slate-100"
            >
              Get Started →
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;
