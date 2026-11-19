from discountStrategy import DiscountStrategy

class StudentDiscount(DiscountStrategy):
    def __init__(self, percentage: float = 5.0) -> None:
        self.percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)