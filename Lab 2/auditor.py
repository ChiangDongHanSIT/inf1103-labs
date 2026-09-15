inventory = 0
rejected_entries = 0

while input("Enter stock quantity (or 'quit' to exit): ") != 'quit':
    if input.isdigit():
        quantity = int(input)
        inventory += quantity
    else:
        print("Invalid input. Please enter a valid number.")
        rejected_entries += 1
    if input < 0:
        print("Invalid input. Please enter a non-negative number.")
        rejected_entries += 1
    if input > 500:
        print("Inventory limit exceeded!")
        break
    if input == 'quit':
        break

print(f"Total inventory: {inventory}")
print(f"Rejected entries: {rejected_entries}")