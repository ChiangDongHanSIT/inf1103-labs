from product import Product
from orderLine import OrderLine
from discountStrategy import DiscountStrategy
from noDiscount import NoDiscount

class Order:
    def __init__(
        self, order_id: str, discount: DiscountStrategy | None = None
    ) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = (
            discount if discount is not None else NoDiscount()
        )

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.order_lines:
            if line.get_product().get_product_id() == product_id:
                self.order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)