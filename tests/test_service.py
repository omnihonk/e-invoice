"""
tests/test_service.py
─────────────────────
Pure unit tests for the service layer — no HTTP, no DB, no Redis.

Covers:
  • format_vat_id()             – VAT prefix normalisation logic
  • build_drafthorse_document() – CII Document object construction
  • generate_invoice_xml()      – XML serialisation

Notes on drafthorse internals
──────────────────────────────
Drafthorse element objects are *not* plain Python types:
  • StringElement  – access the value with str(element)
  • DecimalElement – no direct numeric access; read via serialised XML
  • Container      – iterate, do not subscript
"""

from datetime import date
from decimal import Decimal

import pytest
from lxml import etree

from schemas.session import InvoiceSession, LineItem
from schemas.schemas import BuyerCreate, SellerCreate
from services.service import (
    build_drafthorse_document,
    format_vat_id,
    generate_invoice_xml,
)


# ── XML parsing helpers (reused from test_xml.py style) ──────────────────────

_NS = {
    "rsm": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
    "ram": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
    "udt": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
}


def _xml_text(session: InvoiceSession, xpath: str) -> str:
    """Serialise *session* to XML and return the text of the first XPath match."""
    xml = generate_invoice_xml(session)
    tree = etree.fromstring(xml)
    nodes = tree.xpath(xpath, namespaces=_NS)
    if not nodes:
        return ""
    node = nodes[0]
    return node.text if hasattr(node, "text") else str(node)


# ══════════════════════════════════════════════════════════════════════════════
# format_vat_id
# ══════════════════════════════════════════════════════════════════════════════

class TestFormatVatId:

    def test_already_prefixed_returned_as_is(self):
        assert format_vat_id("DE123456789", "DE") == "DE123456789"

    def test_numeric_only_gets_country_prefix(self):
        assert format_vat_id("123456789", "DE") == "DE123456789"

    def test_foreign_country_prefix_applied(self):
        result = format_vat_id("987654321", "FR")
        assert result == "FR987654321"

    def test_lowercase_input_normalised_to_upper(self):
        result = format_vat_id("de123456789", "DE")
        assert result == "DE123456789"

    def test_whitespace_stripped_from_tax_id(self):
        result = format_vat_id("DE 123 456 789", "DE")
        assert result == "DE123456789"

    def test_empty_tax_id_returns_empty_string(self):
        assert format_vat_id("", "DE") == ""

    def test_none_tax_id_returns_empty_string(self):
        assert format_vat_id(None, "DE") == ""  # type: ignore[arg-type]

    def test_invalid_country_code_falls_back_to_de(self):
        # country_code has only 1 char → not a valid ISO code → fallback to DE
        result = format_vat_id("123456789", "X")
        assert result == "DE123456789"

    def test_already_two_letter_alpha_prefix_not_doubled(self):
        result = format_vat_id("AT123456789", "AT")
        assert result == "AT123456789"


# ══════════════════════════════════════════════════════════════════════════════
# build_drafthorse_document
# ══════════════════════════════════════════════════════════════════════════════

