from decimal import Decimal

def total_amount(base_amount: int, rate: Decimal):
    return round(base_amount * rate / 100, 2)
