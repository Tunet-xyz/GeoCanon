"""A release must have one identity across metadata and both MCP contracts."""

import json
import re
from pathlib import Path

from geo_canon import __version__


def test_release_identity_and_license():
    root = Path(__file__).resolve().parents[1]
    metadata = (root / "pyproject.toml").read_text()
    assert re.search(rf'^version = "{re.escape(__version__)}"$', metadata, re.M)
    assert 'license = "MIT"' in metadata and 'license-files = ["LICENSE"]' in metadata
    assert json.loads((root / "src/geocanon_mcp/agent-contract.json").read_text())["server"]["version"] == __version__
    assert (root / "mcp/agent-contract.json").read_bytes() == (
        root / "src/geocanon_mcp/agent-contract.json"
    ).read_bytes()
    assert f"## [{__version__}] - " in (root / "CHANGELOG.md").read_text()
