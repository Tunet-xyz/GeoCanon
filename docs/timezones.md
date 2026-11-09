# Timezones

Jurisdiction → IANA timezone mapping with 190+ built-in entries.

Uses Python's `zoneinfo` module (3.9+) by default, with `pytz` fallback available via `pip install "GeoCanon[timezones]"`.

The fallback is used when the IANA timezone data is unavailable. Install
`tzdata` or the `timezones` extra in stripped-down environments. Override zone
names are not checked: `get_timezone_name` returns them unchanged, and an
invalid name raises when `get_timezone_for_jurisdiction` or
`get_current_local_time` uses it, without falling back to the built-in mapping
(`ZoneInfoNotFoundError` when `pytz` is not installed).

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
