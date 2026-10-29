import time

import pandas as pd


from app.schemas.ai_analytics import AnalyticsQuery

from app.services.llm_service import AIAgentPlan

from app.services.forecast_service import forecast

from app.services.retrieval_service import (
    retrieve_relevant_chunks,
)

# Default forecasting model used for each supported business metric

DEFAULT_FORECAST_MODELS = {
    "revenue": "linear",
    "orders": "random_forest",
    "customers": "polynomial",
}


# Apply all filters generated for the current analytics query


def _apply_filters(
    df: pd.DataFrame,
    filters,
) -> pd.DataFrame:

    filtered_df = df.copy()

    for item in filters:

        field = item.field

        operator = item.operator

        value = item.value

        # Make sure the requested filter column exists before applying the condition

        if field not in filtered_df.columns:

            raise ValueError(
                f"Column '{field}' does not exist in the selected dataset."
            )

        series = filtered_df[field]

        # Keep rows where the column value is equal to the requested value

        if operator == "eq":

            filtered_df = filtered_df[series == value]

        # Keep rows where the column value is different from the requested value

        elif operator == "neq":

            filtered_df = filtered_df[series != value]

        # Keep rows where the column value is greater than the requested value

        elif operator == "gt":

            filtered_df = filtered_df[series > value]

        # Keep rows where the column value is greater than or equal to the requested value

        elif operator == "gte":

            filtered_df = filtered_df[series >= value]

        # Keep rows where the column value is less than the requested value

        elif operator == "lt":

            filtered_df = filtered_df[series < value]

        # Keep rows where the column value is less than or equal to the requested value

        elif operator == "lte":

            filtered_df = filtered_df[series <= value]

        # Perform a case insensitive text search while safely handling missing values

        elif operator == "contains":

            filtered_df = filtered_df[
                series.astype(str).str.contains(
                    str(value),
                    case=False,
                    na=False,
                )
            ]

        # Keep rows where the column value exists in the provided list

        elif operator == "in":

            if not isinstance(value, list):

                raise ValueError("The 'in' filter requires a list of values.")

            filtered_df = filtered_df[series.isin(value)]

    return filtered_df


# Check that a requested column exists and contains numeric values


def _validate_numeric_field(
    df: pd.DataFrame,
    field: str,
):

    # Stop the operation if the requested column does not exist

    if field not in df.columns:

        raise ValueError(f"Column '{field}' does not exist in the selected dataset.")

    # Operations such as sum and average require numeric data

    if not pd.api.types.is_numeric_dtype(df[field]):

        raise ValueError(f"Column '{field}' must be numeric for this operation.")


def _normalize_group_values(
    df: pd.DataFrame,
    field: str,
) -> pd.DataFrame:

    result = df.copy()

    if not pd.api.types.is_string_dtype(result[field]):

        return result

    result["_normalized_group"] = (
        result[field]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace("&", "and", regex=False)
        .str.replace(r"\s+", " ", regex=True)
    )

    labels = (
        result[result["_normalized_group"] != ""]
        .groupby("_normalized_group")[field]
        .agg(lambda values: values.value_counts().index[0])
        .to_dict()
    )

    result[field] = result["_normalized_group"].map(labels).fillna(result[field])

    result.drop(
        columns=["_normalized_group"],
        inplace=True,
    )

    return result


# Convert Pandas and NumPy values into types that can be returned as JSON


def _make_json_safe(value):

    # Recursively convert values inside dictionaries

    if isinstance(value, dict):

        return {str(key): _make_json_safe(item) for key, item in value.items()}

    # Recursively convert values inside lists

    if isinstance(value, list):

        return [_make_json_safe(item) for item in value]

    # Convert NumPy scalar values into normal Python values

    if hasattr(value, "item"):

        return value.item()

    # Convert dates and timestamps into ISO formatted strings

    if hasattr(value, "isoformat"):

        return value.isoformat()

    return value


# Build the structured display data used by the frontend


