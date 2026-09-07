# import pandas as pd

# from app.repositories.sales_repository import (
#     get_dataset,
#     get_payments,
#     get_reviews,
# )

# CATEGORY_TRANSLATIONS = {
#     "beleza_saude": "Beauty & Health",
#     "relogios_presentes": "Watches & Gifts",
#     "cama_mesa_banho": "Bed, Table & Bath",
#     "esporte_lazer": "Sports & Leisure",
#     "informatica_acessorios": "Computer Accessories",
#     "moveis_decoracao": "Furniture & Decor",
#     "utilidades_domesticas": "Home Essentials",
#     "cool_stuff": "Cool Stuff",
#     "automotivo": "Automotive",
#     "ferramentas_jardim": "Garden Tools",
#     "brinquedos": "Toys",
#     "artigos_de_festas": "Party Supplies",
#     "moveis_cozinha_area_de_servico_jantar_e_jardim": "Kitchen & Garden Furniture",
# }


# PAYMENT_TRANSLATIONS = {
#     "credit_card": "Credit Card",
#     "boleto": "Bank Slip",
#     "voucher": "Voucher",
#     "debit_card": "Debit Card",
# }


# async def get_kpis(dataset_id="olist", user_id=None):

#     df = await get_dataset(
#         dataset_id,
#         user_id,
#     )

#     payments = await get_payments(
#         dataset_id,
#         user_id,
#     )

#     reviews = await get_reviews(
#         dataset_id,
#         user_id,
#     )

#     if dataset_id != "olist":

#         total_revenue = float(df["revenue"].sum()) if "revenue" in df.columns else 0.0
#         total_orders = int(df["orders"].sum()) if "orders" in df.columns else 0
#         total_customers = int(df["customers"].sum()) if "customers" in df.columns else 0

#         total_products = (
#             int(df["product_id"].nunique())
#             if "product_id" in df.columns
#             else 0
#         )

#         avg_review_score = (
#             float(reviews["review_score"].mean())
#             if "review_score" in reviews.columns and not reviews.empty
#             else 0.0
#         )

#         avg_payment_value = (
#             float(payments["payment_value"].mean())
#             if "payment_value" in payments.columns and not payments.empty
#             else 0.0
#         )

#         if "category" in df.columns and "revenue" in df.columns:
#             category_revenue = df.groupby("category")["revenue"].sum()

#             top_category = (
#                 category_revenue.idxmax()
#                 if not category_revenue.empty
#                 else "N/A"
#             )
#         else:
#             top_category = "N/A"

#         top_seller = (
#             str(df["seller_id"].value_counts().idxmax())
#             if "seller_id" in df.columns and not df["seller_id"].empty
#             else "N/A"
#         )

#         if "payment_type" in payments.columns and not payments.empty:
#             payment_counts = payments["payment_type"].value_counts()
#             top_payment_method = payment_counts.idxmax()
#         else:
#             top_payment_method = "N/A"

#         return {
#             "total_revenue": round(total_revenue, 2),
#             "total_orders": total_orders,
#             "total_customers": total_customers,
#             "total_products": total_products,
#             "avg_review_score": round(avg_review_score, 2),
#             "avg_payment_value": round(avg_payment_value, 2),
#             "top_selling_category": str(top_category),
#             "top_seller": top_seller,
#             "top_payment_method": PAYMENT_TRANSLATIONS.get(
#                 top_payment_method,
#                 str(top_payment_method).replace("_", " ").title(),
#             ),
#         }

#     # Basic totals used in the dashboard
#     total_revenue = float(df["item_total"].sum())
#     total_orders = int(df["order_id"].nunique())
#     total_customers = int(df["customer_id"].nunique())
#     total_products = int(df["product_id"].nunique())

#     avg_review_score = float(reviews["review_score"].mean())
#     avg_payment_value = float(payments["payment_value"].mean())

#     # Find which category generated the most revenue
#     category_revenue = df.groupby("product_category_name")["item_total"].sum()
#     top_category = category_revenue.idxmax()

#     seller_revenue = df.groupby("seller_id")["item_total"].sum()
#     top_seller = seller_revenue.idxmax()

#     payment_counts = payments["payment_type"].value_counts()
#     top_payment_method = payment_counts.idxmax()

#     return {
#         "total_revenue": round(total_revenue, 2),
#         "total_orders": total_orders,
#         "total_customers": total_customers,
#         "total_products": total_products,
#         "avg_review_score": round(avg_review_score, 2),
#         "avg_payment_value": round(avg_payment_value, 2),
#         "top_selling_category": CATEGORY_TRANSLATIONS.get(
#             top_category,
#             top_category.replace("_", " ").title(),
#         ),
#         "top_seller": top_seller,
#         "top_payment_method": PAYMENT_TRANSLATIONS.get(
#             top_payment_method,
#             top_payment_method.replace("_", " ").title(),
#         ),
#     }


