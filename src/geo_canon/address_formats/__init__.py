"""
GeoCanon — Address Formats

Jurisdiction → postal address format mapping, postal-code validation,
field labels, and formatting helpers for building locale-aware address forms.
"""

from __future__ import annotations

import re
import string
from typing import NamedTuple

from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


class AddressFormat(NamedTuple):
    """Describes how postal addresses are structured in a jurisdiction."""

    # Field order template — placeholders: {name}, {company}, {address1},
    # {address2}, {city}, {state}, {postal_code}, {country}
    template: str

    # Label for the "state" field (varies by country)
    state_label: str | Promise

    # Label for the "postal code" field
    postal_code_label: str | Promise

    # Whether the state/province/region field is required
    state_required: bool

    # Regex pattern for postal/ZIP code validation (empty string = no code)
    postal_code_pattern: str

    # Example postal code for UI placeholders
    postal_code_example: str


# ---------------------------------------------------------------------------
# Default templates
# ---------------------------------------------------------------------------

# Recipient first in the small-to-large orders; last in the large-to-small
# orders (Japan, China, Russia, Taiwan), as domestic mail writes them.
_RECIPIENT = "{name}\n{company}\n"
_RECIPIENT_LAST = "\n{company}\n{name}"

# Most common worldwide: street → city → postal code → country
_TPL_DEFAULT = _RECIPIENT + "{address1}\n{address2}\n{city} {postal_code}\n{country}"

# The same, with the required region on its own line
_TPL_DEFAULT_STATE = (
    _RECIPIENT + "{address1}\n{address2}\n{city} {postal_code}\n{state}\n{country}"
)

# US/Philippines style: street → city, STATE ZIP
_TPL_US = _RECIPIENT + "{address1}\n{address2}\n{city}, {state} {postal_code}\n{country}"

# UK style: street → city → postal code (state rarely used)
_TPL_UK = _RECIPIENT + "{address1}\n{address2}\n{city}\n{postal_code}\n{country}"

# Japan style: postal code → prefecture → city → street (reversed)
_TPL_JP = "〒{postal_code}\n{state}{city}\n{address1}\n{address2}" + _RECIPIENT_LAST

# Brazil style: street → city – STATE → postal code → country
_TPL_BR = _RECIPIENT + "{address1}\n{address2}\n{city} - {state}\n{postal_code}\n{country}"

# Germany/Nordics: street → postal_code city → country
_TPL_DE = _RECIPIENT + "{address1}\n{address2}\n{postal_code} {city}\n{country}"

# France style: street → postal_code city → country
_TPL_FR = _RECIPIENT + "{address1}\n{address2}\n{postal_code} {city}\n{country}"

# Spain/Turkey/Iran: street → postal_code city province → country
_TPL_ES = _RECIPIENT + "{address1}\n{address2}\n{postal_code} {city} {state}\n{country}"

# Russia/CIS: country → postal_code → region → city → street (reversed)
_TPL_RU = "{country}\n{postal_code}\n{state}\n{city}\n{address1}\n{address2}" + _RECIPIENT_LAST

# China: country → postal_code → state → city → street (reversed)
_TPL_CN = "{country}\n{postal_code}\n{state}\n{city}\n{address1}\n{address2}" + _RECIPIENT_LAST

# South Korea: state → city → street → postal code
_TPL_KR = _RECIPIENT + "{state} {city}\n{address1}\n{address2}\n{postal_code}\n{country}"

# India: street → city → state → postal code
_TPL_IN = _RECIPIENT + "{address1}\n{address2}\n{city}\n{state} {postal_code}\n{country}"

# Canada/Australia: street → city STATE postal_code
_TPL_CA = _RECIPIENT + "{address1}\n{address2}\n{city} {state} {postal_code}\n{country}"


# ---------------------------------------------------------------------------
# Master registry — jurisdiction name → AddressFormat
# ---------------------------------------------------------------------------

