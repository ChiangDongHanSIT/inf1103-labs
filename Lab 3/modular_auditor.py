def get_valid_input():
    inventory = 0
    failed_entries = 0
    while True:
        quantity = input("Enter item quantity (or 'quit' to finish): ")
        if quantity == "quit":
            return inventory, failed_entries
        elif not quantity.isdigit():
            failed_entries += 1
            print("Invalid input. Please enter a valid number.")
        elif inventory + int(quantity) > 500:
            failed_entries += 1
            print("Quantity exceeds maximum limit of 500. Entry rejected.")
        else:
            inventory += int(quantity)

inventory, failed_entries = get_valid_input()

print(f"Total inventory: {inventory}")
print(f"Failed entries: {failed_entries}")