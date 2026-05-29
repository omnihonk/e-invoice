from sqlmodel import SQLModel, create_engine

from constants import DATABASE_URL

# Import all models to register them with SQLModel metadata
from models.party import SellerTradeParty, BuyerTradeParty, InvoiceNumberSequence
from models.product import Product, ProductCharacteristic
from models.session_data import Session
from models.tradelines import LineItem
from sqlmodel import Session as DBSession, select
from datetime import date


engine = create_engine(
    DATABASE_URL, 
    echo=True,
    connect_args={"check_same_thread": False} # For SQLite
)

def get_next_invoice_number(year: int = None) -> str:
    """
    Get the next unique consecutive invoice number for the given year,
    or current year if not specified.
    """
    if year is None:
        year = date.today().year
        
    with DBSession(engine) as session:
        # Find the sequence for this year
        statement = select(InvoiceNumberSequence).where(InvoiceNumberSequence.year == year)
        seq = session.exec(statement).first()
        
        if not seq:
            # First invoice of this year
            seq = InvoiceNumberSequence(year=year, current_value=1)
            session.add(seq)
        else:
            seq.current_value += 1
            session.add(seq)
            
        session.commit()
        session.refresh(seq)
        
        # Format as e.g. RE-2026-0001
        return f"RE-{year}-{seq.current_value:04d}"

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











# class BuyerRepository:
#     def __init__(self):
#         self.engine = create_engine(DATABASE_URL, echo=True)
    
#     def create(self, name: str, party_id: str = None, postcode: str = None,
#               city_name: str = None, country_id: str = None,
#               contact_person: str = None, contact_email: str = None,
#               contact_phone: str = None):
#         """Create a buyer trade party with all related entities"""
#         with Session(self.engine) as session:
#             # Create address if provided
#             address = None
#             if postcode or city_name or country_id:
#                 address = PostalTradeAddress(
#                     postcode=postcode,
#                     city_name=city_name,
#                     country_id=country_id or "DE"  # Default to Germany
#                 )
#                 session.add(address)
#                 session.commit()
#                 session.refresh(address)

#             # Create contact information if provided
#             contact = None
#             if contact_person or contact_email or contact_phone:
#                 phone = None
#                 email = None

#                 if contact_phone:
#                     phone = PhoneNumber(number=contact_phone)
#                     session.add(phone)
#                     session.commit()
#                     session.refresh(phone)

#                 if contact_email:
#                     email = EmailURI(address=contact_email)
#                     session.add(email)
#                     session.commit()
#                     session.refresh(email)

#                 contact = TradeContact(
#                     person_name=contact_person,
#                     telephone_id=phone.id if phone else None,
#                     email_id=email.id if email else None
#                 )
#                 session.add(contact)
#                 session.commit()
#                 session.refresh(contact)

#             # Create the buyer party using base TradeParty with party_type
#             buyer = TradeParty(
#                 party_id=party_id,
#                 name=name,
#                 party_type="buyer",
#                 contact_id=contact.id if contact else None,
#                 address_id=address.id if address else None
#             )
#             session.add(buyer)
#             session.commit()
#             session.refresh(buyer)

#             return buyer

# def create_seller(name: str, party_id: str = None, trade_name: str = None,
#                   organization_id: str = None, postcode: str = None,
#                   city_name: str = None, country_id: str = None,
#                   contact_person: str = None, contact_email: str = None,
#                   contact_phone: str = None):
#     """Create a seller trade party with all related entities"""
#     engine = create_engine(DATABASE_URL, echo=True)
#     with Session(engine) as session:
#         # Create address if provided
#         address = None
#         if postcode or city_name or country_id:
#             address = PostalTradeAddress(
#                 postcode=postcode,
#                 city_name=city_name,
#                 country_id=country_id or "DE"  # Default to Germany
#             )
#             session.add(address)
#             session.commit()
#             session.refresh(address)

#         # Create legal organization if provided
#         legal_org = None
#         if trade_name or organization_id:
#             legal_org = LegalOrganization(
#                 scheme_id="9930",
#                 organization_id=organization_id,
#                 trade_name=trade_name,
#                 trade_address_id=address.id if address else None
#             )
#             session.add(legal_org)
#             session.commit()
#             session.refresh(legal_org)

#         # Create contact information if provided
#         contact = None
#         if contact_person or contact_email or contact_phone:
#             phone = None
#             email = None

#             if contact_phone:
#                 phone = PhoneNumber(number=contact_phone)
#                 session.add(phone)
#                 session.commit()
#                 session.refresh(phone)

#             if contact_email:
#                 email = EmailURI(address=contact_email)
#                 session.add(email)
#                 session.commit()
#                 session.refresh(email)

#             contact = TradeContact(
#                 person_name=contact_person,
#                 telephone_id=phone.id if phone else None,
#                 email_id=email.id if email else None
#             )
#             session.add(contact)
#             session.commit()
#             session.refresh(contact)

#         # Create the seller party using base TradeParty with party_type
#         seller = TradeParty(
#             party_id=party_id,
#             name=name,
#             party_type="seller",
#             legal_organization_id=legal_org.id if legal_org else None,
#             contact_id=contact.id if contact else None,
#             address_id=address.id if address else None
#         )
#         session.add(seller)
#         session.commit()
#         session.refresh(seller)

#         return seller


# def create_buyer(name: str, party_id: str = None, postcode: str = None,
#                  city_name: str = None, country_id: str = None,
#                  contact_person: str = None, contact_email: str = None,
#                  contact_phone: str = None):
#     """Create a buyer trade party with all related entities"""
#     engine = create_engine(DATABASE_URL, echo=True)
#     with Session(engine) as session:
#         # Create address if provided
#         address = None
#         if postcode or city_name or country_id:
#             address = PostalTradeAddress(
#                 postcode=postcode,
#                 city_name=city_name,
#                 country_id=country_id or "DE"  # Default to Germany
#             )
#             session.add(address)
#             session.commit()
#             session.refresh(address)

#         # Create contact information if provided
#         contact = None
#         if contact_person or contact_email or contact_phone:
#             phone = None
#             email = None

#             if contact_phone:
#                 phone = PhoneNumber(number=contact_phone)
#                 session.add(phone)
#                 session.commit()
#                 session.refresh(phone)

#             if contact_email:
#                 email = EmailURI(address=contact_email)
#                 session.add(email)
#                 session.commit()
#                 session.refresh(email)

#             contact = TradeContact(
#                 person_name=contact_person,
#                 telephone_id=phone.id if phone else None,
#                 email_id=email.id if email else None
#             )
#             session.add(contact)
#             session.commit()
#             session.refresh(contact)

#         # Create the buyer party using base TradeParty with party_type
#         buyer = TradeParty(
#             party_id=party_id,
#             name=name,
#             party_type="buyer",
#             contact_id=contact.id if contact else None,
#             address_id=address.id if address else None
#         )
#         session.add(buyer)
#         session.commit()
#         session.refresh(buyer)

#         return buyer