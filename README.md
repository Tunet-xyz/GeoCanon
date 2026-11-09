# GeoCanon

[![PyPI](https://img.shields.io/pypi/v/GeoCanon)](https://pypi.org/project/GeoCanon/)
[![Python 3.10–3.13](https://img.shields.io/badge/python-3.10%E2%80%933.13-blue)](https://pypi.org/project/GeoCanon/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/Tunet-xyz/geo_canon/blob/main/LICENSE)

**Jurisdictions, dial codes, flags, ISO codes, timezones, holidays, languages,
currencies, and address formats for Django, in one package.**

Part of the [Tunet](https://www.tunet.xyz/engineering/) open-source libraries, alongside [AccessGate](https://github.com/Tunet-xyz/access_gate), [SessionArmor](https://github.com/Tunet-xyz/session_armor), and [SwapLayer](https://github.com/Tunet-xyz/swap_layer). See the [GeoCanon product page](https://www.tunet.xyz/engineering/geo-canon/) for the public capability overview.

GeoCanon is a locale and jurisdiction toolkit for Django. Instead of
hand-maintained country lists, dial-code maps, timezone tables, and holiday
calendars scattered across a codebase, you import one consistent library and
ship internationally from your first deploy.

## Features

| Module | What it provides |
| --- | --- |
| Jurisdictions | 190+ countries with translatable names, a form field, a context-switch form, and middleware |
| ISO codes | ISO 3166-1 alpha-2, alpha-3, and numeric codes with reverse lookups |
| Dial codes | International dial codes and phone-number checks per dial code |
| Flags | Country to flag CSS class mapping for the [flag-icons](https://flagicons.lipis.dev/) library |
| Timezones | 190+ jurisdiction to IANA timezone mappings, using `zoneinfo` with a `pytz` fallback |
| Languages | ISO 639-1 language choices (70+) and a default language per jurisdiction |
| Duration | Human-readable durations that follow Django's active translation |
| Holidays | National public holidays through the `holidays` library, for every jurisdiction its installed release covers |
| Currencies | ISO 4217 currency mapping for every jurisdiction, symbols, and formatting |
| Address formats | Postal address templates, postal-code validation, and field labels for every jurisdiction |
| Locale formatting | Optional Babel-backed number, currency, date, time, and list formatting |
| Settings | A lightweight settings container, with optional Pydantic 2 validation |

- **Zero configuration:** sensible defaults; customize only what you need.
- **Minimal dependencies:** only Django is required; every extra is optional.
- **Translatable labels:** names use `gettext_lazy`, so your project's
  translations apply.
- **Typed:** type hints throughout and a PEP 561 `py.typed` marker.

## Version 1.0

The documented Python helpers, configuration, Django integration, and local MCP
entry point form the stable 1.x API. GeoCanon supports Python 3.10–3.13 and
Django 4.2–6.x (`Django<7`); use an upstream-supported Django release.

GeoCanon 1.x is not on PyPI yet; PyPI still serves 0.1.0. The `v1.0.0` tag
predates the fixes listed under Unreleased in the changelog, so until the next
release is published, install from `main`:

```bash
pip install "GeoCanon @ git+https://github.com/Tunet-xyz/geo_canon@main"
```

Upgrading from 0.1.0, the only earlier release on PyPI, keeps its public names
and adds the `phones`, `locale`, and `validation` extras. Some data and checks
are corrected: Jamaica and Trinidad and Tobago use the `+1` dial code (store
`+1` and put the area code in the number), reverse ISO lookups return the
canonical jurisdiction keys (legacy names still work), phone and postal-code
checks accept ASCII only (normalize input first), and an invalid configured
timezone override raises an error instead of being ignored. See the [changelog](https://github.com/Tunet-xyz/geo_canon/blob/main/CHANGELOG.md).

## Installation

```bash
pip install GeoCanon                   # Core: Django only
pip install "GeoCanon[holidays]"       # Public holiday detection
pip install "GeoCanon[timezones]"      # pytz fallback when system timezone data is missing
pip install "GeoCanon[phones]"         # phonenumbers parsing and formatting
pip install "GeoCanon[locale]"         # Babel locale-aware formatting
pip install "GeoCanon[validation]"     # Pydantic 2 settings validation
pip install "GeoCanon[all]"            # Everything above
```

| Extra | What it adds |
| --- | --- |
| `holidays` | Public holiday detection |
| `timezones` | `pytz` fallback when system timezone data is unavailable |
| `phones` | Robust phone parsing, validation, formatting, and number type detection |
| `locale` | Babel-backed number, currency, date, time, datetime, percent, and list formatting |
| `validation` | Pydantic 2 validation for the settings model |
| `all` | Everything above |

## Quick start

Configuration is optional:

```python
# settings.py
from geo_canon.settings import GeoCanonSettings

GEOCANON = GeoCanonSettings(
    default_jurisdiction="United Kingdom",
    timezone_overrides={"My Custom Region": "Europe/London"},
)
```

Then use the helpers anywhere:

```python
from geo_canon import (
    get_jurisdiction_choices,      # 190+ countries, sorted, translatable
    get_dial_code,                 # "Romania" → "+40"
    validate_phone,                # per-dial-code digit patterns
    get_flag_css_class,            # "Romania" → "fi-ro"
    get_current_local_time,        # "Romania" → aware datetime in Europe/Bucharest
    get_language_for_jurisdiction,  # "Romania" → "ro"
    format_duration,               # 3661 → "1 hour, 1 minute, 1 second"
    get_currency_code,             # "Romania" → "RON"
    format_currency,               # (1234.5, "Japan") → "¥1,235"
)

get_dial_code("United States")              # "+1"
get_current_local_time("Japan")             # datetime in Asia/Tokyo
get_language_for_jurisdiction("France")     # "fr"
format_duration(7200)                       # "2 hours"
format_currency(1234.50, "United Kingdom")  # "£1,234.50"

# Address-aware forms
from geo_canon import validate_postal_code, get_state_label
validate_postal_code("United Kingdom", "SW1A 1AA")  # True
get_state_label("Japan")                             # "Prefecture"

# ISO country codes
from geo_canon import get_alpha2, get_alpha3
get_alpha2("Romania")  # "RO"
get_alpha3("Romania")  # "ROU"
```

## Django integration

```python
from geo_canon.jurisdictions.forms import JurisdictionContextSwitchForm

# Drop-in jurisdiction selector
form = JurisdictionContextSwitchForm()
```

```python
# settings.py
MIDDLEWARE = [
    ...
    "geo_canon.jurisdictions.middleware.JurisdictionMiddleware",
]

# Now every request has request.jurisdiction
```

`JurisdictionMiddleware` reads the jurisdiction from the session's
`jurisdiction` key, falling back to `default_jurisdiction`; it never reads query
strings or headers. It needs Django's `SessionMiddleware` before it. Store only
validated values in that key, for example from `JurisdictionContextSwitchForm`.

## Optional extras

```python
# Holiday detection with GeoCanon[holidays]
from datetime import date
from geo_canon.holidays import is_public_holiday
is_public_holiday("Romania", date(2025, 12, 25))  # True

# Richer phone formatting with GeoCanon[phones]
from geo_canon import format_phone_number, validate_phone_number
validate_phone_number("6502530000", "United States")  # True
format_phone_number("6502530000", "United States")    # "+16502530000"

# Locale-aware formatting with GeoCanon[locale]
from geo_canon import format_currency_locale
format_currency_locale(1234.5, "United States")       # "$1,234.50"
```

## MCP server

GeoCanon includes a local stdio MCP server:

```bash
geocanon-mcp
```

From a source checkout, run `python mcp/server.py`. Its tools return guidance
for settings, forms, middleware, and locale workflows; the calling agent writes
any code, for a person to review. It runs locally under the caller's control,
makes no network connections, and needs no credentials or account. See
[mcp/README.md](https://github.com/Tunet-xyz/geo_canon/blob/main/mcp/README.md) for its methods, tools, and limits.

## Scope and limitations

Bundled mappings are maintained release data rather than a live legal or
standards feed. Every jurisdiction has a dial code, currency, address format,
language, and timezone; holiday coverage depends on the installed `holidays`
release. Review the
[data provenance and update policy](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/data-provenance.md) before using
defaults for compliance, tax, postal, or other high-stakes decisions.

Lookups for unknown jurisdictions return `None` or `False` rather than raising;
configuration and timezone errors raise exceptions with hints. Phone and
postal-code checks validate format only, not that a number or address exists.
GeoCanon has not had an independent security audit; the
[security assurance case](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/SECURITY_ASSURANCE.md) lists the evidence the
repository provides.

## Documentation

- [Documentation index](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/README.md): guides, security
  documents, and the release procedure.
- Guides: [jurisdictions](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/jurisdictions.md), [dial codes](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/dial-codes.md), [timezones](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/timezones.md), [currencies](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/currencies.md), [address formats](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/address-formats.md), [locale formatting](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/locale-formats.md), [settings](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/settings.md), [MCP server](https://github.com/Tunet-xyz/geo_canon/blob/main/mcp/README.md).
- Security: [security policy](https://github.com/Tunet-xyz/geo_canon/blob/main/SECURITY.md),
  [threat model](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/THREAT_MODEL.md),
  [security assurance](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/SECURITY_ASSURANCE.md),
  [audit scope](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/AUDIT_SCOPE.md), and
  [secure development](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/SECURE_DEVELOPMENT.md).
- [Changelog](https://github.com/Tunet-xyz/geo_canon/blob/main/CHANGELOG.md), including which versions reached PyPI.

## Development

```bash
git clone https://github.com/Tunet-xyz/geo_canon.git
cd geo_canon
python -m pip install -e ".[all,dev]"
python -m ruff check src tests
python -m mypy src/geo_canon
python -m bandit -r src
python -m pytest --cov=geo_canon --cov-branch
```

These are the checks the manual CI workflows run. The
[security assurance case](https://github.com/Tunet-xyz/geo_canon/blob/main/docs/SECURITY_ASSURANCE.md) lists the full
evidence commands, including the dependency audit.

## Contributing and releases

See [CONTRIBUTING.md](https://github.com/Tunet-xyz/geo_canon/blob/main/CONTRIBUTING.md) for the owner-reviewed contribution
process and [VERSIONING.md](https://github.com/Tunet-xyz/geo_canon/blob/main/VERSIONING.md) for the shared SemVer and
release policy. Report vulnerabilities privately as described in
[SECURITY.md](https://github.com/Tunet-xyz/geo_canon/blob/main/SECURITY.md). CI workflows run only when the owner
starts them, so include your local test results in pull requests. Everyone
taking part follows the [code of conduct](https://github.com/Tunet-xyz/geo_canon/blob/main/CODE_OF_CONDUCT.md).

## License

MIT. Copyright (c) 2026 Tunet Ltd. See [LICENSE](https://github.com/Tunet-xyz/geo_canon/blob/main/LICENSE).
