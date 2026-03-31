from flask import Flask, request, jsonify

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

# ▶️ Run the Flask server
if __name__ == "__main__":
    app.run(debug=True)