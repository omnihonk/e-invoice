import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from dependencies import get_session
from main import app
from models.party import SellerTradeParty, BuyerTradeParty
from models.product import Product

@pytest.fixture(name="db_session")
def db_session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

class TestDBRouters:

    def test_seller_crud_endpoints(self, db_session):
        def get_session_override():
            return db_session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        # 1. Create Seller
        response = client.post(
            "/sellers/",
            json={
                "name": "Test Seller GmbH",
                "post_code": "54321",
                "city_name": "Berlin",
                "line_one": "Musterstr 1",
                "country_id": "DE",
                "tax_scheme_id": "VA",
                "tax_id": "DE123456789",
            },
        )
        assert response.status_code == 200
        seller_id = response.json()["id"]
        assert response.json()["name"] == "Test Seller GmbH"

        # 2. Get Seller by ID
        response = client.get(f"/sellers/{seller_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Test Seller GmbH"

        # 3. Read All Sellers
        response = client.get("/all_sellers")
        assert response.status_code == 200
        assert len(response.json()) == 1

        # 4. Delete Seller
        response = client.delete(f"/sellers/{seller_id}")
        assert response.status_code == 200
        assert "deleted" in response.json()["message"]

        # 5. Get Seller (deleted) -> 404
        response = client.get(f"/sellers/{seller_id}")
        assert response.status_code == 404

        app.dependency_overrides.clear()

    def test_buyer_crud_endpoints(self, db_session):
        def get_session_override():
            return db_session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        # 1. Create Buyer
        response = client.post(
            "/buyers/",
            json={
                "name": "Test Buyer AG",
                "post_code": "12345",
                "city_name": "München",
                "line_one": "Buyerstr 2",
                "country_id": "DE",
                "tax_scheme_id": "VA",
                "tax_id": "DE987654321",
            },
        )
        assert response.status_code == 200
        buyer_id = response.json()["id"]
        assert response.json()["name"] == "Test Buyer AG"

        # 2. Get Buyer by ID
        response = client.get(f"/buyers/{buyer_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Test Buyer AG"

        # 3. Read All Buyers
        response = client.get("/all_buyers")
        assert response.status_code == 200
        assert len(response.json()) == 1

        # 4. Delete Buyer
        response = client.delete(f"/buyers/{buyer_id}")
        assert response.status_code == 200
        assert "deleted" in response.json()["message"]

        # 5. Get Buyer (deleted) -> 404
        response = client.get(f"/buyers/{buyer_id}")
        assert response.status_code == 404

        app.dependency_overrides.clear()

    def test_buyer_auto_assigned_global_id(self, db_session):
        def get_session_override():
            return db_session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        # 1. Create first buyer without global_id -> should get 490012 (consecutive starting after 490011)
        response1 = client.post(
            "/buyers/",
            json={
                "name": "First Auto Buyer",
                "post_code": "12345",
                "city_name": "München",
                "line_one": "Buyerstr 2",
                "country_id": "DE",
                "tax_scheme_id": "VA",
                "tax_id": "DE987654321",
            },
        )
        assert response1.status_code == 200
        assert response1.json()["global_id"] == "490012"

        # 2. Create second buyer without global_id -> should get 490013
        response2 = client.post(
            "/buyers/",
            json={
                "name": "Second Auto Buyer",
                "post_code": "12345",
                "city_name": "München",
                "line_one": "Buyerstr 3",
                "country_id": "DE",
                "tax_scheme_id": "VA",
                "tax_id": "DE987654322",
            },
        )
        assert response2.status_code == 200
        assert response2.json()["global_id"] == "490013"

        # 2b. Create buyer with empty string global_id -> should get 490014
        response_empty = client.post(
            "/buyers/",
            json={
                "name": "Empty ID Buyer",
                "post_code": "12345",
                "city_name": "München",
                "line_one": "Buyerstr empty",
                "country_id": "DE",
                "tax_scheme_id": "VA",
                "tax_id": "DE987654326",
                "global_id": ""
            },
        )
        assert response_empty.status_code == 200
        assert response_empty.json()["global_id"] == "490014"

        # 2c. Create buyer with whitespace global_id -> should get 490015
        response_space = client.post(
            "/buyers/",
            json={
                "name": "Space ID Buyer",
                "post_code": "12345",
                "city_name": "München",
                "line_one": "Buyerstr space",
                "country_id": "DE",
                "tax_scheme_id": "VA",
                "tax_id": "DE987654327",
                "global_id": "   "
            },
        )
        assert response_space.status_code == 200
        assert response_space.json()["global_id"] == "490015"

        # 3. Create a third buyer WITH a custom global_id -> should be preserved
        response3 = client.post(
            "/buyers/",
            json={
                "name": "Third Manual Buyer",
                "post_code": "12345",
                "city_name": "München",
                "line_one": "Buyerstr 4",
                "country_id": "DE",
                "tax_scheme_id": "VA",
                "tax_id": "DE987654323",
                "global_id": "CUSTOM-99"
            },
        )
        assert response3.status_code == 200
        assert response3.json()["global_id"] == "CUSTOM-99"

        app.dependency_overrides.clear()

    def test_product_crud_endpoints(self, db_session):
        def get_session_override():
            return db_session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        # 1. Create Product
        response = client.post(
            "/products/",
            json={
                "id": 42,
                "name": "Super Product X",
                "net_price": 4.2500,
                "seller_assigned_id": "JMP-42",
            },
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Super Product X"
        assert response.json()["id"] == 42

        # 2. Get Product by ID
        response = client.get("/products/42")
        assert response.status_code == 200
        assert response.json()["name"] == "Super Product X"

        # 3. Read All Products
        response = client.get("/products/")
        assert response.status_code == 200
        assert len(response.json()) == 1

        # 4. Delete Product
        response = client.delete("/products/42")
        assert response.status_code == 200
        assert "deleted" in response.json()["message"]

        # 5. Get Product (deleted) -> 404
        response = client.get("/products/42")
        assert response.status_code == 404

        app.dependency_overrides.clear()
