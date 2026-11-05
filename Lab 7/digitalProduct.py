from product import Product

class DigitalProduct(Product):

    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def set_download_size(self, download_size: float):
        if download_size > 0:
            self.__download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"  [Type: Digital] Download Size: {self.__download_size:.2f} MB")
        print(f"  Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via instant download link."