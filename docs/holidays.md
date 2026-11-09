# Public holidays

Detect public holidays for 140+ countries. Requires the `holidays` extra:

```bash
pip install "GeoCanon[holidays]"
```

## Functions

### `is_public_holiday(jurisdiction, date=None, *, year=None) -> bool`
```python
from geo_canon.holidays import is_public_holiday
import datetime

is_public_holiday("Romania", datetime.date(2025, 12, 25))  # True
is_public_holiday("Romania", datetime.date(2025, 2, 15))   # False
```

### `get_holidays_for_year(jurisdiction, year=None) -> dict[date, str]`
```python
from geo_canon.holidays import get_holidays_for_year

holidays = get_holidays_for_year("United States", 2025)
# {date(2025, 1, 1): "New Year's Day", ...}
```

### `get_supported_holiday_jurisdictions() -> list[str]`
Returns the sorted list of jurisdictions with holiday support.
