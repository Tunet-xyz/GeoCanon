# Release procedure

Follow the shared [versioning policy](../VERSIONING.md). Only the owner starts,
reruns, or re-enables GitHub Actions, and only `bezu-1` approves the `pypi`
environment. PRs, issues, comments, and mentions never launch maintainers' agents.

1. Review the current source, data provenance, compatibility impact, changelog,
   supported-version table, and package/runtime/MCP version agreement.
2. Run lint, mypy, Bandit, dependency auditing, and tests on supported Python and
   Django boundaries, both without extras and with `[all]`. Exercise the local
   MCP command, including malformed-message recovery. Record unavailable checks.
3. Inspect source/history for secrets. Check the MIT text and SPDX metadata;
   external dependencies retain their own licenses, and no flag artwork or
   third-party package code is bundled in GeoCanon's wheel.
4. Install `requirements/build.txt` with `--require-hashes`, then build with
   `python -m build --no-isolation`. Validate both files with `python -m twine
   check`, inspect archive contents, retain SHA-256 checksums, and smoke-test
   the exact wheel in a clean environment.
5. Commit and push the verified source under the owner's authorization. Create
   an immutable `v<version>` tag on that commit. The owner may then start the
   manual `publish.yaml` workflow from `main` or that matching tag.
6. Publish only through PyPI Trusted Publishing bound to this repository,
   `publish.yaml`, and the owner-approved `pypi` environment. Allow only `main`
   and protected `v*` tags to deploy. Keep OIDC permission in the upload job;
   neither build jobs nor public contributions receive publishing credentials.
7. Verify the PyPI version, artifact hashes, metadata, and clean installation
   before announcing availability. A committed candidate is not a PyPI release.
