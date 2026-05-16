from typing import Optional

from sqlmodel import Field, SQLModel

# SpecifiedTradeProduct	Artikelinformationen	BG-31		0	0	1	1
# collapse or expandGlobalID	Kennung eines Artikels nach registriertem Schema	BT-157		0	0	?	?
# @schemeID	Kennung des Schemas	BT-157-1	ICD	0	0	1	1
# SellerAssignedID	Artikelkennung des Verkäufers	BT-155		0	0	0	?
# BuyerAssignedID	Artikelkennung des Käufers	BT-156		0	0	0	?
# Name	Artikelname	BT-153		0	0	1	1
# Description	Artikelbeschreibung	BT-154		0	0	0	?


class ProductBase(SQLModel):
    # wenn global_id dann auch scheme_id
    global_id: Optional[str] = Field(default=None, max_length=100)
    seller_assigned_id: Optional[str] = Field(default=None, max_length=100)  # JMP.ID
    buyer_assigned_id: Optional[str] = Field(default=None, max_length=100)
    industry_assigned_id: Optional[str] = Field(default=None, max_length=100)
    model_id: Optional[str] = Field(default=None, max_length=100)
    name: str = Field(max_length=100)
    description: Optional[str] = Field(
        default=None, max_length=255
    )  # Wenn Trade Agreements -> eventuell back_populate?
    net_price: float = Field(
        default=0.0000, decimal_places=4, description="Netto Preis pro Einheit"
    )


class Product(ProductBase, table=True):
    __tablename__ = "products"

    id: int = Field(primary_key=True)  # unique=True?

    # currency: str = Field(max_length=3)


class ProductCharacteristic(SQLModel, table=True):
    __tablename__ = "product_characteristics"

    id: int = Field(primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    type_code: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Type code of the product characteristic",
    )
    description: Optional[str] = Field(default=None, max_length=255)
    value_measure: Optional[float] = Field(
        default=None, description="Numerische Messgröße"
    )
    value: Optional[str] = Field(default=None, max_length=100)
    drawing: Optional[str] = Field(default=None, max_length=100)
    surface: Optional[str] = Field(default=None, max_length=100)
    material: Optional[str] = Field(default=None, max_length=100)
    origin_country: Optional[str] = Field(
        default=None, max_length=100, description="Land der Produktherkunft"
    )
