# import os

# import pandas as pd

# from app.repositories import dataset_repository

# DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


# _cache = {}


# def _read(file_name):
#     file_path = os.path.join(DATA_DIR, file_name)

#     return pd.read_csv(file_path)


# def _load_raw():

#     customers = _read("olist_customers.csv")
#     sellers = _read("olist_sellers.csv")
#     products = _read("olist_products.csv")
#     orders = _read("olist_orders.csv")
#     order_items = _read("olist_order_items.csv")
#     payments = _read("olist_payments.csv")
#     reviews = _read("olist_reviews.csv")

#     date_columns = [
#         "order_purchase_timestamp",
#         "order_approved_at",
#         "order_delivered_carrier_date",
#         "order_delivered_customer_date",
#         "order_estimated_delivery_date",
#     ]

#     # Convert the date columns once when the data is loaded
#     for column in date_columns:
#         orders[column] = pd.to_datetime(
#             orders[column],
#             errors="coerce",
#         )

#     order_items["shipping_limit_date"] = pd.to_datetime(
#         order_items["shipping_limit_date"],
#         errors="coerce",
#     )

#     review_dates = [
#         "review_creation_date",
#         "review_answer_timestamp",
#     ]

#     for column in review_dates:
#         reviews[column] = pd.to_datetime(
#             reviews[column],
#             errors="coerce",
#         )

#     # Remove rows missing the fields needed for the joins
#     orders = orders.dropna(subset=["order_id", "customer_id"])

#     order_items = order_items.dropna(subset=["order_id", "product_id", "price"])

#     products["product_category_name"] = products["product_category_name"].fillna(
#         "unknown"
#     )

#     return {
#         "customers": customers,
#         "sellers": sellers,
#         "products": products,
#         "orders": orders,
#         "order_items": order_items,
#         "payments": payments,
#         "reviews": reviews,
#     }


# def get_raw_tables():

#     # Load the CSV files only once and reuse them
#     if "raw" not in _cache:
#         _cache["raw"] = _load_raw()

#     return _cache["raw"]


# async def get_full_dataset(dataset_id="olist", user_id=None):

#     if dataset_id != "olist":
#         dataset = await dataset_repository.find_dataset_by_id(
#             dataset_id,
#             user_id,
#         )

#         if not dataset:
#             raise ValueError("Dataset not found.")

#         return pd.DataFrame(dataset["normalized_data"])

#     if "full" in _cache:
#         return _cache["full"]

#     raw = get_raw_tables()

#     # Combine the main tables into one dataset for the dashboard
#     df = raw["order_items"]

#     df = df.merge(
#         raw["orders"],
#         on="order_id",
#         how="left",
#     )

#     df = df.merge(
#         raw["products"],
#         on="product_id",
#         how="left",
#     )

#     df = df.merge(
#         raw["sellers"],
#         on="seller_id",
#         how="left",
#     )

#     df = df.merge(
#         raw["customers"],
#         on="customer_id",
#         how="left",
#     )

#     df = df.merge(
#         raw["reviews"][["order_id", "review_score"]],
#         on="order_id",
#         how="left",
#     )

#     # REMOVE CANCELLED ORDERES
#     df = df[df["order_status"] != "canceled"].copy()

#     # Add the month and total value used by the analytics
#     df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)

#     df["item_total"] = df["price"] + df["freight_value"]

#     _cache["full"] = df

#     return df


# def get_payments_with_orders():

#     # Reuse the processed payment data if it is already loaded
#     if "payments_full" in _cache:
#         return _cache["payments_full"]

#     raw = get_raw_tables()

#     df = raw["payments"]

#     df = df.merge(
#         raw["orders"],
#         on="order_id",
#         how="left",
#     )

#     df = df[df["order_status"] != "canceled"].copy()

#     _cache["payments_full"] = df

#     return df


# def get_reviews_with_orders():

#     # Reuse the processed review data if it is already loaded
#     if "reviews_full" in _cache:
#         return _cache["reviews_full"]

#     raw = get_raw_tables()

#     df = raw["reviews"]

#     df = df.merge(
#         raw["orders"],
#         on="order_id",
#         how="left",
#     )

#     _cache["reviews_full"] = df

#     return df









import io
import os

import pandas as pd

from app.repositories import dataset_repository


DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
)

# Cache raw Olist tables and processed datasets
_cache = {}

# Separate cache for custom datasets
_custom_dataset_cache = {}


def _read(file_name):
    file_path = os.path.join(
        DATA_DIR,
        file_name,
    )

    return pd.read_csv(file_path)


