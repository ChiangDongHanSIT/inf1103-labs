class Product:

    def __init__(self, product):
        self.__product_id = 1000
        self.__product = product
        self.__price = 0.0
        self.__stock = 0

    def update_stock(self, quantity):
        self.__stock += quantity
        print(f"{quantity} has been added to stock.")

    def display_information(self):
        print("Product_ID: {self.__product_id}")
        print("Product Name: {self.__product}")
        print("Product Price: {self.__price}")
        print("Product Stock: {self.__stock}")