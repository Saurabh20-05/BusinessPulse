

from app.utils.data_loader import (
    get_full_dataset,
    get_payments_with_orders,
    get_reviews_with_orders,
)


def get_dataset():
    return get_full_dataset()


def get_payments():
    return get_payments_with_orders()


def get_reviews():
    return get_reviews_with_orders()