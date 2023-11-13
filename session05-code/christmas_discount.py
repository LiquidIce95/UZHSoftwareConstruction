from datetime import date

# The ChristmasDiscount class
class ChristmasDiscount:
    def apply_discount(self, amount: float) -> float:
        today = date.today()
        discount_percentage = 0
        
        is_christmas = today.month == 12 and today.day == 25
        
        if is_christmas:
            discount_percentage = 0.15
        
        return amount - (amount * discount_percentage)

