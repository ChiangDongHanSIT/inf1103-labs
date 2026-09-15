inventory = 0
rejected_entries = 0
quantity = input("Enter item quantity (or 'quit' to finish): ")

while quantity != "quit":
    if not quantity.isdigit():
        print("Invalid input. Please enter a valid number.")
        rejected_entries += 1
        quantity = input("Enter item quantity (or 'quit' to finish): ")
    elif inventory + int(quantity) > 500:
        print("Quantity exceeds maximum limit of 500. Entry rejected.")
        rejected_entries += 1
        break
    else:
        inventory += int(quantity)
        print(f"{quantity} added.")
        quantity = input("Enter item quantity (or 'quit' to finish): ")

print(f"Total inventory: {inventory}")
print(f"Rejected entries: {rejected_entries}")