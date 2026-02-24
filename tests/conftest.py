"""
Pytest configuration for GeoCanon tests.

Configures a minimal Django environment before running tests.
"""

import django
from django.conf import settings


def pytest_configure():
    """Configure Django settings for tests."""
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                }
            },
            INSTALLED_APPS=[
                "django.contrib.contenttypes",
                "django.contrib.auth",
            ],
            MIDDLEWARE=[],
            USE_TZ=True,
            SECRET_KEY="test-secret-key-for-geocanon-tests-only",
            # GeoCanon settings (test defaults)
            GEOCANON={
                "default_jurisdiction": "United Kingdom",
                "default_language": "en",
                "timezone_overrides": {
                    "Test Region": "Europe/London",
                },
            },
        )
        django.setup()
