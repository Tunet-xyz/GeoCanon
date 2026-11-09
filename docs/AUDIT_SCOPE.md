# GeoCanon audit scope

An assessment must name an immutable Git commit and the exact wheel and sdist
SHA-256 digests. Findings against a moving branch or an unverified local build
are not release evidence.

## In scope

- All code under `src/geo_canon` and `src/geocanon_mcp`: the lookups,
  validators, formatters, settings, Django forms and middleware, and the MCP
  server.
- The bundled data, its stated sources, and its update policy.
- The boundaries with the optional dependencies (`holidays`, `pytz`,
  `phonenumbers`, Babel, and Pydantic).
- Build, dependency, and release configuration.

## Out of scope unless separately commissioned

- Django itself and the optional dependencies' own code and data.
- The legal, tax, regulatory, or postal correctness of bundled data, beyond
  checking it against its stated sources.
- The host application's templates, escaping, data storage, authentication,
  and authorization.

## Review entry points

Start with the [threat model](THREAT_MODEL.md), the
[data provenance](data-provenance.md) document, and the
[security assurance case](SECURITY_ASSURANCE.md). Then trace the phone and
postal-code patterns, the middleware's session input, settings loading, and the
MCP server's message handling. Record tool versions, and distinguish automated
findings from manual design conclusions.
