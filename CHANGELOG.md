# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- A Contributor Covenant 2.1 code of conduct, and issue templates for bug
  reports and feature requests that send vulnerability reports to private
  reporting.
- Jurisdiction key `"Cote d'Ivoire"` (shown as "Côte d'Ivoire"), for 197
  jurisdictions; choice labels sort ignoring accents.
- Every jurisdiction has a dial code, currency, address format, language, and
  timezone. The legacy names Cape Verde, Congo, Democratic Republic of Congo,
  Ivory Coast, North Korea, and South Korea are accepted everywhere and resolve
  to the same data; Aruba, Curacao, and Palestine (ISO table only) gain a dial
  code, language, and timezone.
- 18 dial-code choices (Belize, Bhutan, Bolivia, Curaçao, Guatemala, Kiribati,
  Kosovo, Marshall Islands, Micronesia, Nauru, Palau, Palestine, Samoa, Sao Tome
  and Principe, Solomon Islands, Timor-Leste, Tuvalu, Vanuatu); every choice
  has a phone pattern.
- Dzongkha (`dz`), Bhutan's default language, for 74 language choices.
- `python -m geo_canon.mcp` runs the MCP server.
- A CodeQL workflow (`codeql.yaml`) with the security-extended queries, which
  only the owner starts, and weekly Dependabot updates for pip and GitHub
  Actions dependencies, as in the other Tunet libraries.

### Changed

- The Product URL points at `www.tunet.xyz`, which serves the product page.
- Documentation: timezone and language counts match the bundled data,
  `default_language`, `holiday_country_overrides` and `enable_form_widgets`
  are marked as reserved settings that 1.x accepts but does not use, and the
  MCP and contribution notes are written for outside readers.
- The security policy uses the layout shared by the Tunet libraries: private
  reporting through the Security tab or by email, one set of response targets
  (critical fixes within 7 days instead of 30), package scope, and secure-use
  guidance. Its supported-versions table lists 1.0.x instead of the
  never-published 0.3.x and 0.4.x.
- `VERSIONING.md` is worded for outside readers; its rules are unchanged.
- Documentation has the layout shared by the Tunet libraries: a reworked docs
  index, the same sections in the release procedure and MCP README, and new
  threat model, security assurance, audit scope, and secure-development
  documents. Guides are corrected against the code: examples say which output
  needs the `locale` or `phones` extra, Italy has its own address template,
  both settings containers reject unknown fields, override timezone names are
  checked only when used, and holidays are national holidays only.
- README sections follow the order the Tunet libraries share: features, version
  status, installation, quick start, usage, MCP server, scope and limitations,
  documentation, development, contributing, and license, with PyPI, Python, and
  license badges. It says 1.x is not yet on PyPI and how to install it from
  `main`, quotes the extras, names 0.1.0 as the upgrade path, drops the unused
  `default_language` from the example, and states what the middleware reads
  and what phone and postal checks prove.
- The repository is now `Tunet-xyz/geo_canon` (the old `Tunet-xyz/GeoCanon` URL
  redirects): project URLs, documentation links, and the README use it, and the
  README names the other Tunet libraries. Install commands in the guides use
  `pip install "GeoCanon[...]"`, and guide titles use sentence case.
- The `holidays` extra requires `holidays>=0.66`. Holiday coverage is every
  jurisdiction whose ISO code the installed release supports (all 197 with
  holidays 0.108), and `get_supported_holiday_jurisdictions()` includes the
  legacy names.
- Reverse ISO lookups return canonical keys: `get_jurisdiction_by_alpha2("CG")`
  is `"Congo (Congo-Brazzaville)"` (was `"Congo"`) and `"CI"` is
  `"Cote d'Ivoire"` (was `"Ivory Coast"`); the same applies to alpha-3 codes
  and `get_country_by_iso`.
- Jamaica and Trinidad and Tobago use the `+1` dial code (were `+876` and
  `+868`). Store `+1` and put the area code in the number.
- `validate_phone` and `validate_postal_code` match the whole value and accept
  only ASCII digits, letters, and whitespace: trailing newlines, full-width or
  Arabic-Indic digits, the Kelvin sign, and no-break spaces now fail. Normalize
  input before validating it.