def _build_display_data(
    query: AnalyticsQuery,
    data,
):

    safe_data = _make_json_safe(data)

    response = {
        "type": query.visualization,
        "data": safe_data,
        "table_data": None,
        "chart_data": None,
    }

    # Build table data when the result contains rows or key value pairs

    if query.visualization == "table":

        if isinstance(safe_data, list) and safe_data:

            if all(isinstance(item, dict) for item in safe_data):

                response["table_data"] = {
                    "columns": list(safe_data[0].keys()),
                    "rows": safe_data,
                }

        elif isinstance(safe_data, dict):

            rows = [
                {
                    "key": key,
                    "value": value,
                }
                for key, value in safe_data.items()
            ]

            response["table_data"] = {
                "columns": [
                    "key",
                    "value",
                ],
                "rows": rows,
            }

    # Build chart data for grouped results and forecast series

    if query.visualization == "chart":

        if isinstance(safe_data, list) and safe_data:

            if all(isinstance(item, dict) for item in safe_data):

                numeric_fields = [
                    key
                    for key in safe_data[0].keys()
                    if any(
                        isinstance(
                            item.get(key),
                            (int, float),
                        )
                        and not isinstance(
                            item.get(key),
                            bool,
                        )
                        for item in safe_data
                    )
                ]

                x_field = query.group_by

                if x_field and x_field in safe_data[0] and numeric_fields:

                    y_field = (
                        query.field
                        if query.field in numeric_fields
                        else numeric_fields[0]
                    )

                    response["chart_data"] = {
                        "chart_type": "bar",
                        "x_key": x_field,
                        "series": [
                            {
                                "data_key": y_field,
                                "label": y_field,
                            }
                        ],
                        "data": safe_data,
                    }

        elif isinstance(safe_data, dict):

            predicted = safe_data.get("predicted")

            # Forecast series use the month as the x axis and value as the y axis

            if (
                isinstance(predicted, list)
                and predicted
                and all(isinstance(item, dict) for item in predicted)
                and all("month" in item and "value" in item for item in predicted)
            ):

                response["chart_data"] = {
                    "chart_type": "line",
                    "x_key": "month",
                    "series": [
                        {
                            "data_key": "value",
                            "label": "Forecast",
                        }
                    ],
                    "data": predicted,
                }

    return response


# Handle queries that ask about dataset structure and metadata


