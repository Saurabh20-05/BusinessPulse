from app.repositories.sales_repository import get_dataset


async def customers_by_state(dataset_id="olist", user_id=None):

    df = await get_dataset(
        dataset_id,
        user_id,
    )

    if dataset_id != "olist":
        if "state" not in df.columns or "customers" not in df.columns:
            return []

        state_counts = (
            df.groupby("state")["customers"]
            .sum()
            .sort_values(ascending=False)
        )

        return [
            {"state": state, "customers": int(customers)}
            for state, customers in state_counts.items()
        ]

    # Count each customer only once before grouping by state
    state_counts = (
        df.drop_duplicates(subset="customer_id")
        .groupby("customer_state")["customer_id"]
        .count()
    )

    state_counts = state_counts.sort_values(ascending=False)

    return [
        {"state": state, "customers": int(customers)}
        for state, customers in state_counts.items()
    ]
