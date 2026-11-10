# Dial codes

International dialling codes with per-country phone number validation.

## Data

```python
from geo_canon.dial_codes import DIAL_CODE_CHOICES, COUNTRY_DIAL_CODE, PHONE_PATTERNS
```

- `DIAL_CODE_CHOICES` — list of `("+XX", "Country (+XX)")` tuples for forms
- `COUNTRY_DIAL_CODE` — dict mapping country name → dial code
- `PHONE_PATTERNS` — dict mapping dial code → compiled regex for the national
  number, without its trunk prefix

## Functions

### `get_dial_code(country: str) -> str | None`
```python
get_dial_code("Romania")  # "+40"
get_dial_code("Unknown")  # None
```

### `get_dial_code_choices() -> list[tuple[str, str]]`
Returns `DIAL_CODE_CHOICES` — suitable for a Django `ChoiceField`.

### `validate_phone(phone: str, dial_code: str) -> bool`
Validates that the whole national number matches the pattern for the dial code.
Only ASCII digits pass: a trailing newline or full-width digits fail.

Pass the number without the trunk prefix dialled inside the country, such as
the UK's leading 0 or Russia's 8. A leading 0 passes only where it is part of
the number: Italy and Vatican City (`+39`), Côte d'Ivoire (`+225`), Burkina
Faso (`+226`), Benin (`+229`), Gabon (`+241`), Congo (`+242`), San Marino
(`+378`), and Tajikistan (`+992`).

```python
validate_phone("7123456789", "+44")   # True (UK: 10 digits)
validate_phone("07123456789", "+44")  # False (drop the trunk prefix 0)
validate_phone("123", "+44")          # False
```

## Optional `phones` Extra

Install `GeoCanon[phones]` to enable robust parsing and formatting via
`phonenumbers`:

```bash
pip install "GeoCanon[phones]"
```

### `validate_phone_number(phone, jurisdiction=None, *, region=None) -> bool`

Validates national or international phone numbers. `jurisdiction` is converted
to an ISO-3166 alpha-2 region code automatically.

```python
from geo_canon import validate_phone_number

validate_phone_number("6502530000", "United States")  # True
validate_phone_number("+1 650-253-0000")              # True with [phones]; False without it
```

When `phonenumbers` is not installed, this falls back to GeoCanon's lightweight
regex validation for known jurisdictions. It drops the country code after a `+`
and the country's trunk prefix, if it has one, then checks the rest with
`validate_phone`. The trunk prefixes come from libphonenumber: 0 in most
countries, 1 in the `+1` countries and the Marshall Islands, 8 in Russia,
Kazakhstan, and Turkmenistan, 06 in Hungary, 0 or 8 in Lithuania, and 0, 80,
or 8 in Belarus. A 1 or an 8 is dropped only when the digits after it form a
valid number, so Russian area codes that start with 8 are kept.

```python
validate_phone_number("8 (912) 345-67-89", "Russia")  # True, with or without the extra
```

The fallback patterns are approximations, mostly digit counts, and reject some
real numbers, such as many German, Swedish, and Japanese fixed lines. Install
the `phones` extra when validity matters.

### `format_phone_number(phone, jurisdiction=None, *, region=None, phone_format="E164") -> str | None`

Formats a parsed phone number. Supported formats are `E164`, `INTERNATIONAL`,
`NATIONAL`, and `RFC3966`. It needs the `phones` extra and returns `None`
without it.

```python
from geo_canon import format_phone_number

format_phone_number("6502530000", "United States")
# "+16502530000"

format_phone_number("6502530000", "United States", phone_format="INTERNATIONAL")
# "+1 650-253-0000"
```

### `get_phone_number_type(phone, jurisdiction=None, *, region=None) -> str | None`

Returns types such as `mobile`, `fixed_line`, `fixed_line_or_mobile`, `voip`,
or `unknown`. It needs the `phones` extra and returns `None` without it.

### `is_phone_extra_available() -> bool`

Returns whether `phonenumbers` is installed.
