# Data provenance and update policy

GeoCanon ships curated defaults so applications can use a stable, typed API without making network calls at runtime. Those defaults are versioned package data, not a live mirror of standards bodies or a substitute for jurisdiction-specific advice.

## Source classes

GeoCanon's data model follows these public standards and upstream datasets:

| Surface | Reference source | How GeoCanon uses it |
| --- | --- | --- |
| Jurisdiction and country codes | [ISO 3166](https://www.iso.org/iso-3166-country-codes.html) | Stable jurisdiction keys and alpha-2, alpha-3, and numeric code mappings. |
| Currency codes | [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html) | Currency codes, symbols, and decimal-place defaults. |
| Timezone identifiers | [IANA Time Zone Database](https://www.iana.org/time-zones) | Default IANA timezone choices for jurisdiction lookups. |
| Locale formatting | [Unicode CLDR](https://cldr.unicode.org/) through Babel | Optional locale-aware number, currency, date, time, and list formatting. |
| Phone metadata | [Google libphonenumber](https://github.com/google/libphonenumber) through `phonenumbers` | Optional parsing, validation, number type detection, and display formatting. |
| Public holidays | The optional [`holidays`](https://github.com/vacanza/holidays) package | Runtime holiday calculation for every jurisdiction whose ISO code the installed `holidays` release (0.66 or later) supports; dates and names come from that release. |
| Flag CSS classes | The ISO alpha-2 convention used by [`flag-icons`](https://github.com/lipis/flag-icons) | Generates CSS class names; GeoCanon does not bundle flag artwork. |

The repository currently maintains the core jurisdiction, code, timezone, language, currency, dial-code, and address mappings directly. It does not automatically synchronize those tables from upstream services during installation or runtime.

The phone fallback's trunk prefixes and pattern lengths come from libphonenumber's metadata in `phonenumbers` 9.0.43: the national prefixes, and the possible lengths of fixed-line and mobile numbers, and of other number types unless a region also uses that length for local numbers dialled without the area code. `tests/phone_examples.json` freezes that data and libphonenumber's example numbers, so the tests give the same results with any `phonenumbers` release or none. The patterns follow numbering changes such as Benin's move to ten-digit numbers on 2024-11-30. On 2026-11-10 the currency table was checked against ISO 4217 and the CLDR 47 territory currencies, and updated for Zimbabwe's ZWG (April 2024), Curaçao's XCG (2025-03-31), and Bulgaria's euro (2026-01-01); the [currencies guide](currencies.md#withdrawn-currencies) lists the conversion rates from the issuing central banks.

## Update policy

- Review bundled mappings before each minor release and record material additions, removals, and renames in `CHANGELOG.md`.
- Ship factual corrections that affect existing lookups in a patch release when compatibility can be preserved.
- Use a minor release for new data surfaces, changed defaults, or corrections that can materially change application behavior.
- Keep reverse lookups and cross-module invariants covered by tests so duplicated identifiers cannot silently drift.
- Treat dependency-backed results as belonging to the installed dependency version; pin optional dependencies when reproducibility matters.

Corrections should include a primary-source reference in the pull request or issue that introduces the change.

## Limitations

- A country can have multiple timezones, currencies, languages, address conventions, or phone-number patterns. A single default is a product convenience, not a complete geopolitical model.
- Postal formats and labels vary within jurisdictions and change over time. Validate addresses through an authoritative delivery provider when deliverability matters.
- Holiday coverage and naming depend on the installed `holidays` version. GeoCanon asks for national holidays only; it does not pass subdivisions.
- Phone validity and formatting depend on `phonenumbers` metadata; a syntactically valid number is not proof that the number exists or belongs to a user.
- Without the `phones` extra, phone checks test digits and lengths only: a malformed number whose length fits another number type passes, and a few real numbers still fail (the [dial-codes guide](dial-codes.md) lists them).
- Locale formatting is presentation logic, not tax, accounting, accessibility, or legal advice.
- Jurisdiction names and boundaries can be disputed. Applications with policy or legal consequences should maintain their own reviewed overrides and decision records.

## Release review checklist

1. Run the full test suite, including import-before-Django-setup checks.
2. Compare code, currency, timezone, and address mapping changes against primary references.
3. Review renamed or removed identifiers for backwards compatibility.
4. Exercise the package with and without every optional extra.
5. Build the wheel and source distribution, run `twine check`, and smoke-test imports from the wheel.
