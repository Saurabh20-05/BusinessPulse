from app.repositories.sales_repository import get_payments

PAYMENT_TRANSLATIONS = {
    "credit_card": "Credit Card",
    "boleto": "Bank Slip",
    "voucher": "Voucher",
    "debit_card": "Debit Card",
}


async def payment_method_distribution(dataset_id="olist", user_id=None):

    payments = await get_payments(
        dataset_id,
        user_id,
    )

    # Count how often each payment method was used
    payment_counts = payments["payment_type"].value_counts()

    return [
        {
            "payment_type": PAYMENT_TRANSLATIONS.get(payment_type, payment_type),
            "count": int(count),
        }
        for payment_type, count in payment_counts.items()
    ]