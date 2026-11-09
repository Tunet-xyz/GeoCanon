"""
GeoCanon — Dial Codes

International dialling-code choices for Django forms, a country → dial-code
mapping, and per-country phone-number validation patterns.
"""

from __future__ import annotations

import re

from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _

try:
    import phonenumbers as _phonenumbers
except ImportError:  # pragma: no cover - exercised indirectly by fallback tests
    _phonenumbers = None  # type: ignore[assignment]  # Optional module may be absent.

# ---------------------------------------------------------------------------
# Dial-code choices for Django ChoiceField / Select widgets
# ---------------------------------------------------------------------------

DIAL_CODE_CHOICES: list[tuple[str, str | Promise]] = [
    ("+93", _("Afghanistan (+93)")),
    ("+355", _("Albania (+355)")),
    ("+213", _("Algeria (+213)")),
    ("+376", _("Andorra (+376)")),
    ("+244", _("Angola (+244)")),
    ("+54", _("Argentina (+54)")),
    ("+374", _("Armenia (+374)")),
    ("+297", _("Aruba (+297)")),
    ("+61", _("Australia (+61)")),
    ("+43", _("Austria (+43)")),
    ("+994", _("Azerbaijan (+994)")),
    ("+973", _("Bahrain (+973)")),
    ("+880", _("Bangladesh (+880)")),
    ("+375", _("Belarus (+375)")),
    ("+32", _("Belgium (+32)")),
    ("+501", _("Belize (+501)")),
    ("+229", _("Benin (+229)")),
    ("+975", _("Bhutan (+975)")),
    ("+591", _("Bolivia (+591)")),
    ("+387", _("Bosnia and Herzegovina (+387)")),
    ("+267", _("Botswana (+267)")),
    ("+55", _("Brazil (+55)")),
    ("+246", _("British Indian Ocean Territory (+246)")),
    ("+673", _("Brunei (+673)")),
    ("+359", _("Bulgaria (+359)")),
    ("+226", _("Burkina Faso (+226)")),
    ("+257", _("Burundi (+257)")),
    ("+855", _("Cambodia (+855)")),
    ("+237", _("Cameroon (+237)")),
    ("+1", _("Canada / United States (+1)")),
    ("+238", _("Cape Verde (+238)")),
    ("+236", _("Central African Republic (+236)")),
    ("+235", _("Chad (+235)")),
    ("+56", _("Chile (+56)")),
    ("+86", _("China (+86)")),
    ("+57", _("Colombia (+57)")),
    ("+269", _("Comoros (+269)")),
    ("+242", _("Congo (+242)")),
    ("+243", _("Democratic Republic of Congo (+243)")),
    ("+506", _("Costa Rica (+506)")),
    ("+385", _("Croatia (+385)")),
    ("+53", _("Cuba (+53)")),
    ("+599", _("Curaçao (+599)")),
    ("+357", _("Cyprus (+357)")),
    ("+420", _("Czech Republic (+420)")),
    ("+45", _("Denmark (+45)")),
    ("+253", _("Djibouti (+253)")),
    ("+593", _("Ecuador (+593)")),
    ("+20", _("Egypt (+20)")),
    ("+503", _("El Salvador (+503)")),
    ("+240", _("Equatorial Guinea (+240)")),
    ("+291", _("Eritrea (+291)")),
    ("+372", _("Estonia (+372)")),
    ("+268", _("Eswatini (+268)")),
    ("+251", _("Ethiopia (+251)")),
    ("+500", _("Falkland Islands (+500)")),
    ("+298", _("Faroe Islands (+298)")),
    ("+679", _("Fiji (+679)")),
    ("+358", _("Finland (+358)")),
    ("+33", _("France (+33)")),
    ("+241", _("Gabon (+241)")),
    ("+220", _("Gambia (+220)")),
    ("+995", _("Georgia (+995)")),
    ("+49", _("Germany (+49)")),
    ("+233", _("Ghana (+233)")),
    ("+350", _("Gibraltar (+350)")),
    ("+30", _("Greece (+30)")),
    ("+299", _("Greenland (+299)")),
    ("+502", _("Guatemala (+502)")),
    ("+224", _("Guinea (+224)")),
    ("+245", _("Guinea-Bissau (+245)")),
    ("+592", _("Guyana (+592)")),
    ("+509", _("Haiti (+509)")),
    ("+504", _("Honduras (+504)")),
    ("+852", _("Hong Kong (+852)")),
    ("+36", _("Hungary (+36)")),
    ("+354", _("Iceland (+354)")),
    ("+91", _("India (+91)")),
    ("+62", _("Indonesia (+62)")),
    ("+98", _("Iran (+98)")),
    ("+964", _("Iraq (+964)")),
    ("+353", _("Ireland (+353)")),
    ("+972", _("Israel (+972)")),
    ("+39", _("Italy (+39)")),
    ("+225", _("Ivory Coast (+225)")),
    ("+81", _("Japan (+81)")),
    ("+962", _("Jordan (+962)")),
    ("+7", _("Kazakhstan / Russia (+7)")),
    ("+254", _("Kenya (+254)")),
    ("+686", _("Kiribati (+686)")),
    ("+383", _("Kosovo (+383)")),
    ("+965", _("Kuwait (+965)")),
    ("+996", _("Kyrgyzstan (+996)")),
    ("+856", _("Laos (+856)")),
    ("+371", _("Latvia (+371)")),
    ("+961", _("Lebanon (+961)")),
    ("+266", _("Lesotho (+266)")),
    ("+231", _("Liberia (+231)")),
    ("+218", _("Libya (+218)")),
    ("+423", _("Liechtenstein (+423)")),
    ("+370", _("Lithuania (+370)")),
    ("+352", _("Luxembourg (+352)")),
    ("+853", _("Macau (+853)")),
    ("+261", _("Madagascar (+261)")),
    ("+265", _("Malawi (+265)")),
    ("+60", _("Malaysia (+60)")),
    ("+960", _("Maldives (+960)")),
    ("+223", _("Mali (+223)")),
    ("+356", _("Malta (+356)")),
    ("+692", _("Marshall Islands (+692)")),
    ("+222", _("Mauritania (+222)")),
    ("+230", _("Mauritius (+230)")),
    ("+52", _("Mexico (+52)")),
    ("+691", _("Micronesia (+691)")),
    ("+373", _("Moldova (+373)")),
    ("+377", _("Monaco (+377)")),
    ("+976", _("Mongolia (+976)")),
    ("+382", _("Montenegro (+382)")),
    ("+212", _("Morocco (+212)")),
    ("+258", _("Mozambique (+258)")),
    ("+95", _("Myanmar (+95)")),
    ("+264", _("Namibia (+264)")),
    ("+674", _("Nauru (+674)")),
    ("+977", _("Nepal (+977)")),
    ("+31", _("Netherlands (+31)")),
    ("+64", _("New Zealand (+64)")),
    ("+505", _("Nicaragua (+505)")),
    ("+227", _("Niger (+227)")),
    ("+234", _("Nigeria (+234)")),
    ("+850", _("North Korea (+850)")),
    ("+389", _("North Macedonia (+389)")),
    ("+47", _("Norway (+47)")),
    ("+968", _("Oman (+968)")),
    ("+92", _("Pakistan (+92)")),
    ("+680", _("Palau (+680)")),
    ("+970", _("Palestine (+970)")),
    ("+507", _("Panama (+507)")),
    ("+675", _("Papua New Guinea (+675)")),
    ("+595", _("Paraguay (+595)")),
    ("+51", _("Peru (+51)")),
    ("+63", _("Philippines (+63)")),
    ("+48", _("Poland (+48)")),
    ("+351", _("Portugal (+351)")),
    ("+974", _("Qatar (+974)")),
    ("+262", _("Réunion (+262)")),
    ("+40", _("Romania (+40)")),
    ("+250", _("Rwanda (+250)")),
    ("+290", _("Saint Helena (+290)")),
    ("+685", _("Samoa (+685)")),
    ("+378", _("San Marino (+378)")),
    ("+239", _("Sao Tome and Principe (+239)")),
    ("+966", _("Saudi Arabia (+966)")),
    ("+221", _("Senegal (+221)")),
    ("+381", _("Serbia (+381)")),
    ("+248", _("Seychelles (+248)")),
    ("+232", _("Sierra Leone (+232)")),
    ("+65", _("Singapore (+65)")),
    ("+421", _("Slovakia (+421)")),
    ("+386", _("Slovenia (+386)")),
    ("+677", _("Solomon Islands (+677)")),
    ("+252", _("Somalia (+252)")),
    ("+27", _("South Africa (+27)")),
    ("+82", _("South Korea (+82)")),
    ("+211", _("South Sudan (+211)")),
    ("+34", _("Spain (+34)")),
    ("+94", _("Sri Lanka (+94)")),
    ("+249", _("Sudan (+249)")),
    ("+597", _("Suriname (+597)")),
    ("+46", _("Sweden (+46)")),
    ("+41", _("Switzerland (+41)")),
    ("+963", _("Syria (+963)")),
    ("+886", _("Taiwan (+886)")),
    ("+992", _("Tajikistan (+992)")),
    ("+255", _("Tanzania (+255)")),
    ("+66", _("Thailand (+66)")),
    ("+670", _("Timor-Leste (+670)")),
    ("+228", _("Togo (+228)")),
    ("+676", _("Tonga (+676)")),
    ("+216", _("Tunisia (+216)")),
    ("+90", _("Turkey (+90)")),
    ("+993", _("Turkmenistan (+993)")),
    ("+688", _("Tuvalu (+688)")),
    ("+256", _("Uganda (+256)")),
    ("+380", _("Ukraine (+380)")),
    ("+971", _("United Arab Emirates (+971)")),
    ("+44", _("United Kingdom (+44)")),
    ("+598", _("Uruguay (+598)")),
    ("+998", _("Uzbekistan (+998)")),
    ("+678", _("Vanuatu (+678)")),
    ("+58", _("Venezuela (+58)")),
    ("+84", _("Vietnam (+84)")),
    ("+967", _("Yemen (+967)")),
    ("+260", _("Zambia (+260)")),
    ("+263", _("Zimbabwe (+263)")),
]

