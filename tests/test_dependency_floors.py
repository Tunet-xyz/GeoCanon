"""The minimum-dependencies job must install exactly the floors pyproject declares."""

from __future__ import annotations

import sys
from pathlib import Path

from packaging.requirements import Requirement
from packaging.version import Version

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

ROOT = Path(__file__).resolve().parents[1]


def declared_floors() -> dict[str, Version]:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    lines = list(project["dependencies"])
    for extra, requirements in project["optional-dependencies"].items():
        if extra != "dev":
            lines.extend(requirements)
    floors: dict[str, Version] = {}
    for line in lines:
        requirement = Requirement(line)
        lower = [Version(spec.version) for spec in requirement.specifier if spec.operator == ">="]
        assert len(lower) == 1, f"{line} needs exactly one '>=' floor"
        name = requirement.name.lower()
        assert floors.setdefault(name, lower[0]) == lower[0], f"{name} has two floors"
    return floors


def minimum_pins() -> dict[str, Version]:
    pins: dict[str, Version] = {}
    text = (ROOT / "requirements/minimum.txt").read_text(encoding="utf-8")
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        requirement = Requirement(line)
        (spec,) = requirement.specifier
        assert spec.operator == "==", line
        # "==4.2.*" pins the floor's release series; "==0.66" pins the floor itself.
        pins[requirement.name.lower()] = Version(spec.version.removesuffix(".*"))
    return pins


def test_minimum_constraints_pin_every_declared_floor():
    assert minimum_pins() == declared_floors()


def test_minimum_dependencies_job_installs_the_constraints():
    workflow = (ROOT / ".github/workflows/tests.yaml").read_text(encoding="utf-8")
    assert "minimum-dependencies:" in workflow
    assert "-c requirements/minimum.txt" in workflow
