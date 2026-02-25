# Flags

Country → flag CSS class mapping, compatible with [flag-icons](https://flagicons.lipis.dev/).

The `FLAG_CSS_CLASS` dictionary is derived from the [ISO Country Codes](iso-codes.md) module — each entry is `fi-{alpha_2.lower()}`.

## Functions

### `get_flag_css_class(country: str, default: str = "fi-un") -> str`
```python
get_flag_css_class("Romania")   # "fi-ro"
get_flag_css_class("Unknown")   # "fi-un"
```

### `get_country_by_iso(iso_code: str) -> str | None`
Reverse lookup from ISO-3166-1 alpha-2 code.
```python
get_country_by_iso("ro")  # "Romania"
```

### `annotate_flag_class(records, ...)`
Bulk-annotate a list of dicts with flag classes:
```python
records = [{"jurisdiction": "Romania"}, {"jurisdiction": "Germany"}]
annotate_flag_class(records)
# [{"jurisdiction": "Romania", "flag_class": "fi-ro"}, ...]
```
