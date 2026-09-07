# from pydantic import BaseModel


# class KPIResponse(BaseModel):
#     total_revenue: float
#     total_orders: int
#     total_customers: int
#     total_products: int
#     avg_review_score: float
#     avg_payment_value: float
#     top_selling_category: str
#     top_seller: str
#     top_payment_method: str


from pydantic import BaseModel


class KPIResponse(BaseModel):

    total_revenue: float

    total_orders: int

    total_customers: int

    total_products: int | None

    avg_review_score: float | None

    avg_payment_value: float | None

    top_selling_category: str

    top_seller: str

    top_payment_method: str
