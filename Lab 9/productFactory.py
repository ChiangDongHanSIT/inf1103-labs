from product import Product
from physicalProduct import PhysicalProduct
from digitalProduct import DigitalProduct
from supplier import Supplier

class ProductFactory:
    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        weight: float = 0.0,
        download_size: float = 0.0,
    ) -> Product:
        if product_type == "physical":
            return PhysicalProduct(
                product_id, name, price, stock_quantity, supplier, weight
            )
        elif product_type == "digital":
            return DigitalProduct(
                product_id, name, price, stock_quantity, supplier, download_size
            )
        else:
            raise ValueError(f"Unknown product type: {product_type}")