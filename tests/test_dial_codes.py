"""Tests for geo_canon.dial_codes"""

from geo_canon.dial_codes import (
    COUNTRY_DIAL_CODE,
    DIAL_CODE_CHOICES,
    PHONE_PATTERNS,
    get_dial_code,
    get_dial_code_choices,
    validate_phone,
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
