


from fastapi import APIRouter

from app.services import kpi_service, chart_service
from app.ml import forecast_models

router = APIRouter(
    prefix="/dashboard", 
    tags=["Dashboard"]
)




# /dashboard
@router.get("")

def get_dashboard_summary():
    
    return {
        "kpis": kpi_service.get_kpis(),
        "monthly_revenue": chart_service.monthly_revenue(),
        "revenue_forecast": forecast_models.forecast_revenue(),
    }
