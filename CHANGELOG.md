# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
