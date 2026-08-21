---
title: Using the CLI
url: https://platform.claude.com/docs/en/cli-sdks-libraries/cli/using
description: Command structure, output formats, GJSON transforms, request bodies, and debugging for the ant CLI.
---

This page covers the `ant` CLI's input and output mechanics that apply across every endpoint. For installing and authenticating, see the [Quickstart](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/quickstart). For chaining commands and version-controlling resources, see [CLI scripting and automation](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/scripting).

## Command structure

Commands follow a `resource action` pattern. Nested resources use colons:

```text wrap
ant <resource>[:<subresource>] <action> [flags]
```

Run `ant --help` for the full resource list, or append `--help` to any subcommand for its flags.

Resources in beta (including agents, sessions, deployments, and environments) live under the `beta:` prefix. Commands in this namespace automatically send the appropriate `anthropic-beta` header for that resource, so you don't need to pass it yourself. Use `--beta <header>` only to override the default (for example, to opt into a different schema version).

```bash
ant models list
ant messages create --model claude-opus-5 --max-tokens 1024 ...
ant beta:agents retrieve --agent-id agent_01...
ant beta:sessions:events list --session-id session_01...
```

### Global flags

| Flag                                  | Description                                                                                                                                                                                                                 |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--profile`                           | Named profile to use for this invocation (equivalent to setting `ANTHROPIC_PROFILE`). See [Switch between workspaces](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/authentication#switch-between-workspaces). |
| `--format`                            | Output format: `auto`, `json`, `jsonl`, `yaml`, `pretty`, `raw`, `explore`                                                                                                                                                  |
| `--transform`                         | Filter or reshape the response with a [GJSON path](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/using#transform-output-with-gjson)                                                                            |
| `-r`, `--raw-output`                  | Print string results without surrounding quotes, like `jq -r`                                                                                                                                                               |
| `--base-url`                          | Override the API base URL                                                                                                                                                                                                   |
| `--debug`                             | Print full HTTP request and response to stderr                                                                                                                                                                              |
| `--format-error`, `--transform-error` | Same as `--format` and `--transform` but applied to [error responses](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/scripting#inspect-errors)                                                                  |

## Output formats

`auto` pretty-prints JSON and is the default for commands that create or modify resources. List and retrieve commands default to the [interactive explorer](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/using#interactive-explorer) when writing to a terminal, and to pretty-printed JSON when piped. Override either default with `--format`:

```bash
ant models retrieve --model-id claude-opus-5 --format yaml
```

```yaml Output
type: model
id: claude-opus-5
display_name: Claude Opus 5
created_at: "2026-07-24T00:00:00Z"
...
```

List endpoints auto-paginate. In the default formats each item is written separately (one compact JSON object per line in `jsonl` mode, a stream of YAML documents in `yaml` mode), which streams cleanly into `head`, `grep`, and `--transform` filters.

### Interactive explorer

The explorer is a fold-and-search TUI for browsing large responses. Arrow keys expand and collapse nodes, `/` searches, `q` exits. List and retrieve commands open it by default when connected to a terminal. Pass `--format explore` to open it explicitly:

```bash
ant models list --format explore
```

## Transform output with GJSON

Use `--transform` to reshape responses before printing. The expression is a [GJSON path](https://github.com/tidwall/gjson/blob/master/SYNTAX.md). For list endpoints the transform runs against each item individually, not the envelope:

```bash
ant beta:agents list \
  --transform "{id,name,model}" \
  --format jsonl
```

```jsonl Output
{"id": "agent_011CYm1BLqPX...", "name": "Docs CLI Test Agent", "model": "claude-opus-5"}
{"id": "agent_011CYkVwfaEt...", "name": "Coffee Making Assistant", "model": "claude-opus-5"}
{"id": "agent_011CYixHhtUP...", "name": "Coding Assistant", "model": "claude-opus-5"}
```

### Extract a scalar

To capture a single field as an unquoted string (for example, the ID of a newly created resource), pair `--transform` with `--raw-output`. The result prints without JSON quotes and is ready to assign to a shell variable:

```bash
AGENT_ID=$(ant beta:agents create \
  --name "My Agent" \
  --model '{id: claude-opus-5}' \
  --transform id --raw-output)

