from app.repositories.sales_repository import (
    get_dataset,
    get_payments,
    get_reviews,
)

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
    "brinquedos": "Toys",
    "artigos_de_festas": "Party Supplies",
    "moveis_cozinha_area_de_servico_jantar_e_jardim": "Kitchen & Garden Furniture",
}


PAYMENT_TRANSLATIONS = {
    "credit_card": "Credit Card",
    "boleto": "Bank Slip",
    "voucher": "Voucher",
    "debit_card": "Debit Card",
}


def get_kpis():

    df = get_dataset()

    payments = get_payments()

    reviews = get_reviews()

    # Basic totals used in the dashboard
    total_revenue = float(df["item_total"].sum())
    total_orders = int(df["order_id"].nunique())
    total_customers = int(df["customer_id"].nunique())
    total_products = int(df["product_id"].nunique())

    avg_review_score = float(reviews["review_score"].mean())
    avg_payment_value = float(payments["payment_value"].mean())

    # Find which category generated the most revenue
    category_revenue = df.groupby("product_category_name")["item_total"].sum()
    top_category = category_revenue.idxmax()

    seller_revenue = df.groupby("seller_id")["item_total"].sum()
    top_seller = seller_revenue.idxmax()

    payment_counts = payments["payment_type"].value_counts()
    top_payment_method = payment_counts.idxmax()

    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "total_customers": total_customers,
        "total_products": total_products,
        "avg_review_score": round(avg_review_score, 2),
        "avg_payment_value": round(avg_payment_value, 2),
        "top_selling_category": CATEGORY_TRANSLATIONS.get(
            top_category,
            top_category.replace("_", " ").title(),
        ),
        "top_seller": top_seller,
        "top_payment_method": PAYMENT_TRANSLATIONS.get(
            top_payment_method,
            top_payment_method.replace("_", " ").title(),
        ),
    }


def get_recent_orders(limit=10):

    df = get_dataset()

    recent_orders = df.sort_values(
        "order_purchase_timestamp",
        ascending=False,
    )
    recent_orders = recent_orders.drop_duplicates(subset="order_id")
    recent_orders = recent_orders.head(limit)

    records = []
    # Build the final list returned by the API

    for _, row in recent_orders.iterrows():

        records.append(
            # adds in the list created above as separate dictionaries each for one order
            {
                "order_id": row["order_id"],
                "customer_state": row["customer_state"],
                "category": CATEGORY_TRANSLATIONS.get(
                    row["product_category_name"],
                    row["product_category_name"].replace("_", " ").title(),
                ),
                "amount": round(float(row["item_total"]), 2),
                "status": row["order_status"],
                "date": row["order_purchase_timestamp"].strftime("%Y-%m-%d"),
            }
        )

    return records


def get_top_categories_table(limit=10):

    df = get_dataset()

    # Group orders by category so we can compare revenue and order count
    category_summary = df.groupby("product_category_name").agg(
        orders=("order_id", "nunique"),
        revenue=("item_total", "sum"),
    )

    category_summary = category_summary.reset_index()

    # Keep the highest earning categories at the top
    category_summary = category_summary.sort_values(
        "revenue",
        ascending=False,
    )
    category_summary = category_summary.head(limit)

    records = []

    for _, row in category_summary.iterrows():
        records.append(
            {
                "category": CATEGORY_TRANSLATIONS.get(
                    row["product_category_name"],
                    row["product_category_name"].replace("_", " ").title(),
                ),
                "orders": int(row["orders"]),
                "revenue": round(float(row["revenue"]), 2),
            }
        )

    return records
