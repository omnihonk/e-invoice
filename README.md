# Notes
https://erechnung.berlin/
Übersicht der erlaubten ZUGFeRD-XML-Elemente: https://erechnung.berlin/cii/

The scheme codes, which are used to specify the identifier scheme, are a combination of the ISO 6523 ICD list, and a Peppol-specific extension list. The common identifiers in Germany are: 
- Scheme Leitweg-ID, code 0204, to be used by the public sector (see also German Peppol Authority Specific Requirements) 
- Scheme (German) VAT number (Umsatzsteuer-Identifikationsnummer), code 9930 
- Scheme Global Location Number (GLN), code 0088 
- Scheme IBAN, code 9918 
- Be aware: Code 9958 MUST NOT be used anymore. 

# ERROR

(global_id, name, role_code, description, address_id, email_uri, fax_number, phone_number, uri_universal_communication, legal_organization_id, trade_contact_id, tax_registration, tax_scheme_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

2026-03-19 21:19:30,773 INFO sqlalchemy.engine.Engine [cached since 14.81s ago] (None, 'Robert Heimburger', None, 'Invoice: RE-01, Date: 2026-03-19', 2, None, None, None, None, None, 2, None, None)

# Formate

CII ist die zwingend vorgeschriebene Syntax für die in Factur-X/ZUGFeRD-Dokumente eingebetteten XML-Daten.

Zugferd braucht Zahlenangaben in Decimal mit 4 Nachkommastellen eg. 20.0000

### Namespaces

```python
NS_RSM = "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100"
NS_UDT = "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100"
NS_RAM = (
    "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"
)
NS_QDT = "urn:un:unece:uncefact:data:standard:QualifiedDataType:100"
```

### Profiles

```python
BASIC = "BASIC" # Zulässig in Deutschland
COMFORT = "COMFORT"
EXTENDED = "EXTENDED"
```

## **Factur-X/ZUGFeRD:**

- Dies ist ein **hybrides Format**, das aus einem PDF/A-Dokument mit einer eingebetteten maschinenlesbaren XML-Datei besteht. Die Software unterstützt alle Profile dieses Standards, einschließlich der deutschen **XRechnung**, und bietet volle PDF/A-Unterstützung.
- The new version is based on UN/CEFACT CII D22B and is fully backward compatible with D16B. All five profiles have their own XSD and Schematron validation artifacts, which are updated in accordance with EN 16931.

- ## **CII (Cross Industry Invoice):**
- Hierbei handelt es sich um die zweite zugelassene XML-Syntax für Rechnungen in der EU

## Plan

- Frontend mit Eingabemasken für Seller, Supplier, Invoice-Items

1. DB für Seller und Supplier
2. Generate XML from given Data
   - Profile selection
     - MINIMUM
     - BASIC WL
     - BASIC - zulässig in Deutschland
     - EN 16931 - zulässig in Deutschland
     - EXTENDED
     - XRECHNUNG
   - Use existing templates
   - Use existing data from DB
3. Validate XML
4. Generate PDF and attach XML

### Workflow

**a)**

- per Rechnung
  - create xml
  - add post request data to xml
  -

**b)**

- pickle each post
- create xml with drafthorse using pickled data
- delete pickled data

**c)**

- write class for all data needed to generate a valid xml
- create object at session start
  - in main?
- pass object between request functions
  - or make it global?

**d)**

- use database table where on row stores all data in seperate files
- after finishing the Invoice delete
  - if not finished it should be possible to restore the session

# Models

seller_assigned_id: Optional[str] = Field(default=None, max_length=100) # JMP.ID

**LineItem**
| JMP Item Line | Model Class Variable | Zugferd Model |
| --- | --- | --- |
| Pos | | |
| JMP.ID | Product: seller_assigned_id | ReferencedProduct(Element): seller_assigned_id |
| Zeichnung | | |
| Artikel | | |
| K-Nummer | | |
| Material | | |
| Oberfläche | | |
| Stückzahl | LineItem.Quantity | LineDelivery.billed_quantity |
| Preis / stk | Product.net_price | ram:NetPriceProductTradePrice><ram:ChargeAmount>1.4500</ram:ChargeAmount> |
| Gesamt | | <ram:LineTotalAmount><ram:LineTotalAmount> |
| | | |

## Obligatorische Felder

| Rechnung             | Rechnungsteller | Rechnungsempfänger |
| -------------------- | --------------- | ------------------ |
| BT-1 rechnungsnummer |                 |                    |
|                      |                 |                    |
|                      |                 |                    |

BT-2 \*

Fälligkeitsdatum / Zahlungsziel
BT-9 \*

## Notes

Despite its name suggesting general applicability, is not used for line-item quantities like ram:BilledQuantity. Instead, it defines internal composition of bundled products.
The fixed precision (20.0000) reflects ZUGFeRD’s requirement for four decimal places, even when values are whole numbers.
It is optional in the standard but critical when describing multi-component products like mixed palettes.

#### Product Quantities

- ram:IncludedReferencedProduct: Parent element of ram:UnitQuantity; contains details about sub-items in a composite product.
- ram:UnitQuantity: internal composition of bundled products
- ram:BilledQuantity: Represents the total number of items (or packages) invoiced at the line level
- ram:PackageQuantity: Indicates how many packages (e.g., cartons) are delivered
  - used alongside ram:BilledQuantity and distinct from ram:UnitQuantity.

