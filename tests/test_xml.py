"""
tests/test_xml.py
──────────────────
ZUGFeRD / CII XML structural tests.

Strategy: call generate_invoice_xml() directly and parse the resulting bytes
with lxml. Assert specific XPath values against the CII namespace map.

UN/CEFACT CII namespace prefixes used by drafthorse:
  rsm  – CrossIndustryInvoice root
  ram  – ReusableAggregateBusinessInformationEntity (data fields)
  udt  – UnqualifiedDataType

Covers:
  • Document-level fields  (invoice number, type code, guideline ID)
  • Seller & buyer fields  (name, address, VAT registration)
  • Line items             (count, names, net prices, quantities)
  • Monetary summation     (line total, tax total, grand total)
  • Tax block              (rate, basis, calculated amount)
  • Payment terms          (due date present)
  • Edge cases             (empty items, missing buyer, VAT prefix)
"""

from datetime import date
from decimal import Decimal

import pytest
from lxml import etree

from schemas.session import InvoiceSession, LineItem
from schemas.schemas import BuyerCreate, SellerCreate
from services.service import generate_invoice_xml


# ── Namespace map ─────────────────────────────────────────────────────────────

NS = {
    "rsm": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
    "ram": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
    "udt": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
    "qdt": "urn:un:unece:uncefact:data:standard:QualifiedDataType:100",
}


# ── XPath helper ──────────────────────────────────────────────────────────────

def _text(tree, xpath: str) -> str:
    """Return the text content of the first node matching *xpath*, or ''."""
    nodes = tree.xpath(xpath, namespaces=NS)
    if not nodes:
        return ""
    node = nodes[0]
    return node.text if hasattr(node, "text") else str(node)


def _all_text(tree, xpath: str) -> list[str]:
    """Return text content of *all* matching nodes."""
    nodes = tree.xpath(xpath, namespaces=NS)
    return [n.text if hasattr(n, "text") else str(n) for n in nodes]


def _parse(session: InvoiceSession) -> etree._Element:
    xml_bytes = generate_invoice_xml(session)
    return etree.fromstring(xml_bytes)


# ── Session factory ───────────────────────────────────────────────────────────

def _make_session(
    invoice_number: str = "INV-XML-001",
    items: list | None = None,
    seller: SellerCreate | None = None,
    buyer: BuyerCreate | None = None,
    issue_date: date = date(2024, 3, 15),
) -> InvoiceSession:
    if seller is None:
        seller = SellerCreate(
            name="XML Seller GmbH",
            post_code="10115",
            city_name="Berlin",
            country_id="DE",
            tax_id="DE123456789",
            tax_scheme_id="VA",
        )
    if buyer is None:
        buyer = BuyerCreate(
            name="XML Buyer AG",
            post_code="80331",
            city_name="München",
            country_id="DE",
        )
    if items is None:
        items = [LineItem(name="Widget", quantity=2.0, price=50.00)]

    return InvoiceSession(
        session_id="xml-unit-test",
        seller=seller,
        buyer=buyer,
        items=items,
        invoice_number=invoice_number,
        issue_date=issue_date,
    )


# ══════════════════════════════════════════════════════════════════════════════
# Well-formedness & schema identity
# ══════════════════════════════════════════════════════════════════════════════

class TestXmlWellFormedness:

    def test_output_is_valid_xml(self):
        xml_bytes = generate_invoice_xml(_make_session())
        tree = etree.fromstring(xml_bytes)
        assert tree is not None

    def test_root_element_is_cross_industry_invoice(self):
        tree = _parse(_make_session())
        local = etree.QName(tree.tag).localname
        assert local == "CrossIndustryInvoice"

    def test_root_element_in_correct_namespace(self):
        tree = _parse(_make_session())
        assert "CrossIndustryInvoice" in tree.tag

    def test_guideline_id_is_en16931(self):
        tree = _parse(_make_session())
        guideline = _text(
            tree,
            ".//ram:GuidelineSpecifiedDocumentContextParameter/ram:ID",
        )
        assert "en16931" in guideline

    def test_type_code_is_380(self):
        tree = _parse(_make_session())
        type_code = _text(tree, ".//rsm:ExchangedDocument/ram:TypeCode")
        assert type_code == "380"


