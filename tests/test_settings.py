"""Tests for geo_canon.settings"""

from geo_canon.settings import GeoCanonSettings, get_geocanon_settings


class TestGeoCanonSettings:
    def test_default_settings(self):
        s = GeoCanonSettings()
        assert s.default_jurisdiction == "United States"
        assert s.default_language == "en"
        assert s.timezone_overrides == {}

    def test_custom_settings(self):
        s = GeoCanonSettings(
            default_jurisdiction="Romania",
            default_language="ro",
        )
        assert s.default_jurisdiction == "Romania"
        assert s.default_language == "ro"

    def test_get_geocanon_settings_from_django(self):
        # conftest sets GEOCANON with UK as default
        settings = get_geocanon_settings()
        assert settings.default_jurisdiction == "United Kingdom"

    def test_django_hint_is_a_quoted_requirement(self, monkeypatch):
        import builtins

        import pytest

        from geo_canon.exceptions import ConfigurationError

        real_import = builtins.__import__

        def no_django_conf(name, *args, **kwargs):
            if name == "django.conf":
                raise ImportError(name)
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", no_django_conf)
        with pytest.raises(ConfigurationError) as caught:
            get_geocanon_settings()
        assert caught.value.hint == 'pip install "Django>=4.2,<7"'

    def test_timezone_overrides(self):
        settings = get_geocanon_settings()
        assert "Test Region" in settings.timezone_overrides
