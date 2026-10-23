> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 19 · May 4–8, 2026

> Load plugins from .zip archives and URLs, search command history across every project with Ctrl+R, branch new worktrees from local HEAD or the remote default, and block actions unconditionally with auto mode hard deny rules.

Releases [v2.1.128 → v2.1.136](https://code.claude.com/docs/en/changelog.md#2-1-128)
2 features · May 4–8

Plugins from .zip archives and URLs

`--plugin-dir` now accepts a `.zip` plugin archive in addition to a directory, and the new `--plugin-url` flag fetches a plugin archive from a URL for the current session. Useful for trying a plugin before adding it to a marketplace, or for shipping internal plugins from an artifact store.

Load a plugin straight from a URL:

```bash terminal theme={null}
claude --plugin-url https://example.com/my-plugin.zip
```

[Plugins guide](https://code.claude.com/docs/en/plugins/overview.md)

History search across all your projects
v2.1.129

`Ctrl+R` reverse-search now defaults to all prompts across every project, restoring the behavior from before v2.1.124. Press `Ctrl+S` while searching to narrow back to the current project or session. Handy when you remember a command you ran in another repo last week and don't want to go digging for it.

[Interactive mode: command history](https://code.claude.com/docs/en/interactive-mode.md#command-history)

Other wins

New `worktree.baseRef` setting (`fresh` | `head`) controls whether `--worktree`, the `EnterWorktree` tool, and agent-isolation worktrees branch from the remote default branch or local `HEAD`; the default `fresh` keeps unpushed commits out of new worktreesNew `settings.autoMode.hard_deny` rules block matching actions unconditionally in auto mode, regardless of allow exceptions, for actions that should never run automatically even when broader allow rules applyHooks now receive the active effort level via the `effort.level` JSON input field and the `$CLAUDE_EFFORT` environment variable, and Bash tool commands can read `$CLAUDE_EFFORT``CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` opts out of the fullscreen alternate-screen renderer and keeps the conversation in the terminal's native scrollback`CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE` lets Homebrew or WinGet installations run the upgrade in the background and prompt to restart`CLAUDE_CODE_SESSION_ID` is now in the Bash tool subprocess environment, matching the `session_id` passed to hooks`/mcp` now shows the tool count for connected servers and flags servers that connected with 0 tools`--channels` now works with console (API key) authenticationSubprocesses such as Bash, hooks, MCP, and LSP no longer inherit `OTEL_*` environment variables, so OTEL-instrumented apps run via the Bash tool no longer pick up the CLI's own OTLP endpointSub-agent progress summaries now hit the prompt cache, cutting `cache_creation` token cost by roughly 3xSeveral OAuth and credential reliability fixes: parallel sessions no longer dead-end at 401 after a refresh-token race, MCP OAuth refresh tokens are no longer lost when multiple servers refresh concurrently, and a rare login loop from a concurrent credential write is fixedNew `parentSettingsBehavior` admin key lets admins opt SDK `managedSettings` into the policy merge

[Full changelog for v2.1.128–v2.1.136 →](https://code.claude.com/docs/en/changelog.md#2-1-128)
