"""Tests for geo_canon.dial_codes"""

from geo_canon.dial_codes import (
    DIAL_CODE_CHOICES,
    PHONE_PATTERNS,
    format_phone_number,
    get_dial_code,
    get_dial_code_choices,
    get_phone_number_type,
    is_phone_extra_available,
    validate_phone,
    validate_phone_number,
)


class TestDialCodes:
    def test_dial_code_choices_not_empty(self):
        assert len(DIAL_CODE_CHOICES) > 100

    def test_get_dial_code_romania(self):
        assert get_dial_code("Romania") == "+40"

    def test_get_dial_code_us(self):
        assert get_dial_code("United States") == "+1"

    def test_get_dial_code_uk(self):
        assert get_dial_code("United Kingdom") == "+44"

    def test_get_dial_code_unknown(self):
        assert get_dial_code("Narnia") is None

    def test_get_dial_code_choices_returns_list(self):
        choices = get_dial_code_choices()
        assert isinstance(choices, list)
        assert all(isinstance(c, tuple) and len(c) == 2 for c in choices)


class TestPhoneValidation:
    def test_valid_uk_phone(self):
        assert validate_phone("7123456789", "+44") is True

    def test_invalid_uk_phone_too_short(self):
        assert validate_phone("712345", "+44") is False

    def test_valid_us_phone(self):
        assert validate_phone("2125551234", "+1") is True

    def test_invalid_us_phone(self):
        assert validate_phone("123", "+1") is False

    def test_valid_romania_phone(self):
        assert validate_phone("712345678", "+40") is True

    def test_unknown_dial_code(self):
        assert validate_phone("1234", "+999") is False

    def test_phone_patterns_all_compiled(self):
        import re

        for code, pattern in PHONE_PATTERNS.items():
            assert isinstance(pattern, re.Pattern), f"Pattern for {code} is not compiled"


class TestPhoneNumbersExtra:
    def test_phone_extra_available_returns_bool(self):
        assert isinstance(is_phone_extra_available(), bool)

    def test_fallback_validation_without_phonenumbers(self, monkeypatch):
        import geo_canon.dial_codes as dial_codes

        monkeypatch.setattr(dial_codes, "_phonenumbers", None)
        assert validate_phone_number("07123456789", "United Kingdom") is True
        assert validate_phone_number("123", "United Kingdom") is False

    def test_formatting_returns_none_without_phonenumbers(self, monkeypatch):
        import geo_canon.dial_codes as dial_codes

        monkeypatch.setattr(dial_codes, "_phonenumbers", None)
        assert format_phone_number("07123456789", "United Kingdom") is None
        assert get_phone_number_type("07123456789", "United Kingdom") is None

    def test_phonenumbers_formatting_when_installed(self):
        import pytest

        pytest.importorskip("phonenumbers")

        assert validate_phone_number("6502530000", "United States") is True
        assert format_phone_number("6502530000", "United States") == "+16502530000"
        assert (
            format_phone_number("6502530000", "United States", phone_format="INTERNATIONAL")
            == "+1 650-253-0000"
        )
        assert get_phone_number_type("6502530000", "United States") in {
            "fixed_line",
            "fixed_line_or_mobile",
        }
