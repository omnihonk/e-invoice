


# class BillingSpecifiedPeriod(SQLModel, table=True):
#     __tablename__ = "billing_specified_period"

#     id: Optional[int] = Field(default=None, primary_key=True)
#     description: Optional[str] = Field(default=None, description="Freitext der Zahlungsbedingungen")
#     start: datetime = Field(nullable=False)
#     end: datetime = Field(nullable=False)

#     # Relationship
#     trade_settlement_header_monetary_summation: Optional["TradeSettlementHeaderMonetarySummation"] = Relationship(back_populates="billing_specified_period")
    
# class ApplicableTradeTax(SQLModel, table=True):
#     __tablename__ = "applicable_trade_tax"

#     id: Optional[int] = Field(default=None, primary_key=True)
#     calculated_amount: Optional[float] = Field(default=None, decimal_places=2,scription="Steuerbetrag")
#     type_code: Optional[str] = Field(default=None, description="Steuerart (Code)")
#     exemption_reason: Optional[str] = Field(default=None, description="Grund der Steuerbefreiung (Freitext)")
#     basis_amount: Optional[float] = Field(default=None, description="Basisbetrag der Steuerberechnung")
#     line_total_basis_amount: Optional[float] = Field(default=None, description="Warenbetrag des Steuersatzes")
#     allowance_charge_basis_amount: Optional[float] = Field(default=None, description="Zuschlags-/Abschlagsbetrag des Steuersatzes")
#     rate_applicable_percent: Optional[float] = Field(default=None, description="Steuersatz in Prozent")
#     category_code: Optional[str] = Field(default=None, description="Steuerkategorie (Code)")
#     exemption_reason_code: Optional[str] = Field(default=None, description="Grund der Steuerbefreiung (Code)")
#     tax_point_date: Optional[datetime] = Field(default=None, description="Steuerdatum")
#     due_date_type_code: Optional[str] = Field(default=None, description="Fälligkeitsdatumstyp (Code)")
#     tax_category_code: Optional[str] = Field(default=None, description="Steuerkategorie (Code)")
#     tax_type_code: Optional[str] = Field(default=None, description="Steuerart (Code)")
#     tax_currency_code: Optional[str] = Field(default=None, description="Steuerwährung (Code)")
#     tax_basis_amount: Optional[float] = Field(default=None, description="Steuerbasisbetrag")
#     tax_calculated_amount: Optional[float] = Field(default=None, description="Steuerberechneter Betrag")
#     tax_percent: Optional[float] = Field(default=None, description="Steuerprozentsatz")
#     tax_exemption_reason: Optional[str] = Field(default=None, description="Grund der Steuerbefreiung (Freitext)")
#     tax_exemption_reason_code: Optional[str] = Field(default=None, description="Grund der Steuerbefreiung (Code)")
#     tax_exemption_basis_amount: Optional[float] = Field(default=None, description="Steuerbefreiungsgrundbetrag")
#     tax_exemption_basis_percent: Optional[float] = Field(default=None, description="Steuerbefreiungsgrundprozentsatz")
    
#     # Relationship
#     trade_settlement_header_monetary_summation: Optional["TradeSettlementHeaderMonetarySummation"] = Relationship(back_populates="applicable_trade_tax")    

# class TradeAllowanceCharge(SQLModel, table=True):
#     __tablename__ = "trade_allowance_charge"
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     indicator: Optional[bool] = Field(default=False, description="Schalter für Zu-/Abschlag")
#     sequence_numeric: Optional[int] = Field(default=None, description="Berechnungsreihenfolge")
#     calculation_percent: Optional[float] = Field(default=None, description="Rabatt in Prozent")
#     basis_amount: Optional[float] = Field(default=None, description="Basisbetrag des Rabatts")
#     basis_quantity: Optional[float] = Field(default=None, description="Basismenge des Rabatts")
#     actual_amount: Optional[float] = Field(default=None, description="Tatsächlicher Rabattbetrag")
#     reason_code: Optional[str] = Field(default=None, description="Grund des Rabatts (Code)")
#     reason: Optional[str] = Field(default=None, description="Grund des Rabatts (Freitext)")
#     category_trade_tax: Optional["CategoryTradeTax"] = Relationship(back_populates="trade_allowance_charge")
#     billing_specified_period: Optional["BillingSpecifiedPeriod"] = Relationship(back_populates="trade_allowance_charge")
    
# class TradeSettlementHeaderMonetarySummation(SQLModel, table=True):
#     __tablename__ = "trade_settlement_header_monetary_summation"
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     line_total_amount: Optional[float] = Field(default=None, description="Summe der Zeilenbeträge")
#     charge_total_amount: Optional[float] = Field(default=None, description="Summe der Zuschläge")
#     allowance_total_amount: Optional[float] = Field(default=None, description="Summe der Abschläge")
#     tax_basis_total_amount: Optional[float] = Field(default=None, description="Summe der Steuerbasen")
#     tax_total_amount: Optional[float] = Field(default=None, description="Summe der Steuern")
#     rounding_amount: Optional[float] = Field(default=None, description="Rundungsbetrag")
#     grand_total_amount: Optional[float] = Field(default=None, description="Gesamtbetrag")
#     total_prepaid_amount: Optional[float] = Field(default=None, description="Vorauszahlungsbetrag")
#     due_payable_amount: Optional[float] = Field(default=None, description="Fälliger Betrag")
    
#     # Relationships
#     billing_specified_period: Optional["BillingSpecifiedPeriod"] = Relationship(back_populates="trade_settlement_header_monetary_summation")
#     applicable_trade_tax: Optional["ApplicableTradeTax"] = Relationship(back_populates="trade_settlement_header_monetary_summation")
#     specified_trade_settlement_payment_means: Optional["SpecifiedTradeSettlementPaymentMeans"] = Relationship(back_populates="trade_settlement_header_monetary_summation")
#     specified_trade_settlement_monetary_summation: Optional["SpecifiedTradeSettlementMonetarySummation"] = Relationship(back_populates="trade_settlement_header_monetary_summation")
#     specified_trade_settlement_payment_means: Optional["SpecifiedTradeSettlementPaymentMeans"] = Relationship(back_populates="trade_settlement_header_monetary_summation")
#     specified_trade_settlement_monetary_summation: Optional["SpecifiedTradeSettlementMonetarySummation"] = Relationship(back_populates="trade_settlement_header_monetary_summation")
    