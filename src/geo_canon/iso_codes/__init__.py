"""
GeoCanon — ISO Country Codes

Jurisdiction → ISO 3166-1 alpha-2, alpha-3, and numeric code mapping.

This module is the **single source of truth** for country-code data in
GeoCanon.  Other modules (e.g. ``flags``) derive their data from it.
"""

from __future__ import annotations

from typing import NamedTuple

from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _

# ---------------------------------------------------------------------------
# Data structure
# ---------------------------------------------------------------------------


class ISOCountryInfo(NamedTuple):
    """ISO 3166-1 codes for a single jurisdiction."""

    alpha_2: str  # Two-letter code  (e.g. "RO")
    alpha_3: str  # Three-letter code (e.g. "ROU")
    numeric: str  # Numeric code      (e.g. "642")
    name: str | Promise  # English short name (translatable)


# ---------------------------------------------------------------------------
# Master registry — jurisdiction name → ISOCountryInfo
# ---------------------------------------------------------------------------

JURISDICTION_ISO: dict[str, ISOCountryInfo] = {
    "Afghanistan": ISOCountryInfo("AF", "AFG", "004", _("Afghanistan")),
    "Albania": ISOCountryInfo("AL", "ALB", "008", _("Albania")),
    "Algeria": ISOCountryInfo("DZ", "DZA", "012", _("Algeria")),
    "Andorra": ISOCountryInfo("AD", "AND", "020", _("Andorra")),
    "Angola": ISOCountryInfo("AO", "AGO", "024", _("Angola")),
    "Antigua and Barbuda": ISOCountryInfo("AG", "ATG", "028", _("Antigua and Barbuda")),
    "Argentina": ISOCountryInfo("AR", "ARG", "032", _("Argentina")),
    "Armenia": ISOCountryInfo("AM", "ARM", "051", _("Armenia")),
    "Aruba": ISOCountryInfo("AW", "ABW", "533", _("Aruba")),
    "Australia": ISOCountryInfo("AU", "AUS", "036", _("Australia")),
    "Austria": ISOCountryInfo("AT", "AUT", "040", _("Austria")),
    "Azerbaijan": ISOCountryInfo("AZ", "AZE", "031", _("Azerbaijan")),
    "Bahamas": ISOCountryInfo("BS", "BHS", "044", _("Bahamas")),
    "Bahrain": ISOCountryInfo("BH", "BHR", "048", _("Bahrain")),
    "Bangladesh": ISOCountryInfo("BD", "BGD", "050", _("Bangladesh")),
    "Barbados": ISOCountryInfo("BB", "BRB", "052", _("Barbados")),
    "Belarus": ISOCountryInfo("BY", "BLR", "112", _("Belarus")),
    "Belgium": ISOCountryInfo("BE", "BEL", "056", _("Belgium")),
    "Belize": ISOCountryInfo("BZ", "BLZ", "084", _("Belize")),
    "Benin": ISOCountryInfo("BJ", "BEN", "204", _("Benin")),
    "Bhutan": ISOCountryInfo("BT", "BTN", "064", _("Bhutan")),
    "Bolivia": ISOCountryInfo("BO", "BOL", "068", _("Bolivia")),
    "Bosnia and Herzegovina": ISOCountryInfo("BA", "BIH", "070", _("Bosnia and Herzegovina")),
    "Botswana": ISOCountryInfo("BW", "BWA", "072", _("Botswana")),
    "Brazil": ISOCountryInfo("BR", "BRA", "076", _("Brazil")),
    "Brunei": ISOCountryInfo("BN", "BRN", "096", _("Brunei")),
    "Bulgaria": ISOCountryInfo("BG", "BGR", "100", _("Bulgaria")),
    "Burkina Faso": ISOCountryInfo("BF", "BFA", "854", _("Burkina Faso")),
    "Burundi": ISOCountryInfo("BI", "BDI", "108", _("Burundi")),
    "Cabo Verde": ISOCountryInfo("CV", "CPV", "132", _("Cabo Verde")),
    "Cambodia": ISOCountryInfo("KH", "KHM", "116", _("Cambodia")),
    "Cameroon": ISOCountryInfo("CM", "CMR", "120", _("Cameroon")),
    "Canada": ISOCountryInfo("CA", "CAN", "124", _("Canada")),
    "Cape Verde": ISOCountryInfo("CV", "CPV", "132", _("Cape Verde")),
    "Central African Republic": ISOCountryInfo("CF", "CAF", "140", _("Central African Republic")),
    "Chad": ISOCountryInfo("TD", "TCD", "148", _("Chad")),
    "Chile": ISOCountryInfo("CL", "CHL", "152", _("Chile")),
    "China": ISOCountryInfo("CN", "CHN", "156", _("China")),
    "Colombia": ISOCountryInfo("CO", "COL", "170", _("Colombia")),
    "Comoros": ISOCountryInfo("KM", "COM", "174", _("Comoros")),
    "Congo": ISOCountryInfo("CG", "COG", "178", _("Congo")),
    "Congo (Congo-Brazzaville)": ISOCountryInfo("CG", "COG", "178", _("Congo (Congo-Brazzaville)")),
    "Congo (DRC)": ISOCountryInfo("CD", "COD", "180", _("Congo (DRC)")),
    "Costa Rica": ISOCountryInfo("CR", "CRI", "188", _("Costa Rica")),
    "Croatia": ISOCountryInfo("HR", "HRV", "191", _("Croatia")),
    "Cuba": ISOCountryInfo("CU", "CUB", "192", _("Cuba")),
    "Curacao": ISOCountryInfo("CW", "CUW", "531", _("Curaçao")),
    "Cyprus": ISOCountryInfo("CY", "CYP", "196", _("Cyprus")),
    "Czech Republic": ISOCountryInfo("CZ", "CZE", "203", _("Czech Republic")),
    "Democratic Republic of Congo": ISOCountryInfo(
        "CD", "COD", "180", _("Democratic Republic of Congo")
    ),
    "Denmark": ISOCountryInfo("DK", "DNK", "208", _("Denmark")),
    "Djibouti": ISOCountryInfo("DJ", "DJI", "262", _("Djibouti")),
    "Dominica": ISOCountryInfo("DM", "DMA", "212", _("Dominica")),
    "Dominican Republic": ISOCountryInfo("DO", "DOM", "214", _("Dominican Republic")),
    "Ecuador": ISOCountryInfo("EC", "ECU", "218", _("Ecuador")),
    "Egypt": ISOCountryInfo("EG", "EGY", "818", _("Egypt")),
    "El Salvador": ISOCountryInfo("SV", "SLV", "222", _("El Salvador")),
    "Equatorial Guinea": ISOCountryInfo("GQ", "GNQ", "226", _("Equatorial Guinea")),
    "Eritrea": ISOCountryInfo("ER", "ERI", "232", _("Eritrea")),
    "Estonia": ISOCountryInfo("EE", "EST", "233", _("Estonia")),
    "Eswatini": ISOCountryInfo("SZ", "SWZ", "748", _("Eswatini")),
    "Ethiopia": ISOCountryInfo("ET", "ETH", "231", _("Ethiopia")),
    "Fiji": ISOCountryInfo("FJ", "FJI", "242", _("Fiji")),
    "Finland": ISOCountryInfo("FI", "FIN", "246", _("Finland")),
    "France": ISOCountryInfo("FR", "FRA", "250", _("France")),
    "Gabon": ISOCountryInfo("GA", "GAB", "266", _("Gabon")),
    "Gambia": ISOCountryInfo("GM", "GMB", "270", _("Gambia")),
    "Georgia": ISOCountryInfo("GE", "GEO", "268", _("Georgia")),
    "Germany": ISOCountryInfo("DE", "DEU", "276", _("Germany")),
    "Ghana": ISOCountryInfo("GH", "GHA", "288", _("Ghana")),
    "Greece": ISOCountryInfo("GR", "GRC", "300", _("Greece")),
    "Grenada": ISOCountryInfo("GD", "GRD", "308", _("Grenada")),
    "Guatemala": ISOCountryInfo("GT", "GTM", "320", _("Guatemala")),
    "Guinea": ISOCountryInfo("GN", "GIN", "324", _("Guinea")),
    "Guinea-Bissau": ISOCountryInfo("GW", "GNB", "624", _("Guinea-Bissau")),
    "Guyana": ISOCountryInfo("GY", "GUY", "328", _("Guyana")),
    "Haiti": ISOCountryInfo("HT", "HTI", "332", _("Haiti")),
    "Honduras": ISOCountryInfo("HN", "HND", "340", _("Honduras")),
    "Hong Kong": ISOCountryInfo("HK", "HKG", "344", _("Hong Kong")),
    "Hungary": ISOCountryInfo("HU", "HUN", "348", _("Hungary")),
    "Iceland": ISOCountryInfo("IS", "ISL", "352", _("Iceland")),
    "India": ISOCountryInfo("IN", "IND", "356", _("India")),
    "Indonesia": ISOCountryInfo("ID", "IDN", "360", _("Indonesia")),
    "Iran": ISOCountryInfo("IR", "IRN", "364", _("Iran")),
    "Iraq": ISOCountryInfo("IQ", "IRQ", "368", _("Iraq")),
    "Ireland": ISOCountryInfo("IE", "IRL", "372", _("Ireland")),
    "Israel": ISOCountryInfo("IL", "ISR", "376", _("Israel")),
    "Italy": ISOCountryInfo("IT", "ITA", "380", _("Italy")),
    "Ivory Coast": ISOCountryInfo("CI", "CIV", "384", _("Ivory Coast")),
    "Jamaica": ISOCountryInfo("JM", "JAM", "388", _("Jamaica")),
    "Japan": ISOCountryInfo("JP", "JPN", "392", _("Japan")),
    "Jordan": ISOCountryInfo("JO", "JOR", "400", _("Jordan")),
    "Kazakhstan": ISOCountryInfo("KZ", "KAZ", "398", _("Kazakhstan")),
    "Kenya": ISOCountryInfo("KE", "KEN", "404", _("Kenya")),
    "Kiribati": ISOCountryInfo("KI", "KIR", "296", _("Kiribati")),
    "Korea (North)": ISOCountryInfo("KP", "PRK", "408", _("Korea (North)")),
    "Korea (South)": ISOCountryInfo("KR", "KOR", "410", _("Korea (South)")),
    "Kosovo": ISOCountryInfo("XK", "XKX", "983", _("Kosovo")),
    "Kuwait": ISOCountryInfo("KW", "KWT", "414", _("Kuwait")),
    "Kyrgyzstan": ISOCountryInfo("KG", "KGZ", "417", _("Kyrgyzstan")),
    "Laos": ISOCountryInfo("LA", "LAO", "418", _("Laos")),
    "Latvia": ISOCountryInfo("LV", "LVA", "428", _("Latvia")),
    "Lebanon": ISOCountryInfo("LB", "LBN", "422", _("Lebanon")),
    "Lesotho": ISOCountryInfo("LS", "LSO", "426", _("Lesotho")),
    "Liberia": ISOCountryInfo("LR", "LBR", "430", _("Liberia")),
    "Libya": ISOCountryInfo("LY", "LBY", "434", _("Libya")),
    "Liechtenstein": ISOCountryInfo("LI", "LIE", "438", _("Liechtenstein")),
    "Lithuania": ISOCountryInfo("LT", "LTU", "440", _("Lithuania")),
    "Luxembourg": ISOCountryInfo("LU", "LUX", "442", _("Luxembourg")),
    "Madagascar": ISOCountryInfo("MG", "MDG", "450", _("Madagascar")),
    "Malawi": ISOCountryInfo("MW", "MWI", "454", _("Malawi")),
    "Malaysia": ISOCountryInfo("MY", "MYS", "458", _("Malaysia")),
    "Maldives": ISOCountryInfo("MV", "MDV", "462", _("Maldives")),
    "Mali": ISOCountryInfo("ML", "MLI", "466", _("Mali")),
    "Malta": ISOCountryInfo("MT", "MLT", "470", _("Malta")),
    "Marshall Islands": ISOCountryInfo("MH", "MHL", "584", _("Marshall Islands")),
    "Mauritania": ISOCountryInfo("MR", "MRT", "478", _("Mauritania")),
    "Mauritius": ISOCountryInfo("MU", "MUS", "480", _("Mauritius")),
    "Mexico": ISOCountryInfo("MX", "MEX", "484", _("Mexico")),
    "Micronesia": ISOCountryInfo("FM", "FSM", "583", _("Micronesia")),
    "Moldova": ISOCountryInfo("MD", "MDA", "498", _("Moldova")),
    "Monaco": ISOCountryInfo("MC", "MCO", "492", _("Monaco")),
    "Mongolia": ISOCountryInfo("MN", "MNG", "496", _("Mongolia")),
    "Montenegro": ISOCountryInfo("ME", "MNE", "499", _("Montenegro")),
    "Morocco": ISOCountryInfo("MA", "MAR", "504", _("Morocco")),
    "Mozambique": ISOCountryInfo("MZ", "MOZ", "508", _("Mozambique")),
    "Myanmar": ISOCountryInfo("MM", "MMR", "104", _("Myanmar")),
    "Namibia": ISOCountryInfo("NA", "NAM", "516", _("Namibia")),
    "Nauru": ISOCountryInfo("NR", "NRU", "520", _("Nauru")),
    "Nepal": ISOCountryInfo("NP", "NPL", "524", _("Nepal")),
    "Netherlands": ISOCountryInfo("NL", "NLD", "528", _("Netherlands")),
    "New Zealand": ISOCountryInfo("NZ", "NZL", "554", _("New Zealand")),
    "Nicaragua": ISOCountryInfo("NI", "NIC", "558", _("Nicaragua")),
    "Niger": ISOCountryInfo("NE", "NER", "562", _("Niger")),
    "Nigeria": ISOCountryInfo("NG", "NGA", "566", _("Nigeria")),
    "North Korea": ISOCountryInfo("KP", "PRK", "408", _("North Korea")),
    "North Macedonia": ISOCountryInfo("MK", "MKD", "807", _("North Macedonia")),
    "Norway": ISOCountryInfo("NO", "NOR", "578", _("Norway")),
    "Oman": ISOCountryInfo("OM", "OMN", "512", _("Oman")),
    "Pakistan": ISOCountryInfo("PK", "PAK", "586", _("Pakistan")),
    "Palau": ISOCountryInfo("PW", "PLW", "585", _("Palau")),
    "Palestine": ISOCountryInfo("PS", "PSE", "275", _("Palestine")),
    "Panama": ISOCountryInfo("PA", "PAN", "591", _("Panama")),
    "Papua New Guinea": ISOCountryInfo("PG", "PNG", "598", _("Papua New Guinea")),
    "Paraguay": ISOCountryInfo("PY", "PRY", "600", _("Paraguay")),
    "Peru": ISOCountryInfo("PE", "PER", "604", _("Peru")),
    "Philippines": ISOCountryInfo("PH", "PHL", "608", _("Philippines")),
    "Poland": ISOCountryInfo("PL", "POL", "616", _("Poland")),
    "Portugal": ISOCountryInfo("PT", "PRT", "620", _("Portugal")),
    "Qatar": ISOCountryInfo("QA", "QAT", "634", _("Qatar")),
    "Romania": ISOCountryInfo("RO", "ROU", "642", _("Romania")),
    "Russia": ISOCountryInfo("RU", "RUS", "643", _("Russia")),
    "Rwanda": ISOCountryInfo("RW", "RWA", "646", _("Rwanda")),
    "Saint Kitts and Nevis": ISOCountryInfo("KN", "KNA", "659", _("Saint Kitts and Nevis")),
    "Saint Lucia": ISOCountryInfo("LC", "LCA", "662", _("Saint Lucia")),
    "Saint Vincent and the Grenadines": ISOCountryInfo(
        "VC", "VCT", "670", _("Saint Vincent and the Grenadines")
    ),
    "Samoa": ISOCountryInfo("WS", "WSM", "882", _("Samoa")),
    "San Marino": ISOCountryInfo("SM", "SMR", "674", _("San Marino")),
    "Sao Tome and Principe": ISOCountryInfo("ST", "STP", "678", _("Sao Tome and Principe")),
    "Saudi Arabia": ISOCountryInfo("SA", "SAU", "682", _("Saudi Arabia")),
    "Senegal": ISOCountryInfo("SN", "SEN", "686", _("Senegal")),
    "Serbia": ISOCountryInfo("RS", "SRB", "688", _("Serbia")),
    "Seychelles": ISOCountryInfo("SC", "SYC", "690", _("Seychelles")),
    "Sierra Leone": ISOCountryInfo("SL", "SLE", "694", _("Sierra Leone")),
    "Singapore": ISOCountryInfo("SG", "SGP", "702", _("Singapore")),
    "Slovakia": ISOCountryInfo("SK", "SVK", "703", _("Slovakia")),
    "Slovenia": ISOCountryInfo("SI", "SVN", "705", _("Slovenia")),
    "Solomon Islands": ISOCountryInfo("SB", "SLB", "090", _("Solomon Islands")),
    "Somalia": ISOCountryInfo("SO", "SOM", "706", _("Somalia")),
    "South Africa": ISOCountryInfo("ZA", "ZAF", "710", _("South Africa")),
    "South Korea": ISOCountryInfo("KR", "KOR", "410", _("South Korea")),
    "South Sudan": ISOCountryInfo("SS", "SSD", "728", _("South Sudan")),
    "Spain": ISOCountryInfo("ES", "ESP", "724", _("Spain")),
    "Sri Lanka": ISOCountryInfo("LK", "LKA", "144", _("Sri Lanka")),
    "Sudan": ISOCountryInfo("SD", "SDN", "729", _("Sudan")),
    "Suriname": ISOCountryInfo("SR", "SUR", "740", _("Suriname")),
    "Sweden": ISOCountryInfo("SE", "SWE", "752", _("Sweden")),
    "Switzerland": ISOCountryInfo("CH", "CHE", "756", _("Switzerland")),
    "Syria": ISOCountryInfo("SY", "SYR", "760", _("Syria")),
    "Taiwan": ISOCountryInfo("TW", "TWN", "158", _("Taiwan")),
    "Tajikistan": ISOCountryInfo("TJ", "TJK", "762", _("Tajikistan")),
    "Tanzania": ISOCountryInfo("TZ", "TZA", "834", _("Tanzania")),
    "Thailand": ISOCountryInfo("TH", "THA", "764", _("Thailand")),
    "Timor-Leste": ISOCountryInfo("TL", "TLS", "626", _("Timor-Leste")),
    "Togo": ISOCountryInfo("TG", "TGO", "768", _("Togo")),
    "Tonga": ISOCountryInfo("TO", "TON", "776", _("Tonga")),
    "Trinidad and Tobago": ISOCountryInfo("TT", "TTO", "780", _("Trinidad and Tobago")),
    "Tunisia": ISOCountryInfo("TN", "TUN", "788", _("Tunisia")),
    "Turkey": ISOCountryInfo("TR", "TUR", "792", _("Turkey")),
    "Turkmenistan": ISOCountryInfo("TM", "TKM", "795", _("Turkmenistan")),
    "Tuvalu": ISOCountryInfo("TV", "TUV", "798", _("Tuvalu")),
    "Uganda": ISOCountryInfo("UG", "UGA", "800", _("Uganda")),
    "Ukraine": ISOCountryInfo("UA", "UKR", "804", _("Ukraine")),
    "United Arab Emirates": ISOCountryInfo("AE", "ARE", "784", _("United Arab Emirates")),
    "United Kingdom": ISOCountryInfo("GB", "GBR", "826", _("United Kingdom")),
    "United States": ISOCountryInfo("US", "USA", "840", _("United States")),
    "Uruguay": ISOCountryInfo("UY", "URY", "858", _("Uruguay")),
    "Uzbekistan": ISOCountryInfo("UZ", "UZB", "860", _("Uzbekistan")),
    "Vanuatu": ISOCountryInfo("VU", "VUT", "548", _("Vanuatu")),
    "Vatican City": ISOCountryInfo("VA", "VAT", "336", _("Vatican City")),
    "Venezuela": ISOCountryInfo("VE", "VEN", "862", _("Venezuela")),
    "Vietnam": ISOCountryInfo("VN", "VNM", "704", _("Vietnam")),
    "Yemen": ISOCountryInfo("YE", "YEM", "887", _("Yemen")),
    "Zambia": ISOCountryInfo("ZM", "ZMB", "894", _("Zambia")),
    "Zimbabwe": ISOCountryInfo("ZW", "ZWE", "716", _("Zimbabwe")),
}


