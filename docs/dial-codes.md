# Dial codes

International dialling codes with per-country phone number validation.

## Data

```python
from geo_canon.dial_codes import DIAL_CODE_CHOICES, COUNTRY_DIAL_CODE, PHONE_PATTERNS
```

- `DIAL_CODE_CHOICES` — list of `("+XX", "Country (+XX)")` tuples for forms
- `COUNTRY_DIAL_CODE` — dict mapping country name → dial code
- `PHONE_PATTERNS` — dict mapping dial code → compiled regex for national digits

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

```python
validate_phone("7123456789", "+44")  # True (UK: 10 digits)
validate_phone("123", "+44")         # False
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
regex validation for known jurisdictions.

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
