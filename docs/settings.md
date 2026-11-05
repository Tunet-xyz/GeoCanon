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

The core installation uses a lightweight settings container. Install
`GeoCanon[validation]` (or `[all]`) for Pydantic 2 runtime type validation and
rejection of unknown fields. Do not assume runtime type coercion or validation
from the dependency-free container alone. `GEOCANON` may also be a plain dict.

Timezone lookups work before Django settings are configured. Once configured,
invalid settings raise an error; GeoCanon does not silently ignore a malformed
timezone override configuration.

## Accessing Settings

```python
from geo_canon.settings import get_geocanon_settings

settings = get_geocanon_settings()
settings.default_jurisdiction  # "United States"
```

This reads from `django.conf.settings.GEOCANON`. Accepts a `GeoCanonSettings` instance or a plain dict.
