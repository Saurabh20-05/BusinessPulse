

from pydantic import BaseModel


class MonthlyOrder(BaseModel):
    month: str
    orders: int


class RecentOrder(BaseModel):
    order_id: str
    customer_state: str
    category: str
    amount: float
    status: str
    date: str