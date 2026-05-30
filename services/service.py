from schemas.session import InvoiceSession
from facturx import generate_from_binary

# Re-export necessary functions for backward compatibility with routers & tests
from services.helpers import format_vat_id
from services.drafthorse_service import build_drafthorse_document
from services.pdf_service import generate_invoice_pdf

def generate_invoice_xml(session: InvoiceSession) -> bytes:
    """Generate the CrossIndustryInvoice (CII) XML from the invoice session."""
    doc = build_drafthorse_document(session)
    return doc.serialize(schema="FACTUR-X_EN16931")

def generate_facturx_invoice(session: InvoiceSession) -> bytes:
    """Generate a hybrid Factur-X / ZUGFeRD e-invoice (PDF + embedded CII XML)."""
    xml_bytes = generate_invoice_xml(session)
    pdf_bytes = generate_invoice_pdf(session)
    
    result_pdf = generate_from_binary(pdf_bytes, xml_bytes)
    return result_pdf