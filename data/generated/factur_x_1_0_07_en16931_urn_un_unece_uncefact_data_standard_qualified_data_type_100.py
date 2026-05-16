from __future__ import annotations
from dataclasses import dataclass, field

__NAMESPACE__ = "urn:un:unece:uncefact:data:standard:QualifiedDataType:100"


@dataclass(kw_only=True)
class AllowanceChargeReasonCodeType:
    value: str = field(
        default=''
    )
@dataclass(kw_only=True)
class CountryIdtype:
    class Meta:
        name = "CountryIDType"

    value: str = field(
        default=''
    )
@dataclass(kw_only=True)
class CurrencyCodeType:
    value: str = field(
        default=''
    )
@dataclass(kw_only=True)
class DocumentCodeType:
    value: str = field(
        default=''
    )
@dataclass(kw_only=True)
class FormattedDateTimeType:
    date_time_string: FormattedDateTimeType.DateTimeString = field(
        metadata={
            "name": "DateTimeString",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:QualifiedDataType:100",
        }
    )

    @dataclass(kw_only=True)
    class DateTimeString:
        value: str = field(
            default=''
        )
        format: str = field(
            metadata={
                "type": "Attribute",
            }
        )
@dataclass(kw_only=True)
class PaymentMeansCodeType:
    value: str = field(
        default=''
    )
@dataclass(kw_only=True)
class ReferenceCodeType:
    value: str = field(
        default=''
    )
@dataclass(kw_only=True)
class TaxCategoryCodeType:
    value: str = field(
        default=''
    )
@dataclass(kw_only=True)
class TaxTypeCodeType:
    value: str = field(
        default=''
    )
@dataclass(kw_only=True)
class TimeReferenceCodeType:
    value: str = field(
        default=''
    )