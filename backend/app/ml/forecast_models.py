
import numpy as np
import pandas as pd


from sklearn.linear_model import LinearRegression



from app.utils.data_loader import get_full_dataset




FORECAST_MONTHS = 4
MODEL_NAME = "Linear Regression"




def _get_monthly_data(value_col, agg="sum", count_col=None):


    df = get_full_dataset()

    if count_col:
        series = df.groupby("order_month")[count_col].nunique()
    else:
        series = df.groupby("order_month")[value_col].agg(agg)

    return series.sort_index()








def _train_model(series):


    month_numbers = np.arange(len(series)).reshape(-1, 1)
    values = series.values


    model = LinearRegression()
    model.fit(month_numbers, values)





    future_months = np.arange(len(series),len(series) + FORECAST_MONTHS).reshape(-1, 1)


    future_values = model.predict(future_months)

    # PREVENT NEGATIVE VALUES
    future_values = np.clip(future_values, 0, None)


    return future_values








def _get_future_months(series):


    last_month = pd.Period(series.index[-1], freq="M")

    months = []


    for i in range(1, FORECAST_MONTHS + 1):
        months.append(str(last_month + i))

    return months




















def forecast_revenue():
    series = _get_monthly_data("item_total")
    return _prepare_response(series, MODEL_NAME)















def forecast_orders():

    series = _get_monthly_data(
        value_col=None,
        count_col="order_id"
    )

    return _prepare_response(series, MODEL_NAME)












def forecast_customers():

    df = get_full_dataset()

    series = (
        df.groupby("order_month")["customer_id"]
        .nunique()
        .sort_index()
    )


    return _prepare_response(series, MODEL_NAME)

























def _prepare_response(series, model_name):


    future_values = _train_model(series)
    future_months = _get_future_months(series)


    historical = []


    for month, value in series.items():
        historical.append({
            "month": month,
            "value": round(float(value), 2)
        })



    predicted = []


    for month, value in zip(future_months, future_values):
        predicted.append({
            "month": month,
            "value": round(float(value), 2)
        })


    return {
        "model_used": model_name,
        "historical": historical,
        "predicted": predicted,
    }
