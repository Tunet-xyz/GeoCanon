# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.4.x   | :white_check_mark: |
| 0.3.x   | :white_check_mark: |
| < 0.3   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in GeoCanon, please report it responsibly.

### How to Report

**Please DO NOT open a public GitHub issue for security vulnerabilities.**

Instead, please email security concerns to: **alex@tunet.xyz**

Include the following in your report:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Acknowledgement:** Within 48 hours
- **Initial assessment:** Within 5 business days
- **Fix release:** Within 30 days for critical issues

### Scope

The following are in scope:
- Locale data injection or manipulation
- Regex denial-of-service in phone validation patterns
- Path traversal via jurisdiction or locale inputs
- Any bypass of input validation or Pydantic settings

### Out of Scope

- Vulnerabilities in Django itself (report to Django security team)
- Issues in third-party extras (`holidays`, `pytz`)
- Issues requiring physical access to the server

## Security Features

GeoCanon includes several security features:

- ✅ Input validation via Pydantic settings
- ✅ Rich exceptions with actionable hints (no internal leakage)
- ✅ Type hints throughout for static analysis
- ✅ PEP 561 `py.typed` marker for mypy/pyright
- ✅ Per-country regex patterns for phone validation (no `eval`)
- ✅ All lookups use O(1) dictionary access (no injection surface)
