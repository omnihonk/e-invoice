from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal

__NAMESPACE__ = "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100"


@dataclass(kw_only=True)
class AmountType:
    value: Decimal = field()
    currency_id: None | str = field(
        default=None,
        metadata={
            "name": "currencyID",
            "type": "Attribute",
        }
    )
@dataclass(kw_only=True)
class BinaryObjectType:
    value: bytes = field(
        default=b'',
        metadata={
            "format": "base64",
        }
    )
    mime_code: str = field(
        metadata={
            "name": "mimeCode",
            "type": "Attribute",
        }
    )
    filename: str = field(
        metadata={
            "type": "Attribute",
        }
    )
@dataclass(kw_only=True)
class CodeType:
    value: str = field(
        default=''
    )
    list_id: None | str = field(
        default=None,
        metadata={
            "name": "listID",
            "type": "Attribute",
        }
    )
    list_version_id: None | str = field(
        default=None,
        metadata={
            "name": "listVersionID",
            "type": "Attribute",
        }
    )
@dataclass(kw_only=True)
class DateTimeType:
    date_time_string: None | DateTimeType.DateTimeString = field(
        default=None,
        metadata={
            "name": "DateTimeString",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
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
class DateType:
    date_string: None | DateType.DateString = field(
        default=None,
        metadata={
            "name": "DateString",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
        }
    )

    @dataclass(kw_only=True)
    class DateString:
        value: str = field(
            default=''
        )
        format: str = field(
            metadata={
                "type": "Attribute",
            }
        )
@dataclass(kw_only=True)
class Idtype:
    class Meta:
        name = "IDType"

    value: str = field(
        default=''
    )
    scheme_id: None | str = field(
        default=None,
        metadata={
            "name": "schemeID",
            "type": "Attribute",
        }
    )
@dataclass(kw_only=True)
class IndicatorType:
    indicator: None | bool = field(
        default=None,
        metadata={
            "name": "Indicator",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
        }
    )
@dataclass(kw_only=True)
class PercentType:
    value: Decimal = field()
@dataclass(kw_only=True)
class QuantityType:
    value: Decimal = field()
    unit_code: None | str = field(
        default=None,
        metadata={
            "name": "unitCode",
            "type": "Attribute",
        }
    )
@dataclass(kw_only=True)
class TextType:
    value: str = field(
        default=''
    )