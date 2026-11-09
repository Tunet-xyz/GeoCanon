# GeoCanon security assurance case

This document links GeoCanon's security claims to repository evidence. Passing
evidence increases confidence; it is not an independent audit or a
certification.

## Claims and evidence

| Claim | Implementation | Automated evidence |
| --- | --- | --- |
| Phone and postal-code validation follows the bundled patterns | `dial_codes`, `address_formats` | `tests/test_dial_codes.py`, `tests/test_address_formats.py` |
| Unknown jurisdictions and values are not guessed | lookups in each module | the module tests, such as `tests/test_jurisdictions.py` and `tests/test_currencies.py` |
| The jurisdiction form accepts only known jurisdictions | `jurisdictions/forms.py` | `tests/test_forms.py` |
| Settings load from Django with defaults and overrides | `settings.py` | `tests/test_settings.py` |
| Optional features fall back without their extras | `locale_formats`, phone helpers | `tests/test_locale_formats.py`, `tests/test_import.py` |
| The MCP server is bounded and read-only | `geocanon_mcp/server.py` | `tests/test_mcp_server.py` |
| One release identity across metadata and both MCP contracts | `pyproject.toml`, the contracts | `tests/test_release_identity.py` |
| No code evaluation or unsafe calls | the whole package | Bandit |

Two claims have no dedicated test yet and rest on code review: the jurisdiction
middleware reads only the session or the default (`jurisdictions/middleware.py`),
and settings reject unknown keys, with Pydantic validation when the `validation`
extra is installed (`settings.py`).

## Evidence commands

Run from a clean checkout of the revision being assessed:

```bash
python -m pip install -e ".[all,dev]"
python -m ruff check src tests
python -m mypy src/geo_canon src/geocanon_mcp
python -m bandit -r src
python -m pip freeze --exclude GeoCanon > audit-requirements.txt
python -m pip_audit --strict --disable-pip --no-deps -r audit-requirements.txt
python -m pytest --cov=geo_canon --cov=geocanon_mcp --cov-branch
```

Repeat the tests without extras to cover the fallbacks.

## Workflow evidence

The GitHub workflows are manual: only the owner starts them, and none runs on
a schedule. Record which of them ran for the assessed commit.

| Workflow | What it runs |
| --- | --- |
| `tests.yaml` | Ruff, mypy, and pytest with branch coverage |
| `security.yaml` | Bandit and a strict dependency audit |
| `publish.yaml` | The same checks, a hash-locked build with checksums, and PyPI publication |

Keep the workflow URLs and logs, commit SHA, and release checksums as the
evidence bundle; workflow artifacts expire.

## Manual evidence still required

- Independent code and data review, including a check of the bundled data
  against its sources ([data provenance](data-provenance.md)).
- A test of the jurisdiction middleware with hostile session values.
- The host application's escaping of GeoCanon output and its handling of
  personal data in error messages.
- Repository settings from GitHub (see
  [secure development](SECURE_DEVELOPMENT.md#repository-controls)).
