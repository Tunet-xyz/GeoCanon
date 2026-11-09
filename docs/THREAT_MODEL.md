# GeoCanon threat model

This threat model covers the GeoCanon package at a specific source revision.
It is not a system accreditation and must be combined with the host
application's data, deployment, and operational threat models.

## Security objective

GeoCanon turns jurisdiction names and user-supplied values into reference data,
validation results, and formatted text. It must never execute input, read files
or reach the network because of input, or run a validation pattern in
super-linear time. Its bundled data is maintained release data, not an
authoritative legal, postal, tax, or telecom source.

## Assets and trust boundaries

- Protected assets are the integrity of the bundled mappings (jurisdictions,
  ISO codes, dial codes and phone patterns, timezones, currencies, address
  formats, languages, and the holiday registry) and the availability of the
  host's request handling.
- Values passed to lookups, validators, formatters, and forms (jurisdiction
  names, phone numbers, postal codes, amounts, address fields) come from the
  application and may originate with untrusted users.
- `JurisdictionMiddleware` sets `request.jurisdiction` from the session's
  `jurisdiction` key, or from the configured default. It never reads query
  strings or headers. Whatever the application writes to that session key is
  trusted.
- Settings (`GEOCANON`) are trusted configuration.
- The optional dependencies (`holidays`, `pytz`, `phonenumbers`, Babel, and
  Pydantic) are trusted code with their own data.
- The MCP server reads requests from a local client over stdio, without
  authentication.

## Threats and controls

| Threat | Package control | Residual responsibility |
| --- | --- | --- |
| Regular-expression denial of service in phone or postal validation | Patterns are anchored, with bounded quantifiers and no nested repetition; `phonenumbers` caps input at 250 characters | Limit field lengths at the form or API boundary |
| Code or template injection through input | No `eval`, `exec`, or import of input; `format_address` passes values as template arguments, never as the template | Escape formatted output for its destination (HTML, PDF, email) |
| File or network access through input | Lookups use dictionary keys; timezone names come from the bundled map or settings; Babel sanitizes locale identifiers | Review settings overrides before deployment |
| Untrusted jurisdiction in the session | The middleware reads only the session key or the configured default | Write only validated values (for example from `JurisdictionContextSwitchForm`) to the session, and escape `request.jurisdiction` when rendering it |
| Wrong or stale reference data used for decisions | [Data provenance](data-provenance.md) and update policy; data changes are recorded in the changelog | Review defaults before compliance, tax, postal, or telecom decisions |
| Hostile or oversized MCP input | Line and number size limits, strict JSON, argument checks, error replies instead of crashes | Run the server only for a local client you trust |
| Supply-chain substitution | Pinned workflow actions, hash-locked build tools, Trusted Publishing, owner-approved releases | Pin and verify releases; keep the optional dependencies updated |

## Required invariants

1. No input is evaluated as code, imported, or used as a file path.
2. Validation patterns are anchored and use only bounded quantifiers.
3. Unknown jurisdictions and values produce `None` or `False` (the timezone
   helpers raise an error instead), never a guessed result.
4. The middleware never takes the jurisdiction from query strings or headers.
5. The MCP server reads only its packaged contract and makes no network or
   subprocess calls.

## Out of scope

The legal, tax, regulatory, or postal correctness of bundled data; Django
itself; the optional dependencies' data and vulnerabilities; escaping of
GeoCanon output in the host's templates; and authentication and authorization.

## Residual risks

- Bundled data can be wrong or out of date, and holiday coverage depends on the
  installed `holidays` release.
- Validators check format only, and only ASCII input passes; normalize user
  input (for example full-width digits) before validating it.
- The middleware does not validate the session value it copies to
  `request.jurisdiction`.
- Error messages can still contain part of a caller's value: other values are
  escaped and cut to 64 characters, and phone numbers show at most their last
  two digits.
- The MCP server has no authentication and echoes request content in its
  replies, with error details cut to 200 characters.
- GeoCanon has not had an independent security audit.

## Review triggers

Review this model for every new data source or bulk data update, validation
pattern, optional dependency, settings field, middleware or form input path,
and MCP server change. Record newly accepted residual risks before merge.
