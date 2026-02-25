"""Tests for geo_canon.iso_codes."""

import pytest

from geo_canon.iso_codes import (
    ISO_ALPHA2_TO_JURISDICTION,
    ISO_ALPHA3_TO_JURISDICTION,
    JURISDICTION_ISO,
    ISOCountryInfo,
    get_alpha2,
    get_alpha3,
    get_iso_codes,
    get_jurisdiction_by_alpha2,
    get_jurisdiction_by_alpha3,
    get_numeric_code,
)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class TestISORegistry:
    def test_registry_not_empty(self):
        assert len(JURISDICTION_ISO) > 150

    def test_values_are_iso_country_info(self):
        for k, v in JURISDICTION_ISO.items():
            assert isinstance(v, ISOCountryInfo), f"{k} is not ISOCountryInfo"

    def test_alpha2_always_two_chars(self):
        for k, v in JURISDICTION_ISO.items():
            assert len(v.alpha_2) == 2, f"{k} alpha_2 is '{v.alpha_2}'"

    def test_alpha3_always_three_chars(self):
        for k, v in JURISDICTION_ISO.items():
            assert len(v.alpha_3) == 3, f"{k} alpha_3 is '{v.alpha_3}'"

    def test_numeric_always_three_digits(self):
        for k, v in JURISDICTION_ISO.items():
            assert len(v.numeric) == 3, f"{k} numeric is '{v.numeric}'"
            assert v.numeric.isdigit(), f"{k} numeric '{v.numeric}' is not all digits"

    def test_alpha2_uppercase(self):
        for k, v in JURISDICTION_ISO.items():
            assert v.alpha_2 == v.alpha_2.upper(), f"{k} alpha_2 not uppercase"

    def test_alpha3_uppercase(self):
        for k, v in JURISDICTION_ISO.items():
            assert v.alpha_3 == v.alpha_3.upper(), f"{k} alpha_3 not uppercase"

    def test_reverse_alpha2_index_not_empty(self):
        assert len(ISO_ALPHA2_TO_JURISDICTION) > 100

    def test_reverse_alpha3_index_not_empty(self):
        assert len(ISO_ALPHA3_TO_JURISDICTION) > 100


# ---------------------------------------------------------------------------
# get_iso_codes
# ---------------------------------------------------------------------------


class TestGetIsoCodes:
    def test_romania(self):
        info = get_iso_codes("Romania")
        assert info is not None
        assert info.alpha_2 == "RO"
        assert info.alpha_3 == "ROU"
        assert info.numeric == "642"

    def test_united_states(self):
        info = get_iso_codes("United States")
        assert info is not None
        assert info.alpha_2 == "US"
        assert info.alpha_3 == "USA"
        assert info.numeric == "840"

    def test_united_kingdom(self):
        info = get_iso_codes("United Kingdom")
        assert info is not None
        assert info.alpha_2 == "GB"
        assert info.alpha_3 == "GBR"
        assert info.numeric == "826"

    def test_japan(self):
        info = get_iso_codes("Japan")
        assert info is not None
        assert info.alpha_2 == "JP"
        assert info.alpha_3 == "JPN"

    def test_germany(self):
        info = get_iso_codes("Germany")
        assert info is not None
        assert info.alpha_2 == "DE"
        assert info.alpha_3 == "DEU"

    def test_unknown_returns_none(self):
        assert get_iso_codes("Narnia") is None


# ---------------------------------------------------------------------------
# get_alpha2 / get_alpha3 / get_numeric_code
# ---------------------------------------------------------------------------


class TestShortcutAccessors:
    def test_get_alpha2(self):
        assert get_alpha2("Romania") == "RO"
        assert get_alpha2("France") == "FR"

    def test_get_alpha2_unknown(self):
        assert get_alpha2("Narnia") is None

    def test_get_alpha3(self):
        assert get_alpha3("Romania") == "ROU"
        assert get_alpha3("Brazil") == "BRA"

    def test_get_alpha3_unknown(self):
        assert get_alpha3("Narnia") is None

    def test_get_numeric_code(self):
        assert get_numeric_code("Romania") == "642"
        assert get_numeric_code("United States") == "840"

    def test_get_numeric_code_unknown(self):
        assert get_numeric_code("Narnia") is None


# ---------------------------------------------------------------------------
# Reverse lookups
# ---------------------------------------------------------------------------


class TestReverseLookups:
    def test_by_alpha2(self):
        assert get_jurisdiction_by_alpha2("RO") == "Romania"
        assert get_jurisdiction_by_alpha2("US") == "United States"
        assert get_jurisdiction_by_alpha2("GB") == "United Kingdom"

    def test_by_alpha2_case_insensitive(self):
        assert get_jurisdiction_by_alpha2("ro") == "Romania"
        assert get_jurisdiction_by_alpha2("us") == "United States"

    def test_by_alpha2_unknown(self):
        assert get_jurisdiction_by_alpha2("ZZ") is None

    def test_by_alpha3(self):
        assert get_jurisdiction_by_alpha3("ROU") == "Romania"
        assert get_jurisdiction_by_alpha3("USA") == "United States"
        assert get_jurisdiction_by_alpha3("GBR") == "United Kingdom"

    def test_by_alpha3_case_insensitive(self):
        assert get_jurisdiction_by_alpha3("rou") == "Romania"

    def test_by_alpha3_unknown(self):
        assert get_jurisdiction_by_alpha3("ZZZ") is None


# ---------------------------------------------------------------------------
# Cross-module consistency
# ---------------------------------------------------------------------------


class TestCrossModuleConsistency:
    def test_flags_derive_from_iso_codes(self):
        """FLAG_CSS_CLASS should be generated from JURISDICTION_ISO."""
        from geo_canon.flags import FLAG_CSS_CLASS

        for name, info in JURISDICTION_ISO.items():
            expected = f"fi-{info.alpha_2.lower()}"
            assert FLAG_CSS_CLASS.get(name) == expected, (
                f"Flag mismatch for {name}: expected {expected}, "
                f"got {FLAG_CSS_CLASS.get(name)}"
            )

    def test_get_country_by_iso_consistent(self):
        """get_country_by_iso should agree with iso_codes reverse lookup."""
        from geo_canon.flags import get_country_by_iso

        for code, name in ISO_ALPHA2_TO_JURISDICTION.items():
            flag_name = get_country_by_iso(code.lower())
            assert flag_name == name, (
                f"Mismatch for {code}: iso_codes={name}, flags={flag_name}"
            )
