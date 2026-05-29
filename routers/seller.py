from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from dependencies import get_session
from models.party import (
    SellerTradeParty,
    SellerTradePartyCreate,
)
from typing import List

router = APIRouter(tags=["sellers"])

@router.post("/sellers/", response_model=SellerTradeParty)
def create_seller(
    *, session: Session = Depends(get_session), trade_party: SellerTradePartyCreate
):
    db_trade_party = SellerTradeParty.model_validate(trade_party)
    session.add(db_trade_party)
    session.commit()
    session.refresh(db_trade_party)
    return db_trade_party

@router.get("/all_sellers", response_model=List[SellerTradeParty])
def read_all_sellers(*, session: Session = Depends(get_session)):
    sellers = session.exec(select(SellerTradeParty)).all()
    return sellers

@router.get("/sellers/{party_id}", response_model=SellerTradeParty)
def read_seller(party_id: int, *, session: Session = Depends(get_session)):
    seller = session.get(SellerTradeParty, party_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller

@router.put("/sellers/{party_id}", response_model=SellerTradeParty)
def update_seller(
    party_id: int,
    *,
    session: Session = Depends(get_session),
    trade_party: SellerTradePartyCreate
):
    db_seller = session.get(SellerTradeParty, party_id)
    if not db_seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    seller_data = trade_party.model_dump(exclude_unset=True)
    for key, value in seller_data.items():
        setattr(db_seller, key, value)
        
    session.add(db_seller)
    session.commit()
    session.refresh(db_seller)
    return db_seller
