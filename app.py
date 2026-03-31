from flask import Flask, request, jsonify
import requests
app = Flask(__name__)

# 🔹 Temporary in-memory storage
inventory = []
current_id = 1

# ✅ GET /inventory → Fetch all items
@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory), 200

# ✅ GET /inventory/<id> → Fetch single item
@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

# ✅ POST /inventory → Add new item
@app.route('/inventory', methods=['POST'])
def add_item():
    global current_id
    data = request.get_json()
    new_item = {
        "id": current_id,
        "name": data.get("name"),
        "brand": data.get("brand"),
        "quantity": data.get("quantity", 0),
        "price": data.get("price", 0)
    }
    inventory.append(new_item)
    current_id += 1
    return jsonify(new_item), 201

# ✅ PATCH /inventory/<id> → Update item
@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    data = request.get_json()
    for item in inventory:
        if item["id"] == item_id:
            item.update(data)
            return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

# ✅ DELETE /inventory/<id> → Remove item
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    for item in inventory:
        if item["id"] == item_id:
            inventory = [i for i in inventory if i["id"] != item_id]
            return jsonify({"message": "Item deleted"}), 200
    return jsonify({"error": "Item not found"}), 404

def fetch_product_by_barcode(barcode):
    """
    Fetch product data from OpenFoodFacts by barcode.
    Returns None if product not found.
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("status") == 1:
            product = data.get("product", {})
            return {
                "name": product.get("product_name"),
                "brand": product.get("brands"),
                "ingredients": product.get("ingredients_text"),
                "category": product.get("categories")
            }
        return None
    except Exception as e:
        print("Error fetching product:", e)
        return None




# GET /external/<barcode>
@app.route('/external/<barcode>', methods=['GET'])
def get_external_product(barcode):
    product = fetch_product_by_barcode(barcode)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

# POST /inventory/from-barcode/<barcode>
@app.route('/inventory/from-barcode/<barcode>', methods=['POST'])
def add_item_from_barcode(barcode):
    global current_id
    product = fetch_product_by_barcode(barcode)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    new_item = {
        "id": current_id,
        "name": product.get("name"),
        "brand": product.get("brand"),
        "ingredients": product.get("ingredients"),
        "category": product.get("category"),
        "quantity": 1,
        "price": 0
    }

    inventory.append(new_item)
    current_id += 1
    return jsonify(new_item), 201


# ▶️ Run the Flask server
if __name__ == "__main__":
    app.run(debug=True)