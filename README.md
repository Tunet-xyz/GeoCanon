# GeoCanon
### Global-Ready Django Apps From Day One

**Jurisdictions. Dial Codes. Flags. ISO Codes. Timezones. Holidays. Languages. Currencies. Address Formats. One Package.**

Part of the [Tunet](https://github.com/Tunet-xyz) ecosystem — alongside [SwapLayer](https://github.com/Tunet-xyz/swap_layer) and [SessionArmor](https://github.com/Tunet-xyz/session_armor).

---

## What is GeoCanon?

GeoCanon is a **locale & jurisdiction toolkit** for Django that gives your app global awareness out of the box.

Instead of hand-rolling country lists, phone validation, timezone lookups, and holiday calendars, you import **one consistent library** and ship internationally from your first deploy.

### The Problem

```python
# Scattered across your codebase...
COUNTRIES = [("US", "United States"), ...]  # hand-maintained
DIAL_CODES = {"+1": "US", ...}             # incomplete
TIMEZONE_MAP = {"US": "America/New_York"}   # 8 entries
# No holiday detection, no flag icons, no language defaults
```

### The Solution

```python
from geo_canon import (
    get_jurisdiction_choices,      # 190+ countries, sorted, translatable
    get_dial_code,                 # "Romania" → "+40"
    validate_phone,                # per-country regex validation
    get_flag_css_class,            # "Romania" → "fi-ro"
    get_current_local_time,        # "Romania" → aware datetime in Europe/Bucharest
    get_language_for_jurisdiction,  # "Romania" → "ro"
    format_duration,               # 3661 → "1 hour, 1 minute, 1 second"
    get_currency_code,             # "Romania" → "RON"
    format_currency,               # (1234.5, "Japan") → "¥1,235"
)

# Address-aware forms
from geo_canon import validate_postal_code, get_state_label
validate_postal_code("United Kingdom", "SW1A 1AA")  # True
get_state_label("Japan")                             # "Prefecture"

# ISO country codes
from geo_canon import get_alpha2, get_alpha3
get_alpha2("Romania")  # "RO"
get_alpha3("Romania")  # "ROU"

# Optional: holiday detection
from geo_canon.holidays import is_public_holiday
is_public_holiday("Romania", date(2025, 12, 25))  # True

# Optional: richer phone formatting with geocanon[phones]
from geo_canon import format_phone_number, validate_phone_number
validate_phone_number("6502530000", "United States")  # True
format_phone_number("6502530000", "United States")    # "+16502530000"

# Optional: locale-aware formatting with geocanon[locale]
from geo_canon import format_currency_locale
format_currency_locale(1234.5, "United States")       # "$1,234.50"
```

---

## Quick Start

### 1. Install

```bash
# Core (zero non-Django dependencies)
pip install geocanon

# With optional extras
pip install geocanon[holidays]     # Public holiday detection
pip install geocanon[timezones]    # pytz fallback for Python <3.9
pip install geocanon[phones]       # phonenumbers parsing/formatting
pip install geocanon[locale]       # Babel locale-aware formatting
pip install geocanon[all]          # Everything
```

**Available extras:**
| Extra | What it adds |
|-------|-------------|
| `holidays` | Public holiday detection (140+ countries) |
| `timezones` | `pytz` fallback for legacy Python |
| `phones` | Robust phone parsing, validation, formatting, and number type detection |
| `locale` | Babel-backed number, currency, date, time, datetime, percent, and list formatting |
| `all` | Everything above |

### 2. Configure (optional)

```python
# settings.py — zero config required, but you CAN customise:
from geo_canon.settings import GeoCanonSettings

GEOCANON = GeoCanonSettings(
    default_jurisdiction="United Kingdom",
    default_language="en",
    timezone_overrides={"My Custom Region": "Europe/London"},
)
```

### 3. Use Anywhere

```python
from geo_canon import get_dial_code, get_flag_css_class, get_current_local_time

# Phone dial codes
get_dial_code("Romania")       # "+40"
get_dial_code("United States") # "+1"

# Flag CSS classes (for flag-icons library)
get_flag_css_class("Romania")  # "fi-ro"

# Current local time
get_current_local_time("Japan")  # datetime in Asia/Tokyo

# Language defaults
from geo_canon import get_language_for_jurisdiction
get_language_for_jurisdiction("France")  # "fr"

# Duration formatting (i18n-aware)
from geo_canon import format_duration
format_duration(7200)  # "2 hours"

# Currency formatting
from geo_canon import format_currency, get_currency_code
get_currency_code("Romania")                # "RON"
format_currency(1234.50, "United Kingdom")  # "£1,234.50"
format_currency(1234.5, "Japan")            # "¥1,235"
```

### 4. Django Forms

```python
from geo_canon.jurisdictions.forms import JurisdictionContextSwitchForm

# Drop-in jurisdiction selector
form = JurisdictionContextSwitchForm()
```

### 5. Middleware

```python
# settings.py
MIDDLEWARE = [
    ...
    "geo_canon.jurisdictions.middleware.JurisdictionMiddleware",
]

# Now every request has request.jurisdiction
```

---

## Modules

| Module | Status | Description |
|--------|--------|-------------|
| **Jurisdictions** | Production | 190+ countries with translatable names, forms, middleware |
| **Dial Codes** | Production | International dial codes + per-country phone validation |
| **Flags** | Production | Country → ISO-3166 flag CSS class mapping |
| **ISO Codes** | Production | ISO 3166-1 alpha-2, alpha-3, and numeric codes |
| **Timezones** | Production | 200+ jurisdiction → IANA timezone mappings |
| **Languages** | Production | Language choices + jurisdiction → default language |
| **Duration** | Production | i18n-aware human-readable duration formatting |
| **Holidays** | Production | Public holiday detection for 140+ countries |
| **Currencies** | Production | ISO 4217 currency mapping, symbols, and formatting |
| **Address Formats** | Production | Postal address formats, postal-code validation, and field labels |
| **Locale Formatting** | Production | Optional Babel-backed number, currency, date, time, and list formatting |
| **Settings** | Production | Pydantic-validated configuration |

---

## Features

- **190+ jurisdictions** — sorted, translatable, with O(1) lookups
- **ISO 3166-1 codes** — alpha-2, alpha-3, and numeric with reverse lookups
- **Phone validation** — per-country regex patterns for national number formats
- **Flag icons** — CSS class mapping compatible with [flag-icons](https://flagicons.lipis.dev/)
- **200+ timezones** — uses `zoneinfo` (3.9+) with `pytz` fallback
- **Holiday detection** — powered by the battle-tested `holidays` library
- **170+ currency mappings** — ISO 4217 codes, symbols, and locale-aware formatting
- **170+ address formats** — postal-code validation, localised field labels, and `format_address()`
- **75+ languages** — ISO 639-1 choices with jurisdiction → language mapping
- **Duration formatting** — respects Django's active translation
- **Jurisdiction middleware** — automatic `request.jurisdiction` on every request
- **Django form fields** — drop-in `JurisdictionChoiceField` and context-switch form
- **Pydantic settings** — type-safe configuration with sensible defaults
- **Rich exceptions** — actionable error messages with hints and docs links
- **Zero config** — works with defaults, customise when you need to
- **PEP 561** — `py.typed` marker for mypy/pyright

---

## Why GeoCanon?

- **One Source of Truth** — no more scattered country lists and timezone dicts
- **Production-Tested** — extracted from a live Django platform serving multiple jurisdictions
- **Translatable** — all labels use `gettext_lazy` for full i18n support
- **Minimal Dependencies** — only Django required; extras are truly optional
- **Type-Safe** — Pydantic validation, type hints throughout, PEP 561 compliant
- **Extensible** — override timezones, holiday mappings, and more via settings

---

## License

MIT — Copyright (c) 2026 Tunet Ltd. See [LICENSE](LICENSE).

---

**[→ Read Full Documentation](docs/README.md)**
