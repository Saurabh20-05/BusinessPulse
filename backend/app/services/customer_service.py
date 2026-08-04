





from app.repositories.sales_repository import get_dataset



def customers_by_state():

    df = get_dataset()


    state_counts = (df.drop_duplicates(subset="customer_id").groupby("customer_state")["customer_id"].count())

    state_counts = state_counts.sort_values(ascending=False)


    return [
        {"state": state, "customers": int(customers)}
        for state, customers in state_counts.items()
    ]








