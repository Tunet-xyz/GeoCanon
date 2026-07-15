"""
GeoCanon Custom Exceptions

Provides rich, actionable error messages that guide developers to solutions.
"""

from __future__ import annotations


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
    """Raised when a jurisdiction is not recognised."""

    def __init__(self, jurisdiction: str, available: list[str] | None = None):
        hint_parts = [f"'{jurisdiction}' is not a registered jurisdiction."]
        if available:
            hint_parts.append(f"Available: {', '.join(available[:10])}...")
        super().__init__(
            f"Jurisdiction not found: {jurisdiction}",
            hint=" ".join(hint_parts),
            docs_url="https://github.com/Tunet-xyz/GeoCanon/blob/main/docs/jurisdictions.md",
        )


class TimezoneNotFoundError(GeoCanonError):
    """Raised when a timezone mapping is missing for a jurisdiction."""

    def __init__(self, jurisdiction: str):
        super().__init__(
            f"No timezone configured for jurisdiction: {jurisdiction}",
            hint="Add a GEOCANON.timezone_overrides entry or submit a PR to add this mapping.",
            docs_url="https://github.com/Tunet-xyz/GeoCanon/blob/main/docs/timezones.md",
        )


class HolidaysNotAvailableError(GeoCanonError):
    """Raised when the holidays extra is not installed."""

    def __init__(self):
        super().__init__(
            "The 'holidays' package is required for public holiday support.",
            hint="Install with: pip install geocanon[holidays]",
        )


class DialCodeNotFoundError(GeoCanonError):
    """Raised when a dial code is not recognised."""

    def __init__(self, dial_code: str):
        super().__init__(
            f"Dial code not found: {dial_code}",
            hint="Ensure the dial code starts with '+' and is a valid international prefix.",
        )


class PhoneValidationError(GeoCanonError):
    """Raised when a phone number fails validation for its dial code."""

    def __init__(self, phone: str, dial_code: str, expected_pattern: str):
        super().__init__(
            f"Phone number '{phone}' is invalid for dial code {dial_code}",
            hint=f"Expected pattern: {expected_pattern}",
        )
