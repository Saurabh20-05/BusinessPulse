from fastapi import APIRouter, Depends

from app.services.data_quality_service import get_data_quality
from app.utils.auth import get_authenticated_user

router = APIRouter(
    prefix="/data-quality",
    tags=["Data Quality"],
    dependencies=[Depends(get_authenticated_user)],
)


# Check the selected dataset for common data quality issues
@router.get("")
async def data_quality(
    dataset_id: str = "olist",
    current_user=Depends(get_authenticated_user),
):
    return await get_data_quality(
        dataset_id,
        current_user["id"],
    )

