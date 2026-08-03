from fastapi import APIRouter

from app.services import chart_service

router = APIRouter(
    prefix="/historical", 
    tags=["Historical Analytics"]
)



@router.get("")

def get_historical_overview():

    return {
        "monthly_revenue": chart_service.monthly_revenue(),
        "monthly_orders": chart_service.monthly_orders(),
        "revenue_by_category": chart_service.revenue_by_category(),
        "top_categories": chart_service.top_categories(),
        "payment_distribution": chart_service.payment_method_distribution(),
        "customers_by_state": chart_service.customers_by_state(),
        "review_distribution": chart_service.review_score_distribution(),
        "price_distribution": chart_service.price_distribution(),
        "revenue_vs_orders": chart_service.revenue_vs_orders(),
        "correlation_heatmap": chart_service.correlation_heatmap(),
    }
