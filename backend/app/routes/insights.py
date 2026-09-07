from fastapi import APIRouter, Depends

from app.services.insights_service import get_business_insights
from app.utils.auth import get_authenticated_user

router = APIRouter(
    prefix="/insights",
    tags=["Insights"],
    dependencies=[Depends(get_authenticated_user)],
)


# Return business insights for the selected dataset
@router.get("")
async def business_insights(
    dataset_id: str = "olist",
    current_user=Depends(get_authenticated_user),
):
    return await get_business_insights(
        dataset_id,
        current_user["id"],
    )
