"""
GeoCanon — Flags

Country-name → ISO-3166 flag CSS class mapping.

Uses the ``flag-icons`` CSS library convention (``fi-XX``).  See
https://flagicons.lipis.dev/ for the full icon set.

The alpha-2 codes are sourced from :mod:`geo_canon.iso_codes` — this
module is a thin presentation layer on top of that registry.
"""

from __future__ import annotations

from geo_canon.iso_codes import ISO_ALPHA2_TO_JURISDICTION, JURISDICTION_ISO

# ---------------------------------------------------------------------------
# Country name → flag-icon CSS class  (fi-XX where XX = ISO-3166-1 alpha-2)
# Derived from the canonical iso_codes registry.
# ---------------------------------------------------------------------------

FLAG_CSS_CLASS: dict[str, str] = {
    name: f"fi-{info.alpha_2.lower()}" for name, info in JURISDICTION_ISO.items()
}

# ---------------------------------------------------------------------------
# Reverse lookup: ISO-3166-1 alpha-2 → country name
# Reuses the index already built by iso_codes.
# ---------------------------------------------------------------------------

_ISO_TO_COUNTRY: dict[str, str] = {
    code.lower(): name for code, name in ISO_ALPHA2_TO_JURISDICTION.items()
}


def get_flag_css_class(country: str, default: str = "fi-un") -> str:
    """
    Return the ``flag-icons`` CSS class for *country*.

    Falls back to *default* (UN flag) when the country is not found.

    >>> get_flag_css_class("Romania")
    'fi-ro'
    """
    return FLAG_CSS_CLASS.get(country, default)


def get_country_by_iso(iso_code: str) -> str | None:
    """
    Return the country name for a two-letter ISO-3166-1 alpha-2 code.

    >>> get_country_by_iso("ro")
    'Romania'
    """
    return _ISO_TO_COUNTRY.get(iso_code.lower())


def annotate_flag_class(
    records: list[dict],
    jurisdiction_key: str = "jurisdiction",
    flag_key: str = "flag_class",
    default: str = "fi-un",
) -> list[dict]:
    """
    Annotate each dict in *records* with a ``flag_class`` key.

    This is a convenience for list-views that need to render flag icons::

        records = annotate_flag_class(queryset.values())
    """
    for record in records:
        country = record.get(jurisdiction_key, "")
        record[flag_key] = FLAG_CSS_CLASS.get(country, default)
    return records
