
import os

import pandas as pd



DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


_cache = {}






def _read(file_name):
    file_path = os.path.join(DATA_DIR, file_name)

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












    orders = orders.dropna(subset=["order_id", "customer_id"])


    order_items = order_items.dropna(
        subset=["order_id", "product_id", "price"]
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












def get_full_dataset():

    if "full" in _cache:
        return _cache["full"]

    

    raw = get_raw_tables()


    df = raw["order_items"]


    df = df.merge(raw["orders"],on="order_id",how="left",)


    df = df.merge(raw["products"],on="product_id",how="left",)


    df = df.merge(raw["sellers"],on="seller_id",how="left",)


    df = df.merge(raw["customers"],on="customer_id",how="left",)


    # REMOVE CANCELLED ORDERES
    df = df[df["order_status"] != "canceled"].copy()


    df["order_month"] = (df["order_purchase_timestamp"].dt.to_period("M").astype(str))


    df["item_total"] = (df["price"] + df["freight_value"])

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


    df = df[df["order_status"] != "canceled"].copy()

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