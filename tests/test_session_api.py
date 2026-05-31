"""
tests/test_session_api.py
──────────────────────────
HTTP-level tests for the session router endpoints.

Covers:
  • POST /session/start                    – session creation
  • POST /session/{id}/seller              – seller update, 404 on bad ID
  • POST /session/{id}/buyer               – buyer update, 404 on bad ID
  • POST /session/{id}/items               – items update, 404 on bad ID
  • POST /session/{id}/generate            – PDF generation, 404 on bad ID
  • Edge cases: empty items, minimal payloads, invalid session IDs
"""

import os
from dotenv import load_dotenv

load_dotenv()

import pytest


# ══════════════════════════════════════════════════════════════════════════════
# /session/start
# ══════════════════════════════════════════════════════════════════════════════

class TestStartSession:

    def test_start_returns_200(self, client):
        response = client.post("/session/start")
        assert response.status_code == 200

    def test_start_returns_session_id(self, client):
        response = client.post("/session/start")
        data = response.json()
        assert "session_id" in data
        assert isinstance(data["session_id"], str)
        assert len(data["session_id"]) > 0

    def test_each_start_produces_unique_session_id(self, client):
        id_1 = client.post("/session/start").json()["session_id"]
        id_2 = client.post("/session/start").json()["session_id"]
        assert id_1 != id_2


# ══════════════════════════════════════════════════════════════════════════════
# /session/{id}/seller
# ══════════════════════════════════════════════════════════════════════════════

_MINIMAL_SELLER = {
    "name": "Minimal Seller GmbH",
    "post_code": "54321",
    "city_name": "Berlin",
    "country_id": "DE",
    "tax_id": "DE123456789",
}

_FULL_SELLER = {
    "name": os.getenv("SELLER_NAME", "Mock Seller GmbH"),
    "post_code": os.getenv("SELLER_POST_CODE", "12345"),
    "city_name": os.getenv("SELLER_CITY_NAME", "Musterstadt"),
    "country_id": "DE",
    "line_one": os.getenv("SELLER_LINE_ONE", "Musterstrasse 123"),
    "tax_id": os.getenv("SELLER_TAX_ID", "DE123456789"),
    "tax_scheme_id": "VA",
    "phone_number": os.getenv("SELLER_PHONE_NUMBER", "+49 123 456789"),
    "email_address": os.getenv("SELLER_EMAIL_ADDRESS", "billing@example.de"),
    "fax_number": os.getenv("SELLER_FAX_NUMBER", "+49 123 456780"),
    "bank_name": os.getenv("SELLER_BANK_NAME", "Musterbank e.G."),
    "iban": os.getenv("SELLER_IBAN", "DE89370400440532013000"),
    "bic": os.getenv("SELLER_BIC", "TESTDEF1MUB"),
    "hrb": os.getenv("SELLER_HRB", "HRB 12345, Amtsgericht Musterstadt"),
    "tax_number": os.getenv("SELLER_TAX_NUMBER", "123/456/78900"),
    "signatory": os.getenv("SELLER_SIGNATORY", "Max Mustermann"),
    "signatory_title": os.getenv("SELLER_SIGNATORY_TITLE", "Geschäftsführer"),
    "payment_terms": "14 Tage nach Rechnungsstellung",
}


