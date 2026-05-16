from pydantic import BaseModel
from typing import Optional

class BuyerCreate(BaseModel):
    name: str
    party_id: Optional[str] = None
    postcode: Optional[str] = None
    city_name: Optional[str] = None
    country_id: Optional[str] = None
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
    trade_name: Optional[str] = None
    organization_id: Optional[str] = None
    postcode: Optional[str] = None
    city_name: Optional[str] = None
    country_id: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None