from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from dependencies import get_session
from models.party import (
    BuyerTradeParty,
    BuyerTradePartyCreate,
)
from typing import List

router = APIRouter(tags=["buyers"])

@router.post("/buyers/", response_model=BuyerTradeParty)
def create_buyer(
    *, session: Session = Depends(get_session), trade_party: BuyerTradePartyCreate
):
    db_trade_party = BuyerTradeParty.model_validate(trade_party)
    session.add(db_trade_party)
    session.commit()
    session.refresh(db_trade_party)
    return db_trade_party

@router.get("/all_buyers", response_model=List[BuyerTradeParty])
def read_all_buyers(*, session: Session = Depends(get_session)):
    buyers = session.exec(select(BuyerTradeParty)).all()
    return buyers

@router.get("/buyers/{party_id}", response_model=BuyerTradeParty)
def read_buyer(party_id: int, *, session: Session = Depends(get_session)):
    buyer = session.get(BuyerTradeParty, party_id)
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return buyer

@router.put("/buyers/{party_id}", response_model=BuyerTradeParty)
def update_buyer(
    party_id: int,
    *,
    session: Session = Depends(get_session),
    trade_party: BuyerTradePartyCreate
):
    db_buyer = session.get(BuyerTradeParty, party_id)
    if not db_buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    
    buyer_data = trade_party.model_dump(exclude_unset=True)
    for key, value in buyer_data.items():
        setattr(db_buyer, key, value)
        
    session.add(db_buyer)
    session.commit()
    session.refresh(db_buyer)
    return db_buyer

@router.delete("/buyers/{party_id}")
def delete_buyer(party_id: int, *, session: Session = Depends(get_session)):
    buyer = session.get(BuyerTradeParty, party_id)
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    session.delete(buyer)
    session.commit()
    return {"message": f"Buyer {party_id} deleted successfully"}
