import pandas as pd

from app.repositories.sales_repository import get_dataset
from app.utils.data_loader import get_raw_tables


def get_status(percentage):
    if percentage == 0:
        return "good"

    if percentage <= 5:
        return "warning"

    return "error"


def calculate_quality_score(
    missing_percentage,
    duplicate_percentage,
    invalid_date_percentage,
    negative_percentage,
):
    penalty = (
        missing_percentage * 0.4
        + duplicate_percentage * 0.2
        + invalid_date_percentage * 0.2
        + negative_percentage * 0.2
    )

    return int(round(max(0, 100 - penalty)))


def analyze_dataframe(df):
    if df.empty:
        return {
            "rows": 0,
            "columns": 0,
            "missing_values": 0,
            "duplicate_rows": 0,
            "invalid_dates": 0,
            "negative_values": 0,
            "missing_percentage": 0,
            "duplicate_percentage": 0,
            "invalid_date_percentage": 0,
            "negative_percentage": 0,
            "columns_detail": [],
        }

    rows = len(df)
    columns = len(df.columns)

    missing_values = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    total_cells = rows * columns

    missing_percentage = (
        missing_values / total_cells * 100
        if total_cells
        else 0
    )

    duplicate_percentage = (
        duplicate_rows / rows * 100
        if rows
        else 0
    )

    date_columns = [
        column
        for column in df.columns
        if "date" in column.lower()
        or "time" in column.lower()
    ]

    invalid_dates = 0
    total_date_values = 0

    for column in date_columns:
        non_empty_values = int(df[column].notna().sum())

        converted = pd.to_datetime(
            df[column],
            errors="coerce",
        )

        invalid_dates += (
            non_empty_values
            - int(converted.notna().sum())
        )

        total_date_values += non_empty_values

    invalid_date_percentage = (
        invalid_dates / total_date_values * 100
        if total_date_values
        else 0
    )

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_columns):
        negative_values = int(
            (df[numeric_columns] < 0).sum().sum()
        )

        total_numeric_values = int(
            df[numeric_columns].notna().sum().sum()
        )
    else:
        negative_values = 0
        total_numeric_values = 0

    negative_percentage = (
        negative_values / total_numeric_values * 100
        if total_numeric_values
        else 0
    )

    columns_detail = []

    for column in df.columns:
        series = df[column]

        if pd.api.types.is_numeric_dtype(series):
            data_type = "number"
        elif pd.api.types.is_datetime64_any_dtype(series):
            data_type = "date"
        else:
            data_type = "text"

        columns_detail.append(
            {
                "name": column,
                "type": data_type,
                "missing": int(series.isna().sum()),
                "unique": int(series.nunique(dropna=True)),
            }
        )

    return {
        "rows": rows,
        "columns": columns,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "invalid_dates": invalid_dates,
        "negative_values": negative_values,
        "missing_percentage": round(
            missing_percentage,
            2,
        ),
        "duplicate_percentage": round(
            duplicate_percentage,
            2,
        ),
        "invalid_date_percentage": round(
            invalid_date_percentage,
            2,
        ),
        "negative_percentage": round(
            negative_percentage,
            2,
        ),
        "columns_detail": columns_detail,
    }


async def get_data_quality(
    dataset_id="olist",
    user_id=None,
):
    if dataset_id == "olist":
        tables = get_raw_tables()

        table_results = []

        for table_name, table_df in tables.items():
            result = analyze_dataframe(table_df)

            result["table"] = table_name

            table_results.append(result)

        total_rows = sum(
            result["rows"]
            for result in table_results
        )

        total_columns = sum(
            result["columns"]
            for result in table_results
        )

        total_missing = sum(
            result["missing_values"]
            for result in table_results
        )

        total_duplicates = sum(
            result["duplicate_rows"]
            for result in table_results
        )

        total_invalid_dates = sum(
            result["invalid_dates"]
            for result in table_results
        )

        total_negative_values = sum(
            result["negative_values"]
            for result in table_results
        )

        total_cells = sum(
            result["rows"] * result["columns"]
            for result in table_results
        )

        missing_percentage = (
            total_missing / total_cells * 100
            if total_cells
            else 0
        )

        duplicate_percentage = (
            total_duplicates / total_rows * 100
            if total_rows
            else 0
        )

        total_date_values = sum(
            int(
                table_df[column].notna().sum()
            )
            for table_df in tables.values()
            for column in table_df.columns
            if "date" in column.lower()
            or "time" in column.lower()
        )

        invalid_date_percentage = (
            total_invalid_dates
            / total_date_values
            * 100
            if total_date_values
            else 0
        )

        total_numeric_values = sum(
            int(
                table_df.select_dtypes(
                    include="number"
                ).notna().sum().sum()
            )
            for table_df in tables.values()
        )

        negative_percentage = (
            total_negative_values
            / total_numeric_values
            * 100
            if total_numeric_values
            else 0
        )

        quality_score = calculate_quality_score(
            missing_percentage,
            duplicate_percentage,
            invalid_date_percentage,
            negative_percentage,
        )

        return {
            "quality_score": quality_score,
            "summary": {
                "rows": total_rows,
                "columns": total_columns,
                "missing_values": total_missing,
                "duplicate_rows": total_duplicates,
            },
            "checks": {
                "missing_values": {
                    "count": total_missing,
                    "percentage": round(
                        missing_percentage,
                        2,
                    ),
                    "status": get_status(
                        missing_percentage
                    ),
                },
                "duplicate_rows": {
                    "count": total_duplicates,
                    "percentage": round(
                        duplicate_percentage,
                        2,
                    ),
                    "status": get_status(
                        duplicate_percentage
                    ),
                },
                "invalid_dates": {
                    "count": total_invalid_dates,
                    "percentage": round(
                        invalid_date_percentage,
                        2,
                    ),
                    "status": get_status(
                        invalid_date_percentage
                    ),
                },
                "negative_values": {
                    "count": total_negative_values,
                    "percentage": round(
                        negative_percentage,
                        2,
                    ),
                    "status": get_status(
                        negative_percentage
                    ),
                },
            },
            "columns": [
                column
                for result in table_results
                for column in result["columns_detail"]
            ],
            "tables": table_results,
        }

    df = await get_dataset(
        dataset_id,
        user_id,
    )

    result = analyze_dataframe(df)

    quality_score = calculate_quality_score(
        result["missing_percentage"],
        result["duplicate_percentage"],
        result["invalid_date_percentage"],
        result["negative_percentage"],
    )

    return {
        "quality_score": quality_score,
        "summary": {
            "rows": result["rows"],
            "columns": result["columns"],
            "missing_values": result["missing_values"],
            "duplicate_rows": result["duplicate_rows"],
        },
        "checks": {
            "missing_values": {
                "count": result["missing_values"],
                "percentage": result["missing_percentage"],
                "status": get_status(
                    result["missing_percentage"]
                ),
            },
            "duplicate_rows": {
                "count": result["duplicate_rows"],
                "percentage": result["duplicate_percentage"],
                "status": get_status(
                    result["duplicate_percentage"]
                ),
            },
            "invalid_dates": {
                "count": result["invalid_dates"],
                "percentage": result["invalid_date_percentage"],
                "status": get_status(
                    result["invalid_date_percentage"]
                ),
            },
            "negative_values": {
                "count": result["negative_values"],
                "percentage": result["negative_percentage"],
                "status": get_status(
                    result["negative_percentage"]
                ),
            },
        },
        "columns": result["columns_detail"],
    }