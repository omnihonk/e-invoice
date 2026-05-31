from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class InvoiceOrder(SQLModel, table=True):
    __tablename__ = "invoice_orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_number: str = Field(unique=True, index=True, description="The unique consecutive order number, e.g. ORD-00001")
    invoice_number: Optional[str] = Field(default=None, index=True, description="The corresponding e-invoice number, e.g. RE-2026-0001")
    session_id: str = Field(index=True, description="The UUID session ID from which this invoice was generated")
    session_data_json: str = Field(description="JSON serialized InvoiceSession snapshot")
    pdf_binary: bytes = Field(description="The compiled hybrid PDF/A binary data")
    xml_binary: bytes = Field(description="The embedded machine-readable CrossIndustryInvoice XML data")
    buyer_name: Optional[str] = Field(default=None, index=True, description="Name of the buyer/customer")
    buyer_id: Optional[str] = Field(default=None, index=True, description="ID or Kundennummer of the buyer")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of when the order was created")


class OrderNumberSequence(SQLModel, table=True):
    __tablename__ = "order_number_sequences"

    id: Optional[int] = Field(default=None, primary_key=True)
    year: int = Field(index=True, unique=True, description="Kalenderjahr der Sequenz")
    current_value: int = Field(default=0, description="Aktueller Zähler für die Auftragsnummer in diesem Jahr")
