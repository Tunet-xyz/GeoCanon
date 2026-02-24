# Settings

GeoCanon works with zero configuration. Optionally customise via `GEOCANON` in your Django `settings.py`.

## Configuration

```python
from geo_canon.settings import GeoCanonSettings

GEOCANON = GeoCanonSettings(
    default_jurisdiction="United States",   # Default when none specified
    default_language="en",                  # Default ISO 639-1 code
    timezone_overrides={},                  # Extra jurisdiction → IANA timezone
    holiday_country_overrides={},           # Extra jurisdiction → ISO country code
    enable_form_widgets=True,               # Include Django form widgets
)
```

All fields have sensible defaults; you only need to set what you want to change.

## Accessing Settings

```python
from geo_canon.settings import get_geocanon_settings

settings = get_geocanon_settings()
settings.default_jurisdiction  # "United States"
```

This reads from `django.conf.settings.GEOCANON`. Accepts a `GeoCanonSettings` instance or a plain dict.
