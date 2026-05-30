from sqlmodel import SQLModel, create_engine

from constants import DATABASE_URL

# Import all models to register them with SQLModel metadata
from models.party import SellerTradeParty, BuyerTradeParty, InvoiceNumberSequence
from models.product import Product, ProductCharacteristic
from models.session_data import Session
from models.tradelines import LineItem
from models.invoice_order import InvoiceOrder, OrderNumberSequence
from sqlmodel import Session as DBSession, select
from datetime import date


engine = create_engine(
    DATABASE_URL, 
    echo=True,
    connect_args={"check_same_thread": False} # For SQLite
)

def get_next_invoice_number(year: int = None, db_session: DBSession = None) -> str:
    """
    Get the next unique consecutive invoice number for the given year,
    or current year if not specified.
    """
    if year is None:
        year = date.today().year
        
    if db_session is None:
        with DBSession(engine) as session:
            return _get_next_invoice_number_impl(year, session)
    else:
        return _get_next_invoice_number_impl(year, db_session)

def _get_next_invoice_number_impl(year: int, session: DBSession) -> str:
    statement = select(InvoiceNumberSequence).where(InvoiceNumberSequence.year == year)
    seq = session.exec(statement).first()
    
    if not seq:
        seq = InvoiceNumberSequence(year=year, current_value=1)
        session.add(seq)
    else:
        seq.current_value += 1
        session.add(seq)
        
    session.commit()
    session.refresh(seq)
    return f"RE-{year}-{seq.current_value:04d}"

def get_next_order_number(year: int = None, db_session: DBSession = None) -> int:
    """
    Get the next consecutive order sequence value for the given year,
    or current year if not specified.
    """
    if year is None:
        year = date.today().year

    if db_session is None:
        with DBSession(engine) as session:
            return _get_next_order_number_impl(year, session)
    else:
        return _get_next_order_number_impl(year, db_session)

def _get_next_order_number_impl(year: int, session: DBSession) -> int:
    statement = select(OrderNumberSequence).where(OrderNumberSequence.year == year)
    seq = session.exec(statement).first()
    
    if not seq:
        seq = OrderNumberSequence(year=year, current_value=1)
        session.add(seq)
    else:
        seq.current_value += 1
        session.add(seq)
        
    session.commit()
    session.refresh(seq)
    return seq.current_value

def create_db_and_tables():
    """Create database tables and handle migrations if necessary"""
    SQLModel.metadata.create_all(engine)
    from sqlalchemy import text
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE seller_trade_parties ADD COLUMN is_default BOOLEAN DEFAULT 0"))
            conn.commit()
            print("Successfully added is_default column to seller_trade_parties")
        except Exception:
            # Column already exists, ignore
            pass

        try:
            conn.execute(text("ALTER TABLE order_number_sequences ADD COLUMN year INTEGER"))
            conn.commit()
            print("Successfully added year column to order_number_sequences")
        except Exception:
            # Column already exists, ignore
            pass


