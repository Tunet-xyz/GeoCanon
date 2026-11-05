# Timezones

Jurisdiction → IANA timezone mapping with 200+ built-in entries.

Uses Python's `zoneinfo` module (3.9+) by default, with `pytz` fallback available via `pip install geocanon[timezones]`.

The fallback is used when the IANA timezone data is unavailable. Install
`tzdata` or the `timezones` extra in stripped-down environments. Invalid
configured overrides raise an error instead of falling back silently.

## Functions

### `get_timezone_name(jurisdiction: str) -> str`
Returns the IANA timezone string. Checks `GEOCANON.timezone_overrides` first.
```python
get_timezone_name("Romania")  # "Europe/Bucharest"
```

### `get_current_local_time(jurisdiction: str) -> datetime`
Returns an aware datetime in the jurisdiction's timezone.
```python
get_current_local_time("Japan")  # datetime in Asia/Tokyo
```

### `get_timezone_for_jurisdiction(jurisdiction: str) -> ZoneInfo | pytz.timezone`
Returns the timezone object directly.

## Extending

Add custom timezone mappings in your settings:
```python
GEOCANON = GeoCanonSettings(
    timezone_overrides={
        "My Region": "Europe/London",
    }
)
```
