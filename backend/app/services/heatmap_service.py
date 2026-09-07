from app.repositories.sales_repository import (
    get_dataset,
    get_payments,
    get_reviews,
)

import pandas as pd


async def correlation_heatmap(dataset_id="olist", user_id=None):

    df = await get_dataset(
        dataset_id,
        user_id,
    )

    if dataset_id != "olist":
        available_metrics = [
            column
            for column in [
                "revenue",
                "orders",
                "customers",
                "price",
                "review_score",
            ]
            if column in df.columns
        ]

        if len(available_metrics) < 2:
            return {"labels": [], "matrix": []}

        numeric_df = df[available_metrics].apply(
            pd.to_numeric,
            errors="coerce",
        )

        numeric_df = numeric_df.dropna(
            axis=1,
            how="all",
        )

        if len(numeric_df.columns) < 2:
            return {"labels": [], "matrix": []}

        corr = numeric_df.corr().round(2)

        matrix = []

        labels = list(corr.columns)

        for row_label in labels:
            for col_label in labels:
                value = corr.loc[row_label, col_label]

                matrix.append(
                    {
                        "x": col_label,
                        "y": row_label,
                        "value": (
                            float(value)
                            if pd.notna(value)
                            else 0.0
                        ),
                    }
                )

        return {"labels": labels, "matrix": matrix}

    payments = await get_payments(
        dataset_id,
        user_id,
    )

    payments = payments[
        ["order_id", "payment_value", "payment_installments"]
    ]

    reviews = await get_reviews(
        dataset_id,
        user_id,
    )

    reviews = reviews[["order_id", "review_score"]]

    # Combine item data into one row per order
    order_level = df.groupby("order_id").agg(
        price=("price", "sum"),
        freight_value=("freight_value", "sum"),
    )

    order_level = order_level.reset_index()

    merged = order_level.merge(
        payments,
        on="order_id",
        how="left",
    )

    merged = merged.merge(
        reviews,
        on="order_id",
        how="left",
    )

    merged = merged.drop(
        columns=["order_id"]
    ).dropna()

    # Calculate how the selected metrics relate to each other
    corr = merged.corr().round(2)

    matrix = []

    labels = list(corr.columns)

    # Convert the correlation table into points for the heatmap
    for row_label in labels:
        for col_label in labels:
            matrix.append(
                {
                    "x": col_label,
                    "y": row_label,
                    "value": float(
                        corr.loc[row_label, col_label]
                    ),
                }
            )

    return {
        "labels": labels,
        "matrix": matrix,
    }