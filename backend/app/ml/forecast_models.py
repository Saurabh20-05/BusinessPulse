import pandas as pd

from sklearn.metrics import mean_absolute_error, r2_score

from app.utils.data_loader import get_full_dataset

FORECAST_MONTHS = 4


# Get total revenue for each month
async def get_revenue_series(dataset_id="olist", user_id=None):
    df = await get_full_dataset(dataset_id, user_id)

    if dataset_id != "olist":
        if "date" not in df.columns or "revenue" not in df.columns:
            return pd.Series(dtype=float)

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
        )

        series = df.groupby(df["date"].dt.to_period("M"))["revenue"].sum().sort_index()

        series = series[series > 0]

        return series

    series = df.groupby("order_month")["item_total"].sum().sort_index()

    series = series[series > 0]

    return series


# Get the total number of orders for each month
async def get_orders_series(dataset_id="olist", user_id=None):
    df = await get_full_dataset(dataset_id, user_id)

    if dataset_id != "olist":
        if "date" not in df.columns or "orders" not in df.columns:
            return pd.Series(dtype=float)

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
        )

        series = df.groupby(df["date"].dt.to_period("M"))["orders"].sum().sort_index()

        series = series[series > 0]

        return series

    series = df.groupby("order_month")["order_id"].nunique().sort_index()

    series = series[series > 0]

    return series


# Track the average customer review score by month
async def get_customer_series(dataset_id="olist", user_id=None):
    df = await get_full_dataset(dataset_id, user_id)

    if dataset_id != "olist":
        if "date" not in df.columns or "customers" not in df.columns:
            return pd.Series(dtype=float)

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
        )

        series = (
            df.groupby(df["date"].dt.to_period("M"))["customers"].sum().sort_index()
        )

        series = series[series > 0]

        return series

    review_series = df.groupby("order_month")["review_score"].mean().sort_index()

    review_series = review_series.dropna()

    return review_series


# Generate the months we need to predict
def get_future_months(series):

    last_month = pd.Period(series.index[-1], freq="M")

    return [str(last_month + i) for i in range(1, FORECAST_MONTHS + 1)]


def calculate_metrics(actual, predicted):

    return {
        "mae": round(
            float(mean_absolute_error(actual, predicted)),
            2,
        ),
        "r2": round(
            float(r2_score(actual, predicted)),
            3,
        ),
    }


def prepare_response(
    model_name,
    series,
    future_values,
    metrics,
):

    # Format past and predicted values for the API response
    future_months = get_future_months(series)

    historical = [
        {
            "month": str(month),
            "value": round(float(value), 2),
        }
        for month, value in series.items()
    ]

    predicted = [
        {
            "month": month,
            "value": round(float(value), 2),
        }
        for month, value in zip(
            future_months,
            future_values,
        )
    ]

    return {
        "model_used": model_name,
        "historical": historical,
        "predicted": predicted,
        "metrics": metrics,
    }
