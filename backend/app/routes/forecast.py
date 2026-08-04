from fastapi import APIRouter

from app.services import forecast_service

from app.schemas.forecast import ForecastResponse

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"],
)


@router.get(
    "/revenue",
    response_model=ForecastResponse,
    summary="Revenue Forecast",
    description="Predicts future monthly revenue.",
    status_code=200,
    responses={
        200: {
            "description": "Revenue forecast generated successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "model_used": "Linear Regression",
                        "historical": [
                            {
                                "month": "2018-06",
                                "value": 248754.12
                            }
                        ],
                        "predicted": [
                            {
                                "month": "2018-09",
                                "value": 261438.55
                            },
                            {
                                "month": "2018-10",
                                "value": 269782.12
                            }
                        ],
                        "metrics": {
                            "mae": 10234.62,
                            "r2": 0.91
                        }
                    }
                }
            }
        }
    }
)
def get_revenue_forecast():
    return forecast_service.forecast_revenue()












@router.get(
    "/orders",
    response_model=ForecastResponse,
    summary="Orders Forecast",
    description="Predicts future monthly orders",
    responses={
        200: {
            "description": "Orders forecast generated successfully."
        },
    500:{
        "description":"Internal Server Error."
    }
    },
    status_code=200,
)
def get_orders_forecast():
    return forecast_service.forecast_orders()


@router.get(
    "/customers",
    response_model=ForecastResponse,
    summary="Customer Satisfaction Forecast",
    description="Predicts future average customer review score.",
    responses={
        200: {
            "description": "Customer forecast generated successfully."
        },
    500:{
        "description":"Internal Server Error."
    }
    },
    status_code=200,
)
def get_customer_forecast():
    return forecast_service.forecast_customers()