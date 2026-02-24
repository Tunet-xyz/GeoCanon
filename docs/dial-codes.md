# Dial Codes

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
Validates that the national number matches the expected pattern for the dial code.

```python
validate_phone("7123456789", "+44")  # True (UK: 10 digits)
validate_phone("123", "+44")         # False
```
