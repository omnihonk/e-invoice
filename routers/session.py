import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Response, Depends
from sqlmodel import Session as DBSession, select
from schemas.session import InvoiceSession, LineItem
from schemas.schemas import BuyerCreate, SellerCreate
from core.redis_client import get_session, save_session
from services.service import generate_facturx_invoice
from services.validation_service import validate_pdf_bytes
from database.db import get_next_invoice_number, get_next_order_number
from dependencies import get_session as get_db_session

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
def update_buyer(session_id: str, buyer: BuyerCreate, db_session: DBSession = Depends(get_db_session)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.buyer = buyer
    
    # Auto-generation logic for unique consecutive invoice number
    auto_gen = True
    if buyer.auto_invoice_number is False:
        auto_gen = False
    elif buyer.auto_invoice_number is None and buyer.invoice_number is not None:
        auto_gen = False

    if auto_gen:
        invoice_num = get_next_invoice_number(db_session=db_session)
        session.invoice_number = invoice_num
        session.buyer.invoice_number = invoice_num
        session.auto_invoice_number = True
    else:
        session.invoice_number = buyer.invoice_number
        session.auto_invoice_number = False
        
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
def generate_invoice(session_id: str, db_session: DBSession = Depends(get_db_session)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    from services.service import generate_invoice_xml
    xml_bytes = generate_invoice_xml(session)
    pdf_bytes = generate_facturx_invoice(session)
    
    from models.invoice_order import InvoiceOrder
    
    order_number = None
    statement = select(InvoiceOrder).where(InvoiceOrder.session_id == session_id)
    existing_order = db_session.exec(statement).first()
    
    if existing_order:
        order_number = existing_order.order_number
        existing_order.invoice_number = session.invoice_number
        existing_order.session_data_json = session.model_dump_json()
        existing_order.pdf_binary = pdf_bytes
        existing_order.xml_binary = xml_bytes
        db_session.add(existing_order)
        db_session.commit()
    else:
        year = session.issue_date.year
        seq_val = get_next_order_number(year=year, db_session=db_session)
        order_number = f"{year}_{seq_val:05d}"
        if session.order_freetext:
            # Normalize: replace spaces with underscores, then keep safe chars
            normalized = session.order_freetext.replace(" ", "_")
            clean_freetext = "".join(c for c in normalized if c.isalnum() or c in ("-", "_"))
            if clean_freetext:
                order_number = f"{order_number}_{clean_freetext}"
                
        session.order_number = order_number
        save_session(session)
        
        new_order = InvoiceOrder(
            order_number=order_number,
            invoice_number=session.invoice_number,
            session_id=session_id,
            session_data_json=session.model_dump_json(),
            pdf_binary=pdf_bytes,
            xml_binary=xml_bytes
        )
        db_session.add(new_order)
        db_session.commit()
            
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=invoice_{session.invoice_number or 'draft'}.pdf",
            "X-Order-Number": order_number,
            "Access-Control-Expose-Headers": "X-Order-Number"
        }
    )

@router.post("/{session_id}/validate")
def validate_invoice(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    pdf_bytes = generate_facturx_invoice(session)
    result = validate_pdf_bytes(pdf_bytes)
    return result

