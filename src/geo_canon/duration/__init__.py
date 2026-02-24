"""
GeoCanon — Duration Formatting

Translatable, human-readable duration formatting using Django's ``ngettext``.
"""

from __future__ import annotations

from django.utils.translation import ngettext


def format_duration(total_seconds: int) -> str:
    """
    Format *total_seconds* into a human-readable, translatable string.

    The output respects the active Django translation.

    >>> format_duration(3661)
    '1 hour, 1 minute, 1 second'

    >>> format_duration(0)
    '0 seconds'
    """
    if total_seconds < 0:
        raise ValueError("total_seconds must be non-negative")

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    parts: list[str] = []

    if hours:
        parts.append(ngettext("%d hour", "%d hours", hours) % hours)

    if minutes:
        parts.append(ngettext("%d minute", "%d minutes", minutes) % minutes)

    if seconds or not parts:
        parts.append(ngettext("%d second", "%d seconds", seconds) % seconds)

    return ", ".join(parts)
