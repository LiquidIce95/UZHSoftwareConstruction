import pytest
from datetime import date
import christmas_discount_testable

# pytest test cases
def test_christmas_discount():
    discount_obj = christmas_discount_testable.ChristmasDiscount()
    price = 100.0

    d = date(2023,12,25)
    final_price = discount_obj.apply_discount(price,d)

    assert final_price == 85.0

def test_christmas_no_discount():
    discount_obj = christmas_discount_testable.ChristmasDiscount()
    price = 100.0

    day = date(2023,12,24)
    final_price = discount_obj.apply_discount(price,day)

    assert final_price == 100.0