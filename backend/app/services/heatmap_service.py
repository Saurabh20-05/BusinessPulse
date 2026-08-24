from app.repositories.sales_repository import (
    get_dataset,
    get_payments,
    get_reviews,
)


def correlation_heatmap():

    df = get_dataset()

    payments = get_payments()

    payments = payments[["order_id", "payment_value", "payment_installments"]]

    reviews = get_reviews()

    reviews = reviews[["order_id", "review_score"]]

    # Combine item data into one row per order
    order_level = df.groupby("order_id").agg(
        price=("price", "sum"),
        freight_value=("freight_value", "sum"),
    )

    order_level = order_level.reset_index()

    merged = order_level.merge(payments, on="order_id", how="left")
    merged = merged.merge(reviews, on="order_id", how="left")
    merged = merged.drop(columns=["order_id"]).dropna()

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
                    "value": float(corr.loc[row_label, col_label]),
                }
            )

    return {"labels": labels, "matrix": matrix}
