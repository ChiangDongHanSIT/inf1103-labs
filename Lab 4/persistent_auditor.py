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

def generate_report():
    print("Current Orders:\n")
    if inventory_list == []:
        print("No current orders.")
    else:
        for item in inventory_list:
            print(f"{item[0]}, {item[1]}, {item[2]}")

def load_inventory():
    global inventory
    global item_id
    if os.path.exists("inventory.txt"):
        with open("inventory.txt", "r") as file:
            for line in file:
                if line.startswith("Total:"):
                    inventory = int(line.strip().split(":")[1])
                else:
                    item_id, product_name, quantity = line.strip().split(",")
                    item_id = int(item_id)
                    quantity = int(quantity)
                    inventory += quantity
                    inventory_list.append((item_id, product_name, quantity))
    else:
        with open("inventory.txt", "w") as file:
            pass 

def save_inventory(item_id, product_name, quantity):
    if os.path.exists("inventory.txt"):
        with open("inventory.txt", "a") as file:
            file.write(f"{item_id},{product_name},{quantity}\n")
    else:
        with open("inventory.txt", "w") as file:
            file.write(f"{item_id},{product_name},{quantity}\n")

def save_total_inventory(inventory):
    with open("inventory.txt", "a") as file:
        file.write(f"Total: {inventory}\n")

load_inventory()

while True:
    generate_report()
    product_name = input("Enter Product Name: ")
    if product_name == "quit":
        generate_report()
        save_total_inventory(inventory)
        break
    else:
        user_input = get_valid_input()
    if user_input == "quit":
        generate_report()
        save_total_inventory(inventory)
        break
    elif user_input == "invalid":
        failed_attempts += 1
        continue
    elif user_input + inventory > 500:
        failed_attempts += 1
        print("Error: Adding this item would exceed the maximum inventory capacity of 500 units.")
        generate_report()
        break
    else:
        inventory = process_delivery(inventory, user_input)
        calculated_tax = calculate_tax(user_input)
        item_id += 1
        inventory_list.append((item_id, product_name, user_input))
        save_inventory(item_id, product_name, user_input)
        print(f"New Order Added:")
        print(f"{item_id}, {product_name}, {user_input}")
        print(f"\nOrder successfully saved to inventory.txt")