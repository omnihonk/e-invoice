"""
Shared fixtures for the e-invoice test suite.

The project root is added to sys.path automatically by pytest via the
``pythonpath = ["."]`` setting in pyproject.toml, so no manual path
manipulation is needed here.
"""

from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

import core.redis_client as _redis_module
from dependencies import get_session as get_db_session
from main import app
from schemas.session import InvoiceSession, LineItem
from schemas.schemas import BuyerCreate, SellerCreate


# ── In-memory session store isolation ───────────────────────────────────────

@pytest.fixture(autouse=True)
def clear_in_memory_store():
    """
    Reset the module-level in-memory session store before *and* after every
    test so no state leaks between test functions.
    """
    _redis_module._in_memory_db.clear()
    yield
    _redis_module._in_memory_db.clear()


# ── HTTP client ──────────────────────────────────────────────────────────────

@pytest.fixture
def client() -> TestClient:
    """FastAPI TestClient with no DB overrides (session routes don't use SQLite)."""
    return TestClient(app)


@pytest.fixture
def db_client():
    """
    FastAPI TestClient backed by a fresh in-memory SQLite DB.
    Use this fixture for tests that exercise the /buyers/ and /sellers/ endpoints.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def _override():
            return session

        app.dependency_overrides[get_db_session] = _override
        yield TestClient(app)
        app.dependency_overrides.clear()


# ── Seller fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
def minimal_seller() -> SellerCreate:
    """Bare-minimum seller — only the fields required by the XML builder."""
    return SellerCreate(
        name="Minimal Seller GmbH",
        post_code="54321",
        city_name="Berlin",
        country_id="DE",
        tax_id="DE123456789",
    )


@pytest.fixture
def full_seller() -> SellerCreate:
    """Fully-populated seller matching a real JMP-style invoice."""
    return SellerCreate(
        name="JMP Fertigungstechnik GmbH",
        post_code="14776",
        city_name="Brandenburg an der Havel",
        country_id="DE",
        line_one="Industriestrasse 42",
        tax_id="DE987654321",
        tax_scheme_id="VA",
        phone_number="+49 3381 123456",
        fax_number="+49 3381 123457",
        email_address="billing@jmp-example.de",
        bank_name="VR-Bank Fläming e.G.",
        iban="DE97160620082104401500",
        bic="GENODEF1LUK",
        hrb="HRB 28603 P, Amtsgericht Potsdam",
        tax_number="050/111/02842",
        signatory="K. Heimburger",
        signatory_title="Geschäftsführer",
        payment_terms="14 Tage nach Rechnungsstellung",
    )


# ── Buyer fixtures ───────────────────────────────────────────────────────────

@pytest.fixture
def minimal_buyer() -> BuyerCreate:
    """Bare-minimum buyer."""
    return BuyerCreate(
        name="Minimal Buyer AG",
        post_code="12345",
        city_name="München",
        country_id="DE",
    )


@pytest.fixture
def full_buyer() -> BuyerCreate:
    """Fully-populated buyer with all optional reference fields."""
    return BuyerCreate(
        name="Acme Corporation GmbH",
        post_code="80331",
        city_name="München",
        country_id="DE",
        line_one="Maximilianstrasse 1",
        tax_id="DE111222333",
        tax_scheme_id="VA",
        invoice_number="RE-2024-0042",
        invoice_date="2024-03-15",
        payment_due="2024-03-29",
        delivery_date="2024-03-14",
        reference="AU-2024-555",
        party_id="K-00123",
        global_id="CUST-0042",
        contact_person="Erika Mustermann",
    )


# ── Line-item fixtures ───────────────────────────────────────────────────────

@pytest.fixture
def sample_items() -> list[LineItem]:
    """Two representative line items with all extended fields."""
    return [
        LineItem(
            name="Gehäuseteil A",
            quantity=10.0,
            price=12.50,
            unit_code="C62",
            article_id="JMP-001",
            customer_article_id="K-001",
            material="1.4301",
            surface="blank",
        ),
        LineItem(
            name="Flanschplatte B",
            quantity=5.0,
            price=8.25,
            unit_code="C62",
            article_id="JMP-002",
            drawing_ref="DRW-0042",
            material="S235",
            surface="verzinkt",
        ),
    ]


@pytest.fixture
def single_item() -> list[LineItem]:
    """Single cheap line item for precise numeric assertions."""
    return [
        LineItem(name="Beratungsleistung", quantity=1.0, price=100.00, unit_code="HUR")
    ]


# ── Session fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def minimal_session(minimal_seller, minimal_buyer, sample_items) -> InvoiceSession:
    return InvoiceSession(
        session_id="test-session-minimal",
        seller=minimal_seller,
        buyer=minimal_buyer,
        items=sample_items,
        invoice_number="INV-TEST-001",
        issue_date=date(2024, 3, 15),
    )


@pytest.fixture
def full_session(full_seller, full_buyer, sample_items) -> InvoiceSession:
    return InvoiceSession(
        session_id="test-session-full",
        seller=full_seller,
        buyer=full_buyer,
        items=sample_items,
        invoice_number="RE-2024-0042",
        issue_date=date(2024, 3, 15),
    )


@pytest.fixture
def single_item_session(minimal_seller, minimal_buyer, single_item) -> InvoiceSession:
    """Session with one item at a round price — simplifies numeric assertions."""
    return InvoiceSession(
        session_id="test-session-single",
        seller=minimal_seller,
        buyer=minimal_buyer,
        items=single_item,
        invoice_number="INV-SINGLE-001",
        issue_date=date(2024, 1, 1),
    )
