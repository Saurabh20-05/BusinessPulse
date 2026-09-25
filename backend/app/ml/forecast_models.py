# import pandas as pd

# from sklearn.metrics import mean_absolute_error, r2_score

# from app.utils.data_loader import get_full_dataset

# FORECAST_MONTHS = 4


# # Get total revenue for each month
# async def get_revenue_series(dataset_id="olist", user_id=None):
#     df = await get_full_dataset(dataset_id, user_id)

#     if dataset_id != "olist":
#         if "date" not in df.columns or "revenue" not in df.columns:
#             return pd.Series(dtype=float)

#         df["date"] = pd.to_datetime(
#             df["date"],
#             errors="coerce",
#         )

#         series = df.groupby(df["date"].dt.to_period("M"))["revenue"].sum().sort_index()

#         series = series[series > 0]

#         return series

#     series = df.groupby("order_month")["item_total"].sum().sort_index()

#     series = series[series > 0]

#     return series


# # Get the total number of orders for each month
# async def get_orders_series(dataset_id="olist", user_id=None):
#     df = await get_full_dataset(dataset_id, user_id)

#     if dataset_id != "olist":
#         if "date" not in df.columns or "orders" not in df.columns:
#             return pd.Series(dtype=float)

#         df["date"] = pd.to_datetime(
#             df["date"],
#             errors="coerce",
#         )

#         series = df.groupby(df["date"].dt.to_period("M"))["orders"].sum().sort_index()

#         series = series[series > 0]

#         return series

#     series = df.groupby("order_month")["order_id"].nunique().sort_index()

#     series = series[series > 0]

#     return series


# # Track the average customer review score by month
# async def get_customer_series(dataset_id="olist", user_id=None):
#     df = await get_full_dataset(dataset_id, user_id)

#     if dataset_id != "olist":
#         if "date" not in df.columns or "customers" not in df.columns:
#             return pd.Series(dtype=float)

#         df["date"] = pd.to_datetime(
#             df["date"],
#             errors="coerce",
#         )

#         series = (
#             df.groupby(df["date"].dt.to_period("M"))["customers"].sum().sort_index()
#         )

#         series = series[series > 0]

#         return series

#     review_series = df.groupby("order_month")["review_score"].mean().sort_index()

#     review_series = review_series.dropna()

#     return review_series


# # Generate the months we need to predict
# def get_future_months(series):

#     last_month = pd.Period(series.index[-1], freq="M")

#     return [str(last_month + i) for i in range(1, FORECAST_MONTHS + 1)]


# def calculate_metrics(actual, predicted):

#     return {
#         "mae": round(
#             float(mean_absolute_error(actual, predicted)),
#             2,
#         ),
#         "r2": round(
#             float(r2_score(actual, predicted)),
#             3,
#         ),
#     }


# def prepare_response(
#     model_name,
#     series,
#     future_values,
#     metrics,
# ):

#     # Format past and predicted values for the API response
#     future_months = get_future_months(series)

#     historical = [
#         {
#             "month": str(month),
#             "value": round(float(value), 2),
#         }
#         for month, value in series.items()
#     ]

#     predicted = [
#         {
#             "month": month,
#             "value": round(float(value), 2),
#         }
#         for month, value in zip(
#             future_months,
#             future_values,
#         )
#     ]

#     return {
#         "model_used": model_name,
#         "historical": historical,
#         "predicted": predicted,
#         "metrics": metrics,
#     }






import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from app.utils.data_loader import (
    get_full_dataset,
    get_payments_with_orders,
    get_reviews_with_orders,
)

FORECAST_MONTHS = 4


async def get_revenue_series(dataset_id="olist", user_id=None):
    """
    Return monthly revenue data for forecasting.
    """

    if dataset_id != "olist":
        df = await get_full_dataset(dataset_id, user_id)

        if df.empty or "date" not in df.columns or "revenue" not in df.columns:
            return pd.Series(dtype=float)

        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        df = df.dropna(subset=["date", "revenue"])

        series = (
            df.groupby(df["date"].dt.to_period("M"))["revenue"]
            .sum()
            .sort_index()
        )

        series.index = series.index.to_timestamp()

        return series

    df = await get_full_dataset("olist", None)

    if df.empty:
        return pd.Series(dtype=float)

    if "order_month" in df.columns and "item_total" in df.columns:
        series = (
            df.groupby("order_month")["item_total"]
            .sum()
            .sort_index()
        )

        return series

    if "order_purchase_timestamp" in df.columns:
        df["order_purchase_timestamp"] = pd.to_datetime(
            df["order_purchase_timestamp"],
            errors="coerce",
        )

        df = df.dropna(subset=["order_purchase_timestamp"])

        if "price" in df.columns:
            series = (
                df.groupby(
                    df["order_purchase_timestamp"].dt.to_period("M")
                )["price"]
                .sum()
                .sort_index()
            )

            series.index = series.index.to_timestamp()

            return series

    return pd.Series(dtype=float)


