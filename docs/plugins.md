> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Create plugins

> Create custom plugins to extend Claude Code with skills, agents, hooks, and MCP servers.

Plugins let you extend Claude Code with custom functionality that can be shared across projects and teams. This guide covers creating your own plugins with skills, agents, hooks, and MCP servers.

Looking to install existing plugins? See [Discover and install plugins](/docs/en/discover-plugins). For complete technical specifications, see [Plugins reference](/docs/en/plugins-reference).

## When to use plugins vs standalone configuration

Claude Code supports two ways to add custom skills, agents, and hooks:

| Approach                                                                                                        | Skill names          | Best for                                                                                        |
| :-------------------------------------------------------------------------------------------------------------- | :------------------- | :---------------------------------------------------------------------------------------------- |
| **Standalone** (`.claude/` directory)                                                                           | `/hello`             | Personal workflows, project-specific customizations, quick experiments                          |
| **Plugins** (self-contained directories with skills, agents, hooks, or a `.claude-plugin/plugin.json` manifest) | `/plugin-name:hello` | Sharing with teammates, distributing to community, versioned releases, reusable across projects |

<Tip>
  Start with standalone configuration in `.claude/` for quick iteration, then [convert to a plugin](#convert-existing-configurations-to-plugins) when you're ready to share.
</Tip>

## Quickstart

This quickstart walks you through creating a plugin with a custom skill. You'll create a manifest (the configuration file that defines your plugin), add a skill, and test it locally using the `--plugin-dir` flag.

### Prerequisites

* Claude Code [installed and authenticated](/docs/en/quickstart#step-1-install-claude-code)

### Create your first plugin

<Steps>
  <Step title="Create the plugin directory">
    Every plugin lives in its own directory containing your skills, agents, or hooks, optionally alongside a `.claude-plugin/plugin.json` manifest. The location doesn't matter for this quickstart because you'll point Claude Code at the directory with `--plugin-dir` in the test step. Create it anywhere convenient, such as a scratch folder or a projects directory:

    ```bash theme={null}
    mkdir my-first-plugin
    ```

    The remaining steps run from the parent directory and reference paths like `my-first-plugin/...` relative to it.
  </Step>

  <Step title="Create the plugin manifest">
    The manifest file at `.claude-plugin/plugin.json` defines your plugin's identity: its name, description, and version. Claude Code uses this metadata to display your plugin in the plugin manager.

    Create the `.claude-plugin` directory inside your plugin folder:

    ```bash theme={null}
    mkdir my-first-plugin/.claude-plugin
    ```

    Then create `my-first-plugin/.claude-plugin/plugin.json` with this content:

    ```json my-first-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "my-first-plugin",
      "description": "A greeting plugin to learn the basics",
      "version": "1.0.0",
      "author": {
        "name": "Your Name"
      }
    }
    ```

    | Field         | Purpose                                                                                                                                                                                                                                                                                                                                    |
    | :------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `name`        | Unique identifier and skill namespace. Skills are prefixed with this (e.g., `/my-first-plugin:hello`).                                                                                                                                                                                                                                     |
    | `description` | Shown in the plugin manager when browsing or installing plugins.                                                                                                                                                                                                                                                                           |
    | `version`     | Optional. If set, users only receive updates when you bump this field, except for a [`command` source](/docs/en/plugin-marketplaces#command-sources); see [version management](/docs/en/plugins-reference#version-management). If omitted, the version comes from the next source in [version management](/docs/en/plugins-reference#version-management). |
    | `author`      | Optional. Helpful for attribution.                                                                                                                                                                                                                                                                                                         |

    For additional fields like `homepage`, `repository`, and `license`, see the [full manifest schema](/docs/en/plugins-reference#plugin-manifest-schema).
  </Step>

  <Step title="Add a skill">
    Skills live in the `skills/` directory. Each skill is a folder containing a `SKILL.md` file. The folder name becomes the skill name, prefixed with the plugin's namespace (`hello/` in a plugin named `my-first-plugin` creates `/my-first-plugin:hello`).

    Create a skill directory in your plugin folder:

    ```bash theme={null}
    mkdir -p my-first-plugin/skills/hello
    ```

    Then create `my-first-plugin/skills/hello/SKILL.md` with this content:

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    description: Greet the user with a friendly message
    disable-model-invocation: true
    ---

    Greet the user warmly and ask how you can help them today.
    ```
  </Step>

  <Step title="Test your plugin">
    Run Claude Code with the `--plugin-dir` flag to load your plugin:

    ```bash theme={null}
    claude --plugin-dir ./my-first-plugin
    ```

    Once Claude Code starts, try your new skill:

    ```shell theme={null}
    /my-first-plugin:hello
    ```

    You'll see Claude respond with a greeting. Run `/help` and open the **Custom commands** tab to see your skill listed under the plugin namespace.

    <Note>
      **Why namespacing?** Plugin skills are always namespaced (like `/my-first-plugin:hello`) to prevent conflicts when multiple plugins have skills with the same name.

      To change the namespace prefix, update the `name` field in `plugin.json`.
    </Note>
  </Step>

  <Step title="Add skill arguments">
    Make your skill dynamic by accepting user input. The `$ARGUMENTS` placeholder captures any text the user provides after the skill name.

    Update your `SKILL.md` file:

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    description: Greet the user with a personalized message
    ---

    # Hello Skill

    Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.
    ```

    Run `/reload-plugins` to pick up the changes. The skills count in the summary covers only `commands/` directories, so it can report `0 skills` even though the skill you just edited reloaded. Then try the skill with your name:

    ```shell theme={null}
    /my-first-plugin:hello Alex
    ```

    Claude will greet you by name. For more on passing arguments to skills, see [Skills](/docs/en/skills#pass-arguments-to-skills).
  </Step>
</Steps>

<Tip>
  The `--plugin-dir` flag is useful for development and testing. When you're ready to share your plugin with others, see [Create and distribute a plugin marketplace](/docs/en/plugin-marketplaces).
</Tip>

## Develop a plugin in your skills directory

Instead of passing `--plugin-dir` on every launch, you can keep a plugin in your skills directory and have Claude Code load it automatically. `claude plugin init` scaffolds one:

```bash theme={null}
claude plugin init my-tool
```

This creates `~/.claude/skills/my-tool/` with a `.claude-plugin/plugin.json` manifest and a starter `SKILL.md`. On the next session it loads as `my-tool@skills-dir` with no marketplace or install step.

For the auto-load rules, personal vs. project scope, the workspace-trust requirement, and how to update or remove one, see [Skills-directory plugins](/docs/en/plugins-reference#skills-directory-plugins).

## Plugin structure overview

You've created a plugin with a skill, but plugins can include much more: custom agents, hooks, MCP servers, LSP servers, and background monitors.

<Warning>
  **Common mistake**: Don't put `commands/`, `agents/`, `skills/`, or `hooks/` inside the `.claude-plugin/` directory. Only `plugin.json` goes inside `.claude-plugin/`. All other directories must be at the plugin root level.

  The plugin root is the individual plugin's own directory: the one you pass to `--plugin-dir` or that contains `.claude-plugin/plugin.json`. It is never `~/.claude/`. For example, Claude Code doesn't read a `.mcp.json` placed at `~/.claude/.mcp.json`.
</Warning>

| Directory         | Location    | Purpose                                                                                                                                                                                                                                                     |
| :---------------- | :---------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.claude-plugin/` | Plugin root | Contains `plugin.json` manifest (optional if components use default locations)                                                                                                                                                                              |
| `skills/`         | Plugin root | Skills as `<name>/SKILL.md` directories                                                                                                                                                                                                                     |
| `commands/`       | Plugin root | Skills as flat Markdown files. Use `skills/` for new plugins                                                                                                                                                                                                |
| `agents/`         | Plugin root | Custom agent definitions                                                                                                                                                                                                                                    |
| `hooks/`          | Plugin root | Event handlers in `hooks.json`                                                                                                                                                                                                                              |
| `.mcp.json`       | Plugin root | MCP server configurations                                                                                                                                                                                                                                   |
| `.lsp.json`       | Plugin root | LSP server configurations for code intelligence                                                                                                                                                                                                             |
| `monitors/`       | Plugin root | Background monitor configurations in `monitors.json`                                                                                                                                                                                                        |
| `bin/`            | Plugin root | Executables added to the Bash tool's `PATH` while the plugin is enabled. You can't include this directory in a plugin you [distribute through claude.ai organization settings](/docs/en/plugin-marketplaces#keep-executables-out-of-the-top-level-bin-directory) |
| `settings.json`   | Plugin root | Default [settings](/docs/en/settings) applied when the plugin is enabled                                                                                                                                                                                         |

A plugin that ships exactly one skill can place `SKILL.md` directly at the plugin root instead of creating a `skills/` directory. Claude Code loads it as a single skill and uses the frontmatter `name` field for the invocation name. Use the `skills/` layout for plugins that may grow to more than one skill.

## Develop more complex plugins

Once you're comfortable with basic plugins, you can create more sophisticated extensions.

### Add Skills to your plugin

Plugins can include [Agent Skills](/docs/en/skills) to extend Claude's capabilities. Skills are model-invoked: Claude automatically uses them based on the task context.

Add a `skills/` directory at your plugin root with Skill folders containing `SKILL.md` files:

```text theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── code-review/
        └── SKILL.md
```

Each `SKILL.md` contains YAML frontmatter and instructions. Include a `description` so Claude knows when to use the skill:

```yaml theme={null}
---
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

After you install the plugin, check the install summary: if it reports `Run /reload-plugins to activate.`, run that command to load the Skills. For complete Skill authoring guidance including progressive disclosure and tool restrictions, see [Agent Skills](/docs/en/skills).

### Add LSP servers to your plugin

<Tip>
  For common languages like TypeScript, Python, and Rust, install the pre-built LSP plugins from the official marketplace. Create custom LSP plugins only when you need support for languages not already covered.
</Tip>

LSP (Language Server Protocol) plugins give Claude real-time code intelligence. If you need to support a language that doesn't have an official LSP plugin, you can create your own by adding an `.lsp.json` file to your plugin:

```json .lsp.json theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

Users installing your plugin must have the language server binary installed on their machine.

To confirm the server starts, launch Claude Code with the plugin enabled and check the `/plugin` Errors tab: a language server that fails to start appears there, for example with `Executable not found in $PATH` when the binary isn't installed. An entry with an invalid configuration is skipped instead; run `claude --debug` to see why.

For complete LSP configuration options, see [LSP servers](/docs/en/plugins-reference#lsp-servers).

### Add background monitors to your plugin

Background monitors let your plugin watch logs, files, or external status in the background and notify Claude as events arrive. Claude Code starts each monitor automatically when the plugin is active, so you don't need to instruct Claude to start the watch.

Add a `monitors/monitors.json` file at the plugin root with an array of monitor entries:

```json monitors/monitors.json theme={null}
[
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log"
  }
]
```

Each stdout line from `command` is delivered to Claude as a notification during the session. For the full schema, including the `when` trigger and variable substitution, see [Monitors](/docs/en/plugins-reference#monitors).

### Ship default settings with your plugin

Plugins can include a `settings.json` file at the plugin root to apply default configuration when the plugin is enabled. Currently, only the `agent` and `subagentStatusLine` keys are supported.

Setting `agent` activates one of the plugin's [custom agents](/docs/en/sub-agents) as the main thread, applying its system prompt, tool restrictions, and model. This lets a plugin change how Claude Code behaves by default when enabled.

```json settings.json theme={null}
{
  "agent": "security-reviewer"
}
```

This example activates the `security-reviewer` agent defined in the plugin's `agents/` directory. Settings from `settings.json` take priority over `settings` declared in `plugin.json`. Unknown keys are silently ignored.

### Organize complex plugins

For plugins with many components, organize your directory structure by functionality. For complete directory layouts and organization patterns, see [Plugin directory structure](/docs/en/plugins-reference#plugin-directory-structure).

### Test your plugins locally

Use the `--plugin-dir` flag to test plugins during development. This loads your plugin directly without requiring installation.

```bash theme={null}
claude --plugin-dir ./my-plugin
```

The flag also accepts a `.zip` archive of the plugin directory.

```bash theme={null}
claude --plugin-dir ./my-plugin.zip
```

When a `--plugin-dir` plugin has the same name as an installed marketplace plugin, the local copy takes precedence for that session. This lets you test changes to a plugin you already have installed without uninstalling it first. The exception is plugins that managed settings force-enable or force-disable: `--plugin-dir` cannot override those.

As you make changes to your plugin, run `/reload-plugins` to pick up the updates without restarting. This reloads plugins, skills, agents, hooks, plugin MCP servers, and plugin LSP servers. Test your plugin components:

* Try your skills with `/plugin-name:skill-name`
* Check that agents appear in `/context` under Custom Agents, or @-mention one by its scoped name
* Trigger the event each hook matches, such as asking Claude to edit a file for a `PostToolUse` hook, and confirm its effect. Claude Code records which hooks matched, their exit codes, and their output in the [debug log](/docs/en/hooks#debug-hooks)

<Tip>
  You can load multiple plugins at once by specifying the flag multiple times:

  ```bash theme={null}
  claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
  ```
</Tip>

To test a plugin that is already packaged as a `.zip` archive and hosted at a URL, such as a CI build artifact, use `--plugin-url` instead. Claude Code fetches the archive at startup and loads it for that session only. If Claude Code can't fetch the archive, or the archive is invalid, it starts without the plugin and records a plugin load error that you can review in the `/plugin` manager's **Errors** tab. The same [trust considerations](/docs/en/discover-plugins#security) apply as for any plugin source: only point this flag at archives you control or trust.

To load multiple plugins, repeat the flag for each URL:

```bash theme={null}
claude --plugin-url https://example.com/my-plugin.zip --plugin-url https://example.com/other.zip
```

Or pass space-separated URLs as one quoted argument:

```bash theme={null}
claude --plugin-url "https://example.com/my-plugin.zip https://example.com/other.zip"
```

### Debug plugin issues

If your plugin isn't working as expected:

1. **Check the structure**: Ensure your directories are at the plugin root, not inside `.claude-plugin/`
2. **Test components individually**: Check each skill, agent, and hook separately
3. **Use validation and debugging tools**: See [Debugging and development tools](/docs/en/plugins-reference#debugging-and-development-tools) for CLI commands and troubleshooting techniques

### Share your plugins

When your plugin is ready to share:

1. **Add documentation**: Include a `README.md` with installation and usage instructions
2. **Choose a versioning strategy**: Decide whether to set an explicit `version` or rely on the fallback described in [version management](/docs/en/plugins-reference#version-management).
3. **Create or use a marketplace**: Distribute through [plugin marketplaces](/docs/en/plugin-marketplaces) for installation
4. **Test with others**: Have team members test the plugin before wider distribution

Once your plugin is in a marketplace, others can install it using the instructions in [Discover and install plugins](/docs/en/discover-plugins). To keep a plugin internal to your team, host the marketplace in a [private repository](/docs/en/plugin-marketplaces#private-repositories).

### Submit your plugin to the community marketplace

Anthropic maintains two public marketplaces for Claude Code plugins:

* **`claude-plugins-official`**: a curated set of plugins maintained by Anthropic. Claude Code registers it automatically the first time you start Claude Code interactively. If you run Claude Code non-interactively before that first interactive launch, or a [marketplace policy](/docs/en/plugin-marketplaces#managed-marketplace-restrictions) blocked an earlier attempt, register it yourself with `claude plugin marketplace add anthropics/claude-plugins-official`.
* **`claude-community`**: the public community marketplace where third-party submissions land after review. Users add it with `/plugin marketplace add anthropics/claude-plugins-community` and install from it as `@claude-community`.

To submit your plugin for community-marketplace review, use one of the in-app forms:

* **claude.ai**: [claude.ai/admin-settings/directory/submissions/plugins/new](https://claude.ai/admin-settings/directory/submissions/plugins/new)
* **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

The claude.ai form requires a Team or Enterprise organization and directory management access; organization Owners have this access by default. Individual authors who aren't part of a Team or Enterprise organization can use the Console form instead.

Run `claude plugin validate ./your-plugin` locally before you submit, replacing `./your-plugin` with the path to your plugin directory. The review pipeline runs the same check on every submission, along with automated safety screening. When validation passes, Claude Code prints `✔ Validation passed`, or `✔ Validation passed with warnings` if there are warnings. Warnings don't fail validation; add `--strict` to treat them as errors.

Approved plugins are pinned to a specific commit SHA in the [`anthropics/claude-plugins-community`](https://github.com/anthropics/claude-plugins-community) catalog, and CI bumps the pin automatically as you push new commits to your repository. The public catalog syncs nightly from the review pipeline, so there can be a delay between approval and your plugin appearing in `marketplace.json`. To check whether your plugin is installable yet, search for its name in the [community catalog](https://github.com/anthropics/claude-plugins-community/blob/main/.claude-plugin/marketplace.json).

The official marketplace, `claude-plugins-official`, is curated separately. Anthropic decides which plugins to include at its discretion. There is no application process, and the submission form does not add plugins to the official marketplace.

If Anthropic lists your plugin in the official marketplace, your CLI can prompt Claude Code users to install it. See [Recommend your plugin from your CLI](/docs/en/plugin-hints).

## Convert existing configurations to plugins

If you already have skills or hooks in your `.claude/` directory, you can convert them into a plugin for easier sharing and distribution.

### Migration steps

<Steps>
  <Step title="Create the plugin structure">
    Create a new plugin directory in your project root, alongside the existing `.claude/` folder, so the relative `cp` paths in the next step resolve:

    ```bash theme={null}
    mkdir -p my-plugin/.claude-plugin
    ```

    Create the manifest file at `my-plugin/.claude-plugin/plugin.json`:

    ```json my-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "my-plugin",
      "description": "Migrated from standalone configuration",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Copy your existing files">
    Copy each configuration directory you have to the plugin root. You might not have all three: if a directory doesn't exist, `cp` prints `No such file or directory` and copies nothing, so skip that command or ignore the error.

    ```bash theme={null}
    cp -r .claude/commands my-plugin/

    cp -r .claude/agents my-plugin/

    cp -r .claude/skills my-plugin/
    ```

    Your plugin now contains copies of the directories you had under `.claude/`. Run `ls my-plugin` to confirm: you should see each directory you copied.
  </Step>

  <Step title="Migrate hooks">
    If you have hooks in your settings, create a hooks directory:

    ```bash theme={null}
    mkdir my-plugin/hooks
    ```

    Create `my-plugin/hooks/hooks.json` with your hooks configuration. Copy the `hooks` object from your `.claude/settings.json` or `settings.local.json`, since the format is the same. The command receives hook input as JSON on stdin, so use `jq` to extract the file path:

    ```json my-plugin/hooks/hooks.json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }]
          }
        ]
      }
    }
    ```
  </Step>

  <Step title="Test your migrated plugin">
    Load your plugin to verify everything works:

    ```bash theme={null}
    claude --plugin-dir ./my-plugin
    ```

    Test each component: run your commands, check that agents appear in `/context`, and trigger the event each hook matches to confirm its effect. Claude Code records which hooks matched and how they exited in the [debug log](/docs/en/hooks#debug-hooks).
  </Step>
</Steps>

### What changes when migrating

| Standalone (`.claude/`)       | Plugin                           |
| :---------------------------- | :------------------------------- |
| Only available in one project | Can be shared via marketplaces   |
| Files in `.claude/commands/`  | Files in `plugin-name/commands/` |
| Hooks in `settings.json`      | Hooks in `hooks/hooks.json`      |
| Must manually copy to share   | Install with `/plugin install`   |

<Note>
  After migrating, remove the original files from `.claude/` to avoid duplicates. Project and user `.claude/agents/` definitions override same-named plugin agents, so the plugin version only takes effect once the originals are removed. Plugin skills are namespaced as `/plugin-name:skill-name`, so the original `/skill-name` and the plugin copy both remain available rather than one overriding the other.
</Note>

## Next steps

Now that you understand Claude Code's plugin system, here are suggested paths for different goals:

### For plugin users

* [Discover and install plugins](/docs/en/discover-plugins): browse marketplaces and install plugins
* [Configure team marketplaces](/docs/en/discover-plugins#configure-team-marketplaces): set up repository-level plugins for your team

### For plugin developers

* [Create and distribute a marketplace](/docs/en/plugin-marketplaces): package and share your plugins
* [Plugins reference](/docs/en/plugins-reference): complete technical specifications
* Dive deeper into specific plugin components:
  * [Skills](/docs/en/skills): skill development details
  * [Subagents](/docs/en/sub-agents): agent configuration and capabilities
  * [Hooks](/docs/en/hooks): event handling and automation
  * [MCP](/docs/en/mcp): external tool integration
