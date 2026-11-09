# Locale formatting

Optional Babel-backed formatting helpers for numbers, currencies, dates, times,
datetimes, percentages, and lists.

Install the extra:

```bash
pip install "GeoCanon[locale]"
```

GeoCanon still imports without Babel installed. When Babel is missing or a
locale cannot be resolved, these helpers return simple fallback strings.

## Locale Resolution

### `get_locale_for_jurisdiction(jurisdiction, *, language=None) -> str | None`

Builds a likely Babel locale from GeoCanon's language and ISO country mappings.

```python
from geo_canon import get_locale_for_jurisdiction

get_locale_for_jurisdiction("Romania")        # "ro_RO"
get_locale_for_jurisdiction("United States")  # "en_US"
get_locale_for_jurisdiction("Switzerland", language="fr")  # "fr_CH"
```

### `is_locale_extra_available() -> bool`

Returns whether Babel is installed.

## Numbers

```python
from geo_canon import format_decimal_locale, format_percent_locale

format_decimal_locale(1234.5, "United States")
# "1,234.5"

format_percent_locale(0.125, "United States")
# "12%"
```

## Currencies

```python
from geo_canon import format_currency_locale

format_currency_locale(1234.5, "United States")
# "$1,234.50"

format_currency_locale(1234.5, "Germany")
# "1.234,50\xa0€" with Babel; "€1,234.50" without it
```

Pass `currency_code` to format a different currency in the jurisdiction's
locale. The override needs the `locale` extra and a locale Babel can resolve:

```python
format_currency_locale(1234.5, "United States", currency_code="EUR")
```

## Dates And Times

```python
from datetime import date, datetime, time
from geo_canon import format_date_locale, format_datetime_locale, format_time_locale

format_date_locale(date(2025, 12, 25), "United States")
format_time_locale(time(14, 30), "United States")
format_datetime_locale(datetime(2025, 12, 25, 14, 30), "United States")
```

Each helper accepts a Babel format name:

```python
format_date_locale(date(2025, 12, 25), "United States", date_format="long")
format_time_locale(time(14, 30), "United States", time_format="short")
format_datetime_locale(
    datetime(2025, 12, 25, 14, 30),
    "United States",
    datetime_format="full",
)
```

## Lists

```python
from geo_canon import format_list_locale

format_list_locale(["red", "blue", "green"], "United States")
# "red, blue, and green" with Babel; "red, blue and green" without it
```
