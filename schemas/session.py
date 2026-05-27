from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from .schemas import BuyerCreate, SellerCreate

class LineItem(BaseModel):
    id: Optional[str] = None
    name: str
    quantity: float
    price: float = Field(default=0.0000)
    unit_code: str = "C62"

class InvoiceSession(BaseModel):
    session_id: str
    seller: Optional[SellerCreate] = None
    buyer: Optional[BuyerCreate] = None
    items: List[LineItem] = Field(default_factory=list)
    invoice_number: Optional[str] = None
    issue_date: date = Field(default_factory=date.today)
