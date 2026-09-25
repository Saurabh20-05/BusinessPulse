# from pydantic import BaseModel, Field


# class ForecastPoint(BaseModel):
#     month: str
#     value: float


# class ForecastMetrics(BaseModel):

#     mae: float = Field(description="Mean Absolute Error")

#     r2: float = Field(description="Coefficient of Determination")


# class ForecastResponse(BaseModel):
#     model_used: str
#     historical: list[ForecastPoint]
#     predicted: list[ForecastPoint]
#     metrics: ForecastMetrics


from pydantic import BaseModel, Field


class ForecastPoint(BaseModel):
    month: str
    value: float


class ForecastMetrics(BaseModel):
    mae: float = Field(
        description="Mean Absolute Error"
    )

    rmse: float = Field(
        description="Root Mean Squared Error"
    )

    r2: float = Field(
        description="Coefficient of Determination"
    )


class ForecastResponse(BaseModel):
    prediction_type: str
    model_key: str
    model_used: str

    historical: list[ForecastPoint]

    predicted: list[ForecastPoint]

    metrics: ForecastMetrics