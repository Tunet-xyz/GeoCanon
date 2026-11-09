"""Tests for geo_canon.exceptions"""

from geo_canon.exceptions import (
    ConfigurationError,
    DialCodeNotFoundError,
    GeoCanonError,
    HolidaysNotAvailableError,
    JurisdictionNotFoundError,
    PhoneValidationError,
    TimezoneNotFoundError,
)


class TestExceptions:
    def test_base_error(self):
        err = GeoCanonError("Something went wrong", hint="Try again")
        assert "Something went wrong" in str(err)
        assert "Try again" in str(err)
        assert err.hint == "Try again"

    def test_configuration_error(self):
        err = ConfigurationError("Bad config")
        assert isinstance(err, GeoCanonError)

    def test_jurisdiction_not_found(self):
        err = JurisdictionNotFoundError("Narnia", available=["Romania", "France"])
        assert "Narnia" in str(err)
        assert err.hint is not None

    def test_timezone_not_found(self):
        err = TimezoneNotFoundError("Narnia")
        assert "Narnia" in str(err)

    def test_holidays_not_available(self):
        err = HolidaysNotAvailableError()
        assert "holidays" in str(err).lower()

    def test_dial_code_not_found(self):
        err = DialCodeNotFoundError("+999")
        assert "+999" in str(err)

    def test_phone_validation_error_does_not_repeat_the_number(self):
        err = PhoneValidationError("+44 7123 456789", "+44", r"^\d{10}$")
        message = str(err)
        assert "7123" not in message and "456789" not in message
        assert "ending in 89" in message
        assert "+44" in message
        assert "123" not in str(PhoneValidationError("123", "+44", r"^\d{10}$"))

    def test_caller_values_are_escaped_and_bounded(self):
        multiline = str(JurisdictionNotFoundError("Narnia\nERROR forged log line"))
        assert "Narnia\nERROR" not in multiline
        assert "Narnia\\nERROR" in multiline
        assert len(str(TimezoneNotFoundError("x" * 100_000))) < 500
        assert len(str(DialCodeNotFoundError("+" + "9" * 100_000))) < 500

    def test_holidays_hint_uses_the_published_package_name(self):
        assert 'pip install "GeoCanon[holidays]"' in str(HolidaysNotAvailableError())

    def test_lookups_return_none_instead_of_raising(self):
        from geo_canon import get_dial_code, is_valid_jurisdiction, validate_phone

        assert get_dial_code("Narnia") is None
        assert is_valid_jurisdiction("Narnia") is False
        assert validate_phone("123", "+999") is False