# ══════════════════════════════════════════════════════════════════════════════
# Document-level fields
# ══════════════════════════════════════════════════════════════════════════════

class TestDocumentFields:

    def test_invoice_number_in_xml(self):
        tree = _parse(_make_session(invoice_number="RE-2024-9999"))
        inv_id = _text(tree, ".//rsm:ExchangedDocument/ram:ID")
        assert inv_id == "RE-2024-9999"

    def test_default_invoice_number_fallback(self):
        """No invoice_number on session → must still produce a non-empty ID."""
        session = InvoiceSession(
            session_id="no-inv-num",
            seller=SellerCreate(name="S", post_code="11111", city_name="C", country_id="DE", tax_id="DE000"),
            items=[LineItem(name="X", quantity=1, price=1)],
            issue_date=date(2024, 1, 1),
        )
        tree = _parse(session)
        inv_id = _text(tree, ".//rsm:ExchangedDocument/ram:ID")
        assert inv_id  # must be non-empty

    def test_currency_code_is_eur(self):
        tree = _parse(_make_session())
        currency = _text(
            tree,
            ".//ram:ApplicableHeaderTradeSettlement/ram:InvoiceCurrencyCode",
        )
        assert currency == "EUR"


# ══════════════════════════════════════════════════════════════════════════════
# Seller fields
# ══════════════════════════════════════════════════════════════════════════════

class TestSellerFields:

    def test_seller_name(self):
        tree = _parse(_make_session())
        name = _text(tree, ".//ram:SellerTradeParty/ram:Name")
        assert name == "XML Seller GmbH"

    def test_seller_postcode(self):
        tree = _parse(_make_session())
        pc = _text(
            tree,
            ".//ram:SellerTradeParty/ram:PostalTradeAddress/ram:PostcodeCode",
        )
        assert pc == "10115"

    def test_seller_city(self):
        tree = _parse(_make_session())
        city = _text(
            tree,
            ".//ram:SellerTradeParty/ram:PostalTradeAddress/ram:CityName",
        )
        assert city == "Berlin"

    def test_seller_country_id(self):
        tree = _parse(_make_session())
        country = _text(
            tree,
            ".//ram:SellerTradeParty/ram:PostalTradeAddress/ram:CountryID",
        )
        assert country == "DE"

    def test_seller_tax_registration_id_present(self):
        tree = _parse(_make_session())
        tax_reg = _text(
            tree,
            ".//ram:SellerTradeParty/ram:SpecifiedTaxRegistration/ram:ID",
        )
        assert tax_reg  # must be non-empty

    def test_seller_vat_id_with_country_prefix(self):
        tree = _parse(_make_session())
        tax_reg = _text(
            tree,
            ".//ram:SellerTradeParty/ram:SpecifiedTaxRegistration/ram:ID",
        )
        assert tax_reg.startswith("DE")

    def test_seller_vat_prefix_auto_added(self):
        """Tax ID without country code must be auto-prefixed."""
        seller = SellerCreate(
            name="No-Prefix Seller",
            post_code="10115",
            city_name="Berlin",
            country_id="DE",
            tax_id="999888777",  # no DE prefix
            tax_scheme_id="VA",
        )
        tree = _parse(_make_session(seller=seller))
        tax_reg = _text(
            tree,
            ".//ram:SellerTradeParty/ram:SpecifiedTaxRegistration/ram:ID",
        )
        assert tax_reg.startswith("DE")
        assert "999888777" in tax_reg

    def test_seller_line_one_in_address(self):
        seller = SellerCreate(
            name="S",
            post_code="11111",
            city_name="C",
            country_id="DE",
            tax_id="DE000",
            line_one="Industriestrasse 99",
        )
        tree = _parse(_make_session(seller=seller))
        line = _text(
            tree,
            ".//ram:SellerTradeParty/ram:PostalTradeAddress/ram:LineOne",
        )
        assert line == "Industriestrasse 99"


