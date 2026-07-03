"""Tests for geo_canon.timezones"""

import datetime

import pytest

from geo_canon.exceptions import TimezoneNotFoundError
from geo_canon.timezones import (
    TIMEZONE_MAP,
    get_current_local_time,
    get_timezone_name,
)


class TestTimezones:
    def test_timezone_map_not_empty(self):
        assert len(TIMEZONE_MAP) > 150

    def test_known_timezone_romania(self):
        assert get_timezone_name("Romania") == "Europe/Bucharest"

    def test_known_timezone_uk(self):
        assert get_timezone_name("United Kingdom") == "Europe/London"

    def test_known_timezone_japan(self):
        assert get_timezone_name("Japan") == "Asia/Tokyo"

    def test_unknown_jurisdiction_raises(self):
        with pytest.raises(TimezoneNotFoundError):
            get_timezone_name("Narnia")

    def test_override_from_settings(self):
        # The conftest sets "Test Region" → "Europe/London"
        assert get_timezone_name("Test Region") == "Europe/London"

    def test_get_current_local_time_returns_aware_datetime(self):
        dt = get_current_local_time("Romania")
        assert isinstance(dt, datetime.datetime)
        assert dt.tzinfo is not None

    def test_get_current_local_time_uk(self):
        dt = get_current_local_time("United Kingdom")
        assert isinstance(dt, datetime.datetime)
        assert dt.tzinfo is not None
