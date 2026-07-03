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

    def test_phone_validation_error(self):
        err = PhoneValidationError("123", "+44", r"^\d{10}$")
        assert "123" in str(err)
        assert "+44" in str(err)
