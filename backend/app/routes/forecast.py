from fastapi import APIRouter, Depends, HTTPException

from app.services import forecast_service

from app.schemas.forecast import ForecastResponse

from app.utils.auth import get_authenticated_user

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"],
    dependencies=[Depends(get_authenticated_user)],
)


# Generate a forecast for future monthly revenue
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
                        "historical": [{"month": "2018-06", "value": 248754.12}],
                        "predicted": [
                            {"month": "2018-09", "value": 261438.55},
                            {"month": "2018-10", "value": 269782.12},
                        ],
                        "metrics": {"mae": 10234.62, "r2": 0.91},
                    }
                }
            },
        }
    },
)
async def get_revenue_forecast(
    dataset_id: str = "olist",
    current_user: dict = Depends(get_authenticated_user),
):
    try:
        return await forecast_service.forecast_revenue(
            dataset_id,
            current_user["id"],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# Generate a forecast for future monthly orders
@router.get(
    "/orders",
    response_model=ForecastResponse,
    summary="Orders Forecast",
    description="Predicts future monthly orders",
    responses={
        200: {"description": "Orders forecast generated successfully."},
        500: {"description": "Internal Server Error."},
    },
    status_code=200,
)
async def get_orders_forecast(
    dataset_id: str = "olist",
    current_user: dict = Depends(get_authenticated_user),
):
    try:
        return await forecast_service.forecast_orders(
            dataset_id,
            current_user["id"],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# Generate a forecast for future average customer satisfaction
@router.get(
    "/customers",
    response_model=ForecastResponse,
    summary="Customer Satisfaction Forecast",
    description="Predicts future average customer review score.",
    responses={
        200: {"description": "Customer forecast generated successfully."},
        500: {"description": "Internal Server Error."},
    },
    status_code=200,
)
async def get_customer_forecast(
    dataset_id: str = "olist",
    current_user: dict = Depends(get_authenticated_user),
):

    try:

        return await forecast_service.forecast_customers(
            dataset_id,
            current_user["id"],
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
