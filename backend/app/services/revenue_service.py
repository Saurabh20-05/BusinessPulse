


import numpy as np

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

















def monthly_revenue():


    df = get_dataset()
    # CREATE monthly_revenue where we store
    monthly_revenue = df.groupby("order_month")["item_total"].sum()
    monthly_revenue = monthly_revenue.sort_index()



    return [
        {"month": month, "revenue": round(float(revenue), 2)}
        for month, revenue in monthly_revenue.items()
    ]












def revenue_vs_orders():

    df = get_dataset()


    monthly_data = df.groupby("order_month").agg(orders=("order_id", "nunique"),revenue=("item_total", "sum"),)
    monthly_data = monthly_data.sort_index()


    return [
        {
            "month": month,
            "orders": int(row["orders"]),
            "revenue": round(float(row["revenue"]), 2),
        }

        for month, row in monthly_data.iterrows()
    ]






