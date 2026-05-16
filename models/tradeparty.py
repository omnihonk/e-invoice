from sqlmodel import SQLModel, Field
from typing import Optional


class BuyerBase(SQLModel):
    name: Optional[str] = Field(default=None, max_length=255)
    address: Optional[str] = Field(default=None, max_length=255)
    tax_registration:str = Field(default=None, description="Ust.-Id.-Nr.")
    tax_scheme_id: str = Field(default=None, max_length=50, description="Steuernummer")
