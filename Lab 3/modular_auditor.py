def get_valid_input():
    while True:
        quantity = input("Enter item quantity (or 'quit' to finish): ")
        if quantity == "quit":
            return "quit"
        elif not quantity.isdigit():
            print("Invalid input. Please enter a valid number.")
        else:
            return int(quantity)
        
def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    tax_rate = 0.10
    return amount * tax_rate