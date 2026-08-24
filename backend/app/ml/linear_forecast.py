import numpy as np

from sklearn.linear_model import LinearRegression

from app.ml.forecast_models import (
    get_revenue_series,
    calculate_metrics,
    prepare_response,
)

MODEL_NAME = "Linear Regression"


def forecast():

    series = get_revenue_series()

    # Use month numbers as the input for the model
    x = np.arange(len(series)).reshape(-1, 1)
    y = series.values

    model = LinearRegression()
    model.fit(x, y)

    historical_prediction = model.predict(x)

    metrics = calculate_metrics(
        y,
        historical_prediction,
    )

    # Create the next 4 months for forecasting
    future_x = np.arange(
        len(series),
        len(series) + 4,
    ).reshape(-1, 1)

    future_prediction = model.predict(future_x)

    # Revenue should not go below zero
    future_prediction = np.clip(
        future_prediction,
        0,
        None,
    )

    return prepare_response(
        MODEL_NAME,
        series,
        future_prediction,
        metrics,
    )
