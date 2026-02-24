"""Tests for geo_canon.duration"""

from geo_canon.duration import format_duration

import pytest


class TestFormatDuration:
    def test_zero_seconds(self):
        assert format_duration(0) == "0 seconds"

    def test_one_second(self):
        assert format_duration(1) == "1 second"

    def test_multiple_seconds(self):
        assert format_duration(45) == "45 seconds"

    def test_one_minute(self):
        assert format_duration(60) == "1 minute"

    def test_minutes_and_seconds(self):
        assert format_duration(90) == "1 minute, 30 seconds"

    def test_one_hour(self):
        assert format_duration(3600) == "1 hour"

    def test_hours_minutes_seconds(self):
        assert format_duration(3661) == "1 hour, 1 minute, 1 second"

    def test_large_value(self):
        result = format_duration(86400)
        assert "24 hours" in result

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            format_duration(-1)
