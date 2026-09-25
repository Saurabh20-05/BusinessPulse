// import { Link } from "react-router-dom";
// import { useTranslation } from "react-i18next";

// import { BarChart3, Gauge, Lightbulb, TrendingUp } from "lucide-react";

// function Home() {
//   const { t } = useTranslation();
//   return (
//     <div className="fade-in bg-slate-200">
//       {/* Hero Section */}

//       <section className="max-w-6xl mx-auto px-6 pt-20 pb-16 text-center">
//         <p className="text-sm font-semibold uppercase tracking-widest text-primary-600">
//           {t("homeHeroLabel")}
//         </p>

//         <h1 className="mt-4 text-5xl sm:text-6xl font-bold tracking-tight text-slate-900">
//           {t("homeHeroTitle")}
//           <span className="block text-primary-600">
//             {t("homeHeroTitleHighlight")}
//           </span>
//         </h1>

//         <p className="mt-6 max-w-2xl mx-auto text-lg text-slate-600 leading-relaxed">
//           {t("homeHeroDescription")}
//         </p>

//         <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
//           <Link
//             to="/dashboard"
//             className="inline-block rounded-xl bg-primary-600 px-7 py-3 text-lg font-medium text-white shadow-sm transition hover:bg-primary-700"
//           >
//             {t("exploreDashboard")}
//           </Link>

//           <Link
//             to="/dataset"
//             className="inline-block rounded-xl border border-slate-300 bg-white px-7 py-3 text-lg font-medium text-slate-700 transition hover:bg-slate-50"
//           >
//             {t("uploadDataset")}
//           </Link>
//         </div>
//       </section>

//       {/* Feature Cards */}

//       <section className="max-w-6xl mx-auto px-6 pb-16">
//         <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
//           <Link
//             to="/dashboard?tab=historical"
//             className="group block rounded-2xl border border-slate-200 bg-white p-6 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl"
//           >
//             <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition group-hover:bg-primary-600 group-hover:text-white">
//               <BarChart3 size={25} />
//             </div>

//             <p className="mt-5 text-xs font-semibold uppercase tracking-wider text-primary-600">
//               {t("analyze")}
//             </p>

//             <h3 className="mt-2 text-xl font-bold text-slate-900">
//               {t("businessAnalytics")}
//             </h3>

//             <p className="mt-3 text-sm leading-6 text-slate-600">
//               {t("businessAnalyticsDescription")}
//             </p>

//             <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
//               {t("exploreAnalytics")} →
//             </p>
//           </Link>

//           <Link
//             to="/dashboard?tab=current"
//             className="group block rounded-2xl border border-slate-200 bg-white p-6 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl"
//           >
//             <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition group-hover:bg-primary-600 group-hover:text-white">
//               <Gauge size={25} />
//             </div>

//             <p className="mt-5 text-xs font-semibold uppercase tracking-wider text-primary-600">
//               {t("monitor")}
//             </p>

//             <h3 className="mt-2 text-xl font-bold text-slate-900">
//               {t("currentDashboard")}
//             </h3>

//             <p className="mt-3 text-sm leading-6 text-slate-600">
//               {t("currentDashboardDescription")}
//             </p>

//             <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
//               {t("viewDashboard")} →
//             </p>
//           </Link>

//           <Link
//             to="/insights"
//             className="group block rounded-2xl border border-slate-200 bg-white p-6 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl"
//           >
//             <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition group-hover:bg-primary-600 group-hover:text-white">
//               <Lightbulb size={25} />
//             </div>

//             <p className="mt-5 text-xs font-semibold uppercase tracking-wider text-primary-600">
//               {t("understand")}
//             </p>

//             <h3 className="mt-2 text-xl font-bold text-slate-900">
//               {t("businessInsights")}
//             </h3>

//             <p className="mt-3 text-sm leading-6 text-slate-600">
//               {t("businessInsightsDescription")}
//             </p>

//             <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
//               {t("viewInsights")} →
//             </p>
//           </Link>

//           <Link
//             to="/dashboard?tab=forecast"
//             className="group block rounded-2xl border border-slate-200 bg-white p-6 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl"
//           >
//             <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition group-hover:bg-primary-600 group-hover:text-white">
//               <TrendingUp size={25} />
//             </div>

//             <p className="mt-5 text-xs font-semibold uppercase tracking-wider text-primary-600">
//               {t("forecast")}
//             </p>

//             <h3 className="mt-2 text-xl font-bold text-slate-900">
//               {t("futurePredictions")}
//             </h3>