class TestBuildDrafthorseDocument:

    def _make_session(self, **kwargs) -> InvoiceSession:
        seller = SellerCreate(
            name="Test Seller GmbH",
            post_code="10115",
            city_name="Berlin",
            country_id="DE",
            tax_id="DE123456789",
        )
        buyer = BuyerCreate(
            name="Test Buyer AG",
            post_code="80331",
            city_name="München",
            country_id="DE",
        )
        items = [LineItem(name="Widget", quantity=2.0, price=50.00)]
        defaults = dict(
            session_id="svc-test-001",
            seller=seller,
            buyer=buyer,
            items=items,
            invoice_number="INV-SVC-001",
            issue_date=date(2024, 6, 1),
        )
        defaults.update(kwargs)
        return InvoiceSession(**defaults)

    # ── Document-level fields — via str() on StringElement ───────────────────

    def test_invoice_number_set_on_document(self):
        session = self._make_session(invoice_number="INV-001")
        doc = build_drafthorse_document(session)
        assert str(doc.header.id) == "INV-001"

    def test_type_code_is_380(self):
        """380 = Commercial invoice per UN/CEFACT."""
        session = self._make_session()
        doc = build_drafthorse_document(session)
        assert str(doc.header.type_code) == "380"

    def test_guideline_is_en16931(self):
        session = self._make_session()
        doc = build_drafthorse_document(session)
        assert "en16931" in str(doc.context.guideline_parameter.id)

    def test_currency_code_is_eur(self):
        session = self._make_session()
        doc = build_drafthorse_document(session)
        assert str(doc.trade.settlement.currency_code) == "EUR"

    # ── Seller ────────────────────────────────────────────────────────────────

    def test_seller_name_set(self):
        session = self._make_session()
        doc = build_drafthorse_document(session)
        assert str(doc.trade.agreement.seller.name) == "Test Seller GmbH"

    def test_seller_address_city(self):
        session = self._make_session()
        doc = build_drafthorse_document(session)
        assert str(doc.trade.agreement.seller.address.city_name) == "Berlin"

    def test_seller_address_postcode(self):
        session = self._make_session()
        doc = build_drafthorse_document(session)
        assert str(doc.trade.agreement.seller.address.postcode) == "10115"

    def test_seller_address_country(self):
        session = self._make_session()
        doc = build_drafthorse_document(session)
        assert str(doc.trade.agreement.seller.address.country_id) == "DE"

    def test_seller_vat_id_prefixed_when_missing_country_code(self):
        """Seller tax_id without country prefix should be auto-prefixed in the XML."""
        seller = SellerCreate(
            name="No Prefix Seller",
            post_code="10115",
            city_name="Berlin",
            country_id="DE",
            tax_id="123456789",  # no DE prefix
            tax_scheme_id="VA",
        )
        buyer = BuyerCreate(name="Buyer", post_code="12345", city_name="Munich", country_id="DE")
        session = InvoiceSession(
            session_id="prefix-test",
            seller=seller,
            buyer=buyer,
            items=[LineItem(name="X", quantity=1, price=1)],
            issue_date=date(2024, 1, 1),
        )
        # Check via serialised XML — the most reliable path
        tax_reg = _xml_text(
            session,
            ".//ram:SellerTradeParty/ram:SpecifiedTaxRegistration/ram:ID",
        )
        assert tax_reg.startswith("DE")
        assert "123456789" in tax_reg

    # ── Buyer ─────────────────────────────────────────────────────────────────

    def test_buyer_name_set(self):
        session = self._make_session()
        doc = build_drafthorse_document(session)
        assert str(doc.trade.agreement.buyer.name) == "Test Buyer AG"

    def test_buyer_address_city(self):
        session = self._make_session()
        doc = build_drafthorse_document(session)
        assert str(doc.trade.agreement.buyer.address.city_name) == "München"

    # ── Line items ────────────────────────────────────────────────────────────

    def test_line_items_count(self):
        session = self._make_session()
        doc = build_drafthorse_document(session)
        assert len(doc.trade.items.children) == 1

    def test_line_item_name(self):
        session = self._make_session()
        doc = build_drafthorse_document(session)
        assert str(doc.trade.items.children[0].product.name) == "Widget"

    def test_multiple_items_count(self):
        items = [
            LineItem(name="Item A", quantity=1, price=10),
            LineItem(name="Item B", quantity=3, price=5),
            LineItem(name="Item C", quantity=2, price=7),
        ]
        session = InvoiceSession(
            session_id="multi-item",
            seller=SellerCreate(name="S", post_code="11111", city_name="City", country_id="DE", tax_id="DE000000000"),
            buyer=BuyerCreate(name="B", post_code="22222", city_name="Town", country_id="DE"),
            items=items,
            issue_date=date(2024, 1, 1),
        )
        doc = build_drafthorse_document(session)
        assert len(doc.trade.items.children) == 3

    # ── Monetary summation — via serialised XML ───────────────────────────────

    def test_monetary_summation_line_total(self):
        """2 units × 50.00 = 100.00 net."""
        session = self._make_session()
        val = _xml_text(
            session,
            ".//ram:SpecifiedTradeSettlementHeaderMonetarySummation/ram:LineTotalAmount",
        )
        assert Decimal(val) == Decimal("100.00")

    def test_monetary_summation_tax_total(self):
        """19% of 100.00 = 19.00."""
        session = self._make_session()
        val = _xml_text(
            session,
            ".//ram:SpecifiedTradeSettlementHeaderMonetarySummation/ram:TaxTotalAmount",
        )
        assert Decimal(val) == Decimal("19.00")

    def test_monetary_summation_grand_total(self):
        """100.00 + 19.00 = 119.00."""
        session = self._make_session()
        val = _xml_text(
            session,
            ".//ram:SpecifiedTradeSettlementHeaderMonetarySummation/ram:GrandTotalAmount",
        )
        assert Decimal(val) == Decimal("119.00")

    # ── Edge cases ────────────────────────────────────────────────────────────

    def test_session_with_no_seller_does_not_raise(self):
        """A session without a seller should still produce a document object."""
        session = InvoiceSession(
            session_id="no-seller",
            buyer=BuyerCreate(name="B", post_code="12345", city_name="C", country_id="DE"),
            items=[LineItem(name="X", quantity=1, price=10)],
            issue_date=date(2024, 1, 1),
        )
        doc = build_drafthorse_document(session)
        assert doc is not None

    def test_session_with_empty_items_produces_zero_totals(self):
        """
        An invoice with no items produces a grand total of 0.00.
        We access the DecimalElement value via .to_etree().text since the
        full document cannot be XSD-serialised without at least one line item.
        """
        session = InvoiceSession(
            session_id="empty-items",
            seller=SellerCreate(name="S", post_code="11111", city_name="City", country_id="DE", tax_id="DE000000000"),
            buyer=BuyerCreate(name="B", post_code="22222", city_name="Town", country_id="DE"),
            items=[],
            issue_date=date(2024, 1, 1),
        )
        doc = build_drafthorse_document(session)
        grand_el = doc.trade.settlement.monetary_summation.grand_total.to_etree()
        assert grand_el is not None
        assert Decimal(grand_el.text) == Decimal("0.00")

    def test_zero_price_item_does_not_raise(self):
        session = InvoiceSession(
            session_id="zero-price",
            seller=SellerCreate(name="S", post_code="11111", city_name="City", country_id="DE", tax_id="DE000000000"),
            buyer=BuyerCreate(name="B", post_code="22222", city_name="Town", country_id="DE"),
            items=[LineItem(name="Free Sample", quantity=1, price=0.0)],
            issue_date=date(2024, 1, 1),
        )
        val = _xml_text(
            session,
            ".//ram:SpecifiedTradeSettlementHeaderMonetarySummation/ram:GrandTotalAmount",
        )
        assert Decimal(val) == Decimal("0.00")

    def test_fractional_price_rounded_to_two_decimals(self):
        """Prices with many decimal places must be rounded to 2dp in totals."""
        session = InvoiceSession(
            session_id="fractional",
            seller=SellerCreate(name="S", post_code="11111", city_name="City", country_id="DE", tax_id="DE000000000"),
            buyer=BuyerCreate(name="B", post_code="22222", city_name="Town", country_id="DE"),
            items=[LineItem(name="Precise Part", quantity=3, price=1.333333)],
            issue_date=date(2024, 1, 1),
        )
        val = _xml_text(
            session,
            ".//ram:SpecifiedTradeSettlementHeaderMonetarySummation/ram:LineTotalAmount",
        )
        # 3 × 1.333333 = 3.999999 → rounds to 4.00
        assert Decimal(val) == Decimal("4.00")


