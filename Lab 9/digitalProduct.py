from product import Product
from supplier import Supplier

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def set_download_size(self, download_size: float) -> None:
        if download_size > 0:
            self.__download_size = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"  [Type: Digital] Download Size: {self.__download_size:.2f} MB")
        print(f"  Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via instant download link."