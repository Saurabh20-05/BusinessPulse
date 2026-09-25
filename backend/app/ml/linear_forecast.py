# import numpy as np

# from sklearn.linear_model import LinearRegression

# from app.ml.forecast_models import (
#     get_revenue_series,
#     calculate_metrics,
#     prepare_response,
# )

# MODEL_NAME = "Linear Regression"


# async def forecast(dataset_id="olist", user_id=None):

#     series = await get_revenue_series(dataset_id, user_id)

#     if len(series) < 2:
#         raise ValueError(
#             "At least 2 months of revenue data are required for forecasting."
#         )

#     # Use the month index as the input for the model
#     x = np.arange(len(series)).reshape(-1, 1)
#     y = series.values

#     model = LinearRegression()
#     model.fit(x, y)

#     # Check how well the model fits the existing data
#     historical_prediction = model.predict(x)

#     metrics = calculate_metrics(
#         y,
#         historical_prediction,
#     )

#     # Predict revenue for the next four months
#     future_x = np.arange(
#         len(series),
#         len(series) + 4,
#     ).reshape(-1, 1)

#     future_prediction = model.predict(future_x)

#     # Revenue should not go below zero
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

from sklearn.linear_model import LinearRegression

from app.ml.forecast_models import (
    get_revenue_series,
    get_orders_series,
    get_customer_series,
    calculate_metrics,
    prepare_response,
    FORECAST_MONTHS,
)

MODEL_NAME = "Linear Regression"


def forecast_series(series):
    if len(series) < 2:
        raise ValueError(
            "At least 2 months of data are required for forecasting."
        )

    # Use the month index as the input for the model
    x = np.arange(len(series)).reshape(-1, 1)
    y = series.values

    model = LinearRegression()
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
    series = await get_revenue_series(
        dataset_id,
        user_id,
    )

    return forecast_series(series)


async def forecast_orders(dataset_id="olist", user_id=None):
    series = await get_orders_series(
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
