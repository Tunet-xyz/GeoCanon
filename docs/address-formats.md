# Address Formats

Jurisdiction → postal address format mapping, postal-code validation, localised field labels, and address formatting.

## Data Structures

### `AddressFormat`

A `NamedTuple` with six fields:

| Field | Type | Example (US) |
|-------|------|-------------|
| `template` | `str` | `"{address1}\n{address2}\n{city}, {state} {postal_code}\n{country}"` |
| `state_label` | `str` | `"State"` (translatable) |
| `postal_code_label` | `str` | `"ZIP Code"` (translatable) |
| `state_required` | `bool` | `True` |
| `postal_code_pattern` | `str` | `r"^\d{5}(-\d{4})?$"` |
| `postal_code_example` | `str` | `"10001"` |

### Registry

| Registry | Type | Description |
|----------|------|-------------|
| `JURISDICTION_ADDRESS_FORMAT` | `dict[str, AddressFormat]` | Jurisdiction name → format (170+ entries) |

## API Reference

### `get_address_format(jurisdiction) → AddressFormat | None`

```python
from geo_canon.address_formats import get_address_format

fmt = get_address_format("United States")
fmt.state_label       # "State"
fmt.postal_code_label # "ZIP Code"
fmt.state_required    # True
```

### `validate_postal_code(jurisdiction, postal_code) → bool`

```python
from geo_canon.address_formats import validate_postal_code

validate_postal_code("United States", "10001")       # True
validate_postal_code("United States", "10001-1234")   # True
validate_postal_code("United States", "ABCDE")        # False
validate_postal_code("Hong Kong", "")                 # True (no postal system)
```

### `get_postal_code_regex(jurisdiction) → str | None`

```python
from geo_canon.address_formats import get_postal_code_regex

get_postal_code_regex("United States")  # r"^\d{5}(-\d{4})?$"
get_postal_code_regex("Hong Kong")      # "" (no postal system)
get_postal_code_regex("Narnia")         # None
```

### `get_state_label(jurisdiction) → str | None`

Returns the locale-appropriate label for the state/province/region field:

```python
from geo_canon.address_formats import get_state_label

get_state_label("United States")          # "State"
get_state_label("Canada")                 # "Province"
get_state_label("Japan")                  # "Prefecture"
get_state_label("United Arab Emirates")   # "Emirate"
get_state_label("Ireland")               # "County"
```

### `get_postal_code_label(jurisdiction) → str | None`

Returns the locale-appropriate label for the postal code field:

```python
from geo_canon.address_formats import get_postal_code_label

get_postal_code_label("United States")  # "ZIP Code"
get_postal_code_label("United Kingdom") # "Postcode"
get_postal_code_label("Germany")        # "PLZ"
get_postal_code_label("Brazil")         # "CEP"
get_postal_code_label("India")          # "PIN Code"
get_postal_code_label("France")         # "Code Postal"
```

### `is_state_required(jurisdiction) → bool`

```python
from geo_canon.address_formats import is_state_required

is_state_required("United States")  # True
is_state_required("Australia")      # True
is_state_required("France")         # False
```

### `format_address(jurisdiction, *, name, company, address1, address2, city, state, postal_code, country) → str`

Format address fields according to the jurisdiction's conventions. All keyword arguments are optional strings. Empty lines are collapsed automatically. No registered template includes `{name}` or `{company}`, so those two arguments are dropped; they are printed only for a jurisdiction without a registered format, where the non-empty fields are joined one per line.

```python
from geo_canon.address_formats import format_address

print(format_address(
    "United States",
    address1="123 Main St",
    city="New York",
    state="NY",
    postal_code="10001",
    country="United States",
))
# 123 Main St
# New York, NY 10001
# United States

print(format_address(
    "Japan",
    address1="1-1 Chiyoda",
    state="Tokyo",
    city="Chiyoda-ku",
    postal_code="100-0001",
))
# 〒100-0001
# TokyoChiyoda-ku
# 1-1 Chiyoda

print(format_address(
    "Germany",
    address1="Unter den Linden 1",
    city="Berlin",
    postal_code="10117",
    country="Germany",
))
# Unter den Linden 1
# 10117 Berlin
# Germany
```

## Format Templates

The module ships with jurisdiction-appropriate templates:

| Style | Used by | Order |
|-------|---------|-------|
| Default | Most countries | street → city postal_code → country |
| US | US, Philippines, Mexico | street → city, STATE ZIP → country |
| UK | United Kingdom | street → city → postcode → country |
| DE/Nordics | Germany, Austria, Scandinavia | street → PLZ city → country |
| FR | France, Spain | street → code_postal city → country |
| IT | Italy | street → CAP city province |
| JP | Japan | 〒postal → prefecture city → street |
| BR | Brazil | street → city – STATE → CEP → country |
| CN | China | country → province → city → street |
| RU | Russia | country → postal → city → street |
| KR | South Korea | province city → street → postal → country |
| IN | India | street → city → state PIN → country |
| CA/AU | Canada, Australia, NZ | street → city STATE postal → country |

## State Field Labels

The "state" field has different names worldwide — the module maps each:

| Label | Jurisdictions |
|-------|--------------|
| State | US, Australia, Brazil, India, Nigeria |
| Province | Canada, Argentina, China, Italy, Philippines |
| County | UK, Ireland, Romania, Hungary |
| Prefecture | Japan |
| Region | France, many African countries |
| Emirate | UAE |
| Canton | Switzerland, Luxembourg |
| Voivodeship | Poland |

## Notes

- All labels use `gettext_lazy` for i18n support
- `postal_code_pattern` is empty string (not `None`) when a jurisdiction has no postal code system
- `validate_postal_code` is case-insensitive
- `format_address` automatically strips empty lines