def _execute_metadata_query(
    df: pd.DataFrame,
    query: AnalyticsQuery,
):

    operation = query.operation

    # Return every column with its position, name, and data type

    if operation == "columns":

        result = [
            {
                "position": index,
                "name": column,
                "dtype": str(df[column].dtype),
            }
            for index, column in enumerate(
                df.columns,
                start=1,
            )
        ]

        return {
            "type": query.visualization,
            "data": result,
        }

    # Return the total number of rows in the dataset

    if operation == "row_count":

        return {
            "type": query.visualization,
            "data": int(len(df)),
        }

    # Return information about a specific column using its one based position

    if operation == "column_name":

        if query.column_number is None:

            raise ValueError("'column_name' requires a column number.")

        if query.column_number < 1:

            raise ValueError("Column number must be at least 1.")

        if query.column_number > len(df.columns):

            raise ValueError(
                f"Column {query.column_number} does not exist. "
                f"The dataset has {len(df.columns)} columns."
            )

        column_name = df.columns[query.column_number - 1]

        return {
            "type": query.visualization,
            "data": {
                "position": query.column_number,
                "name": column_name,
                "dtype": str(df[column_name].dtype),
            },
        }

    # Return the values stored in a specific column

    if operation == "column_values":

        if query.column_number is None:

            raise ValueError("'column_values' requires a column number.")

        if query.column_number < 1:

            raise ValueError("Column number must be at least 1.")

        if query.column_number > len(df.columns):

            raise ValueError(
                f"Column {query.column_number} does not exist. "
                f"The dataset has {len(df.columns)} columns."
            )

        column_name = df.columns[query.column_number - 1]

        values = df[column_name].tolist()

        # Apply the requested limit after retrieving the column values

        if query.limit:

            values = values[: query.limit]

        return {
            "type": query.visualization,
            "data": {
                "column_number": query.column_number,
                "column_name": column_name,
                "values": _make_json_safe(values),
            },
        }

    # Return a specific value using one based row and column numbers

    if operation == "cell_value":

        if query.row_number is None:

            raise ValueError("'cell_value' requires a row number.")

        if query.column_number is None:

            raise ValueError("'cell_value' requires a column number.")

        if query.row_number < 1:

            raise ValueError("Row number must be at least 1.")

        if query.column_number < 1:

            raise ValueError("Column number must be at least 1.")

        if query.row_number > len(df):

            raise ValueError(
                f"Row {query.row_number} does not exist. "
                f"The dataset has {len(df)} rows."
            )

        if query.column_number > len(df.columns):

            raise ValueError(
                f"Column {query.column_number} does not exist. "
                f"The dataset has {len(df.columns)} columns."
            )

        # Convert the one based column number into a zero based DataFrame index

        column_name = df.columns[query.column_number - 1]

        # Convert the one based row and column numbers into zero based indexes

        value = df.iloc[
            query.row_number - 1,
            query.column_number - 1,
        ]

        return {
            "type": query.visualization,
            "data": {
                "row_number": query.row_number,
                "column_number": query.column_number,
                "column_name": column_name,
                "value": _make_json_safe(value),
            },
        }

    # Return the Pandas data type of every column

    if operation == "data_types":

        result = {column: str(dtype) for column, dtype in df.dtypes.items()}

        return {
            "type": query.visualization,
            "data": result,
        }

    # Count missing values separately for every column

    if operation == "missing_values":

        result = df.isna().sum().to_dict()

        result = {column: int(value) for column, value in result.items()}

        return {
            "type": query.visualization,
            "data": result,
        }

    # Return distinct non empty values from a selected column

    if operation == "unique_values":

        if not query.field:

            raise ValueError("'unique_values' requires a field.")

        if query.field not in df.columns:

            raise ValueError(f"Column '{query.field}' does not exist.")

        values = df[query.field].dropna().drop_duplicates().tolist()

        # Limit the number of unique values returned when requested

        if query.limit:

            values = values[: query.limit]

        return {
            "type": query.visualization,
            "data": {
                "field": query.field,
                "values": _make_json_safe(values),
            },
        }

    # Return a compact overview of the dataset

    if operation == "summary":

        result = {
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "missing_values": int(df.isna().sum().sum()),
        }

        return {
            "type": query.visualization,
            "data": result,
        }

    # Reject metadata operations that are not supported by the backend

    raise ValueError(f"Unsupported metadata operation: {operation}")


# Execute forecasting requests using the selected dataset and forecasting model


