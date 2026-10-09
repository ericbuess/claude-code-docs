> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Manage mods for your organization

> Control Claude Code mods with managed settings: stop user-installed mods, allow only your own, review what a mod can do, and enforce policy with your own mod.

A [mod](/docs/en/plugins/mods/overview) is a plugin that runs code inside Claude Code with the permissions of the user who installed it. Mods aren't sandboxed. Through [managed settings](/docs/en/managed-settings), you decide whether mods run on your users' machines, which ones, and in what order. You can also install a mod of your own that watches or refuses what other mods do.

This page is for the person who deploys managed settings for Claude Code, whether as a file, through MDM, or from the claude.ai admin console. Mods are on by default in Claude Code v2.1.286 and later. Start with the section that matches what you came to do:

* **Keep users' own mods out, with or without mods of your own**: [Stop user-installed mods from loading](#stop-user-installed-mods-from-loading)
* **See what your users get when you change nothing**: [Know what happens by default](#know-what-happens-by-default)
* **Leave mods on with other limits**: [Choose how much to allow](#choose-how-much-to-allow)

<Note>
  These cases are covered on other pages:

  * **You haven't deployed managed settings before**: start with [Deploy managed settings](/docs/en/managed-settings)
  * **You want to control which plugins users can install**: see [Manage plugins for your organization](/docs/en/plugins/org)
</Note>

## Stop user-installed mods from loading

To keep every mod your users bring from running its hooks, set the `allowManagedModsOnly` option on the [built-in guard](#know-what-happens-by-default), a policy mod that Claude Code loads ahead of every mod a user installs. The option goes in managed settings under `pluginConfigs`, keyed by `cc-plugin-sec-default@builtin`:

```json managed-settings.json theme={null}
{
  "pluginConfigs": {
    "cc-plugin-sec-default@builtin": {
      "options": {
        "allowManagedModsOnly": true
      }
    }
  }
}
```

With the option set in managed settings:

* **No mod a user brings runs its hooks**: that covers a mod in a plugin the user installed, a mod loaded with `--plugin-dir`, and a mod [Claude wrote during a session](/docs/en/plugins/mods/create#ask-claude-for-a-mod)
* **Your organization's mods still run**: a mod that [counts as your organization's](#install-your-organizations-mods) isn't checked. Every other mod counts as a user's and is refused. That includes a mod in a plugin you enable from a GitHub or other remote marketplace, and one your organization turns on for its members on claude.ai. If none counts as yours, no installed mod runs its hooks.
* **Users can't undo it**: the guard reads the option from managed settings only, so the same entry in a user, project, or local settings file, or in a file passed with `--settings`, changes nothing
* **A file or MDM policy covers every provider**: when you deliver the option as a file or through MDM, it works the same way on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry. For delivery from the claude.ai admin console, see [Platform availability](/docs/en/server-managed-settings#platform-availability)
* **Users' other customizations keep working**: their [hooks in settings files](/docs/en/hooks) and in plugins' `hooks/hooks.json`, status lines, and `/goal` aren't affected
* **Built-in mods keep running**: mods built into Claude Code, such as `AGENTS.md` support, each have [their own switch](/docs/en/plugins/mods/overview#mods-built-into-claude-code)

To confirm the option on a user's machine, start Claude Code there with `--plugin-dir` and the path of a directory that holds a mod, such as `claude --plugin-dir ./first-mod`. The mod's hooks don't run, and the transcript and the debug log have the [guard's message](/docs/en/plugins/mods/troubleshoot#messages-from-the-built-in-guard), which names the mod and `allowManagedModsOnly`. If the message isn't there, see [Check that a policy is in force](/docs/en/managed-settings#check-that-a-policy-is-in-force) and the [rules that decide whether an option takes effect](#set-options-on-the-built-in-guard).

If you set `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` to `0` during early access, replace it with this option. Claude Code v2.1.287 and later ignores the variable at any value, so a `0` there leaves mods on.

## Know what happens by default

With no mod settings of your own, this is what your users get:

* **Mods are on.** A user can install a plugin that contains a mod from any marketplace your plugin settings allow, or load one from a directory with `--plugin-dir`.
* **A built-in guard runs first.** Claude Code loads a built-in mod named `sec-default@builtin` ahead of every mod a user installs. Users can't turn it off. `/plugin` and the debug log list it as `cc-plugin-sec-default`. The guard loads when either of these is true:

  * The machine has managed settings
  * The user is signed in to Claude Code with a Team or Enterprise plan

  A user who authenticates with an API key, or through Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry, gets the guard only on a machine that has managed settings.
* **The guard protects what you manage.** A user's mod can't change what your managed hooks receive or decide, the system prompt, your managed `CLAUDE.md` and other managed instructions, what any mod reads as settings, or the tools and descriptions of your managed MCP servers.
* **Everything else is allowed.** The guard adds no other restrictions. A user's mod can still read and write files, start processes, make network requests, rewrite tool calls and prompts, deny a tool call, approve one that would otherwise prompt, and draw in the interface, all with that user's permissions.
* **Deny rules and your managed hooks take precedence.** Where the guard loads, a user's mod can't approve a call that a `deny` rule refuses, whichever settings file holds the rule. A block from a `PreToolUse` hook in managed settings is final too. Both apply to Claude's tool calls. Neither applies to a mod's own [`$.fs` and `$.process` calls](/docs/en/plugins/mods/api#reach-files-processes-and-the-network): with `Read(.env)` denied, a mod can still read that file with `$.fs.read` or start a program that does. To limit those calls, keep the mod from loading or handle the call in a [policy mod](#enforce-a-policy-with-a-mod-of-your-own).
* **Other permission checks can be overridden.** A user's mod that approves tool calls can approve a call that an `ask` rule would prompt for, or that a `PreToolUse` hook outside managed settings blocked. In auto mode, a call the mod approves runs without a classifier check.

The guard's source is public in the [`mods/sec-default` directory of the Claude Code repository](https://github.com/anthropics/claude-code/tree/main/mods/sec-default).

### Know which controls still apply

Mods don't replace the controls you already have:

* **Settings hooks keep working.** Command, HTTP, prompt, and agent hooks in settings files and in plugins' `hooks/hooks.json` run as before, alongside mods. Nothing about them is deprecated.
* **Deny rules take precedence where the guard loads.** A user's mod can't approve a call that a `deny` rule refuses, unless you set [`allowModsToOverrideDenyRules`](#set-options-on-the-built-in-guard).
* **Managed hooks run first.** A `PreToolUse` hook in managed settings runs before any mod sees the tool call, and its block is final. If a mod then rewrites the call, your managed hooks run again on the rewritten call, so a block still applies. `PreToolUse` hooks from other settings files and from plugins run after the last mod, so a mod that returns its own result in place of running the tool keeps those from running. See [The order mods run in](/docs/en/plugins/mods/events#the-order-mods-run-in).
* **Network policy covers `$.http.fetch`.** If your organization turns off web fetching, or nonessential network traffic is turned off for the session, Claude Code refuses a network request that a mod makes with `$.http.fetch`. The policy doesn't cover a program the mod starts with `$.process.run`. That program reaches the network with the user's own access.
* **Plugin controls cover mods.** A mod is a plugin, so the [settings that restrict what users can install](/docs/en/plugins/org#restrict-what-users-can-install), such as `strictKnownMarketplaces`, decide whether it can be installed at all.
* **Mods can't change the permission prompt.** A mod can restyle much of Claude Code's interface, but not the permission prompt, so it can't change what a prompt shows. A mod can still approve or deny a tool call before the prompt appears, as [Know what happens by default](#know-what-happens-by-default) describes.
* **Trust prompts come first.** In an interactive session in a directory the user hasn't trusted yet, no mod loads until they answer the trust prompt.
* **`--safe-mode` turns installed mods off, yours included.** Start a session with `claude --safe-mode` to check whether a mod caused a problem.

None of these controls sandboxes a mod. A mod you allow runs as the user, with the user's access to files, processes, and the network.

## Decide whether to leave mods on

A mod can do more than the other parts of a plugin because it runs inside Claude Code. It sees every prompt and tool call, can change them, and can allow or deny a tool call before a permission prompt appears.

What a user can load as a mod depends on the plugin controls you already have:

| Your plugin controls today | What a user can load as a mod |
| :- | :- |
| None | A mod from any marketplace, from any directory with `--plugin-dir`, or that Claude writes during a session |
| A marketplace allowlist | A mod from the marketplaces you allow, or from any directory with `--plugin-dir`. A mod Claude writes during a session loads only when the allowlist [includes `skills-dir`](/docs/en/plugins/org#keep-skills-directory-plugins-loading). |
| A marketplace allowlist and `disableSideloadFlags` | A mod from the marketplaces you allow |

[Manage plugins for your organization](/docs/en/plugins/org) lists the ways a plugin loads and the setting that controls each.

To check the mods in a marketplace before your users install them, see [Review what a mod can do](#review-what-a-mod-can-do). To keep users' mods out until you've done that, see [Stop user-installed mods from loading](#stop-user-installed-mods-from-loading).

### Review what a mod can do

You can see what a mod is able to do without running it. In your shell, run `claude plugin validate` on the plugin's directory:

```bash theme={null}
claude plugin validate ./some-mod
```

The `hooks:` and `calls:` lines in the output describe the mod's code:

```text theme={null}
  ❯ ./register.js hooks: session.start, tool.call, ui.render{component=Pane}
  ❯ ./register.js calls: $.fs.read, $.http.fetch, $.store.set, $.ui.open
```

The `hooks:` line lists the events the mod receives. The `calls:` line lists the mods API methods its code calls. The [mods API](/docs/en/plugins/mods/api), written `$` in a mod's code, is how a mod reaches files, processes, and the network. Claude Code refuses to load a mod that uses the mods API in a way this command can't read.

Look at the `calls:` line for these:

| Call | What it means |
| :- | :- |
| `$.fs.read`, `$.fs.write` | Reads or writes files anywhere the user can |
| `$.process.run`, `$.process.spawn` | Starts programs as the user |
| `$.http.fetch` | Makes network requests |
| `$.env.get`, `$.settings.read` | Reads environment variables and settings, which can hold API keys. An `env reads:` line in the output names each variable. |
| `$.env.set` | Sets an environment variable for Claude Code and for every command and MCP server it starts afterward, which can change what those programs run. An `env writes:` line names each variable. |
| `$.mcp.call` | Calls a tool on a connected MCP server, under the session's permission rules |
| `$.model.complete` | Uses the user's plan or API key for model calls |
| `$.prompt.submit` | Submits a prompt, and can send it as the user's own words |
| `$.session.send` | Sends a message that another session's, subagent's, or [teammate's](/docs/en/agent-teams) Claude reads |

In the `hooks:` line, [`tool.call`](/docs/en/plugins/mods/reference#tools) and [`prompt.submit`](/docs/en/plugins/mods/reference#prompts-and-what-claude-reads) mean the mod sees every tool call and every prompt, and can change them. [`session.append`](/docs/en/plugins/mods/reference#session) means the mod can rewrite each row of the conversation before it's stored. [`ui.render{component=AskUserQuestion}`](/docs/en/plugins/mods/interface#change-what-claude-code-already-draws) means the mod can redraw the dialog Claude uses to ask the user a question. `tool.check` means the mod can approve or deny a tool call before a permission prompt appears. [Know what happens by default](#know-what-happens-by-default) lists which of your rules and hooks take precedence over its answer.

## Choose how much to allow

Mod policies range from no installed mods at all to any mod a user chooses, with your own mod checking the others, and each one is a few managed settings. Find the policy you want in the first column and set what the second column names. [Deploy managed settings](/docs/en/managed-settings) covers where managed settings live.

| What you want | Settings |
| :- | :- |
| No installed mod runs, with settings hooks untouched | Set [`allowManagedModsOnly`](#set-options-on-the-built-in-guard) and deploy no mods of your own |
| No installed mods and no hooks at all, your managed hooks included | Set `disableAllHooks` to `true` |
| Only your organization's mods | Set the guard's [`allowManagedModsOnly` option](#stop-user-installed-mods-from-loading), and [install your mods](#install-your-organizations-mods) so that they count as yours |
| Any mod from marketplaces you approve | Keep your [marketplace restrictions](/docs/en/plugins/org#restrict-what-users-can-install), and set `disableSideloadFlags` to `true` |
| Any mod, with your own mod checking the others | [Install your mod](#install-your-organizations-mods), and list it with `sec-default@builtin` in `prependPlugins` |

What each setting does:

* **`allowManagedModsOnly`**: an option on the built-in guard. Claude Code refuses users' own mods, so none of their hooks run. Users' settings hooks, status lines, and `/goal` keep working. [Stop user-installed mods from loading](#stop-user-installed-mods-from-loading) lists what it covers.
* **`allowManagedHooksOnly`**: a wider setting. Only [your organization's mods](#install-your-organizations-mods) and the mods built into Claude Code load. A mod a user installed themselves doesn't. The setting also blocks hooks in users' own settings files. Read [What runs under `allowManagedHooksOnly`](/docs/en/settings-reference#what-runs-under-allowmanagedhooksonly) before you set it.
* **`disableAllHooks`**: the widest setting. In managed settings, it stops the mods in every installed plugin, yours included, and turns off every hook in settings files, so a `PreToolUse` hook in your managed settings no longer blocks anything. Custom status lines and `/goal` stop working too. Read [`disableAllHooks`](/docs/en/settings-reference#disableallhooks) before you set it.
* **`disableSideloadFlags`**: rejects `--plugin-dir` and `--plugin-url` at startup, and keeps mods Claude writes during a session from loading. The setting also rejects `--agents` and `--mcp-config`. Read [`disableSideloadFlags`](/docs/en/settings-reference#disablesideloadflags) before you set it.

Mods built into Claude Code, such as `AGENTS.md` support, aren't affected by these settings. Each has [its own switch](/docs/en/plugins/mods/overview#mods-built-into-claude-code).

A user whose mod was refused or didn't load finds the reason in their debug log. [Refusal messages](/docs/en/plugins/mods/troubleshoot#refusal-messages) lists the lines for `allowManagedHooksOnly` and `disableAllHooks`, and [Messages from the built-in guard](/docs/en/plugins/mods/troubleshoot#messages-from-the-built-in-guard) has the line for `allowManagedModsOnly`.

### Allow only your organization's mods

To run your organization's mods and block the ones users bring, deploy the settings from the **Only your organization's mods** row of the [policy table](#choose-how-much-to-allow), plus `disableSideloadFlags`. With this complete `managed-settings.json`, Claude Code refuses users' own mods, so none of their hooks run, and your policy mod runs ahead of other mods:

```json managed-settings.json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "directory", "path": "/opt/acme/claude-plugins" }
    }
  },
  "enabledPlugins": { "acme-guard@acme-tools": true },
  "prependPlugins": ["acme-guard@acme-tools", "sec-default@builtin"],
  "pluginConfigs": {
    "cc-plugin-sec-default@builtin": {
      "options": { "allowManagedModsOnly": true }
    }
  },
  "disableSideloadFlags": true
}
```

Each group of keys does one job:

* **`extraKnownMarketplaces`, `enabledPlugins`, and `prependPlugins`**: install your mod so that it counts as yours, and run it first with the guard after it. [Install your organization's mods and set the order](#install-your-organizations-mods) covers the directory these keys point at.
* **`pluginConfigs`**: sets the guard's `allowManagedModsOnly` option, so Claude Code refuses users' own mods. Their settings hooks, status lines, and `/goal` keep working.
* **`disableSideloadFlags`**: see [`disableSideloadFlags`](/docs/en/settings-reference#disablesideloadflags) for the flags it rejects at startup

To confirm the policy on a test machine, in your shell start a session with `claude --debug` and read the debug log:

* **Your mod**: its `hooks module` line has `tier prepend`
* **A mod the user installed**: a line reads `refused by cc-plugin-sec-default: mods are limited to your organization's by policy (allowManagedModsOnly)`. An earlier line says that mod's hooks module `loaded`, so look for the refusal.
* **A plugin directory**: `claude --plugin-dir ./any-mod` exits with a message that starts `--plugin-dir is disabled by your organization's managed settings (disableSideloadFlags)`

To also limit which marketplaces users can add, combine this file with your [marketplace restrictions](/docs/en/plugins/org#restrict-what-users-can-install).

### Apply your plugin controls to mods

A mod is a plugin, so the ways you [manage plugins for your organization](/docs/en/plugins/org) also apply to a plugin that holds a mod:

* **See which plugins load across your fleet**: [Audit and review](/docs/en/plugins/org#audit-and-review)
* **Decide when a plugin you reviewed can update**: [Set update policy](/docs/en/plugins/org#set-update-policy)
* **Give one group a different policy, such as a pilot**: [Plan for what managed settings can't enforce](/docs/en/plugins/org#plan-for-what-managed-settings-can’t-enforce)
* **Check which apps and session kinds apply the plugin keys**: [When each surface applies the plugin keys](/docs/en/plugins/org#when-each-surface-applies-the-plugin-keys)
* **Set up CI and containers**: [Seed containers and CI](/docs/en/plugins/org#seed-containers-and-ci)
* **Offer mods your users may install**: [Host a marketplace](/docs/en/plugins/host-marketplace). A mod that Claude Code copies from a GitHub, git, URL, or npm source counts as a user's, not as [your organization's](#install-your-organizations-mods).

### Set options on the built-in guard

The built-in guard takes options. Set them in managed settings under `pluginConfigs`, keyed by `cc-plugin-sec-default@builtin`, as the example in [Stop user-installed mods from loading](#stop-user-installed-mods-from-loading) does.

The table gives what your users get with each option unset and with it set to `true`:

| Option | Unset | `true` |
| :- | :- | :- |
| `allowManagedModsOnly` | Users' own mods run | Only [your organization's mods](#install-your-organizations-mods), and mods built into Claude Code, run their hooks. Claude Code refuses every other mod, including one a user installed or named with `--plugin-dir`. |
| `allowModsToOverrideDenyRules` | Deny rules take precedence over users' mods | A user's mod that approves tool calls can approve a call that a `deny` rule refuses |

These rules decide whether an option takes effect:

* **The id has one form here**: Claude Code reads the options only under `cc-plugin-sec-default@builtin`. `prependPlugins` accepts `sec-default@builtin` as well, and `pluginConfigs` doesn't.
* **Only managed settings count**: the same entry in a user, project, or local settings file, or in a file passed with `--settings`, neither sets an option nor loosens one
* **The guard has to load**: if you set `prependPlugins`, [name the guard in the list](#install-your-organizations-mods). Where the guard doesn't load, neither option applies.
* **The guard fails closed**: if the guard can't read managed settings, it refuses every user's mod at load. If it can't check the deny rules for a call that a user's mod approved, it refuses the call.

The [messages from the built-in guard](/docs/en/plugins/mods/troubleshoot#messages-from-the-built-in-guard) are what your users see when either option applies.

## Run your organization's own mods

You can deploy mods of your own to every user, choose where they run relative to users' mods, and use one to enforce a policy.

<h3 id="install-your-organizations-mods">
  Install your organization's mods and set the order
</h3>

Your organization's mods load where users' mods don't and can run ahead of them, so Claude Code has to be able to tell that a mod came from you. It treats a mod as your organization's only when all of these are true:

* Managed `enabledPlugins` sets the mod's plugin to `true`
* Managed settings name the plugin's [marketplace](/docs/en/plugins/create-marketplace) as a directory on the user's machine, by absolute path. An `extraKnownMarketplaces` entry does that and registers the marketplace for the user too.
* The marketplace lists the plugin by a relative path, so Claude Code [loads it in place](/docs/en/plugins/loading#in-place-and-copied-plugins) from that directory

To meet them, have your device management copy the marketplace directory to the same path on every machine. Make the directory and every directory above it writable only by an administrator, as the managed settings file is. Anyone who can write there can rewrite your mod. Managed settings you deliver from the claude.ai admin console can carry the keys, but they can't put the directory on a machine.

The directory holds the marketplace's manifest and the plugin:

```text theme={null}
/opt/acme/claude-plugins/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── acme-guard/
        ├── .claude-plugin/
        │   └── plugin.json
        └── hooks/
            ├── hooks.json
            └── register.js
```

The manifest lists the plugin by its path relative to that directory:

```json /opt/acme/claude-plugins/.claude-plugin/marketplace.json theme={null}
{
  "name": "acme-tools",
  "owner": { "name": "Acme" },
  "plugins": [
    { "name": "acme-guard", "source": "./plugins/acme-guard", "description": "Acme policy mod" }
  ]
}
```

A plugin that Claude Code copies into its cache counts as a user's, even when managed `enabledPlugins` enables it. That covers every plugin from a GitHub, git, URL, or npm source. Its mod runs among users' mods, `prependPlugins` and `appendPlugins` skip it, `allowManagedModsOnly` refuses it, and `allowManagedHooksOnly` keeps it from loading. The user's debug log has a line that starts with the plugin's id and `is enabled by managed settings, but`.

Claude Code fires an event each time it's about to act, such as run a tool, and passes it to each mod in turn. A mod that counts as yours [runs before users' mods](/docs/en/plugins/mods/events#the-order-mods-run-in) even when you list it nowhere. To set its place, list its id in one of two settings. The id is the plugin's name, `@`, and the marketplace's name, such as `acme-guard@acme-tools`.

* **`prependPlugins`**: your mod sees every event before any user's mod and every result after. It can change the event, refuse it, or skip the users' mods.
* **`appendPlugins`**: your mod runs after every user's mod, so it sees only the events those mods pass on, in the form they pass them

This example declares the `acme-tools` marketplace at `/opt/acme/claude-plugins`, enables `acme-guard` from it, and runs that mod first, with the built-in guard after it:

```json managed-settings.json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "directory", "path": "/opt/acme/claude-plugins" }
    }
  },
  "enabledPlugins": { "acme-guard@acme-tools": true },
  "prependPlugins": ["acme-guard@acme-tools", "sec-default@builtin"]
}
```

Each key does one job:

* **`extraKnownMarketplaces`**: names the directory that holds the `acme-tools` marketplace. `path` is the absolute path of the directory that contains `.claude-plugin/marketplace.json`.
* **`enabledPlugins`**: turns `acme-guard` on for every user who receives these managed settings
* **`prependPlugins`**: puts `acme-guard` first and the built-in guard second, both ahead of any mod a user installs. Claude Code follows the order you list.

To confirm that a user's machine received the settings, see [Check that a policy is in force](/docs/en/managed-settings#check-that-a-policy-is-in-force).

To confirm where the mod runs, start a session on that machine with `claude --debug` and search the [debug log](/docs/en/plugins/mods/troubleshoot#read-the-debug-log) for the mod's id:

* **`hooks module acme-guard@acme-tools loaded`, with `tier prepend`**: the mod counts as your organization's and runs first
* **The same line with `tier user`**: Claude Code treats it as a user's mod. A second line, `prependPlugins names acme-guard@acme-tools, which is not an enabled managed plugin with a hooks module; skipped`, says the list skipped it.

These rules decide which ids in the two lists take effect:

* **The list replaces the default**: when you set `prependPlugins` in managed settings, name `sec-default@builtin` in it to keep the built-in guard. The guard is built in and needs no `enabledPlugins` entry.
* **Your own ids must count as yours**: in managed settings, Claude Code skips an id whose plugin doesn't meet the conditions for an organization's mod
* **Repositories can't set them**: Claude Code reads both settings from managed settings and never from a repository's settings file. A user can set them in `~/.claude/settings.json` to order their own mods only on a machine with no managed settings, and only when they aren't signed in with a Team or Enterprise plan. Anywhere else, Claude Code ignores both keys in user settings. A list there neither adds nor removes the built-in guard.

### Enforce a policy with a mod of your own

To keep every user's mod out, you don't need a mod of your own. Set [`allowManagedModsOnly`](#stop-user-installed-mods-from-loading). Write a policy mod when you want to allow some users' mods and refuse others, or to record what mods do.

Each time another mod is about to load, your mod receives the list that `claude plugin validate` prints, in an event named [`plugin.register`](/docs/en/plugins/mods/reference#other-mods). A mod in `prependPlugins` can read that list and refuse the mod. It can also [handle any mods API call by name](/docs/en/plugins/mods/api#reach-files-processes-and-the-network) to record or refuse that call for every other mod. The name is the method without the `$.`, so a hook on `fs.write` sees every `$.fs.write` call.

This policy mod refuses any user's mod whose own code calls `$.process.run` or `$.process.spawn`. It also keeps an audit log, writing each tool call and each file a mod writes to the debug log. Because it runs first, the log records what was requested, before any user's mod changes it. Save it as `acme-guard/hooks/register.js`:

```javascript acme-guard/hooks/register.js theme={null}
// The methods no user's mod may call, each spelled namespace.method
const BLOCKED_CALLS = ['process.run', 'process.spawn']

export function register(on) {
  // Runs each time another mod is about to load
  on('plugin.register', async ($, e, next) => {
    // Keep the calls in that mod's code that are on the blocked list
    const blocked = e.uses.calls.filter((call) => BLOCKED_CALLS.includes(call))
    if (e.tier === 'user' && blocked.length > 0) {
      // Returning refuse keeps the mod from loading, and the text is the reason
      return { refuse: 'Acme policy: mods may not call ' + blocked.join(', ') }
    }
    // Let every other mod load
    return next(e)
  })

  // Record each tool call, then let it go ahead unchanged
  on('tool.call', async ($, e, next) => {
    $.ui.log('audit tool.call ' + e.tool, { to: 'debug' })
    return next(e)
  })

  // Record which mod wrote a file, then the path, quoted because the mod chose it
  on('fs.write', async ($, e, next) => {
    $.ui.log('audit fs.write by ' + next.origin.plugin + ' ' + JSON.stringify(e.path), { to: 'debug' })
    return next(e)
  })
}
```

The file registers three hooks:

* **`plugin.register`**: decides whether another mod loads. It refuses a user's mod that calls a blocked method and passes every other mod on.
* **`tool.call`**: writes a line such as `audit tool.call Bash` to the debug log for each tool call, and changes nothing
* **`fs.write`**: writes a line such as `audit fs.write by reader "/tmp/notes.md"` for each `$.fs.write` call another mod makes, and changes nothing. The mod's name comes first and the path is quoted, so a path that a mod picks can't pass for another field of the line.

The `plugin.register` hook reads two fields of the event:

* **`e.tier`**: where the mod would run, one of `prepend`, `user`, `append`, or `builtin`. Every mod a person installs is `user`.
* **`e.uses.calls`**: the mods API methods the mod calls, each written `namespace.method` such as `process.run`, without the `$.` that `claude plugin validate` prints

When a user installs a mod that calls `$.process.run`, the mod doesn't load, and their debug log has a line that ends with `refused by acme-guard:` and your reason. The refusal also reaches the transcript in a [session that hot-reloads a plugin directory](/docs/en/plugins/mods/troubleshoot#find-out-why-a-mod-does-nothing). To block a call without refusing the whole mod, return `{ deny: 'your reason' }` from a hook on that call's name.

To send the audit lines somewhere other than the debug log, call `$.http.fetch` from the same hooks.

A session can run without your mod. If the worker thread that runs installed mods [crashes three times](/docs/en/plugins/mods/troubleshoot#mods-that-run-in-the-hooks-worker-are-off-for-this-session), Claude Code unloads every mod that isn't built in, including yours, until the user runs `/reload-plugins` or starts a new session. And a user who starts Claude Code with `--safe-mode` runs without installed mods, yours included.

[Create a mod](/docs/en/plugins/mods/create) covers the files a mod needs. [Test a policy mod](/docs/en/plugins/mods/test#test-a-mod-that-judges-other-mods) has a test file for this policy mod.

#### Refuse mods when your check fails

If your `plugin.register` hook throws or exceeds its time limit, Claude Code skips the hook, so the check fails open and the mod it was checking loads. To fail closed and refuse users' mods, move the check into a named function and add a `.catch` handler that returns the refusal. This version of the file shows the `plugin.register` hook only, so keep the two audit hooks from the first version in `register`:

```javascript acme-guard/hooks/register.js theme={null}
const BLOCKED_CALLS = ['process.run', 'process.spawn']

// The same check as before, moved into a function of its own
async function checkMod($, e, next) {
  const blocked = e.uses.calls.filter((call) => BLOCKED_CALLS.includes(call))
  if (e.tier === 'user' && blocked.length > 0) {
    return { refuse: 'Acme policy: mods may not call ' + blocked.join(', ') }
  }
  return next(e)
}

export function register(on) {
  // The handler runs only when checkMod throws or exceeds its time limit
  on('plugin.register', checkMod).catch(async ($, e, next) => {
    // Let your organization's mods and built-in mods load
    if (e.tier !== 'user') return next(e)
    // Refuse the user's mod that couldn't be checked
    return { refuse: 'Acme policy check failed, so this mod was not loaded' }
  })
}
```

With the handler in place, a mod that was being checked when the check threw or timed out doesn't load, and the refusal line carries the second reason, as in `refused by acme-guard: Acme policy check failed, so this mod was not loaded`. The handler passes every mod outside the `user` tier to `next(e)`, so a failed check doesn't stop the mods your organization lists. [Handle a hook that fails](/docs/en/plugins/mods/events#handle-a-hook-that-fails) covers `.catch` for other events.

## Next steps

* [Plugin security](/docs/en/plugins/security): what any plugin can do on a user's machine, and how to review one before it's installed
* [Mods overview](/docs/en/plugins/mods/overview): what a mod is and how it compares to hooks, skills, and MCP servers
* [The order mods run in](/docs/en/plugins/mods/events#the-order-mods-run-in): how `prependPlugins` and `appendPlugins` fit with users' mods
* [Settings and environment variables](/docs/en/plugins/mods/reference#settings-and-environment-variables): every setting named on this page in one table
