"""Tests for geo_canon.jurisdictions"""

from geo_canon.jurisdictions import (
    JURISDICTION_NAMES,
    JURISDICTIONS,
    get_jurisdiction_choices,
    is_valid_jurisdiction,
)


class TestJurisdictions:
    def test_jurisdictions_is_sorted(self):
        names = [j[0] for j in JURISDICTIONS]
        assert names == sorted(names)

    def test_jurisdictions_not_empty(self):
        assert len(JURISDICTIONS) > 150

    def test_common_countries_present(self):
        for country in [
            "United States",
            "United Kingdom",
            "Germany",
            "France",
            "Japan",
            "Romania",
            "India",
            "Brazil",
            "Australia",
        ]:
            assert country in JURISDICTION_NAMES, f"{country} missing from jurisdictions"

    def test_is_valid_jurisdiction_true(self):
        assert is_valid_jurisdiction("Romania") is True

    def test_is_valid_jurisdiction_false(self):
        assert is_valid_jurisdiction("Narnia") is False

    def test_get_jurisdiction_choices_returns_list_of_tuples(self):
        choices = get_jurisdiction_choices()
        assert isinstance(choices, list)
        assert all(isinstance(c, tuple) and len(c) == 2 for c in choices)

    def test_each_jurisdiction_has_string_key(self):
        for key, _label in JURISDICTIONS:
            assert isinstance(key, str)
            assert len(key) > 0
