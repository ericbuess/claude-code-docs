> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Measure plugin cost and usage

> Measure a Claude Code plugin's token cost, find out whether people still use it, and pick the telemetry events for organization-wide plugin questions.

Every session where a plugin is enabled includes the names and descriptions of its skills, agents, and commands in Claude's context, and those tokens count against the user's usage whether or not the plugin gets used. This page shows how to see that number for a plugin, how to reduce it if you maintain the plugin, and where usage shows up so you can tell whether a plugin is still being used.

This page is for plugin authors and maintainers. If you administer Claude Code for an organization, [Measure across a fleet](#measure-across-a-fleet) covers the same questions across every machine.

<Note>
  These cases are covered on other pages:

  * **Testing how reliably the plugin changes Claude's behavior**: see [Test plugins with evals](/docs/en/plugin-evals)
  * **Trimming your own session's context**: see [Manage installed plugins](/docs/en/plugins/install#manage-installed-plugins) and the [context window](/docs/en/context-window) page
</Note>

Start with [Measure what a plugin costs](#measure-what-a-plugin-costs).

## Measure what a plugin costs

To see what a plugin adds to Claude's context, run [`claude plugin details`](/docs/en/plugins/cli-reference#plugin-details) with the plugin's name. You run it in your shell, not at the prompt of a running Claude Code session. The plugin has to be loaded: installed, in a skills directory, or passed with `--plugin-dir` in the same command, as in `claude --plugin-dir ./formatter plugin details formatter`.

This example reads an installed plugin named `formatter` that has two skills, a command, an agent, a hook, and an MCP server:

```bash theme={null}
claude plugin details formatter
```

```text theme={null}
formatter 1.0.0
  Description: Formats and lints code on save
  Source: formatter@my-marketplace

Component inventory
  Skills (3)  format-all, format-code, lint-fix
  Agents (1)  style-reviewer
  Hooks (1)  PostToolUse  (harness-only — no model context cost)
  MCP servers (1)  formatter-tools  (tool schemas resolved at runtime; not counted)
  LSP servers (0)

Projected token cost
  Always-on:   ~146 tok   added to every session

Per-component (rounded)
  component       always-on  on-invoke
  format-code           ~40        ~30
  lint-fix              ~50        ~30
  style-reviewer        ~40        ~40
  format-all           < 20        ~30

  On-invoke cost is paid each time a skill or agent fires.
  Token counts are estimates and may differ from actual usage.
```

Each part of the output answers a different question:

* **Component inventory**: what Claude Code found in the plugin. Commands are counted with skills, so `format-all` appears under `Skills`. Hooks and MCP servers get no cost estimate and no per-component row; to see what a plugin's MCP tools add, run `/context` in a session with the plugin enabled and read the `MCP tools` category.
* **Always-on**: the tokens that the names and descriptions of the plugin's skills, agents, and commands add to every session where the plugin is enabled, whether or not anything runs. This is the number every user carries, and the one to reduce.
* **Per-component**: each row splits one skill, agent, or command into its always-on share and its on-invoke cost, which is the body that loads only when that component runs. Use the always-on column to find which component contributes most.

### Lower the always-on figure

If you maintain the plugin, these changes reduce what it adds to every session. If you only use it, your options are to disable or uninstall it; see [Manage installed plugins](/docs/en/plugins/install#manage-installed-plugins).

The always-on figure counts each component's name plus its `description` and `when_to_use` frontmatter. To lower it:

* Shorten skill and agent descriptions.
* Split a large plugin so users install only the components they need.

A skill's description is also what Claude matches a request against, so a shorter one can stop the skill triggering. After you trim descriptions, check triggering with a [`tool_used: Skill` grader](/docs/en/plugin-evals#create-your-first-eval-suite) in your eval suite.

For what each component type contributes, see [plugin components](/docs/en/plugins/components).

### Cost shown to users before install

Plugins in the official marketplace show their cost to users before install. In `/plugin`, when a user browses a marketplace's plugin list and selects a plugin, the details pane shows a **Context cost** section with an `Every turn:` line and a `When invoked:` line. When the always-on figure is 2,000 tokens or more, the `Every turn:` line appears highlighted.

A plugin in your own marketplace has no **Context cost** section.

## Check whether a plugin is used

Claude Code doesn't report a plugin's usage back to its author. Usage is recorded on the machine of each person who installed the plugin, so what you can learn depends on your relationship to those people:

* **You administer Claude Code for their organization**: the OpenTelemetry events and the Analytics API count installs and skill activations across every machine. See [Measure across a fleet](#measure-across-a-fleet).
* **They're teammates you can ask**: each user's own Claude Code shows them whether they still use the plugin, in four places: the [`/plugin` panel](#not-used-recently-in-/plugin), [`/skill-doctor`](#find-skills-that-never-run), [`/doctor`](#unused-plugins-in-/doctor), and [`/usage`](#usage-share-in-/usage). All four are commands the user runs at the Claude Code prompt in a session on their own machine.
* **Neither**: you have no usage signal from Claude Code for that plugin.

For usage of a plugin listed in Anthropic's directory, see [Track published plugin usage](https://claude.com/docs/connectors/building/after-publishing#track-published-plugin-usage) on claude.com.

### Not used recently in `/plugin`

On the **Installed** tab of `/plugin`, a plugin the user installed from a marketplace moves under a **Not used recently** header once it has gone unused for at least 14 days and 10 sessions. The plugin's details also show a `Last used:` line. For what users do with that header and line, see [Find plugins you no longer use](/docs/en/plugins/install#find-plugins-you-no-longer-use).

The **Not used recently** header never appears for:

* Plugins loaded with `--plugin-dir` or from a skills directory
* Plugins enabled through managed settings, or mounted from a [seed directory](/docs/en/plugins/org#seed-containers-and-ci)
* Plugins that include a theme, output style, monitor, or workflow, because those are in use without a tracked invocation

A plugin's [language server](/docs/en/plugins/components#lsp-servers) counts as used when it delivers diagnostics or answers a code navigation request, so an LSP plugin whose server is active in your sessions isn't listed as unused.

When the user's organization sets [`strictKnownMarketplaces`](/docs/en/plugins/org#restrict-what-users-can-install), neither the header nor the `Last used:` line appears.

### Find skills that never run

Run `/skill-doctor` to see what each of your skills costs and how often it gets used. It flags skills that are in Claude's skill listing but have never been invoked, including skills from plugins.

In an interactive session, the report opens in the `/plugin` manager's **Stats** tab. See [Find unused skills](/docs/en/skills#find-unused-skills) for what the report covers and where it's available.

### Unused plugins in `/doctor`

The `/doctor` checkup lists each user-installed skill, MCP server, and plugin, and recommends disabling the ones that were not used. See [`/doctor` in the commands reference](/docs/en/commands#all-commands).

### Usage share in `/usage`

On a Pro, Max, Team, or Enterprise plan, the `/usage` breakdown attributes recent usage to skills, subagents, plugins, and MCP servers as a share of the total. See [Using the `/usage` command](/docs/en/costs#using-the-/usage-command).

## Measure across a fleet

If you administer Claude Code for an organization, you can measure plugin cost and usage across every machine from either of these sources:

* **OpenTelemetry events**: Claude Code exports these to your own backend once you [configure an exporter](/docs/en/monitoring-usage). See [OpenTelemetry events for plugin installs and use](#pick-the-opentelemetry-event-for-each-question).
* **Analytics API**: served from Anthropic's records, with no exporter needed. See [Query the Analytics API](#query-the-analytics-api).

<h3 id="pick-the-opentelemetry-event-for-each-question">
  OpenTelemetry events for plugin installs and use
</h3>

These OpenTelemetry events and attributes answer each plugin question from your backend:

| Question                                          | OpenTelemetry event or attribute                                                                                                                         |
| :------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Which plugins get installed, and from where       | [`claude_code.plugin_installed`](/docs/en/monitoring-usage#plugin-installed-event), one per install                                                           |
| Which plugins are active in how many sessions     | [`claude_code.plugin_loaded`](/docs/en/monitoring-usage#plugin-loaded-event), one per enabled plugin at session start                                         |
| Which skills activate, and which plugin owns them | [`claude_code.skill_activated`](/docs/en/monitoring-usage#skill-activated-event), with `plugin.name` and `marketplace.name` for plugin skills                 |
| What a plugin's hooks report                      | [`claude_code.hook_plugin_metrics`](/docs/en/monitoring-usage#hook-plugin-metrics-event), emitted only for hooks in official-marketplace plugins              |
| What a plugin costs in API spend                  | `plugin.name` and `marketplace.name` on the [cost counter](/docs/en/monitoring-usage#cost-counter), set when the active skill or subagent belongs to a plugin |

### Redacted plugin names in your backend

Plugins from the official marketplace report their plugin name and marketplace name to your backend verbatim. Every other plugin's name is redacted or omitted by default, including a plugin from your organization's own marketplace. The plugin's [trust tier](/docs/en/plugins/security#find-plugins-in-telemetry) decides which.

To get real names on some events, set the [`OTEL_LOG_TOOL_DETAILS`](/docs/en/monitoring-usage#common-configuration-variables) environment variable to `1` on the machines that export telemetry, for example in the `env` block of the same [managed settings](/docs/en/monitoring-usage#administrator-configuration) that configure the exporter:

| Event                                 | Default                                                                                            | With `OTEL_LOG_TOOL_DETAILS=1`                      |
| :------------------------------------ | :------------------------------------------------------------------------------------------------- | :-------------------------------------------------- |
| `plugin_loaded`                       | `plugin.name` and `marketplace.name` are the literal string `third-party`                          | Real names                                          |
| `plugin_installed`, `skill_activated` | `plugin.name` and `marketplace.name` omitted; on `skill_activated`, `skill.name` is `custom_skill` | Real names                                          |
| Cost counter                          | `plugin.name` is `third-party`; `marketplace.name` absent                                          | Real `plugin.name`; `marketplace.name` still absent |

On `plugin_loaded`, `plugin_id_hash` still identifies each plugin by default, so you can count distinct third-party plugins.

### Query the Analytics API

On the Enterprise plan, the Analytics API answers "which plugins does my organization install and invoke" from Anthropic's records, with no exporter needed. [`GET /v1/organizations/analytics/plugins`](https://platform.claude.com/docs/en/api/admin/analytics/plugins/list) returns per-plugin, per-day install and invocation counts across Claude Code and Cowork, which you can group by user, RBAC group, or product.

Plugin activity that reaches Anthropic without a plugin name appears in one aggregate `third-party` row. [Find plugins in telemetry](/docs/en/plugins/security#find-plugins-in-telemetry) says which plugins Claude Code reports by name.

Authenticate the request with an API key that has the `read:analytics` scope, which a Primary Owner creates as described under [Access data programmatically](/docs/en/analytics#access-data-programmatically).

See the [endpoint reference](https://platform.claude.com/docs/en/api/admin/analytics/plugins/list) for the parameters and response fields.

## Next steps

* [Test plugins with evals](/docs/en/plugin-evals): measure how reliably the plugin steers Claude, not only what it costs
* [Lower the always-on figure](#lower-the-always-on-figure): what to change in the plugin to reduce its per-turn cost
* [Plugin security and trust](/docs/en/plugins/security#find-plugins-in-telemetry): which telemetry fields carry plugin names and when they're redacted
* [Monitoring usage](/docs/en/monitoring-usage): the full OpenTelemetry event reference
