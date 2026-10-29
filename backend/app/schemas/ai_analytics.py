# from typing import Any, Literal

# from pydantic import BaseModel, ConfigDict, Field


# class AIAnalyticsRequest(BaseModel):
#     model_config = ConfigDict(extra="forbid")

#     dataset_id: str

#     question: str = Field(
#         min_length=2,
#         max_length=1000,
#     )


# class AnalyticsFilter(BaseModel):
#     model_config = ConfigDict(extra="forbid")

#     field: str

#     operator: Literal[
#         "eq",
#         "neq",
#         "gt",
#         "gte",
#         "lt",
#         "lte",
#         "contains",
#         "in",
#     ]

#     value: Any


# class AnalyticsQuery(BaseModel):
#     model_config = ConfigDict(extra="forbid")

#     query_type: Literal[
#         "analytics",
#         "metadata",
#         "forecast",
#         "rag",
#     ]

#     operation: Literal[
#         "count",
#         "sum",
#         "average",
#         "min",
#         "max",
#         "highest_average",
#         "lowest_average",
#         "group_by",
#         "top_n",
#         "columns",
#         "row_count",
#         "column_name",
#         "column_values",
#         "cell_value",
#         "data_types",
#         "missing_values",
#         "unique_values",
#         "summary",
#         "forecast",
#         "forecast_total",
#         "forecast_average",
#         "forecast_min",
#         "forecast_max",
#         "forecast_highest_month",
#         "forecast_lowest_month",
#         "forecast_month",
#         "knowledge_search",
#     ]

#     field: str | None = None
#     group_by: str | None = None

#     filters: list[AnalyticsFilter] = Field(
#         default_factory=list,
#     )

#     limit: int | None = Field(
#         default=None,
#         ge=1,
#         le=100,
#     )

#     sort: Literal[
#         "asc",
#         "desc",
#     ] | None = None

#     visualization: Literal[
#         "text",
#         "kpi",
#         "table",
#         "chart",
#     ] = "text"

#     direct_answer: str | None = None
#     direct_result: str | None = None

#     row_number: int | None = Field(
#         default=None,
#         ge=1,
#     )

#     column_number: int | None = Field(
#         default=None,
#         ge=1,
#     )

#     prediction_type: Literal[
#         "revenue",
#         "orders",
#         "customers",
#     ] | None = None

#     horizon: int | None = Field(
#         default=None,
#         ge=1,
#         le=4,
#     )

#     forecast_offset: int | None = Field(
#         default=None,
#         ge=1,
#         le=4,
#     )

#     model_name: Literal[
#         "linear",
#         "random_forest",
#         "polynomial",
#     ] | None = None


# class AIAnalyticsResponse(BaseModel):
#     model_config = ConfigDict(extra="forbid")

#     question: str
#     query: AnalyticsQuery
#     answer: str
#     result: Any

#     visualization: Literal[
#         "text",
#         "kpi",
#         "table",
#         "chart",
#     ] = "text"

#     table_data: dict[str, Any] | None = None
#     chart_data: dict[str, Any] | None = None


from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class AIAnalyticsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dataset_id: str

    question: str = Field(
        min_length=2,
        max_length=1000,
    )


class AnalyticsFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field: str

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

    value: Any


class AnalyticsQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query_type: Literal[
        "analytics",
        "metadata",
        "forecast",
        "rag",
        "general",
    ]

    operation: Literal[
        "count",
        "sum",
        "average",
        "min",
        "max",
        "highest_average",
        "lowest_average",
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
        "knowledge_search",
        "general",
    ]

    field: str | None = None
    group_by: str | None = None

    filters: list[AnalyticsFilter] = Field(
        default_factory=list,
    )

    limit: int | None = Field(
        default=None,
        ge=1,
        le=100,
    )

    sort: (
        Literal[
            "asc",
            "desc",
        ]
        | None
    ) = None

    visualization: Literal[
        "text",
        "kpi",
        "table",
        "chart",
    ] = "text"

    direct_answer: str | None = None
    direct_result: str | None = None

    row_number: int | None = Field(
        default=None,
        ge=1,
    )

    column_number: int | None = Field(
        default=None,
        ge=1,
    )

    prediction_type: (
        Literal[
            "revenue",
            "orders",
            "customers",
        ]
        | None
    ) = None

    horizon: int | None = Field(
        default=None,
        ge=1,
        le=4,
    )

    forecast_offset: int | None = Field(
        default=None,
        ge=1,
        le=4,
    )

    model_name: (
        Literal[
            "linear",
            "random_forest",
            "polynomial",
        ]
        | None
    ) = None


class AIAnalyticsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str
    query: AnalyticsQuery
    answer: str
    result: Any

    visualization: Literal[
        "text",
        "kpi",
        "table",
        "chart",
    ] = "text"

    table_data: dict[str, Any] | None = None
    chart_data: dict[str, Any] | None = None
