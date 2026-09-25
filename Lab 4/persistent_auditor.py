import os

inventory = 0
failed_attempts = 0
item_id = 1000
inventory_list = []

def get_valid_input():
    quantity = input("Enter Quantity: ")
    if quantity == "quit":
        return "quit"
    elif "-" in quantity:
        print("Invalid input. Please enter a positive number.")
        return "invalid"
    elif not quantity.isdigit():
        print("Invalid input. Please enter a valid number.")
        return "invalid"
    else:
        return int(quantity)
        
def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    tax_rate = 0.10
    return amount * tax_rate

def generate_report(total_units,failed_attempts):
    print("\nCurrent Orders:")
    print(f"Total units in inventory: {total_units}")
    print(f"Failed attempts: {failed_attempts}")
    print(f"Total tax collected: ${calculate_tax(total_units):.2f}")

def load_inventory():
    if os.path.exists("inventory.txt"):
        with open("inventory.txt", "r") as file:
            for line in file:
                item_id, product_name, quantity = line.strip().split(",")
                inventory_list.append((int(item_id), product_name, int(quantity)))
    else:
        with open("inventory.txt", "w") as file:
            pass 

def save_inventory(item_id, product_name, quantity):
    with open("inventory.txt", "w") as file:
        for item_id, product_name, quantity in inventory_list:
            file.write(f"{item_id},{product_name},{quantity}\n")

load_inventory()

while True:
    product_name = input("Enter Product Name: ")
    user_input = get_valid_input()
    if user_input == "quit" or product_name == "quit":
        generate_report(inventory, failed_attempts)
        break
    elif user_input == "invalid":
        failed_attempts += 1
        continue
    elif user_input + inventory > 500:
        failed_attempts += 1
        print("Error: Adding this item would exceed the maximum inventory capacity of 500 units.")
        generate_report(inventory, failed_attempts)
        break
    else:
        inventory = process_delivery(inventory, user_input)
        calculated_tax = calculate_tax(user_input)
        item_id += 1
        inventory_list.append((item_id, product_name, user_input))
        save_inventory(item_id, product_name, user_input)
        print(f"New Order Added:\n {item_id}, {product_name}, {user_input}")