from pydantic import BaseModel

class HeatmapPoint(BaseModel):
    x: str
    y: str
    value: float


class HeatmapResponse(BaseModel):
    labels: list[str]
    matrix: list[HeatmapPoint]


response_model=HeatmapResponse