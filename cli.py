import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def list_inventory():
    response = requests.get(f"{BASE_URL}/inventory")
    if response.status_code == 200:
        items = response.json()
        if items:
            for item in items:
                print(f"{item['id']}: {item['name']} | {item.get('brand', '')} | Qty: {item.get('quantity', 0)} | Price: ${item.get('price', 0)}")
        else:
            print("Inventory is empty.")
    else:
        print("Error fetching inventory.")

def add_item():
    name = input("Enter product name: ")
    brand = input("Enter brand: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))
    data = {"name": name, "brand": brand, "quantity": quantity, "price": price}
    response = requests.post(f"{BASE_URL}/inventory", json=data)
    if response.status_code == 201:
        print("Item added:", response.json())
    else:
        print("Error adding item.")

def add_item_by_barcode():
    barcode = input("Enter product barcode: ")
    response = requests.post(f"{BASE_URL}/inventory/from-barcode/{barcode}")
    if response.status_code == 201:
        print("Item added:", response.json())
    else:
        print("Error adding item from barcode:", response.json().get("error"))

def update_item():
    item_id = int(input("Enter item ID to update: "))
    field = input("Enter field to update (name, brand, quantity, price): ")
    value = input("Enter new value: ")
    if field in ["quantity", "price"]:
        value = float(value) if field == "price" else int(value)
    response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json={field: value})
    if response.status_code == 200:
        print("Item updated:", response.json())
    else:
        print("Error updating item:", response.json().get("error"))

def delete_item():
    item_id = int(input("Enter item ID to delete: "))
    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 200:
        print("Item deleted.")
    else:
        print("Error deleting item:", response.json().get("error"))

def main():
    while True:
        print("\nInventory CLI")
        print("1. List inventory")
        print("2. Add item manually")
        print("3. Add item by barcode")
        print("4. Update item")
        print("5. Delete item")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            list_inventory()
        elif choice == "2":
            add_item()
        elif choice == "3":
            add_item_by_barcode()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            print("Exiting CLI.")
            sys.exit()
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()