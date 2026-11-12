from product import Product
from canBeShipped import CanBeShipped
from supplier import Supplier

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def set_weight(self, weight: float) -> None:
        if weight > 0:
            self.__weight = weight

    def display_information(self) -> None:
        super().display_information()
        print(f"  [Type: Physical] Weight: {self.__weight:.2f} kg")
        print(f"  Fulfilment: {self.get_fulfilment_info()}")
        print(f"  Shipping Cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return 5.00 + (self.__weight * 2.00)