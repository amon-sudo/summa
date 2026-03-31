import requests
print(requests.__version__)

BASE_URL = "http://127.0.0.1:5000"

def print_menu():
    print("\n--- Inventory CLI ---")
    print("1. View all items")
    print("2. Add new item")
    print("3. Update item")
    print("4. Delete item")
    print("5. Find/Add item from OpenFoodFacts barcode")
    print("6. Exit")

# ---------------------
# View all items
# ---------------------
def get_all_items():
    res = requests.get(f"{BASE_URL}/inventory")
    if res.status_code == 200:
        items = res.json()
        if not items:
            print("Inventory is empty.")
        else:
            for item in items:
                print(item)
    else:
        print("Error fetching inventory.")

# ---------------------
# Add new item manually
# ---------------------
def add_item():
    name = input("Enter product name: ")
    brand = input("Enter brand: ")
    try:
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price: "))
    except ValueError:
        print("Invalid input for quantity or price.")
        return

    payload = {"name": name, "brand": brand, "quantity": quantity, "price": price}
    res = requests.post(f"{BASE_URL}/inventory", json=payload)
    if res.status_code == 201:
        print("Item added:", res.json())
    else:
        print("Error adding item.")

# ---------------------
# Update item
# ---------------------
def update_item():
    try:
        item_id = int(input("Enter item ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    updates = {}
    quantity = input("Enter new quantity (leave blank to skip): ")
    price = input("Enter new price (leave blank to skip): ")
    
    if quantity:
        try:
            updates["quantity"] = int(quantity)
        except ValueError:
            print("Invalid quantity.")
            return
    if price:
        try:
            updates["price"] = float(price)
        except ValueError:
            print("Invalid price.")
            return

    if not updates:
        print("Nothing to update.")
        return

    res = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=updates)
    if res.status_code == 200:
        print("Item updated:", res.json())
    else:
        print(res.json()["error"])

# ---------------------
# Delete item
# ---------------------
def delete_item():
    try:
        item_id = int(input("Enter item ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    res = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    if res.status_code == 200:
        print(res.json()["message"])
    else:
        print(res.json()["error"])

# ---------------------
# Find/Add item from barcode
# ---------------------
def add_item_from_barcode():
    barcode = input("Enter barcode: ")
    # Fetch product info
    res = requests.get(f"{BASE_URL}/external/{barcode}")
    if res.status_code == 200:
        product = res.json()
        print("Product found:", product)
        confirm = input("Add to inventory? (y/n): ").lower()
        if confirm == 'y':
            res_add = requests.post(f"{BASE_URL}/inventory/from-barcode/{barcode}")
            if res_add.status_code == 201:
                print("Product added:", res_add.json())
            else:
                print("Error adding product:", res_add.json())
    else:
        print("Product not found.")

# ---------------------
# CLI Loop
# ---------------------
def main():
    while True:
        print_menu()
        choice = input("Enter choice: ")
        if choice == "1":
            get_all_items()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            add_item_from_barcode()
        elif choice == "6":
            print("Exiting CLI.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()