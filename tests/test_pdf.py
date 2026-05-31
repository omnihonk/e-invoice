"""
tests/test_pdf.py
──────────────────
Structural tests for the generated PDF output.

Strategy: assert the PDF bytes are valid (correct magic header, non-empty).
Correctness of content values is verified separately via the XML layer in
test_xml.py (the embedded CII XML is the authoritative data source in
a Factur-X / ZUGFeRD document).

Covers:
  • generate_invoice_pdf()   – raw WeasyPrint PDF output
  • generate_facturx_invoice() – final hybrid PDF/A output
  • Various seller configurations (with/without logo, footer fields, signatory)
"""

import pytest

from services.service import generate_facturx_invoice, generate_invoice_pdf


# ── Helpers ───────────────────────────────────────────────────────────────────

def _is_valid_pdf(data: bytes) -> bool:
    """Check that data starts with the PDF magic bytes."""
    return data[:4] == b"%PDF"


# ══════════════════════════════════════════════════════════════════════════════
# generate_invoice_pdf
# ══════════════════════════════════════════════════════════════════════════════

class TestGenerateInvoicePdf:

    def test_returns_bytes(self, minimal_session):
        result = generate_invoice_pdf(minimal_session)
        assert isinstance(result, bytes)

    def test_pdf_is_non_empty(self, minimal_session):
        result = generate_invoice_pdf(minimal_session)
        assert len(result) > 0

    def test_pdf_has_valid_magic_header(self, minimal_session):
        result = generate_invoice_pdf(minimal_session)
        assert _is_valid_pdf(result), "Output does not start with %PDF magic bytes"

    def test_full_seller_pdf_has_valid_header(self, full_session):
        result = generate_invoice_pdf(full_session)
        assert _is_valid_pdf(result)

    def test_pdf_with_all_footer_fields(self, full_session):
        """Full seller with bank details, HRB, tax number — should not raise."""
        result = generate_invoice_pdf(full_session)
        assert _is_valid_pdf(result)
        assert len(result) > 1024

    def test_pdf_with_signatory(self, full_session):
        """Signatory name + title must not break PDF rendering."""
        assert full_session.seller.signatory is not None
        result = generate_invoice_pdf(full_session)
        assert _is_valid_pdf(result)

    def test_pdf_with_no_buyer(self, minimal_session):
        """Removing the buyer from a session should not raise during PDF gen."""
        minimal_session.buyer = None
        result = generate_invoice_pdf(minimal_session)
        assert _is_valid_pdf(result)

    def test_pdf_with_no_seller(self, minimal_session):
        """A missing seller should degrade gracefully (empty header area)."""
        minimal_session.seller = None
        result = generate_invoice_pdf(minimal_session)
        assert _is_valid_pdf(result)

    def test_pdf_size_is_reasonable(self, minimal_session):
        """A real WeasyPrint PDF should be at least a few KB."""
        result = generate_invoice_pdf(minimal_session)
        assert len(result) > 2048, f"PDF suspiciously small: {len(result)} bytes"

    def test_pdf_with_many_items(self, minimal_session, sample_items):
        """Duplicate items to stress-test the table rendering path."""
        from schemas.session import LineItem
        many_items = sample_items * 20  # 40 rows
        minimal_session.items = many_items
        result = generate_invoice_pdf(minimal_session)
        assert _is_valid_pdf(result)

    def test_pdf_with_single_item_session(self, single_item_session):
        result = generate_invoice_pdf(single_item_session)
        assert _is_valid_pdf(result)

    def test_pdf_with_empty_items_does_not_raise(self, minimal_session):
        minimal_session.items = []
        result = generate_invoice_pdf(minimal_session)
        assert _is_valid_pdf(result)

    def test_pdf_with_zero_price_item(self, minimal_session):
        from schemas.session import LineItem
        minimal_session.items = [LineItem(name="Free Sample", quantity=1, price=0.0)]
        result = generate_invoice_pdf(minimal_session)
        assert _is_valid_pdf(result)

    def test_pdf_with_german_umlauts_in_buyer_name(self, minimal_session, minimal_buyer):
        """Umlauts (ä, ö, ü) in buyer name must render without encoding errors."""
        minimal_buyer.name = "Müller & Söhne GbR"
        minimal_buyer.city_name = "Schöneberg"
        minimal_session.buyer = minimal_buyer
        result = generate_invoice_pdf(minimal_session)
        assert _is_valid_pdf(result)

    def test_pdf_with_dynamic_columns_rendering(self, minimal_session):
        """Line items with a mix of filled and empty optional columns should render valid PDF."""
        from schemas.session import LineItem
        minimal_session.items = [
            LineItem(name="Item A", quantity=1.0, price=10.0, material="Steel"),
            LineItem(name="Item B", quantity=2.0, price=20.0, drawing_ref="DWG-999")
        ]
        result = generate_invoice_pdf(minimal_session)
        assert _is_valid_pdf(result)

    def test_pdf_dynamic_columns_html_elements(self, minimal_session):
        """Verify HTML template rendering hides empty optional columns and displays populated ones."""
        from lxml import html
        from schemas.session import LineItem
        from services.pdf_service import env
        
        minimal_session.items = [
            LineItem(name="Item A", quantity=1.0, price=10.0, material="Steel"),
            LineItem(name="Item B", quantity=2.0, price=20.0, drawing_ref="DWG-999")
        ]
        
        template = env.get_template("buyer_invoice.html")
        context = {
            "session": minimal_session,
            "seller": minimal_session.seller,
            "buyer": minimal_session.buyer,
            "logo_html": "",
            "header_full": "Seller",
            "seller_post_city": "Berlin",
            "buyer_addr_html": "Munich",
            "invoice_num": "RE-001",
            "issue_date_str": "31.05.2026",
            "issue_city": "Berlin",
            "payment_terms": "14 days",
            "delivery_date_str": "31.05.2026",
            "line_total": 50.0,
            "tax_total": 9.5,
            "grand_total": 59.5,
            "seller_tax_id_formatted": "DE123456",
            "has_customer_article_id": False,
            "has_drawing_ref": True,
            "has_article_id": False,
            "has_material": True,
            "has_surface": False,
        }
        rendered = template.render(context)
        tree = html.fromstring(rendered)
        
        headers = tree.xpath("//thead/tr/th/@class")
        assert "col-pos" in headers
        assert "col-drawing" in headers
        assert "col-name" in headers
        assert "col-material" in headers
        assert "col-price num" in headers
        assert "col-qty num" in headers
        assert "col-total num" in headers
        
        assert "col-cust-art" not in headers
        assert "col-art-id" not in headers
        assert "col-surface" not in headers


