


from pydantic import BaseModel


class CategoryRevenue(BaseModel):
    category: str
    revenue: float


class TopCategory(BaseModel):
    category: str
    orders: int
    revenue: float