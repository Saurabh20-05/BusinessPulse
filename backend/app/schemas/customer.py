

from pydantic import BaseModel


class CustomerByState(BaseModel):
    state: str
    customers: int