# ---------------------------------------------------------------------------
# Country name → dial code (quick lookup)
# ---------------------------------------------------------------------------

COUNTRY_DIAL_CODE: dict[str, str] = {
    "Afghanistan": "+93",
    "Albania": "+355",
    "Algeria": "+213",
    "Andorra": "+376",
    "Angola": "+244",
    "Antigua and Barbuda": "+1",
    "Argentina": "+54",
    "Armenia": "+374",
    "Aruba": "+297",
    "Australia": "+61",
    "Austria": "+43",
    "Azerbaijan": "+994",
    "Bahamas": "+1",
    "Bahrain": "+973",
    "Bangladesh": "+880",
    "Barbados": "+1",
    "Belarus": "+375",
    "Belgium": "+32",
    "Belize": "+501",
    "Benin": "+229",
    "Bhutan": "+975",
    "Bolivia": "+591",
    "Bosnia and Herzegovina": "+387",
    "Botswana": "+267",
    "Brazil": "+55",
    "Brunei": "+673",
    "Bulgaria": "+359",
    "Burkina Faso": "+226",
    "Burundi": "+257",
    "Cabo Verde": "+238",
    "Cambodia": "+855",
    "Cameroon": "+237",
    "Canada": "+1",
    "Cape Verde": "+238",
    "Central African Republic": "+236",
    "Chad": "+235",
    "Chile": "+56",
    "China": "+86",
    "Colombia": "+57",
    "Comoros": "+269",
    "Congo": "+242",
    "Congo (Congo-Brazzaville)": "+242",
    "Congo (DRC)": "+243",
    "Costa Rica": "+506",
    "Cote d'Ivoire": "+225",
    "Croatia": "+385",
    "Cuba": "+53",
    "Curacao": "+599",
    "Cyprus": "+357",
    "Czech Republic": "+420",
    "Democratic Republic of Congo": "+243",
    "Denmark": "+45",
    "Djibouti": "+253",
    "Dominica": "+1",
    "Dominican Republic": "+1",
    "Ecuador": "+593",
    "Egypt": "+20",
    "El Salvador": "+503",
    "Equatorial Guinea": "+240",
    "Eritrea": "+291",
    "Estonia": "+372",
    "Eswatini": "+268",
    "Ethiopia": "+251",
    "Fiji": "+679",
    "Finland": "+358",
    "France": "+33",
    "Gabon": "+241",
    "Gambia": "+220",
    "Georgia": "+995",
    "Germany": "+49",
    "Ghana": "+233",
    "Greece": "+30",
    "Grenada": "+1",
    "Guatemala": "+502",
    "Guinea": "+224",
    "Guinea-Bissau": "+245",
    "Guyana": "+592",
    "Haiti": "+509",
    "Honduras": "+504",
    "Hong Kong": "+852",
    "Hungary": "+36",
    "Iceland": "+354",
    "India": "+91",
    "Indonesia": "+62",
    "Iran": "+98",
    "Iraq": "+964",
    "Ireland": "+353",
    "Israel": "+972",
    "Italy": "+39",
    "Ivory Coast": "+225",
    "Jamaica": "+1",
    "Japan": "+81",
    "Jordan": "+962",
    "Kazakhstan": "+7",
    "Kenya": "+254",
    "Kiribati": "+686",
    "Korea (North)": "+850",
    "Korea (South)": "+82",
    "Kosovo": "+383",
    "Kuwait": "+965",
    "Kyrgyzstan": "+996",
    "Laos": "+856",
    "Latvia": "+371",
    "Lebanon": "+961",
    "Lesotho": "+266",
    "Liberia": "+231",
    "Libya": "+218",
    "Liechtenstein": "+423",
    "Lithuania": "+370",
    "Luxembourg": "+352",
    "Madagascar": "+261",
    "Malawi": "+265",
    "Malaysia": "+60",
    "Maldives": "+960",
    "Mali": "+223",
    "Malta": "+356",
    "Marshall Islands": "+692",
    "Mauritania": "+222",
    "Mauritius": "+230",
    "Mexico": "+52",
    "Micronesia": "+691",
    "Moldova": "+373",
    "Monaco": "+377",
    "Mongolia": "+976",
    "Montenegro": "+382",
    "Morocco": "+212",
    "Mozambique": "+258",
    "Myanmar": "+95",
    "Namibia": "+264",
    "Nauru": "+674",
    "Nepal": "+977",
    "Netherlands": "+31",
    "New Zealand": "+64",
    "Nicaragua": "+505",
    "Niger": "+227",
    "Nigeria": "+234",
    "North Korea": "+850",
    "North Macedonia": "+389",
    "Norway": "+47",
    "Oman": "+968",
    "Pakistan": "+92",
    "Palau": "+680",
    "Palestine": "+970",
    "Panama": "+507",
    "Papua New Guinea": "+675",
    "Paraguay": "+595",
    "Peru": "+51",
    "Philippines": "+63",
    "Poland": "+48",
    "Portugal": "+351",
    "Qatar": "+974",
    "Romania": "+40",
    "Russia": "+7",
    "Rwanda": "+250",
    "Saint Kitts and Nevis": "+1",
    "Saint Lucia": "+1",
    "Saint Vincent and the Grenadines": "+1",
    "Samoa": "+685",
    "San Marino": "+378",
    "Sao Tome and Principe": "+239",
    "Saudi Arabia": "+966",
    "Senegal": "+221",
    "Serbia": "+381",
    "Seychelles": "+248",
    "Sierra Leone": "+232",
    "Singapore": "+65",
    "Slovakia": "+421",
    "Slovenia": "+386",
    "Solomon Islands": "+677",
    "Somalia": "+252",
    "South Africa": "+27",
    "South Korea": "+82",
    "South Sudan": "+211",
    "Spain": "+34",
    "Sri Lanka": "+94",
    "Sudan": "+249",
    "Suriname": "+597",
    "Sweden": "+46",
    "Switzerland": "+41",
    "Syria": "+963",
    "Taiwan": "+886",
    "Tajikistan": "+992",
    "Tanzania": "+255",
    "Thailand": "+66",
    "Timor-Leste": "+670",
    "Togo": "+228",
    "Tonga": "+676",
    "Trinidad and Tobago": "+1",
    "Tunisia": "+216",
    "Turkey": "+90",
    "Turkmenistan": "+993",
    "Tuvalu": "+688",
    "Uganda": "+256",
    "Ukraine": "+380",
    "United Arab Emirates": "+971",
    "United Kingdom": "+44",
    "United States": "+1",
    "Uruguay": "+598",
    "Uzbekistan": "+998",
    "Vanuatu": "+678",
    "Vatican City": "+39",
    "Venezuela": "+58",
    "Vietnam": "+84",
    "Yemen": "+967",
    "Zambia": "+260",
    "Zimbabwe": "+263",
}