def _load_raw():
    customers = _read("olist_customers.csv")
    sellers = _read("olist_sellers.csv")
    products = _read("olist_products.csv")
    orders = _read("olist_orders.csv")
    order_items = _read("olist_order_items.csv")
    payments = _read("olist_payments.csv")
    reviews = _read("olist_reviews.csv")

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        orders[column] = pd.to_datetime(
            orders[column],
            errors="coerce",
        )

    order_items["shipping_limit_date"] = pd.to_datetime(
        order_items["shipping_limit_date"],
        errors="coerce",
    )

    review_dates = [
        "review_creation_date",
        "review_answer_timestamp",
    ]

    for column in review_dates:
        reviews[column] = pd.to_datetime(
            reviews[column],
            errors="coerce",
        )

    orders = orders.dropna(
        subset=[
            "order_id",
            "customer_id",
        ]
    )

    order_items = order_items.dropna(
        subset=[
            "order_id",
            "product_id",
            "price",
        ]
    )

    products["product_category_name"] = (
        products["product_category_name"]
        .fillna("unknown")
    )

    return {
        "customers": customers,
        "sellers": sellers,
        "products": products,
        "orders": orders,
        "order_items": order_items,
        "payments": payments,
        "reviews": reviews,
    }


def get_raw_tables():
    if "raw" not in _cache:
        _cache["raw"] = _load_raw()

    return _cache["raw"]


async def get_full_dataset(
    dataset_id="olist",
    user_id=None,
):
    """
    Return the complete dataset as a Pandas DataFrame.

    Olist is loaded from the local CSV files.

    Custom datasets are loaded once from GridFS and then
    cached in memory for subsequent dashboard requests.
    """

    # -----------------------------------------
    # CUSTOM DATASET
    # -----------------------------------------
    if dataset_id != "olist":
        cache_key = (
            dataset_id,
            user_id,
        )

        if cache_key in _custom_dataset_cache:
            return _custom_dataset_cache[cache_key]

        dataset = await dataset_repository.find_dataset_by_id(
            dataset_id,
            user_id,
        )

        if not dataset:
            raise ValueError("Dataset not found.")

        # Prefer normalized CSV after configuration
        file_id = dataset.get(
            "normalized_file_id"
        )

        # Fall back to original CSV
        if not file_id:
            file_id = dataset.get("file_id")

        if not file_id:
            raise ValueError(
                "Dataset file is not available."
            )

        file_data = (
            await dataset_repository.get_file_from_gridfs(
                file_id
            )
        )

        if not file_data:
            raise ValueError(
                "Unable to read dataset file."
            )

        try:
            df = pd.read_csv(
                io.BytesIO(file_data)
            )
        except Exception as exc:
            raise ValueError(
                f"Unable to load dataset: {str(exc)}"
            )

        # Cache the complete DataFrame
        _custom_dataset_cache[cache_key] = df

        return df

    # -----------------------------------------
    # OLIST DATASET
    # -----------------------------------------
    if "full" in _cache:
        return _cache["full"]

    raw = get_raw_tables()

    df = raw["order_items"]

    df = df.merge(
        raw["orders"],
        on="order_id",
        how="left",
    )

    df = df.merge(
        raw["products"],
        on="product_id",
        how="left",
    )

    df = df.merge(
        raw["sellers"],
        on="seller_id",
        how="left",
    )

    df = df.merge(
        raw["customers"],
        on="customer_id",
        how="left",
    )

    df = df.merge(
        raw["reviews"][
            [
                "order_id",
                "review_score",
            ]
        ],
        on="order_id",
        how="left",
    )

    df = df[
        df["order_status"] != "canceled"
    ].copy()

    df["order_month"] = (
        df["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )

    df["item_total"] = (
        df["price"]
        + df["freight_value"]
    )

    _cache["full"] = df

    return df


def get_payments_with_orders():
    if "payments_full" in _cache:
        return _cache["payments_full"]

    raw = get_raw_tables()

    df = raw["payments"]

    df = df.merge(
        raw["orders"],
        on="order_id",
        how="left",
    )

    df = df[
        df["order_status"] != "canceled"
    ].copy()

    _cache["payments_full"] = df

    return df


def get_reviews_with_orders():
    if "reviews_full" in _cache:
        return _cache["reviews_full"]

    raw = get_raw_tables()

    df = raw["reviews"]

    df = df.merge(
        raw["orders"],
        on="order_id",
        how="left",
    )

    _cache["reviews_full"] = df

    return df


def clear_custom_dataset_cache(
    dataset_id=None,
    user_id=None,
):
    """
    Clear cached custom dataset data.

    If dataset_id and user_id are supplied,
    only that dataset is cleared.
    Otherwise all custom dataset cache is cleared.
    """

    if dataset_id is not None and user_id is not None:
        _custom_dataset_cache.pop(
            (
                dataset_id,
                user_id,
            ),
            None,
        )
        return

    _custom_dataset_cache.clear()