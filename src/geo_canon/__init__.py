"""
GeoCanon — Global-ready Django apps from day one.

Jurisdictions, dial codes, flags, holidays, timezones, languages & more.

Quick start::

    from geo_canon import (
        get_jurisdiction_choices,
        get_dial_code,
        get_flag_css_class,
        get_current_local_time,
        get_language_for_jurisdiction,
        format_duration,
    )
"""

from __future__ import annotations

__version__ = "0.1.0"

# ---------------------------------------------------------------------------
# Jurisdictions
# ---------------------------------------------------------------------------
from .jurisdictions import (
    JURISDICTION_NAMES,
    JURISDICTIONS,
    get_jurisdiction_choices,
    is_valid_jurisdiction,
)

# ---------------------------------------------------------------------------
# Dial codes
# ---------------------------------------------------------------------------
from .dial_codes import (
    COUNTRY_DIAL_CODE,
    DIAL_CODE_CHOICES,
    get_dial_code,
    get_dial_code_choices,
    validate_phone,
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
# Timezones
# ---------------------------------------------------------------------------
from .timezones import (
    TIMEZONE_MAP,
    get_current_local_time,
    get_timezone_for_jurisdiction,
    get_timezone_name,
)

# ---------------------------------------------------------------------------
# Duration
# ---------------------------------------------------------------------------
from .duration import format_duration

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
# Settings
# ---------------------------------------------------------------------------
from .settings import GeoCanonSettings, get_geocanon_settings

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
    # Flags
    "FLAG_CSS_CLASS",
    "get_flag_css_class",
    "get_country_by_iso",
    "annotate_flag_class",
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
