import json
import os

from product import Product
from inventory import Inventory

INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")

# ---------------- File handling ----------------
def load_inventory(inventory, file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        for product_id, details in data.items():
            product = Product(product_id,
                              details["product_name"],
                              details["product_price"],
                              details["stock_quantity"])
            inventory.add_product(product)
        print("Inventory loaded successfully from JSON file.")
    except FileNotFoundError:
        print(f"File {file_path} not found. Starting with an empty inventory.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}. Starting with an empty inventory.")


def save_inventory(inventory, file_path):
    data = {}
    for product in inventory.get_products():
        data[product.get_product_id()] = {
            "product_name": product.get_name(),
            "product_price": product.get_price(),
            "stock_quantity": product.get_stock()
        }
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print("Inventory saved successfully.")
    except Exception as e:
        print(f"Error saving inventory to {file_path}: {e}")


# ---------------- Menu ----------------
def display_menu():
    print("\n1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")


def main():
    print("\n====================================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("====================================================")

    # Main program creates the inventory and the starting products
    inventory = Inventory()
    if os.path.exists(INVENTORY_FILE):
        print("inventory.json found.")
        load_inventory(inventory, INVENTORY_FILE)
    else:
        print("No existing inventory found. Starting with default products.")
        inventory.add_product(Product("P001", "Laptop", 1200.00, 15))
        inventory.add_product(Product("P002", "Mouse", 25.50, 40))
        inventory.add_product(Product("P003", "Keyboard", 45.00, 25))

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            inventory.display_all()

        elif choice == '2':
            print("\nAdd New Product")
            product_id = input("Product ID: ")
            product_name = input("Product Name: ")
            product_price = float(input("Product Price: "))
            stock_quantity = int(input("Stock Quantity: "))
            product = Product(product_id, product_name, product_price, stock_quantity)
            inventory.add_product(product)

        elif choice == '3':
            print("\nUpdate Stock")
            product_id = input("Enter Product ID: ")
            product = inventory.search_product(product_id)
            if product is None:
                print(f"Product ID {product_id} not found. Cannot update stock.")
                continue
            print("\nProduct Found:")
            product.display_information()
            new_stock_quantity = int(input("\nNew Stock Quantity: "))
            product.update_stock(new_stock_quantity)

        elif choice == '4':
            print("\nSearch Product")
            product_id = input("Enter Product ID: ")
            product = inventory.search_product(product_id)
            if product is None:
                print(f"Product ID {product_id} not found.")
            else:
                print("\nProduct Found")
                product.display_information()

        elif choice == '5':
            print("\nSaving inventory...")
            save_inventory(inventory, INVENTORY_FILE)

        elif choice == '6':
            print("\nSaving inventory before exit...")
            save_inventory(inventory, INVENTORY_FILE)
            print("\nThank you for using the Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("\nInvalid choice. Please try again.")

main()