//             <p className="mt-3 text-sm leading-6 text-slate-600">
//               {t("futurePredictionsDescription")}
//             </p>

//             <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
//               {t("viewForecast")} →
//             </p>
//           </Link>
//         </div>
//       </section>

//       <section className="max-w-6xl mx-auto px-6 pb-16">
//         <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-md">
//           <div className="flex items-center justify-between gap-8">
//             <div>
//               <p className="text-sm font-semibold uppercase tracking-widest text-primary-600">
//                 {t("dataQuality")}
//               </p>

//               <h2 className="mt-3 text-3xl font-bold text-slate-900">
//                 {t("knowYourData")}
//               </h2>

//               <p className="mt-4 max-w-xl text-base leading-7 text-slate-600">
//                 {t("dataQualityDescription")}
//               </p>
//             </div>

//             <div className="flex justify-start md:justify-end">
//               <Link
//                 to="/data-quality"
//                 className="rounded-xl border border-slate-300 bg-white px-6 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
//               >
//                 {t("dataQualityDescription")}
//               </Link>
//             </div>
//           </div>
//         </div>
//       </section>

//       {/* About Project */}

//       <section className="max-w-5xl mx-auto px-6 pb-16 text-center">
//         <p className="text-sm font-semibold uppercase tracking-widest text-primary-600">
//           {t("onePlatform")}
//         </p>

//         <h2 className="mt-3 text-3xl font-bold text-slate-900">
//           {t("fromDataToDecisions")}
//         </h2>

//         <p className="mx-auto mt-4 max-w-3xl text-base leading-7 text-slate-600">
//           {t("aboutDescription")}
//         </p>
//       </section>

//       {/* How It Works */}

//       <section className="max-w-6xl mx-auto px-6 pb-20">
//         <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-md">
//           <div className="text-center">
//             <p className="text-sm font-semibold uppercase tracking-widest text-primary-600">
//               {t("simpleWorkflow")}
//             </p>

//             <h2 className="mt-3 text-3xl font-bold text-slate-900">
//               {t("howBusinessPulseWorks")}
//             </h2>

//             <p className="mx-auto mt-3 max-w-2xl text-sm leading-6 text-slate-600">
//               {t("workflowDescription")}
//             </p>
//           </div>

//           <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
//             <div className="text-center">
//               <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-50 text-lg font-bold text-primary-600">
//                 1
//               </div>

//               <h3 className="mt-4 font-semibold text-slate-900">
//                 {t("uploadData")}
//               </h3>

//               <p className="mt-2 text-sm leading-6 text-slate-600">
//                 {t("uploadDataDescription")}
//               </p>
//             </div>

//             <div className="text-center">
//               <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-50 text-lg font-bold text-primary-600">
//                 2
//               </div>

//               <h3 className="mt-4 font-semibold text-slate-900">
//                 {t("mapColumnsHome")}
//               </h3>

//               <p className="mt-2 text-sm leading-6 text-slate-600">
//                 {t("mapColumnsDescriptionHome")}
//               </p>
//             </div>

//             <div className="text-center">
//               <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-50 text-lg font-bold text-primary-600">
//                 3
//               </div>

//               <h3 className="mt-4 font-semibold text-slate-900">
//                 {t("checkData")}
//               </h3>

//               <p className="mt-2 text-sm leading-6 text-slate-600">
//                 {t("checkDataDescription")}
//               </p>
//             </div>

//             <div className="text-center">
//               <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-50 text-lg font-bold text-primary-600">
//                 4
//               </div>

//               <h3 className="mt-4 font-semibold text-slate-900">
//                 {t("analyzeData")}
//               </h3>

//               <p className="mt-2 text-sm leading-6 text-slate-600">
//                 {t("analyzeDataDescription")}
//               </p>
//             </div>
//           </div>
//         </div>
//       </section>

//       {/* Final Call To Action */}

//       <section className="max-w-6xl mx-auto px-6 pb-20">
//         <div className="rounded-2xl bg-primary-600 px-8 py-12 text-center shadow-lg">
//           <p className="text-sm font-semibold uppercase tracking-widest text-primary-100">
//             {t("readyToGetStarted")}
//           </p>

//           <h2 className="mt-3 text-3xl font-bold text-white">
//             {t("startExploringData")}
//           </h2>

//           <p className="mx-auto mt-4 max-w-2xl text-sm leading-6 text-primary-100">
//             {t("finalCtaDescription")}
//           </p>

