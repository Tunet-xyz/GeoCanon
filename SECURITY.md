# Security policy

## Supported versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

Security fixes ship as new 1.0.x releases on
[PyPI](https://pypi.org/project/GeoCanon/). GeoCanon 1.0.0 is tagged (`v1.0.0`)
but not yet published there; PyPI still serves 0.1.0, which is not supported.

## Reporting a vulnerability

Do not report a suspected vulnerability in a public issue, pull request, or
discussion. Report it privately in either of these ways:

- On GitHub, open the repository's **Security** tab and choose
  **Report a vulnerability**
  ([direct link](https://github.com/Tunet-xyz/geo_canon/security/advisories/new)).
- Email **alex@tunet.xyz**.

Include a description, the affected versions, reproduction steps, the potential
impact, and any suggested mitigation. Use synthetic examples; do not send
credentials, personal data, or production samples.

## Response targets

We aim to acknowledge reports within 48 hours and provide an initial assessment
within five business days. Targets begin when severity is confirmed:

| Severity | Containment/mitigation target | Fix target |
| --- | --- | --- |
| Critical | 24 hours | 7 days |
| High | 3 business days | 14 days |
| Moderate | 10 business days | 30 days |
| Low | 30 days | 90 days |

These are maximum targets, not a promise to delay urgent fixes. If a complete
fix needs longer, we will prioritize a safe mitigation, coordinate disclosure,
and communicate a revised timeline privately. Please allow a reasonable period
for remediation before public disclosure. We will request a CVE and publish a
GitHub security advisory when impact warrants it.

## Scope

### In scope

- Injection or manipulation of locale or jurisdiction data.
- Regular-expression denial of service in phone or postal-code validation
  patterns.
- Path traversal through jurisdiction or locale inputs.
- Any bypass of input validation or of Pydantic settings validation.
- Malformed or oversized input that stops the local MCP server from serving.

### Out of scope

- Vulnerabilities in Django itself; report them to the Django security team.
- Vulnerabilities in the optional dependencies (`holidays`, `pytz`,
  `phonenumbers`, Babel, and Pydantic); report them to those projects.
- Inaccurate reference data (country, currency, holiday, or address facts)
  without a security impact; report it as a regular issue.
- Issues that require physical access to the server.

## Secure use

- Bundled mappings are maintained release data, not a live legal or standards
  feed. Review the [data provenance and update policy](docs/data-provenance.md)
  before relying on defaults for compliance, tax, postal, or other high-stakes
  decisions.
- Phone and postal-code validators check format only; they do not show that a
  number or address exists or belongs to the person who entered it.
- Install the `validation` extra to validate settings with Pydantic 2.
- Keep the optional dependencies up to date; their data and security fixes ship
  separately from GeoCanon.

## Releases and advisories

Security fixes are released from a reviewed commit on `main` through the
owner-approved trusted-publishing workflow described in
[docs/RELEASE.md](docs/RELEASE.md). Workflows run only when the owner starts
them, and PyPI uploads use short-lived OIDC credentials from a protected
environment. Stable API changes follow [VERSIONING.md](VERSIONING.md); a
security fix may intentionally reject previously accepted ambiguous input, with
the compatibility and migration impact explained in the release notes. Pin and
verify release artifacts, watch this repository's security advisories, test
your integration, and upgrade supported versions promptly.
