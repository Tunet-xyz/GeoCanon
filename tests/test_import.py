"""Tests for the top-level geo_canon import."""

import geo_canon


class TestTopLevelImport:
    def test_version(self):
        assert geo_canon.__version__ == "1.0.0"

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


class TestLazyExports:
    def test_every_public_name_resolves_to_its_module_attribute(self):
        import importlib

        assert set(geo_canon.__all__) == set(geo_canon._EXPORTS) | {"__version__"}
        for name, module_name in geo_canon._EXPORTS.items():
            module = importlib.import_module(f"geo_canon.{module_name}")
            assert getattr(geo_canon, name) is getattr(module, name), name

    def test_star_import_gives_every_public_name(self):
        namespace: dict[str, object] = {}
        exec("from geo_canon import *", namespace)
        assert set(geo_canon.__all__) <= set(namespace)

    def test_submodules_are_reachable_as_attributes(self):
        for module_name in geo_canon._SUBMODULES:
            assert getattr(geo_canon, module_name).__name__ == f"geo_canon.{module_name}"

    def test_type_checking_imports_match_the_exports(self):
        import ast
        from pathlib import Path

        tree = ast.parse(Path(geo_canon.__file__).read_text(encoding="utf-8"))
        guarded = next(
            node
            for node in tree.body
            if isinstance(node, ast.If) and getattr(node.test, "id", "") == "TYPE_CHECKING"
        )
        imported = {
            alias.name: node.module
            for node in guarded.body
            if isinstance(node, ast.ImportFrom)
            for alias in node.names
        }
        assert imported == geo_canon._EXPORTS

    def test_unknown_names_raise_attribute_error(self):
        import pytest

        with pytest.raises(AttributeError):
            geo_canon.no_such_name  # noqa: B018
        assert "get_dial_code" in dir(geo_canon)
