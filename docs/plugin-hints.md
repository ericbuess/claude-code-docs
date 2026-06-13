> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Recommend your plugin from your CLI

> Emit a one-line marker from your CLI so Claude Code prompts users to install your official plugin.

If you maintain a CLI or SDK and have a plugin in the official Anthropic marketplace, your tool can prompt Claude Code users to install that plugin. Your CLI writes a one-line marker to stderr when it detects it is running inside Claude Code. Claude Code reads the marker, strips it from the output, and shows the user a one-time install prompt.

Claude Code strips the hint line from the command output before sending it to the model, so the marker never appears in the conversation and is not counted toward token usage. The protocol requires no extra commands and does not change what your CLI prints for users outside Claude Code.

This page is for CLI and SDK maintainers. If you are looking to install plugins, see [Discover and install plugins](/en/discover-plugins).

## How it works

Claude Code sets the [`CLAUDECODE`](/en/env-vars) environment variable to `1` for every command it runs through the Bash and PowerShell tools, and for [hook](/en/hooks) commands. {/* min-version: 2.1.172 */}From v2.1.172 it also sets [`CLAUDE_CODE_CHILD_SESSION`](/en/env-vars) to `1` in those same subprocesses. When your CLI sees one of these variables, it writes a self-closing `<claude-code-hint />` tag to stderr. In hook commands the hint tag is stripped and ignored. Only Bash and PowerShell tool output triggers the install prompt.

When Claude Code receives the command output, it:

1. Scans for hint lines and removes them before the output reaches the model
2. Checks that the hint targets a plugin in an official Anthropic marketplace
3. Checks that the plugin is not already installed and has not been prompted before
4. Shows the user an install prompt that names the command that emitted the hint

Claude Code never installs a plugin automatically. The user always confirms.

## Emit the hint

Gate emission on an environment variable so the marker is unlikely to appear when a human runs your CLI directly, then write the tag to stderr on its own line. Choose which variable to check:

* `CLAUDECODE`: set on every Claude Code version, so it reaches the most sessions. It is also set in tmux sessions and stdio MCP server subprocesses that Claude Code starts, and IDE extensions set it in their integrated terminals, where a human may be running your CLI directly.
* {/* min-version: 2.1.172 */}`CLAUDE_CODE_CHILD_SESSION`: set only in subprocesses Claude Code itself spawns, such as tool calls, hook commands, and [status line](/en/statusline) commands, so the tag does not normally reach a human terminal. A long-lived process that was started inside a session, such as a tmux server, captures the variable, so shells later launched from that process still show the raw tag. Requires Claude Code v2.1.172 or later, so sessions on older versions miss the hint.

The following examples gate on `CLAUDECODE` for maximum reach and emit a hint for a plugin named `example-cli` in the official marketplace:

<CodeGroup>
  ```javascript Node.js theme={null}
  if (process.env.CLAUDECODE) {
    process.stderr.write(
      '<claude-code-hint v="1" type="plugin" value="example-cli@claude-plugins-official" />\n',
    )
  }
  ```

  ```python Python theme={null}
  import os, sys

  if os.environ.get("CLAUDECODE"):
      print(
          '<claude-code-hint v="1" type="plugin" value="example-cli@claude-plugins-official" />',
          file=sys.stderr,
      )
  ```

  ```go Go theme={null}
  if os.Getenv("CLAUDECODE") != "" {
      fmt.Fprintln(os.Stderr,
          `<claude-code-hint v="1" type="plugin" value="example-cli@claude-plugins-official" />`)
  }
  ```

  ```shell Shell theme={null}
  [ -n "$CLAUDECODE" ] &&
    printf '%s\n' '<claude-code-hint v="1" type="plugin" value="example-cli@claude-plugins-official" />' >&2
  ```
</CodeGroup>

Replace `example-cli` with your plugin's name in the official marketplace.

## Choose where to emit

