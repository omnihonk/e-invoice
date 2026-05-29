from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from dependencies import get_session
from models.party import (
    SellerTradeParty,
    SellerTradePartyCreate,
)
from typing import List, Optional

router = APIRouter(tags=["sellers"])

@router.get("/sellers/default", response_model=Optional[SellerTradeParty])
def read_default_seller(*, session: Session = Depends(get_session)):
    default_seller = session.exec(select(SellerTradeParty).where(SellerTradeParty.is_default == True)).first()
    return default_seller

@router.post("/sellers/", response_model=SellerTradeParty)
def create_seller(
    *, session: Session = Depends(get_session), trade_party: SellerTradePartyCreate
):
    db_trade_party = SellerTradeParty.model_validate(trade_party)
    if db_trade_party.is_default:
        other_sellers = session.exec(select(SellerTradeParty).where(SellerTradeParty.is_default == True)).all()
        for s in other_sellers:
            s.is_default = False
            session.add(s)
            
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
    if seller_data.get("is_default"):
        other_sellers = session.exec(
            select(SellerTradeParty)
            .where(SellerTradeParty.is_default == True)
            .where(SellerTradeParty.id != party_id)
        ).all()
        for s in other_sellers:
            s.is_default = False
            session.add(s)

    for key, value in seller_data.items():
        setattr(db_seller, key, value)
        
    session.add(db_seller)
    session.commit()
    session.refresh(db_seller)
    return db_seller

@router.delete("/sellers/{party_id}")
def delete_seller(party_id: int, *, session: Session = Depends(get_session)):
    seller = session.get(SellerTradeParty, party_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    session.delete(seller)
    session.commit()
    return {"message": f"Seller {party_id} deleted successfully"}