# async def get_recent_orders(
#     limit=10,
#     dataset_id="olist",
#     user_id=None,
# ):

#     df = await get_dataset(
#         dataset_id,
#         user_id,
#     )

#     if dataset_id != "olist":

#         if "date" not in df.columns:
#             return []

#         recent_orders = df.copy()

#         recent_orders["date"] = pd.to_datetime(
#             recent_orders["date"],
#             errors="coerce",
#         )

#         recent_orders = recent_orders.dropna(subset=["date"])
#         recent_orders = recent_orders.sort_values(
#             "date",
#             ascending=False,
#         )
#         recent_orders = recent_orders.head(limit)

#         records = []

#         for index, row in recent_orders.iterrows():

#             records.append(
#                 {
#                     "order_id": (
#                         str(row["order_id"])
#                         if "order_id" in df.columns
#                         else f"custom-{index}"
#                     ),
#                     "customer_state": (
#                         str(row["state"])
#                         if "state" in df.columns
#                         else "N/A"
#                     ),
#                     "category": (
#                         str(row["category"])
#                         if "category" in df.columns
#                         else "N/A"
#                     ),
#                     "amount": (
#                         round(float(row["revenue"]), 2)
#                         if "revenue" in df.columns
#                         else 0.0
#                     ),
#                     "status": (
#                         str(row["status"])
#                         if "status" in df.columns
#                         else "N/A"
#                     ),
#                     "date": row["date"].strftime("%Y-%m-%d"),
#                 }
#             )

#         return records

#     recent_orders = df.sort_values(
#         "order_purchase_timestamp",
#         ascending=False,
#     )
#     recent_orders = recent_orders.drop_duplicates(subset="order_id")
#     recent_orders = recent_orders.head(limit)

#     records = []

#     # Build the final list returned by the API
#     for _, row in recent_orders.iterrows():

#         records.append(
#             {
#                 "order_id": row["order_id"],
#                 "customer_state": row["customer_state"],
#                 "category": CATEGORY_TRANSLATIONS.get(
#                     row["product_category_name"],
#                     row["product_category_name"].replace("_", " ").title(),
#                 ),
#                 "amount": round(float(row["item_total"]), 2),
#                 "status": row["order_status"],
#                 "date": row["order_purchase_timestamp"].strftime("%Y-%m-%d"),
#             }
#         )

#     return records


# async def get_top_categories_table(
#     limit=10,
#     dataset_id="olist",
#     user_id=None,
# ):

#     df = await get_dataset(
#         dataset_id,
#         user_id,
#     )

#     if dataset_id != "olist":

#         if "category" not in df.columns or "revenue" not in df.columns:
#             return []

#         if "orders" in df.columns:
#             category_summary = df.groupby("category").agg(
#                 orders=("orders", "sum"),
#                 revenue=("revenue", "sum"),
#             )
#         else:
#             category_summary = df.groupby("category").agg(
#                 revenue=("revenue", "sum"),
#             )
#             category_summary["orders"] = 0

#         category_summary = category_summary.reset_index()

#         category_summary = category_summary.sort_values(
#             "revenue",
#             ascending=False,
#         )

#         category_summary = category_summary.head(limit)

#         return [
#             {
#                 "category": str(row["category"]),
#                 "orders": int(row["orders"]),
#                 "revenue": round(float(row["revenue"]), 2),
#             }
#             for _, row in category_summary.iterrows()
#         ]

#     # Group orders by category so we can compare revenue and order count
#     category_summary = df.groupby("product_category_name").agg(
#         orders=("order_id", "nunique"),
#         revenue=("item_total", "sum"),
#     )

#     category_summary = category_summary.reset_index()

#     # Keep the highest earning categories at the top
#     category_summary = category_summary.sort_values(
#         "revenue",
#         ascending=False,
#     )
#     category_summary = category_summary.head(limit)

#     records = []

#     for _, row in category_summary.iterrows():
#         records.append(
#             {
#                 "category": CATEGORY_TRANSLATIONS.get(
#                     row["product_category_name"],
#                     row["product_category_name"].replace("_", " ").title(),
#                 ),
#                 "orders": int(row["orders"]),
#                 "revenue": round(float(row["revenue"]), 2),
#             }
#         )

#     return records


import pandas as pd

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