# ---------------------------------------------------------------------------
# Per-dial-code phone-number validation patterns (national digits only)
# ---------------------------------------------------------------------------


def _national_number(pattern: str) -> re.Pattern[str]:
    """Compile a national-number pattern in which ``\\d`` matches only 0-9."""
    return re.compile(pattern, re.ASCII)


PHONE_PATTERNS: dict[str, re.Pattern[str]] = {
    "+93": _national_number(r"^\d{9}$"),  # Afghanistan
    "+355": _national_number(r"^\d{9}$"),  # Albania
    "+213": _national_number(r"^\d{9}$"),  # Algeria
    "+376": _national_number(r"^\d{6}$"),  # Andorra
    "+244": _national_number(r"^\d{9}$"),  # Angola
    "+54": _national_number(r"^\d{10}$"),  # Argentina
    "+374": _national_number(r"^\d{8}$"),  # Armenia
    "+297": _national_number(r"^\d{7}$"),  # Aruba
    "+61": _national_number(r"^\d{9}$"),  # Australia
    "+43": _national_number(r"^\d{10,11}$"),  # Austria
    "+994": _national_number(r"^\d{9}$"),  # Azerbaijan
    "+973": _national_number(r"^\d{8}$"),  # Bahrain
    "+880": _national_number(r"^\d{10}$"),  # Bangladesh
    "+375": _national_number(r"^\d{9}$"),  # Belarus
    "+32": _national_number(r"^\d{9}$"),  # Belgium
    "+501": _national_number(r"^\d{7}$"),  # Belize
    "+229": _national_number(r"^\d{8}$"),  # Benin
    "+975": _national_number(r"^\d{7,8}$"),  # Bhutan
    "+591": _national_number(r"^\d{8}$"),  # Bolivia
    "+387": _national_number(r"^\d{8}$"),  # Bosnia and Herzegovina
    "+267": _national_number(r"^\d{7,8}$"),  # Botswana
    "+55": _national_number(r"^\d{10,11}$"),  # Brazil
    "+246": _national_number(r"^\d{7}$"),  # British Indian Ocean Territory
    "+673": _national_number(r"^\d{7}$"),  # Brunei
    "+359": _national_number(r"^\d{9}$"),  # Bulgaria
    "+226": _national_number(r"^\d{8}$"),  # Burkina Faso
    "+257": _national_number(r"^\d{8}$"),  # Burundi
    "+855": _national_number(r"^\d{8,9}$"),  # Cambodia
    "+237": _national_number(r"^\d{9}$"),  # Cameroon
    "+1": _national_number(r"^\d{10}$"),  # Canada / United States
    "+238": _national_number(r"^\d{7}$"),  # Cape Verde
    "+236": _national_number(r"^\d{8}$"),  # Central African Republic
    "+235": _national_number(r"^\d{8}$"),  # Chad
    "+56": _national_number(r"^\d{9}$"),  # Chile
    "+86": _national_number(r"^\d{11}$"),  # China
    "+57": _national_number(r"^\d{10}$"),  # Colombia
    "+269": _national_number(r"^\d{7}$"),  # Comoros
    "+242": _national_number(r"^\d{9}$"),  # Congo
    "+243": _national_number(r"^\d{9}$"),  # DR Congo
    "+506": _national_number(r"^\d{8}$"),  # Costa Rica
    "+385": _national_number(r"^\d{8,9}$"),  # Croatia
    "+53": _national_number(r"^\d{8}$"),  # Cuba
    "+599": _national_number(r"^\d{7,8}$"),  # Curaçao
    "+357": _national_number(r"^\d{8}$"),  # Cyprus
    "+420": _national_number(r"^\d{9}$"),  # Czech Republic
    "+45": _national_number(r"^\d{8}$"),  # Denmark
    "+253": _national_number(r"^\d{8}$"),  # Djibouti
    "+593": _national_number(r"^\d{9}$"),  # Ecuador
    "+20": _national_number(r"^\d{10}$"),  # Egypt
    "+503": _national_number(r"^\d{8}$"),  # El Salvador
    "+240": _national_number(r"^\d{9}$"),  # Equatorial Guinea
    "+291": _national_number(r"^\d{7}$"),  # Eritrea
    "+372": _national_number(r"^\d{7,8}$"),  # Estonia
    "+268": _national_number(r"^\d{8}$"),  # Eswatini
    "+251": _national_number(r"^\d{9}$"),  # Ethiopia
    "+500": _national_number(r"^\d{5}$"),  # Falkland Islands
    "+298": _national_number(r"^\d{6}$"),  # Faroe Islands
    "+679": _national_number(r"^\d{7}$"),  # Fiji
    "+358": _national_number(r"^\d{9,10}$"),  # Finland
    "+33": _national_number(r"^\d{9}$"),  # France
    "+241": _national_number(r"^\d{7}$"),  # Gabon
    "+220": _national_number(r"^\d{7}$"),  # Gambia
    "+995": _national_number(r"^\d{9}$"),  # Georgia
    "+49": _national_number(r"^\d{10,11}$"),  # Germany
    "+233": _national_number(r"^\d{9}$"),  # Ghana
    "+350": _national_number(r"^\d{8}$"),  # Gibraltar
    "+30": _national_number(r"^\d{10}$"),  # Greece
    "+299": _national_number(r"^\d{6}$"),  # Greenland
    "+502": _national_number(r"^\d{8}$"),  # Guatemala
    "+224": _national_number(r"^\d{9}$"),  # Guinea
    "+245": _national_number(r"^\d{7}$"),  # Guinea-Bissau
    "+592": _national_number(r"^\d{7}$"),  # Guyana
    "+509": _national_number(r"^\d{8}$"),  # Haiti
    "+504": _national_number(r"^\d{8}$"),  # Honduras
    "+852": _national_number(r"^\d{8}$"),  # Hong Kong
    "+36": _national_number(r"^\d{9}$"),  # Hungary
    "+354": _national_number(r"^\d{7}$"),  # Iceland
    "+91": _national_number(r"^\d{10}$"),  # India
    "+62": _national_number(r"^\d{9,11}$"),  # Indonesia
    "+98": _national_number(r"^\d{10}$"),  # Iran
    "+964": _national_number(r"^\d{10}$"),  # Iraq
    "+353": _national_number(r"^\d{9}$"),  # Ireland
    "+972": _national_number(r"^\d{9}$"),  # Israel
    "+39": _national_number(r"^\d{9,10}$"),  # Italy
    "+225": _national_number(r"^\d{10}$"),  # Ivory Coast
    "+81": _national_number(r"^\d{10}$"),  # Japan
    "+962": _national_number(r"^\d{9}$"),  # Jordan
    "+7": _national_number(r"^\d{10}$"),  # Kazakhstan / Russia
    "+254": _national_number(r"^\d{9}$"),  # Kenya
    "+686": _national_number(r"^(?:\d{5}|\d{8})$"),  # Kiribati
    "+383": _national_number(r"^\d{8,9}$"),  # Kosovo
    "+965": _national_number(r"^\d{8}$"),  # Kuwait
    "+996": _national_number(r"^\d{9}$"),  # Kyrgyzstan
    "+856": _national_number(r"^\d{8}$"),  # Laos
    "+371": _national_number(r"^\d{8}$"),  # Latvia
    "+961": _national_number(r"^\d{7,8}$"),  # Lebanon
    "+266": _national_number(r"^\d{8}$"),  # Lesotho
    "+231": _national_number(r"^\d{7,8}$"),  # Liberia
    "+218": _national_number(r"^\d{9}$"),  # Libya
    "+423": _national_number(r"^\d{7}$"),  # Liechtenstein
    "+370": _national_number(r"^\d{8}$"),  # Lithuania
    "+352": _national_number(r"^\d{8,9}$"),  # Luxembourg
    "+853": _national_number(r"^\d{8}$"),  # Macau
    "+261": _national_number(r"^\d{9}$"),  # Madagascar
    "+265": _national_number(r"^\d{9}$"),  # Malawi
    "+60": _national_number(r"^\d{9,10}$"),  # Malaysia
    "+960": _national_number(r"^\d{7}$"),  # Maldives
    "+223": _national_number(r"^\d{8}$"),  # Mali
    "+356": _national_number(r"^\d{8}$"),  # Malta
    "+692": _national_number(r"^\d{7}$"),  # Marshall Islands
    "+222": _national_number(r"^\d{8}$"),  # Mauritania
    "+230": _national_number(r"^\d{8}$"),  # Mauritius
    "+52": _national_number(r"^\d{10}$"),  # Mexico
    "+691": _national_number(r"^\d{7}$"),  # Micronesia
    "+373": _national_number(r"^\d{8}$"),  # Moldova
    "+377": _national_number(r"^\d{8}$"),  # Monaco
    "+976": _national_number(r"^\d{8}$"),  # Mongolia
    "+382": _national_number(r"^\d{8}$"),  # Montenegro
    "+212": _national_number(r"^\d{9}$"),  # Morocco
    "+258": _national_number(r"^\d{9}$"),  # Mozambique
    "+95": _national_number(r"^\d{9,10}$"),  # Myanmar
    "+264": _national_number(r"^\d{9}$"),  # Namibia
    "+674": _national_number(r"^\d{7}$"),  # Nauru
    "+977": _national_number(r"^\d{10}$"),  # Nepal
    "+31": _national_number(r"^\d{9}$"),  # Netherlands
    "+64": _national_number(r"^\d{8,9}$"),  # New Zealand
    "+505": _national_number(r"^\d{8}$"),  # Nicaragua
    "+227": _national_number(r"^\d{8}$"),  # Niger
    "+234": _national_number(r"^\d{10}$"),  # Nigeria
    "+850": _national_number(r"^\d{10}$"),  # North Korea
    "+389": _national_number(r"^\d{8}$"),  # North Macedonia
    "+47": _national_number(r"^\d{8}$"),  # Norway
    "+968": _national_number(r"^\d{8}$"),  # Oman
    "+92": _national_number(r"^\d{10}$"),  # Pakistan
    "+680": _national_number(r"^\d{7}$"),  # Palau
    "+970": _national_number(r"^\d{8,9}$"),  # Palestine
    "+507": _national_number(r"^\d{8}$"),  # Panama
    "+675": _national_number(r"^\d{8}$"),  # Papua New Guinea
    "+595": _national_number(r"^\d{9}$"),  # Paraguay
    "+51": _national_number(r"^\d{9}$"),  # Peru
    "+63": _national_number(r"^\d{10}$"),  # Philippines
    "+48": _national_number(r"^\d{9}$"),  # Poland
    "+351": _national_number(r"^\d{9}$"),  # Portugal
    "+974": _national_number(r"^\d{8}$"),  # Qatar
    "+262": _national_number(r"^\d{9}$"),  # Réunion
    "+40": _national_number(r"^\d{9}$"),  # Romania
    "+250": _national_number(r"^\d{9}$"),  # Rwanda
    "+290": _national_number(r"^\d{4,5}$"),  # Saint Helena
    "+685": _national_number(r"^\d{5,7}$"),  # Samoa
    "+378": _national_number(r"^\d{8,10}$"),  # San Marino
    "+239": _national_number(r"^\d{7}$"),  # Sao Tome and Principe
    "+966": _national_number(r"^\d{9}$"),  # Saudi Arabia
    "+221": _national_number(r"^\d{9}$"),  # Senegal
    "+381": _national_number(r"^\d{9}$"),  # Serbia
    "+248": _national_number(r"^\d{7}$"),  # Seychelles
    "+232": _national_number(r"^\d{8}$"),  # Sierra Leone
    "+65": _national_number(r"^\d{8}$"),  # Singapore
    "+421": _national_number(r"^\d{9}$"),  # Slovakia
    "+386": _national_number(r"^\d{8}$"),  # Slovenia
    "+677": _national_number(r"^(?:\d{5}|\d{7})$"),  # Solomon Islands
    "+252": _national_number(r"^\d{8}$"),  # Somalia
    "+27": _national_number(r"^\d{9}$"),  # South Africa
    "+82": _national_number(r"^\d{9,10}$"),  # South Korea
    "+211": _national_number(r"^\d{9}$"),  # South Sudan
    "+34": _national_number(r"^\d{9}$"),  # Spain
    "+94": _national_number(r"^\d{9}$"),  # Sri Lanka
    "+249": _national_number(r"^\d{9}$"),  # Sudan
    "+597": _national_number(r"^\d{7}$"),  # Suriname
    "+46": _national_number(r"^\d{9}$"),  # Sweden
    "+41": _national_number(r"^\d{9}$"),  # Switzerland
    "+963": _national_number(r"^\d{9}$"),  # Syria
    "+886": _national_number(r"^\d{9}$"),  # Taiwan
    "+992": _national_number(r"^\d{9}$"),  # Tajikistan
    "+255": _national_number(r"^\d{9}$"),  # Tanzania
    "+66": _national_number(r"^\d{9}$"),  # Thailand
    "+670": _national_number(r"^\d{7,8}$"),  # Timor-Leste
    "+228": _national_number(r"^\d{8}$"),  # Togo
    "+676": _national_number(r"^\d{5}$"),  # Tonga
    "+216": _national_number(r"^\d{8}$"),  # Tunisia
    "+90": _national_number(r"^\d{10}$"),  # Turkey
    "+993": _national_number(r"^\d{8}$"),  # Turkmenistan
    "+688": _national_number(r"^\d{5,7}$"),  # Tuvalu
    "+256": _national_number(r"^\d{9}$"),  # Uganda
    "+380": _national_number(r"^\d{9}$"),  # Ukraine
    "+971": _national_number(r"^\d{9}$"),  # UAE
    "+44": _national_number(r"^\d{10}$"),  # United Kingdom
    "+598": _national_number(r"^\d{8}$"),  # Uruguay
    "+998": _national_number(r"^\d{9}$"),  # Uzbekistan
    "+678": _national_number(r"^(?:\d{5}|\d{7})$"),  # Vanuatu
    "+58": _national_number(r"^\d{10}$"),  # Venezuela
    "+84": _national_number(r"^\d{9,10}$"),  # Vietnam
    "+967": _national_number(r"^\d{9}$"),  # Yemen
    "+260": _national_number(r"^\d{9}$"),  # Zambia
    "+263": _national_number(r"^\d{9}$"),  # Zimbabwe
}


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------


