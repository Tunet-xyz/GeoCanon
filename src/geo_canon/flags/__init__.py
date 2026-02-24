"""
GeoCanon — Flags

Country-name → ISO-3166 flag CSS class mapping.

Uses the ``flag-icons`` CSS library convention (``fi-XX``).  See
https://flagicons.lipis.dev/ for the full icon set.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Country name → flag-icon CSS class  (fi-XX where XX = ISO-3166-1 alpha-2)
# ---------------------------------------------------------------------------

FLAG_CSS_CLASS: dict[str, str] = {
    "Afghanistan": "fi-af",
    "Albania": "fi-al",
    "Algeria": "fi-dz",
    "Andorra": "fi-ad",
    "Angola": "fi-ao",
    "Antigua and Barbuda": "fi-ag",
    "Argentina": "fi-ar",
    "Armenia": "fi-am",
    "Australia": "fi-au",
    "Austria": "fi-at",
    "Azerbaijan": "fi-az",
    "Bahamas": "fi-bs",
    "Bahrain": "fi-bh",
    "Bangladesh": "fi-bd",
    "Barbados": "fi-bb",
    "Belarus": "fi-by",
    "Belgium": "fi-be",
    "Belize": "fi-bz",
    "Benin": "fi-bj",
    "Bhutan": "fi-bt",
    "Bolivia": "fi-bo",
    "Bosnia and Herzegovina": "fi-ba",
    "Botswana": "fi-bw",
    "Brazil": "fi-br",
    "Brunei": "fi-bn",
    "Bulgaria": "fi-bg",
    "Burkina Faso": "fi-bf",
    "Burundi": "fi-bi",
    "Cabo Verde": "fi-cv",
    "Cambodia": "fi-kh",
    "Cameroon": "fi-cm",
    "Canada": "fi-ca",
    "Central African Republic": "fi-cf",
    "Chad": "fi-td",
    "Chile": "fi-cl",
    "China": "fi-cn",
    "Colombia": "fi-co",
    "Comoros": "fi-km",
    "Congo (Congo-Brazzaville)": "fi-cg",
    "Congo (DRC)": "fi-cd",
    "Costa Rica": "fi-cr",
    "Croatia": "fi-hr",
    "Cuba": "fi-cu",
    "Cyprus": "fi-cy",
    "Czech Republic": "fi-cz",
    "Denmark": "fi-dk",
    "Djibouti": "fi-dj",
    "Dominica": "fi-dm",
    "Dominican Republic": "fi-do",
    "Ecuador": "fi-ec",
    "Egypt": "fi-eg",
    "El Salvador": "fi-sv",
    "Equatorial Guinea": "fi-gq",
    "Eritrea": "fi-er",
    "Estonia": "fi-ee",
    "Eswatini": "fi-sz",
    "Ethiopia": "fi-et",
    "Fiji": "fi-fj",
    "Finland": "fi-fi",
    "France": "fi-fr",
    "Gabon": "fi-ga",
    "Gambia": "fi-gm",
    "Georgia": "fi-ge",
    "Germany": "fi-de",
    "Ghana": "fi-gh",
    "Greece": "fi-gr",
    "Grenada": "fi-gd",
    "Guatemala": "fi-gt",
    "Guinea": "fi-gn",
    "Guinea-Bissau": "fi-gw",
    "Guyana": "fi-gy",
    "Haiti": "fi-ht",
    "Honduras": "fi-hn",
    "Hong Kong": "fi-hk",
    "Hungary": "fi-hu",
    "Iceland": "fi-is",
    "India": "fi-in",
    "Indonesia": "fi-id",
    "Iran": "fi-ir",
    "Iraq": "fi-iq",
    "Ireland": "fi-ie",
    "Israel": "fi-il",
    "Italy": "fi-it",
    "Jamaica": "fi-jm",
    "Japan": "fi-jp",
    "Jordan": "fi-jo",
    "Kazakhstan": "fi-kz",
    "Kenya": "fi-ke",
    "Kiribati": "fi-ki",
    "Korea (North)": "fi-kp",
    "Korea (South)": "fi-kr",
    "Kosovo": "fi-xk",
    "Kuwait": "fi-kw",
    "Kyrgyzstan": "fi-kg",
    "Laos": "fi-la",
    "Latvia": "fi-lv",
    "Lebanon": "fi-lb",
    "Lesotho": "fi-ls",
    "Liberia": "fi-lr",
    "Libya": "fi-ly",
    "Liechtenstein": "fi-li",
    "Lithuania": "fi-lt",
    "Luxembourg": "fi-lu",
    "Madagascar": "fi-mg",
    "Malawi": "fi-mw",
    "Malaysia": "fi-my",
    "Maldives": "fi-mv",
    "Mali": "fi-ml",
    "Malta": "fi-mt",
    "Marshall Islands": "fi-mh",
    "Mauritania": "fi-mr",
    "Mauritius": "fi-mu",
    "Mexico": "fi-mx",
    "Micronesia": "fi-fm",
    "Moldova": "fi-md",
    "Monaco": "fi-mc",
    "Mongolia": "fi-mn",
    "Montenegro": "fi-me",
    "Morocco": "fi-ma",
    "Mozambique": "fi-mz",
    "Myanmar": "fi-mm",
    "Namibia": "fi-na",
    "Nauru": "fi-nr",
    "Nepal": "fi-np",
    "Netherlands": "fi-nl",
    "New Zealand": "fi-nz",
    "Nicaragua": "fi-ni",
    "Niger": "fi-ne",
    "Nigeria": "fi-ng",
    "North Macedonia": "fi-mk",
    "Norway": "fi-no",
    "Oman": "fi-om",
    "Pakistan": "fi-pk",
    "Palau": "fi-pw",
    "Panama": "fi-pa",
    "Papua New Guinea": "fi-pg",
    "Paraguay": "fi-py",
    "Peru": "fi-pe",
    "Philippines": "fi-ph",
    "Poland": "fi-pl",
    "Portugal": "fi-pt",
    "Qatar": "fi-qa",
    "Romania": "fi-ro",
    "Russia": "fi-ru",
    "Rwanda": "fi-rw",
    "Saint Kitts and Nevis": "fi-kn",
    "Saint Lucia": "fi-lc",
    "Saint Vincent and the Grenadines": "fi-vc",
    "Samoa": "fi-ws",
    "San Marino": "fi-sm",
    "Sao Tome and Principe": "fi-st",
    "Saudi Arabia": "fi-sa",
    "Senegal": "fi-sn",
    "Serbia": "fi-rs",
    "Seychelles": "fi-sc",
    "Sierra Leone": "fi-sl",
    "Singapore": "fi-sg",
    "Slovakia": "fi-sk",
    "Slovenia": "fi-si",
    "Solomon Islands": "fi-sb",
    "Somalia": "fi-so",
    "South Africa": "fi-za",
    "South Korea": "fi-kr",
    "South Sudan": "fi-ss",
    "Spain": "fi-es",
    "Sri Lanka": "fi-lk",
    "Sudan": "fi-sd",
    "Suriname": "fi-sr",
    "Sweden": "fi-se",
    "Switzerland": "fi-ch",
    "Syria": "fi-sy",
    "Taiwan": "fi-tw",
    "Tajikistan": "fi-tj",
    "Tanzania": "fi-tz",
    "Thailand": "fi-th",
    "Timor-Leste": "fi-tl",
    "Togo": "fi-tg",
    "Tonga": "fi-to",
    "Trinidad and Tobago": "fi-tt",
    "Tunisia": "fi-tn",
    "Turkey": "fi-tr",
    "Turkmenistan": "fi-tm",
    "Tuvalu": "fi-tv",
    "Uganda": "fi-ug",
    "Ukraine": "fi-ua",
    "United Arab Emirates": "fi-ae",
    "United Kingdom": "fi-gb",
    "United States": "fi-us",
    "Uruguay": "fi-uy",
    "Uzbekistan": "fi-uz",
    "Vanuatu": "fi-vu",
    "Vatican City": "fi-va",
    "Venezuela": "fi-ve",
    "Vietnam": "fi-vn",
    "Yemen": "fi-ye",
    "Zambia": "fi-zm",
    "Zimbabwe": "fi-zw",
}

# ---------------------------------------------------------------------------
# Reverse lookup: ISO-3166-1 alpha-2 → country name
# ---------------------------------------------------------------------------

_ISO_TO_COUNTRY: dict[str, str] = {v.removeprefix("fi-"): k for k, v in FLAG_CSS_CLASS.items()}


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
