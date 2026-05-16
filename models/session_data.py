from datetime import datetime

from sqlmodel import Field, SQLModel


class SessionBase(SQLModel):
    line_item_id: int = Field(foreign_key="line_items.id")
    seller_id: int = Field(foreign_key="seller_trade_parties.id")
    buyer_id: int = Field(foreign_key="buyer_trade_parties.id")


class Session(SQLModel, table=True):
    __tablename__ = "sessions"

    id: int = Field(primary_key=True)


class SessionCreate(SessionBase):
    created_at: datetime = Field(default_factory=datetime.now())
    updated_at: datetime = Field(
        default_factory=datetime.now(), sa_column_kwargs={"onupdate": datetime.now()}
    )


class SessionRead(SessionBase):
    id: int


# class SessionInvoiceData(SQLModel, table=True):
#     __tablename__ = "session_invoice_data"

#     session_id: str = Field(max_length=100, primary_key=True)
#     trade_party_id_buyer: str = Field(max_length=100)
#     trade_party_id_seller: str = Field(max_length=100)
#     line_items: List["InvoiceLineItem"] = Field(default=[])