def get_dial_code_choices() -> list[tuple[str, str | Promise]]:
    """Return dial-code choices suitable for a Django ``ChoiceField``."""
    return list(DIAL_CODE_CHOICES)


def get_dial_code(country: str) -> str | None:
    """
    Return the international dial code for *country*, or ``None``.

    >>> get_dial_code("Romania")
    '+40'
    """
    return COUNTRY_DIAL_CODE.get(country)


def validate_phone(phone: str, dial_code: str) -> bool:
    """
    Validate that *phone* (national digits only, no leading zero) matches the
    expected pattern for *dial_code*.

    The whole string must match, and only the ASCII digits 0-9 count as
    digits. Returns ``True`` when valid, ``False`` otherwise.

    >>> validate_phone("7123456789", "+44")
    True
    """
    pattern = PHONE_PATTERNS.get(dial_code)
    if pattern is None:
        return False
    return pattern.fullmatch(phone) is not None


def is_phone_extra_available() -> bool:
    """Return whether the optional ``phonenumbers`` dependency is installed."""
    return _phonenumbers is not None


def _get_region_code(jurisdiction: str | None = None, region: str | None = None) -> str | None:
    if region:
        return region.upper()
    if not jurisdiction:
        return None

    from geo_canon.iso_codes import get_alpha2

    return get_alpha2(jurisdiction)


