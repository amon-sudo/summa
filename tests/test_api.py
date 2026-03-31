# test_api.py

import pytest
from app import app, inventory, fetch_product_by_barcode
from unittest.mock import patch

# -------------------------
# API Endpoint Tests
# -------------------------

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_empty_inventory(client):
    inventory.clear()
    res = client.get("/inventory")
    assert res.status_code == 200
    assert res.json == []

def test_add_item(client):
    inventory.clear()
    res = client.post("/inventory", json={"name": "Milk", "brand": "Brookside", "quantity": 5, "price": 100})
    assert res.status_code == 201
    assert res.json["name"] == "Milk"
    assert "id" in res.json

# ... include other CRUD tests here (update, delete, etc.)

# -------------------------
# Mock External API Tests
# -------------------------

def test_fetch_product_success():
    mock_response = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Almonds, Water",
            "categories": "Beverages"
        }
    }
    # Patch requests.get inside fetch_product_by_barcode
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        product = fetch_product_by_barcode("123456789")
        assert product["name"] == "Organic Almond Milk"
        assert product["brand"] == "Silk"

def test_fetch_product_not_found():
    mock_response = {"status": 0}
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        product = fetch_product_by_barcode("000000")
        assert product is None