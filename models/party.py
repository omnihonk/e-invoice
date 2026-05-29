"""
models/party.py
───────────────
Persistent SQLModel Database Models for e-invoice master data.

ARCHITECTURAL NOTE:
Why separate Pydantic (schemas/) and SQLModel (models/)?
- SQLModel classes here define persistent, relational tables mapped to SQLite.
  They store master records (like reusable Buyer/Seller address books) 
  which remain on disk across sessions.
- Pure Pydantic models (in schemas/) define fast, flaccid session drafts 
  and validation payloads stored temporarily in Redis.
This guarantees robust table consistency for core database entities.
"""

from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

# Die andere nTradeparties werde in der Datenbank nicht benötigt. DB Modelle sollten genug Daten bieten



class SellerTradePartyBase(SQLModel):
    """
    Base class for seller trade party
    Based on EN16931 XML Tag <ram:SellerTradeParty>
    ---------------------------------------------------
                        <ram:SellerTradeParty>
                                <ram:ID>549910</ram:ID>
                                <ram:GlobalID schemeID="0088">4333741000005</ram:GlobalID>
                                <ram:Name>MUSTERLIEFERANT GMBH</ram:Name>
                                <ram:DefinedTradeContact>
                                        <ram:TelephoneUniversalCommunication>
                                                <ram:CompleteNumber>+49 932 431 500</ram:CompleteNumber>
                                        </ram:TelephoneUniversalCommunication>
                                        <ram:EmailURIUniversalCommunication>
                                                <ram:URIID>max.mustermann@musterlieferant.de</ram:URIID>
                                        </ram:EmailURIUniversalCommunication>
                                </ram:DefinedTradeContact>
                                <ram:PostalTradeAddress>
                                        <ram:PostcodeCode>99199</ram:PostcodeCode>
                                        <ram:LineOne>BAHNHOFSTRASSE 99</ram:LineOne>
                                        <ram:CityName>MUSTERHAUSEN</ram:CityName>
                                        <ram:CountryID>DE</ram:CountryID>
                                </ram:PostalTradeAddress>
                                <ram:SpecifiedTaxRegistration>
                                        <ram:ID schemeID="FC">201/113/40209</ram:ID>
                                </ram:SpecifiedTaxRegistration>
                        </ram:SellerTradeParty>
    """

    global_id: Optional[str] = Field(
        default=None, max_length=50, description="Globale Kennung des Handelspartners"
    )
    name: str = Field(
        default="", max_length=255, description="Name des Handelspartners/Unternehmens"
    )
    role_code: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Zusätzliche rechliche Informationen des Handelspartners",
    )
    description: Optional[str] = Field(
        default=None, max_length=500, description="Beschreibung des Handelspartners"
    )

    # DefinedTradeContact
    phone_number: Optional[str] = Field(default=None, max_length=50)
    email_address: Optional[EmailStr] = Field(default=None, max_length=255)
    fax_number: Optional[str] = Field(default=None, max_length=50)

    # PostalTradeAddress
    post_code: str = Field(max_length=20)
    city_name: str = Field(max_length=100)
    line_one: str = Field(max_length=255, description="Adresszeile 1")
    line_two: Optional[str] = Field(
        default=None, max_length=255, description="Adresszeile 2"
    )
    line_three: Optional[str] = Field(
        default=None, max_length=255, description="Adresszeile 3"
    )
    country_id: str = Field(max_length=10)  # ISO country code
    country_subdivision: Optional[str] = Field(
        default=None, max_length=100, description="Bundesland"
    )

    # SpecifiedTaxRegistration
    tax_scheme_id: str = Field(max_length=50, description="Art der Steuernummer (VA)")
    tax_id: str = Field(max_length=50, description="Ust.-Id.-Nr.")

    trading_business_name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Firmenname, sofern abweichend vom Namen",
    )

    # PDF-Branding & Rechnungsfußzeile
    logo_base64: Optional[str] = Field(
        default=None, description="Base64-kodiertes Firmenlogo (PNG/JPEG)"
    )
    bank_name: Optional[str] = Field(
        default=None, max_length=255, description="Bankname, z.B. VR-Bank Fläming e.G."
    )
    iban: Optional[str] = Field(
        default=None, max_length=50, description="IBAN des Geschäftskontos"
    )
    bic: Optional[str] = Field(
        default=None, max_length=20, description="BIC/SWIFT-Code der Bank"
    )
    hrb: Optional[str] = Field(
        default=None, max_length=100, description="Handelsregisternummer, z.B. HRB 28603 P, Amtsgericht Potsdam"
    )
    tax_number: Optional[str] = Field(
        default=None, max_length=50, description="Steuernummer (nicht USt-ID)"
    )
    signatory: Optional[str] = Field(
        default=None, max_length=100, description="Name des Unterzeichners, z.B. K. Heimburger"
    )
    signatory_title: Optional[str] = Field(
        default=None, max_length=100, description="Titel des Unterzeichners, z.B. Geschäftsführer"
    )
    payment_terms: Optional[str] = Field(
        default=None, max_length=255, description="Zahlungsbedingungen, z.B. 14 Tage nach Rechnungsstellung"
    )
    is_default: Optional[bool] = Field(
        default=False, description="Ob dieser Lieferant als Standard geladen werden soll"
    )


