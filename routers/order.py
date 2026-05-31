import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Response, Depends
from sqlmodel import Session as DBSession, select

from dependencies import get_session as get_db_session
from models.invoice_order import InvoiceOrder
from schemas.order import OrderListItem, OrderDetails

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("", response_model=List[OrderListItem])
def list_orders(
    buyer_name: Optional[str] = None,
    buyer_id: Optional[str] = None,
    db_session: DBSession = Depends(get_db_session)
):
    """List all invoice generation orders (metadata only) with optional buyer filtering."""
    statement = select(InvoiceOrder)
    if buyer_name:
        statement = statement.where(InvoiceOrder.buyer_name.contains(buyer_name))
    if buyer_id:
        statement = statement.where(InvoiceOrder.buyer_id == buyer_id)
        
    statement = statement.order_by(InvoiceOrder.created_at.desc())
    results = db_session.exec(statement).all()
    return [
        OrderListItem(
            order_number=o.order_number,
            invoice_number=o.invoice_number,
            session_id=o.session_id,
            created_at=o.created_at,
            buyer_name=o.buyer_name,
            buyer_id=o.buyer_id
        ) for o in results
    ]

@router.get("/{order_number}", response_model=OrderDetails)
def get_order_details(order_number: str, db_session: DBSession = Depends(get_db_session)):
    """Retrieve full details of a specific order including its session data snapshot."""
    statement = select(InvoiceOrder).where(InvoiceOrder.order_number == order_number)
    order = db_session.exec(statement).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    try:
        session_data = json.loads(order.session_data_json)
    except Exception:
        session_data = {}
        
    return OrderDetails(
        order_number=order.order_number,
        invoice_number=order.invoice_number,
        session_id=order.session_id,
        created_at=order.created_at,
        session_data=session_data,
        buyer_name=order.buyer_name,
        buyer_id=order.buyer_id
    )

@router.get("/{order_number}/pdf")
def get_order_pdf(order_number: str, db_session: DBSession = Depends(get_db_session)):
    """Download the generated hybrid ZUGFeRD / Factur-X PDF for this order."""
    statement = select(InvoiceOrder).where(InvoiceOrder.order_number == order_number)
    order = db_session.exec(statement).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    filename = f"invoice_{order.invoice_number or 'draft'}.pdf"
    return Response(
        content=order.pdf_binary,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/{order_number}/xml")
def get_order_xml(order_number: str, db_session: DBSession = Depends(get_db_session)):
    """Download the embedded CrossIndustryInvoice XML metadata for this order."""
    statement = select(InvoiceOrder).where(InvoiceOrder.order_number == order_number)
    order = db_session.exec(statement).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    filename = f"facturx_{order.invoice_number or 'draft'}.xml"
    return Response(
        content=order.xml_binary,
        media_type="application/xml",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
