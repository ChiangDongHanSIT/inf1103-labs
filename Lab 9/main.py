import json
import os

from supplier import Supplier
from product import Product
from physicalProduct import PhysicalProduct
from digitalProduct import DigitalProduct
from inventory import Inventory
from order import Order

INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")
UNKNOWN_SUPPLIER_ID = "S000"

def load_inventory(inventory: Inventory, suppliers: dict[str, Supplier],
                   file_path: str) -> None:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        for product_id, details in data.items():
            product_type = details.get("product_type", "physical").lower()
            name = details["product_name"]
            price = details["product_price"]
            stock = details["stock_quantity"]
            supplier_id = details.get("supplier_id", UNKNOWN_SUPPLIER_ID)
            if supplier_id not in suppliers:
                suppliers[supplier_id] = Supplier(
                    supplier_id,
                    details.get("supplier_name", "Unknown Supplier"),
                    details.get("supplier_email", "unknown@example.com"))
            supplier = suppliers[supplier_id]

            if product_type == "physical":
                weight = details.get("weight", 0.0)
                product: Product = PhysicalProduct(product_id, name, price, stock,
                                                   supplier, weight)
            elif product_type == "digital":
                download_size = details.get("download_size", 0.0)
                product = DigitalProduct(product_id, name, price, stock,
                                         supplier, download_size)
            else:
                print(f"Warning: Unknown product type '{product_type}' for ID {product_id}. Skipped.")
                continue

            inventory.add_product(product)
        print("Inventory loaded successfully from JSON file.")
    except FileNotFoundError:
        print(f"File {file_path} not found. Starting with default inventory.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}. Starting with default inventory.")

def save_inventory(inventory: Inventory, file_path: str) -> None:
    data: dict[str, dict] = {}
    for product in inventory.get_products():
        supplier = product.get_supplier()
        record = {
            "product_name": product.get_name(),
            "product_price": product.get_price(),
            "stock_quantity": product.get_stock(),
            "supplier_id": supplier.get_supplier_id(),
            "supplier_name": supplier.get_name(),
            "supplier_email": supplier.get_contact_email(),
        }
        if isinstance(product, PhysicalProduct):
            record["product_type"] = "physical"
            record["weight"] = product.get_weight()
        elif isinstance(product, DigitalProduct):
            record["product_type"] = "digital"
            record["download_size"] = product.get_download_size()
        else:
            continue
        data[product.get_product_id()] = record
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print("Inventory saved successfully.")
    except Exception as e:
        print(f"Error saving inventory to {file_path}: {e}")

def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier:
    if suppliers:
        print("Known suppliers:")
        for supplier in suppliers.values():
            supplier.display_information()
    supplier_id = input("Supplier ID: ").strip()
    if supplier_id in suppliers:
        return suppliers[supplier_id]
    name = input("New supplier name: ").strip()
    email = input("New supplier contact email: ").strip()
    suppliers[supplier_id] = Supplier(supplier_id, name, email)
    return suppliers[supplier_id]

def display_menu() -> None:
    print("\n1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Create Order")
    print("7. Save Inventory")
    print("8. Exit")

def create_order(inventory: Inventory, order_count: int) -> Order | None:
    order = Order(f"O{order_count:03d}")
    print(f"\nCreating order {order.get_order_id()} (blank product ID to finish)")
    while True:
        product_id = input("Product ID: ").strip()
        if product_id == "":
            break
        product = inventory.find_product(product_id)
        if product is None:
            print(f"Product ID {product_id} not found.")
            continue
        try:
            quantity = int(input("Quantity: "))
        except ValueError:
            print("Quantity must be an integer.")
            continue
        order.add_order_line(product, quantity)
    if not order.get_order_lines():
        print("Order has no lines. Order discarded.")
        return None
    order.display_order()
    return order

def main() -> None:
    print("\n====================================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("====================================================")

    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}
    orders: list[Order] = []

    if os.path.exists(INVENTORY_FILE):
        print("inventory.json found.")
        load_inventory(inventory, suppliers, INVENTORY_FILE)
    else:
        print("No existing inventory found. Starting with default products.")
        hardwareSupplier = Supplier("S001", "Hardware Supplier", "hardwareSupplier@email.com")
        softwareSupplier = Supplier("S002", "Software Supplier", "softwareSupplier@email.com")
        suppliers[hardwareSupplier.get_supplier_id()] = hardwareSupplier
        suppliers[softwareSupplier.get_supplier_id()] = softwareSupplier
        inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, hardwareSupplier, 2.5))
        inventory.add_product(DigitalProduct("P002", "Antivirus License", 45.00, 100, softwareSupplier, 250.0))
        inventory.add_product(PhysicalProduct("P003", "Mouse", 25.50, 40, hardwareSupplier, 0.2))

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-8): ").strip()

        if choice == '1':
            inventory.display_all_products()

        elif choice == '2':
            print("\nAdd New Product")
            print("1. Physical Product")
            print("2. Digital Product")
            p_type_choice = input("Select Product Type (1-2): ").strip()

            if p_type_choice not in ['1', '2']:
                print("Invalid product type option.")
                continue

            product_id = input("Product ID: ").strip()
            if inventory.find_product(product_id) is not None:
                print(f"Product ID {product_id} already exists. Cannot add duplicate.")
                continue

            product_name = input("Product Name: ").strip()
            try:
                product_price = float(input("Product Price: "))
                stock_quantity = int(input("Stock Quantity: "))
                if p_type_choice == '1':
                    weight = float(input("Weight (kg): "))
                else:
                    download_size = float(input("Download Size (MB): "))
            except ValueError:
                print("Invalid numeric value entered. Product creation failed.")
                continue

            supplier = choose_supplier(suppliers)
            if p_type_choice == '1':
                product = PhysicalProduct(product_id, product_name, product_price,
                                          stock_quantity, supplier, weight)
            else:
                product = DigitalProduct(product_id, product_name, product_price,
                                         stock_quantity, supplier, download_size)

            inventory.add_product(product)
            print(f"Product '{product_name}' added successfully.")

        elif choice == '3':
            print("\nUpdate Stock")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.find_product(product_id)
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
            product = inventory.find_product(product_id)
            if product is None:
                print(f"Product ID {product_id} not found.")
            else:
                print("\nProduct Found:")
                product.display_information()

        elif choice == '5':
            print("\nRemove Product")
            product_id = input("Enter Product ID: ").strip()
            removed = inventory.remove_product(product_id)
            if removed is not None:
                print(f"Product '{removed.get_name()}' removed from inventory "
                      "(the product object still exists).")

        elif choice == '6':
            order = create_order(inventory, len(orders) + 1)
            if order is not None:
                orders.append(order)

        elif choice == '7':
            print("\nSaving inventory...")
            save_inventory(inventory, INVENTORY_FILE)

        elif choice == '8':
            print("\nSaving inventory before exit...")
            save_inventory(inventory, INVENTORY_FILE)
            print("\nThank you for using the Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("\nInvalid choice. Please try again.")
main()