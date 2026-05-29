"""
schemas/session.py
──────────────────
Transient Pydantic Schemas for API & In-Progress Invoice Sessions.

ARCHITECTURAL NOTE:
Why separate Pydantic (schemas/) and SQLModel (models/)?
- Pure Pydantic models here define transient structures (like InvoiceSession) 
  which represent active invoice drafts stored as fast JSON documents in Redis.
- SQLModel models (in models/) represent persistent database tables (SQLite)
  used for master data (reusable customer lists, product catalogs).
This decouples transaction session data from master registry tables.
"""

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
    # Extended fields for invoice PDF template (FKS column layout)
    article_id: Optional[str] = None          # JMP Art.-Nr. (seller_assigned_id)
    customer_article_id: Optional[str] = None # K-Nummer
    drawing_ref: Optional[str] = None         # Zeichnung
    material: Optional[str] = None            # Material
    surface: Optional[str] = None             # Oberfläche

class InvoiceSession(BaseModel):
    session_id: str
    seller: Optional[SellerCreate] = None
    buyer: Optional[BuyerCreate] = None
    items: List[LineItem] = Field(default_factory=list)
    invoice_number: Optional[str] = None
    issue_date: date = Field(default_factory=date.today)
    layout_name: str = "fks"
