import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from dependencies import get_session
from main import app


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
            "is_buyer": True,
            "global_id": "123",
            "role_code": "BUYER",
            "country_id": "DE",
            "city_name": "Test City",
            "street_name": "Test Street",
            "postcode": "12345",
        },
    )
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Test Buyer"
    assert data["is_buyer"]

def test_get_all_buyers(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)

    response = client.get("/all_buyers/")
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["name"] == "Test Buyer"
    assert data[0]["is_buyer"]
