"""
GeoCanon — Public Holidays

Jurisdiction-aware public holiday detection powered by the ``holidays``
library (optional dependency, install via ``pip install "GeoCanon[holidays]"``).
"""

from __future__ import annotations

import datetime
from typing import Any

from ..exceptions import HolidaysNotAvailableError

try:
    import holidays as _holidays_lib

    _HAS_HOLIDAYS = True
except ImportError:
    _holidays_lib = None  # type: ignore[assignment]
    _HAS_HOLIDAYS = False


def _require_holidays() -> None:
    if not _HAS_HOLIDAYS:
        raise HolidaysNotAvailableError()


# ---------------------------------------------------------------------------
# Jurisdiction name → holidays country class
# ---------------------------------------------------------------------------


def _build_registry() -> dict[str, Any]:
    """
    Map every name in :mod:`geo_canon.iso_codes` to its ``holidays`` country class.

    The class is looked up by ISO 3166-1 alpha-2 code, so canonical names and
    their legacy aliases share one calendar. Countries the installed
    ``holidays`` release does not cover are left out instead of failing.
    """
    if not _HAS_HOLIDAYS:
        return {}

    from ..iso_codes import JURISDICTION_ISO

    supported = _holidays_lib.list_supported_countries()
    return {
        name: getattr(_holidays_lib, info.alpha_2)
        for name, info in JURISDICTION_ISO.items()
        if info.alpha_2 in supported
    }


# Lazy singleton
_registry: dict[str, Any] | None = None


def _get_registry() -> dict[str, Any]:
    global _registry
    if _registry is None:
        _registry = _build_registry()
    return _registry


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def is_public_holiday(
    jurisdiction: str,
    date: datetime.date | None = None,
    *,
    year: int | None = None,
) -> bool:
    """
    Check whether *date* is a public holiday in *jurisdiction*.

    Uses today when *date* is ``None``.

    >>> from geo_canon.holidays import is_public_holiday
    >>> is_public_holiday("Romania", datetime.date(2025, 12, 25))
    True
    """
    _require_holidays()
    date = date or datetime.date.today()
    year = year or date.year
    registry = _get_registry()

    holiday_factory = registry.get(jurisdiction)
    if holiday_factory is None:
        return False

    country_holidays = holiday_factory(years=year)
    return date in country_holidays


def get_holidays_for_year(
    jurisdiction: str,
    year: int | None = None,
) -> dict[datetime.date, str]:
    """
    Return all public holidays for *jurisdiction* in *year* as ``{date: name}``.

    Defaults to the current year when *year* is ``None``.
    """
    _require_holidays()
    year = year or datetime.date.today().year
    registry = _get_registry()

    holiday_factory = registry.get(jurisdiction)
    if holiday_factory is None:
        return {}

    country_holidays = holiday_factory(years=year)
    return dict(country_holidays.items())


def get_supported_holiday_jurisdictions() -> list[str]:
    """
    Return the names that have holiday support with the installed ``holidays``.

    The list includes the legacy aliases that lookups accept (for example
    ``"South Korea"`` next to ``"Korea (South)"``); filter it with
    :func:`geo_canon.jurisdictions.is_valid_jurisdiction` for canonical names.
    """
    _require_holidays()
    return sorted(_get_registry().keys())
