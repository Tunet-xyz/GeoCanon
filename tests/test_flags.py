"""Tests for geo_canon.flags"""

from geo_canon.flags import (
    FLAG_CSS_CLASS,
    annotate_flag_class,
    get_country_by_iso,
    get_flag_css_class,
)


class TestFlags:
    def test_flag_class_romania(self):
        assert get_flag_css_class("Romania") == "fi-ro"

    def test_flag_class_uk(self):
        assert get_flag_css_class("United Kingdom") == "fi-gb"

    def test_flag_class_us(self):
        assert get_flag_css_class("United States") == "fi-us"

    def test_flag_class_unknown_returns_default(self):
        assert get_flag_css_class("Narnia") == "fi-un"

    def test_flag_class_custom_default(self):
        assert get_flag_css_class("Narnia", default="fi-xx") == "fi-xx"

    def test_flag_css_class_dict_not_empty(self):
        assert len(FLAG_CSS_CLASS) > 150

    def test_get_country_by_iso(self):
        assert get_country_by_iso("ro") == "Romania"
        assert get_country_by_iso("RO") == "Romania"

    def test_get_country_by_iso_unknown(self):
        assert get_country_by_iso("zz") is None


class TestAnnotateFlagClass:
    def test_annotate_adds_flag_class_key(self):
        records = [{"jurisdiction": "Romania"}, {"jurisdiction": "Germany"}]
        result = annotate_flag_class(records)
        assert result[0]["flag_class"] == "fi-ro"
        assert result[1]["flag_class"] == "fi-de"

    def test_annotate_unknown_uses_default(self):
        records = [{"jurisdiction": "Unknown"}]
        result = annotate_flag_class(records)
        assert result[0]["flag_class"] == "fi-un"

    def test_annotate_custom_keys(self):
        records = [{"country": "Japan"}]
        result = annotate_flag_class(records, jurisdiction_key="country", flag_key="icon")
        assert result[0]["icon"] == "fi-jp"
