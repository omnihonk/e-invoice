import os
from decimal import Decimal
from datetime import date
from jinja2 import Environment, FileSystemLoader
import weasyprint

from schemas.session import InvoiceSession
from services.helpers import format_vat_id, format_eur, format_qty

# Configure Jinja Environment
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
env.filters["format_eur"] = format_eur
env.filters["format_qty"] = format_qty

def generate_invoice_pdf(session: InvoiceSession) -> bytes:
    """Generate a branded PDF using Jinja2 templates and WeasyPrint."""
    seller = session.seller
    buyer = session.buyer
    layout_name = session.layout_name or "buyer"

    # Logo HTML pre-computing
    logo_html = ""
    if seller and getattr(seller, "logo_base64", None):
        b64 = seller.logo_base64
        if "," in b64:
            b64 = b64.split(",", 1)[1]
        logo_html = f'<img src="data:image/png;base64,{b64}" class="logo-img" alt="Logo"/>'

    # Sender Full string
    seller_name = seller.name if seller else ""
    seller_addr1 = getattr(seller, "line_one", "") or ""
    
    pc = ""
    city = ""
    if seller:
        pc = getattr(seller, "post_code", None) or getattr(seller, "postcode", None) or ""
        city = getattr(seller, "city_name", None) or ""
    
    seller_post_city = f"{pc} {city}".strip()
    
    header_addr_parts = [p for p in [seller_addr1, seller_post_city] if p]
    header_address = ", ".join(header_addr_parts)
    header_full = f"{seller_name}, {header_address}" if header_addr_parts else seller_name

    # Buyer Address details
    buyer_pc = ""
    buyer_city = ""
    buyer_country = ""
    buyer_addr1 = ""
    if buyer:
        buyer_addr1 = getattr(buyer, "line_one", "") or ""
        buyer_pc = getattr(buyer, "post_code", None) or getattr(buyer, "postcode", None) or ""
        buyer_city = getattr(buyer, "city_name", None) or ""
        buyer_country = getattr(buyer, "country_id", "") or ""
    
    buyer_addr_lines = [l for l in [buyer_addr1, f"{buyer_pc} {buyer_city}".strip(), buyer_country] if l]
    buyer_addr_html = "<br/>".join(buyer_addr_lines)

    # Reference codes
    invoice_num = session.invoice_number or (
        getattr(buyer, "invoice_number", None) if buyer else None) or "INV-0001"
    
    issue_date_str = session.issue_date.strftime("%d.%m.%Y")
    issue_city = getattr(seller, "city_name", None) or "" if seller else ""

    # Payment terms
    payment_terms = (getattr(seller, "payment_terms", None) if seller else None) or "14 Tage nach Rechnungsstellung"
    if buyer and getattr(buyer, "payment_due", None):
        payment_terms = f"Zahlbar bis {buyer.payment_due}"

    # Delivery Date
    delivery_date_str = ""
    if buyer and getattr(buyer, "delivery_date", None):
        try:
            delivery_date_str = date.fromisoformat(buyer.delivery_date).strftime("%d.%m.%Y")
        except Exception:
            delivery_date_str = buyer.delivery_date

    # Pre-calculate Totals
    def d2(val):
        return Decimal(str(val)).quantize(Decimal("0.01"))

    line_total = Decimal("0.00")
    for item in session.items:
        line_total += d2(Decimal(str(item.price)) * Decimal(str(item.quantity)))
    
    line_total = d2(line_total)
    tax_total = d2(line_total * Decimal("0.19"))
    grand_total = d2(line_total + tax_total)

    # Tax ID formatting
    seller_tax_id_formatted = ""
    if seller:
        tax_id = getattr(seller, "tax_id", None) or "DE123456789"
        tax_scheme = getattr(seller, "tax_scheme_id", None) or "VA"
        country_id = getattr(seller, "country_id", "DE") or "DE"
        if tax_scheme == "VA":
            seller_tax_id_formatted = format_vat_id(tax_id, country_id)
        else:
            seller_tax_id_formatted = tax_id

    # Optional columns existence check
    def has_val(item, attr):
        if isinstance(item, dict):
            val = item.get(attr)
        else:
            val = getattr(item, attr, None)
        return bool(val and str(val).strip())

    has_customer_article_id = any(has_val(item, "customer_article_id") for item in session.items)
    has_drawing_ref = any(has_val(item, "drawing_ref") for item in session.items)
    has_article_id = any(has_val(item, "article_id") for item in session.items)
    has_material = any(has_val(item, "material") for item in session.items)
    has_surface = any(has_val(item, "surface") for item in session.items)

    # Load layout template
    template_file = f"{layout_name}_invoice.html"
    template = env.get_template(template_file)

    # Context compilation
    context = {
        "session": session,
        "seller": seller,
        "buyer": buyer,
        "logo_html": logo_html,
        "header_full": header_full,
        "seller_post_city": seller_post_city,
        "buyer_addr_html": buyer_addr_html,
        "invoice_num": invoice_num,
        "issue_date_str": issue_date_str,
        "issue_city": issue_city,
        "payment_terms": payment_terms,
        "delivery_date_str": delivery_date_str,
        "line_total": line_total,
        "tax_total": tax_total,
        "grand_total": grand_total,
        "seller_tax_id_formatted": seller_tax_id_formatted,
        "has_customer_article_id": has_customer_article_id,
        "has_drawing_ref": has_drawing_ref,
        "has_article_id": has_article_id,
        "has_material": has_material,
        "has_surface": has_surface,
    }

    html_content = template.render(context)
    pdf_bytes = weasyprint.HTML(string=html_content).write_pdf()
    return pdf_bytes