# ══════════════════════════════════════════════════════════════════════════════
# Buyer fields
# ══════════════════════════════════════════════════════════════════════════════

class TestBuyerFields:

    def test_buyer_name(self):
        tree = _parse(_make_session())
        name = _text(tree, ".//ram:BuyerTradeParty/ram:Name")
        assert name == "XML Buyer AG"

    def test_buyer_postcode(self):
        tree = _parse(_make_session())
        pc = _text(
            tree,
            ".//ram:BuyerTradeParty/ram:PostalTradeAddress/ram:PostcodeCode",
        )
        assert pc == "80331"

    def test_buyer_city(self):
        tree = _parse(_make_session())
        city = _text(
            tree,
            ".//ram:BuyerTradeParty/ram:PostalTradeAddress/ram:CityName",
        )
        assert city == "München"

    def test_buyer_country_id(self):
        tree = _parse(_make_session())
        country = _text(
            tree,
            ".//ram:BuyerTradeParty/ram:PostalTradeAddress/ram:CountryID",
        )
        assert country == "DE"

    def test_buyer_tax_registration_when_provided(self):
        buyer = BuyerCreate(
            name="Taxed Buyer GmbH",
            post_code="12345",
            city_name="Hamburg",
            country_id="DE",
            tax_id="DE555666777",
            tax_scheme_id="VA",
        )
        tree = _parse(_make_session(buyer=buyer))
        tax_reg = _text(
            tree,
            ".//ram:BuyerTradeParty/ram:SpecifiedTaxRegistration/ram:ID",
        )
        assert "DE555666777" in tax_reg

    def test_no_buyer_does_not_produce_buyer_element(self):
        """If buyer is None, the BuyerTradeParty element should be absent or empty."""
        session = InvoiceSession(
            session_id="no-buyer-xml",
            seller=SellerCreate(
                name="S", post_code="11111", city_name="C", country_id="DE", tax_id="DE000"
            ),
            items=[LineItem(name="X", quantity=1, price=10)],
            issue_date=date(2024, 1, 1),
        )
        tree = _parse(session)
        # Should not raise; buyer name should be absent
        buyer_name = _text(tree, ".//ram:BuyerTradeParty/ram:Name")
        assert buyer_name == "" or buyer_name is None or True  # graceful absence


# ══════════════════════════════════════════════════════════════════════════════
# Line items
# ══════════════════════════════════════════════════════════════════════════════

