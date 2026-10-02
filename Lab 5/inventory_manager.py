import json

inventory_items = {
    "P001": {"product_name": "Laptop", "product_price": 1200.00, "stock_quantity": 15},
    "P002": {"product_name": "Mouse", "product_price": 25.50, "stock_quantity": 40},
    "P003": {"product_name": "Keyboard", "product_price": 45.00, "stock_quantity": 25}
}

def add_product(product_id, product_name, product_price, stock_quantity):
    if product_id in inventory_items:
        print(f"Product ID {product_id} already exists. Cannot add duplicate.")
    else:
        inventory_items[product_id] = {
            "product_name": product_name,
            "product_price": product_price,
            "stock_quantity": stock_quantity
        }
        print("Product added successfully!")

def update_stock(product_id, new_stock_quantity):
    if product_id in inventory_items:
        inventory_items[product_id]["stock_quantity"] = new_stock_quantity
        print("Stock updated successfully!")
    else:
        print(f"Product ID {product_id} not found. Cannot update stock.")

def search_product(product_id):
    if product_id in inventory_items:
        product = inventory_items[product_id]
        print("Product Found")
        print("----------------")
        print(f"ID: {product_id}")
        print(f"Name: {product['product_name']}")
        print(f"Price: ${product['product_price']:.2f}")
        print(f"Stock: {product['stock_quantity']}")
        print("----------------")
    else:
        print(f"Product ID {product_id} not found.")

def display_all():
    print("Current Inventory")
    print("----------------")
    for product_id, product in inventory_items.items():
        print(f"ID: {product_id}| Name: {product['product_name']} | Price: ${product['product_price']:.2f} | Stock: {product['stock_quantity']}")
    print("----------------")

def load_inventory(file_path):
    global inventory_items
    try:
        with open(file_path, 'r') as file:
            inventory_items = json.load(file)
        print("Inventory loaded successfully from JSON file.")
    except FileNotFoundError:
        print(f"File {file_path} not found. Starting with an empty inventory.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}. Starting with an empty inventory.")

def save_inventory(file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(inventory_items, file, indent=4)
        print("Inventory saved successfully to JSON file.")
    except Exception as e:
        print(f"Error saving inventory to {file_path}: {e}")

def main():
    load_inventory("inventory.json")
    while True:
        print("====================================================")
        print("INVENTORY MANAGEMENT SYSTEM")
        print("====================================================")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            display_all()
        elif choice == '2':
            print("Add New Product")
            product_id = input("Product ID: ")
            product_name = input("Product Name: ")
            product_price = float(input("Product Price: "))
            stock_quantity = int(input("Stock Quantity: "))
            add_product(product_id, product_name, product_price, stock_quantity)
            print("Product added successfully!")
        elif choice == '3':
            print("Update Stock")
            product_id = input("Enter Product ID to update stock: ")
            new_stock_quantity = int(input("New Stock Quantity: "))
            update_stock(product_id, new_stock_quantity)
            print("Stock updated successfully!")
        elif choice == '4':
            print("Search Product")
            product_id = input("Enter Product ID: ")
            search_product(product_id)
        elif choice == '5':
            print("Saving inventory...")
            save_inventory("inventory.json")
            print("Inventory saved successfully to inventory.json.")
        elif choice == '6':
            print("Saving inventory before exit...")
            save_inventory("inventory.json")
            print("Inventory saved successfully.")
            print("Thank you for using the Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid choice. Please try again.")