"""
Shared fixtures for the e-invoice test suite.

The project root is added to sys.path automatically by pytest via the
``pythonpath = ["."]`` setting in pyproject.toml, so no manual path
manipulation is needed here.
"""

from datetime import date
import os
from dotenv import load_dotenv

# Load local secrets from .env if present
load_dotenv()

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
        name=os.getenv("SELLER_NAME", "Mock Seller GmbH"),
        post_code=os.getenv("SELLER_POST_CODE", "12345"),
        city_name=os.getenv("SELLER_CITY_NAME", "Musterstadt"),
        country_id="DE",
        line_one=os.getenv("SELLER_LINE_ONE", "Musterstrasse 123"),
        tax_id=os.getenv("SELLER_TAX_ID", "DE123456789"),
        tax_scheme_id="VA",
        phone_number=os.getenv("SELLER_PHONE_NUMBER", "+49 123 456789"),
        fax_number=os.getenv("SELLER_FAX_NUMBER", "+49 123 456780"),
        email_address=os.getenv("SELLER_EMAIL_ADDRESS", "billing@example.de"),
        bank_name=os.getenv("SELLER_BANK_NAME", "Musterbank e.G."),
        iban=os.getenv("SELLER_IBAN", "DE89370400440532013000"),
        bic=os.getenv("SELLER_BIC", "TESTDEF1MUB"),
        hrb=os.getenv("SELLER_HRB", "HRB 12345, Amtsgericht Musterstadt"),
        tax_number=os.getenv("SELLER_TAX_NUMBER", "123/456/78900"),
        signatory=os.getenv("SELLER_SIGNATORY", "Max Mustermann"),
        signatory_title=os.getenv("SELLER_SIGNATORY_TITLE", "Geschäftsführer"),
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
