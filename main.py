import os

from drafthorse.models.document import Document
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database.db import create_db_and_tables
from dependencies import get_session
from models.party import (
    BuyerTradeParty,
    BuyerTradePartyCreate,
    SellerTradeParty,
    SellerTradePartyCreate,
)


def parse_e_invoice_xml():
    sample_xml_path = os.path.join(
        r"C:\Users\heimb\Code\Python\e-invoice\python-drafthorse\tests\samples\zugferd_2p1_EN16931_Einfach.xml"
    )
    sample_xml = open(sample_xml_path, "rb").read()
    doc = Document.parse(sample_xml)

    print(doc)


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_db_and_tables()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/buyers/", response_model=BuyerTradePartyCreate)
def create_buyer(
    *, session: Session = Depends(get_session), trade_party: BuyerTradePartyCreate
):
    db_trade_party = BuyerTradeParty.model_validate(trade_party)
    db_trade_party.is_buyer = True
    # # get postal trade address id
    # postal_trade_address_id = session.exec(select(PostalTradeAddress.id).where(PostalTradeAddress.company_name == trade_party.name)).first()
    # db_trade_party.postal_trade_address_id = postal_trade_address_id
    # # get trade contact id
    # trade_contact_id = session.exec(select(TradeContact.id).where(TradeContact.company_name == trade_party.name)).first()
    # db_trade_party.trade_contact_id = trade_contact_id
    session.add(db_trade_party)

    session.commit()
    session.refresh(db_trade_party)
    return db_trade_party


@app.post("/sellers/", response_model=SellerTradePartyCreate)
def create_seller(
    *, session: Session = Depends(get_session), trade_party: SellerTradePartyCreate
):
    db_trade_party = SellerTradeParty.model_validate(trade_party)
    session.add(db_trade_party)
    session.commit()
    session.refresh(db_trade_party)
    return db_trade_party


@app.post("/invoice-items/")
def create_invoice_items(items: list[dict]):
    print(items)
    return {"message": "Invoice items created", "items": items}


@app.get("/all_buyers", response_model=list[BuyerTradeParty])
def read_all_buyers(*, session: Session = Depends(get_session)):
    buyers = session.exec(select(BuyerTradeParty)).all()
    return buyers


@app.get("/buyers/{party_id}", response_model=BuyerTradeParty)
def read_buyer(party_id: int):
    return {"party_id": party_id}


@app.get("/sellers/{party_id}", response_model=SellerTradeParty)
def read_seller(party_id: int):
    return {"party_id": party_id}
