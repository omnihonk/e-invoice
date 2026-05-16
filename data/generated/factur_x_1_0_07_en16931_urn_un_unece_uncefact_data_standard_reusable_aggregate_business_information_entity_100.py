from __future__ import annotations
from dataclasses import dataclass, field
from generated.factur_x_1_0_07_en16931_urn_un_unece_uncefact_data_standard_qualified_data_type_100 import (
    AllowanceChargeReasonCodeType,
    CountryIdtype,
    CurrencyCodeType,
    DocumentCodeType,
    FormattedDateTimeType,
    PaymentMeansCodeType,
    ReferenceCodeType,
    TaxCategoryCodeType,
    TaxTypeCodeType,
    TimeReferenceCodeType,
)
from generated.factur_x_1_0_07_en16931_urn_un_unece_uncefact_data_standard_unqualified_data_type_100 import (
    AmountType,
    BinaryObjectType,
    CodeType,
    DateTimeType,
    DateType,
    Idtype,
    IndicatorType,
    PercentType,
    QuantityType,
    TextType,
)

__NAMESPACE__ = "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"


@dataclass(kw_only=True)
class CreditorFinancialAccountType:
    ibanid: None | Idtype = field(
        default=None,
        metadata={
            "name": "IBANID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    account_name: None | TextType = field(
        default=None,
        metadata={
            "name": "AccountName",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    proprietary_id: None | Idtype = field(
        default=None,
        metadata={
            "name": "ProprietaryID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class CreditorFinancialInstitutionType:
    bicid: Idtype = field(
        metadata={
            "name": "BICID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class DebtorFinancialAccountType:
    ibanid: Idtype = field(
        metadata={
            "name": "IBANID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class DocumentContextParameterType:
    id: Idtype = field(
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class LegalOrganizationType:
    id: None | Idtype = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    trading_business_name: None | TextType = field(
        default=None,
        metadata={
            "name": "TradingBusinessName",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class LineTradeDeliveryType:
    billed_quantity: QuantityType = field(
        metadata={
            "name": "BilledQuantity",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class NoteType:
    content: TextType = field(
        metadata={
            "name": "Content",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    subject_code: None | CodeType = field(
        default=None,
        metadata={
            "name": "SubjectCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class ProcuringProjectType:
    id: Idtype = field(
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    name: TextType = field(
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class ProductCharacteristicType:
    description: TextType = field(
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    value: TextType = field(
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class ProductClassificationType:
    class_code: None | CodeType = field(
        default=None,
        metadata={
            "name": "ClassCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class ReferencedDocumentType:
    issuer_assigned_id: None | Idtype = field(
        default=None,
        metadata={
            "name": "IssuerAssignedID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    uriid: None | Idtype = field(
        default=None,
        metadata={
            "name": "URIID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    line_id: None | Idtype = field(
        default=None,
        metadata={
            "name": "LineID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    type_code: None | DocumentCodeType = field(
        default=None,
        metadata={
            "name": "TypeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    name: None | TextType = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    attachment_binary_object: None | BinaryObjectType = field(
        default=None,
        metadata={
            "name": "AttachmentBinaryObject",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    reference_type_code: None | ReferenceCodeType = field(
        default=None,
        metadata={
            "name": "ReferenceTypeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    formatted_issue_date_time: None | FormattedDateTimeType = field(
        default=None,
        metadata={
            "name": "FormattedIssueDateTime",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class SpecifiedPeriodType:
    start_date_time: None | DateTimeType = field(
        default=None,
        metadata={
            "name": "StartDateTime",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    end_date_time: None | DateTimeType = field(
        default=None,
        metadata={
            "name": "EndDateTime",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class SupplyChainEventType:
    occurrence_date_time: DateTimeType = field(
        metadata={
            "name": "OccurrenceDateTime",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class TaxRegistrationType:
    id: Idtype = field(
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class TradeAccountingAccountType:
    id: Idtype = field(
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class TradeAddressType:
    postcode_code: None | CodeType = field(
        default=None,
        metadata={
            "name": "PostcodeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    line_one: None | TextType = field(
        default=None,
        metadata={
            "name": "LineOne",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    line_two: None | TextType = field(
        default=None,
        metadata={
            "name": "LineTwo",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    line_three: None | TextType = field(
        default=None,
        metadata={
            "name": "LineThree",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    city_name: None | TextType = field(
        default=None,
        metadata={
            "name": "CityName",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    country_id: CountryIdtype = field(
        metadata={
            "name": "CountryID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    country_sub_division_name: None | TextType = field(
        default=None,
        metadata={
            "name": "CountrySubDivisionName",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class TradeCountryType:
    id: CountryIdtype = field(
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class TradePaymentTermsType:
    description: None | TextType = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    due_date_date_time: None | DateTimeType = field(
        default=None,
        metadata={
            "name": "DueDateDateTime",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    direct_debit_mandate_id: None | Idtype = field(
        default=None,
        metadata={
            "name": "DirectDebitMandateID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class TradeSettlementFinancialCardType:
    id: Idtype = field(
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    cardholder_name: None | TextType = field(
        default=None,
        metadata={
            "name": "CardholderName",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class TradeSettlementHeaderMonetarySummationType:
    line_total_amount: AmountType = field(
        metadata={
            "name": "LineTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    charge_total_amount: None | AmountType = field(
        default=None,
        metadata={
            "name": "ChargeTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    allowance_total_amount: None | AmountType = field(
        default=None,
        metadata={
            "name": "AllowanceTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    tax_basis_total_amount: AmountType = field(
        metadata={
            "name": "TaxBasisTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    tax_total_amount: list[AmountType] = field(
        default_factory=list,
        metadata={
            "name": "TaxTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "max_occurs": 2,
        }
    )
    rounding_amount: None | AmountType = field(
        default=None,
        metadata={
            "name": "RoundingAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    grand_total_amount: AmountType = field(
        metadata={
            "name": "GrandTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    total_prepaid_amount: None | AmountType = field(
        default=None,
        metadata={
            "name": "TotalPrepaidAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    due_payable_amount: AmountType = field(
        metadata={
            "name": "DuePayableAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class TradeSettlementLineMonetarySummationType:
    line_total_amount: AmountType = field(
        metadata={
            "name": "LineTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class TradeTaxType:
    calculated_amount: None | AmountType = field(
        default=None,
        metadata={
            "name": "CalculatedAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    type_code: TaxTypeCodeType = field(
        metadata={
            "name": "TypeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    exemption_reason: None | TextType = field(
        default=None,
        metadata={
            "name": "ExemptionReason",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    basis_amount: None | AmountType = field(
        default=None,
        metadata={
            "name": "BasisAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    category_code: TaxCategoryCodeType = field(
        metadata={
            "name": "CategoryCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    exemption_reason_code: None | CodeType = field(
        default=None,
        metadata={
            "name": "ExemptionReasonCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    tax_point_date: None | DateType = field(
        default=None,
        metadata={
            "name": "TaxPointDate",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    due_date_type_code: None | TimeReferenceCodeType = field(
        default=None,
        metadata={
            "name": "DueDateTypeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    rate_applicable_percent: None | PercentType = field(
        default=None,
        metadata={
            "name": "RateApplicablePercent",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class UniversalCommunicationType:
    uriid: None | Idtype = field(
        default=None,
        metadata={
            "name": "URIID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    complete_number: None | TextType = field(
        default=None,
        metadata={
            "name": "CompleteNumber",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class DocumentLineDocumentType:
    line_id: Idtype = field(
        metadata={
            "name": "LineID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    included_note: None | NoteType = field(
        default=None,
        metadata={
            "name": "IncludedNote",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class ExchangedDocumentContextType:
    business_process_specified_document_context_parameter: None | DocumentContextParameterType = field(
        default=None,
        metadata={
            "name": "BusinessProcessSpecifiedDocumentContextParameter",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    guideline_specified_document_context_parameter: DocumentContextParameterType = field(
        metadata={
            "name": "GuidelineSpecifiedDocumentContextParameter",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class ExchangedDocumentType:
    id: Idtype = field(
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    type_code: DocumentCodeType = field(
        metadata={
            "name": "TypeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    issue_date_time: DateTimeType = field(
        metadata={
            "name": "IssueDateTime",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    included_note: list[NoteType] = field(
        default_factory=list,
        metadata={
            "name": "IncludedNote",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class TradeAllowanceChargeType:
    charge_indicator: IndicatorType = field(
        metadata={
            "name": "ChargeIndicator",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    calculation_percent: None | PercentType = field(
        default=None,
        metadata={
            "name": "CalculationPercent",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    basis_amount: None | AmountType = field(
        default=None,
        metadata={
            "name": "BasisAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    actual_amount: AmountType = field(
        metadata={
            "name": "ActualAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    reason_code: None | AllowanceChargeReasonCodeType = field(
        default=None,
        metadata={
            "name": "ReasonCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    reason: None | TextType = field(
        default=None,
        metadata={
            "name": "Reason",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    category_trade_tax: None | TradeTaxType = field(
        default=None,
        metadata={
            "name": "CategoryTradeTax",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class TradeContactType:
    person_name: None | TextType = field(
        default=None,
        metadata={
            "name": "PersonName",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    department_name: None | TextType = field(
        default=None,
        metadata={
            "name": "DepartmentName",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    telephone_universal_communication: None | UniversalCommunicationType = field(
        default=None,
        metadata={
            "name": "TelephoneUniversalCommunication",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    email_uriuniversal_communication: None | UniversalCommunicationType = field(
        default=None,
        metadata={
            "name": "EmailURIUniversalCommunication",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class TradeProductType:
    global_id: None | Idtype = field(
        default=None,
        metadata={
            "name": "GlobalID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    seller_assigned_id: None | Idtype = field(
        default=None,
        metadata={
            "name": "SellerAssignedID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    buyer_assigned_id: None | Idtype = field(
        default=None,
        metadata={
            "name": "BuyerAssignedID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    name: TextType = field(
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    description: None | TextType = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    applicable_product_characteristic: list[ProductCharacteristicType] = field(
        default_factory=list,
        metadata={
            "name": "ApplicableProductCharacteristic",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    designated_product_classification: list[ProductClassificationType] = field(
        default_factory=list,
        metadata={
            "name": "DesignatedProductClassification",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    origin_trade_country: None | TradeCountryType = field(
        default=None,
        metadata={
            "name": "OriginTradeCountry",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class TradeSettlementPaymentMeansType:
    type_code: PaymentMeansCodeType = field(
        metadata={
            "name": "TypeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    information: None | TextType = field(
        default=None,
        metadata={
            "name": "Information",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    applicable_trade_settlement_financial_card: None | TradeSettlementFinancialCardType = field(
        default=None,
        metadata={
            "name": "ApplicableTradeSettlementFinancialCard",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    payer_party_debtor_financial_account: None | DebtorFinancialAccountType = field(
        default=None,
        metadata={
            "name": "PayerPartyDebtorFinancialAccount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    payee_party_creditor_financial_account: None | CreditorFinancialAccountType = field(
        default=None,
        metadata={
            "name": "PayeePartyCreditorFinancialAccount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    payee_specified_creditor_financial_institution: None | CreditorFinancialInstitutionType = field(
        default=None,
        metadata={
            "name": "PayeeSpecifiedCreditorFinancialInstitution",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class LineTradeSettlementType:
    applicable_trade_tax: TradeTaxType = field(
        metadata={
            "name": "ApplicableTradeTax",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    billing_specified_period: None | SpecifiedPeriodType = field(
        default=None,
        metadata={
            "name": "BillingSpecifiedPeriod",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    specified_trade_allowance_charge: list[TradeAllowanceChargeType] = field(
        default_factory=list,
        metadata={
            "name": "SpecifiedTradeAllowanceCharge",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    specified_trade_settlement_line_monetary_summation: TradeSettlementLineMonetarySummationType = field(
        metadata={
            "name": "SpecifiedTradeSettlementLineMonetarySummation",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    additional_referenced_document: None | ReferencedDocumentType = field(
        default=None,
        metadata={
            "name": "AdditionalReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    receivable_specified_trade_accounting_account: None | TradeAccountingAccountType = field(
        default=None,
        metadata={
            "name": "ReceivableSpecifiedTradeAccountingAccount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class TradePartyType:
    id: list[Idtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    global_id: list[Idtype] = field(
        default_factory=list,
        metadata={
            "name": "GlobalID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    name: None | TextType = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    description: None | TextType = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    specified_legal_organization: None | LegalOrganizationType = field(
        default=None,
        metadata={
            "name": "SpecifiedLegalOrganization",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    defined_trade_contact: None | TradeContactType = field(
        default=None,
        metadata={
            "name": "DefinedTradeContact",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    postal_trade_address: None | TradeAddressType = field(
        default=None,
        metadata={
            "name": "PostalTradeAddress",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    uriuniversal_communication: None | UniversalCommunicationType = field(
        default=None,
        metadata={
            "name": "URIUniversalCommunication",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    specified_tax_registration: list[TaxRegistrationType] = field(
        default_factory=list,
        metadata={
            "name": "SpecifiedTaxRegistration",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "max_occurs": 2,
        }
    )
@dataclass(kw_only=True)
class TradePriceType:
    charge_amount: AmountType = field(
        metadata={
            "name": "ChargeAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    basis_quantity: None | QuantityType = field(
        default=None,
        metadata={
            "name": "BasisQuantity",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    applied_trade_allowance_charge: None | TradeAllowanceChargeType = field(
        default=None,
        metadata={
            "name": "AppliedTradeAllowanceCharge",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class HeaderTradeAgreementType:
    buyer_reference: None | TextType = field(
        default=None,
        metadata={
            "name": "BuyerReference",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    seller_trade_party: TradePartyType = field(
        metadata={
            "name": "SellerTradeParty",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    buyer_trade_party: TradePartyType = field(
        metadata={
            "name": "BuyerTradeParty",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    seller_tax_representative_trade_party: None | TradePartyType = field(
        default=None,
        metadata={
            "name": "SellerTaxRepresentativeTradeParty",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    seller_order_referenced_document: None | ReferencedDocumentType = field(
        default=None,
        metadata={
            "name": "SellerOrderReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    buyer_order_referenced_document: None | ReferencedDocumentType = field(
        default=None,
        metadata={
            "name": "BuyerOrderReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    contract_referenced_document: None | ReferencedDocumentType = field(
        default=None,
        metadata={
            "name": "ContractReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    additional_referenced_document: list[ReferencedDocumentType] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    specified_procuring_project: None | ProcuringProjectType = field(
        default=None,
        metadata={
            "name": "SpecifiedProcuringProject",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class HeaderTradeDeliveryType:
    ship_to_trade_party: None | TradePartyType = field(
        default=None,
        metadata={
            "name": "ShipToTradeParty",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    actual_delivery_supply_chain_event: None | SupplyChainEventType = field(
        default=None,
        metadata={
            "name": "ActualDeliverySupplyChainEvent",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    despatch_advice_referenced_document: None | ReferencedDocumentType = field(
        default=None,
        metadata={
            "name": "DespatchAdviceReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    receiving_advice_referenced_document: None | ReferencedDocumentType = field(
        default=None,
        metadata={
            "name": "ReceivingAdviceReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class HeaderTradeSettlementType:
    creditor_reference_id: None | Idtype = field(
        default=None,
        metadata={
            "name": "CreditorReferenceID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    payment_reference: None | TextType = field(
        default=None,
        metadata={
            "name": "PaymentReference",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    tax_currency_code: None | CurrencyCodeType = field(
        default=None,
        metadata={
            "name": "TaxCurrencyCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    invoice_currency_code: CurrencyCodeType = field(
        metadata={
            "name": "InvoiceCurrencyCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    payee_trade_party: None | TradePartyType = field(
        default=None,
        metadata={
            "name": "PayeeTradeParty",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    specified_trade_settlement_payment_means: list[TradeSettlementPaymentMeansType] = field(
        default_factory=list,
        metadata={
            "name": "SpecifiedTradeSettlementPaymentMeans",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    applicable_trade_tax: list[TradeTaxType] = field(
        default_factory=list,
        metadata={
            "name": "ApplicableTradeTax",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "min_occurs": 1,
        }
    )
    billing_specified_period: None | SpecifiedPeriodType = field(
        default=None,
        metadata={
            "name": "BillingSpecifiedPeriod",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    specified_trade_allowance_charge: list[TradeAllowanceChargeType] = field(
        default_factory=list,
        metadata={
            "name": "SpecifiedTradeAllowanceCharge",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    specified_trade_payment_terms: None | TradePaymentTermsType = field(
        default=None,
        metadata={
            "name": "SpecifiedTradePaymentTerms",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    specified_trade_settlement_header_monetary_summation: TradeSettlementHeaderMonetarySummationType = field(
        metadata={
            "name": "SpecifiedTradeSettlementHeaderMonetarySummation",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    invoice_referenced_document: list[ReferencedDocumentType] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    receivable_specified_trade_accounting_account: None | TradeAccountingAccountType = field(
        default=None,
        metadata={
            "name": "ReceivableSpecifiedTradeAccountingAccount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class LineTradeAgreementType:
    buyer_order_referenced_document: None | ReferencedDocumentType = field(
        default=None,
        metadata={
            "name": "BuyerOrderReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    gross_price_product_trade_price: None | TradePriceType = field(
        default=None,
        metadata={
            "name": "GrossPriceProductTradePrice",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    net_price_product_trade_price: TradePriceType = field(
        metadata={
            "name": "NetPriceProductTradePrice",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class SupplyChainTradeLineItemType:
    associated_document_line_document: DocumentLineDocumentType = field(
        metadata={
            "name": "AssociatedDocumentLineDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    specified_trade_product: TradeProductType = field(
        metadata={
            "name": "SpecifiedTradeProduct",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    specified_line_trade_agreement: LineTradeAgreementType = field(
        metadata={
            "name": "SpecifiedLineTradeAgreement",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    specified_line_trade_delivery: LineTradeDeliveryType = field(
        metadata={
            "name": "SpecifiedLineTradeDelivery",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    specified_line_trade_settlement: LineTradeSettlementType = field(
        metadata={
            "name": "SpecifiedLineTradeSettlement",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
@dataclass(kw_only=True)
class SupplyChainTradeTransactionType:
    included_supply_chain_trade_line_item: list[SupplyChainTradeLineItemType] = field(
        default_factory=list,
        metadata={
            "name": "IncludedSupplyChainTradeLineItem",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "min_occurs": 1,
        }
    )
    applicable_header_trade_agreement: HeaderTradeAgreementType = field(
        metadata={
            "name": "ApplicableHeaderTradeAgreement",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    applicable_header_trade_delivery: HeaderTradeDeliveryType = field(
        metadata={
            "name": "ApplicableHeaderTradeDelivery",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )
    applicable_header_trade_settlement: HeaderTradeSettlementType = field(
        metadata={
            "name": "ApplicableHeaderTradeSettlement",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        }
    )