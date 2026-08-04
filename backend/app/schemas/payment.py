from pydantic import BaseModel


class PaymentDistribution(BaseModel):
    payment_type: str
    count: int