def _parse_phone_number(
    phone: str,
    jurisdiction: str | None = None,
    region: str | None = None,
):
    if _phonenumbers is None:
        return None

    region_code = _get_region_code(jurisdiction, region)
    try:
        return _phonenumbers.parse(phone, region_code)
    except _phonenumbers.NumberParseException:
        return None


def _national_digits_for_fallback(phone: str, dial_code: str) -> str:
    digits = re.sub(r"\D", "", phone)
    calling_code = dial_code.lstrip("+")

    if phone.strip().startswith("+") and digits.startswith(calling_code):
        digits = digits[len(calling_code) :]

    if digits.startswith("0"):
        digits = digits[1:]

    return digits


def validate_phone_number(
    phone: str,
    jurisdiction: str | None = None,
    *,
    region: str | None = None,
) -> bool:
    """
    Validate a phone number using ``phonenumbers`` when installed.

    ``jurisdiction`` is converted to its ISO-3166 alpha-2 region code.  When
    the optional dependency is not installed, this falls back to GeoCanon's
    lightweight dial-code regex validation for known jurisdictions.
    """
    if _phonenumbers is not None:
        parsed = _parse_phone_number(phone, jurisdiction, region)
        return bool(parsed and _phonenumbers.is_valid_number(parsed))

    dial_code = None
    if jurisdiction is not None:
        dial_code = get_dial_code(jurisdiction)
    elif region is not None:
        from geo_canon.iso_codes import get_jurisdiction_by_alpha2

        region_jurisdiction = get_jurisdiction_by_alpha2(region)
        if region_jurisdiction is not None:
            dial_code = get_dial_code(region_jurisdiction)

    if dial_code is None:
        return False

    return validate_phone(_national_digits_for_fallback(phone, dial_code), dial_code)


