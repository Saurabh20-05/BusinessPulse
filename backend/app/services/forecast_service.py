from app.ml.linear_forecast import (
    forecast as linear_forecast,
)

from app.ml.random_forest_forecast import (
    forecast as random_forest_forecast,
)

from app.ml.polynomial_forecast import (
    forecast as polynomial_forecast,
)


# Pick the model used for each type of forecast
async def forecast_revenue(dataset_id="olist", user_id=None):
    return await linear_forecast(dataset_id, user_id)


async def forecast_orders(dataset_id="olist", user_id=None):
    return await random_forest_forecast(dataset_id, user_id)


async def forecast_customers(dataset_id="olist", user_id=None):
    return await polynomial_forecast(dataset_id, user_id)