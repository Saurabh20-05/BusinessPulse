# import numpy as np

# from sklearn.ensemble import RandomForestRegressor

# from app.ml.forecast_models import (
#     get_orders_series,
#     calculate_metrics,
#     prepare_response,
# )

# MODEL_NAME = "Random Forest Regressor"


# async def forecast(dataset_id="olist", user_id=None):

#     series = await get_orders_series(dataset_id, user_id)

#     if len(series) < 2:
#         raise ValueError(
#             "At least 2 months of order data are required for forecasting."
#         )

#     # Use the month number to train the model
#     x = np.arange(len(series)).reshape(-1, 1)
#     y = series.values

#     model = RandomForestRegressor(
#         n_estimators=100,
#         random_state=42,
#     )

#     model.fit(x, y)

#     historical_prediction = model.predict(x)

#     metrics = calculate_metrics(
#         y,
#         historical_prediction,
#     )

#     # Get the next 4 months for the forecast
#     future_x = np.arange(
#         len(series),
#         len(series) + 4,
#     ).reshape(-1, 1)

#     future_prediction = model.predict(future_x)

#     # Avoid returning negative order values
#     future_prediction = np.clip(
#         future_prediction,
#         0,
#         None,
#     )

#     return prepare_response(
#         MODEL_NAME,
#         series,
#         future_prediction,
#         metrics,
#     )






import numpy as np

from sklearn.ensemble import RandomForestRegressor

from app.ml.forecast_models import (
    get_revenue_series,
    get_orders_series,
    get_customer_series,
    calculate_metrics,
    prepare_response,
    FORECAST_MONTHS,
)

MODEL_NAME = "Random Forest Regressor"


def forecast_series(series):
    if len(series) < 2:
        raise ValueError(
            "At least 2 months of data are required for forecasting."
        )

    # Use the month index as the input for the model
    x = np.arange(len(series)).reshape(-1, 1)
    y = series.values

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
    )

    model.fit(x, y)

    # Check how well the model fits the existing data
    historical_prediction = model.predict(x)

    metrics = calculate_metrics(
        y,
        historical_prediction,
    )

    # Predict the next four months
    future_x = np.arange(
        len(series),
        len(series) + FORECAST_MONTHS,
    ).reshape(-1, 1)

    future_prediction = model.predict(future_x)

    # Predictions should not go below zero
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


async def forecast(dataset_id="olist", user_id=None):
    series = await get_orders_series(
        dataset_id,
        user_id,
    )

    return forecast_series(series)


async def forecast_revenue(dataset_id="olist", user_id=None):
    series = await get_revenue_series(
        dataset_id,
        user_id,
    )

    return forecast_series(series)


async def forecast_customers(dataset_id="olist", user_id=None):
    series = await get_customer_series(
        dataset_id,
        user_id,
    )

    return forecast_series(series)
