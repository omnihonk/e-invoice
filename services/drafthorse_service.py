from datetime import date, timedelta
from decimal import Decimal

from drafthorse.models.document import Document
from drafthorse.models.tradelines import LineItem as DHTLineItem

from schemas.session import InvoiceSession
from services.helpers import format_vat_id

def build_drafthorse_document(session: InvoiceSession) -> Document:
    """Build the full ZUGFeRD / Factur-X Document from session data."""
    doc = Document()
    
    _setup_context_and_header(doc, session)
    _setup_seller(doc, session)
    _setup_buyer(doc, session)
    _setup_delivery_and_payment(doc, session)
    _setup_items_and_totals(doc, session)
    
    return doc

def _setup_context_and_header(doc: Document, session: InvoiceSession):
    """Set up the ZUGFeRD profile context and basic header details."""
    # BASIC / EN 16931 profile
    doc.context.guideline_parameter.id = "urn:cen.eu:en16931:2017"
    
    invoice_num = session.invoice_number
    if not invoice_num and session.buyer and getattr(session.buyer, "invoice_number", None):
        invoice_num = session.buyer.invoice_number
    doc.header.id = invoice_num or "INV-0001"
    doc.header.type_code = "380" # Commercial invoice
    
    issue_date = session.issue_date
    if session.buyer and getattr(session.buyer, "invoice_date", None):
        try:
            issue_date = date.fromisoformat(session.buyer.invoice_date)
        except Exception:
            pass
    doc.header.issue_date_time = issue_date

def _setup_seller(doc: Document, session: InvoiceSession):
    """Set up the Seller information including address, contact and tax registries."""
    if not session.seller:
        return
        
    seller = doc.trade.agreement.seller
    seller.name = session.seller.name
    
    postcode = getattr(session.seller, "post_code", None) or getattr(session.seller, "postcode", None)
    if postcode:
        seller.address.postcode = postcode
    if session.seller.city_name:
        seller.address.city_name = session.seller.city_name
    if session.seller.country_id:
        seller.address.country_id = session.seller.country_id
    if getattr(session.seller, "line_one", None):
        seller.address.line_one = session.seller.line_one
    if getattr(session.seller, "line_two", None):
        seller.address.line_two = session.seller.line_two
    if getattr(session.seller, "line_three", None):
        seller.address.line_three = session.seller.line_three
    if getattr(session.seller, "country_subdivision", None):
        seller.address.country_subdivision = session.seller.country_subdivision
        
    # Seller tax registration (BR-CO-26)
    tax_id = getattr(session.seller, "tax_id", None) or "DE123456789"
    tax_scheme = getattr(session.seller, "tax_scheme_id", None) or "VA"
    country_id = getattr(session.seller, "country_id", "DE") or "DE"
    if tax_scheme == "VA":
        tax_id = format_vat_id(tax_id, country_id)
        
    reg = seller.tax_registrations.child_type()
    reg.id = (tax_scheme, tax_id)
    seller.tax_registrations.add(reg)

    # Contact Setup
    contact_person = getattr(session.seller, "contact_person", None)
    phone = getattr(session.seller, "contact_phone", None) or getattr(session.seller, "phone_number", None)
    email = getattr(session.seller, "contact_email", None) or getattr(session.seller, "email_address", None)
    if contact_person or phone or email:
        if contact_person:
            seller.contact.person_name = contact_person
        if phone:
            seller.contact.telephone.number = phone
        if email:
            seller.contact.email.address = email

def _setup_buyer(doc: Document, session: InvoiceSession):
    """Set up the Buyer information including address, contact and tax registries."""
    if not session.buyer:
        return
        
    buyer = doc.trade.agreement.buyer
    buyer.name = session.buyer.name
    
    # Set buyer customer number (assigned by seller) as ram:ID (BR-CO-09 / BT-46)
    buyer_id = getattr(session.buyer, "global_id", None) or getattr(session.buyer, "party_id", None)
    if buyer_id:
        buyer.id = buyer_id
    
    postcode = getattr(session.buyer, "post_code", None) or getattr(session.buyer, "postcode", None)
    if postcode:
        buyer.address.postcode = postcode
    if session.buyer.city_name:
        buyer.address.city_name = session.buyer.city_name
    if session.buyer.country_id:
        buyer.address.country_id = session.buyer.country_id
    if getattr(session.buyer, "line_one", None):
        buyer.address.line_one = session.buyer.line_one
    if getattr(session.buyer, "line_two", None):
        buyer.address.line_two = session.buyer.line_two
    if getattr(session.buyer, "line_three", None):
        buyer.address.line_three = session.buyer.line_three
    if getattr(session.buyer, "country_subdivision", None):
        buyer.address.country_subdivision = session.buyer.country_subdivision
        
    # Buyer tax registration (BR-CO-45)
    tax_id = getattr(session.buyer, "tax_id", None)
    if tax_id:
        tax_scheme = getattr(session.buyer, "tax_scheme_id", None) or "VA"
        country_id = getattr(session.buyer, "country_id", "DE") or "DE"
        if tax_scheme == "VA":
            tax_id = format_vat_id(tax_id, country_id)
        reg = buyer.tax_registrations.child_type()
        reg.id = (tax_scheme, tax_id)
        buyer.tax_registrations.add(reg)

    # Contact Setup
    contact_person = getattr(session.buyer, "contact_person", None)
    phone = getattr(session.buyer, "contact_phone", None) or getattr(session.buyer, "phone_number", None)
    email = getattr(session.buyer, "contact_email", None) or getattr(session.buyer, "email_address", None)
    if contact_person or phone or email:
        if contact_person:
            buyer.contact.person_name = contact_person
        if phone:
            buyer.contact.telephone.number = phone
        if email:
            buyer.contact.email.address = email