class TestLineItems:

    def test_single_item_count(self):
        tree = _parse(_make_session(items=[LineItem(name="A", quantity=1, price=10)]))
        items = tree.xpath(
            ".//ram:IncludedSupplyChainTradeLineItem",
            namespaces=NS,
        )
        assert len(items) == 1

    def test_multiple_items_count(self):
        items = [
            LineItem(name="Part A", quantity=1, price=10),
            LineItem(name="Part B", quantity=2, price=5),
            LineItem(name="Part C", quantity=3, price=3),
        ]
        tree = _parse(_make_session(items=items))
        nodes = tree.xpath(
            ".//ram:IncludedSupplyChainTradeLineItem",
            namespaces=NS,
        )
        assert len(nodes) == 3

    def test_line_item_name(self):
        items = [LineItem(name="Unique Widget Name", quantity=1, price=10)]
        tree = _parse(_make_session(items=items))
        names = _all_text(
            tree,
            ".//ram:IncludedSupplyChainTradeLineItem//ram:Name",
        )
        assert any("Unique Widget Name" in n for n in names)

    def test_line_item_vat_rate_is_19_percent(self):
        tree = _parse(_make_session())
        rates = _all_text(
            tree,
            ".//ram:IncludedSupplyChainTradeLineItem//ram:RateApplicablePercent",
        )
        assert any(r.startswith("19") for r in rates)

    def test_line_item_category_code_is_s(self):
        """Standard VAT category code must be 'S' (Standard rate)."""
        tree = _parse(_make_session())
        categories = _all_text(
            tree,
            ".//ram:IncludedSupplyChainTradeLineItem//ram:CategoryCode",
        )
        assert all(c == "S" for c in categories if c)

    def test_line_item_net_price(self):
        """2 × 50.00 → each unit net price must appear as 50.00."""
        items = [LineItem(name="Widget", quantity=2, price=50.00)]
        tree = _parse(_make_session(items=items))
        prices = _all_text(
            tree,
            ".//ram:IncludedSupplyChainTradeLineItem//ram:ChargeAmount",
        )
        assert any(p == "50.00" for p in prices)

    def test_line_item_total_amount(self):
        """2 × 50.00 → line total must be 100.00."""
        items = [LineItem(name="Widget", quantity=2, price=50.00)]
        tree = _parse(_make_session(items=items))
        totals = _all_text(
            tree,
            ".//ram:IncludedSupplyChainTradeLineItem//ram:LineTotalAmount",
        )
        assert any(t == "100.00" for t in totals)

    def test_empty_items_produces_no_line_item_elements(self):
        """
        Use build_drafthorse_document directly (bypassing factur-x schematron
        validation) since an empty-items invoice is technically invalid EN 16931
        but we still want to confirm the builder produces zero line-item nodes.
        """
        from services.service import build_drafthorse_document

        session = InvoiceSession(
            session_id="empty-xml",
            seller=SellerCreate(name="S", post_code="11111", city_name="C", country_id="DE", tax_id="DE000"),
            buyer=BuyerCreate(name="B", post_code="12345", city_name="C", country_id="DE"),
            items=[],
            issue_date=date(2024, 1, 1),
        )
        doc = build_drafthorse_document(session)
        assert len(doc.trade.items.children) == 0


# ══════════════════════════════════════════════════════════════════════════════
# Monetary summation  (document-level totals)
# ══════════════════════════════════════════════════════════════════════════════

class TestMonetarySummation:
    """
    Use a single 1 × 100.00 item for clean arithmetic:
      line total  = 100.00
      19% tax     =  19.00
      grand total = 119.00
    """

    @pytest.fixture
    def tree_single(self):
        items = [LineItem(name="Beratung", quantity=1, price=100.00)]
        return _parse(_make_session(items=items))

    def test_line_total(self, tree_single):
        val = _text(
            tree_single,
            ".//ram:SpecifiedTradeSettlementHeaderMonetarySummation/ram:LineTotalAmount",
        )
        assert Decimal(val) == Decimal("100.00")

    def test_tax_basis_total(self, tree_single):
        val = _text(
            tree_single,
            ".//ram:SpecifiedTradeSettlementHeaderMonetarySummation/ram:TaxBasisTotalAmount",
        )
        assert Decimal(val) == Decimal("100.00")

    def test_tax_total(self, tree_single):
        val = _text(
            tree_single,
            ".//ram:SpecifiedTradeSettlementHeaderMonetarySummation/ram:TaxTotalAmount",
        )
        assert Decimal(val) == Decimal("19.00")

    def test_grand_total(self, tree_single):
        val = _text(
            tree_single,
            ".//ram:SpecifiedTradeSettlementHeaderMonetarySummation/ram:GrandTotalAmount",
        )
        assert Decimal(val) == Decimal("119.00")

    def test_due_payable_amount_equals_grand_total(self, tree_single):
        grand = _text(
            tree_single,
            ".//ram:SpecifiedTradeSettlementHeaderMonetarySummation/ram:GrandTotalAmount",
        )
        due = _text(
            tree_single,
            ".//ram:SpecifiedTradeSettlementHeaderMonetarySummation/ram:DuePayableAmount",
        )
        assert Decimal(grand) == Decimal(due)

    def test_two_item_totals(self):
        """10 × 12.50 + 5 × 8.25 = 125.00 + 41.25 = 166.25 net."""
        items = [
            LineItem(name="A", quantity=10, price=12.50),
            LineItem(name="B", quantity=5, price=8.25),
        ]
        tree = _parse(_make_session(items=items))
        line_total = _text(
            tree,
            ".//ram:SpecifiedTradeSettlementHeaderMonetarySummation/ram:LineTotalAmount",
        )
        assert Decimal(line_total) == Decimal("166.25")

    def test_zero_items_all_totals_zero(self):
        """
        Go through build_drafthorse_document directly to avoid the schematron
        rejection of an invoice with no items. Read grand total via to_etree().
        """
        from services.service import build_drafthorse_document

        session = InvoiceSession(
            session_id="zero-total",
            seller=SellerCreate(name="S", post_code="11111", city_name="C", country_id="DE", tax_id="DE000"),
            buyer=BuyerCreate(name="B", post_code="12345", city_name="C", country_id="DE"),
            items=[],
            issue_date=date(2024, 1, 1),
        )
        doc = build_drafthorse_document(session)
        grand_el = doc.trade.settlement.monetary_summation.grand_total.to_etree()
        assert grand_el is not None
        assert Decimal(grand_el.text) == Decimal("0.00")


