import numpy as np

from sklearn.ensemble import RandomForestRegressor

from app.ml.forecast_models import (
    get_orders_series,
    calculate_metrics,
    prepare_response,
)

MODEL_NAME = "Random Forest Regressor"


def forecast():

    series = get_orders_series()

    # Use the month number to train the model
    x = np.arange(len(series)).reshape(-1, 1)
    y = series.values

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
    )

    model.fit(x, y)

    historical_prediction = model.predict(x)

    metrics = calculate_metrics(
        y,
        historical_prediction,
    )

    # Get the next 4 months for the forecast
    future_x = np.arange(
        len(series),
        len(series) + 4,
    ).reshape(-1, 1)

    future_prediction = model.predict(future_x)

    # Avoid returning negative order values
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
