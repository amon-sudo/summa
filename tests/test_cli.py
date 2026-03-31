import pytest
from unittest.mock import patch
import cli
import builtins

# -------------------------
# Helper: simulate input
# -------------------------
def simulate_inputs(inputs):
    """Patch builtins.input to simulate multiple user inputs."""
    input_iter = iter(inputs)
    return patch("builtins.input", lambda _: next(input_iter))

# -------------------------
# Test View All Items
# -------------------------
@patch("requests.get")
def test_get_all_items(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"id": 1, "name": "Milk", "brand": "Brookside", "quantity": 5, "price": 100}
    ]
    cli.get_all_items()  # Should print the inventory list

# -------------------------
# Test Add New Item
# -------------------------
@patch("requests.post")
def test_add_item(mock_post):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {"id": 1, "name": "Milk"}

    inputs = ["Milk", "Brookside", "5", "100"]
    with simulate_inputs(inputs):
        cli.add_item()  # Should call POST and print success

# -------------------------
# Test Update Item
# -------------------------
@patch("requests.patch")
def test_update_item(mock_patch):
    mock_patch.return_value.status_code = 200
    mock_patch.return_value.json.return_value = {"id": 1, "quantity": 10}

    inputs = ["1", "10", ""]  # Update quantity only
    with simulate_inputs(inputs):
        cli.update_item()  # Should call PATCH and print updated item

# -------------------------
# Test Delete Item
# -------------------------
@patch("requests.delete")
def test_delete_item(mock_delete):
    mock_delete.return_value.status_code = 200
    mock_delete.return_value.json.return_value = {"message": "Item deleted"}

    inputs = ["1"]
    with simulate_inputs(inputs):
        cli.delete_item()  # Should call DELETE and print message

# -------------------------
# Test Add Item from Barcode
# -------------------------
@patch("requests.get")
@patch("requests.post")
def test_add_item_from_barcode(mock_post, mock_get):
    # Mock GET /external/<barcode>
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "ingredients": "Almonds, Water",
        "category": "Beverages"
    }

    # Mock POST /inventory/from-barcode/<barcode>
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {"id": 1, "name": "Organic Almond Milk"}

    inputs = ["123456789", "y"]  # Barcode + confirm 'y'
    with simulate_inputs(inputs):
        cli.add_item_from_barcode()  # Should fetch and add the product