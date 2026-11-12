from product import Product

class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            print(f"Product ID {product.get_product_id()} already exists. "
                  "Cannot add duplicate.")
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is None:
            print(f"Product ID {product_id} not found. Nothing removed.")
            return None
        self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all_products(self) -> None:
        print("\nCurrent Inventory")
        print("--------------------------------")
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()
        print("--------------------------------")

    def get_products(self) -> list[Product]:
        return list(self.__products)