#### Units

- unitCode: Attribute using UN/ECE 2007 D16B standard codes; C62 specifically means "piece" or "unit".
  - Type: XML attribute (string)
  - Parent elements: Commonly appears on <ram:BilledQuantity>, <ram:PackageQuantity>, <ram:BasisQuantity>, <ram:UnitQuantity>
  - Standard: Based on UN/CEFACT Recommendation 20
  - Example values:
    - "C62" = piece (each)
    - "H87" = liter
    - "XBC" = box (containing 20 units, context-specific)
    - "XPX" = package (generic)

### DB Models anpassen

- Product
  - price: float = Field(default=0.0000, decimal_places=4, description="Preis pro Einheit")
    - Relationship zu Trade Agreement?
    - ram:GrossPriceProductTradePrice
    - NetPriceProductTradePrice

# CII Merkmale nach §14 UStG

1. Name und Anschrift beider Parteien Beides wird zusammengefasst unter dem Tag <ram:ApplicableHeaderTradeAgreement>. <ram:SellerTradeParty> umfasst alle Infos zum Lieferanten, <ram:BuyerTradeParty> alle Infos zum Käufer.
2. Steuernummer/USt.-ID Wieder zu finden unter <ram:ApplicableHeaderTradeAgreement>. Läuft dann unter <ram:SpecifiedTaxRegistration>. Hier befinden sich die IDs. Die Unterscheidung, um welche Art der ID es sich handelt, wird anhand des Codes schemeID getroffen. VA steht für USt.-ID, FC für Steuernummer.
3. Ausstellungsdatum Ganz oben. <ram:IsssueDateTime>. format steht für das angegebene Format. Typisch wird die 102 (YYYYMMTT) verwendet, kann aber auch abweichen.
4. Rechnungsnummer Noch weiter oben zu finden unter <ram:ID>.
5. Die Positionen Jede Position wird von <ram:IncludedSupplyChainTradeLineItem> umschlossen. Hier kann unter anderem gefunden werden:
   - <ram:AssociatedDocumentLineDocument> → Die Positionsnummer.
   - <ram:SpecifiedTradeProduct> → Die Produktnummer und der Name
   - <ram:SpecifiedLineTradeAgreement> → Angaben zu Menge und Preis der Position
   - <ram:ApplicableTradeTax> → Angaben zu Steuern auf die Position
6. Liefer-/Leistungsdatum Hier gibt es 2 Varianten: Es wird ein genaues Datum genannt oder ein Zeitraum.
   - Datum: findet sich meist unter <ram:ApplicableHeaderTradeDelivery>
   - Zeitraum: gab es bisher nur bei ubl, wird ergänzt
7. und 8. Steuern und Gesamtbeträge Meist am Ende zu finden.
   - Steuern: <ram:ApplicableTradeTax>
   - Gesamtbeträge: <ram:SpecifiedTradeSettlementHeaderMonetarySummation>

# en16931_comfort_pflichtfelder_cii.csv

EN 16931 (neu ergänzt, u.a.):

Währung, steuerlicher Zeitpunkt, Rechnungsnotizen (BT-5 bis BT-8, BT-21/22)
Alle Referenzen: Projekt, Vertrag, Bestellung, Ausschreibung, Lieferschein (BT-11 bis BT-18)
Vollständige Adressen aller Parteien mit allen Unterfeldern (BT-35 bis BT-43, BT-50 bis BT-58)
Steuerlicher Vertreter komplett (BT-62 bis BT-69)
Abweichender Zahlungsempfänger (BT-59 bis BT-61)
Lieferanschrift vollständig (BT-70 bis BT-80)
Alle Zahlungsmittel inkl. Kreditkarte und Lastschrift (BT-81 bis BT-91)
Nachlässe und Zuschläge auf Dokument- und Positionsebene (BT-92 bis BT-105)
Erweiterte Positionsfelder: Preise, Eigenschaften, Klassifizierungen (BT-136 bis BT-161)

EXTENDED (neu ergänzt, u.a.):

GLN-Kennungen für Verkäufer/Käufer/Lieferort (BT-X-1 bis BT-X-3)
Skonto-Felder mit Betrag/Prozent/Frist (BT-X-4 bis BT-X-6)
Unterpositionen und hierarchische Positionsstruktur (BT-X-7/8)
Vorauszahlungen mit Betrag/Datum/Referenz (BT-X-9 bis BT-X-11)
Lieferscheinreferenzen auf Kopf- und Positionsebene (BT-X-12/13)
Positionsstatus und Liefermengen (BT-X-14/15)

# Post to API from VUE Component

```
    // Send the data to the backend
    const response = await fetch("http://localhost:8000/invoice-items/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(invoiceItems),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log("Upload successful:", result);

    // You can add user feedback here, e.g., show a success message
    alert("Data uploaded successfully!");
  } catch (error) {
    console.error("Error uploading data:", error);
    // You can add user feedback here, e.g., show an error message
    alert("Error uploading data. Please try again.");
  }
```
