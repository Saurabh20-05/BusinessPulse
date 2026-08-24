from app.repositories.sales_repository import get_dataset


def monthly_orders():

    df = get_dataset()

    # Count each order only once for every month
    monthly_orders = df.groupby("order_month")["order_id"].nunique()
    monthly_orders = monthly_orders.sort_index()

    return [
        {"month": month, "orders": int(orders)}
        for month, orders in monthly_orders.items()
    ]