JURISDICTION_ADDRESS_FORMAT: dict[str, AddressFormat] = {
    "Afghanistan": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, r"^\d{4}$", "1001"
    ),
    "Albania": AddressFormat(
        _TPL_DEFAULT, _("County"), _("Postal Code"), False, r"^\d{4}$", "1001"
    ),
    "Algeria": AddressFormat(_TPL_DE, _("Province"), _("Postal Code"), False, r"^\d{5}$", "16000"),
    "Andorra": AddressFormat(_TPL_DE, _("Parish"), _("Postal Code"), False, r"^AD\d{3}$", "AD500"),
    "Angola": AddressFormat(_TPL_DEFAULT, _("Province"), _("Postal Code"), False, "", ""),
    "Antigua and Barbuda": AddressFormat(
        _TPL_DEFAULT, _("Parish"), _("Postal Code"), False, "", ""
    ),
    "Argentina": AddressFormat(
        _TPL_US, _("Province"), _("Postal Code"), True, r"^[A-Z]\d{4}[A-Z]{3}$", "C1420ABC"
    ),
    "Armenia": AddressFormat(_TPL_DE, _("Province"), _("Postal Code"), False, r"^\d{4}$", "0001"),
    "Aruba": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Australia": AddressFormat(_TPL_CA, _("State"), _("Postcode"), True, r"^\d{4}$", "2000"),
    "Austria": AddressFormat(_TPL_DE, _("State"), _("PLZ"), False, r"^\d{4}$", "1010"),
    "Azerbaijan": AddressFormat(
        _TPL_DE, _("Region"), _("Postal Code"), False, r"^AZ\d{4}$", "AZ1000"
    ),
    "Bahamas": AddressFormat(_TPL_DEFAULT, _("Island"), _("Postal Code"), False, "", ""),
    "Bahrain": AddressFormat(
        _TPL_DEFAULT, _("Governorate"), _("Postal Code"), False, r"^\d{3,4}$", "317"
    ),
    "Bangladesh": AddressFormat(
        _TPL_DEFAULT, _("Division"), _("Postal Code"), False, r"^\d{4}$", "1205"
    ),
    "Barbados": AddressFormat(
        _TPL_DEFAULT, _("Parish"), _("Postal Code"), False, r"^BB\d{5}$", "BB15028"
    ),
    "Belarus": AddressFormat(_TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{6}$", "220000"),
    "Belgium": AddressFormat(_TPL_DE, _("Province"), _("Postal Code"), False, r"^\d{4}$", "1000"),
    "Belize": AddressFormat(_TPL_DEFAULT, _("District"), _("Postal Code"), False, "", ""),
    "Benin": AddressFormat(_TPL_DEFAULT, _("Department"), _("Postal Code"), False, "", ""),
    "Bhutan": AddressFormat(
        _TPL_DEFAULT, _("District"), _("Postal Code"), False, r"^\d{5}$", "11001"
    ),
    "Bolivia": AddressFormat(
        _TPL_DEFAULT, _("Department"), _("Postal Code"), False, r"^\d{4}$", "0101"
    ),
    "Bosnia and Herzegovina": AddressFormat(
        _TPL_DE, _("Entity"), _("Postal Code"), False, r"^\d{5}$", "71000"
    ),
    "Botswana": AddressFormat(_TPL_DEFAULT, _("District"), _("Postal Code"), False, "", ""),
    "Brazil": AddressFormat(_TPL_BR, _("State"), _("CEP"), True, r"^\d{5}-?\d{3}$", "01001-000"),
    "Brunei": AddressFormat(
        _TPL_DEFAULT, _("District"), _("Postal Code"), False, r"^[A-Z]{2}\d{4}$", "BS8811"
    ),
    "Bulgaria": AddressFormat(_TPL_DE, _("Province"), _("Postal Code"), False, r"^\d{4}$", "1000"),
    "Burkina Faso": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Burundi": AddressFormat(_TPL_DEFAULT, _("Province"), _("Postal Code"), False, "", ""),
    "Cabo Verde": AddressFormat(
        _TPL_DEFAULT, _("Island"), _("Postal Code"), False, r"^\d{4}$", "7600"
    ),
    "Cambodia": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, r"^\d{5,6}$", "12000"
    ),
    "Cameroon": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Canada": AddressFormat(
        _TPL_CA, _("Province"), _("Postal Code"), True, r"^[A-Z]\d[A-Z]\s?\d[A-Z]\d$", "K1A 0B1"
    ),
    "Cape Verde": AddressFormat(
        _TPL_DEFAULT, _("Island"), _("Postal Code"), False, r"^\d{4}$", "7600"
    ),
    "Central African Republic": AddressFormat(
        _TPL_DEFAULT, _("Prefecture"), _("Postal Code"), False, "", ""
    ),
    "Chad": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Chile": AddressFormat(
        _TPL_DEFAULT_STATE, _("Region"), _("Postal Code"), True, r"^\d{7}$", "8320000"
    ),
    "China": AddressFormat(_TPL_CN, _("Province"), _("Postal Code"), True, r"^\d{6}$", "100000"),
    "Colombia": AddressFormat(
        _TPL_DEFAULT_STATE, _("Department"), _("Postal Code"), True, r"^\d{6}$", "110111"
    ),
    "Comoros": AddressFormat(_TPL_DEFAULT, _("Island"), _("Postal Code"), False, "", ""),
    "Congo": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Congo (Congo-Brazzaville)": AddressFormat(
        _TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""
    ),
    "Congo (DRC)": AddressFormat(_TPL_DEFAULT, _("Province"), _("Postal Code"), False, "", ""),
    "Costa Rica": AddressFormat(
        _TPL_DEFAULT_STATE, _("Province"), _("Postal Code"), True, r"^\d{4,5}$", "10101"
    ),
    "Cote d'Ivoire": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Croatia": AddressFormat(_TPL_DE, _("County"), _("Postal Code"), False, r"^\d{5}$", "10000"),
    "Cuba": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, r"^\d{5}$", "10400"
    ),
    "Curacao": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Cyprus": AddressFormat(_TPL_DE, _("District"), _("Postal Code"), False, r"^\d{4}$", "1010"),
    "Czech Republic": AddressFormat(
        _TPL_DE, _("Region"), _("PSČ"), False, r"^\d{3}\s?\d{2}$", "110 00"
    ),
    "Democratic Republic of Congo": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, "", ""
    ),
    "Denmark": AddressFormat(_TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{4}$", "1050"),
    "Djibouti": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Dominica": AddressFormat(_TPL_DEFAULT, _("Parish"), _("Postal Code"), False, "", ""),
    "Dominican Republic": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, r"^\d{5}$", "10101"
    ),
    "Ecuador": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, r"^\d{6}$", "170150"
    ),
    "Egypt": AddressFormat(
        _TPL_DEFAULT_STATE, _("Governorate"), _("Postal Code"), True, r"^\d{5}$", "11511"
    ),
    "El Salvador": AddressFormat(
        _TPL_DEFAULT_STATE, _("Department"), _("Postal Code"), True, r"^\d{4}$", "1101"
    ),
    "Equatorial Guinea": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, "", ""
    ),
    "Eritrea": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Estonia": AddressFormat(_TPL_DE, _("County"), _("Postal Code"), False, r"^\d{5}$", "10111"),
    "Eswatini": AddressFormat(
        _TPL_DEFAULT, _("Region"), _("Postal Code"), False, r"^[A-Z]\d{3}$", "H100"
    ),
    "Ethiopia": AddressFormat(
        _TPL_DEFAULT, _("Region"), _("Postal Code"), False, r"^\d{4}$", "1000"
    ),
    "Fiji": AddressFormat(_TPL_DEFAULT, _("Division"), _("Postal Code"), False, "", ""),
    "Finland": AddressFormat(_TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{5}$", "00100"),
    "France": AddressFormat(_TPL_FR, _("Region"), _("Code Postal"), False, r"^\d{5}$", "75001"),
    "Gabon": AddressFormat(_TPL_DEFAULT, _("Province"), _("Postal Code"), False, "", ""),
    "Gambia": AddressFormat(_TPL_DEFAULT, _("Division"), _("Postal Code"), False, "", ""),
    "Georgia": AddressFormat(_TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{4}$", "0105"),
    "Germany": AddressFormat(_TPL_DE, _("State"), _("PLZ"), False, r"^\d{5}$", "10115"),
    "Ghana": AddressFormat(
        _TPL_DEFAULT,
        _("Region"),
        _("Postal Code"),
        False,
        r"^[A-Z]{2}-?\d{3,4}-?\d{4}$",
        "GA-184-6435",
    ),
    "Greece": AddressFormat(
        _TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{3}\s?\d{2}$", "105 57"
    ),
    "Grenada": AddressFormat(_TPL_DEFAULT, _("Parish"), _("Postal Code"), False, "", ""),
    "Guatemala": AddressFormat(
        _TPL_DEFAULT, _("Department"), _("Postal Code"), False, r"^\d{5}$", "01001"
    ),
    "Guinea": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, r"^\d{3}$", "001"),
    "Guinea-Bissau": AddressFormat(
        _TPL_DEFAULT, _("Region"), _("Postal Code"), False, r"^\d{4}$", "1000"
    ),
    "Guyana": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Haiti": AddressFormat(
        _TPL_DEFAULT, _("Department"), _("Postal Code"), False, r"^\d{4}$", "6110"
    ),
    "Honduras": AddressFormat(
        _TPL_DEFAULT, _("Department"), _("Postal Code"), False, r"^\d{5}$", "11101"
    ),
    "Hong Kong": AddressFormat(
        _RECIPIENT + "{address1}\n{address2}\n{city}\n{state}",
        _("District"),
        _("Postal Code"),
        False,
        "",
        "",
    ),
    "Hungary": AddressFormat(_TPL_DE, _("County"), _("Postal Code"), False, r"^\d{4}$", "1011"),
    "Iceland": AddressFormat(_TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{3}$", "101"),
    "India": AddressFormat(_TPL_IN, _("State"), _("PIN Code"), True, r"^\d{6}$", "110001"),
    "Indonesia": AddressFormat(
        _TPL_DEFAULT_STATE, _("Province"), _("Postal Code"), True, r"^\d{5}$", "10110"
    ),
    "Iran": AddressFormat(
        _TPL_ES, _("Province"), _("Postal Code"), True, r"^\d{5}-?\d{5}$", "11369-44318"
    ),
    "Iraq": AddressFormat(
        _TPL_DEFAULT, _("Governorate"), _("Postal Code"), False, r"^\d{5}$", "10001"
    ),
    "Ireland": AddressFormat(
        _RECIPIENT + "{address1}\n{address2}\n{city}\n{state}\n{postal_code}",
        _("County"),
        _("Eircode"),
        False,
        r"^[A-Z]\d{2}\s?[A-Z0-9]{4}$",
        "D02 AF30",
    ),
    "Israel": AddressFormat(_TPL_DE, _("District"), _("Postal Code"), False, r"^\d{7}$", "6100000"),
    "Italy": AddressFormat(
        _RECIPIENT + "{address1}\n{address2}\n{postal_code} {city} {state}",
        _("Province"),
        _("CAP"),
        True,
        r"^\d{5}$",
        "00100",
    ),
    "Ivory Coast": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Jamaica": AddressFormat(
        _TPL_DEFAULT, _("Parish"), _("Postal Code"), False, r"^JM[A-Z]{3}\d{2}$", "JMAAW01"
    ),
    "Japan": AddressFormat(
        _TPL_JP, _("Prefecture"), _("Postal Code"), True, r"^\d{3}-?\d{4}$", "100-0001"
    ),
    "Jordan": AddressFormat(
        _TPL_DE, _("Governorate"), _("Postal Code"), False, r"^\d{5}$", "11110"
    ),
    "Kazakhstan": AddressFormat(
        _TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{6}$", "010000"
    ),
    "Kenya": AddressFormat(_TPL_DEFAULT, _("County"), _("Postal Code"), False, r"^\d{5}$", "00100"),
    "Kiribati": AddressFormat(_TPL_DEFAULT, _("Island"), _("Postal Code"), False, "", ""),
    "Korea (North)": AddressFormat(_TPL_DEFAULT, _("Province"), _("Postal Code"), False, "", ""),
    "Korea (South)": AddressFormat(
        _TPL_KR, _("Province"), _("Postal Code"), True, r"^\d{5}$", "03051"
    ),
    "Kosovo": AddressFormat(_TPL_DE, _("District"), _("Postal Code"), False, r"^\d{5}$", "10000"),
    "Kuwait": AddressFormat(
        _TPL_DE, _("Governorate"), _("Postal Code"), False, r"^\d{5}$", "13001"
    ),
    "Kyrgyzstan": AddressFormat(
        _TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{6}$", "720001"
    ),
    "Laos": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, r"^\d{5}$", "01000"
    ),
    "Latvia": AddressFormat(
        _TPL_DE, _("Region"), _("Postal Code"), False, r"^LV-\d{4}$", "LV-1050"
    ),
    "Lebanon": AddressFormat(
        _TPL_DEFAULT, _("Governorate"), _("Postal Code"), False, r"^\d{4}\s?\d{4}$", "1100 2010"
    ),
    "Lesotho": AddressFormat(
        _TPL_DEFAULT, _("District"), _("Postal Code"), False, r"^\d{3}$", "100"
    ),
    "Liberia": AddressFormat(
        _TPL_DEFAULT, _("County"), _("Postal Code"), False, r"^\d{4}$", "1000"
    ),
    "Libya": AddressFormat(_TPL_DEFAULT, _("District"), _("Postal Code"), False, "", ""),
    "Liechtenstein": AddressFormat(_TPL_DE, _("Municipality"), _("PLZ"), False, r"^\d{4}$", "9490"),
    "Lithuania": AddressFormat(
        _TPL_DE, _("County"), _("Postal Code"), False, r"^LT-\d{5}$", "LT-01001"
    ),
    "Luxembourg": AddressFormat(_TPL_DE, _("Canton"), _("Postal Code"), False, r"^\d{4}$", "1009"),
    "Madagascar": AddressFormat(_TPL_DE, _("Province"), _("Postal Code"), False, r"^\d{3}$", "101"),
    "Malawi": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Malaysia": AddressFormat(
        _TPL_DEFAULT_STATE, _("State"), _("Postcode"), True, r"^\d{5}$", "50000"
    ),
    "Maldives": AddressFormat(
        _TPL_DEFAULT, _("Atoll"), _("Postal Code"), False, r"^\d{5}$", "20026"
    ),
    "Mali": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Malta": AddressFormat(
        _TPL_DEFAULT, _("Region"), _("Postal Code"), False, r"^[A-Z]{3}\s?\d{4}$", "VLT 1535"
    ),
    "Marshall Islands": AddressFormat(
        _TPL_US, _("State"), _("ZIP Code"), False, r"^\d{5}$", "96960"
    ),
    "Mauritania": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Mauritius": AddressFormat(
        _TPL_DEFAULT, _("District"), _("Postal Code"), False, r"^\d{5}$", "71602"
    ),
    "Mexico": AddressFormat(_TPL_US, _("State"), _("C.P."), True, r"^\d{5}$", "06600"),
    "Micronesia": AddressFormat(_TPL_US, _("State"), _("ZIP Code"), False, r"^\d{5}$", "96941"),
    "Moldova": AddressFormat(
        _TPL_DE, _("Region"), _("Postal Code"), False, r"^MD-?\d{4}$", "MD-2001"
    ),
    "Monaco": AddressFormat(_TPL_FR, _("Quarter"), _("Code Postal"), False, r"^980\d{2}$", "98000"),
    "Mongolia": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, r"^\d{5,6}$", "14200"
    ),
    "Montenegro": AddressFormat(
        _TPL_DE, _("Municipality"), _("Postal Code"), False, r"^\d{5}$", "81000"
    ),
    "Morocco": AddressFormat(_TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{5}$", "10000"),
    "Mozambique": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, r"^\d{4}$", "1100"
    ),
    "Myanmar": AddressFormat(
        _TPL_DEFAULT, _("State/Region"), _("Postal Code"), False, r"^\d{5}$", "11181"
    ),
    "Namibia": AddressFormat(
        _TPL_DEFAULT, _("Region"), _("Postal Code"), False, r"^\d{5}$", "10001"
    ),
    "Nauru": AddressFormat(_TPL_DEFAULT, _("District"), _("Postal Code"), False, "", ""),
    "Nepal": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, r"^\d{5}$", "44600"
    ),
    "Netherlands": AddressFormat(
        _TPL_DE, _("Province"), _("Postcode"), False, r"^\d{4}\s?[A-Z]{2}$", "1011 AB"
    ),
    "New Zealand": AddressFormat(_TPL_CA, _("Region"), _("Postcode"), False, r"^\d{4}$", "6011"),
    "Nicaragua": AddressFormat(
        _TPL_DEFAULT, _("Department"), _("Postal Code"), False, r"^\d{5}$", "11001"
    ),
    "Niger": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, r"^\d{4}$", "8000"),
    "Nigeria": AddressFormat(
        _TPL_DEFAULT_STATE, _("State"), _("Postal Code"), True, r"^\d{6}$", "100001"
    ),
    "North Korea": AddressFormat(_TPL_DEFAULT, _("Province"), _("Postal Code"), False, "", ""),
    "North Macedonia": AddressFormat(
        _TPL_DE, _("Municipality"), _("Postal Code"), False, r"^\d{4}$", "1000"
    ),
    "Norway": AddressFormat(_TPL_DE, _("County"), _("Postal Code"), False, r"^\d{4}$", "0001"),
    "Oman": AddressFormat(
        _TPL_DEFAULT, _("Governorate"), _("Postal Code"), False, r"^\d{3}$", "100"
    ),
    "Pakistan": AddressFormat(
        _TPL_DEFAULT_STATE, _("Province"), _("Postal Code"), True, r"^\d{5}$", "44000"
    ),
    "Palau": AddressFormat(_TPL_US, _("State"), _("ZIP Code"), False, r"^\d{5}$", "96940"),
    "Palestine": AddressFormat(
        _TPL_DEFAULT, _("Governorate"), _("Postal Code"), False, r"^\d{3}$", "100"
    ),
    "Panama": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, r"^\d{4}$", "0801"
    ),
    "Papua New Guinea": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, r"^\d{3}$", "111"
    ),
    "Paraguay": AddressFormat(
        _TPL_DEFAULT, _("Department"), _("Postal Code"), False, r"^\d{4}$", "1209"
    ),
    "Peru": AddressFormat(
        _TPL_DEFAULT_STATE, _("Region"), _("Postal Code"), True, r"^\d{5}$", "15001"
    ),
    "Philippines": AddressFormat(_TPL_US, _("Province"), _("ZIP Code"), True, r"^\d{4}$", "1000"),
    "Poland": AddressFormat(
        _TPL_DE, _("Voivodeship"), _("Postal Code"), False, r"^\d{2}-\d{3}$", "00-001"
    ),
    "Portugal": AddressFormat(
        _TPL_DE, _("District"), _("Código Postal"), False, r"^\d{4}-\d{3}$", "1000-001"
    ),
    "Qatar": AddressFormat(_TPL_DEFAULT, _("Municipality"), _("Postal Code"), False, "", ""),
    "Romania": AddressFormat(_TPL_DE, _("County"), _("Cod Poștal"), False, r"^\d{6}$", "010011"),
    "Russia": AddressFormat(_TPL_RU, _("Region"), _("Postal Code"), True, r"^\d{6}$", "101000"),
    "Rwanda": AddressFormat(_TPL_DEFAULT, _("Province"), _("Postal Code"), False, "", ""),
    "Saint Kitts and Nevis": AddressFormat(
        _TPL_DEFAULT, _("Parish"), _("Postal Code"), False, "", ""
    ),
    "Saint Lucia": AddressFormat(_TPL_DEFAULT, _("District"), _("Postal Code"), False, "", ""),
    "Saint Vincent and the Grenadines": AddressFormat(
        _TPL_DEFAULT, _("Parish"), _("Postal Code"), False, "", ""
    ),
    "Samoa": AddressFormat(
        _TPL_DEFAULT, _("District"), _("Postal Code"), False, r"^WS\d{4}$", "WS1382"
    ),
    "San Marino": AddressFormat(
        _TPL_DE, _("Municipality"), _("Postal Code"), False, r"^4789\d$", "47890"
    ),
    "Sao Tome and Principe": AddressFormat(
        _TPL_DEFAULT, _("District"), _("Postal Code"), False, "", ""
    ),
    "Saudi Arabia": AddressFormat(
        _TPL_DEFAULT, _("Region"), _("Postal Code"), False, r"^\d{5}(-\d{4})?$", "11564"
    ),
    "Senegal": AddressFormat(_TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{5}$", "10000"),
    "Serbia": AddressFormat(_TPL_DE, _("District"), _("Postal Code"), False, r"^\d{5,6}$", "11000"),
    "Seychelles": AddressFormat(_TPL_DEFAULT, _("District"), _("Postal Code"), False, "", ""),
    "Sierra Leone": AddressFormat(_TPL_DEFAULT, _("District"), _("Postal Code"), False, "", ""),
    "Singapore": AddressFormat(
        _RECIPIENT + "{address1}\n{address2}\nSingapore {postal_code}",
        _("Region"),
        _("Postal Code"),
        False,
        r"^\d{6}$",
        "018956",
    ),
    "Slovakia": AddressFormat(_TPL_DE, _("Region"), _("PSČ"), False, r"^\d{3}\s?\d{2}$", "811 01"),
    "Slovenia": AddressFormat(_TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{4}$", "1000"),
    "Solomon Islands": AddressFormat(_TPL_DEFAULT, _("Province"), _("Postal Code"), False, "", ""),
    "Somalia": AddressFormat(
        _TPL_DEFAULT, _("Region"), _("Postal Code"), False, r"^[A-Z]{2}\s?\d{5}$", "JH 09010"
    ),
    "South Africa": AddressFormat(
        _TPL_DEFAULT_STATE, _("Province"), _("Postal Code"), True, r"^\d{4}$", "0001"
    ),
    "South Korea": AddressFormat(
        _TPL_KR, _("Province"), _("Postal Code"), True, r"^\d{5}$", "03051"
    ),
    "South Sudan": AddressFormat(_TPL_DEFAULT, _("State"), _("Postal Code"), False, "", ""),
    "Spain": AddressFormat(_TPL_ES, _("Province"), _("Código Postal"), True, r"^\d{5}$", "28001"),
    "Sri Lanka": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, r"^\d{5}$", "00100"
    ),
    "Sudan": AddressFormat(_TPL_DEFAULT, _("State"), _("Postal Code"), False, r"^\d{5}$", "11111"),
    "Suriname": AddressFormat(_TPL_DEFAULT, _("District"), _("Postal Code"), False, "", ""),
    "Sweden": AddressFormat(
        _TPL_DE, _("County"), _("Postal Code"), False, r"^\d{3}\s?\d{2}$", "111 22"
    ),
    "Switzerland": AddressFormat(_TPL_DE, _("Canton"), _("PLZ"), False, r"^\d{4}$", "3000"),
    "Syria": AddressFormat(_TPL_DEFAULT, _("Governorate"), _("Postal Code"), False, "", ""),
    "Taiwan": AddressFormat(
        "{postal_code}\n{state}{city}\n{address1}\n{address2}" + _RECIPIENT_LAST,
        _("County/City"),
        _("Postal Code"),
        True,
        r"^\d{3,5}$",
        "100",
    ),
    "Tajikistan": AddressFormat(
        _TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{6}$", "734025"
    ),
    "Tanzania": AddressFormat(
        _TPL_DEFAULT, _("Region"), _("Postal Code"), False, r"^\d{5}$", "11101"
    ),
    "Thailand": AddressFormat(
        _TPL_DEFAULT_STATE, _("Province"), _("Postal Code"), True, r"^\d{5}$", "10100"
    ),
    "Timor-Leste": AddressFormat(_TPL_DEFAULT, _("Municipality"), _("Postal Code"), False, "", ""),
    "Togo": AddressFormat(_TPL_DEFAULT, _("Region"), _("Postal Code"), False, "", ""),
    "Tonga": AddressFormat(_TPL_DEFAULT, _("Division"), _("Postal Code"), False, "", ""),
    "Trinidad and Tobago": AddressFormat(
        _TPL_DEFAULT, _("Region"), _("Postal Code"), False, r"^\d{6}$", "120110"
    ),
    "Tunisia": AddressFormat(
        _TPL_DE, _("Governorate"), _("Code Postal"), False, r"^\d{4}$", "1000"
    ),
    "Turkey": AddressFormat(_TPL_ES, _("Province"), _("Postal Code"), True, r"^\d{5}$", "06100"),
    "Turkmenistan": AddressFormat(
        _TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{6}$", "744000"
    ),
    "Tuvalu": AddressFormat(_TPL_DEFAULT, _("Island"), _("Postal Code"), False, "", ""),
    "Uganda": AddressFormat(_TPL_DEFAULT, _("District"), _("Postal Code"), False, "", ""),
    "Ukraine": AddressFormat(_TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{5}$", "01001"),
    "United Arab Emirates": AddressFormat(
        _TPL_DEFAULT_STATE, _("Emirate"), _("Postal Code"), True, "", ""
    ),
    "United Kingdom": AddressFormat(
        _TPL_UK,
        _("County"),
        _("Postcode"),
        False,
        r"^[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}$",
        "SW1A 1AA",
    ),
    "United States": AddressFormat(
        _TPL_US, _("State"), _("ZIP Code"), True, r"^\d{5}(-\d{4})?$", "10001"
    ),
    "Uruguay": AddressFormat(
        _TPL_DEFAULT, _("Department"), _("Postal Code"), False, r"^\d{5}$", "11000"
    ),
    "Uzbekistan": AddressFormat(
        _TPL_DE, _("Region"), _("Postal Code"), False, r"^\d{6}$", "100000"
    ),
    "Vanuatu": AddressFormat(_TPL_DEFAULT, _("Province"), _("Postal Code"), False, "", ""),
    "Vatican City": AddressFormat(_TPL_FR, _("Region"), _("CAP"), False, r"^00120$", "00120"),
    "Venezuela": AddressFormat(
        _TPL_DEFAULT_STATE, _("State"), _("Postal Code"), True, r"^\d{4}(-[A-Z])?\d?$", "1010"
    ),
    "Vietnam": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, r"^\d{5,6}$", "100000"
    ),
    "Yemen": AddressFormat(_TPL_DEFAULT, _("Governorate"), _("Postal Code"), False, "", ""),
    "Zambia": AddressFormat(
        _TPL_DEFAULT, _("Province"), _("Postal Code"), False, r"^\d{5}$", "10101"
    ),
    "Zimbabwe": AddressFormat(_TPL_DEFAULT, _("Province"), _("Postal Code"), False, "", ""),
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_address_format(jurisdiction: str) -> AddressFormat | None:
    """
    Return the :class:`AddressFormat` for *jurisdiction*, or ``None``.

    >>> from geo_canon.address_formats import get_address_format
    >>> fmt = get_address_format("United States")
    >>> fmt.state_label
    'State'
    >>> fmt.postal_code_label
    'ZIP Code'
    """
    return JURISDICTION_ADDRESS_FORMAT.get(jurisdiction)


def get_postal_code_regex(jurisdiction: str) -> str | None:
    """
    Return the postal-code validation regex for *jurisdiction*, or ``None``.

    Returns an empty string if the jurisdiction has no standardised postal
    code system.

    >>> from geo_canon.address_formats import get_postal_code_regex
    >>> get_postal_code_regex("United States")
    '^\\\\d{5}(-\\\\d{4})?$'
    """
    fmt = JURISDICTION_ADDRESS_FORMAT.get(jurisdiction)
    return fmt.postal_code_pattern if fmt else None


def validate_postal_code(jurisdiction: str, postal_code: str) -> bool:
    """
    Return ``True`` if *postal_code* matches the expected pattern for
    *jurisdiction*.

    Returns ``True`` for jurisdictions with no known postal-code system
    (e.g. Angola, Hong Kong) — there is nothing to validate.

    Leading and trailing ASCII whitespace is ignored. The rest must match the
    whole pattern, letters case-insensitively, and only ASCII letters, digits
    and whitespace count as such.

    >>> from geo_canon.address_formats import validate_postal_code
    >>> validate_postal_code("United States", "10001")
    True
    >>> validate_postal_code("United States", "ABCDE")
    False
    >>> validate_postal_code("Hong Kong", "")
    True
    """
    fmt = JURISDICTION_ADDRESS_FORMAT.get(jurisdiction)
    if fmt is None:
        return False
    if not fmt.postal_code_pattern:
        # No postal code system — anything is acceptable
        return True
    candidate = postal_code.strip(string.whitespace)
    flags = re.IGNORECASE | re.ASCII
    return re.fullmatch(fmt.postal_code_pattern, candidate, flags) is not None


def get_state_label(jurisdiction: str) -> str | Promise | None:
    """
    Return the localised label for the "state" field (State, Province,
    County, Prefecture, etc.) for *jurisdiction*.

    >>> from geo_canon.address_formats import get_state_label
    >>> get_state_label("Japan")
    'Prefecture'
    >>> get_state_label("Canada")
    'Province'
    """
    fmt = JURISDICTION_ADDRESS_FORMAT.get(jurisdiction)
    return str(fmt.state_label) if fmt else None


def get_postal_code_label(jurisdiction: str) -> str | Promise | None:
    """
    Return the localised label for the postal-code field (ZIP Code,
    Postcode, PLZ, CEP, etc.) for *jurisdiction*.

    >>> from geo_canon.address_formats import get_postal_code_label
    >>> get_postal_code_label("United States")
    'ZIP Code'
    >>> get_postal_code_label("Germany")
    'PLZ'
    """
    fmt = JURISDICTION_ADDRESS_FORMAT.get(jurisdiction)
    return str(fmt.postal_code_label) if fmt else None


def format_address(
    jurisdiction: str,
    *,
    name: str = "",
    company: str = "",
    address1: str = "",
    address2: str = "",
    city: str = "",
    state: str = "",
    postal_code: str = "",
    country: str = "",
) -> str:
    """
    Format an address string according to *jurisdiction*'s conventions.

    Empty fields leave no blank lines or stray spaces behind.

    >>> from geo_canon.address_formats import format_address
    >>> print(format_address(
    ...     "United States",
    ...     name="Jane Doe",
    ...     address1="123 Main St",
    ...     city="New York",
    ...     state="NY",
    ...     postal_code="10001",
    ...     country="United States",
    ... ))
    Jane Doe
    123 Main St
    New York, NY 10001
    United States
    """
    fmt = JURISDICTION_ADDRESS_FORMAT.get(jurisdiction)
    if fmt is None:
        # Sensible fallback
        parts = [
            p for p in [name, company, address1, address2, city, state, postal_code, country] if p
        ]
        return "\n".join(parts)

    raw = fmt.template.format(
        name=name,
        company=company,
        address1=address1,
        address2=address2,
        city=city,
        state=state,
        postal_code=postal_code,
        country=country,
    )
    # Drop lines left empty by missing fields, and the spaces they leave behind
    lines = [" ".join(line.split()) for line in raw.splitlines() if line.strip()]
    return "\n".join(lines)


def is_state_required(jurisdiction: str) -> bool:
    """
    Return whether the state/province/region field is required in
    *jurisdiction*'s address format.

    Returns ``False`` for unknown jurisdictions.

    >>> from geo_canon.address_formats import is_state_required
    >>> is_state_required("United States")
    True
    >>> is_state_required("France")
    False
    """
    fmt = JURISDICTION_ADDRESS_FORMAT.get(jurisdiction)
    return fmt.state_required if fmt else False
