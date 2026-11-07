# Settings

GeoCanon works with zero configuration. Optionally customise via `GEOCANON` in your Django `settings.py`.

## Configuration

```python
from geo_canon.settings import GeoCanonSettings

GEOCANON = GeoCanonSettings(
    default_jurisdiction="United States",   # Default when none specified
    default_language="en",                  # Reserved: accepted, not used in 1.x
    timezone_overrides={},                  # Extra jurisdiction → IANA timezone
    holiday_country_overrides={},           # Reserved: accepted, not used in 1.x
    enable_form_widgets=True,               # Reserved: accepted, not used in 1.x
)
```

All fields have sensible defaults; you only need to set what you want to change.
`default_language`, `holiday_country_overrides` and `enable_form_widgets` are
accepted so existing settings keep validating, but GeoCanon 1.x does not use
them yet.

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
