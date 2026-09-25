# from app.ml.linear_forecast import (
#     forecast as linear_forecast,
# )

# from app.ml.random_forest_forecast import (
#     forecast as random_forest_forecast,
# )

# from app.ml.polynomial_forecast import (
#     forecast as polynomial_forecast,
# )


# # Pick the model used for each type of forecast
# async def forecast_revenue(dataset_id="olist", user_id=None):
#     return await linear_forecast(dataset_id, user_id)


# async def forecast_orders(dataset_id="olist", user_id=None):
#     return await random_forest_forecast(dataset_id, user_id)


# async def forecast_customers(dataset_id="olist", user_id=None):
#     return await polynomial_forecast(dataset_id, user_id)



from app.ml.forecast_models import (
    get_revenue_series,
    get_orders_series,
    get_customer_series,
)

from app.ml.linear_forecast import (
    forecast_series as linear_forecast,
)

from app.ml.random_forest_forecast import (
    forecast_series as random_forest_forecast,
)

from app.ml.polynomial_forecast import (
    forecast_series as polynomial_forecast,
)


MODEL_FUNCTIONS = {
    "linear": linear_forecast,
    "random_forest": random_forest_forecast,
    "polynomial": polynomial_forecast,
}


MODEL_NAMES = {
    "linear": "Linear Regression",
    "random_forest": "Random Forest Regressor",
    "polynomial": "Polynomial Regression (Degree 2)",
}


async def forecast(
    prediction_type,
    model_name="linear",
    dataset_id="olist",
    user_id=None,
):
    if model_name not in MODEL_FUNCTIONS:
        raise ValueError(
            "Invalid model. Choose linear, random_forest, or polynomial."
        )

    if prediction_type == "revenue":
        series = await get_revenue_series(
            dataset_id,
            user_id,
        )

    elif prediction_type == "orders":
        series = await get_orders_series(
            dataset_id,
            user_id,
        )

    elif prediction_type == "customers":
        series = await get_customer_series(
            dataset_id,
            user_id,
        )

    else:
        raise ValueError(
            "Invalid prediction type. Choose revenue, orders, or customers."
        )

    if len(series) < 2:
        raise ValueError(
            "At least 2 months of data are required for forecasting."
        )

    forecast_function = MODEL_FUNCTIONS[model_name]

    result = forecast_function(series)

    # Keep customer satisfaction predictions within the review scale.
    if prediction_type == "customers":
        for point in result["predicted"]:
            point["value"] = round(
                min(
                    max(point["value"], 1),
                    5,
                ),
                2,
            )

    result["prediction_type"] = prediction_type
    result["model_key"] = model_name
    result["model_used"] = MODEL_NAMES[model_name]

    return result


async def forecast_revenue(
    dataset_id="olist",
    user_id=None,
    model_name="linear",
):
    return await forecast(
        prediction_type="revenue",
        model_name=model_name,
        dataset_id=dataset_id,
        user_id=user_id,
    )


async def forecast_orders(
    dataset_id="olist",
    user_id=None,
    model_name="random_forest",
):
    return await forecast(
        prediction_type="orders",
        model_name=model_name,
        dataset_id=dataset_id,
        user_id=user_id,
    )


async def forecast_customers(
    dataset_id="olist",
    user_id=None,
    model_name="polynomial",
):
    return await forecast(
        prediction_type="customers",
        model_name=model_name,
        dataset_id=dataset_id,
        user_id=user_id,
    )
