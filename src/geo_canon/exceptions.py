"""
GeoCanon Custom Exceptions

Provides rich, actionable error messages that guide developers to solutions.

Messages quote caller-supplied values escaped and shortened, and never repeat
a phone number. GeoCanon's own lookups return ``None`` or ``False`` instead of
raising :class:`JurisdictionNotFoundError`, :class:`DialCodeNotFoundError` or
:class:`PhoneValidationError`; applications can raise them for consistent
errors.
"""

from __future__ import annotations

_MAX_QUOTED_CHARS = 64


def _quoted(value: object) -> str:
    """Quote a caller's value for a message: escaped, and cut to a bounded length."""
    text = str(value)
    if len(text) > _MAX_QUOTED_CHARS:
        text = text[:_MAX_QUOTED_CHARS] + "..."
    return repr(text)


def _phone_reference(phone: object) -> str:
    """Refer to a phone number without repeating it: at most its last two digits."""
    digits = [char for char in str(phone) if char in "0123456789"]
    if len(digits) >= 6:
        return "Phone number ending in " + "".join(digits[-2:])
    return "Phone number"


class GeoCanonError(Exception):
    """Base exception for all GeoCanon errors."""

    def __init__(
        self,
        message: str,
        *,
        hint: str | None = None,
        docs_url: str | None = None,
        examples: list[str] | None = None,
    ):
        self.hint = hint
        self.docs_url = docs_url
        self.examples = examples or []

        parts = [message]
        if hint:
            parts.append(f"\n  Hint: {hint}")
        if docs_url:
            parts.append(f"\n  Docs: {docs_url}")
        if self.examples:
            parts.append("\n  Examples:")
            for ex in self.examples:
                parts.append(f"    - {ex}")

        super().__init__("\n".join(parts))


class ConfigurationError(GeoCanonError):
    """Raised when GeoCanon is misconfigured."""

    pass


class JurisdictionNotFoundError(GeoCanonError):
    """
    A jurisdiction is not recognised.

    GeoCanon's lookups return ``None`` instead; raise it from application code.
    """

    def __init__(self, jurisdiction: str, available: list[str] | None = None):
        hint_parts = [f"{_quoted(jurisdiction)} is not a registered jurisdiction."]
        if available:
            hint_parts.append(f"Available: {', '.join(available[:10])}...")
        super().__init__(
            f"Jurisdiction not found: {_quoted(jurisdiction)}",
            hint=" ".join(hint_parts),
            docs_url="https://github.com/Tunet-xyz/geo_canon/blob/main/docs/jurisdictions.md",
        )


class TimezoneNotFoundError(GeoCanonError):
    """Raised when a timezone mapping is missing for a jurisdiction."""

    def __init__(self, jurisdiction: str):
        super().__init__(
            f"No timezone configured for jurisdiction: {_quoted(jurisdiction)}",
            hint="Add a GEOCANON.timezone_overrides entry or submit a PR to add this mapping.",
            docs_url="https://github.com/Tunet-xyz/geo_canon/blob/main/docs/timezones.md",
        )


class HolidaysNotAvailableError(GeoCanonError):
    """Raised when the holidays extra is not installed."""

    def __init__(self):
        super().__init__(
            "The 'holidays' package is required for public holiday support.",
            hint='Install with: pip install "GeoCanon[holidays]"',
        )


class DialCodeNotFoundError(GeoCanonError):
    """
    A dial code is not recognised.

    GeoCanon's lookups return ``None`` or ``False`` instead; raise it from
    application code.
    """

    def __init__(self, dial_code: str):
        super().__init__(
            f"Dial code not found: {_quoted(dial_code)}",
            hint="Ensure the dial code starts with '+' and is a valid international prefix.",
        )


class PhoneValidationError(GeoCanonError):
    """
    A phone number fails validation for its dial code.

    GeoCanon's validators return ``False`` instead; raise it from application
    code. The message names at most the number's last two digits.
    """

    def __init__(self, phone: str, dial_code: str, expected_pattern: str):
        super().__init__(
            f"{_phone_reference(phone)} is invalid for dial code {_quoted(dial_code)}",
            hint=f"Expected pattern: {expected_pattern}",
        )