def format_phone_number(
    phone: str,
    jurisdiction: str | None = None,
    *,
    region: str | None = None,
    phone_format: str = "E164",
) -> str | None:
    """
    Format a phone number with ``phonenumbers``.

    Supported formats are ``E164``, ``INTERNATIONAL``, ``NATIONAL``, and
    ``RFC3966``.  Returns ``None`` when the optional dependency is not
    installed or the number cannot be parsed.
    """
    if _phonenumbers is None:
        return None

    parsed = _parse_phone_number(phone, jurisdiction, region)
    if parsed is None or not _phonenumbers.is_possible_number(parsed):
        return None

    normalized_format = phone_format.upper().replace("-", "_")
    format_value = getattr(_phonenumbers.PhoneNumberFormat, normalized_format, None)
    if format_value is None:
        return None

    return _phonenumbers.format_number(parsed, format_value)


def get_phone_number_type(
    phone: str,
    jurisdiction: str | None = None,
    *,
    region: str | None = None,
) -> str | None:
    """
    Return the phone-number type reported by ``phonenumbers``.

    Examples include ``"mobile"``, ``"fixed_line"``, and
    ``"fixed_line_or_mobile"``.  Returns ``None`` when the optional dependency
    is not installed or the number cannot be parsed.
    """
    if _phonenumbers is None:
        return None

    parsed = _parse_phone_number(phone, jurisdiction, region)
    if parsed is None or not _phonenumbers.is_possible_number(parsed):
        return None

    phone_type = _phonenumbers.number_type(parsed)
    type_names = {
        _phonenumbers.PhoneNumberType.FIXED_LINE: "fixed_line",
        _phonenumbers.PhoneNumberType.MOBILE: "mobile",
        _phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "fixed_line_or_mobile",
        _phonenumbers.PhoneNumberType.TOLL_FREE: "toll_free",
        _phonenumbers.PhoneNumberType.PREMIUM_RATE: "premium_rate",
        _phonenumbers.PhoneNumberType.SHARED_COST: "shared_cost",
        _phonenumbers.PhoneNumberType.VOIP: "voip",
        _phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "personal_number",
        _phonenumbers.PhoneNumberType.PAGER: "pager",
        _phonenumbers.PhoneNumberType.UAN: "uan",
        _phonenumbers.PhoneNumberType.VOICEMAIL: "voicemail",
        _phonenumbers.PhoneNumberType.UNKNOWN: "unknown",
    }
    return type_names.get(phone_type, "unknown")