async def _execute_forecast_query(
    query: AnalyticsQuery,
    dataset_id: str,
    user_id: str,
):

    operation = query.operation

    # Use four forecast points by default when the user does not specify a horizon

    horizon = query.horizon or 4

    forecast_offset = query.forecast_offset

    # Keep the forecast range within the supported limit

    if horizon < 1:

        raise ValueError("Forecast horizon must be at least 1 month.")

    if horizon > 4:

        raise ValueError("Forecast horizon cannot exceed 4 months.")

    # Validate the requested position when the user asks for a specific future month

    if forecast_offset is not None:

        if forecast_offset < 1:

            raise ValueError("Forecast offset must be at least 1 month.")

        if forecast_offset > 4:

            raise ValueError("Forecast offset cannot exceed 4 months.")

    # Return the calendar month for a specific forecast position

    if operation == "forecast_month":

        result = await forecast(
            prediction_type=(query.prediction_type or "revenue"),
            model_name=(
                query.model_name
                or DEFAULT_FORECAST_MODELS[query.prediction_type or "revenue"]
            ),
            dataset_id=dataset_id,
            user_id=user_id,
        )

        predicted = result.get(
            "predicted",
            [],
        )

        if not predicted:

            raise ValueError("No forecast values were generated.")

        # Convert the requested one based forecast position into a zero based list index

        selected_index = (
            forecast_offset - 1 if forecast_offset is not None else horizon - 1
        )

        if selected_index >= len(predicted):

            raise ValueError(
                f"The requested forecast month "
                f"({selected_index + 1}) is not available."
            )

        selected_point = predicted[selected_index]

        month = selected_point.get("month")

        if not month:

            raise ValueError("The forecast result does not contain a month.")

        return {
            "type": query.visualization,
            "data": {
                "month": month,
                "forecast_offset": (selected_index + 1),
            },
        }

    # Forecast queries must specify which business metric should be predicted

    if not query.prediction_type:

        raise ValueError("Forecast queries require a prediction type.")

    prediction_type = query.prediction_type

    # Make sure the requested metric has a supported default forecasting model

    if prediction_type not in DEFAULT_FORECAST_MODELS:

        raise ValueError(f"Unsupported prediction type: " f"{prediction_type}")

    # Use the model selected by the query or fall back to the default model for that metric

    model_name = query.model_name or DEFAULT_FORECAST_MODELS[prediction_type]

    # Run the forecasting model using the selected dataset and authenticated user

    result = await forecast(
        prediction_type=prediction_type,
        model_name=model_name,
        dataset_id=dataset_id,
        user_id=user_id,
    )

    predicted = result.get(
        "predicted",
        [],
    )

    if not predicted:

        raise ValueError("No forecast values were generated.")

    # Return only the requested forecast point when a specific offset is provided

    if forecast_offset is not None:

        selected_index = forecast_offset - 1

        if selected_index >= len(predicted):

            raise ValueError(
                f"The requested forecast month "
                f"({forecast_offset}) is not available."
            )

        selected_point = predicted[selected_index]

        if operation == "forecast":

            return {
                "type": query.visualization,
                "data": {
                    "prediction_type": prediction_type,
                    "model_used": result.get("model_used"),
                    "forecast_offset": forecast_offset,
                    "predicted": [_make_json_safe(selected_point)],
                },
            }

    # Keep only the number of forecast points requested by the user

    predicted = predicted[:horizon]

    # Return the complete forecast series

    if operation == "forecast":

        return {
            "type": query.visualization,
            "data": {
                "prediction_type": prediction_type,
                "model_used": result.get("model_used"),
                "predicted": _make_json_safe(predicted),
            },
        }

    # Calculate the combined value across the requested forecast horizon

    if operation == "forecast_total":

        values = [
            float(point["value"])
            for point in predicted
            if point.get("value") is not None
        ]

        if not values:

            raise ValueError("Forecast did not contain numeric values.")

        return {
            "type": query.visualization,
            "data": {
                "prediction_type": prediction_type,
                "horizon": horizon,
                "total": sum(values),
                "predicted": _make_json_safe(predicted),
            },
        }

    # Calculate the average forecast value across the requested horizon

    if operation == "forecast_average":

        values = [
            float(point["value"])
            for point in predicted
            if point.get("value") is not None
        ]

        if not values:

            raise ValueError("Forecast did not contain numeric values.")

        return {
            "type": query.visualization,
            "data": {
                "prediction_type": prediction_type,
                "horizon": horizon,
                "average": sum(values) / len(values),
                "predicted": _make_json_safe(predicted),
            },
        }

    # Find the lowest, highest, earliest minimum, or latest maximum forecast point

    if operation in {
        "forecast_min",
        "forecast_max",
        "forecast_highest_month",
        "forecast_lowest_month",
    }:

        valid_points = [point for point in predicted if point.get("value") is not None]

        if not valid_points:

            raise ValueError("Forecast did not contain numeric values.")

        # Select the point with the smallest value for minimum related operations

        if operation in {
            "forecast_min",
            "forecast_lowest_month",
        }:

            selected_point = min(
                valid_points,
                key=lambda point: float(point["value"]),
            )

        # Select the point with the largest value for maximum related operations

        else:

            selected_point = max(
                valid_points,
                key=lambda point: float(point["value"]),
            )

        return {
            "type": query.visualization,
            "data": {
                "prediction_type": prediction_type,
                "month": selected_point.get("month"),
                "value": selected_point.get("value"),
                "predicted": _make_json_safe(predicted),
            },
        }

    # Reject forecast operations that are not supported by the backend

    raise ValueError(f"Unsupported forecast operation: " f"{operation}")


