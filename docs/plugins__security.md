> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Plugin security and trust

> Decide whether to trust a plugin before you install it, from what a plugin can do on your machine to how to review one and remove it.

A Claude Code plugin you install can execute arbitrary code on your machine with your user privileges.

You install a plugin from a marketplace, which is the catalog Claude Code fetches it from. Some marketplace names are [reserved for Anthropic's own marketplaces](#marketplace-tiers), and every other marketplace is third-party. A marketplace's name tells you who publishes the catalog, not what each plugin in it does, so [review a plugin before you install it](#review-a-plugin-before-you-install) whichever marketplace it comes from.

Read this page if you're deciding whether to install a plugin, or if you review tools before your team can use them.

<Note>
  These cases are covered on other pages:

  * **Claude Code's own security model**: see [Security](/docs/en/security)
  * **Restricting or requiring plugins for an organization**: see [Manage plugins for your organization](/docs/en/plugins/org)
  * **The `security-guidance` or `claude-security` plugins**: this page isn't about them. See [`security-guidance`](/docs/en/security-guidance) and [`claude-security`](/docs/en/claude-security)
</Note>

Start with [what a plugin can do](#understand-what-a-plugin-can-do) and [which marketplaces are Anthropic's](#marketplace-tiers), then [review the plugin before you install it](#review-a-plugin-before-you-install).

## Understand what a plugin can do

A plugin can carry content that runs code on your machine with your user privileges and content that enters Claude's context as instructions, so [review a plugin before you install it](#review-a-plugin-before-you-install). Here's what an installed plugin can do:

* **Hooks**: a plugin's [hooks](/docs/en/hooks) run as shell commands at points in Claude Code's lifecycle, such as before or after a tool call.
* **MCP and LSP servers**: Claude Code connects to the [MCP servers](/docs/en/mcp) an enabled plugin declares and gives Claude their tools. A stdio MCP server runs as a process that Claude Code starts on your machine. Claude Code also starts the language servers the plugin declares.
* **`bin/` directory**: Claude Code adds each enabled plugin's `bin/` directory to the `PATH` of the Bash tool's shell, so Claude's Bash commands can run any executable there.
* **Skills, commands, and agents**: these enter Claude's context as instructions, so they influence what Claude does with the tools it already has.
* **Updates**: when auto-update is on for the marketplace you installed a plugin from, Claude Code updates that plugin in the background, so the files you reviewed can change on disk. [When auto-update runs](/docs/en/plugins/loading#when-auto-update-runs) has the timing. To turn auto-update on or off per marketplace, see [Keep plugins updated](/docs/en/plugins/install#keep-plugins-updated).

Claude Code's [permission rules](/docs/en/permissions) and [sandbox](/docs/en/sandboxing) cover the tool calls Claude makes, not the code a plugin runs by itself:

* **Hooks and server processes**: command hooks execute shell commands with your full user permissions. Claude Code runs hooks and MCP servers outside the sandbox.
* **Claude's tool calls**: a call to one of the plugin's MCP tools, and a Bash command that runs an executable from the plugin's `bin/`, are tool calls, so your permission rules apply to them.

Installing a plugin also enables it, unless its manifest or marketplace entry sets [`defaultEnabled: false`](/docs/en/plugins/install#choose-an-install-scope) and you haven't enabled it yourself.

To remove a plugin you no longer trust, see [Remove a plugin you no longer trust](#remove-a-plugin-you-no-longer-trust).

<h2 id="marketplace-tiers">
  Identify Anthropic's marketplaces by name
</h2>

A marketplace's name places it in one of three tiers: official, community, or third-party. Claude Code accepts the official and community names only for marketplaces sourced from `github.com/anthropics/` repositories, so a third-party marketplace can't present itself as an Anthropic one. A marketplace that a coworker or your organization publishes is third-party.

The table lists which names fall in each tier:

| Tier        | Which marketplaces                                                                               |
| :---------- | :----------------------------------------------------------------------------------------------- |
| Official    | The [official marketplace names](#official-marketplace-names), such as `claude-plugins-official` |
| Community   | `claude-community`, `claude-plugins-community`, and `healthcare`                                 |
| Third-party | Every other marketplace                                                                          |

Where the `claude-community` catalog pins a plugin to a commit SHA, which it does for nearly every entry, Claude Code refuses to install a different commit.

### Official marketplace names

These marketplace names make up the official tier:

* `claude-plugins-official`
* `claude-code-marketplace`
* `claude-code-plugins`
* `anthropic-marketplace`
* `anthropic-plugins`
* `agent-skills`
* `anthropic-agent-skills`
* `life-sciences`
* `knowledge-work-plugins`
* `claude-for-legal`
* `claude-for-financial-services`
* `financial-services-plugins`
* `first-party-plugins`
* `claude-tag-plugins`

For how the official, community, and demo marketplaces differ and where to browse what each one lists, see [Anthropic's marketplaces](/docs/en/plugins/anthropic-marketplaces).

## Review a plugin before you install

Before you install a plugin, look at what it adds and where it comes from.

<Steps>
  <Step title="Check the marketplace's source">
    In your shell, run `claude plugin marketplace list` to print the source each marketplace was added from, such as a GitHub repository or a directory.
  </Step>

  <Step title="Read the details pane">
    In a Claude Code session, run `/plugin` and select the plugin. The details pane shows a **Will install** section listing the plugin's commands, agents, skills, hooks, and MCP and LSP servers. For a plugin Anthropic has no published component data for, the section shows what the marketplace entry declares, or a note: `Components will be discovered at installation` for a plugin stored inside the marketplace, or `Component summary not available for remote plugin` for one fetched from elsewhere.
  </Step>

  <Step title="Read the plugin's source">
    In the details pane, select **Open homepage** or **View on GitHub** below the install options. If the pane offers neither, open the marketplace repository you found in the first step. Find the plugin's directory there. The **Will install** section shows that a hook exists but not what it runs, so read these files in the plugin's directory:

    * **`hooks/hooks.json`**: the command each hook runs
    * **`.mcp.json`**: each server's command or URL
    * **`bin/`**: every file in the directory
  </Step>

  <Step title="List what the plugin contains">
    Clone the repository that holds the plugin's directory, then run `claude --plugin-dir <plugin directory> plugin details <plugin name>` in your shell to see what Claude Code finds in it. The command reads the plugin's files without starting a session and prints a `Component inventory` listing the plugin's skills and commands, agents, hooks with each hook's event, and MCP and LSP servers.
  </Step>
</Steps>

After you install a plugin, run `claude plugin details <plugin name>` in your shell to print the same `Component inventory` for the installed copy under `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`.

### Remove a plugin you no longer trust

In your shell, run [`claude plugin uninstall <plugin>`](/docs/en/plugins/cli-reference#plugin-uninstall) with the `--scope` you installed it at. Then check what the uninstall removed and what it left:

* **Persistent data**: when that was the last scope the plugin was installed at, uninstalling also deletes the plugin's persistent data directory, unless you pass `--keep-data`.
* **Cached files**: the plugin's files stay on disk under `~/.claude/plugins/cache/` for 14 days before a [background sweep removes them](/docs/en/plugins/loading#cleanup-of-previous-versions). After you uninstall your last plugin, orphaned directories stay until you install another. To delete the files now, remove the plugin's directory under `~/.claude/plugins/cache/<marketplace>/<plugin>/` yourself.
* **The marketplace**: if you don't trust the marketplace's owner either, [remove the marketplace](/docs/en/plugins/install#manage-marketplaces) too, which uninstalls every plugin you installed from it.

## Recognize when Claude Code refuses or warns

The details pane you open from the **Discover** or **Marketplaces** tab in `/plugin` shows the same trust warning for each plugin. Claude Code refuses instead of warning in cases such as those under [Untrusted marketplace sources and failed integrity checks](#untrusted-marketplace-sources-and-failed-integrity-checks).

### Trust warning before you install

The warning reads the same whatever marketplace the plugin comes from:

```text theme={null}
Make sure you trust a plugin before installing, updating, or using it. Anthropic does not control what MCP servers, files, or other software are included in plugins and cannot verify that they will work as intended or that they won't change. See each plugin's homepage for more information.
```

If your organization sets `pluginTrustMessage` in [managed settings](/docs/en/plugins/org), Claude Code appends that text to the warning.

### Untrusted marketplace sources and failed integrity checks

Claude Code refuses to load a marketplace or to install a plugin in these cases, each with its own error message:

* **Untrusted marketplace source**: when a marketplace uses an official or community name but its source is outside `github.com/anthropics/`, Claude Code stops loading the marketplace and the plugins you installed from it. The error is [Marketplace is registered from an untrusted source](/docs/en/errors#marketplace-is-registered-from-an-untrusted-source).
* **Archive integrity**: when a marketplace entry pins an [`archive` source](/docs/en/plugins/marketplace-reference#archive-plugin-source) to a `sha256` digest and the downloaded file's digest doesn't match it, Claude Code refuses the install. The error is [Plugin archive integrity check failed](/docs/en/errors#plugin-archive-integrity-check-failed).

The `sha256` pin is separate from the community catalog's commit SHA pin, which selects the git commit to check out.

## Enforce plugin controls for your organization

With [managed settings](/docs/en/plugins/org), an administrator can enforce these plugin controls:

* Allowlist or blocklist marketplace sources
* Force-enable plugins
* Turn off the `--plugin-dir` and `--plugin-url` flags and the `CLAUDE_CODE_PLUGIN_DIRS` variable
* Limit hooks to those from managed settings and force-enabled plugins
* Stop plugins from members' claude.ai accounts from loading in Claude Code, with [`syncClaudeAiPlugins`](/docs/en/plugins/org#control-matrix)

The [control matrix](/docs/en/plugins/org#control-matrix) says what each key does and doesn't cover.

## Find plugins in telemetry

If your organization exports Claude Code's [OpenTelemetry events](/docs/en/monitoring-usage) to its own backend, the [marketplace tiers](#marketplace-tiers) decide which plugin names appear there:

* **[Plugin loaded event](/docs/en/monitoring-usage#plugin-loaded-event)**: the event reports official-tier plugin and marketplace names as they are. For the community and third-party tiers, `plugin.name` and `marketplace.name` are the literal string `third-party` unless you set `OTEL_LOG_TOOL_DETAILS=1`.
* **Plugin scope**: the loaded event's `plugin.scope` still reports where the plugin came from, such as `org` for a plugin your managed settings enable or `user-local` for any other third-party plugin. The [plugin loaded event](/docs/en/monitoring-usage#plugin-loaded-event) lists every value.
* **[Plugin installed event](/docs/en/monitoring-usage#plugin-installed-event)**: unless you set `OTEL_LOG_TOOL_DETAILS=1`, the event omits the name fields for non-official plugins instead of reporting `third-party`.
* **[Claude Code Analytics API](https://platform.claude.com/docs/en/api/admin/analytics/plugins/list)**: Claude Code reports plugins from the official and community tiers by name and reports every other plugin as `third-party`.

## Next steps

* [Manage plugins for your organization](/docs/en/plugins/org): restrict which marketplaces users can install from and require the ones you trust
* [Install and manage plugins](/docs/en/plugins/install): review a plugin's details pane before you choose a scope
* [Anthropic's marketplaces](/docs/en/plugins/anthropic-marketplaces): which marketplace names are Anthropic's
* [Security](/docs/en/security): Claude Code's own security model
