from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

# text → Beschreibung der Position
# quantity → Menge (z. B. 1, 3,5)
# net_price → Einzelpreis netto
# tax_rate → Steuersatz in % (optional, wenn leer → Standard)
# unit → Einheit, z. B. C62 (Stück), LS (Pauschal), HUR (Stunde), DAY (Tage), WEE Wochen, MON (Monat)


class LineItemBase(SQLModel):
    invoice_id: Optional[int] = Field(default=None)
    line_id: int = Field(
        description="Kennung der Rechnungsposition",
    )
    note: str = Field(default="", description="Beschreibung der Position")
    product_id: Optional[int] = Field(default=None, foreign_key="products.id")
    quantity: float = Field(default=0.0000, decimal_places=4)
    unit_price: float = Field(
        default=0.0000, decimal_places=4
    )
    net_total_price: float = Field(
        default=0.0000, decimal_places=4, description="Nettobetrag der Position"
    )
    tax_total: float = Field(
        default=0.0000, decimal_places=4, description="Steuern der Position"
    )
    grand_total: float = Field(
        default=0.0000, decimal_places=4, description="Bruttobetrag der Position"
    )


class LineItem(LineItemBase, table=True):
    __tablename__ = "line_items"
    id: Optional[int] = Field(default=None, primary_key=True)


class LineItemCreate(LineItemBase):
    created_at: datetime = Field(default_factory=datetime.now())
    updated_at: datetime = Field(
        default_factory=datetime.now(), sa_column_kwargs={"onupdate": datetime.now()}
    )


class LineItemRead(LineItemBase):
    id: int

    # Relationships
    # invoice: "Invoice" = Relationship(back_populates="line_items")
    # product: Optional["Product"] = Relationship(back_populates="line_items")
    # seller: Optional["Seller"] = Relationship(back_populates="line_items")
    # buyer: Optional["Buyer"] = Relationship(back_populates="line_items")
    # # seller_assigned_id: Optional[str] = Relationship(back_populates="line_items")
    # # buyer_assigned_id: Optional[str] = Relationship(back_populates="line_items")
    # # industry_assigned_id: Optional[str] = Relationship(back_populates="line_items")
    # # model_id: Optional[str] = Relationship(back_populates="line_items")
    # # name: str = Relationship(back_populates="line_items")
    # # description: Optional[str] = Relationship(back_populates="line_items")
    # # currency: str = Field(max_length=3)