class TestUpdateSeller:

    def test_update_seller_returns_200(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        response = client.post(f"/session/{session_id}/seller", json=_MINIMAL_SELLER)
        assert response.status_code == 200

    def test_update_seller_returns_message(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        response = client.post(f"/session/{session_id}/seller", json=_MINIMAL_SELLER)
        assert response.json()["message"] == "Seller updated"

    def test_update_seller_persists_name(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        client.post(f"/session/{session_id}/seller", json=_MINIMAL_SELLER)
        # Verify the session actually stored the seller
        response = client.post(f"/session/{session_id}/seller", json=_MINIMAL_SELLER)
        assert response.json()["session"]["seller"]["name"] == "Minimal Seller GmbH"

    def test_update_seller_full_payload_returns_200(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        response = client.post(f"/session/{session_id}/seller", json=_FULL_SELLER)
        assert response.status_code == 200

    def test_update_seller_invalid_session_returns_404(self, client):
        response = client.post("/session/non-existent-id/seller", json=_MINIMAL_SELLER)
        assert response.status_code == 404

    def test_update_seller_replaces_existing(self, client):
        """A second POST to /seller should overwrite the first."""
        session_id = client.post("/session/start").json()["session_id"]
        client.post(f"/session/{session_id}/seller", json=_MINIMAL_SELLER)
        new_seller = {**_MINIMAL_SELLER, "name": "Updated Seller GmbH"}
        response = client.post(f"/session/{session_id}/seller", json=new_seller)
        assert response.json()["session"]["seller"]["name"] == "Updated Seller GmbH"


# ══════════════════════════════════════════════════════════════════════════════
# /session/{id}/buyer
# ══════════════════════════════════════════════════════════════════════════════

_MINIMAL_BUYER = {
    "name": "Minimal Buyer AG",
    "post_code": "12345",
    "city_name": "München",
    "country_id": "DE",
}

_FULL_BUYER = {
    "name": "Acme Corporation GmbH",
    "post_code": "80331",
    "city_name": "München",
    "country_id": "DE",
    "line_one": "Maximilianstrasse 1",
    "tax_id": "DE111222333",
    "tax_scheme_id": "VA",
    "invoice_number": "RE-2024-0042",
    "invoice_date": "2024-03-15",
    "payment_due": "2024-03-29",
    "delivery_date": "2024-03-14",
    "reference": "AU-2024-555",
    "party_id": "K-00123",
    "global_id": "CUST-0042",
    "contact_person": "Erika Mustermann",
}


class TestUpdateBuyer:

    def test_update_buyer_returns_200(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        response = client.post(f"/session/{session_id}/buyer", json=_MINIMAL_BUYER)
        assert response.status_code == 200

    def test_update_buyer_returns_message(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        response = client.post(f"/session/{session_id}/buyer", json=_MINIMAL_BUYER)
        assert response.json()["message"] == "Buyer updated"

    def test_update_buyer_persists_name(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        response = client.post(f"/session/{session_id}/buyer", json=_MINIMAL_BUYER)
        assert response.json()["session"]["buyer"]["name"] == "Minimal Buyer AG"

    def test_update_buyer_full_payload_returns_200(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        response = client.post(f"/session/{session_id}/buyer", json=_FULL_BUYER)
        assert response.status_code == 200

    def test_update_buyer_with_all_reference_fields(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        response = client.post(f"/session/{session_id}/buyer", json=_FULL_BUYER)
        buyer_data = response.json()["session"]["buyer"]
        assert buyer_data["invoice_number"] == "RE-2024-0042"
        assert buyer_data["reference"] == "AU-2024-555"
        assert buyer_data["contact_person"] == "Erika Mustermann"

    def test_update_buyer_invalid_session_returns_404(self, client):
        response = client.post("/session/non-existent-id/buyer", json=_MINIMAL_BUYER)
        assert response.status_code == 404

    def test_update_buyer_auto_generates_invoice_number(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        # auto_invoice_number defaults to True if not specified
        buyer_data = {**_MINIMAL_BUYER, "auto_invoice_number": True}
        response = client.post(f"/session/{session_id}/buyer", json=buyer_data)
        assert response.status_code == 200
        inv_num_1 = response.json()["session"]["invoice_number"]
        assert inv_num_1.startswith("RE-")
        
        # Second buyer update should increment the sequence number
        session_id_2 = client.post("/session/start").json()["session_id"]
        response_2 = client.post(f"/session/{session_id_2}/buyer", json=buyer_data)
        inv_num_2 = response_2.json()["session"]["invoice_number"]
        assert inv_num_2.startswith("RE-")
        assert inv_num_1 != inv_num_2

    def test_update_buyer_disabled_auto_generation_uses_manual_number(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        buyer_data = {
            **_MINIMAL_BUYER,
            "auto_invoice_number": False,
            "invoice_number": "TEST-MANUAL-999"
        }
        response = client.post(f"/session/{session_id}/buyer", json=buyer_data)
        assert response.status_code == 200
        assert response.json()["session"]["invoice_number"] == "TEST-MANUAL-999"


# ══════════════════════════════════════════════════════════════════════════════
# /session/{id}/items
# ══════════════════════════════════════════════════════════════════════════════

_SAMPLE_ITEMS = [
    {
        "name": "Gehäuseteil A",
        "quantity": 10.0,
        "price": 12.50,
        "unit_code": "C62",
        "article_id": "JMP-001",
        "customer_article_id": "K-001",
        "material": "1.4301",
        "surface": "blank",
    },
    {
        "name": "Flanschplatte B",
        "quantity": 5.0,
        "price": 8.25,
        "unit_code": "C62",
        "article_id": "JMP-002",
        "drawing_ref": "DRW-0042",
        "material": "S235",
        "surface": "verzinkt",
    },
]


class TestUpdateItems:

    def test_update_items_returns_200(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        response = client.post(f"/session/{session_id}/items", json=_SAMPLE_ITEMS)
        assert response.status_code == 200

    def test_update_items_returns_message(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        response = client.post(f"/session/{session_id}/items", json=_SAMPLE_ITEMS)
        assert response.json()["message"] == "Items updated"

    def test_update_items_count_persisted(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        response = client.post(f"/session/{session_id}/items", json=_SAMPLE_ITEMS)
        assert len(response.json()["session"]["items"]) == 2

    def test_update_items_with_empty_list_is_accepted(self, client):
        """Sending an empty items list is a valid API call."""
        session_id = client.post("/session/start").json()["session_id"]
        response = client.post(f"/session/{session_id}/items", json=[])
        assert response.status_code == 200
        assert response.json()["session"]["items"] == []

    def test_update_items_replaces_previous_items(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        client.post(f"/session/{session_id}/items", json=_SAMPLE_ITEMS)
        replacement = [{"name": "Single Item", "quantity": 1.0, "price": 999.0, "unit_code": "C62"}]
        response = client.post(f"/session/{session_id}/items", json=replacement)
        assert len(response.json()["session"]["items"]) == 1
        assert response.json()["session"]["items"][0]["name"] == "Single Item"

    def test_update_items_with_extended_fields(self, client):
        """Extended PDF-template fields (material, surface, etc.) are accepted."""
        session_id = client.post("/session/start").json()["session_id"]
        response = client.post(f"/session/{session_id}/items", json=_SAMPLE_ITEMS)
        item = response.json()["session"]["items"][0]
        assert item["material"] == "1.4301"
        assert item["surface"] == "blank"
        assert item["article_id"] == "JMP-001"

    def test_update_items_invalid_session_returns_404(self, client):
        response = client.post("/session/non-existent-id/items", json=_SAMPLE_ITEMS)
        assert response.status_code == 404

    def test_single_item_with_zero_price_is_accepted(self, client):
        session_id = client.post("/session/start").json()["session_id"]
        zero_price_item = [{"name": "Free Sample", "quantity": 1.0, "price": 0.0, "unit_code": "C62"}]
        response = client.post(f"/session/{session_id}/items", json=zero_price_item)
        assert response.status_code == 200


# ══════════════════════════════════════════════════════════════════════════════
# /session/{id}/generate
# ══════════════════════════════════════════════════════════════════════════════

def _build_complete_session(client):
    """Helper: set up a session with seller, buyer, and items. Returns session_id."""
    session_id = client.post("/session/start").json()["session_id"]
    client.post(f"/session/{session_id}/seller", json=_MINIMAL_SELLER)
    client.post(f"/session/{session_id}/buyer", json=_MINIMAL_BUYER)
    client.post(f"/session/{session_id}/items", json=_SAMPLE_ITEMS)
    return session_id


class TestGenerateInvoice:

    def test_generate_returns_200(self, client):
        session_id = _build_complete_session(client)
        response = client.post(f"/session/{session_id}/generate")
        assert response.status_code == 200

    def test_generate_returns_pdf_content_type(self, client):
        session_id = _build_complete_session(client)
        response = client.post(f"/session/{session_id}/generate")
        assert response.headers["content-type"] == "application/pdf"

    def test_generate_returns_non_empty_body(self, client):
        session_id = _build_complete_session(client)
        response = client.post(f"/session/{session_id}/generate")
        assert len(response.content) > 0

    def test_generate_content_disposition_contains_invoice(self, client):
        session_id = _build_complete_session(client)
        response = client.post(f"/session/{session_id}/generate")
        disposition = response.headers.get("content-disposition", "")
        assert "invoice" in disposition.lower()

    def test_generate_invalid_session_returns_404(self, client):
        response = client.post("/session/non-existent-id/generate")
        assert response.status_code == 404

    def test_generate_without_buyer_raises_validation_error(self, client):
        """
        EN 16931 rule BR-07 mandates a buyer name. Without a buyer the Factur-X
        library raises a validation exception. TestClient propagates it, so we
        capture it with pytest.raises.
        """
        session_id = client.post("/session/start").json()["session_id"]
        client.post(f"/session/{session_id}/seller", json=_MINIMAL_SELLER)
        client.post(f"/session/{session_id}/items", json=_SAMPLE_ITEMS)
        import pytest as _pytest
        with _pytest.raises(Exception, match="(?i)(schematron|buyer|BR-07|invalid)"):
            client.post(f"/session/{session_id}/generate")

    def test_generate_with_full_seller_and_buyer(self, client):
        """Fully-populated payloads should generate without error."""
        session_id = client.post("/session/start").json()["session_id"]
        client.post(f"/session/{session_id}/seller", json=_FULL_SELLER)
        client.post(f"/session/{session_id}/buyer", json=_FULL_BUYER)
        client.post(f"/session/{session_id}/items", json=_SAMPLE_ITEMS)
        response = client.post(f"/session/{session_id}/generate")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"

    def test_full_workflow_step_by_step(self, client):
        """Integration smoke-test: all four steps in sequence."""
        # Step 1: start
        resp = client.post("/session/start")
        assert resp.status_code == 200
        sid = resp.json()["session_id"]

        # Step 2: seller
        resp = client.post(f"/session/{sid}/seller", json=_FULL_SELLER)
        assert resp.status_code == 200

        # Step 3: buyer
        resp = client.post(f"/session/{sid}/buyer", json=_FULL_BUYER)
        assert resp.status_code == 200

        # Step 4: items
        resp = client.post(f"/session/{sid}/items", json=_SAMPLE_ITEMS)
        assert resp.status_code == 200

        # Step 5: generate
        resp = client.post(f"/session/{sid}/generate")
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "application/pdf"
        assert len(resp.content) > 1024  # a real PDF is well above 1 KB
