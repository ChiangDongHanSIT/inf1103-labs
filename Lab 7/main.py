import json
import os

from physicalProduct import PhysicalProduct
from digitalProduct import DigitalProduct
from inventory import Inventory

INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")

# ---------------- File handling ----------------
def load_inventory(inventory, file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        for product_id, details in data.items():
            product_type = details.get("product_type", "physical").lower()
            name = details["product_name"]
            price = details["product_price"]
            stock = details["stock_quantity"]

            if product_type == "physical":
                weight = details.get("weight", 0.0)
                product = PhysicalProduct(product_id, name, price, stock, weight)
            elif product_type == "digital":
                download_size = details.get("download_size", 0.0)
                product = DigitalProduct(product_id, name, price, stock, download_size)
            else:
                print(f"Warning: Unknown product type '{product_type}' for ID {product_id}. Skipped.")
                continue

            inventory.add_product(product)
        print("Inventory loaded successfully from JSON file.")
    except FileNotFoundError:
        print(f"File {file_path} not found. Starting with default inventory.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}. Starting with default inventory.")


def save_inventory(inventory, file_path):
    data = {}
    for product in inventory.get_products():
        if isinstance(product, PhysicalProduct):
            data[product.get_product_id()] = {
                "product_type": "physical",
                "product_name": product.get_name(),
                "product_price": product.get_price(),
                "stock_quantity": product.get_stock(),
                "weight": product.get_weight()
            }
        elif isinstance(product, DigitalProduct):
            data[product.get_product_id()] = {
                "product_type": "digital",
                "product_name": product.get_name(),
                "product_price": product.get_price(),
                "stock_quantity": product.get_stock(),
                "download_size": product.get_download_size()
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
    print("INVENTORY MANAGEMENT SYSTEM (Lab 7)")
    print("====================================================")

    inventory = Inventory()

    if os.path.exists(INVENTORY_FILE):
        print("inventory.json found.")
        load_inventory(inventory, INVENTORY_FILE)
    else:
        print("No existing inventory found. Starting with default products.")
        inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5))
        inventory.add_product(DigitalProduct("P002", "Antivirus License", 45.00, 100, 250.0))
        inventory.add_product(PhysicalProduct("P003", "Mouse", 25.50, 40, 0.2))

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == '1':
            inventory.display_all()

        elif choice == '2':
            print("\nAdd New Product")
            print("1. Physical Product")
            print("2. Digital Product")
            p_type_choice = input("Select Product Type (1-2): ").strip()

            if p_type_choice not in ['1', '2']:
                print("Invalid product type option.")
                continue

            product_id = input("Product ID: ").strip()
            if inventory.search_product(product_id) is not None:
                print(f"Product ID {product_id} already exists. Cannot add duplicate.")
                continue

            product_name = input("Product Name: ").strip()
            try:
                product_price = float(input("Product Price: "))
                stock_quantity = int(input("Stock Quantity: "))

                if p_type_choice == '1':
                    weight = float(input("Weight (kg): "))
                    product = PhysicalProduct(product_id, product_name, product_price, stock_quantity, weight)
                else:
                    download_size = float(input("Download Size (MB): "))
                    product = DigitalProduct(product_id, product_name, product_price, stock_quantity, download_size)

                inventory.add_product(product)
                print(f"Product '{product_name}' added successfully.")
            except ValueError:
                print("Invalid numeric value entered. Product creation failed.")

        elif choice == '3':
            print("\nUpdate Stock")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.search_product(product_id)
            if product is None:
                print(f"Product ID {product_id} not found. Cannot update stock.")
                continue
            print("\nProduct Found:")
            product.display_information()
            try:
                new_stock_quantity = int(input("\nNew Stock Quantity: "))
                product.update_stock(new_stock_quantity)
            except ValueError:
                print("Stock quantity must be an integer.")

        elif choice == '4':
            print("\nSearch Product")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.search_product(product_id)
            if product is None:
                print(f"Product ID {product_id} not found.")
            else:
                print("\nProduct Found:")
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

if __name__ == "__main__":
    main()