//           <div className="mt-7">
//             <Link
//               to="/dataset"
//               className="inline-block rounded-xl bg-white px-6 py-3 text-sm font-semibold text-primary-700 transition hover:bg-slate-100"
//             >
//               {t("getStarted")} →
//             </Link>
//           </div>
//         </div>
//       </section>
//     </div>
//   );
// }

// export default Home;





import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";

import {
  BarChart3,
  Database,
  Gauge,
  Lightbulb,
  ShieldCheck,
  Sparkles,
  TrendingUp,
} from "lucide-react";

function Home() {
  const { t } = useTranslation();

  return (
    <div className="fade-in bg-slate-200">
      {/* Main introduction section */}
      <section className="max-w-6xl mx-auto px-6 pt-20 pb-16 text-center">
        <p className="text-sm font-semibold uppercase tracking-widest text-primary-600">
          {t("homeHeroLabel")}
        </p>

        <h1 className="mt-4 text-5xl sm:text-6xl font-bold tracking-tight text-slate-900">
          {t("homeHeroTitle")}
          <span className="block text-primary-600">
            {t("homeHeroTitleHighlight")}
          </span>
        </h1>

        <p className="mt-6 max-w-2xl mx-auto text-lg text-slate-600 leading-relaxed">
          {t("homeHeroDescription")}
        </p>

        <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
          <Link
            to="/dashboard"
            className="inline-block rounded-xl bg-primary-600 px-7 py-3 text-lg font-medium text-white shadow-sm transition hover:bg-primary-700"
          >
            {t("exploreDashboard")}
          </Link>

          <Link
            to="/dataset"
            className="inline-block rounded-xl border border-slate-300 bg-white px-7 py-3 text-lg font-medium text-slate-700 transition hover:bg-slate-50"
          >
            {t("uploadDataset")}
          </Link>
        </div>
      </section>

      {/* Main BusinessPulse feature cards */}
      <section className="max-w-6xl mx-auto px-6 pb-16">
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <Link
            to="/dashboard?tab=historical"
            className="group block rounded-2xl border border-slate-200 bg-white p-6 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition group-hover:bg-primary-600 group-hover:text-white">
              <BarChart3 size={25} />
            </div>

            <p className="mt-5 text-xs font-semibold uppercase tracking-wider text-primary-600">
              {t("analyze")}
            </p>

            <h3 className="mt-2 text-xl font-bold text-slate-900">
              {t("businessAnalytics")}
            </h3>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              {t("businessAnalyticsDescription")}
            </p>

            <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
              {t("exploreAnalytics")} →
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
              {t("monitor")}
            </p>

            <h3 className="mt-2 text-xl font-bold text-slate-900">
              {t("currentDashboard")}
            </h3>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              {t("currentDashboardDescription")}
            </p>

            <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
              {t("viewDashboard")} →
            </p>
          </Link>

          <Link
            to="/dataset"
            className="group block rounded-2xl border border-slate-200 bg-white p-6 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition group-hover:bg-primary-600 group-hover:text-white">
              <Database size={25} />
            </div>

            <p className="mt-5 text-xs font-semibold uppercase tracking-wider text-primary-600">
              {t("manage")}
            </p>

            <h3 className="mt-2 text-xl font-bold text-slate-900">
              {t("datasetManagement")}
            </h3>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              {t("datasetManagementDescription")}
            </p>

            <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
              {t("manageDatasets")} →
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
              {t("understand")}
            </p>

            <h3 className="mt-2 text-xl font-bold text-slate-900">
              {t("businessInsights")}
            </h3>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              {t("businessInsightsDescription")}
            </p>

            <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
              {t("viewInsights")} →
            </p>
          </Link>

          <Link
            to="/data-quality"
            className="group block rounded-2xl border border-slate-200 bg-white p-6 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition group-hover:bg-primary-600 group-hover:text-white">
              <ShieldCheck size={25} />
            </div>

            <p className="mt-5 text-xs font-semibold uppercase tracking-wider text-primary-600">
              {t("validate")}
            </p>

            <h3 className="mt-2 text-xl font-bold text-slate-900">
              {t("dataQuality")}
            </h3>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              {t("dataQualityDescription")}
            </p>

            <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
              {t("viewDataQuality")} →
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
              {t("forecast")}
            </p>

            <h3 className="mt-2 text-xl font-bold text-slate-900">
              {t("futurePredictions")}
            </h3>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              {t("futurePredictionsDescription")}
            </p>

            <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
              {t("viewForecast")} →
            </p>
          </Link>

          <Link
            to="/ai-analytics"
            className="group block rounded-2xl border border-slate-200 bg-white p-6 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl sm:col-span-2 lg:col-span-3"
          >
            <div className="flex flex-col items-center text-center">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition group-hover:bg-primary-600 group-hover:text-white">
                <Sparkles size={25} />
              </div>

              <p className="mt-5 text-xs font-semibold uppercase tracking-wider text-primary-600">
                {t("ask")}
              </p>

              <h3 className="mt-2 text-xl font-bold text-slate-900">
                {t("aiAnalytics")}
              </h3>

              <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">
                {t("aiAnalyticsDescription")}
              </p>

              <p className="mt-5 text-sm font-semibold text-primary-600 transition group-hover:text-primary-700">
                {t("exploreAIAnalytics")} →
              </p>
            </div>
          </Link>
        </div>
      </section>

      {/* Explain the overall BusinessPulse workflow */}
      <section className="max-w-5xl mx-auto px-6 pb-16 text-center">
        <p className="text-sm font-semibold uppercase tracking-widest text-primary-600">
          {t("onePlatform")}
        </p>

        <h2 className="mt-3 text-3xl font-bold text-slate-900">
          {t("fromDataToDecisions")}
        </h2>

        <p className="mx-auto mt-4 max-w-3xl text-base leading-7 text-slate-600">
          {t("aboutDescription")}
        </p>
      </section>

      {/* Show the main workflow from dataset preparation to AI analysis */}
      <section className="max-w-6xl mx-auto px-6 pb-20">
        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-md">
          <div className="text-center">
            <p className="text-sm font-semibold uppercase tracking-widest text-primary-600">
              {t("simpleWorkflow")}
            </p>

            <h2 className="mt-3 text-3xl font-bold text-slate-900">
              {t("howBusinessPulseWorks")}
            </h2>

            <p className="mx-auto mt-3 max-w-2xl text-sm leading-6 text-slate-600">
              {t("workflowDescription")}
            </p>
          </div>

          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-5">
            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-50 text-lg font-bold text-primary-600">
                1
              </div>

              <h3 className="mt-4 font-semibold text-slate-900">
                {t("uploadData")}
              </h3>

              <p className="mt-2 text-sm leading-6 text-slate-600">
                {t("uploadDataDescription")}
              </p>
            </div>

            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-50 text-lg font-bold text-primary-600">
                2
              </div>

              <h3 className="mt-4 font-semibold text-slate-900">
                {t("mapColumnsHome")}
              </h3>

              <p className="mt-2 text-sm leading-6 text-slate-600">
                {t("mapColumnsDescriptionHome")}
              </p>
            </div>

            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-50 text-lg font-bold text-primary-600">
                3
              </div>

              <h3 className="mt-4 font-semibold text-slate-900">
                {t("checkData")}
              </h3>

              <p className="mt-2 text-sm leading-6 text-slate-600">
                {t("checkDataDescription")}
              </p>
            </div>

            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-50 text-lg font-bold text-primary-600">
                4
              </div>

              <h3 className="mt-4 font-semibold text-slate-900">
                {t("analyzeData")}
              </h3>

              <p className="mt-2 text-sm leading-6 text-slate-600">
                {t("analyzeDataDescription")}
              </p>
            </div>

            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-50 text-lg font-bold text-primary-600">
                5
              </div>

              <h3 className="mt-4 font-semibold text-slate-900">
                {t("askYourData")}
              </h3>

              <p className="mt-2 text-sm leading-6 text-slate-600">
                {t("askYourDataDescription")}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Final entry point for users who want to start with their own data */}
      <section className="max-w-6xl mx-auto px-6 pb-20">
        <div className="rounded-2xl bg-primary-600 px-8 py-12 text-center shadow-lg">
          <p className="text-sm font-semibold uppercase tracking-widest text-primary-100">
            {t("readyToGetStarted")}
          </p>

          <h2 className="mt-3 text-3xl font-bold text-white">
            {t("startExploringData")}
          </h2>

          <p className="mx-auto mt-4 max-w-2xl text-sm leading-6 text-primary-100">
            {t("finalCtaDescription")}
          </p>

          <div className="mt-7">
            <Link
              to="/dataset"
              className="inline-block rounded-xl bg-white px-6 py-3 text-sm font-semibold text-primary-700 transition hover:bg-slate-100"
            >
              {t("getStarted")} →
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;