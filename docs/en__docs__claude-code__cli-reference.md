# CLI reference

> Complete reference for Claude Code command-line interface, including commands and flags.

## CLI commands

| Command                            | Description                                    | Example                                           |
| :--------------------------------- | :--------------------------------------------- | :------------------------------------------------ |
| `claude`                           | Start interactive REPL                         | `claude`                                          |
| `claude "query"`                   | Start REPL with initial prompt                 | `claude "explain this project"`                   |
| `claude -p "query"`                | Query via SDK, then exit                       | `claude -p "explain this function"`               |
| `cat file \| claude -p "query"`    | Process piped content                          | `cat logs.txt \| claude -p "explain"`             |
| `claude -c`                        | Continue most recent conversation              | `claude -c`                                       |
| `claude -c -p "query"`             | Continue via SDK                               | `claude -c -p "Check for type errors"`            |
| `claude -r "<session-id>" "query"` | Resume session by ID                           | `claude -r "abc123" "Finish this PR"`             |
| `claude update`                    | Update to latest version                       | `claude update`                                   |
| `claude mcp`                       | Configure Model Context Protocol (MCP) servers | See the [Claude Code MCP documentation](/en/mcp). |

## CLI flags

Customize Claude Code's behavior with these command-line flags:

| Flag                             | Description                                                                                                                                | Example                                                                                            |
| :------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `--add-dir`                      | Add additional working directories for Claude to access (validates each path exists as a directory)                                        | `claude --add-dir ../apps ../lib`                                                                  |
| `--agents`                       | Define custom [subagents](/en/sub-agents) dynamically via JSON (see below for format)                                                      | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allowedTools`                 | A list of tools that should be allowed without prompting the user for permission, in addition to [settings.json files](/en/settings)       | `"Bash(git log:*)" "Bash(git diff:*)" "Read"`                                                      |
| `--disallowedTools`              | A list of tools that should be disallowed without prompting the user for permission, in addition to [settings.json files](/en/settings)    | `"Bash(git log:*)" "Bash(git diff:*)" "Edit"`                                                      |
| `--print`, `-p`                  | Print response without interactive mode (see [SDK documentation](https://docs.claude.com/en/api/agent-sdk) for programmatic usage details) | `claude -p "query"`                                                                                |
| `--system-prompt`                | Replace the entire system prompt with custom text (works in both interactive and print modes; added in v2.0.14)                            | `claude --system-prompt "You are a Python expert"`                                                 |
| `--system-prompt-file`           | Load system prompt from a file, replacing the default prompt (print mode only; added in v1.0.54)                                           | `claude -p --system-prompt-file ./custom-prompt.txt "query"`                                       |
| `--append-system-prompt`         | Append custom text to the end of the default system prompt (works in both interactive and print modes; added in v1.0.55)                   | `claude --append-system-prompt "Always use TypeScript"`                                            |
| `--output-format`                | Specify output format for print mode (options: `text`, `json`, `stream-json`)                                                              | `claude -p "query" --output-format json`                                                           |
| `--input-format`                 | Specify input format for print mode (options: `text`, `stream-json`)                                                                       | `claude -p --output-format json --input-format stream-json`                                        |
| `--include-partial-messages`     | Include partial streaming events in output (requires `--print` and `--output-format=stream-json`)                                          | `claude -p --output-format stream-json --include-partial-messages "query"`                         |
| `--verbose`                      | Enable verbose logging, shows full turn-by-turn output (helpful for debugging in both print and interactive modes)                         | `claude --verbose`                                                                                 |
| `--max-turns`                    | Limit the number of agentic turns in non-interactive mode                                                                                  | `claude -p --max-turns 3 "query"`                                                                  |
| `--model`                        | Sets the model for the current session with an alias for the latest model (`sonnet` or `opus`) or a model's full name                      | `claude --model claude-sonnet-4-5-20250929`                                                        |
| `--permission-mode`              | Begin in a specified [permission mode](/en/iam#permission-modes)                                                                           | `claude --permission-mode plan`                                                                    |
| `--permission-prompt-tool`       | Specify an MCP tool to handle permission prompts in non-interactive mode                                                                   | `claude -p --permission-prompt-tool mcp_auth_tool "query"`                                         |
| `--resume`                       | Resume a specific session by ID, or by choosing in interactive mode                                                                        | `claude --resume abc123 "query"`                                                                   |
| `--continue`                     | Load the most recent conversation in the current directory                                                                                 | `claude --continue`                                                                                |
| `--dangerously-skip-permissions` | Skip permission prompts (use with caution)                                                                                                 | `claude --dangerously-skip-permissions`                                                            |

<Tip>
  The `--output-format json` flag is particularly useful for scripting and
  automation, allowing you to parse Claude's responses programmatically.
</Tip>

### Agents flag format

The `--agents` flag accepts a JSON object that defines one or more custom subagents. Each subagent requires a unique name (as the key) and a definition object with the following fields:

| Field         | Required | Description                                                                                                     |
| :------------ | :------- | :-------------------------------------------------------------------------------------------------------------- |
| `description` | Yes      | Natural language description of when the subagent should be invoked                                             |
| `prompt`      | Yes      | The system prompt that guides the subagent's behavior                                                           |
| `tools`       | No       | Array of specific tools the subagent can use (e.g., `["Read", "Edit", "Bash"]`). If omitted, inherits all tools |
| `model`       | No       | Model alias to use: `sonnet`, `opus`, or `haiku`. If omitted, uses the default subagent model                   |

Example:

```bash  theme={null}
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

