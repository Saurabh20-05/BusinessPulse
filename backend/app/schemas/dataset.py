from pydantic import BaseModel, Field
from typing import Dict, List


class DatasetUploadResponse(BaseModel):
    dataset_id: str
    filename: str
    rows: int
    columns: List[str]


# Define the column mapping used to normalize an uploaded dataset
class DatasetConfigureRequest(BaseModel):
    dataset_id: str
    mapping: Dict[str, str] = Field(
        description="Mapping from normalized fields to uploaded CSV columns"
    )


class DatasetResponse(BaseModel):
    dataset_id: str
    filename: str
    rows: int
    columns: List[str]
    mapping: Dict[str, str] = {}