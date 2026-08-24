from pydantic import BaseModel


class PriceDistribution(BaseModel):
    range: str
    count: int


response_model = list[PriceDistribution]
