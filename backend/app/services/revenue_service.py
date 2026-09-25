import numpy as np

import pandas as pd

from app.repositories.sales_repository import get_dataset

CATEGORY_TRANSLATIONS = {
    "beleza_saude": "Beauty & Health",
    "relogios_presentes": "Watches & Gifts",
    "cama_mesa_banho": "Bed, Table & Bath",
    "esporte_lazer": "Sports & Leisure",
    "informatica_acessorios": "Computer Accessories",
    "moveis_decoracao": "Furniture & Decor",
    "utilidades_domesticas": "Home Essentials",
    "cool_stuff": "Cool Stuff",
    "automotivo": "Automotive",
    "ferramentas_jardim": "Garden Tools",
}


async def monthly_revenue(dataset_id="olist", user_id=None):

    df = await get_dataset(
        dataset_id,
        user_id,
    )

    if dataset_id != "olist":
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        monthly_revenue = (
          df.groupby(df["date"].dt.to_period("M"))["revenue"]
            .sum()
            .sort_index()
        )

        return [
            {
                "month": str(month),
                "revenue": round(float(revenue), 2),
            }
                 for month, revenue in monthly_revenue.items()
        ]

    # Add up all sales for each month
    monthly_revenue = df.groupby("order_month")["item_total"].sum()
    monthly_revenue = monthly_revenue.sort_index()

    return [
        {"month": month, "revenue": round(float(revenue), 2)}
        for month, revenue in monthly_revenue.items()
    ]







async def revenue_vs_orders(dataset_id="olist", user_id=None):

    df = await get_dataset(
        dataset_id,
        user_id,
    )

    if dataset_id != "olist":
        if "date" not in df.columns or "revenue" not in df.columns:
            return []

        # Support either the standard BusinessPulse field
        # or an alternative order-count field.
        if "orders" in df.columns:
            orders_column = "orders"
        elif "order_count" in df.columns:
            orders_column = "order_count"
        else:
            return []

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
        )

        df["revenue"] = pd.to_numeric(
            df["revenue"],
            errors="coerce",
        )

        df[orders_column] = pd.to_numeric(
            df[orders_column],
            errors="coerce",
        )

        df = df.dropna(
            subset=["date", "revenue", orders_column]
        )

        if df.empty:
            return []

        monthly_data = (
            df.groupby(df["date"].dt.to_period("M"))
            .agg(
                orders=(orders_column, "sum"),
                revenue=("revenue", "sum"),
            )
            .sort_index()
        )

        return [
            {
                "month": str(month),
                "orders": int(row["orders"]),
                "revenue": round(float(row["revenue"]), 2),
            }
            for month, row in monthly_data.iterrows()
        ]

    # Keep revenue and order count together for each month
    monthly_data = df.groupby("order_month").agg(
        orders=("order_id", "nunique"),
        revenue=("item_total", "sum"),
    )

    monthly_data = monthly_data.sort_index()

    return [
        {
            "month": month,
            "orders": int(row["orders"]),
            "revenue": round(float(row["revenue"]), 2),
        }
        for month, row in monthly_data.iterrows()
    ]
