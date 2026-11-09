"""Tests for geo_canon.holidays (requires holidays extra)."""

import datetime
import importlib.util

import pytest

HAS_HOLIDAYS = importlib.util.find_spec("holidays") is not None

pytestmark = pytest.mark.skipif(not HAS_HOLIDAYS, reason="holidays package not installed")


class TestHolidays:
    def test_christmas_is_public_holiday(self):
        from geo_canon.holidays import is_public_holiday

        assert is_public_holiday("Romania", datetime.date(2025, 12, 25)) is True

    def test_regular_day_not_holiday(self):
        from geo_canon.holidays import is_public_holiday

        # Feb 15 is generally not a holiday
        assert is_public_holiday("Romania", datetime.date(2025, 2, 15)) is False

    def test_unknown_jurisdiction_returns_false(self):
        from geo_canon.holidays import is_public_holiday

        assert is_public_holiday("Narnia", datetime.date(2025, 12, 25)) is False

    def test_get_holidays_for_year(self):
        from geo_canon.holidays import get_holidays_for_year

        hols = get_holidays_for_year("United States", 2025)
        assert isinstance(hols, dict)
        assert len(hols) > 5

    def test_get_holidays_unknown_jurisdiction(self):
        from geo_canon.holidays import get_holidays_for_year

        assert get_holidays_for_year("Narnia", 2025) == {}

    def test_supported_jurisdictions(self):
        from geo_canon.holidays import get_supported_holiday_jurisdictions

        jurisdictions = get_supported_holiday_jurisdictions()
        assert isinstance(jurisdictions, list)
        assert "Romania" in jurisdictions
        assert "United States" in jurisdictions


class TestHolidayRegistry:
    def test_registry_follows_the_iso_registry(self):
        import holidays

        from geo_canon.holidays import _get_registry
        from geo_canon.iso_codes import JURISDICTION_ISO

        registry = _get_registry()
        supported = holidays.list_supported_countries()
        for name, info in JURISDICTION_ISO.items():
            if info.alpha_2 in supported:
                assert registry[name] is getattr(holidays, info.alpha_2), name
            else:
                assert name not in registry, name

    def test_canonical_names_and_legacy_aliases_share_a_calendar(self):
        from geo_canon.holidays import get_holidays_for_year, is_public_holiday

        new_year = datetime.date(2025, 1, 1)
        for canonical, alias in [
            ("Korea (South)", "South Korea"),
            ("Congo (Congo-Brazzaville)", "Congo"),
        ]:
            assert is_public_holiday(canonical, new_year) is True, canonical
            assert get_holidays_for_year(canonical, 2025) == get_holidays_for_year(alias, 2025)

    def test_floor_release_covers_the_documented_calendars(self):
        from geo_canon.holidays import get_supported_holiday_jurisdictions, is_public_holiday

        # holidays 0.66 is the first release with Afghanistan and Sri Lanka.
        supported = set(get_supported_holiday_jurisdictions())
        assert {"Afghanistan", "Sri Lanka", "United Kingdom", "Korea (South)"} <= supported
        assert is_public_holiday("United Kingdom", datetime.date(2025, 12, 25)) is True

    def test_countries_missing_from_the_installed_release_are_skipped(self, monkeypatch):
        import types

        import holidays

        import geo_canon.holidays as geo_holidays

        stub = types.SimpleNamespace(RO=holidays.RO, list_supported_countries=lambda: {"RO": []})
        monkeypatch.setattr(geo_holidays, "_holidays_lib", stub)
        monkeypatch.setattr(geo_holidays, "_registry", None)
        assert geo_holidays.get_supported_holiday_jurisdictions() == ["Romania"]
        assert geo_holidays.is_public_holiday("Afghanistan", datetime.date(2025, 1, 1)) is False