- `format_address` places `name` and `company` for every registered template,
  China's template shows the postal code, the 18 jurisdictions that require a
  state show it, and whitespace inside each line is normalized.
- `format_currency_locale(..., currency_code=...)` uses the requested currency's
  symbol, decimals, and code when Babel is missing or rejects the locale.
- Exception messages show at most the last two digits of a phone number and
  quote other caller values escaped and cut to 64 characters.
- Without `pytz`, an unknown timezone name raises `ZoneInfoNotFoundError`;
  `ImportError` is kept for a system with no IANA timezone data.
- `import geo_canon` no longer imports Django; names load on first use.
- The MCP server moved to `geo_canon.mcp` (the `geocanon-mcp` command is
  unchanged). `prompts/get` fills a template in one pass and rejects
  undeclared, missing, or non-string arguments; `tools/call` checks each tool's
  required arguments, types, and allowed values; tool descriptions say the
  tools return contract guidance; error details are cut to 200 characters.
- Django classifiers list 4.2, 5.2, and 6.1, the package declares
  `Typing :: Typed`, and its keywords are sorted and add `mcp`.

### Removed

- The `("+876", "Jamaica (+876)")` dial-code choice and the `+876` and `+868`
  phone patterns.
- The top-level `geocanon_mcp` module, which only installs from the `v1.0.0`
  tag contained.
- `AGENTS.md`, `CLAUDE.md`, and `.github` from the sdist.

## [1.0.0] - 2026-11-05 (tagged; not published to PyPI)

### Changed

- Stabilized the documented jurisdiction, ISO, currency, address, phone, locale,
  timezone, language, duration, settings, form, middleware, and local MCP APIs.
- Adopted the shared SemVer and owner-reviewed release policy with matching
  Claude and Codex instructions; aligned runtime, package, and MCP versions.
- Added a `validation` extra for optional Pydantic 2 settings validation and
  included it in `all`; the core still requires only Django.
- Bounded Django below 7, declared MIT license files, and added a hash-locked
  release toolchain, owner-only manual workflows, and protected publishing flow.

### Fixed

- Preserve lazy Django translations in public type annotations and restore the
  configured type-checker environment so the complete source passes mypy.
- Use the optional pytz timezone database when zoneinfo data is missing, and
  surface invalid configured timezone settings instead of silently ignoring them.
- Bound public MCP messages, reject ambiguous/non-finite JSON and invalid request
  shapes, support ping, and keep stdio serving after malformed or oversized input.

## [0.5.0] - 2026-07-15 (not published to PyPI; included in 1.0.0)

### Added

- **Phones extra** - optional `phonenumbers` integration for robust phone validation, E.164/international/national formatting, and number type detection
- **Locale extra** - optional Babel-backed formatting for decimals, percentages, currencies, dates, times, datetimes, and lists
- **Packaged MCP contract** - added the `geocanon-mcp` stdio command and public agent contract for review-first API, data, and locale workflow guidance

### Fixed

- Preserved Django lazy translation objects while sorting jurisdiction and language choices, so `import geo_canon` works before Django settings are configured.

### Documentation

- Added data provenance, update policy, and limitations for the bundled geographic defaults and optional third-party datasets.

## [0.4.0] - 2026-02-25 (not published to PyPI; included in 1.0.0)

### Added

- **ISO Country Codes** - ISO 3166-1 alpha-2, alpha-3, and numeric code mapping (190+ entries) with reverse lookups (`get_jurisdiction_by_alpha2`, `get_jurisdiction_by_alpha3`)

### Changed

- **Flags** - Refactored to derive `FLAG_CSS_CLASS` from the new `iso_codes` module instead of maintaining a duplicate mapping. All public API unchanged.

## [0.3.0] - 2026-02-25 (not published to PyPI; included in 1.0.0)

### Added

- **Address Formats** - Jurisdiction → postal address format mapping (170+ entries), postal-code validation, localised field labels (`get_state_label`, `get_postal_code_label`), and `format_address()` helper

## [0.2.0] - 2026-02-25 (not published to PyPI; included in 1.0.0)

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

[Unreleased]: https://github.com/Tunet-xyz/geo_canon/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Tunet-xyz/geo_canon/releases/tag/v1.0.0
[0.1.0]: https://pypi.org/project/GeoCanon/0.1.0/
