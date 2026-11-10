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
| `JURISDICTION_CURRENCY` | `dict[str, CurrencyInfo]` | Jurisdiction name → currency info (200+ entries, including legacy names) |
| `CURRENCY_BY_CODE` | `dict[str, CurrencyInfo]` | ISO 4217 code → currency info (deduplicated), including the [withdrawn](#withdrawn-currencies) BGN, ZWL, and ANG |
| `CURRENCY_CHOICES` | `list[tuple[str, str]]` | Sorted choices for Django ChoiceField, currencies in use only |

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

Reverse lookup by ISO 4217 code (case-insensitive). Withdrawn codes still
resolve (see [Withdrawn Currencies](#withdrawn-currencies)):

```python
from geo_canon.currencies import get_currency_by_code

info = get_currency_by_code("EUR")
info.symbol  # "€"
```

### `get_currency_choices() → list[tuple[str, str]]`

Returns deduplicated, sorted choices for Django form fields, for the currencies
in use only:

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

## Withdrawn Currencies

Three jurisdictions have replaced their currencies. Jurisdiction lookups return
the new currency, and `CURRENCY_CHOICES` and `get_currency_choices()` offer only
currencies in use. `CURRENCY_BY_CODE` and `get_currency_by_code()` still
resolve the withdrawn codes, with their old names, symbols, and decimal places,
so stored amounts can be shown in the currency they were recorded in.

| Withdrawn | Jurisdiction | Replaced by | Since | Conversion |
|-----------|--------------|-------------|-------|------------|
| `BGN` Bulgarian Lev (лв) | Bulgaria | `EUR` Euro (€) | 2026-01-01 | 1.95583 BGN = 1 EUR ([ECB](https://www.ecb.europa.eu/press/pr/date/2025/html/ecb.pr250708~b9676a9fa8.en.html)) |
| `ZWL` Zimbabwean Dollar (Z$) | Zimbabwe | `ZWG` Zimbabwe Gold (ZiG) | April 2024 | 2,498.7242 ZWL = 1 ZWG, for balances as at 2024-04-05 ([RBZ](https://www.rbz.co.zw/documents/weekly_review/2024/April/WEEKLY_ECONOMIC_HIGHLIGHTS_5_APRIL_2024_Volume_26_Number_14.pdf)) |
| `ANG` Netherlands Antillean Guilder (ƒ) | Curaçao | `XCG` Caribbean Guilder (Cg) | 2025-03-31 | 1 ANG = 1 XCG ([CBCS](https://caribbean-guilder.com/faq)) |

```python
from geo_canon.currencies import get_currency_by_code, get_currency_code

get_currency_code("Bulgaria")       # "EUR"
get_currency_by_code("BGN").symbol  # "лв"
```

A Django model field whose choices come from `CURRENCY_CHOICES` needs a new
migration now that these codes have left the choices, and validation (a
ModelForm, the admin, or `full_clean()`) rejects a stored `BGN`, `ZWL`, or
`ANG`. Convert stored amounts at the rates above, or add the old codes to the
field's own choices.

## Locale-Aware Formatting

Install `GeoCanon[locale]` to format currencies with Babel/CLDR conventions:

```bash
pip install "GeoCanon[locale]"
```

```python
from geo_canon import format_currency_locale

format_currency_locale(1234.5, "United States")
# "$1,234.50"
```

See [Locale Formatting](locale-formats.md) for number, date, time, percent,
and list formatting helpers.

## Notes

- All currency names use `gettext_lazy` for i18n support
- `CURRENCY_CHOICES` is deduplicated (EUR appears once, not 20+ times) and
  leaves out withdrawn currencies
- The module supports `Decimal`, `float`, and `int` inputs
- Unknown jurisdictions produce a plain `{amount:,.2f}` fallback