async def get_kpis(dataset_id="olist", user_id=None):
    df = await get_dataset(
        dataset_id,
        user_id,
    )

    payments = await get_payments(
        dataset_id,
        user_id,
    )

    reviews = await get_reviews(
        dataset_id,
        user_id,
    )

    if dataset_id != "olist":
        total_revenue = float(df["revenue"].sum()) if "revenue" in df.columns else 0.0

        total_orders = int(df["orders"].sum()) if "orders" in df.columns else 0

        total_customers = int(df["customers"].sum()) if "customers" in df.columns else 0

        total_products = (
            int(df["product_id"].nunique()) if "product_id" in df.columns else None
        )

        avg_review_score = (
            float(reviews["review_score"].mean())
            if "review_score" in reviews.columns and not reviews.empty
            else None
        )

        avg_payment_value = (
            float(payments["payment_value"].mean())
            if "payment_value" in payments.columns and not payments.empty
            else None
        )

        if "category" in df.columns and "revenue" in df.columns:
            category_revenue = df.groupby("category")["revenue"].sum()

            top_category = (
                category_revenue.idxmax() if not category_revenue.empty else "N/A"
            )
        else:
            top_category = "N/A"

        if "seller_id" in df.columns and not df["seller_id"].dropna().empty:
            top_seller = str(df["seller_id"].value_counts().idxmax())
        else:
            top_seller = "N/A"

        if "payment_type" in payments.columns and not payments.empty:
            payment_counts = payments["payment_type"].value_counts()
            top_payment_method = payment_counts.idxmax()
        elif (
            "payment_channel" in df.columns and not df["payment_channel"].dropna().empty
        ):
            payment_counts = df["payment_channel"].value_counts()
            top_payment_method = payment_counts.idxmax()
        else:
            top_payment_method = "N/A"

        return {
            "total_revenue": round(total_revenue, 2),
            "total_orders": total_orders,
            "total_customers": total_customers,
            "total_products": total_products,
            "avg_review_score": (
                round(avg_review_score, 2) if avg_review_score is not None else None
            ),
            "avg_payment_value": (
                round(avg_payment_value, 2) if avg_payment_value is not None else None
            ),
            "top_selling_category": str(top_category),
            "top_seller": top_seller,
            "top_payment_method": PAYMENT_TRANSLATIONS.get(
                top_payment_method,
                str(top_payment_method).replace("_", " ").title(),
            ),
        }

    total_revenue = float(df["item_total"].sum())
    total_orders = int(df["order_id"].nunique())
    total_customers = int(df["customer_id"].nunique())
    total_products = int(df["product_id"].nunique())

    avg_review_score = float(reviews["review_score"].mean())
    avg_payment_value = float(payments["payment_value"].mean())

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


async def get_recent_orders(
    limit=10,
    dataset_id="olist",
    user_id=None,
):
    df = await get_dataset(
        dataset_id,
        user_id,
    )

    if dataset_id != "olist":
        if "date" not in df.columns:
            return []

        recent_orders = df.copy()

        recent_orders["date"] = pd.to_datetime(
            recent_orders["date"],
            errors="coerce",
        )

        recent_orders = recent_orders.dropna(subset=["date"])

        recent_orders = recent_orders.sort_values(
            "date",
            ascending=False,
        )

        recent_orders = recent_orders.head(limit)

        records = []

        for index, row in recent_orders.iterrows():
            records.append(
                {
                    "order_id": (
                        str(row["order_id"])
                        if "order_id" in df.columns
                        else f"custom-{index}"
                    ),
                    "customer_state": (
                        str(row["state"]) if "state" in df.columns else "N/A"
                    ),
                    "category": (
                        str(row["category"]) if "category" in df.columns else "N/A"
                    ),
                    "amount": (
                        round(float(row["revenue"]), 2)
                        if "revenue" in df.columns
                        else 0.0
                    ),
                    "status": (str(row["status"]) if "status" in df.columns else "N/A"),
                    "date": row["date"].strftime("%Y-%m-%d"),
                }
            )

        return records

    recent_orders = df.sort_values(
        "order_purchase_timestamp",
        ascending=False,
    )

    recent_orders = recent_orders.drop_duplicates(subset="order_id")

    recent_orders = recent_orders.head(limit)

    records = []

    for _, row in recent_orders.iterrows():
        records.append(
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


async def get_top_categories_table(
    limit=10,
    dataset_id="olist",
    user_id=None,
):
    df = await get_dataset(
        dataset_id,
        user_id,
    )

    if dataset_id != "olist":
        if "category" not in df.columns or "revenue" not in df.columns:
            return []

        if "orders" in df.columns:
            category_summary = df.groupby("category").agg(
                orders=("orders", "sum"),
                revenue=("revenue", "sum"),
            )
        else:
            category_summary = df.groupby("category").agg(
                revenue=("revenue", "sum"),
            )

            category_summary["orders"] = 0

        category_summary = category_summary.reset_index()

        category_summary = category_summary.sort_values(
            "revenue",
            ascending=False,
        )

        category_summary = category_summary.head(limit)

        return [
            {
                "category": str(row["category"]),
                "orders": int(row["orders"]),
                "revenue": round(float(row["revenue"]), 2),
            }
            for _, row in category_summary.iterrows()
        ]

    category_summary = df.groupby("product_category_name").agg(
        orders=("order_id", "nunique"),
        revenue=("item_total", "sum"),
    )

    category_summary = category_summary.reset_index()

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
