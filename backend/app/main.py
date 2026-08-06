

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import historical, current, forecast

from app.exceptions import register_exception_handlers





app = FastAPI(
    title="BusinessPulse API",
    version="1.0.0",
    summary="Business Analytics and Forecasting API",

    description="""

    ## BusinessPulse API
    
    BusinessPulse is a Business Analytics Dashboard developed using FastAPI, React and Machine Learning.

    ### Features

    - Historical Analytics
    - Current Business KPIs
    - Revenue Forecasting
    - Order Forecasting
    - Customer Forecasting
    - Interactive Dashboard Support

    ### Technologies

    - FastAPI
    - Pandas
    - Scikit-Learn
    - React
    - Recharts
    - Olist Brazilian E-Commerce Dataset
    """,


    contact={
        "name": "Saurabh",
        "email": "saurabh200805@gmail.com",
    },


    license_info={
        "name": "MIT License",
    },

    
)
register_exception_handlers(app)









app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(historical.router)
app.include_router(current.router)
app.include_router(forecast.router)


@app.get(
    "/",
    tags=["General"],
    summary="API Information",
    description="Returns general information about the API.",
)
def root():
    return {
        "message": "BusinessPulse API is running",
        "version": "1.0.0",
        "docs": "/docs",
    }