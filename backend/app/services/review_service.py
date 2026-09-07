from app.repositories.sales_repository import get_reviews


async def review_score_distribution(dataset_id="olist", user_id=None):

    reviews = await get_reviews(
        dataset_id,
        user_id,
    )

    if dataset_id != "olist":
        if "review_score" not in reviews.columns:
            return []

    # Count each review score so it can be shown in the chart
    review_counts = reviews["review_score"].value_counts().sort_index()

    return [
        {"score": int(score), "count": int(count)}
        for score, count in review_counts.items()
    ]