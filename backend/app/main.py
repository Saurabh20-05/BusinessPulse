

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.routes import dashboard, historical, current, forecast, charts



app = FastAPI(
    title="BusinessPulse API",
    description="Backend API for the BusinessPulse dashboard",
    version="1.0.0",
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(dashboard.router)
app.include_router(historical.router)
app.include_router(current.router)
app.include_router(forecast.router)
app.include_router(charts.router)




@app.get("/")

def root():

    return {
        "message": "BusinessPulse API is running",
        "version": "1.0.0",
        "docs": "/docs",
    }
