"""Tests for geo_canon.timezones"""

import datetime
import sys
from types import SimpleNamespace
from unittest.mock import Mock, patch
from zoneinfo import ZoneInfoNotFoundError

import pytest

from geo_canon.exceptions import ConfigurationError, TimezoneNotFoundError
from geo_canon.timezones import (
    TIMEZONE_MAP,
    _get_zone_info,
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

    def test_invalid_configured_settings_are_not_ignored(self, settings):
        settings.GEOCANON = "invalid"
        with pytest.raises(ConfigurationError):
            get_timezone_name("Romania")

    def test_pytz_fallback_when_zoneinfo_data_is_missing(self):
        fallback = Mock()
        with (
            patch("geo_canon.timezones.ZoneInfo", side_effect=ZoneInfoNotFoundError),
            patch("geo_canon.timezones._get_pytz_timezone", return_value=fallback) as pytz,
        ):
            assert _get_zone_info("Europe/Bucharest") is fallback
            pytz.assert_called_once_with("Europe/Bucharest")

    def test_pytz_database_is_used_without_system_zoneinfo_data(self, monkeypatch):
        fallback = datetime.timezone.utc
        timezone = Mock(return_value=fallback)
        monkeypatch.setitem(sys.modules, "pytz", SimpleNamespace(timezone=timezone))
        with patch("geo_canon.timezones.ZoneInfo", side_effect=ZoneInfoNotFoundError):
            assert _get_zone_info("Europe/Bucharest") is fallback
        timezone.assert_called_once_with("Europe/Bucharest")

    def test_missing_optional_database_has_an_actionable_error(self, monkeypatch):
        monkeypatch.setitem(sys.modules, "pytz", None)
        with (
            patch("geo_canon.timezones.ZoneInfo", side_effect=ZoneInfoNotFoundError),
            pytest.raises(ImportError, match=r"Install tzdata or GeoCanon\[timezones\]"),
        ):
            _get_zone_info("Europe/Bucharest")