def _setup_delivery_and_payment(doc: Document, session: InvoiceSession):
    """Set up actual delivery dates and payment terms/due dates."""
    # Set actual delivery date (BR-FX-EN-04)
    delivery_date = session.issue_date
    if session.buyer and getattr(session.buyer, "delivery_date", None):
        try:
            delivery_date = date.fromisoformat(session.buyer.delivery_date)
        except Exception:
            pass
    doc.trade.delivery.event.occurrence = delivery_date

    # Set payment terms / due date (BR-CO-25)
    payment_due_date = session.issue_date + timedelta(days=14)
    if session.buyer and getattr(session.buyer, "payment_due", None):
        try:
            payment_due_date = date.fromisoformat(session.buyer.payment_due)
        except Exception:
            pass
    term = doc.trade.settlement.terms.child_type()
    term.due = payment_due_date
    term.description = "Zahlbar innerhalb von 14 Tagen netto."
    doc.trade.settlement.terms.add(term)

def _setup_items_and_totals(doc: Document, session: InvoiceSession):
    """Add session line items, and compute/set totals & taxes at document level."""
    def d2(val):
        return Decimal(str(val)).quantize(Decimal("0.01"))

    # Setup Items and totals
    line_total = Decimal("0.00")
    for idx, item in enumerate(session.items, start=1):
        li = DHTLineItem()
        li.document.line_id = str(idx)
        li.product.name = item.name
        
        item_price = Decimal(str(item.price))
        item_quantity = Decimal(str(item.quantity))
        item_total = d2(item_price * item_quantity)
        line_total += item_total
        
        li.agreement.net.amount = d2(item_price)
        li.delivery.billed_quantity = (item_quantity, item.unit_code)
        
        # Map custom line item fields to ZUGFeRD / Factur-X standard
        if getattr(item, "article_id", None):
            li.product.seller_assigned_id = item.article_id
        if getattr(item, "customer_article_id", None):
            li.product.buyer_assigned_id = item.customer_article_id
            
        if getattr(item, "drawing_ref", None):
            char = li.product.characteristics.child_type()
            char.description = "Zeichnung"
            char.value = item.drawing_ref
            li.product.characteristics.add(char)
            
        if getattr(item, "material", None):
            char = li.product.characteristics.child_type()
            char.description = "Material"
            char.value = item.material
            li.product.characteristics.add(char)
            
        if getattr(item, "surface", None):
            char = li.product.characteristics.child_type()
            char.description = "Oberfläche"
            char.value = item.surface
            li.product.characteristics.add(char)
        
        li.settlement.trade_tax.type_code = "VAT"
        li.settlement.trade_tax.category_code = "S"
        li.settlement.trade_tax.rate_applicable_percent = Decimal("19.00")
        li.settlement.monetary_summation.total_amount = item_total
        
        doc.trade.items.add(li)
        
    # Setup Taxes and Summation at Document Level
    line_total = d2(line_total)
    tax_total = d2(line_total * Decimal("0.19"))
    grand_total = d2(line_total + tax_total)

    # Set document-level currency
    doc.trade.settlement.currency_code = "EUR"

    # Document-level trade tax
    tax = doc.trade.settlement.trade_tax.child_type()
    tax.calculated_amount = tax_total
    tax.basis_amount = line_total
    tax.type_code = "VAT"
    tax.category_code = "S"
    tax.rate_applicable_percent = Decimal("19.00")
    doc.trade.settlement.trade_tax.add(tax)

    # Document-level monetary summation
    doc.trade.settlement.monetary_summation.line_total = line_total
    doc.trade.settlement.monetary_summation.tax_basis_total = line_total
    doc.trade.settlement.monetary_summation.tax_total = (tax_total, "EUR")
    doc.trade.settlement.monetary_summation.grand_total = grand_total
    doc.trade.settlement.monetary_summation.due_amount = grand_total
