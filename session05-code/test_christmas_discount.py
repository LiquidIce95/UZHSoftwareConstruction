import pytest
from datetime import date
import christmas_discount

# pytest test cases
def test_christmas_discount():
    discount_obj = christmas_discount.ChristmasDiscount()
    price = 100.0
    
    today = date.today()
    is_christmas = today.month == 12 and today.day == 25

    final_price = discount_obj.apply_discount(price)
    
    if is_christmas:
        assert final_price == 85.0
    else:
        assert final_price == 100.0