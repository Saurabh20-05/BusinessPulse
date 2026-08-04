

from fastapi import APIRouter

from app.services import chart_service

router = APIRouter(
    prefix="/charts", 
    tags=["Charts"]
)




@router.get("/revenue")

def get_revenue_chart():

    return chart_service.monthly_revenue()




@router.get("/orders")

def get_orders_chart():

    return chart_service.monthly_orders()




@router.get("/categories")

def get_categories_chart():

    return {
        "by_revenue": chart_service.revenue_by_category(),
        "top_10": chart_service.top_categories(),
    }



@router.get("/payments")

def get_payments_chart():

    return chart_service.payment_method_distribution()








@router.get("/reviews")

def get_reviews_chart():

    return chart_service.review_score_distribution()







@router.get("/heatmap")

def get_heatmap_chart():

    return chart_service.correlation_heatmap()
