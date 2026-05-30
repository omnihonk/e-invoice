from decimal import Decimal

def format_vat_id(tax_id: str, country_code: str) -> str:
    """Format a tax VAT ID with country prefix if missing."""
    if not tax_id:
        return ""
    clean_tax_id = "".join(c for c in tax_id if c.isalnum()).upper()
    if not clean_tax_id:
        return ""
    if len(clean_tax_id) > 2 and clean_tax_id[:2].isalpha():
        return clean_tax_id
    prefix = (country_code or "DE").upper()
    if len(prefix) != 2 or not prefix.isalpha():
        prefix = "DE"
    return f"{prefix}{clean_tax_id}"

def format_eur(value) -> str:
    """Format a numeric value or Decimal as German EUR currency string, e.g. 1.234,56 €"""
    try:
        val = Decimal(str(value)).quantize(Decimal("0.01"))
    except (ValueError, TypeError, KeyError):
        val = Decimal("0.00")
    formatted = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{formatted}&nbsp;€"

def format_qty(value) -> str:
    """Format quantity to strip trailing zero decimals elegantly, e.g. 5.0 -> 5"""
    try:
        val = Decimal(str(value))
        return f"{val:g}"
    except (ValueError, TypeError, KeyError):
        return str(value)