# ---------------------------------------------------------------------------
# Reverse-lookup indices (built once at import time)
# ---------------------------------------------------------------------------

ISO_ALPHA2_TO_JURISDICTION: dict[str, str] = {}
ISO_ALPHA3_TO_JURISDICTION: dict[str, str] = {}

for _name, _info in JURISDICTION_ISO.items():
    # First writer wins — keeps canonical name for shared codes
    if _info.alpha_2 not in ISO_ALPHA2_TO_JURISDICTION:
        ISO_ALPHA2_TO_JURISDICTION[_info.alpha_2] = _name
    if _info.alpha_3 not in ISO_ALPHA3_TO_JURISDICTION:
        ISO_ALPHA3_TO_JURISDICTION[_info.alpha_3] = _name


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_iso_codes(jurisdiction: str) -> ISOCountryInfo | None:
    """
    Return the full :class:`ISOCountryInfo` for *jurisdiction*, or ``None``.

    >>> from geo_canon.iso_codes import get_iso_codes
    >>> info = get_iso_codes("Romania")
    >>> info.alpha_2, info.alpha_3, info.numeric
    ('RO', 'ROU', '642')
    """
    return JURISDICTION_ISO.get(jurisdiction)


def get_alpha2(jurisdiction: str) -> str | None:
    """
    Return the ISO 3166-1 alpha-2 code for *jurisdiction*.

    >>> from geo_canon.iso_codes import get_alpha2
    >>> get_alpha2("Romania")
    'RO'
    """
    info = JURISDICTION_ISO.get(jurisdiction)
    return info.alpha_2 if info else None


