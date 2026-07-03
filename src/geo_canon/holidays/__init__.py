"""
GeoCanon — Public Holidays

Jurisdiction-aware public holiday detection powered by the ``holidays``
library (optional dependency, install via ``pip install geocanon[holidays]``).
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
# Jurisdiction name → holidays country class / instance
# ---------------------------------------------------------------------------


def _build_registry() -> dict[str, Any]:
    """Build the mapping lazily so the library is only imported when needed."""
    if not _HAS_HOLIDAYS:
        return {}

    h = _holidays_lib
    return {
        "Afghanistan": h.AF,
        "Albania": h.AL,
        "Algeria": h.DZ,
        "Andorra": h.AD,
        "Angola": h.AO,
        "Argentina": h.AR,
        "Armenia": h.AM,
        "Aruba": h.AW,
        "Australia": h.AU,
        "Austria": h.AT,
        "Azerbaijan": h.AZ,
        "Bahamas": h.BS,
        "Bahrain": h.BH,
        "Bangladesh": h.BD,
        "Barbados": h.BB,
        "Belarus": h.BY,
        "Belgium": h.BE,
        "Belize": h.BZ,
        "Bolivia": h.BO,
        "Bosnia and Herzegovina": h.BA,
        "Botswana": h.BW,
        "Brazil": h.BR,
        "Brunei": h.BN,
        "Bulgaria": h.BG,
        "Burkina Faso": h.BF,
        "Burundi": h.BI,
        "Cambodia": h.KH,
        "Cameroon": h.CM,
        "Canada": h.CA,
        "Chad": h.TD,
        "Chile": h.CL,
        "China": h.CN,
        "Colombia": h.CO,
        "Congo": h.CG,
        "Costa Rica": h.CR,
        "Croatia": h.HR,
        "Cuba": h.CU,
        "Curacao": h.CW,
        "Cyprus": h.CY,
        "Czech Republic": h.CZ,
        "Denmark": h.DK,
        "Djibouti": h.DJ,
        "Dominica": h.DM,
        "Dominican Republic": h.DO,
        "Ecuador": h.EC,
        "Egypt": h.EG,
        "El Salvador": h.SV,
        "Estonia": h.EE,
        "Eswatini": h.SZ,
        "Ethiopia": h.ET,
        "Finland": h.FI,
        "France": h.FR,
        "Gabon": h.GA,
        "Georgia": h.GE,
        "Germany": h.DE,
        "Ghana": h.GH,
        "Greece": h.GR,
        "Guatemala": h.GT,
        "Haiti": h.HT,
        "Honduras": h.HN,
        "Hong Kong": h.HK,
        "Hungary": h.HU,
        "Iceland": h.IS,
        "India": h.IN,
        "Indonesia": h.ID,
        "Iran": h.IR,
        "Ireland": h.IE,
        "Israel": h.IL,
        "Italy": h.IT,
        "Jamaica": h.JM,
        "Japan": h.JP,
        "Jordan": h.JO,
        "Kazakhstan": h.KZ,
        "Kenya": h.KE,
        "Kuwait": h.KW,
        "Kyrgyzstan": h.KG,
        "Laos": h.LA,
        "Latvia": h.LV,
        "Lesotho": h.LS,
        "Liechtenstein": h.LI,
        "Lithuania": h.LT,
        "Luxembourg": h.LU,
        "Madagascar": h.MG,
        "Malawi": h.MW,
        "Malaysia": h.MY,
        "Maldives": h.MV,
        "Malta": h.MT,
        "Marshall Islands": h.MH,
        "Mauritania": h.MR,
        "Mexico": h.MX,
        "Moldova": h.MD,
        "Monaco": h.MC,
        "Montenegro": h.ME,
        "Morocco": h.MA,
        "Mozambique": h.MZ,
        "Namibia": h.NA,
        "Netherlands": h.NL,
        "New Zealand": h.NZ,
        "Nicaragua": h.NI,
        "Nigeria": h.NG,
        "North Macedonia": h.MK,
        "Norway": h.NO,
        "Pakistan": h.PK,
        "Palau": h.PW,
        "Panama": h.PA,
        "Papua New Guinea": h.PG,
        "Paraguay": h.PY,
        "Peru": h.PE,
        "Philippines": h.PH,
        "Poland": h.PL,
        "Portugal": h.PT,
        "Romania": h.RO,
        "Russia": h.RU,
        "Saint Kitts and Nevis": h.KN,
        "Samoa": h.WS,
        "San Marino": h.SM,
        "Saudi Arabia": h.SA,
        "Serbia": h.RS,
        "Seychelles": h.SC,
        "Singapore": h.SG,
        "Slovakia": h.SK,
        "Slovenia": h.SI,
        "South Africa": h.ZA,
        "South Korea": h.KR,
        "Spain": h.ES,
        "Sri Lanka": h.LK,
        "Sweden": h.SE,
        "Switzerland": h.CH,
        "Taiwan": h.TW,
        "Tanzania": h.TZ,
        "Thailand": h.TH,
        "Timor-Leste": h.TL,
        "Tonga": h.TO,
        "Tunisia": h.TN,
        "Turkey": h.TR,
        "Ukraine": h.UA,
        "United Arab Emirates": h.AE,
        "United Kingdom": h.UK,
        "United States": h.US,
        "Uruguay": h.UY,
        "Uzbekistan": h.UZ,
        "Vanuatu": h.VU,
        "Vatican City": h.VA,
        "Venezuela": h.VE,
        "Vietnam": h.VN,
        "Zambia": h.ZM,
        "Zimbabwe": h.ZW,
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
    """Return the list of jurisdictions that have holiday support."""
    _require_holidays()
    return sorted(_get_registry().keys())
