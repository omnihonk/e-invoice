from datetime import date
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from dependencies import get_session as get_db_session
from main import app
from core.redis_client import save_session
from schemas.session import InvoiceSession, LineItem
from schemas.schemas import BuyerCreate, SellerCreate

@pytest.fixture
def db_session():
    """In-memory SQLite database session isolated for order testing."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def order_client(db_session):
    """FastAPI TestClient with overridden database session."""
    def _override():
        return db_session
    app.dependency_overrides[get_db_session] = _override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_order_creation_and_retrieval_flow(order_client):
    # 1. Setup session drafts in Redis
    seller = SellerCreate(
        name="Test Seller", post_code="12345", city_name="Berlin", country_id="DE"
    )
    buyer = BuyerCreate(
        name="Test Buyer", post_code="54321", city_name="München", country_id="DE"
    )
    items = [LineItem(name="Consulting", quantity=5.0, price=100.00)]
    
    session1 = InvoiceSession(
        session_id="session-uuid-001",
        seller=seller,
        buyer=buyer,
        items=items,
        invoice_number="RE-2026-0001",
        issue_date=date(2026, 5, 29)
    )
    session2 = InvoiceSession(
        session_id="session-uuid-002",
        seller=seller,
        buyer=buyer,
        items=items,
        invoice_number="RE-2026-0002",
        issue_date=date(2026, 5, 29)
    )
    # Session with optional free text
    session3 = InvoiceSession(
        session_id="session-uuid-003",
        seller=seller,
        buyer=buyer,
        items=items,
        invoice_number="RE-2026-0003",
        issue_date=date(2026, 5, 29),
        order_freetext="Projekt Alpha 123" # Spaces should be converted to underscores
    )
    
    save_session(session1)
    save_session(session2)
    save_session(session3)

    # 2. Generate invoice for session1 -> should get 2026_00001
    response = order_client.post("/session/session-uuid-001/generate")
    assert response.status_code == 200
    order_num1 = response.headers.get("X-Order-Number")
    assert order_num1 == "2026_00001"
    
    # Generate again for session1 -> should reuse the same order number
    response_dup = order_client.post("/session/session-uuid-001/generate")
    assert response_dup.status_code == 200
    assert response_dup.headers.get("X-Order-Number") == "2026_00001"

    # 3. Generate invoice for session2 -> should get 2026_00002
    response2 = order_client.post("/session/session-uuid-002/generate")
    assert response2.status_code == 200
    order_num2 = response2.headers.get("X-Order-Number")
    assert order_num2 == "2026_00002"

    # 4. Generate invoice for session3 (with free text) -> should get 2026_00003_Projekt_Alpha_123
    response3 = order_client.post("/session/session-uuid-003/generate")
    assert response3.status_code == 200
    order_num3 = response3.headers.get("X-Order-Number")
    assert order_num3 == "2026_00003_Projekt_Alpha_123"

    # 5. List all orders via GET /orders
    list_response = order_client.get("/orders")
    assert list_response.status_code == 200
    orders_list = list_response.json()
    
    assert len(orders_list) == 3
    assert orders_list[0]["order_number"] == "2026_00003_Projekt_Alpha_123"
    assert orders_list[1]["order_number"] == "2026_00002"
    assert orders_list[2]["order_number"] == "2026_00001"

    # 6. Get order details via GET /orders/{order_number}
    details_response = order_client.get("/orders/2026_00001")
    assert details_response.status_code == 200
    details = details_response.json()
    assert details["order_number"] == "2026_00001"
    assert details["invoice_number"] == "RE-2026-0001"
    assert details["session_id"] == "session-uuid-001"

    # 7. Retrieve PDF and XML binaries via dedicated endpoints
    pdf_response = order_client.get("/orders/2026_00001/pdf")
    assert pdf_response.status_code == 200
    assert pdf_response.headers["content-type"] == "application/pdf"
    assert b"%PDF" in pdf_response.content
    
    xml_response = order_client.get("/orders/2026_00001/xml")
    assert xml_response.status_code == 200
    assert xml_response.headers["content-type"] == "application/xml"
    assert b"<rsm:CrossIndustryInvoice" in xml_response.content

    # 8. Check 404 behavior for invalid orders
    assert order_client.get("/orders/2026_99999").status_code == 404
    assert order_client.get("/orders/2026_99999/pdf").status_code == 404
    assert order_client.get("/orders/2026_99999/xml").status_code == 404
