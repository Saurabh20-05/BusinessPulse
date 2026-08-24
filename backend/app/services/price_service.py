import numpy as np

from app.repositories.sales_repository import get_dataset


def price_distribution(bins=10):

    df = get_dataset()

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
