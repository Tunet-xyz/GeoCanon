# Currencies

Jurisdiction → ISO 4217 currency mapping, symbols, formatting, and Django form choices.

## Data Structures

### `CurrencyInfo`

A `NamedTuple` with four fields:

| Field | Type | Example |
|-------|------|---------|
| `code` | `str` | `"RON"` |
| `name` | `str` | `"Romanian Leu"` (translatable) |
| `symbol` | `str` | `"lei"` |
| `decimal_places` | `int` | `2` |

### Registries

| Registry | Type | Description |
|----------|------|-------------|
| `JURISDICTION_CURRENCY` | `dict[str, CurrencyInfo]` | Jurisdiction name → currency info (170+ entries) |
| `CURRENCY_BY_CODE` | `dict[str, CurrencyInfo]` | ISO 4217 code → currency info (deduplicated) |
| `CURRENCY_CHOICES` | `list[tuple[str, str]]` | Sorted choices for Django ChoiceField |

## API Reference

### `get_currency_for_jurisdiction(jurisdiction) → CurrencyInfo | None`

```python
from geo_canon.currencies import get_currency_for_jurisdiction

info = get_currency_for_jurisdiction("Romania")
# CurrencyInfo(code='RON', name='Romanian Leu', symbol='lei', decimal_places=2)
```

### `get_currency_code(jurisdiction) → str | None`

```python
from geo_canon.currencies import get_currency_code

get_currency_code("Japan")  # "JPY"
get_currency_code("Narnia")  # None
```

### `get_currency_symbol(jurisdiction) → str | None`

```python
from geo_canon.currencies import get_currency_symbol

get_currency_symbol("United Kingdom")  # "£"
```

### `get_currency_by_code(code) → CurrencyInfo | None`

Reverse lookup by ISO 4217 code (case-insensitive):

```python
from geo_canon.currencies import get_currency_by_code

info = get_currency_by_code("EUR")
info.symbol  # "€"
```

### `get_currency_choices() → list[tuple[str, str]]`

Returns deduplicated, sorted choices for Django form fields:

```python
from geo_canon.currencies import get_currency_choices

class PaymentForm(forms.Form):
    currency = forms.ChoiceField(choices=get_currency_choices)
```

### `format_currency(amount, jurisdiction, *, use_symbol=True, include_code=False) → str`

Format a monetary amount with the correct symbol, code, and decimal places:

```python
from geo_canon.currencies import format_currency

format_currency(1234.50, "United Kingdom")
# "£1,234.50"

format_currency(1234.5, "Japan")
# "¥1,235"  (JPY has 0 decimal places)

format_currency(49.99, "Romania", use_symbol=False, include_code=True)
# "49.99 RON"

format_currency(100, "Bahrain")
# ".د.ب100.000"  (BHD has 3 decimal places)
```

## Decimal Places

Most currencies use **2** decimal places, but there are important exceptions:

| Decimal Places | Currencies |
|----------------|-----------|
| **0** | JPY, KRW, VND, CLP, PYG, VUV, UGX, RWF, BIF, DJF, GNF, KMF, XOF, XAF, ISK |
| **2** | USD, EUR, GBP, RON, AUD, CAD, and most others |
| **3** | BHD, KWD, OMR, TND, JOD, IQD, LYD |

The `format_currency` function automatically handles this.

## Notes

- All currency names use `gettext_lazy` for i18n support
- `CURRENCY_CHOICES` is deduplicated — EUR appears once, not 20+ times
- The module supports `Decimal`, `float`, and `int` inputs
- Unknown jurisdictions produce a plain `{amount:,.2f}` fallback
