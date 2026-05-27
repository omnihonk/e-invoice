import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Response
from schemas.session import InvoiceSession, LineItem
from schemas.schemas import BuyerCreate, SellerCreate
from core.redis_client import get_session, save_session
from services.service import generate_facturx_invoice

router = APIRouter(prefix="/session", tags=["session"])

@router.post("/start")
def start_session():
    session_id = str(uuid.uuid4())
    session = InvoiceSession(session_id=session_id)
    save_session(session)
    return {"session_id": session_id}

@router.post("/{session_id}/seller")
def update_seller(session_id: str, seller: SellerCreate):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.seller = seller
    save_session(session)
    return {"message": "Seller updated", "session": session}

@router.post("/{session_id}/buyer")
def update_buyer(session_id: str, buyer: BuyerCreate):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.buyer = buyer
    save_session(session)
    return {"message": "Buyer updated", "session": session}

@router.post("/{session_id}/items")
def update_items(session_id: str, items: List[LineItem]):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.items = items
    save_session(session)
    return {"message": "Items updated", "session": session}

@router.post("/{session_id}/generate")
def generate_invoice(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    pdf_bytes = generate_facturx_invoice(session)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=invoice_{session.invoice_number or 'draft'}.pdf"}
    )
