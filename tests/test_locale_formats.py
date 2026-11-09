"""Tests for geo_canon.locale_formats."""

import datetime

from geo_canon.locale_formats import (
    format_currency_locale,
    format_date_locale,
    format_datetime_locale,
    format_decimal_locale,
    format_list_locale,
    format_percent_locale,
    format_time_locale,
    get_locale_for_jurisdiction,
    is_locale_extra_available,
)


class TestLocaleResolution:
    def test_locale_for_jurisdiction(self):
        assert get_locale_for_jurisdiction("Romania") == "ro_RO"
        assert get_locale_for_jurisdiction("United States") == "en_US"

    def test_locale_language_override(self):
        assert get_locale_for_jurisdiction("Switzerland", language="fr") == "fr_CH"

    def test_unknown_jurisdiction(self):
        assert get_locale_for_jurisdiction("Narnia") is None

    def test_locale_extra_available_returns_bool(self):
        assert isinstance(is_locale_extra_available(), bool)


class TestLocaleFallbacks:
    def test_number_fallbacks_without_babel(self, monkeypatch):
        import geo_canon.locale_formats as locale_formats

        monkeypatch.setattr(locale_formats, "_babel_numbers", None)

        assert format_decimal_locale(1234.5, "United States") == "1,234.5"
        assert format_percent_locale(0.125, "United States") == "12%"
        assert format_currency_locale(1234.5, "United States") == "$1,234.50"

    def test_currency_code_override_without_babel(self, monkeypatch):
        import geo_canon.locale_formats as locale_formats

        monkeypatch.setattr(locale_formats, "_babel_numbers", None)

        assert format_currency_locale(1234.5, "United States", currency_code="EUR") == (
            "€1,234.50 EUR"
        )
        assert format_currency_locale(1234.5, "United States", currency_code="USD") == (
            "$1,234.50 USD"
        )
        assert format_currency_locale(1234.5, "Romania", currency_code="jpy") == "¥1,235 JPY"
        assert format_currency_locale(1234.5, "Narnia", currency_code="EUR") == "€1,234.50 EUR"
        assert format_currency_locale(1234.565, "Narnia", currency_code="XYZ") == (
            "1,234.57 XYZ"
        )

    def test_currency_code_override_when_babel_rejects_the_locale(self):
        import pytest

        pytest.importorskip("babel")

        assert format_currency_locale(
            1234.5, "Tajikistan", currency_code="EUR", locale="xx_XX"
        ) == "€1,234.50 EUR"

    def test_date_fallbacks_without_babel(self, monkeypatch):
        import geo_canon.locale_formats as locale_formats

        monkeypatch.setattr(locale_formats, "_babel_dates", None)

        date_value = datetime.date(2025, 12, 25)
        time_value = datetime.time(14, 30)
        datetime_value = datetime.datetime(2025, 12, 25, 14, 30)

        assert format_date_locale(date_value, "United States") == "2025-12-25"
        assert format_time_locale(time_value, "United States") == "14:30:00"
        assert format_datetime_locale(datetime_value, "United States") == "2025-12-25T14:30:00"

    def test_list_fallback_without_babel(self, monkeypatch):
        import geo_canon.locale_formats as locale_formats

        monkeypatch.setattr(locale_formats, "_babel_lists", None)

        assert format_list_locale(["red"], "United States") == "red"
        assert (
            format_list_locale(["red", "blue", "green"], "United States") == "red, blue and green"
        )


class TestBabelFormatting:
    def test_babel_number_formatting_when_installed(self):
        import pytest

        pytest.importorskip("babel")

        assert format_decimal_locale(1234.5, "United States") == "1,234.5"
        assert format_currency_locale(1234.5, "United States") == "$1,234.50"

    def test_babel_date_formatting_when_installed(self):
        import pytest

        pytest.importorskip("babel")

        result = format_date_locale(datetime.date(2025, 12, 25), "United States")
        assert "2025" in result

    def test_babel_list_formatting_when_installed(self):
        import pytest

        pytest.importorskip("babel")

        result = format_list_locale(["red", "blue", "green"], "United States")
        assert "red" in result
        assert "blue" in result
        assert "green" in result