# ══════════════════════════════════════════════════════════════════════════════
# generate_facturx_invoice  (hybrid PDF/A)
# ══════════════════════════════════════════════════════════════════════════════

class TestGenerateFacturxInvoice:

    def test_returns_bytes(self, minimal_session):
        result = generate_facturx_invoice(minimal_session)
        assert isinstance(result, bytes)

    def test_facturx_has_valid_pdf_header(self, minimal_session):
        result = generate_facturx_invoice(minimal_session)
        assert _is_valid_pdf(result)

    def test_facturx_pdf_is_non_empty(self, minimal_session):
        result = generate_facturx_invoice(minimal_session)
        assert len(result) > 0

    def test_facturx_pdf_larger_than_plain_pdf(self, minimal_session):
        """
        The Factur-X PDF embeds an XML attachment, so it must be at least as
        large as the plain PDF (typically larger).
        """
        plain = generate_invoice_pdf(minimal_session)
        facturx = generate_facturx_invoice(minimal_session)
        # Factur-X is usually larger due to the embedded XML and XMP metadata
        assert len(facturx) >= len(plain)

    def test_facturx_with_full_session(self, full_session):
        result = generate_facturx_invoice(full_session)
        assert _is_valid_pdf(result)
        assert len(result) > 2048

    def test_facturx_single_item(self, single_item_session):
        result = generate_facturx_invoice(single_item_session)
        assert _is_valid_pdf(result)
