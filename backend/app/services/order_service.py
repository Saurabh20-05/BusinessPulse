import pandas as pd

from app.repositories.sales_repository import get_dataset


async def monthly_orders(dataset_id="olist", user_id=None):
    df = await get_dataset(
        dataset_id,
        user_id,
    )

    if dataset_id != "olist":
        # Custom datasets must provide the required fields
        # for monthly order analysis.
        if "date" not in df.columns or "orders" not in df.columns:
            return []

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
        )

        df["orders"] = pd.to_numeric(
            df["orders"],
            errors="coerce",
        )

        df = df.dropna(
            subset=["date", "orders"]
        )

        if df.empty:
            return []

        monthly_orders = (
            df.groupby(df["date"].dt.to_period("M"))["orders"]
            .sum()
            .sort_index()
        )

        return [
            {
                "month": str(month),
                "orders": int(orders),
            }
            for month, orders in monthly_orders.items()
        ]

    # Count each order only once for every month
    monthly_orders = (
        df.groupby("order_month")["order_id"]
        .nunique()
    )

    monthly_orders = monthly_orders.sort_index()

    return [
        {
            "month": month,
            "orders": int(orders),
        }
        for month, orders in monthly_orders.items()
    ]