printf '%s\n' "$AGENT_ID"
```

```text Output wrap
agent_011CYm1BLqPXpQRk5khsSXrs
```

<Note>
  `--raw-output` is distinct from `--format raw`. `--raw-output` strips JSON quotes from string results, like `jq -r`. `--format raw` prints the response body's raw JSON bytes without auto-paginating; on list endpoints it applies `--transform` to the pagination envelope rather than to each item.
</Note>

## Passing request bodies

The right input mechanism depends on the shape of the data: use **flags** for scalar fields and short structured values, pipe a **stdin** document for nested or multiline bodies, and use **`@file` references** to pull file contents into any string or binary field.

### Flags

Scalar fields map directly to flags. Structured fields accept a relaxed YAML-like syntax (unquoted keys, optional quotes around strings) or strict JSON:

```bash
ant beta:sessions create \
  --agent '{type: agent, id: agent_011CYm1BLqPXpQRk5khsSXrs, version: 1}' \
  --environment-id env_01595EKxaaTTGwwY3kyXdtbs \
  --title "CLI docs test session"
```

Repeatable flags build arrays. Each `--tool` or `--event` appends one element:

```bash
ant beta:agents create \
  --name "Research Agent" \
  --model '{id: claude-opus-5}' \
  --tool '{type: agent_toolset_20260401}' \
  --tool '{type: custom, name: search_docs, input_schema: {type: object, properties: {query: {type: string}}}}'
```

### Stdin

Pipe a JSON or YAML document to stdin to supply the full request body. Fields from stdin are merged with flags, with flags taking precedence. Here `version` is the optimistic-locking token returned by an earlier `retrieve`, and `$AGENT_ID` was captured as in [Extract a scalar](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/using#extract-a-scalar):

```bash
echo '{"description": "Updated test agent.", "version": 1}' | \
  ant beta:agents update --agent-id "$AGENT_ID"
```

Heredocs work the same way and are convenient for multiline YAML. Quote the delimiter (as in `<<'YAML'`) to disable variable expansion inside the body.

```bash
ant beta:agents create <<'YAML'
name: Research Agent
model: claude-opus-5
system: |
  You are a research assistant. Cite sources for every claim.
tools:
  - type: agent_toolset_20260401
YAML
```

### File references

Flags that take a file path, such as `--file` on the upload command, accept a bare path:

```bash
ant files upload --file ./report.pdf
```

To inline a file's contents into a string-valued field, prefix the path with `@`:

```bash
ant beta:agents create \
  --name "Researcher" --model '{id: claude-opus-5}' \
  --system @./prompts/researcher.txt
```

Inside structured flag values, wrap the path in quotes. To send a PDF to the Messages API:

```bash
ant messages create \
  --model claude-opus-5 \
  --max-tokens 1024 \
  --message '{role: user, content: [
    {type: document, source: {type: base64, media_type: application/pdf, data: "@./scan.pdf"}},
    {type: text, text: "Extract the text from this scanned document."}
  ]}' \
  --transform 'content.#(type=="text").text' --raw-output
```

The CLI detects the file type and encodes binary files as base64 automatically. To force a specific encoding use `@file://` for plain text or `@data://` for base64. Escape a literal leading `@` with a backslash (`\@username`).

## Debugging

Add `--debug` to any command to print the exact HTTP request and response (headers and body) to stderr. API keys are redacted.

```bash
ant --debug beta:agents list
```

```text Output wrap
GET /v1/agents?beta=true HTTP/1.1
Host: api.anthropic.com
Anthropic-Beta: managed-agents-2026-04-01
Anthropic-Version: 2023-06-01
X-Api-Key: <REDACTED>
...
```

## Available resources

Every API resource the CLI exposes is documented in the [API reference](https://platform.claude.com/docs/en/api/cli/messages/create). For a local listing, run `ant --help`, and append `--help` to any subcommand for its flags and parameters.

## Next steps

<CardGroup cols={3}>
  <Card title="CLI scripting and automation" icon="code" href="https://platform.claude.com/docs/en/cli-sdks-libraries/cli/scripting">
    Version-control API resources, scripting patterns, and use from Claude Code
  </Card>

  <Card title="API reference" icon="book" href="https://platform.claude.com/docs/en/api/cli/messages/create">
    Endpoint-specific parameters, request fields, and response schemas
  </Card>

  <Card title="CLI authentication options" icon="lock" href="https://platform.claude.com/docs/en/cli-sdks-libraries/cli/authentication">
    API keys, headless hosts, multiple workspaces, and named profiles
  </Card>
</CardGroup>
