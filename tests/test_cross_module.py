"""Every module must accept the same jurisdiction names and agree on what they mean."""

from __future__ import annotations

from zoneinfo import ZoneInfo

import pytest

from geo_canon.address_formats import JURISDICTION_ADDRESS_FORMAT
from geo_canon.currencies import JURISDICTION_CURRENCY
from geo_canon.dial_codes import (
    COUNTRY_DIAL_CODE,
    DIAL_CODE_CHOICES,
    PHONE_PATTERNS,
    validate_phone_number,
)
from geo_canon.flags import FLAG_CSS_CLASS, get_country_by_iso
from geo_canon.iso_codes import (
    ISO_ALPHA2_TO_JURISDICTION,
    ISO_ALPHA3_TO_JURISDICTION,
    JURISDICTION_ISO,
    get_jurisdiction_by_alpha2,
    get_jurisdiction_by_alpha3,
)
from geo_canon.jurisdictions import JURISDICTION_NAMES, JURISDICTIONS, is_valid_jurisdiction
from geo_canon.languages import JURISDICTION_LANGUAGE, LANGUAGE_CHOICES
from geo_canon.timezones import TIMEZONE_MAP

# Older names that every lookup still accepts, and the canonical key each one means.
LEGACY_ALIASES = {
    "Cape Verde": "Cabo Verde",
    "Congo": "Congo (Congo-Brazzaville)",
    "Democratic Republic of Congo": "Congo (DRC)",
    "Ivory Coast": "Cote d'Ivoire",
    "North Korea": "Korea (North)",
    "South Korea": "Korea (South)",
}
# ISO 3166 entries that every lookup accepts but the jurisdiction list leaves out.
ISO_ONLY = {"Aruba", "Curacao", "Palestine"}
ACCEPTED_NAMES = JURISDICTION_NAMES | set(LEGACY_ALIASES) | ISO_ONLY

TABLES = {
    "address formats": JURISDICTION_ADDRESS_FORMAT,
    "currencies": JURISDICTION_CURRENCY,
    "dial codes": COUNTRY_DIAL_CODE,
    "flags": FLAG_CSS_CLASS,
    "ISO codes": JURISDICTION_ISO,
    "languages": JURISDICTION_LANGUAGE,
    "timezones": TIMEZONE_MAP,
}


@pytest.mark.parametrize("table", sorted(TABLES))
def test_every_table_covers_every_accepted_name(table):
    assert sorted(ACCEPTED_NAMES - set(TABLES[table])) == []


@pytest.mark.parametrize("table", sorted(TABLES))
def test_no_table_holds_a_name_the_others_lack(table):
    assert sorted(set(TABLES[table]) - ACCEPTED_NAMES) == []


def test_aliases_and_iso_only_names_are_not_jurisdictions():
    for name in set(LEGACY_ALIASES) | ISO_ONLY:
        assert is_valid_jurisdiction(name) is False, name
    for canonical in LEGACY_ALIASES.values():
        assert is_valid_jurisdiction(canonical) is True, canonical


@pytest.mark.parametrize(("alias", "canonical"), sorted(LEGACY_ALIASES.items()))
def test_legacy_aliases_resolve_like_their_canonical_key(alias, canonical):
    for name, table in TABLES.items():
        if name == "ISO codes":
            assert table[alias][:3] == table[canonical][:3]
        else:
            assert table[alias] == table[canonical], name


def test_reverse_iso_lookups_return_canonical_keys():
    for name in JURISDICTION_NAMES:
        info = JURISDICTION_ISO[name]
        assert get_jurisdiction_by_alpha2(info.alpha_2) == name
        assert get_jurisdiction_by_alpha3(info.alpha_3) == name
        assert get_country_by_iso(info.alpha_2.lower()) == name
    for index in (ISO_ALPHA2_TO_JURISDICTION, ISO_ALPHA3_TO_JURISDICTION):
        for code, name in index.items():
            assert is_valid_jurisdiction(name) or name in ISO_ONLY, (code, name)


def test_cote_d_ivoire_is_a_jurisdiction_with_its_iso_codes():
    assert ("Cote d'Ivoire", "Côte d'Ivoire") in [(key, str(label)) for key, label in JURISDICTIONS]
    assert get_jurisdiction_by_alpha2("CI") == "Cote d'Ivoire"
    assert get_jurisdiction_by_alpha3("civ") == "Cote d'Ivoire"
    assert FLAG_CSS_CLASS["Cote d'Ivoire"] == "fi-ci"


def test_jurisdictions_sort_by_label_ignoring_accents():
    keys = [key for key, _label in JURISDICTIONS]
    assert keys.index("Costa Rica") + 1 == keys.index("Cote d'Ivoire")
    assert keys.index("Cote d'Ivoire") + 1 == keys.index("Croatia")


def test_every_default_language_is_a_language_choice():
    codes = {code for code, _label in LANGUAGE_CHOICES}
    assert sorted(set(JURISDICTION_LANGUAGE.values()) - codes) == []


def test_every_timezone_is_a_valid_iana_zone():
    for name, zone in TIMEZONE_MAP.items():
        assert ZoneInfo(zone).key == zone, name


def test_jurisdictions_sharing_a_currency_agree_on_its_details():
    first_seen: dict[str, object] = {}
    for name, info in JURISDICTION_CURRENCY.items():
        assert first_seen.setdefault(info.code, info) == info, name


def test_every_dial_code_has_one_choice_and_a_pattern():
    choice_codes = [code for code, _label in DIAL_CODE_CHOICES]
    assert len(choice_codes) == len(set(choice_codes))
    assert set(choice_codes) == set(PHONE_PATTERNS)
    assert sorted(set(COUNTRY_DIAL_CODE.values()) - set(choice_codes)) == []


@pytest.mark.parametrize(
    "name",
    [
        "Antigua and Barbuda",
        "Bahamas",
        "Barbados",
        "Dominica",
        "Dominican Republic",
        "Grenada",
        "Jamaica",
        "Saint Kitts and Nevis",
        "Saint Lucia",
        "Saint Vincent and the Grenadines",
        "Trinidad and Tobago",
    ],
)
def test_north_american_numbering_plan_countries_use_plus_one(name):
    assert COUNTRY_DIAL_CODE[name] == "+1"


@pytest.mark.parametrize(
    ("number", "jurisdiction"),
    [
        ("+1 876 555 0123", "Jamaica"),
        ("+1 868 555 0123", "Trinidad and Tobago"),
        ("+502 2245 6789", "Guatemala"),
        ("+591 7123 4567", "Bolivia"),
        ("+82 10 1234 5678", "Korea (South)"),
        ("+225 27 22 12 34 56", "Cote d'Ivoire"),
    ],
)
def test_fallback_validation_accepts_well_formed_numbers(monkeypatch, number, jurisdiction):
    import geo_canon.dial_codes as dial_codes

    monkeypatch.setattr(dial_codes, "_phonenumbers", None)
    assert validate_phone_number(number, jurisdiction) is True