def get_alpha3(jurisdiction: str) -> str | None:
    """
    Return the ISO 3166-1 alpha-3 code for *jurisdiction*.

    >>> from geo_canon.iso_codes import get_alpha3
    >>> get_alpha3("Romania")
    'ROU'
    """
    info = JURISDICTION_ISO.get(jurisdiction)
    return info.alpha_3 if info else None


def get_numeric_code(jurisdiction: str) -> str | None:
    """
    Return the ISO 3166-1 numeric code for *jurisdiction*.

    >>> from geo_canon.iso_codes import get_numeric_code
    >>> get_numeric_code("Romania")
    '642'
    """
    info = JURISDICTION_ISO.get(jurisdiction)
    return info.numeric if info else None


def get_jurisdiction_by_alpha2(code: str) -> str | None:
    """
    Reverse-lookup: return the jurisdiction name for an alpha-2 code.

    Case-insensitive.

    >>> from geo_canon.iso_codes import get_jurisdiction_by_alpha2
    >>> get_jurisdiction_by_alpha2("RO")
    'Romania'
    >>> get_jurisdiction_by_alpha2("ro")
    'Romania'
    """
    return ISO_ALPHA2_TO_JURISDICTION.get(code.upper())


def get_jurisdiction_by_alpha3(code: str) -> str | None:
    """
    Reverse-lookup: return the jurisdiction name for an alpha-3 code.

    Case-insensitive.

    >>> from geo_canon.iso_codes import get_jurisdiction_by_alpha3
    >>> get_jurisdiction_by_alpha3("ROU")
    'Romania'
    """
    return ISO_ALPHA3_TO_JURISDICTION.get(code.upper())
