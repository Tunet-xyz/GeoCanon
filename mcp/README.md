# GeoCanon MCP server

This directory holds GeoCanon's public agent contract and a dependency-free
stdio MCP server for it. Agents can use it to discover GeoCanon's modules,
APIs, and optional extras, and to get guidance for settings, forms, and
middleware that handle jurisdictions, addresses, phones, currencies, and
locales. The server runs locally under the caller's control, makes no network
connections, and needs no credentials or account. There is no hosted GeoCanon
MCP service, and nothing here gives access to the maintainer's agents,
accounts, or infrastructure.

## Run

After installing GeoCanon:

```bash
geocanon-mcp
```

From a source checkout:

```bash
python mcp/server.py
```

## Files

| File | Purpose |
| --- | --- |
| `README.md` | This guide. |
| `agent-contract.json` | The public agent contract, byte-identical to the packaged `src/geocanon_mcp/agent-contract.json`. |
| `server.py` | The dependency-free server, identical to the packaged `src/geocanon_mcp/server.py`. |

## Methods and tools

The server implements `initialize`, `ping`, `resources/list`,
`resources/read`, `tools/list`, `tools/call`, `prompts/list`, and
`prompts/get`.

Every tool returns the contract's guidance for its task, with the arguments
you passed and the contract's access and safety rules. The calling agent
writes any settings or code, for a person to review.

| Tool | Guidance on |
| --- | --- |
| `describe_offering` | GeoCanon's modules, APIs, optional extras, and safe operating model. |
| `list_public_capabilities` | Package APIs, modules, optional extras, docs, and browser references. |
| `map_workflow_to_tools` | Mapping a goal to public APIs, docs, extras, approval gates, and verification steps. |
| `prepare_locale_configuration` | `GeoCanonSettings` and an integration plan for jurisdictions, languages, timezones, and overrides. |
| `prepare_global_form` | Forms and middleware for jurisdiction, address, phone, currency, and locale behavior. |
| `operate_browser_docs` | Walking a user through public docs, PyPI, GitHub issues, or reference docs in a browser. |

Resources: `overview`, `public-apis`, `workflows`, `browser-surfaces`, and
`security-and-audit`. Prompt: `agent_onboarding`.

## Limits

The server reads one JSON-RPC message per line. It answers with a JSON-RPC
error, and keeps serving, when a line is longer than 1,100,000 characters
(newline included), is not valid UTF-8 JSON, repeats an object key, uses `NaN`
or `Infinity`, has a number longer than 256 characters, or has an invalid
request shape.

## Boundaries

- Jurisdiction data is not legal, tax, regulatory, or compliance advice; a
  person must review any such use.
- Agents must not handle customers' real addresses or phone numbers unless
  the user supplies safe examples.
- Agents work from published package APIs, public documentation, and this
  contract. They must not assume access to private source code, unredacted
  settings, production data, or provider dashboards unless the user grants
  it.
