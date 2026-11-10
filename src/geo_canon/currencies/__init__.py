"""
GeoCanon — Currencies

Jurisdiction → ISO 4217 currency mapping, symbols, formatting helpers,
and Django form choices for currency selection.
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Any, NamedTuple

from django.utils.functional import Promise
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

# ---------------------------------------------------------------------------
# Currency data structure
# ---------------------------------------------------------------------------


class CurrencyInfo(NamedTuple):
    """Immutable container for a single currency."""

    code: str  # ISO 4217 alpha-3
    name: str | Promise  # English name (translatable)
    symbol: str  # Conventional symbol (e.g. "$", "€", "£")
    decimal_places: int  # Standard minor units (0 for JPY, 2 for most)


# ---------------------------------------------------------------------------
# Master registry — jurisdiction name → CurrencyInfo
# ---------------------------------------------------------------------------

JURISDICTION_CURRENCY: dict[str, CurrencyInfo] = {
    "Afghanistan": CurrencyInfo("AFN", _("Afghan Afghani"), "؋", 2),
    "Albania": CurrencyInfo("ALL", _("Albanian Lek"), "L", 2),
    "Algeria": CurrencyInfo("DZD", _("Algerian Dinar"), "د.ج", 2),
    "Andorra": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Angola": CurrencyInfo("AOA", _("Angolan Kwanza"), "Kz", 2),
    "Antigua and Barbuda": CurrencyInfo("XCD", _("East Caribbean Dollar"), "EC$", 2),
    "Argentina": CurrencyInfo("ARS", _("Argentine Peso"), "$", 2),
    "Armenia": CurrencyInfo("AMD", _("Armenian Dram"), "֏", 2),
    "Aruba": CurrencyInfo("AWG", _("Aruban Florin"), "ƒ", 2),
    "Australia": CurrencyInfo("AUD", _("Australian Dollar"), "A$", 2),
    "Austria": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Azerbaijan": CurrencyInfo("AZN", _("Azerbaijani Manat"), "₼", 2),
    "Bahamas": CurrencyInfo("BSD", _("Bahamian Dollar"), "B$", 2),
    "Bahrain": CurrencyInfo("BHD", _("Bahraini Dinar"), ".د.ب", 3),
    "Bangladesh": CurrencyInfo("BDT", _("Bangladeshi Taka"), "৳", 2),
    "Barbados": CurrencyInfo("BBD", _("Barbadian Dollar"), "Bds$", 2),
    "Belarus": CurrencyInfo("BYN", _("Belarusian Ruble"), "Br", 2),
    "Belgium": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Belize": CurrencyInfo("BZD", _("Belize Dollar"), "BZ$", 2),
    "Benin": CurrencyInfo("XOF", _("West African CFA Franc"), "CFA", 0),
    "Bhutan": CurrencyInfo("BTN", _("Bhutanese Ngultrum"), "Nu.", 2),
    "Bolivia": CurrencyInfo("BOB", _("Bolivian Boliviano"), "Bs.", 2),
    "Bosnia and Herzegovina": CurrencyInfo(
        "BAM", _("Bosnia-Herzegovina Convertible Mark"), "KM", 2
    ),
    "Botswana": CurrencyInfo("BWP", _("Botswanan Pula"), "P", 2),
    "Brazil": CurrencyInfo("BRL", _("Brazilian Real"), "R$", 2),
    "Brunei": CurrencyInfo("BND", _("Brunei Dollar"), "B$", 2),
    "Bulgaria": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Burkina Faso": CurrencyInfo("XOF", _("West African CFA Franc"), "CFA", 0),
    "Burundi": CurrencyInfo("BIF", _("Burundian Franc"), "FBu", 0),
    "Cabo Verde": CurrencyInfo("CVE", _("Cape Verdean Escudo"), "$", 2),
    "Cambodia": CurrencyInfo("KHR", _("Cambodian Riel"), "៛", 2),
    "Cameroon": CurrencyInfo("XAF", _("Central African CFA Franc"), "FCFA", 0),
    "Canada": CurrencyInfo("CAD", _("Canadian Dollar"), "C$", 2),
    "Cape Verde": CurrencyInfo("CVE", _("Cape Verdean Escudo"), "$", 2),
    "Central African Republic": CurrencyInfo("XAF", _("Central African CFA Franc"), "FCFA", 0),
    "Chad": CurrencyInfo("XAF", _("Central African CFA Franc"), "FCFA", 0),
    "Chile": CurrencyInfo("CLP", _("Chilean Peso"), "$", 0),
    "China": CurrencyInfo("CNY", _("Chinese Yuan"), "¥", 2),
    "Colombia": CurrencyInfo("COP", _("Colombian Peso"), "$", 2),
    "Comoros": CurrencyInfo("KMF", _("Comorian Franc"), "CF", 0),
    "Congo": CurrencyInfo("XAF", _("Central African CFA Franc"), "FCFA", 0),
    "Congo (Congo-Brazzaville)": CurrencyInfo("XAF", _("Central African CFA Franc"), "FCFA", 0),
    "Congo (DRC)": CurrencyInfo("CDF", _("Congolese Franc"), "FC", 2),
    "Costa Rica": CurrencyInfo("CRC", _("Costa Rican Colón"), "₡", 2),
    "Cote d'Ivoire": CurrencyInfo("XOF", _("West African CFA Franc"), "CFA", 0),
    "Croatia": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Cuba": CurrencyInfo("CUP", _("Cuban Peso"), "$", 2),
    "Curacao": CurrencyInfo("XCG", _("Caribbean Guilder"), "Cg", 2),
    "Cyprus": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Czech Republic": CurrencyInfo("CZK", _("Czech Koruna"), "Kč", 2),
    "Democratic Republic of Congo": CurrencyInfo("CDF", _("Congolese Franc"), "FC", 2),
    "Denmark": CurrencyInfo("DKK", _("Danish Krone"), "kr", 2),
    "Djibouti": CurrencyInfo("DJF", _("Djiboutian Franc"), "Fdj", 0),
    "Dominica": CurrencyInfo("XCD", _("East Caribbean Dollar"), "EC$", 2),
    "Dominican Republic": CurrencyInfo("DOP", _("Dominican Peso"), "RD$", 2),
    "Ecuador": CurrencyInfo("USD", _("United States Dollar"), "$", 2),
    "Egypt": CurrencyInfo("EGP", _("Egyptian Pound"), "E£", 2),
    "El Salvador": CurrencyInfo("USD", _("United States Dollar"), "$", 2),
    "Equatorial Guinea": CurrencyInfo("XAF", _("Central African CFA Franc"), "FCFA", 0),
    "Eritrea": CurrencyInfo("ERN", _("Eritrean Nakfa"), "Nfk", 2),
    "Estonia": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Eswatini": CurrencyInfo("SZL", _("Swazi Lilangeni"), "E", 2),
    "Ethiopia": CurrencyInfo("ETB", _("Ethiopian Birr"), "Br", 2),
    "Fiji": CurrencyInfo("FJD", _("Fijian Dollar"), "FJ$", 2),
    "Finland": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "France": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Gabon": CurrencyInfo("XAF", _("Central African CFA Franc"), "FCFA", 0),
    "Gambia": CurrencyInfo("GMD", _("Gambian Dalasi"), "D", 2),
    "Georgia": CurrencyInfo("GEL", _("Georgian Lari"), "₾", 2),
    "Germany": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Ghana": CurrencyInfo("GHS", _("Ghanaian Cedi"), "GH₵", 2),
    "Greece": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Grenada": CurrencyInfo("XCD", _("East Caribbean Dollar"), "EC$", 2),
    "Guatemala": CurrencyInfo("GTQ", _("Guatemalan Quetzal"), "Q", 2),
    "Guinea": CurrencyInfo("GNF", _("Guinean Franc"), "FG", 0),
    "Guinea-Bissau": CurrencyInfo("XOF", _("West African CFA Franc"), "CFA", 0),
    "Guyana": CurrencyInfo("GYD", _("Guyanese Dollar"), "G$", 2),
    "Haiti": CurrencyInfo("HTG", _("Haitian Gourde"), "G", 2),
    "Honduras": CurrencyInfo("HNL", _("Honduran Lempira"), "L", 2),
    "Hong Kong": CurrencyInfo("HKD", _("Hong Kong Dollar"), "HK$", 2),
    "Hungary": CurrencyInfo("HUF", _("Hungarian Forint"), "Ft", 2),
    "Iceland": CurrencyInfo("ISK", _("Icelandic Króna"), "kr", 0),
    "India": CurrencyInfo("INR", _("Indian Rupee"), "₹", 2),
    "Indonesia": CurrencyInfo("IDR", _("Indonesian Rupiah"), "Rp", 2),
    "Iran": CurrencyInfo("IRR", _("Iranian Rial"), "﷼", 2),
    "Iraq": CurrencyInfo("IQD", _("Iraqi Dinar"), "ع.د", 3),
    "Ireland": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Israel": CurrencyInfo("ILS", _("Israeli New Shekel"), "₪", 2),
    "Italy": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Ivory Coast": CurrencyInfo("XOF", _("West African CFA Franc"), "CFA", 0),
    "Jamaica": CurrencyInfo("JMD", _("Jamaican Dollar"), "J$", 2),
    "Japan": CurrencyInfo("JPY", _("Japanese Yen"), "¥", 0),
    "Jordan": CurrencyInfo("JOD", _("Jordanian Dinar"), "JD", 3),
    "Kazakhstan": CurrencyInfo("KZT", _("Kazakhstani Tenge"), "₸", 2),
    "Kenya": CurrencyInfo("KES", _("Kenyan Shilling"), "KSh", 2),
    "Kiribati": CurrencyInfo("AUD", _("Australian Dollar"), "A$", 2),
    "Korea (North)": CurrencyInfo("KPW", _("North Korean Won"), "₩", 2),
    "Korea (South)": CurrencyInfo("KRW", _("South Korean Won"), "₩", 0),
    "Kosovo": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Kuwait": CurrencyInfo("KWD", _("Kuwaiti Dinar"), "د.ك", 3),
    "Kyrgyzstan": CurrencyInfo("KGS", _("Kyrgyzstani Som"), "сом", 2),
    "Laos": CurrencyInfo("LAK", _("Lao Kip"), "₭", 2),
    "Latvia": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Lebanon": CurrencyInfo("LBP", _("Lebanese Pound"), "ل.ل", 2),
    "Lesotho": CurrencyInfo("LSL", _("Lesotho Loti"), "L", 2),
    "Liberia": CurrencyInfo("LRD", _("Liberian Dollar"), "L$", 2),
    "Libya": CurrencyInfo("LYD", _("Libyan Dinar"), "ل.د", 3),
    "Liechtenstein": CurrencyInfo("CHF", _("Swiss Franc"), "CHF", 2),
    "Lithuania": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Luxembourg": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Madagascar": CurrencyInfo("MGA", _("Malagasy Ariary"), "Ar", 2),
    "Malawi": CurrencyInfo("MWK", _("Malawian Kwacha"), "MK", 2),
    "Malaysia": CurrencyInfo("MYR", _("Malaysian Ringgit"), "RM", 2),
    "Maldives": CurrencyInfo("MVR", _("Maldivian Rufiyaa"), "Rf", 2),
    "Mali": CurrencyInfo("XOF", _("West African CFA Franc"), "CFA", 0),
    "Malta": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Marshall Islands": CurrencyInfo("USD", _("United States Dollar"), "$", 2),
    "Mauritania": CurrencyInfo("MRU", _("Mauritanian Ouguiya"), "UM", 2),
    "Mauritius": CurrencyInfo("MUR", _("Mauritian Rupee"), "₨", 2),
    "Mexico": CurrencyInfo("MXN", _("Mexican Peso"), "Mex$", 2),
    "Micronesia": CurrencyInfo("USD", _("United States Dollar"), "$", 2),
    "Moldova": CurrencyInfo("MDL", _("Moldovan Leu"), "L", 2),
    "Monaco": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Mongolia": CurrencyInfo("MNT", _("Mongolian Tögrög"), "₮", 2),
    "Montenegro": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Morocco": CurrencyInfo("MAD", _("Moroccan Dirham"), "د.م.", 2),
    "Mozambique": CurrencyInfo("MZN", _("Mozambican Metical"), "MT", 2),
    "Myanmar": CurrencyInfo("MMK", _("Myanmar Kyat"), "K", 2),
    "Namibia": CurrencyInfo("NAD", _("Namibian Dollar"), "N$", 2),
    "Nauru": CurrencyInfo("AUD", _("Australian Dollar"), "A$", 2),
    "Nepal": CurrencyInfo("NPR", _("Nepalese Rupee"), "Rs", 2),
    "Netherlands": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "New Zealand": CurrencyInfo("NZD", _("New Zealand Dollar"), "NZ$", 2),
    "Nicaragua": CurrencyInfo("NIO", _("Nicaraguan Córdoba"), "C$", 2),
    "Niger": CurrencyInfo("XOF", _("West African CFA Franc"), "CFA", 0),
    "Nigeria": CurrencyInfo("NGN", _("Nigerian Naira"), "₦", 2),
    "North Korea": CurrencyInfo("KPW", _("North Korean Won"), "₩", 2),
    "North Macedonia": CurrencyInfo("MKD", _("Macedonian Denar"), "ден", 2),
    "Norway": CurrencyInfo("NOK", _("Norwegian Krone"), "kr", 2),
    "Oman": CurrencyInfo("OMR", _("Omani Rial"), "ر.ع.", 3),
    "Pakistan": CurrencyInfo("PKR", _("Pakistani Rupee"), "₨", 2),
    "Palau": CurrencyInfo("USD", _("United States Dollar"), "$", 2),
    "Palestine": CurrencyInfo("ILS", _("Israeli New Shekel"), "₪", 2),
    "Panama": CurrencyInfo("PAB", _("Panamanian Balboa"), "B/.", 2),
    "Papua New Guinea": CurrencyInfo("PGK", _("Papua New Guinean Kina"), "K", 2),
    "Paraguay": CurrencyInfo("PYG", _("Paraguayan Guaraní"), "₲", 0),
    "Peru": CurrencyInfo("PEN", _("Peruvian Sol"), "S/.", 2),
    "Philippines": CurrencyInfo("PHP", _("Philippine Peso"), "₱", 2),
    "Poland": CurrencyInfo("PLN", _("Polish Złoty"), "zł", 2),
    "Portugal": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Qatar": CurrencyInfo("QAR", _("Qatari Riyal"), "ر.ق", 2),
    "Romania": CurrencyInfo("RON", _("Romanian Leu"), "lei", 2),
    "Russia": CurrencyInfo("RUB", _("Russian Ruble"), "₽", 2),
    "Rwanda": CurrencyInfo("RWF", _("Rwandan Franc"), "RF", 0),
    "Saint Kitts and Nevis": CurrencyInfo("XCD", _("East Caribbean Dollar"), "EC$", 2),
    "Saint Lucia": CurrencyInfo("XCD", _("East Caribbean Dollar"), "EC$", 2),
    "Saint Vincent and the Grenadines": CurrencyInfo("XCD", _("East Caribbean Dollar"), "EC$", 2),
    "Samoa": CurrencyInfo("WST", _("Samoan Tālā"), "WS$", 2),
    "San Marino": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Sao Tome and Principe": CurrencyInfo("STN", _("São Tomé and Príncipe Dobra"), "Db", 2),
    "Saudi Arabia": CurrencyInfo("SAR", _("Saudi Riyal"), "ر.س", 2),
    "Senegal": CurrencyInfo("XOF", _("West African CFA Franc"), "CFA", 0),
    "Serbia": CurrencyInfo("RSD", _("Serbian Dinar"), "din.", 2),
    "Seychelles": CurrencyInfo("SCR", _("Seychellois Rupee"), "SRe", 2),
    "Sierra Leone": CurrencyInfo("SLE", _("Sierra Leonean Leone"), "Le", 2),
    "Singapore": CurrencyInfo("SGD", _("Singapore Dollar"), "S$", 2),
    "Slovakia": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Slovenia": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Solomon Islands": CurrencyInfo("SBD", _("Solomon Islands Dollar"), "SI$", 2),
    "Somalia": CurrencyInfo("SOS", _("Somali Shilling"), "Sh", 2),
    "South Africa": CurrencyInfo("ZAR", _("South African Rand"), "R", 2),
    "South Korea": CurrencyInfo("KRW", _("South Korean Won"), "₩", 0),
    "South Sudan": CurrencyInfo("SSP", _("South Sudanese Pound"), "£", 2),
    "Spain": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Sri Lanka": CurrencyInfo("LKR", _("Sri Lankan Rupee"), "Rs", 2),
    "Sudan": CurrencyInfo("SDG", _("Sudanese Pound"), "ج.س.", 2),
    "Suriname": CurrencyInfo("SRD", _("Surinamese Dollar"), "SRD", 2),
    "Sweden": CurrencyInfo("SEK", _("Swedish Krona"), "kr", 2),
    "Switzerland": CurrencyInfo("CHF", _("Swiss Franc"), "CHF", 2),
    "Syria": CurrencyInfo("SYP", _("Syrian Pound"), "£S", 2),
    "Taiwan": CurrencyInfo("TWD", _("New Taiwan Dollar"), "NT$", 2),
    "Tajikistan": CurrencyInfo("TJS", _("Tajikistani Somoni"), "SM", 2),
    "Tanzania": CurrencyInfo("TZS", _("Tanzanian Shilling"), "TSh", 2),
    "Thailand": CurrencyInfo("THB", _("Thai Baht"), "฿", 2),
    "Timor-Leste": CurrencyInfo("USD", _("United States Dollar"), "$", 2),
    "Togo": CurrencyInfo("XOF", _("West African CFA Franc"), "CFA", 0),
    "Tonga": CurrencyInfo("TOP", _("Tongan Paʻanga"), "T$", 2),
    "Trinidad and Tobago": CurrencyInfo("TTD", _("Trinidad & Tobago Dollar"), "TT$", 2),
    "Tunisia": CurrencyInfo("TND", _("Tunisian Dinar"), "د.ت", 3),
    "Turkey": CurrencyInfo("TRY", _("Turkish Lira"), "₺", 2),
    "Turkmenistan": CurrencyInfo("TMT", _("Turkmenistani Manat"), "T", 2),
    "Tuvalu": CurrencyInfo("AUD", _("Australian Dollar"), "A$", 2),
    "Uganda": CurrencyInfo("UGX", _("Ugandan Shilling"), "USh", 0),
    "Ukraine": CurrencyInfo("UAH", _("Ukrainian Hryvnia"), "₴", 2),
    "United Arab Emirates": CurrencyInfo("AED", _("United Arab Emirates Dirham"), "د.إ", 2),
    "United Kingdom": CurrencyInfo("GBP", _("British Pound Sterling"), "£", 2),
    "United States": CurrencyInfo("USD", _("United States Dollar"), "$", 2),
    "Uruguay": CurrencyInfo("UYU", _("Uruguayan Peso"), "$U", 2),
    "Uzbekistan": CurrencyInfo("UZS", _("Uzbekistani Som"), "сўм", 2),
    "Vanuatu": CurrencyInfo("VUV", _("Vanuatu Vatu"), "VT", 0),
    "Vatican City": CurrencyInfo("EUR", _("Euro"), "€", 2),
    "Venezuela": CurrencyInfo("VES", _("Venezuelan Bolívar Soberano"), "Bs.S", 2),
    "Vietnam": CurrencyInfo("VND", _("Vietnamese Đồng"), "₫", 0),
    "Yemen": CurrencyInfo("YER", _("Yemeni Rial"), "﷼", 2),
    "Zambia": CurrencyInfo("ZMW", _("Zambian Kwacha"), "ZK", 2),
    "Zimbabwe": CurrencyInfo("ZWG", _("Zimbabwe Gold"), "ZiG", 2),
}


# ---------------------------------------------------------------------------
# Withdrawn currencies: no jurisdiction uses them any more, but stored amounts
# may still name them, so get_currency_by_code() keeps resolving them.
# CURRENCY_CHOICES leaves them out.
# ---------------------------------------------------------------------------

_WITHDRAWN_CURRENCIES: dict[str, CurrencyInfo] = {
    "ANG": CurrencyInfo("ANG", _("Netherlands Antillean Guilder"), "ƒ", 2),  # XCG from 2025-03-31
    "BGN": CurrencyInfo("BGN", _("Bulgarian Lev"), "лв", 2),  # EUR from 2026-01-01
    "ZWL": CurrencyInfo("ZWL", _("Zimbabwean Dollar"), "Z$", 2),  # ZWG from April 2024
}


# ---------------------------------------------------------------------------
# ISO 4217 code → CurrencyInfo (deduplicated — many jurisdictions share EUR):
# the currencies in use, then the withdrawn ones
# ---------------------------------------------------------------------------

_CURRENT_BY_CODE: dict[str, CurrencyInfo] = {}
for _info in JURISDICTION_CURRENCY.values():
    _CURRENT_BY_CODE.setdefault(_info.code, _info)

CURRENCY_BY_CODE: dict[str, CurrencyInfo] = {**_CURRENT_BY_CODE, **_WITHDRAWN_CURRENCIES}


# ---------------------------------------------------------------------------
# Django form choices for the currencies in use, sorted by currency name. Keep
# labels lazy so importing geo_canon does not require Django settings.
# ---------------------------------------------------------------------------


def _lazy_source_text(value: Any) -> str:
    return value._args[0] if hasattr(value, "_args") and value._args else str(value)


CURRENCY_CHOICES: list[tuple[str, str | Promise]] = [
    (info.code, format_lazy("{} ({})", info.name, info.code))
    for info in sorted(_CURRENT_BY_CODE.values(), key=lambda item: _lazy_source_text(item.name))
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_currency_for_jurisdiction(jurisdiction: str) -> CurrencyInfo | None:
    """
    Return the :class:`CurrencyInfo` for *jurisdiction*, or ``None``.

    >>> from geo_canon.currencies import get_currency_for_jurisdiction
    >>> get_currency_for_jurisdiction("Romania")
    CurrencyInfo(code='RON', name='Romanian Leu', symbol='lei', decimal_places=2)
    """
    return JURISDICTION_CURRENCY.get(jurisdiction)


def get_currency_code(jurisdiction: str) -> str | None:
    """
    Shortcut: return just the ISO 4217 code for *jurisdiction*.

    >>> from geo_canon.currencies import get_currency_code
    >>> get_currency_code("Japan")
    'JPY'
    """
    info = JURISDICTION_CURRENCY.get(jurisdiction)
    return info.code if info else None


def get_currency_symbol(jurisdiction: str) -> str | None:
    """
    Return the conventional symbol for *jurisdiction*'s currency.

    >>> from geo_canon.currencies import get_currency_symbol
    >>> get_currency_symbol("United Kingdom")
    '£'
    """
    info = JURISDICTION_CURRENCY.get(jurisdiction)
    return info.symbol if info else None


def get_currency_choices() -> list[tuple[str, str | Promise]]:
    """
    Return a list of ``(code, label)`` tuples suitable for a Django
    ``ChoiceField``.  Deduplicated and sorted alphabetically by label.
    Only currencies a jurisdiction uses today are offered; withdrawn ones
    such as ``BGN`` are left out.
    """
    return list(CURRENCY_CHOICES)


def get_currency_by_code(code: str) -> CurrencyInfo | None:
    """
    Look up a currency by its ISO 4217 code.

    Withdrawn codes such as ``BGN`` still resolve, so stored amounts can be
    shown in the currency they were recorded in.

    >>> from geo_canon.currencies import get_currency_by_code
    >>> get_currency_by_code("EUR").symbol
    '€'
    """
    return CURRENCY_BY_CODE.get(code.upper())


def format_currency(
    amount: int | float | Decimal,
    jurisdiction: str,
    *,
    use_symbol: bool = True,
    include_code: bool = False,
) -> str:
    """
    Format *amount* with the currency symbol/code for *jurisdiction*.

    Uses the correct number of decimal places for the currency.

    >>> from geo_canon.currencies import format_currency
    >>> format_currency(1234.5, "Japan")
    '¥1,235'
    >>> format_currency(1234.5, "United Kingdom")
    '£1,234.50'
    >>> format_currency(49.99, "Romania", use_symbol=False, include_code=True)
    '49.99 RON'
    """
    info = JURISDICTION_CURRENCY.get(jurisdiction)
    if info is None:
        # Fallback: plain number with 2 decimal places
        return f"{amount:,.2f}"
    return _format_with_currency(amount, info, use_symbol=use_symbol, include_code=include_code)


def _format_with_currency(
    amount: int | float | Decimal,
    info: CurrencyInfo,
    *,
    use_symbol: bool,
    include_code: bool,
) -> str:
    """Format *amount* in the currency *info* describes (shared by the locale fallback)."""
    # Round to the currency's minor unit precision
    quantized = Decimal(str(amount)).quantize(
        Decimal(10) ** -info.decimal_places,
        rounding=ROUND_HALF_UP,
    )

    # Format with thousands separator
    if info.decimal_places == 0:
        formatted = f"{int(quantized):,}"
    else:
        formatted = f"{quantized:,.{info.decimal_places}f}"

    if use_symbol and not include_code:
        return f"{info.symbol}{formatted}"
    elif include_code and not use_symbol:
        return f"{formatted} {info.code}"
    elif use_symbol and include_code:
        return f"{info.symbol}{formatted} {info.code}"
    else:
        return formatted