class SellerTradeParty(SellerTradePartyBase, table=True):
    __tablename__ = "seller_trade_parties"

    id: int = Field(default=None, primary_key=True)
    # Relationships


class SellerTradePartyCreate(SellerTradePartyBase):
    pass


class SellerTradePartyRead(SellerTradePartyBase):
    id: int


class BuyerTradePartyBase(SQLModel):
    """
    Base class for buyer trade party
    Based on EN16931 XML Tag <ram:BuyerTradeParty>
    ---------------------------------------------------
                        <ram:BuyerTradeParty>
                                <ram:ID>549910</ram:ID>
                                <ram:GlobalID schemeID="0088">4333741000005</ram:GlobalID>
                                <ram:Name>MUSTERLIEFERANT GMBH</ram:Name>
                                <ram:DefinedTradeContact>
                                        <ram:TelephoneUniversalCommunication>
                                                <ram:CompleteNumber>+49 932 431 500</ram:CompleteNumber>
                                        </ram:TelephoneUniversalCommunication>
                                        <ram:EmailURIUniversalCommunication>
                                                <ram:URIID>max.mustermann@musterlieferant.de</ram:URIID>
                                        </ram:EmailURIUniversalCommunication>
                                </ram:DefinedTradeContact>
                                <ram:PostalTradeAddress>
                                        <ram:PostcodeCode>99199</ram:PostcodeCode>
                                        <ram:LineOne>BAHNHOFSTRASSE 99</ram:LineOne>
                                        <ram:CityName>MUSTERHAUSEN</ram:CityName>
                                        <ram:CountryID>DE</ram:CountryID>
                                </ram:PostalTradeAddress>
                                <ram:SpecifiedTaxRegistration>
                                        <ram:ID schemeID="FC">201/113/40209</ram:ID>
                                </ram:SpecifiedTaxRegistration>
                        </ram:BuyerTradeParty>
    """

    global_id: Optional[str] = Field(
        default=None, max_length=50, description="Globale Kennung des Handelspartners"
    )
    name: str = Field(
        default="", max_length=255, description="Name des Handelspartners/Unternehmens"
    )
    role_code: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Zusätzliche rechliche Informationen des Handelspartners",
    )
    description: Optional[str] = Field(
        default=None, max_length=500, description="Beschreibung des Handelspartners"
    )

    # DefinedTradeContact
    phone_number: Optional[str] = Field(default=None, max_length=50)
    email_address: Optional[EmailStr] = Field(default=None, max_length=255)
    fax_number: Optional[str] = Field(default=None, max_length=50)

    # PostalTradeAddress
    post_code: str = Field(max_length=20)
    city_name: str = Field(max_length=100)
    line_one: str = Field(max_length=255, description="Adresszeile 1")
    line_two: Optional[str] = Field(
        default=None, max_length=255, description="Adresszeile 2"
    )
    line_three: Optional[str] = Field(
        default=None, max_length=255, description="Adresszeile 3"
    )
    country_id: str = Field(max_length=10)  # ISO country code
    country_subdivision: Optional[str] = Field(
        default=None, max_length=100, description="Bundesland"
    )

    # SpecifiedTaxRegistration
    tax_scheme_id: str = Field(max_length=50, description="Art der Steuernummer (VA)")
    tax_id: str = Field(max_length=50, description="Ust.-Id.-Nr.")

    trading_business_name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Firmenname, sofern abweichend vom Namen",
    )


class BuyerTradeParty(BuyerTradePartyBase, table=True):
    __tablename__ = "buyer_trade_parties"

    id: int = Field(default=None, primary_key=True)
    # Relationships


class BuyerTradePartyCreate(BuyerTradePartyBase):
    pass


class BuyerTradePartyRead(BuyerTradePartyBase):
    id: int


class InvoiceNumberSequence(SQLModel, table=True):
    __tablename__ = "invoice_number_sequences"

    id: Optional[int] = Field(default=None, primary_key=True)
    year: int = Field(index=True, unique=True, description="Kalenderjahr der Sequenz")
    current_value: int = Field(default=0, description="Aktueller Zähler für die Rechnungsnummer")

