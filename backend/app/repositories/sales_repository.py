from app.utils.data_loader import (
    get_full_dataset,
    get_payments_with_orders,
    get_reviews_with_orders,
)


def get_dataset():
    """
    Returns the complete business dataset.
    """
    return get_full_dataset()


def get_payments():
    """
    Returns the payments dataset joined with orders.
    """
    return get_payments_with_orders()


def get_reviews():
    """
    Returns the reviews dataset joined with orders.
    """
    return get_reviews_with_orders()