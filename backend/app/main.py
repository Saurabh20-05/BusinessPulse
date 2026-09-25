from contextlib import asynccontextmanager
from textwrap import dedent

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.mongodb import client
from app.routes import insights
from app.exceptions import register_exception_handlers


from app.routes import dataset, forecast, historical
from app.routes import auth, current, data_quality

from app.routes import ai_analytics


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Test MongoDB connection when the application starts
    await client.admin.command("ping")

    print("MongoDB connected successfully")

    yield

    # Close MongoDB connection when the application shuts down
    await client.close()

    print("MongoDB connection closed")


app = FastAPI(
    title="BusinessPulse API",
    version="1.0.0",
    summary="Business Analytics and Forecasting API",
    description=dedent("""
## BusinessPulse API

BusinessPulse is a business analytics and forecasting platform built with FastAPI, React, MongoDB, Pandas, and Machine Learning.

It allows authenticated users to analyze business performance, upload their own datasets, check data quality, discover business insights, and generate forecasts.

### Features

- Historical Business Analytics
- Current Business KPIs
- Revenue Analysis
- Order Analysis
- Category Performance
- Payment Distribution
- Customer Distribution
- Review Analysis
- Revenue vs Orders Analysis
- Correlation Analysis
- Revenue Forecasting
- Order Forecasting
- Customer Satisfaction Forecasting
- Custom Dataset Upload
- Dataset Column Mapping
- Dataset Management
- Data Quality Analysis
- Automated Business Insights
- User Authentication
- JWT Authentication
- MongoDB User Management

### Dataset Support

BusinessPulse supports the built-in Olist Brazilian E-Commerce Dataset and user-uploaded CSV datasets.

Uploaded datasets can be mapped to BusinessPulse standard fields before being used for analytics, data quality checks, insights, and forecasting.

### Technologies

- FastAPI
- React
- MongoDB
- PyMongo
- Pandas
- Scikit-Learn
- JWT
- Recharts
- Olist Brazilian E-Commerce Dataset
"""),
    contact={
        "name": "Saurabh",
        "email": "saurabh200805@gmail.com",
    },
    lifespan=lifespan,
)

# Register the handler for unexpected API errors
register_exception_handlers(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://business-pulse-five.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add all API routes to the main application
app.include_router(historical.router)
app.include_router(current.router)
app.include_router(forecast.router)
app.include_router(auth.router)

app.include_router(dataset.router)

app.include_router(insights.router)

app.include_router(data_quality.router)

app.include_router(ai_analytics.router)


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

