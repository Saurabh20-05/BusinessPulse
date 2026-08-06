



import pandas as pd

from sklearn.metrics import mean_absolute_error, r2_score

from app.utils.data_loader import get_full_dataset



FORECAST_MONTHS = 4






def get_revenue_series():

    df = get_full_dataset()

    series = (df.groupby("order_month")["item_total"].sum().sort_index())

    series = series[series > 0]

    return series






def get_orders_series():

    df = get_full_dataset()

    series = (df.groupby("order_month")["item_total"].mean().sort_index())

    series = series[series > 0]

    return series








def get_customer_series():

    df = get_full_dataset()

    review_series = (df.groupby("order_month")["review_score"].mean().sort_index())

    review_series = review_series.dropna()

    return review_series








def get_future_months(series):

    last_month = pd.Period(series.index[-1], freq="M")

    return [
        str(last_month + i)
        for i in range(1, FORECAST_MONTHS + 1)
    ]







def calculate_metrics(actual, predicted):

    return {
        "mae": round(float(mean_absolute_error(actual, predicted)),2,),
        "r2": round(float(r2_score(actual, predicted)),3,),
    }










def prepare_response(
    model_name,
    series,
    future_values,
    metrics,
):

    future_months = get_future_months(series)

    historical = [
        {
            
            "month": month,
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