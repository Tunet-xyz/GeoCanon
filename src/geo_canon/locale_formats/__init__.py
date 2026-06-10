"""
GeoCanon - Locale Formatting

Optional Babel-backed helpers for formatting numbers, currencies, dates,
times, datetimes, percentages, and lists for a jurisdiction.
"""

from __future__ import annotations

import datetime as _datetime
from collections.abc import Iterable
from decimal import Decimal

try:
    from babel import dates as _babel_dates
    from babel import lists as _babel_lists
    from babel import numbers as _babel_numbers
    from babel.core import UnknownLocaleError
except ImportError:  # pragma: no cover - exercised by fallback tests
    _babel_dates = None
    _babel_lists = None
    _babel_numbers = None

    class UnknownLocaleError(Exception):  # type: ignore[no-redef]
        """Fallback exception used when Babel is not installed."""

from geo_canon.currencies import format_currency, get_currency_code
from geo_canon.iso_codes import get_alpha2
from geo_canon.languages import get_language_for_jurisdiction


def is_locale_extra_available() -> bool:
    """Return whether the optional ``Babel`` dependency is installed."""
    return _babel_numbers is not None and _babel_dates is not None and _babel_lists is not None


def get_locale_for_jurisdiction(
    jurisdiction: str,
    *,
    language: str | None = None,
) -> str | None:
    """
    Return a likely Babel locale identifier for *jurisdiction*.

    The locale is composed from GeoCanon's default language mapping and
    ISO-3166 alpha-2 country code, for example ``"ro_RO"`` for Romania.
    """
    language_code = language or get_language_for_jurisdiction(jurisdiction)
    region_code = get_alpha2(jurisdiction)

    if language_code and region_code:
        return f"{language_code}_{region_code}"
    if language_code:
        return language_code
    return None


def _resolve_locale(jurisdiction: str, locale: str | None, language: str | None = None) -> str | None:
    return locale or get_locale_for_jurisdiction(jurisdiction, language=language)


def format_decimal_locale(
    value: int | float | Decimal,
    jurisdiction: str,
    *,
    locale: str | None = None,
    language: str | None = None,
) -> str:
    """Format a decimal number for *jurisdiction* using Babel when available."""
    resolved_locale = _resolve_locale(jurisdiction, locale, language)
    if _babel_numbers is not None and resolved_locale is not None:
        try:
            return _babel_numbers.format_decimal(value, locale=resolved_locale)
        except (UnknownLocaleError, ValueError):
            pass

    return f"{Decimal(str(value)):,}"


def format_percent_locale(
    value: int | float | Decimal,
    jurisdiction: str,
    *,
    locale: str | None = None,
    language: str | None = None,
) -> str:
    """Format a percentage for *jurisdiction* using Babel when available."""
    resolved_locale = _resolve_locale(jurisdiction, locale, language)
    if _babel_numbers is not None and resolved_locale is not None:
        try:
            return _babel_numbers.format_percent(value, locale=resolved_locale)
        except (UnknownLocaleError, ValueError):
            pass

    return f"{Decimal(str(value)) * Decimal('100'):,.0f}%"


def format_currency_locale(
    amount: int | float | Decimal,
    jurisdiction: str,
    *,
    currency_code: str | None = None,
    locale: str | None = None,
    language: str | None = None,
) -> str:
    """Format currency for *jurisdiction* using Babel when available."""
    code = currency_code or get_currency_code(jurisdiction)
    resolved_locale = _resolve_locale(jurisdiction, locale, language)

    if _babel_numbers is not None and code is not None and resolved_locale is not None:
        try:
            return _babel_numbers.format_currency(amount, code, locale=resolved_locale)
        except (UnknownLocaleError, ValueError):
            pass

    return format_currency(amount, jurisdiction, include_code=currency_code is not None)


def format_date_locale(
    value: _datetime.date,
    jurisdiction: str,
    *,
    date_format: str = "medium",
    locale: str | None = None,
    language: str | None = None,
) -> str:
    """Format a date for *jurisdiction* using Babel when available."""
    resolved_locale = _resolve_locale(jurisdiction, locale, language)
    if _babel_dates is not None and resolved_locale is not None:
        try:
            return _babel_dates.format_date(value, format=date_format, locale=resolved_locale)
        except (UnknownLocaleError, ValueError):
            pass

    return value.isoformat()


def format_time_locale(
    value: _datetime.time,
    jurisdiction: str,
    *,
    time_format: str = "medium",
    locale: str | None = None,
    language: str | None = None,
) -> str:
    """Format a time for *jurisdiction* using Babel when available."""
    resolved_locale = _resolve_locale(jurisdiction, locale, language)
    if _babel_dates is not None and resolved_locale is not None:
        try:
            return _babel_dates.format_time(value, format=time_format, locale=resolved_locale)
        except (UnknownLocaleError, ValueError):
            pass

    return value.isoformat()


def format_datetime_locale(
    value: _datetime.datetime,
    jurisdiction: str,
    *,
    datetime_format: str = "medium",
    locale: str | None = None,
    language: str | None = None,
) -> str:
    """Format a datetime for *jurisdiction* using Babel when available."""
    resolved_locale = _resolve_locale(jurisdiction, locale, language)
    if _babel_dates is not None and resolved_locale is not None:
        try:
            return _babel_dates.format_datetime(value, format=datetime_format, locale=resolved_locale)
        except (UnknownLocaleError, ValueError):
            pass

    return value.isoformat()


def format_list_locale(
    values: Iterable[str],
    jurisdiction: str,
    *,
    locale: str | None = None,
    language: str | None = None,
) -> str:
    """Format a list of strings for *jurisdiction* using Babel when available."""
    items = list(values)
    resolved_locale = _resolve_locale(jurisdiction, locale, language)
    if _babel_lists is not None and resolved_locale is not None:
        try:
            return _babel_lists.format_list(items, locale=resolved_locale)
        except (UnknownLocaleError, ValueError):
            pass

    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + f" and {items[-1]}"
