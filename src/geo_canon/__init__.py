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

__version__ = "1.0.0"

# ---------------------------------------------------------------------------
# Jurisdictions
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Address formats
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Currencies
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Dial codes
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Duration
# ---------------------------------------------------------------------------
from .duration import format_duration

# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------
from .exceptions import (
    ConfigurationError,
    DialCodeNotFoundError,
    GeoCanonError,
    HolidaysNotAvailableError,
    JurisdictionNotFoundError,
    PhoneValidationError,
    TimezoneNotFoundError,
)

# ---------------------------------------------------------------------------
# Flags
# ---------------------------------------------------------------------------
from .flags import (
    FLAG_CSS_CLASS,
    annotate_flag_class,
    get_country_by_iso,
    get_flag_css_class,
)

# ---------------------------------------------------------------------------
# ISO country codes
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Languages
# ---------------------------------------------------------------------------
from .languages import (
    JURISDICTION_LANGUAGE,
    LANGUAGE_CHOICES,
    get_language_choices,
    get_language_for_jurisdiction,
)

# ---------------------------------------------------------------------------
# Locale formatting
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
from .settings import GeoCanonSettings, get_geocanon_settings

# ---------------------------------------------------------------------------
# Timezones
# ---------------------------------------------------------------------------
from .timezones import (
    TIMEZONE_MAP,
    get_current_local_time,
    get_timezone_for_jurisdiction,
    get_timezone_name,
)

# Holidays are optional — only export when the extra is installed
try:
    from .holidays import (
        get_holidays_for_year,
        get_supported_holiday_jurisdictions,
        is_public_holiday,
    )
except ImportError:
    pass

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
