# ISO Country Codes

Jurisdiction → ISO 3166-1 alpha-2, alpha-3, and numeric code mapping.

This module is the **single source of truth** for country-code data in GeoCanon. Other modules (e.g. [Flags](flags.md)) derive their data from it.

## Data Structures

### `ISOCountryInfo`

A `NamedTuple` with four fields:

| Field | Type | Example |
|-------|------|---------|
| `alpha_2` | `str` | `"RO"` |
| `alpha_3` | `str` | `"ROU"` |
| `numeric` | `str` | `"642"` |
| `name` | `str` | `"Romania"` (translatable) |

### Registries

| Registry | Type | Description |
|----------|------|-------------|
| `JURISDICTION_ISO` | `dict[str, ISOCountryInfo]` | Jurisdiction name → ISO info (190+ entries) |
| `ISO_ALPHA2_TO_JURISDICTION` | `dict[str, str]` | Alpha-2 code → jurisdiction name |
| `ISO_ALPHA3_TO_JURISDICTION` | `dict[str, str]` | Alpha-3 code → jurisdiction name |

## API Reference

### `get_iso_codes(jurisdiction) → ISOCountryInfo | None`

```python
from geo_canon.iso_codes import get_iso_codes

info = get_iso_codes("Romania")
info.alpha_2   # "RO"
info.alpha_3   # "ROU"
info.numeric   # "642"
```

### `get_alpha2(jurisdiction) → str | None`

```python
from geo_canon.iso_codes import get_alpha2

get_alpha2("Romania")        # "RO"
get_alpha2("United States")  # "US"
```

### `get_alpha3(jurisdiction) → str | None`

```python
from geo_canon.iso_codes import get_alpha3

get_alpha3("Romania")  # "ROU"
get_alpha3("Brazil")   # "BRA"
```

### `get_numeric_code(jurisdiction) → str | None`

```python
from geo_canon.iso_codes import get_numeric_code

get_numeric_code("Romania")        # "642"
get_numeric_code("United States")  # "840"
```

### `get_jurisdiction_by_alpha2(code) → str | None`

Reverse-lookup (case-insensitive):

```python
from geo_canon.iso_codes import get_jurisdiction_by_alpha2

get_jurisdiction_by_alpha2("RO")  # "Romania"
get_jurisdiction_by_alpha2("us")  # "United States"
```

### `get_jurisdiction_by_alpha3(code) → str | None`

```python
from geo_canon.iso_codes import get_jurisdiction_by_alpha3

get_jurisdiction_by_alpha3("ROU")  # "Romania"
get_jurisdiction_by_alpha3("usa")  # "United States"
```

## Cross-Module Integration

The `iso_codes` module feeds into other GeoCanon modules:

| Consumer | How it uses ISO codes |
|----------|---------------------|
| **Flags** | `FLAG_CSS_CLASS` is generated as `fi-{alpha_2.lower()}` |
| **Dial Codes** | Separate table keyed by jurisdiction name; not every ISO name has an entry |
| **Currencies** | Separate table keyed by jurisdiction name; not every ISO name has an entry |

```python
# Example: get everything for a single jurisdiction
from geo_canon import get_alpha2, get_flag_css_class, get_dial_code, get_currency_code

jurisdiction = "Romania"
get_alpha2(jurisdiction)          # "RO"
get_flag_css_class(jurisdiction)  # "fi-ro"  (derived from alpha-2)
get_dial_code(jurisdiction)       # "+40"
get_currency_code(jurisdiction)   # "RON"
```

## Notes

- All country names use `gettext_lazy` for i18n support
- Alpha-2 and alpha-3 codes are stored in uppercase
- Numeric codes are zero-padded to 3 digits (e.g. `"004"` for Afghanistan)
- Kosovo uses the user-assigned code `XK` / `XKX` / `983`
- Some jurisdictions share codes (e.g. "Cape Verde" and "Cabo Verde" both map to `CV`)
