from pydantic import BaseModel


class ReviewDistribution(BaseModel):
    score: int
    count: int