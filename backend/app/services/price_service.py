import numpy as np

from app.repositories.sales_repository import get_dataset


async def price_distribution(
    bins=10,
    dataset_id="olist",
    user_id=None,
):

    df = await get_dataset(
        dataset_id,
        user_id,
    )

    if dataset_id != "olist":
        if "price" not in df.columns:
            return []

    prices = df["price"].dropna()

    # Split the prices into ranges and count how many fall in each
    hist, edges = np.histogram(prices, bins=bins)

    price_data = []

    # Convert the histogram into the format used by the API
    for i in range(len(hist)):

        price_data.append(
            {
                "range": f"{int(edges[i])}-{int(edges[i + 1])}",
                "count": int(hist[i]),
            }
        )

    return price_data