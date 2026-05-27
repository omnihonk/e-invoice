from pydantic import BaseModel
from typing import Optional

class BuyerCreate(BaseModel):
    name: str
    party_id: Optional[str] = None
    global_id: Optional[str] = None
    role_code: Optional[str] = "BUYER"
    description: Optional[str] = None
    phone_number: Optional[str] = None
    email_address: Optional[str] = None
    fax_number: Optional[str] = None
    postcode: Optional[str] = None
    post_code: Optional[str] = None
    city_name: Optional[str] = None
    line_one: Optional[str] = None
    line_two: Optional[str] = None
    line_three: Optional[str] = None
    country_id: Optional[str] = None
    country_subdivision: Optional[str] = None
    tax_scheme_id: Optional[str] = "VA"
    tax_id: Optional[str] = None
    trading_business_name: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    payment_due: Optional[str] = None
    delivery_date: Optional[str] = None
    leitweg_id: Optional[str] = None
    reference: Optional[str] = None
    street: Optional[str] = None


class SellerCreate(BaseModel):
    name: str
    party_id: Optional[str] = None
    global_id: Optional[str] = None
    role_code: Optional[str] = "SELLER"
    description: Optional[str] = None
    phone_number: Optional[str] = None
    email_address: Optional[str] = None
    fax_number: Optional[str] = None
    postcode: Optional[str] = None
    post_code: Optional[str] = None
    city_name: Optional[str] = None
    line_one: Optional[str] = None
    line_two: Optional[str] = None
    line_three: Optional[str] = None
    country_id: Optional[str] = None
    country_subdivision: Optional[str] = None
    tax_scheme_id: Optional[str] = "VA"
    tax_id: Optional[str] = None
    trading_business_name: Optional[str] = None
    trade_name: Optional[str] = None
    organization_id: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None