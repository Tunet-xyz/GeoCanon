"""
Jurisdictions, dial codes, flags, ISO codes, timezones, holidays, languages, currencies, and address formats for Django, in one package.

Quick start::

    from geo_canon import (
        get_jurisdiction_choices,
        get_dial_code,
        get_flag_css_class,
        get_current_local_time,
        get_language_for_jurisdiction,
        get_currency_for_jurisdiction,
        format_duration,
    )
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

__version__ = "1.0.0"

# Every public name and the submodule that defines it. Names load on first use
# (PEP 562), so `import geo_canon` and the MCP server do not import Django.
_EXPORTS: dict[str, str] = {
    "JURISDICTION_ADDRESS_FORMAT": "address_formats",
    "AddressFormat": "address_formats",
    "format_address": "address_formats",
    "get_address_format": "address_formats",
    "get_postal_code_label": "address_formats",
    "get_postal_code_regex": "address_formats",
    "get_state_label": "address_formats",
    "is_state_required": "address_formats",
    "validate_postal_code": "address_formats",
    "CURRENCY_BY_CODE": "currencies",
    "CURRENCY_CHOICES": "currencies",
    "JURISDICTION_CURRENCY": "currencies",
    "CurrencyInfo": "currencies",
    "format_currency": "currencies",
    "get_currency_by_code": "currencies",
    "get_currency_choices": "currencies",
    "get_currency_code": "currencies",
    "get_currency_for_jurisdiction": "currencies",
    "get_currency_symbol": "currencies",
    "COUNTRY_DIAL_CODE": "dial_codes",
    "DIAL_CODE_CHOICES": "dial_codes",
    "format_phone_number": "dial_codes",
    "get_dial_code": "dial_codes",
    "get_dial_code_choices": "dial_codes",
    "get_phone_number_type": "dial_codes",
    "is_phone_extra_available": "dial_codes",
    "validate_phone": "dial_codes",
    "validate_phone_number": "dial_codes",
    "format_duration": "duration",
    "ConfigurationError": "exceptions",
    "DialCodeNotFoundError": "exceptions",
    "GeoCanonError": "exceptions",
    "HolidaysNotAvailableError": "exceptions",
    "JurisdictionNotFoundError": "exceptions",
    "PhoneValidationError": "exceptions",
    "TimezoneNotFoundError": "exceptions",
    "FLAG_CSS_CLASS": "flags",
    "annotate_flag_class": "flags",
    "get_country_by_iso": "flags",
    "get_flag_css_class": "flags",
    "get_holidays_for_year": "holidays",
    "get_supported_holiday_jurisdictions": "holidays",
    "is_public_holiday": "holidays",
    "ISO_ALPHA2_TO_JURISDICTION": "iso_codes",
    "ISO_ALPHA3_TO_JURISDICTION": "iso_codes",
    "JURISDICTION_ISO": "iso_codes",
    "ISOCountryInfo": "iso_codes",
    "get_alpha2": "iso_codes",
    "get_alpha3": "iso_codes",
    "get_iso_codes": "iso_codes",
    "get_jurisdiction_by_alpha2": "iso_codes",
    "get_jurisdiction_by_alpha3": "iso_codes",
    "get_numeric_code": "iso_codes",
    "JURISDICTION_NAMES": "jurisdictions",
    "JURISDICTIONS": "jurisdictions",
    "get_jurisdiction_choices": "jurisdictions",
    "is_valid_jurisdiction": "jurisdictions",
    "JURISDICTION_LANGUAGE": "languages",
    "LANGUAGE_CHOICES": "languages",
    "get_language_choices": "languages",
    "get_language_for_jurisdiction": "languages",
    "format_currency_locale": "locale_formats",
    "format_date_locale": "locale_formats",
    "format_datetime_locale": "locale_formats",
    "format_decimal_locale": "locale_formats",
    "format_list_locale": "locale_formats",
    "format_percent_locale": "locale_formats",
    "format_time_locale": "locale_formats",
    "get_locale_for_jurisdiction": "locale_formats",
    "is_locale_extra_available": "locale_formats",
    "GeoCanonSettings": "settings",
    "get_geocanon_settings": "settings",
    "TIMEZONE_MAP": "timezones",
    "get_current_local_time": "timezones",
    "get_timezone_for_jurisdiction": "timezones",
    "get_timezone_name": "timezones",
}

_SUBMODULES = frozenset(
    {
        "address_formats",
        "currencies",
        "dial_codes",
        "duration",
        "exceptions",
        "flags",
        "holidays",
        "iso_codes",
        "jurisdictions",
        "languages",
        "locale_formats",
        "mcp",
        "settings",
        "timezones",
    }
)

__all__ = [
    "__version__",
    # Jurisdictions
    "JURISDICTIONS",
    "JURISDICTION_NAMES",
    "get_jurisdiction_choices",
    "is_valid_jurisdiction",
    # Dial codes
    "DIAL_CODE_CHOICES",
    "COUNTRY_DIAL_CODE",
    "get_dial_code_choices",
    "get_dial_code",
    "validate_phone",
    "is_phone_extra_available",
    "validate_phone_number",
    "format_phone_number",
    "get_phone_number_type",
    # Flags
    "FLAG_CSS_CLASS",
    "get_flag_css_class",
    "get_country_by_iso",
    "annotate_flag_class",
    # ISO country codes
    "JURISDICTION_ISO",
    "ISO_ALPHA2_TO_JURISDICTION",
    "ISO_ALPHA3_TO_JURISDICTION",
    "ISOCountryInfo",
    "get_iso_codes",
    "get_alpha2",
    "get_alpha3",
    "get_numeric_code",
    "get_jurisdiction_by_alpha2",
    "get_jurisdiction_by_alpha3",
    # Timezones
    "TIMEZONE_MAP",
    "get_timezone_name",
    "get_current_local_time",
    "get_timezone_for_jurisdiction",
    # Duration
    "format_duration",
    # Languages
    "LANGUAGE_CHOICES",
    "JURISDICTION_LANGUAGE",
    "get_language_choices",
    "get_language_for_jurisdiction",
    # Currencies
    "JURISDICTION_CURRENCY",
    "CURRENCY_CHOICES",
    "CURRENCY_BY_CODE",
    "CurrencyInfo",
    "get_currency_for_jurisdiction",
    "get_currency_code",
    "get_currency_symbol",
    "get_currency_choices",
    "get_currency_by_code",
    "format_currency",
    # Locale formatting
    "is_locale_extra_available",
    "get_locale_for_jurisdiction",
    "format_decimal_locale",
    "format_percent_locale",
    "format_currency_locale",
    "format_date_locale",
    "format_time_locale",
    "format_datetime_locale",
    "format_list_locale",
    # Address formats
    "JURISDICTION_ADDRESS_FORMAT",
    "AddressFormat",
    "get_address_format",
    "get_postal_code_regex",
    "validate_postal_code",
    "get_state_label",
    "get_postal_code_label",
    "format_address",
    "is_state_required",
    # Settings
    "GeoCanonSettings",
    "get_geocanon_settings",
    # Exceptions
    "GeoCanonError",
    "ConfigurationError",
    "JurisdictionNotFoundError",
    "TimezoneNotFoundError",
    "HolidaysNotAvailableError",
    "DialCodeNotFoundError",
    "PhoneValidationError",
    # Holidays (optional)
    "is_public_holiday",
    "get_holidays_for_year",
    "get_supported_holiday_jurisdictions",
]


def __getattr__(name: str) -> Any:
    if name in _SUBMODULES:
        return import_module(f".{name}", __name__)
    module_name = _EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(import_module(f".{module_name}", __name__), name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_EXPORTS) | _SUBMODULES)


if TYPE_CHECKING:
    from .address_formats import (
        JURISDICTION_ADDRESS_FORMAT,
        AddressFormat,
        format_address,
        get_address_format,
        get_postal_code_label,
        get_postal_code_regex,
        get_state_label,
        is_state_required,
        validate_postal_code,
    )
    from .currencies import (
        CURRENCY_BY_CODE,
        CURRENCY_CHOICES,
        JURISDICTION_CURRENCY,
        CurrencyInfo,
        format_currency,
        get_currency_by_code,
        get_currency_choices,
        get_currency_code,
        get_currency_for_jurisdiction,
        get_currency_symbol,
    )
    from .dial_codes import (
        COUNTRY_DIAL_CODE,
        DIAL_CODE_CHOICES,
        format_phone_number,
        get_dial_code,
        get_dial_code_choices,
        get_phone_number_type,
        is_phone_extra_available,
        validate_phone,
        validate_phone_number,
    )
    from .duration import (
        format_duration,
    )
    from .exceptions import (
        ConfigurationError,
        DialCodeNotFoundError,
        GeoCanonError,
        HolidaysNotAvailableError,
        JurisdictionNotFoundError,
        PhoneValidationError,
        TimezoneNotFoundError,
    )
    from .flags import (
        FLAG_CSS_CLASS,
        annotate_flag_class,
        get_country_by_iso,
        get_flag_css_class,
    )
    from .holidays import (
        get_holidays_for_year,
        get_supported_holiday_jurisdictions,
        is_public_holiday,
    )
    from .iso_codes import (
        ISO_ALPHA2_TO_JURISDICTION,
        ISO_ALPHA3_TO_JURISDICTION,
        JURISDICTION_ISO,
        ISOCountryInfo,
        get_alpha2,
        get_alpha3,
        get_iso_codes,
        get_jurisdiction_by_alpha2,
        get_jurisdiction_by_alpha3,
        get_numeric_code,
    )
    from .jurisdictions import (
        JURISDICTION_NAMES,
        JURISDICTIONS,
        get_jurisdiction_choices,
        is_valid_jurisdiction,
    )
    from .languages import (
        JURISDICTION_LANGUAGE,
        LANGUAGE_CHOICES,
        get_language_choices,
        get_language_for_jurisdiction,
    )
    from .locale_formats import (
        format_currency_locale,
        format_date_locale,
        format_datetime_locale,
        format_decimal_locale,
        format_list_locale,
        format_percent_locale,
        format_time_locale,
        get_locale_for_jurisdiction,
        is_locale_extra_available,
    )
    from .settings import (
        GeoCanonSettings,
        get_geocanon_settings,
    )
    from .timezones import (
        TIMEZONE_MAP,
        get_current_local_time,
        get_timezone_for_jurisdiction,
        get_timezone_name,
    )
