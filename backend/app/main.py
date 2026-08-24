from contextlib import asynccontextmanager
from textwrap import dedent

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.mongodb import client
from app.routes import historical, current, forecast, auth
from app.exceptions import register_exception_handlers


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

    BusinessPulse is a Business Analytics Dashboard developed using FastAPI, React and Machine Learning.

    ### Features

    - Historical Analytics
    - Current Business KPIs
    - Revenue Forecasting
    - Order Forecasting
    - Customer Forecasting
    - User Authentication
    - JWT Authentication
    - MongoDB User Management
    - Interactive Dashboard Support

    ### Technologies

    - FastAPI
    - Pandas
    - Scikit-Learn
    - PyMongo
    - MongoDB
    - JWT
    - React
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
