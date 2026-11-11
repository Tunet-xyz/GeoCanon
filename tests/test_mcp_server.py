"""Regression checks for the local public-contract protocol boundary."""

import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from geo_canon.mcp.server import MAX_MESSAGE_CHARS, handle, load_contract, main, parse_message

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}


def test_checkout_and_packaged_contract_and_server_agree():
    assert json.loads((ROOT / "mcp/agent-contract.json").read_text()) == load_contract()
    launcher = (ROOT / "mcp/server.py").read_text(encoding="utf-8")
    assert "from geo_canon.mcp.server import main" in launcher


def test_console_script_targets_the_packaged_server():
    metadata = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'geocanon-mcp = "geo_canon.mcp.server:main"' in metadata
    assert 'packages = ["src/geo_canon"]' in metadata


@pytest.mark.parametrize("module", ["geo_canon", "geo_canon.mcp.server"])
def test_importing_the_package_or_server_does_not_load_django(module):
    probe = f"import sys, {module}; print('django' in sys.modules)"
    result = subprocess.run(
        [sys.executable, "-c", probe],
        env=SOURCE_ENV,
        capture_output=True,
        check=True,
        text=True,
        timeout=60,
    )
    assert result.stdout.strip() == "False"


def test_python_dash_m_runs_the_server():
    result = subprocess.run(
        [sys.executable, "-m", "geo_canon.mcp"],
        input=b'{"jsonrpc":"2.0","id":1,"method":"initialize"}\n',
        env=SOURCE_ENV,
        capture_output=True,
        check=True,
        timeout=60,
    )
    reply = json.loads(result.stdout.splitlines()[0])
    assert reply["result"]["serverInfo"]["name"] == load_contract()["server"]["name"]


@pytest.mark.parametrize("message", [[], None, 42, {"id": True}, {"id": []}])
def test_invalid_requests_do_not_crash_the_server(message):
    response = handle(message, load_contract())
    assert response is not None and response["error"]["code"] == -32600


@pytest.mark.parametrize("document", ['{"id":1,"id":2}', '{"id":NaN}', '{"id":1e999}'])
def test_ambiguous_or_nonfinite_json_is_rejected(document):
    with pytest.raises(ValueError):
        parse_message(document)


def test_ping_and_notification_semantics():
    contract = load_contract()
    assert handle({"jsonrpc": "2.0", "id": 1, "method": "ping"}, contract)["result"] == {}
    assert handle({"jsonrpc": "2.0", "method": "ping"}, contract) is None
    response = handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": []}, contract)
    assert response["error"]["code"] == -32602


def test_public_discovery_resources_tools_and_prompts_are_callable():
    contract = load_contract()

    def request(method, params=None):
        response = handle(
            {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}},
            contract,
        )
        assert response is not None and "result" in response
        return response["result"]

    for resource in request("resources/list")["resources"]:
        contents = request("resources/read", {"uri": resource["uri"]})["contents"]
        assert contents and contents[0]["text"]
    for tool in request("tools/list")["tools"]:
        output = request("tools/call", {"name": tool["name"], "arguments": valid_arguments(tool)})
        assert output["isError"] is False
        assert output["structuredContent"]["offering"]["id"] == "geo_canon"
    for prompt in request("prompts/list")["prompts"]:
        arguments = {argument["name"]: "example" for argument in prompt["arguments"]}
        output = request("prompts/get", {"name": prompt["name"], "arguments": arguments})
        assert output["messages"]


def valid_arguments(tool):
    """Arguments that satisfy a tool's inputSchema."""
    arguments = {}
    for name, spec in tool["inputSchema"].get("properties", {}).items():
        if "enum" in spec:
            arguments[name] = spec["enum"][0]
        elif spec.get("type") == "array":
            arguments[name] = ["example"]
        else:
            arguments[name] = "example"
    return arguments