# Run the tool selected by the AI Agent

# Run the tool selected by the AI Agent


async def execute_agent_plan(
    df: pd.DataFrame,
    plan: AIAgentPlan,
    dataset_id: str = "olist",
    user_id: str | None = None,
    question: str | None = None,
):

    # Make sure the agent selected a tool that matches the query it generated

    expected_query_types = {
        "metadata_tool": "metadata",
        "analytics_tool": "analytics",
        "forecast_tool": "forecast",
        "rag_tool": "rag",
        "general_tool": "general",
    }

    expected_query_type = expected_query_types.get(plan.tool)

    if expected_query_type is None:

        raise ValueError(f"Unsupported AI Agent tool: {plan.tool}")

    if plan.query.query_type != expected_query_type:

        raise ValueError(
            f"AI Agent selected '{plan.tool}' but generated a "
            f"'{plan.query.query_type}' query."
        )

    # General questions do not use the dataset executor.
    # They are answered later by generate_final_answer().
    if plan.tool == "general_tool":
        return {
            "type": plan.query.visualization,
            "data": {
                "question": question,
            },
            "table_data": None,
            "chart_data": None,
        }

    # RAG questions are answered using the uploaded PDF knowledge base

    if plan.tool == "rag_tool":

        if not user_id:

            raise ValueError("Authenticated user is required for knowledge retrieval.")

        if not question:

            raise ValueError(
                "The original question is required for knowledge retrieval."
            )

        # Search only the knowledge documents belonging to this user and dataset

        rag_start = time.perf_counter()

        chunks = await retrieve_relevant_chunks(
            question=question,
            dataset_id=dataset_id,
            user_id=user_id,
        )

        print(f"[AI TIMING] RAG retrieval: " f"{time.perf_counter() - rag_start:.2f}s")

        # Return the retrieved document context without calculating anything

        return {
            "type": plan.query.visualization,
            "data": {
                "question": question,
                "chunks": chunks,
            },
            "table_data": None,
            "chart_data": None,
        }

    # Metadata, analytics, and forecast questions continue through the

    # existing deterministic executor

    return await execute_analytics_query(
        df,
        plan.query,
        dataset_id=dataset_id,
        user_id=user_id,
    )


# Main entry point that decides how an AI Analytics query should be executed


