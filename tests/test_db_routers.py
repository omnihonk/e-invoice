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
