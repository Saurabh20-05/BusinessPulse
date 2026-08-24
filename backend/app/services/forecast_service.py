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
def forecast_revenue():
    return linear_forecast()


def forecast_orders():
    return random_forest_forecast()


def forecast_customers():
    return polynomial_forecast()
