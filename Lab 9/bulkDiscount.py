from discountStrategy import DiscountStrategy

class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        self.threshold: float = threshold
        self.amount: float = amount

    def apply(self, total: float) -> float:
        return total - self.amount if total >= self.threshold else total