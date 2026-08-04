

import { Link } from "react-router-dom";

import { BarChart3, Activity, TrendingUp } from "lucide-react";






function Home() {


  return (
    
    
    <div className="fade-in bg-slate-200">
      
    








      <section className="max-w-7xl mx-auto px-6 pt-28 pb-28 text-center">
        
        
        <h1 className="text-6xl sm:text-7xl font-bold text-slate-900"> 
          BusinessPulse 
        </h1>

        
        <p className="mt-8 text-2xl text-slate-600 max-w-4xl mx-auto leading-relaxed">
          Explore a company's past performance, understand its current state, and predict future business trends
        </p>

        
        
        <div className="mt-12">
          
          
          <Link to="/dashboard" className="px-10 py-5 text-2xl bg-primary-600 text-white rounded-2xl hover:bg-primary-700 transition">
            View Dashboard
          </Link>
        
        
        </div>

      </section>












      <section className="max-w-7xl mx-auto px-6 pb-20">
        
        
        <div className="grid sm:grid-cols-3 gap-5">
        
        




          <div className="bg-white rounded-xl border border-slate-200 p-8 shadow-md hover:shadow-xl transition duration-300">
            
            <div className="w-14 h-14 rounded-lg bg-primary-50 flex items-center justify-center text-primary-600 mb-6"><BarChart3 size={28} /></div>

            <h3 className="text-2xl font-bold text-slate-900">
              Historical Analytics
            </h3>

            <p className="mt-3 text-lg text-slate-600 leading-relaxed"> View sales, orders and customer data using different charts.
            
            </p>
          </div>











          <div className="bg-white rounded-xl border border-slate-200 p-8 shadow-md hover:shadow-xl transition duration-300">
            
            <div className="w-14 h-14 rounded-lg bg-primary-50 flex items-center justify-center text-primary-600 mb-6"><Activity size={28} /></div>


            <h3 className="text-2xl font-bold text-slate-900">
              Current Dashboard
            </h3>


            <p className="mt-3 text-lg text-slate-600 leading-relaxed">
              View important business information like revenue, customers and
              orders.
            </p>

          </div>










          <div className="bg-white rounded-xl border border-slate-200 p-8 shadow-md hover:shadow-xl transition duration-300">
            
            <div className="w-14 h-14 rounded-lg bg-primary-50 flex items-center justify-center text-primary-600 mb-6"><TrendingUp size={28} /></div>

            <h3 className="text-2xl font-bold text-slate-900">
              Forecast & Predictions
            </h3>

            <p className="mt-3 text-lg text-slate-600 leading-relaxed">
              Predict future revenue, orders and customers using Linear
              Regression.
            </p>
          
          </div>
        
        
        </div>
      
      </section>















      <section className="max-w-4xl mx-auto px-6 pb-20 text-center">


        <h2 className="text-4xl font-semibold text-slate-900">
          About Project
        </h2>



        <p className="mt-5 text-xl text-slate-600 leading-relaxed">
          BusinessPulse is a business analytics dashboard developed using FastAPI, React, and the Olist Brazilian E-commerce dataset. It analyzes historical business data, visualizes key performance metrics, and predicts future sales trends using machine learning
        </p>

      </section>





    </div>
  );
}

export default Home;