> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 14 · March 30 – April 3, 2026

> Computer use in the CLI, interactive in-product lessons, flicker-free rendering, per-tool MCP result-size overrides, and plugin executables on PATH.

Releases [v2.1.86 → v2.1.91](/docs/en/changelog.md#2-1-86)
5 features · March 30 – April 3

Computer use in the CLI
research preview

Last week computer use landed in the Desktop app. This week it's in the CLI: Claude can open native apps, click through UI, test its own changes, and fix what breaks, all from your terminal. Web apps already had verification loops; native iOS, macOS, and other GUI-only apps didn't. Now they do. Best for closing the loop on apps and tools where there's no API to call. Still early; expect rough edges.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/cli-computer-use.mp4?fit=max&auto=format&n=CfffsX01JHFnIKvD&q=85&s=c17a337902308d7c9121013ded0494db" />

Requires macOS and a Pro or Max plan; otherwise, `computer-use` won't appear in `/mcp`. Run `/mcp`, find `computer-use`, and toggle it on. Then ask Claude to verify a change end to end:

```text title="Claude Code" wrap theme={null}
Open the iOS simulator, tap through onboarding, and screenshot each step
```

[Computer use guide](/docs/en/computer-use.md)

/powerup
v2.1.90

Interactive lessons that teach Claude Code features through animated demos, right inside your terminal. Claude Code releases frequently, and features that would have changed how you work last month can slip by. Run `/powerup` once and you'll know what's there.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/powerup.mp4?fit=max&auto=format&n=CfffsX01JHFnIKvD&q=85&s=fb88beddc0ecc8029da5ab029e4b28f1" />

Run it:

```text title="Claude Code" wrap theme={null}
/powerup
```

[Commands reference](/docs/en/commands.md)

Flicker-free rendering
v2.1.89

Opt into a new alt-screen renderer with virtualized scrollback. The prompt input stays pinned to the bottom, mouse selection works across long conversations, and the flicker on redraw is gone. Unset `CLAUDE_CODE_NO_FLICKER` to roll back.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/flicker-free.mp4?fit=max&auto=format&n=CfffsX01JHFnIKvD&q=85&s=7719e35e52a3f9734b0cf69edac333ad" />

Set the env var and restart Claude Code:

```bash theme={null}
export CLAUDE_CODE_NO_FLICKER=1
claude
```

[Fullscreen rendering](/docs/en/fullscreen.md)

MCP result-size override
v2.1.91

MCP server authors can now raise the truncation cap on a specific tool by setting `anthropic/maxResultSizeChars` in the tool's `tools/list` entry, up to a hard ceiling of 500K characters. The cap used to be global, so tools that occasionally returned inherently large payloads like database schemas or full file trees hit the default limit and got persisted to disk with a file reference. Per-tool overrides keep those results inline when the tool really needs them.

Annotate the tool in your server's `tools/list` response:

```json highlight={5} theme={null}
{
  "name": "get_schema",
  "description": "Returns the full database schema",
  "_meta": {
    "anthropic/maxResultSizeChars": 500000
  }
}
```

[MCP reference](/docs/en/mcp.md#raise-the-limit-for-a-specific-tool)

Plugin executables on PATH
v2.1.91

Place an executable in a `bin/` directory at your plugin root and Claude Code adds that directory to the Bash tool's `PATH` while the plugin is enabled. Claude can then invoke the binary as a bare command from any Bash tool call, with no absolute path or wrapper script needed. Handy for packaging CLI helpers next to the commands, agents, and hooks that call them.

Add a `bin/` directory at the plugin root:

```text highlight={4, 5} theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── bin/
    └── my-tool
```

[Plugins reference](/docs/en/plugins/manifest-reference.md#standard-layout)

Other wins

Auto mode follow-ups: new `PermissionDenied` hook fires on classifier denials (return `retry: true` to let Claude try a different approach), and `/permissions` → Recently denied lets you retry manually with `r`New `defer` value for `permissionDecision` in `PreToolUse` hooks: `-p` sessions pause at a tool call and exit with a `deferred_tool_use` payload so an SDK app or custom UI can surface it, then resume with `--resume``/buddy`: hatch a small creature that watches you code. An April Fools' joke, no longer available`disableSkillShellExecution` setting blocks inline shell from skills, custom commands, and plugin commandsEdit tool now works on files viewed via `cat` or `sed -n` without a separate ReadHook output over 50K saved to disk with a path + preview instead of injected into contextThinking summaries off by default in interactive sessions (`showThinkingSummaries: true` to restore)Voice mode: push-to-talk modifier combos, Windows WebSocket, macOS Apple Silicon mic permission`claude-cli://` deep links accept multi-line prompts (encoded `%0A`)

[Full changelog for v2.1.86–v2.1.91 →](/docs/en/changelog.md#2-1-86)
