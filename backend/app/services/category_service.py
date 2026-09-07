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


async def revenue_by_category(dataset_id="olist", user_id=None):

    df = await get_dataset(
        dataset_id,
        user_id,
    )

    if dataset_id != "olist":
        if "category" not in df.columns:
            return []

        # Use revenue when available.
        # Otherwise, use price as the available sales-value metric.
        if "revenue" in df.columns:
            value_column = "revenue"
        elif "price" in df.columns:
            value_column = "price"
        else:
            return []

        df[value_column] = pd.to_numeric(
            df[value_column],
            errors="coerce",
        )

        df = df.dropna(
            subset=["category", value_column]
        )

        if df.empty:
            return []

        category_revenue = (
            df.groupby("category")[value_column]
            .sum()
            .sort_values(ascending=False)
        )   

        return [
            {
                "category": str(category),
                "revenue": round(float(revenue), 2),
            }
            for category, revenue in category_revenue.items()
        ]

    # Group the sales by category and sort from highest revenue
    category_revenue = df.groupby("product_category_name")["item_total"].sum()
    category_revenue = category_revenue.sort_values(ascending=False)

    return [
        {
            "category": CATEGORY_TRANSLATIONS.get(category, category),
            "revenue": round(float(revenue), 2),
        }
        for category, revenue in category_revenue.items()
    ]






async def top_categories(limit=10, dataset_id="olist", user_id=None):

    # Take only the top categories needed for the dashboard
    data = await revenue_by_category(
        dataset_id,
        user_id,
    )

    return data[:limit]