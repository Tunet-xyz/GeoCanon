"""Tests for geo_canon.holidays (requires holidays extra)."""

import datetime

import pytest

try:
    import holidays as _holidays_lib
    HAS_HOLIDAYS = True
except ImportError:
    HAS_HOLIDAYS = False

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
