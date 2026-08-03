


import numpy as np



from app.utils.data_loader import (
    get_full_dataset,
    get_payments_with_orders,
    get_reviews_with_orders,
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
}






PAYMENT_TRANSLATIONS = {
    "credit_card": "Credit Card",
    "boleto": "Bank Slip",
    "voucher": "Voucher",
    "debit_card": "Debit Card",
}










def monthly_revenue():

    df = get_full_dataset()

    # CREATE monthly_revenue where we store
    monthly_revenue = df.groupby("order_month")["item_total"].sum()
    monthly_revenue = monthly_revenue.sort_index()



    return [
        {"month": month, "revenue": round(float(revenue), 2)}
        for month, revenue in monthly_revenue.items()
    ]







def monthly_orders():

    df = get_full_dataset()

    monthly_orders = df.groupby("order_month")["order_id"].nunique()
    monthly_orders = monthly_orders.sort_index()

    return [
        {"month": month, "orders": int(orders)}
        for month, orders in monthly_orders.items()
    ]







def revenue_by_category():

    df = get_full_dataset()

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

    data = revenue_by_category()

    return data[:limit]











def payment_method_distribution():

    payments = get_payments_with_orders()

    payment_counts = payments["payment_type"].value_counts()


    return [
        {"payment_type": PAYMENT_TRANSLATIONS.get(payment_type, payment_type), "count": int(count)}
        for payment_type, count in payment_counts.items()
    ]









def customers_by_state():

    df = get_full_dataset()


    state_counts = (df.drop_duplicates(subset="customer_id").groupby("customer_state")["customer_id"].count())

    state_counts = state_counts.sort_values(ascending=False)


    return [
        {"state": state, "customers": int(customers)}
        for state, customers in state_counts.items()
    ]













def review_score_distribution():

    reviews = get_reviews_with_orders()

    review_counts = reviews["review_score"].value_counts().sort_index()


    return [
        {"score": int(score), "count": int(count)}
        for score, count in review_counts.items()
    ]










def price_distribution(bins=10):

    df = get_full_dataset()

    prices = df["price"].dropna()

    hist, edges = np.histogram(prices, bins=bins)



    price_data = []

    for i in range(len(hist)):

        price_data.append(

            {
                "range": f"{int(edges[i])}-{int(edges[i + 1])}",
                "count": int(hist[i]),
            }
        )


    return price_data











def revenue_vs_orders():

    df = get_full_dataset()


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




































































































def correlation_heatmap():

    df = get_full_dataset()


    payments = get_payments_with_orders()

    payments = payments[
        ["order_id", "payment_value", "payment_installments"]
    ]


    reviews = get_reviews_with_orders()

    reviews = reviews[
        ["order_id", "review_score"]
    ]



    order_level = df.groupby("order_id").agg(price=("price", "sum"),freight_value=("freight_value", "sum"),)


    order_level = order_level.reset_index()


    merged = order_level.merge(payments, on="order_id", how="left")
    merged = merged.merge(reviews, on="order_id", how="left")
    merged = merged.drop(columns=["order_id"]).dropna()


    corr = merged.corr().round(2)


    matrix = []

    labels = list(corr.columns)



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