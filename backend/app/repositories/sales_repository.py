import pandas as pd

from app.utils.data_loader import (
    get_full_dataset,
    get_payments_with_orders,
    get_reviews_with_orders,
)


async def get_dataset(dataset_id="olist", user_id=None):
    return await get_full_dataset(
        dataset_id,
        user_id,
    )


async def get_payments(dataset_id="olist", user_id=None):
    # Handle payment data from a user's uploaded dataset
    if dataset_id != "olist":
        df = await get_dataset(
            dataset_id,
            user_id,
        )

        if "payment_method" not in df.columns:
            return pd.DataFrame(columns=["payment_type"])

        return df.rename(
            columns={"payment_method": "payment_type"}
        )

    return get_payments_with_orders()


async def get_reviews(dataset_id="olist", user_id=None):
    # Handle review data from a user's uploaded dataset
    if dataset_id != "olist":
        df = await get_dataset(
            dataset_id,
            user_id,
        )

        if "review_score" not in df.columns:
            return pd.DataFrame(columns=["review_score"])

        return df

    return get_reviews_with_orders()