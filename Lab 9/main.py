import csv
import json
import os

from supplier import Supplier
from physicalProduct import PhysicalProduct
from digitalProduct import DigitalProduct
from productFactory import ProductFactory
from inventory import Inventory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(BASE_DIR, "inventory.json")
PRODUCTS_CSV = os.path.join(BASE_DIR, "products.csv")

# ---------------- Section 5.1 ----------------
def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a number greater than or equal to zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number.")

# ---------------- Section 5.2 ----------------
def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None) 
            loaded = 0
            for row in reader:
                try:
                    product_type = row[0].strip()
                    product_id = row[1].strip()
                    name = row[2].strip()
                    price = float(row[3].strip())
                    stock_quantity = int(row[4].strip())

                    product = ProductFactory.create(
                        product_type,
                        product_id,
                        name,
                        price,
                        stock_quantity,
                        supplier,
                    )
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as e:
                    print(f"Skipping invalid row {row}: {e}")
            print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")

def load_inventory(inventory: Inventory, file_path: str) -> None:
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        for product_id, details in data.items():
            try:
                sup_data = details.get("supplier", {})
                supplier = Supplier(
                    sup_data.get("supplier_id", "S001"),
                    sup_data.get("name", "Default Supplier"),
                    sup_data.get("contact_email", "sales@supplier.com"),
                )
                product = ProductFactory.create(
                    product_type=details.get("product_type", "physical").lower(),
                    product_id=product_id,
                    name=details["product_name"],
                    price=float(details["product_price"]),
                    stock_quantity=int(details["stock_quantity"]),
                    supplier=supplier,
                    weight=float(details.get("weight", 0.0)),
                    download_size=float(details.get("download_size", 0.0)),
                )
                inventory.add_product(product)
            except ValueError as e:
                print(f"Skipping invalid product '{product_id}': {e}")
        print("Inventory loaded successfully from JSON file.")
    except FileNotFoundError:
        print(f"File {file_path} not found. Starting with empty inventory.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}. Starting with empty inventory.")

def save_inventory(inventory: Inventory, file_path: str) -> None:
    data = {}
    for product in inventory.get_products():
        supplier = product.get_supplier()
        entry = {
            "product_name": product.get_name(),
            "product_price": product.get_price(),
            "stock_quantity": product.get_stock(),
            "supplier": {
                "supplier_id": supplier.get_supplier_id(),
                "name": supplier.get_name(),
                "contact_email": supplier.get_contact_email(),
            },
        }
        if isinstance(product, PhysicalProduct):
            entry["product_type"] = "physical"
            entry["weight"] = product.get_weight()
        elif isinstance(product, DigitalProduct):
            entry["product_type"] = "digital"
            entry["download_size"] = product.get_download_size()
        data[product.get_product_id()] = entry

    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print("Inventory saved successfully.")
    except OSError as e:
        print(f"Error saving inventory to {file_path}: {e}")

def display_menu() -> None:
    print("\n1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Load Products from CSV")
    print("6. Save Inventory")
    print("7. Exit")

def main() -> None:
    print("\n====================================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("====================================================")

    default_supplier = Supplier("S001", "SIT", "SIT@sit.singaporetech.edu.sg")
    inventory = Inventory()

    if os.path.exists(INVENTORY_FILE):
        print("inventory.json found.")
        load_inventory(inventory, INVENTORY_FILE)
    else:
        print("No existing inventory found. Starting with default products.")
        inventory.add_product(
            ProductFactory.create(
                "physical", "P001", "Laptop", 1200.00, 15, default_supplier, weight=2.5
            )
        )
        inventory.add_product(
            ProductFactory.create(
                "digital",
                "P002",
                "Antivirus License",
                45.00,
                100,
                default_supplier,
                download_size=250.0,
            )
        )

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == "1":
            inventory.display_all_products()

        elif choice == "2":
            print("\nAdd New Product")
            print("1. Physical Product")
            print("2. Digital Product")
            p_type_choice = input("Select Product Type (1-2): ").strip()

            if p_type_choice not in ["1", "2"]:
                print("Invalid product type option.")
                continue

            product_id = input("Product ID: ").strip()
            if inventory.find_product(product_id) is not None:
                print(f"Product ID {product_id} already exists. Cannot add duplicate.")
                continue

            product_name = input("Product Name: ").strip()
            product_price = get_positive_float("Product Price: ")
            stock_quantity = get_non_negative_int("Stock Quantity: ")

            try:
                if p_type_choice == "1":
                    weight = get_positive_float("Weight (kg): ")
                    product = ProductFactory.create(
                        "physical",
                        product_id,
                        product_name,
                        product_price,
                        stock_quantity,
                        default_supplier,
                        weight=weight,
                    )
                else:
                    download_size = get_positive_float("Download Size (MB): ")
                    product = ProductFactory.create(
                        "digital",
                        product_id,
                        product_name,
                        product_price,
                        stock_quantity,
                        default_supplier,
                        download_size=download_size,
                    )
                inventory.add_product(product)
                print(f"Product '{product_name}' added successfully.")
            except ValueError as e:
                print(f"Could not create product: {e}")

        elif choice == "3":
            print("\nUpdate Stock")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.find_product(product_id)
            if product is None:
                print(f"Product ID {product_id} not found. Cannot update stock.")
                continue
            print("\nProduct Found:")
            product.display_information()
            new_stock = get_non_negative_int("\nNew Stock Quantity: ")
            try:
                product.update_stock(new_stock)
                print("Stock updated successfully.")
            except ValueError as e:
                print(f"Update failed: {e}")

        elif choice == "4":
            print("\nSearch Product")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.find_product(product_id)
            if product is None:
                print(f"Product ID {product_id} not found.")
            else:
                print("\nProduct Found:")
                product.display_information()

        elif choice == "5":
            print("\nLoading products from CSV...")
            load_products(PRODUCTS_CSV, inventory, default_supplier)

        elif choice == "6":
            print("\nSaving inventory...")
            save_inventory(inventory, INVENTORY_FILE)

        elif choice == "7":
            print("\nSaving inventory before exit...")
            save_inventory(inventory, INVENTORY_FILE)
            print("Program terminated.")
            break

        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()