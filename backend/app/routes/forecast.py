from fastapi import APIRouter

from app.ml import forecast_models

router = APIRouter(
    prefix="/forecast", 
    tags=["Forecast"]
)




@router.get("")

def get_forecast_overview():

    return {
        "revenue": forecast_models.forecast_revenue(),
        "orders": forecast_models.forecast_orders(),
        "customers": forecast_models.forecast_customers(),
    }




@router.get("/revenue")

def get_revenue_forecast():

    return forecast_models.forecast_revenue()






@router.get("/orders")

def get_orders_forecast():

    return forecast_models.forecast_orders()








@router.get("/customers")

def get_customer_forecast():

    return forecast_models.forecast_customers()