async def get_orders_series(dataset_id="olist", user_id=None):
    """
    Return monthly order data for forecasting.
    """

    if dataset_id != "olist":
        df = await get_full_dataset(dataset_id, user_id)

        if df.empty or "date" not in df.columns or "orders" not in df.columns:
            return pd.Series(dtype=float)

        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        df = df.dropna(subset=["date", "orders"])

        series = (
            df.groupby(df["date"].dt.to_period("M"))["orders"]
            .sum()
            .sort_index()
        )

        series.index = series.index.to_timestamp()

        return series

    df = await get_full_dataset("olist", None)

    if df.empty:
        return pd.Series(dtype=float)

    if "order_purchase_timestamp" in df.columns:
        df["order_purchase_timestamp"] = pd.to_datetime(
            df["order_purchase_timestamp"],
            errors="coerce",
        )

        df = df.dropna(subset=["order_purchase_timestamp"])

        if "order_id" in df.columns:
            series = (
                df.groupby(
                    df["order_purchase_timestamp"].dt.to_period("M")
                )["order_id"]
                .nunique()
                .sort_index()
            )

            series.index = series.index.to_timestamp()

            return series

    return pd.Series(dtype=float)


async def get_customer_series(dataset_id="olist", user_id=None):
    """
    Return monthly customer satisfaction data for forecasting.
    """

    if dataset_id != "olist":
        df = await get_full_dataset(dataset_id, user_id)

        if (
            df.empty
            or "date" not in df.columns
            or "review_score" not in df.columns
        ):
            return pd.Series(dtype=float)

        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        df = df.dropna(subset=["date", "review_score"])

        series = (
            df.groupby(df["date"].dt.to_period("M"))["review_score"]
            .mean()
            .sort_index()
        )

        series.index = series.index.to_timestamp()

        return series

    df = get_reviews_with_orders()

    if df.empty:
        return pd.Series(dtype=float)

    if (
        "order_purchase_timestamp" not in df.columns
        or "review_score" not in df.columns
    ):
        return pd.Series(dtype=float)

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"],
        errors="coerce",
    )

    df = df.dropna(
        subset=[
            "order_purchase_timestamp",
            "review_score",
        ]
    )

    series = (
        df.groupby(
            df["order_purchase_timestamp"].dt.to_period("M")
        )["review_score"]
        .mean()
        .sort_index()
    )

    series.index = series.index.to_timestamp()

    return series


def get_future_months(last_date, months=FORECAST_MONTHS):
    """
    Generate future monthly dates.
    """

    return pd.date_range(
        start=last_date + pd.offsets.MonthBegin(1),
        periods=months,
        freq="MS",
    )


def calculate_metrics(actual, predicted):
    """
    Calculate MAE, RMSE, and R2 metrics.
    """

    actual = list(actual)
    predicted = list(predicted)

    if not actual or not predicted:
        return {
            "mae": 0.0,
            "rmse": 0.0,
            "r2": 0.0,
        }

    mae = mean_absolute_error(
        actual,
        predicted,
    )

    rmse = mean_squared_error(
        actual,
        predicted,
    ) ** 0.5

    if len(actual) < 2:
        r2 = 0.0
    else:
        r2 = r2_score(
            actual,
            predicted,
        )

    return {
        "mae": round(float(mae), 2),
        "rmse": round(float(rmse), 2),
        "r2": round(float(r2), 4),
    }



def prepare_response(
    model_name,
    series,
    future_prediction,
    metrics,
):
    """
    Prepare the common forecast API response.
    """

    historical = []

    for date, value in series.items():
        historical.append(
            {
                "month": pd.Timestamp(date).strftime("%Y-%m"),
                "value": round(float(value), 2),
            }
        )

    future_months = get_future_months(
        pd.Timestamp(series.index[-1])
    )

    predicted = []

    for date, value in zip(
        future_months,
        future_prediction,
    ):
        predicted.append(
            {
                "month": pd.Timestamp(date).strftime("%Y-%m"),
                "value": round(float(value), 2),
            }
        )

    return {
        "model_used": model_name,
        "historical": historical,
        "predicted": predicted,
        "metrics": metrics,
    }