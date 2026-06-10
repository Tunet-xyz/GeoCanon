"""Tests for the top-level geo_canon import."""

import geo_canon


class TestTopLevelImport:
    def test_version(self):
        assert geo_canon.__version__ == "0.4.0"

    def test_jurisdictions_importable(self):
        assert hasattr(geo_canon, "JURISDICTIONS")
        assert hasattr(geo_canon, "get_jurisdiction_choices")

    def test_dial_codes_importable(self):
        assert hasattr(geo_canon, "DIAL_CODE_CHOICES")
        assert hasattr(geo_canon, "get_dial_code")
        assert hasattr(geo_canon, "validate_phone")
        assert hasattr(geo_canon, "validate_phone_number")
        assert hasattr(geo_canon, "format_phone_number")

    def test_flags_importable(self):
        assert hasattr(geo_canon, "FLAG_CSS_CLASS")
        assert hasattr(geo_canon, "get_flag_css_class")

    def test_timezones_importable(self):
        assert hasattr(geo_canon, "TIMEZONE_MAP")
        assert hasattr(geo_canon, "get_current_local_time")

    def test_duration_importable(self):
        assert hasattr(geo_canon, "format_duration")

    def test_languages_importable(self):
        assert hasattr(geo_canon, "LANGUAGE_CHOICES")
        assert hasattr(geo_canon, "get_language_for_jurisdiction")

    def test_settings_importable(self):
        assert hasattr(geo_canon, "GeoCanonSettings")
        assert hasattr(geo_canon, "get_geocanon_settings")

    def test_locale_formats_importable(self):
        assert hasattr(geo_canon, "get_locale_for_jurisdiction")
        assert hasattr(geo_canon, "format_currency_locale")
        assert hasattr(geo_canon, "format_date_locale")

    def test_exceptions_importable(self):
        assert hasattr(geo_canon, "GeoCanonError")
        assert hasattr(geo_canon, "ConfigurationError")