async def execute_analytics_query(
    df: pd.DataFrame,
    query: AnalyticsQuery,
    dataset_id: str = "olist",
    user_id: str | None = None,
):

    # Metadata requests inspect the structure of the dataset

    if query.query_type == "metadata":

        execution_result = _execute_metadata_query(
            df,
            query,
        )

        return _build_display_data(
            query,
            execution_result["data"],
        )

    # Forecast requests require an authenticated user

    if query.query_type == "forecast":

        if not user_id:

            raise ValueError("Authenticated user is required for forecast queries.")

        execution_result = await _execute_forecast_query(
            query,
            dataset_id,
            user_id,
        )

        return _build_display_data(
            query,
            execution_result["data"],
        )

    # Return an empty result when there are no rows available for historical analytics

    if df.empty:

        return _build_display_data(
            query,
            None,
        )

    # Apply all requested filters before running the analytics operation

    working_df = _apply_filters(
        df,
        query.filters,
    )

    operation = query.operation

    # Count either all rows or non empty values in a specific column

    if operation == "count":

        if query.field:

            if query.field not in working_df.columns:

                raise ValueError(f"Column '{query.field}' does not exist.")

            result = int(working_df[query.field].notna().sum())

        else:

            result = int(len(working_df))

        return _build_display_data(
            query,
            result,
        )

    # Find the numeric column with the highest or lowest average value

    if operation in {
        "highest_average",
        "lowest_average",
    }:

        # Get only columns that can be used for numeric calculations

        numeric_columns = working_df.select_dtypes(include="number").columns.tolist()

        if not numeric_columns:

            return _build_display_data(
                query,
                None,
            )

        averages = {}

        # Calculate the average separately for every numeric column

        for column in numeric_columns:

            series = working_df[column].dropna()

            if not series.empty:

                averages[column] = float(series.mean())

        # Return no result when none of the numeric columns contain usable values

        if not averages:

            return _build_display_data(
                query,
                None,
            )

        # Select the column with the highest average

        if operation == "highest_average":

            selected_column = max(
                averages,
                key=averages.get,
            )

        # Select the column with the lowest average

        else:

            selected_column = min(
                averages,
                key=averages.get,
            )

        result = {
            "column": selected_column,
            "average": averages[selected_column],
            "averages": averages,
        }

        return _build_display_data(
            query,
            result,
        )

    # Handle numeric operations for a specific field

    if operation in {
        "sum",
        "average",
        "min",
        "max",
    }:

        if not query.field:

            raise ValueError(f"'{operation}' requires a field.")

        # Make sure the selected field can be used for numeric calculations

        _validate_numeric_field(
            working_df,
            query.field,
        )

        series = working_df[query.field].dropna()

        # Return no result when the selected column has no usable values

        if series.empty:

            return _build_display_data(
                query,
                None,
            )

        # Calculate the sum of all values in the selected field

        if operation == "sum":

            result = float(series.sum())

        # Calculate the average of all values in the selected field

        elif operation == "average":

            result = float(series.mean())

        # Find the smallest value in the selected field

        elif operation == "min":

            result = float(series.min())

        # Find the largest value in the selected field

        else:

            result = float(series.max())

        return _build_display_data(
            query,
            result,
        )

    # Group records by one column and calculate the sum of a numeric field

    if operation == "group_by":

        if not query.field:

            raise ValueError("'group_by' requires a numeric field.")

        if not query.group_by:

            raise ValueError("'group_by' requires a grouping field.")

        # The value being aggregated must be numeric

        _validate_numeric_field(
            working_df,
            query.field,
        )

        if query.group_by not in working_df.columns:

            raise ValueError(f"Column '{query.group_by}' does not exist.")

        grouped_df = _normalize_group_values(
            working_df,
            query.group_by,
        )

        result = (
            grouped_df.groupby(
                query.group_by,
                dropna=False,
            )[query.field]
            .sum()
            .reset_index()
        )

        # Sort the grouped results according to the requested direction

        result = result.sort_values(
            by=query.field,
            ascending=query.sort == "asc",
        )

        # Limit the number of groups when requested

        if query.limit:

            result = result.head(query.limit)

        result = result.fillna("").to_dict(orient="records")

        return _build_display_data(
            query,
            result,
        )

    # Group records by one column and return the requested top results

    if operation == "top_n":

        if not query.field:

            raise ValueError("'top_n' requires a numeric field.")

        if not query.group_by:

            raise ValueError("'top_n' requires a grouping field.")

        # The field being ranked must contain numeric values

        _validate_numeric_field(
            working_df,
            query.field,
        )

        if query.group_by not in working_df.columns:

            raise ValueError(f"Column '{query.group_by}' does not exist.")

        grouped_df = _normalize_group_values(
            working_df,
            query.group_by,
        )

        result = (
            grouped_df.groupby(
                query.group_by,
                dropna=False,
            )[query.field]
            .sum()
            .reset_index()
        )

        # Sort the grouped values before selecting the requested number of results

        result = result.sort_values(
            by=query.field,
            ascending=query.sort == "asc",
        )

        # Return 10 results by default when no limit is provided

        limit = query.limit or 10

        result = result.head(limit)

        result = result.fillna("").to_dict(orient="records")

        return _build_display_data(
            query,
            result,
        )

    # Reject analytics operations that are not supported by the backend

    raise ValueError(f"Unsupported analytics operation: " f"{operation}")
