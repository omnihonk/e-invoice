from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class OrderListItem(BaseModel):
    order_number: str
    invoice_number: Optional[str] = None
    session_id: str
    created_at: datetime

class OrderDetails(BaseModel):
    order_number: str
    invoice_number: Optional[str] = None
    session_id: str
    created_at: datetime
    session_data: Dict[str, Any]
