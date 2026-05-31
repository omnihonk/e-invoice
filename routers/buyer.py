from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from dependencies import get_session
from models.party import (
    BuyerTradeParty,
    BuyerTradePartyCreate,
)
from typing import List

router = APIRouter(tags=["buyers"])

def get_next_buyer_number(session: Session) -> str:
    """Get the next consecutive 6-digit Kundennummer starting with '490'."""
    statement = select(BuyerTradeParty).where(BuyerTradeParty.global_id.like("490%"))
    results = session.exec(statement).all()
    
    max_val = 11  # Default fallback starting after SAXAS (490011)
    for r in results:
        g_id = r.global_id
        if g_id and len(g_id) == 6 and g_id.startswith("490"):
            try:
                val = int(g_id[3:])
                if val > max_val:
                    max_val = val
            except ValueError:
                pass
                
    next_val = max_val + 1
    return f"490{next_val:03d}"

@router.post("/buyers/", response_model=BuyerTradeParty)
def create_buyer(
    *, session: Session = Depends(get_session), trade_party: BuyerTradePartyCreate
):
    db_trade_party = BuyerTradeParty.model_validate(trade_party)
    
    # Auto-assign consecutive Kundennummer starting with 490 if not provided
    if not db_trade_party.global_id or not db_trade_party.global_id.strip():
        db_trade_party.global_id = get_next_buyer_number(session)
        
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
