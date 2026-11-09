# Duration formatting

i18n-aware, human-readable duration formatting.

## Function

### `format_duration(total_seconds: int) -> str`

Formats seconds into hours, minutes, and seconds using Django's `ngettext` for proper pluralisation in the active language.

```python
from geo_canon import format_duration

format_duration(0)     # "0 seconds"
format_duration(1)     # "1 second"
format_duration(90)    # "1 minute, 30 seconds"
format_duration(3661)  # "1 hour, 1 minute, 1 second"
format_duration(7200)  # "2 hours"
```
