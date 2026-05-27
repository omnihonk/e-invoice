import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from dependencies import get_session
from main import app
from models.party import BuyerTradeParty


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_buyer(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)

    response = client.post(
        "/buyers/",
        json={
            "name": "Test Buyer",
            "global_id": "123",
            "role_code": "BUYER",
            "country_id": "DE",
            "city_name": "Test City",
            "line_one": "Test Street",
            "post_code": "12345",
            "tax_scheme_id": "VA",
            "tax_id": "DE123456789",
        },
    )
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Test Buyer"


def test_get_all_buyers(session):
    # Pre-populate the session with a buyer
    buyer = BuyerTradeParty(
        name="Test Buyer",
        global_id="123",
        role_code="BUYER",
        country_id="DE",
        city_name="Test City",
        line_one="Test Street",
        post_code="12345",
        tax_scheme_id="VA",
        tax_id="DE123456789",
    )
    session.add(buyer)
    session.commit()

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)

    response = client.get("/all_buyers")
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["name"] == "Test Buyer"


def test_session_workflow():
    client = TestClient(app)

    # 1. Start session
    response = client.post("/session/start")
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    assert session_id is not None

    # 2. Update seller
    response = client.post(
        f"/session/{session_id}/seller",
        json={
            "name": "Test Seller GmbH",
            "postcode": "54321",
            "city_name": "Seller City",
            "country_id": "DE"
        }
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Seller updated"

    # 3. Update buyer
    response = client.post(
        f"/session/{session_id}/buyer",
        json={
            "name": "Test Buyer AG",
            "postcode": "12345",
            "city_name": "Buyer City",
            "country_id": "DE"
        }
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Buyer updated"

    # 4. Update items
    response = client.post(
        f"/session/{session_id}/items",
        json=[
            {
                "name": "Line Item 1",
                "quantity": 10.0,
                "price": 1.4500,
                "unit_code": "C62"
            }
        ]
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Items updated"

    # 5. Generate Invoice
    response = client.post(f"/session/{session_id}/generate")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 0


def test_vat_prefixing_and_validation():
    client = TestClient(app)

    # 1. Start session
    response = client.post("/session/start")
    assert response.status_code == 200
    session_id = response.json()["session_id"]

    # 2. Update seller with tax_id lacking country prefix
    response = client.post(
        f"/session/{session_id}/seller",
        json={
            "name": "Seller lacking prefix GmbH",
            "post_code": "54321",
            "city_name": "Seller City",
            "country_id": "DE",
            "tax_scheme_id": "VA",
            "tax_id": "123456789"  # Lacks "DE" prefix
        }
    )
    assert response.status_code == 200

    # 3. Update buyer with tax_id lacking country prefix
    response = client.post(
        f"/session/{session_id}/buyer",
        json={
            "name": "Buyer lacking prefix AG",
            "post_code": "12345",
            "city_name": "Buyer City",
            "country_id": "FR",
            "tax_scheme_id": "VA",
            "tax_id": "987654321"  # Lacks "FR" prefix
        }
    )
    assert response.status_code == 200

    # 4. Update items
    response = client.post(
        f"/session/{session_id}/items",
        json=[
            {
                "name": "Consulting",
                "quantity": 1.0,
                "price": 1500.00,
                "unit_code": "HUR"
            }
        ]
    )
    assert response.status_code == 200

    # 5. Generate Invoice - this should pass without any Schematron validation errors
    response = client.post(f"/session/{session_id}/generate")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 0


