from datetime import date

from drafthorse.models.document import Document

from ..models.party import TradeParty, TradePartyCreate


def create_document():
    doc = Document()
    doc.context.guideline_parameter.id = "urn:cen.eu:en16931:2017"
    doc.header.id = "RE1337"
    doc.header.type_code = "380"
    doc.header.issue_date_time = date.today()
    return doc


def create_invoice_items(items: list[dict]):
    # Pos | K-Nummer | Zeichnung | Artikel | JMP.ID | Material | Oberfläche | Stückzahl | Preis / stk | Gesamt | Termin
    print(items)
    
    return {"message": "Invoice items created", "items": items}


def create_trade_party(trade_party: TradePartyCreate,is_buyer:bool):
    db_trade_party = TradeParty.model_validate(trade_party)
    db_trade_party.is_buyer = is_buyer
    
    return db_trade_party