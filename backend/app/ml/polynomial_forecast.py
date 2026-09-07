import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from app.ml.forecast_models import (
    get_customer_series,
    calculate_metrics,
    prepare_response,
)

MODEL_NAME = "Polynomial Regression (Degree 2)"


async def forecast(dataset_id="olist", user_id=None):

    series = await get_customer_series(dataset_id, user_id)

    if len(series) < 2:
        raise ValueError(
            "At least 2 months of customer data are required for forecasting."
        )

    # Use the month position as the input value
    x = np.arange(len(series)).reshape(-1, 1)
    y = series.values

    poly = PolynomialFeatures(degree=2)

    # Add the squared term so the model can follow a curve
    x_poly = poly.fit_transform(x)

    model = LinearRegression()
    model.fit(x_poly, y)

    historical_prediction = model.predict(x_poly)

    metrics = calculate_metrics(
        y,
        historical_prediction,
    )

    # Prepare the next 4 months for prediction
    future_x = np.arange(
        len(series),
        len(series) + 4,
    ).reshape(-1, 1)

    future_poly = poly.transform(future_x)

    future_prediction = model.predict(future_poly)

    # Review scores should not be negative
    future_prediction = np.clip(
        future_prediction,
        1,
        5,
    )

    return prepare_response(
        MODEL_NAME,
        series,
        future_prediction,
        metrics,
    )