def call(method, params):
    return handle({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, load_contract())


def test_prompt_arguments_are_substituted_once():
    reply = call("prompts/get", {"name": "agent_onboarding", "arguments": {"user_goal": "{user_goal}"}})
    text = reply["result"]["messages"][0]["content"]["text"]
    assert text.count("{user_goal}") == 1


def test_prompt_arguments_cannot_inject_or_amplify():
    # Sequential substitution let one argument's value name another argument,
    # so a 10 KB request could produce a reply of several megabytes.
    arguments = {"user_goal": "{a}" * 1000, "a": "{b}" * 1000, "b": "x" * 1000}
    reply = call("prompts/get", {"name": "agent_onboarding", "arguments": arguments})
    assert reply["error"]["code"] == -32602
    assert len(json.dumps(reply)) < 1000


@pytest.mark.parametrize(
    "arguments",
    [{}, {"user_goal": 42}, {"user_goal": ["list"]}],
)
def test_prompt_arguments_are_checked(arguments):
    reply = call("prompts/get", {"name": "agent_onboarding", "arguments": arguments})
    assert reply["error"]["code"] == -32602


@pytest.mark.parametrize(
    ("tool", "arguments"),
    [
        ("map_workflow_to_tools", {}),
        ("prepare_global_form", {"jurisdictions": ["France"]}),
        ("list_public_capabilities", {"surface": "everything"}),
        ("prepare_locale_configuration", {"features": "holidays"}),
        ("prepare_locale_configuration", {"features": [1, 2]}),
        ("operate_browser_docs", {"task": True}),
    ],
)
def test_tool_arguments_follow_the_input_schema(tool, arguments):
    assert call("tools/call", {"name": tool, "arguments": arguments})["error"]["code"] == -32602


def test_tool_results_say_they_return_contract_guidance():
    reply = call("tools/call", {"name": "describe_offering", "arguments": {}})
    assert "does not run GeoCanon or generate code" in reply["result"]["content"][0]["text"]
    for tool in load_contract()["tools"]:
        assert not tool["description"].startswith(("Generate", "Draft")), tool["name"]


def test_error_details_are_bounded(monkeypatch, capsys):
    reply = call("tools/call", {"name": "x" * 100_000, "arguments": {}})
    assert reply["error"]["code"] == -32602
    assert len(reply["error"]["message"]) < 400

    unknown_method = call("m" * 1000, {})
    assert unknown_method["error"] == {
        "code": -32601,
        "message": "Method not found: " + "m" * 200 + "...",
    }

    key = "k" * 1000
    monkeypatch.setattr(sys, "stdin", io.StringIO(f'{{"{key}":1,"{key}":2}}\n'))
    main()
    duplicate = json.loads(capsys.readouterr().out)
    assert duplicate["error"] == {
        "code": -32700,
        "message": "Parse error",
        "data": {"detail": ("Duplicate JSON object key: " + key)[:200] + "..."},
    }


@pytest.mark.parametrize(
    ("method", "params"),
    [
        ("resources/read", {"uri": []}),
        ("resources/read", {"uri": "unknown"}),
        ("tools/call", {"name": [], "arguments": {}}),
        ("tools/call", {"name": "unknown", "arguments": []}),
        ("prompts/get", {"name": [], "arguments": {}}),
        ("prompts/get", {"name": "unknown", "arguments": []}),
    ],
)
def test_invalid_resource_tool_and_prompt_parameters_fail_safely(method, params):
    response = handle({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, load_contract())
    assert response["error"]["code"] == -32602


def test_stdio_recovers_from_hostile_input_and_reports_the_release_version():
    payload = (
        b"[]\n"
        + b" " * (MAX_MESSAGE_CHARS + 1)
        + b"\n"
        + b'\xff\n'
        + b'{"jsonrpc":"2.0","id":3,"method":"initialize"}\n'
    )
    result = subprocess.run(
        [sys.executable, str(ROOT / "mcp/server.py")],
        input=payload,
        capture_output=True,
        check=True,
        timeout=15,
    )
    responses = [json.loads(line) for line in result.stdout.splitlines()]
    assert [response["error"]["code"] for response in responses[:3]] == [
        -32600, -32700, -32700,
    ]
    assert responses[3]["result"]["serverInfo"]["version"] == load_contract()["server"]["version"]
