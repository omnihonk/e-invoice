import pytest
from fastapi.testclient import TestClient

from schemas.schemas import BuyerCreate, SellerCreate

_MINIMAL_SELLER = {
    "name": "Acme Seller GmbH",
    "post_code": "54321",
    "city_name": "Berlin",
    "country_id": "DE",
    "tax_id": "DE123456789",
}

_BUYER_BMW = {
    "name": "BMW AG Group",
    "post_code": "80333",
    "city_name": "Munich",
    "country_id": "DE",
    "global_id": "GLN-BMW-789",
    "party_id": "BMW-123"
}

_BUYER_VW = {
    "name": "Volkswagen AG",
    "post_code": "38440",
    "city_name": "Wolfsburg",
    "country_id": "DE",
    "global_id": "GLN-VW-555",
    "party_id": "VW-999"
}

_SAMPLE_ITEMS = [
    {
        "name": "Industrial Gear A",
        "quantity": 10.0,
        "price": 12.50,
        "unit_code": "C62",
    }
]

class TestOrderQueryAndFields:

    def test_invoice_order_persists_buyer_fields(self, db_client: TestClient):
        # 1. Start a fresh session
        resp = db_client.post("/session/start")
        assert resp.status_code == 200
        session_id = resp.json()["session_id"]

        # 2. Update seller, buyer, and items
        db_client.post(f"/session/{session_id}/seller", json=_MINIMAL_SELLER)
        db_client.post(f"/session/{session_id}/buyer", json=_BUYER_BMW)
        db_client.post(f"/session/{session_id}/items", json=_SAMPLE_ITEMS)

        # 3. Generate invoice and capture order number
        gen_resp = db_client.post(f"/session/{session_id}/generate")
        assert gen_resp.status_code == 200
        order_number = gen_resp.headers.get("X-Order-Number")
        assert order_number is not None

        # 4. Fetch details via GET /orders/{order_number} and assert fields
        details_resp = db_client.get(f"/orders/{order_number}")
        assert details_resp.status_code == 200
        details = details_resp.json()
        assert details["buyer_name"] == "BMW AG Group"
        assert details["buyer_id"] == "GLN-BMW-789"  # global_id takes precedence

    def test_orders_filtering_by_buyer_name(self, db_client: TestClient):
        # 1. Create a BMW invoice order
        resp1 = db_client.post("/session/start")
        sid1 = resp1.json()["session_id"]
        db_client.post(f"/session/{sid1}/seller", json=_MINIMAL_SELLER)
        db_client.post(f"/session/{sid1}/buyer", json=_BUYER_BMW)
        db_client.post(f"/session/{sid1}/items", json=_SAMPLE_ITEMS)
        db_client.post(f"/session/{sid1}/generate")

        # 2. Query orders: should contain BMW
        list_resp = db_client.get("/orders")
        assert list_resp.status_code == 200
        items_all = list_resp.json()
        assert len(items_all) >= 1
        assert any(x["buyer_name"] == "BMW AG Group" for x in items_all)

        # 3. Filter by buyer_name=BMW
        res_filtered = db_client.get("/orders?buyer_name=BMW")
        assert res_filtered.status_code == 200
        items_filtered = res_filtered.json()
        assert len(items_filtered) >= 1
        assert items_filtered[0]["buyer_name"] == "BMW AG Group"
        assert items_filtered[0]["buyer_id"] == "GLN-BMW-789"

        # 4. Filter by buyer_name=Mercedes (non-existent)
        res_empty = db_client.get("/orders?buyer_name=Mercedes")
        assert res_empty.status_code == 200
        assert len(res_empty.json()) == 0

    def test_orders_filtering_by_buyer_id(self, db_client: TestClient):
        # 1. Create a VW invoice order
        resp2 = db_client.post("/session/start")
        sid2 = resp2.json()["session_id"]
        db_client.post(f"/session/{sid2}/seller", json=_MINIMAL_SELLER)
        db_client.post(f"/session/{sid2}/buyer", json=_BUYER_VW)
        db_client.post(f"/session/{sid2}/items", json=_SAMPLE_ITEMS)
        db_client.post(f"/session/{sid2}/generate")

        # 2. Filter by exact buyer_id=GLN-VW-555
        res_filtered = db_client.get("/orders?buyer_id=GLN-VW-555")
        assert res_filtered.status_code == 200
        items_filtered = res_filtered.json()
        assert len(items_filtered) == 1
        assert items_filtered[0]["buyer_name"] == "Volkswagen AG"

        # 3. Filter by wrong buyer_id
        res_empty = db_client.get("/orders?buyer_id=GLN-VW-999")
        assert res_empty.status_code == 200
        assert len(res_empty.json()) == 0
