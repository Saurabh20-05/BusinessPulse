from pydantic import BaseModel, Field


class MonthlyRevenue(BaseModel):
    month: str = Field(
        description="Month"
    )

    revenue: float = Field(
        description="Revenue in Brazilian Real"
    )


class RevenueVsOrders(BaseModel):
    month: str
    revenue: float
    orders: int