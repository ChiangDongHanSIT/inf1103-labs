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

