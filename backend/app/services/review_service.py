from app.repositories.sales_repository import get_reviews


def review_score_distribution():

    reviews = get_reviews()

    # Count each review score so it can be shown in the chart
    review_counts = reviews["review_score"].value_counts().sort_index()

    return [
        {"score": int(score), "count": int(count)}
        for score, count in review_counts.items()
    ]
