from fastapi import APIRouter

from app.services import kpi_service

from app.schemas.kpi import KPIResponse
from app.schemas.order import RecentOrder
from app.schemas.category import TopCategory

router = APIRouter(
    prefix="/current",
    tags=["Current Dashboard"],
)


@router.get(
    "/kpis",
    response_model=KPIResponse,
    summary="Business KPIs",
    description="Returns the main business performance indicators.",
    status_code=200,
    responses={
        200: {
            "description": "Business KPIs retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "total_revenue": 15932742.81,
                        "total_orders": 96461,
                        "total_customers": 93358,
                        "total_products": 32951,
                        "avg_review_score": 4.09,
                        "avg_payment_value": 154.10,
                        "top_selling_category": "Beauty & Health",
                        "top_seller": "4869f7a5dfa277a7dca6462dcf3b52b",
                        "top_payment_method": "Credit Card"
                    }
                }
            }
        }
    }
)
def get_kpis():
    return kpi_service.get_kpis()









@router.get(
    "/recent-orders",
    response_model=list[RecentOrder],
    summary="Recent Orders",
    description="Returns the latest customer orders with their details.",
    responses={
        200: {
            "description": "Recent orders retrieved successfully."
        },
    500:{
        "description":"Internal Server Error."
    }
    },
    status_code=200,
)
def get_recent_orders():
    return kpi_service.get_recent_orders()


@router.get(
    "/top-categories",
    response_model=list[TopCategory],
    summary="Top Categories",
    description="Returns the highest revenue generating product categories along with revenue and total orders.",
    responses={
        200: {
            "description": "Top categories retrieved successfully."
        },
    500:{
        "description":"Internal Server Error."
    }
    },
    status_code=200,
)
def get_top_categories():
    return kpi_service.get_top_categories_table()