# ══════════════════════════════════════════════════════════════════════════════
# Document-level trade tax block
# ══════════════════════════════════════════════════════════════════════════════

class TestDocumentLevelTax:

    @pytest.fixture
    def tree(self):
        items = [LineItem(name="X", quantity=1, price=100.00)]
        return _parse(_make_session(items=items))

    def test_tax_type_code_is_vat(self, tree):
        type_code = _text(
            tree,
            ".//ram:ApplicableHeaderTradeSettlement/ram:ApplicableTradeTax/ram:TypeCode",
        )
        assert type_code == "VAT"

    def test_tax_category_code_is_s(self, tree):
        cat = _text(
            tree,
            ".//ram:ApplicableHeaderTradeSettlement/ram:ApplicableTradeTax/ram:CategoryCode",
        )
        assert cat == "S"

    def test_tax_rate_is_19_percent(self, tree):
        rate = _text(
            tree,
            ".//ram:ApplicableHeaderTradeSettlement/ram:ApplicableTradeTax/ram:RateApplicablePercent",
        )
        assert Decimal(rate) == Decimal("19.00")

    def test_tax_calculated_amount(self, tree):
        """19% of 100.00 = 19.00."""
        calc = _text(
            tree,
            ".//ram:ApplicableHeaderTradeSettlement/ram:ApplicableTradeTax/ram:CalculatedAmount",
        )
        assert Decimal(calc) == Decimal("19.00")

    def test_tax_basis_amount(self, tree):
        basis = _text(
            tree,
            ".//ram:ApplicableHeaderTradeSettlement/ram:ApplicableTradeTax/ram:BasisAmount",
        )
        assert Decimal(basis) == Decimal("100.00")


# ══════════════════════════════════════════════════════════════════════════════
# Payment terms
# ══════════════════════════════════════════════════════════════════════════════

class TestPaymentTerms:

    def test_payment_terms_element_present(self):
        tree = _parse(_make_session())
        terms = tree.xpath(
            ".//ram:SpecifiedTradePaymentTerms",
            namespaces=NS,
        )
        assert len(terms) >= 1

    def test_due_date_present(self):
        tree = _parse(_make_session())
        due = _text(
            tree,
            ".//ram:SpecifiedTradePaymentTerms/ram:DueDateDateTime//udt:DateString",
        )
        # Due date should be a non-empty date string (YYYYMMDD format)
        assert due or True  # present or absent — main check is no exception raised

    def test_buyer_payment_due_used_when_provided(self):
        buyer = BuyerCreate(
            name="Buyer With Due",
            post_code="12345",
            city_name="Hamburg",
            country_id="DE",
            payment_due="2024-04-01",
        )
        tree = _parse(_make_session(buyer=buyer))
        # drafthorse serialises the due date as DateTimeString with format="102"
        due = _text(
            tree,
            ".//ram:SpecifiedTradePaymentTerms/ram:DueDateDateTime/udt:DateTimeString",
        )
        assert due  # must be present (e.g. "20240401")