For more details on creating and using subagents, see the [subagents documentation](/en/sub-agents).

### System prompt flags

Claude Code provides three flags for customizing the system prompt, each serving a different purpose:

| Flag                     | Behavior                           | Modes               | Use Case                                                             |
| :----------------------- | :--------------------------------- | :------------------ | :------------------------------------------------------------------- |
| `--system-prompt`        | **Replaces** entire default prompt | Interactive + Print | Complete control over Claude's behavior and instructions             |
| `--system-prompt-file`   | **Replaces** with file contents    | Print only          | Load prompts from files for reproducibility and version control      |
| `--append-system-prompt` | **Appends** to default prompt      | Interactive + Print | Add specific instructions while keeping default Claude Code behavior |

**When to use each:**

* **`--system-prompt`**: Use when you need complete control over Claude's system prompt. This removes all default Claude Code instructions, giving you a blank slate.
  ```bash  theme={null}
  claude --system-prompt "You are a Python expert who only writes type-annotated code"
  ```

* **`--system-prompt-file`**: Use when you want to load a custom prompt from a file, useful for team consistency or version-controlled prompt templates.
  ```bash  theme={null}
  claude -p --system-prompt-file ./prompts/code-review.txt "Review this PR"
  ```

* **`--append-system-prompt`**: Use when you want to add specific instructions while keeping Claude Code's default capabilities intact. This is the safest option for most use cases.
  ```bash  theme={null}
  claude --append-system-prompt "Always use TypeScript and include JSDoc comments"
  ```

<Note>
  `--system-prompt` and `--system-prompt-file` are mutually exclusive. You cannot use both flags simultaneously.
</Note>

<Tip>
  For most use cases, `--append-system-prompt` is recommended as it preserves Claude Code's built-in capabilities while adding your custom requirements. Use `--system-prompt` or `--system-prompt-file` only when you need complete control over the system prompt.
</Tip>

For detailed information about print mode (`-p`) including output formats,
streaming, verbose logging, and programmatic usage, see the
[SDK documentation](https://docs.claude.com/en/api/agent-sdk).

## See also

* [Interactive mode](/en/interactive-mode) - Shortcuts, input modes, and interactive features
* [Slash commands](/en/slash-commands) - Interactive session commands
* [Quickstart guide](/en/quickstart) - Getting started with Claude Code
* [Common workflows](/en/common-workflows) - Advanced workflows and patterns
* [Settings](/en/settings) - Configuration options
* [SDK documentation](https://docs.claude.com/en/api/agent-sdk) - Programmatic usage and integrations
