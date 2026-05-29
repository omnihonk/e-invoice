import pytest
from services.service import generate_facturx_invoice, generate_invoice_pdf
from services.validation_service import validate_pdf_bytes

class TestMustangValidation:

    def test_validation_of_facturx_invoice(self, full_session):
        """
        A standard generated hybrid Factur-X invoice must pass Mustang validation
        with complete compliance (is_valid == True).
        """
        # Generate full hybrid PDF/A invoice
        facturx_pdf = generate_facturx_invoice(full_session)
        assert isinstance(facturx_pdf, bytes)
        
        # Validate using Mustang CLI
        result = validate_pdf_bytes(facturx_pdf)
        
        assert isinstance(result, dict)
        assert result.get("is_valid") is True, f"Validation failed: {result.get('errors')}"
        assert result.get("status") == "valid"
        assert result.get("info") is not None
        assert "rules" in result.get("info")
        assert result.get("info")["rules"]["fired"] > 0
        assert result.get("info")["rules"]["failed"] == 0
        assert not result.get("errors")

    def test_validation_of_plain_pdf_fails(self, full_session):
        """
        A plain PDF without the attached XML metadata should fail validation,
        as ZUGFeRD/Factur-X requires the authoritative embedded XML document.
        """
        # Generate plain PDF (without attached XML)
        plain_pdf = generate_invoice_pdf(full_session)
        assert isinstance(plain_pdf, bytes)
        
        # Validate using Mustang CLI
        result = validate_pdf_bytes(plain_pdf)
        
        assert isinstance(result, dict)
        assert result.get("is_valid") is False
        assert result.get("status") != "valid"
        # We expect a validation warning/error that the XML metadata or attachment is missing
        assert len(result.get("errors", [])) > 0