You control which code paths emit the hint. Claude Code deduplicates by plugin, so emitting on every invocation has no downside. Touchpoints that work well include:

| Placement                 | Why it works                                               |
| :------------------------ | :--------------------------------------------------------- |
| `--help` output           | Claude often runs help when exploring an unfamiliar CLI    |
| Unknown-subcommand errors | Reaches the moment Claude is confused about your interface |
| Login or auth success     | The user is already in a setup mindset                     |
| First-run welcome message | A natural onboarding moment                                |

## What the user sees

When the hint passes all checks, Claude Code shows a prompt like the following:

```text theme={null}
─────────────────────────────────────────────────────────────
  Plugin recommendation

    The example-cli command suggests installing a plugin.

    Plugin: example-cli
    Marketplace: claude-plugins-official
    Official integration for example-cli deployments

    Would you like to install it?
    ❯ 1. Yes, install example-cli
      2. No
      3. No, and don't show plugin installation hints again

─────────────────────────────────────────────────────────────
```

The prompt names the command that produced the hint so users can spot a mismatch between the tool and the plugin it recommends. If the user does not respond within 30 seconds, the prompt dismisses as **No**.

Prompt frequency is bounded:

* **Once per plugin**: after the prompt is shown, Claude Code records the plugin and never prompts for it again, regardless of the user's answer.
* **Once per session**: across all CLIs on the machine, at most one hint prompt appears per Claude Code session.

Selecting **Yes** installs the plugin to user scope. Selecting **No, and don't show plugin installation hints again** disables all future hint prompts for the user.

## Hint format

The hint is a self-closing tag with three required attributes.

```text theme={null}
<claude-code-hint v="1" type="plugin" value="example-cli@claude-plugins-official" />
```

| Attribute | Required | Description                                       |
| :-------- | :------- | :------------------------------------------------ |
| `v`       | Yes      | Protocol version. `1` is the only supported value |
| `type`    | Yes      | Hint kind. `plugin` is the only supported value   |
| `value`   | Yes      | Plugin identifier in `name@marketplace` form      |

Attribute values may be quoted with double quotes or left unquoted. Unquoted values cannot contain whitespace. Escape sequences are not supported.

## Requirements

Claude Code enforces two conditions before acting on a hint. Hints that fail either check are dropped:

* **Own line**: the tag must occupy its own line. A tag embedded mid-line, for example inside a log statement, is ignored. Leading and trailing whitespace on the line is allowed.
* **Official marketplace**: the `value` must reference a plugin in an Anthropic-controlled marketplace such as `claude-plugins-official`. Hints that point to other marketplaces are silently dropped.

The hint line is always removed from the output before it reaches the model, even when the version or type is unrecognized, so the marker is never counted toward token usage.

The remaining guidance is recommended but not enforced. Claude Code cannot observe whether your CLI follows it:

* **Write to stderr**: stderr keeps the tag out of shell pipelines such as `example-cli deploy | jq`. Claude Code scans both streams, so stdout also works.
* **Gate on an environment variable**: only emit when `CLAUDECODE` or `CLAUDE_CODE_CHILD_SESSION` is set. See [Emit the hint](#emit-the-hint) for how the two variables differ.

## Get your plugin into the official marketplace

The hint protocol only takes effect for plugins listed in the official Anthropic marketplace, `claude-plugins-official`. Anthropic curates that marketplace at its discretion, and the in-app submission forms add plugins to the [community marketplace](/en/plugins#submit-your-plugin-to-the-community-marketplace) instead, which the hint protocol does not check. If you are working with an Anthropic partner contact, reach out to them to coordinate an official-marketplace listing.

## See also

* [Create plugins](/en/plugins): build the plugin your CLI recommends
* [Create and distribute a plugin marketplace](/en/plugin-marketplaces): host plugins outside the official marketplace
* [Environment variables](/en/env-vars): full reference for `CLAUDECODE` and related variables
