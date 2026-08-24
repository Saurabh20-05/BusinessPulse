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


def revenue_by_category():

    df = get_dataset()

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


def top_categories(limit=10):

    # Take only the top categories needed for the dashboard
    data = revenue_by_category()

    return data[:limit]
