from fastapi import APIRouter

from app.services import kpi_service

router = APIRouter(prefix="/current", tags=["Current Dashboard"])




@router.get("")

def get_current_dashboard():

    return {
        "kpis": kpi_service.get_kpis(),
        "recent_orders": kpi_service.get_recent_orders(),
        "top_categories": kpi_service.get_top_categories_table(),
    }
