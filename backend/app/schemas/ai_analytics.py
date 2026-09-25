from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


# Defines the data required when the user sends an AI Analytics request
class AIAnalyticsRequest(BaseModel):
    # Reject any fields that are not explicitly defined in this model
    model_config = ConfigDict(extra="forbid")

    dataset_id: str

    # Limits the question length so invalid or excessively large requests are rejected
    question: str = Field(
        min_length=2,
        max_length=1000,
    )





# Defines the filtering conditions that can be applied to dataset queries
class AnalyticsFilter(BaseModel):
    # Reject unexpected fields in filter objects
    model_config = ConfigDict(extra="forbid")

    # Name of the dataset column on which the filter is applied
    field: str

    # Supported comparison operations for filtering dataset values
    operator: Literal[
        "eq",
        "neq",
        "gt",
        "gte",
        "lt",
        "lte",
        "contains",
        "in",
    ]

    # Value used by the selected filter operation
    value: Any





# Defines the structured query generated from the user's natural language question
class AnalyticsQuery(BaseModel):
    # Reject fields that are not part of the defined query structure
    model_config = ConfigDict(extra="forbid")

    # Identifies whether the query is for historical analytics, metadata, or forecasting
    query_type: Literal[
        "analytics",
        "metadata",
        "forecast",
    ]

    # Defines the exact operation that the backend should perform
    operation: Literal[
        "count",
        "sum",
        "average",
        "min",
        "max",
        "group_by",
        "top_n",
        "columns",
        "row_count",
        "column_name",
        "column_values",
        "cell_value",
        "data_types",
        "missing_values",
        "unique_values",
        "summary",
        "forecast",
        "forecast_total",
        "forecast_average",
        "forecast_min",
        "forecast_max",
        "forecast_highest_month",
        "forecast_lowest_month",
        "forecast_month",
    ]

    # Column used for operations such as sum, average, minimum, or maximum
    field: str | None = None

    # Column used when the result needs to be grouped by a specific field
    group_by: str | None = None

    # List of conditions that must be applied before calculating the result
    filters: list[AnalyticsFilter] = Field(
        default_factory=list,
    )

    # Maximum number of records or groups to return
    limit: int | None = Field(
        default=None,
        ge=1,
        le=100,
    )

    # Controls the sorting direction when the operation supports sorting
    sort: (
        Literal[
            "asc",
            "desc",
        ]
        | None
    ) = None

    # Tells the frontend how the result should be displayed
    visualization: Literal[
        "text",
        "kpi",
        "table",
        "chart",
    ] = "text"

    # Optional answer that can be returned directly for suitable queries
    direct_answer: str | None = None

    # Optional direct result value associated with the query
    direct_result: str | None = None

    # One based row number used for retrieving a specific cell value
    row_number: int | None = Field(
        default=None,
        ge=1,
    )

    # One based column number used for retrieving a specific cell value
    column_number: int | None = Field(
        default=None,
        ge=1,
    )






    # Defines which business metric should be forecast
    prediction_type: (
        Literal[
            "revenue",
            "orders",
            "customers",
        ]
        | None
    ) = None

    # Number of upcoming forecast points requested by the user
    horizon: int | None = Field(
        default=None,
        ge=1,
        le=4,
    )

    # Identifies a specific forecast point when the user asks for a value
    # a certain number of months after the last available month
    forecast_offset: int | None = Field(
        default=None,
        ge=1,
        le=4,
    )






    # Selects the machine learning model used for forecasting
    model_name: (
        Literal[
            "linear",
            "random_forest",
            "polynomial",
        ]
        | None
    ) = None


# Defines the complete response returned by the AI Analytics API
class AIAnalyticsResponse(BaseModel):
    # Reject unexpected fields in the API response
    model_config = ConfigDict(extra="forbid")

    # Original question submitted by the user
    question: str

    # Structured query generated from the user's question
    query: AnalyticsQuery

    # Natural language explanation generated from the calculated result
    answer: str

    # Actual result calculated by the backend
    result: Any

    # Visualization type used by the frontend to display the result
    visualization: str