# ══════════════════════════════════════════════════════════════════════════════
# generate_invoice_xml
# ══════════════════════════════════════════════════════════════════════════════

class TestGenerateInvoiceXml:

    def _minimal_session(self) -> InvoiceSession:
        return InvoiceSession(
            session_id="xml-test-001",
            seller=SellerCreate(
                name="XML Seller GmbH",
                post_code="10115",
                city_name="Berlin",
                country_id="DE",
                tax_id="DE123456789",
            ),
            buyer=BuyerCreate(
                name="XML Buyer AG",
                post_code="80331",
                city_name="München",
                country_id="DE",
            ),
            items=[LineItem(name="Test Product", quantity=1, price=200.00)],
            invoice_number="INV-XML-001",
            issue_date=date(2024, 6, 1),
        )

    def test_returns_bytes(self):
        result = generate_invoice_xml(self._minimal_session())
        assert isinstance(result, bytes)

    def test_output_is_non_empty(self):
        result = generate_invoice_xml(self._minimal_session())
        assert len(result) > 0

    def test_output_is_valid_xml(self):
        from lxml import etree
        result = generate_invoice_xml(self._minimal_session())
        tree = etree.fromstring(result)  # raises if not well-formed
        assert tree is not None

    def test_output_contains_invoice_number(self):
        result = generate_invoice_xml(self._minimal_session())
        assert b"INV-XML-001" in result

    def test_output_contains_seller_name(self):
        result = generate_invoice_xml(self._minimal_session())
        assert b"XML Seller GmbH" in result

    def test_output_contains_buyer_name(self):
        result = generate_invoice_xml(self._minimal_session())
        assert b"XML Buyer AG" in result
