# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Phones extra** - optional `phonenumbers` integration for robust phone validation, E.164/international/national formatting, and number type detection
- **Locale extra** - optional Babel-backed formatting for decimals, percentages, currencies, dates, times, datetimes, and lists

## [0.4.0] - 2026-02-25

### Added

- **ISO Country Codes** - ISO 3166-1 alpha-2, alpha-3, and numeric code mapping (190+ entries) with reverse lookups (`get_jurisdiction_by_alpha2`, `get_jurisdiction_by_alpha3`)

### Changed

- **Flags** - Refactored to derive `FLAG_CSS_CLASS` from the new `iso_codes` module instead of maintaining a duplicate mapping. All public API unchanged.

## [0.3.0] - 2026-02-25

### Added

- **Address Formats** - Jurisdiction → postal address format mapping (170+ entries), postal-code validation, localised field labels (`get_state_label`, `get_postal_code_label`), and `format_address()` helper

## [0.2.0] - 2026-02-25

### Added

- **Currencies** - Jurisdiction → ISO 4217 currency mapping (170+ entries), symbols, `format_currency()` with correct decimal places, and Django form choices

## [0.1.0] - 2026-02-24

### Added

- **Jurisdictions** - 190+ country registry with translatable names, Django form integration, and context-switching middleware
- **Dial Codes** - International dial code choices for Django forms with per-country phone number validation
- **Flags** - Country-to-ISO-3166 flag CSS class mapping for 190+ countries
- **Timezones** - Jurisdiction-aware local time with 200+ timezone mappings (IANA database)
- **Public Holidays** - Holiday detection for 140+ countries via the `holidays` library
- **Languages** - Language code choices for Django forms with jurisdiction-to-language mapping
- **Duration** - i18n-aware human-readable duration formatting
- **Settings** - Pydantic-validated `GeoCanonSettings` for type-safe configuration
- **Exceptions** - Rich, actionable error messages with hints and documentation links
- Full test suite with 80%+ coverage target
- PEP 561 `py.typed` marker for type checker support
