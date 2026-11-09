"""
GeoCanon Settings Management

Provides a structured, validated, and developer-friendly way to manage
GeoCanon configuration across all modules.

Usage:
    # In your Django settings.py
    from geo_canon.settings import GeoCanonSettings

    GEOCANON = GeoCanonSettings()

    # Or customise:
    GEOCANON = GeoCanonSettings(
        default_jurisdiction="United Kingdom",
        default_language="en",
        timezone_overrides={"My Custom Region": "Europe/London"},
    )
"""

from __future__ import annotations

try:
    from pydantic import BaseModel, Field
except ImportError:
    # Graceful fallback - settings work as a plain dataclass when pydantic is absent
    BaseModel = None  # type: ignore[assignment, misc]

from .exceptions import ConfigurationError

if BaseModel is not None:

    class GeoCanonSettings(BaseModel):
        """
        Validated GeoCanon configuration.

        Attach as ``GEOCANON`` in your Django ``settings.py``.
        """

        default_jurisdiction: str = Field(
            default="United States",
            description="Default jurisdiction used when none is specified",
        )
        default_language: str = Field(
            default="en",
            description="Default ISO-639-1 language code",
        )
        timezone_overrides: dict[str, str] = Field(
            default_factory=dict,
            description=(
                "Extra jurisdiction → IANA timezone mappings that extend or override the built-in map"
            ),
        )
        holiday_country_overrides: dict[str, str] = Field(
            default_factory=dict,
            description=(
                "Extra jurisdiction name → ISO-3166 country code overrides for the holidays library"
            ),
        )
        enable_form_widgets: bool = Field(
            default=True,
            description="Include Django form widgets and fields",
        )

        model_config = {"frozen": False, "extra": "forbid"}

else:
    # Lightweight fallback without pydantic
    class GeoCanonSettings:  # type: ignore[no-redef]
        """Lightweight settings container (pydantic not installed)."""

        def __init__(
            self,
            *,
            default_jurisdiction: str = "United States",
            default_language: str = "en",
            timezone_overrides: dict[str, str] | None = None,
            holiday_country_overrides: dict[str, str] | None = None,
            enable_form_widgets: bool = True,
        ):
            self.default_jurisdiction = default_jurisdiction
            self.default_language = default_language
            self.timezone_overrides = timezone_overrides or {}
            self.holiday_country_overrides = holiday_country_overrides or {}
            self.enable_form_widgets = enable_form_widgets


def get_geocanon_settings() -> GeoCanonSettings:
    """
    Retrieve the ``GEOCANON`` settings object from Django settings.

    Falls back to defaults if ``GEOCANON`` is not defined.
    """
    try:
        from django.conf import settings as django_settings
    except ImportError as exc:
        raise ConfigurationError(
            "Django is required to use GeoCanon.",
            hint='pip install "Django>=4.2,<7"',
        ) from exc

    geocanon = getattr(django_settings, "GEOCANON", None)

    if geocanon is None:
        return GeoCanonSettings()

    if isinstance(geocanon, GeoCanonSettings):
        return geocanon

    if isinstance(geocanon, dict):
        return GeoCanonSettings(**geocanon)

    raise ConfigurationError(
        f"GEOCANON must be a GeoCanonSettings instance or dict, got {type(geocanon).__name__}",
        hint="Use: GEOCANON = GeoCanonSettings(...) in your settings.py",
    )
