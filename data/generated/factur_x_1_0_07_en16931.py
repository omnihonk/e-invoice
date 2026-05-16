from __future__ import annotations
from dataclasses import dataclass, field
from generated.factur_x_1_0_07_en16931_urn_un_unece_uncefact_data_standard_reusable_aggregate_business_information_entity_100 import (
    ExchangedDocumentContextType,
    ExchangedDocumentType,
    SupplyChainTradeTransactionType,
)

__NAMESPACE__ = "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100"


@dataclass(kw_only=True)
class CrossIndustryInvoiceType:
    exchanged_document_context: ExchangedDocumentContextType = field(
        metadata={
            "name": "ExchangedDocumentContext",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
        }
    )
    exchanged_document: ExchangedDocumentType = field(
        metadata={
            "name": "ExchangedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
        }
    )
    supply_chain_trade_transaction: SupplyChainTradeTransactionType = field(
        metadata={
            "name": "SupplyChainTradeTransaction",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
        }
    )
@dataclass(kw_only=True)
class CrossIndustryInvoice(CrossIndustryInvoiceType):
    class Meta:
        namespace = "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100"