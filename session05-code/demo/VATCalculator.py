
class VATCalculator:
    def __init__(self, vat_rate_percentage):
        self.vat_rate = vat_rate_percentage / 100
    
    def __call__(self, amount):  # protocol
        return amount + (amount * self.vat_rate)


apply_20_vat = VATCalculator(20)
total = apply_20_vat(100)
print(f"Total amount after VAT applied {total}")

apply_8_vat = VATCalculator(8)
total = apply_8_vat(100)
print(f"Total amount after VAT applied {total}")