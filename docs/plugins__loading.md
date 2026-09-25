> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Plugin loading reference

> Trace where Claude Code loads each plugin from, which settings file decides whether it loads, and why an update changed nothing.

Use this page when a plugin didn't load, loaded a different copy than you expected, or didn't pick up an update, and you want to see which source, settings scope, or file on disk decided that. It gives the rules Claude Code applies when a session starts and each time you run `/reload-plugins`. You can also ask Claude to read this page and diagnose your setup.

<Note>
  These cases are covered on other pages:

  * **Install, enable, disable, and update steps**: see [Install and manage plugins](/docs/en/plugins/install)
  * **You have a specific error message**: see [Troubleshoot plugins](/docs/en/plugins/troubleshooting)
</Note>

Start with [Check which stage a plugin reached](#check-which-stage-a-plugin-reached) for the three stages an installed plugin passes through, or go to the section that matches what you're seeing:

* A plugin you turned off still loads: [Find where a plugin is enabled](#find-where-a-plugin-is-enabled)
* An update changed nothing: [Versions and updates](#versions-and-updates)
* You're looking at the files under `~/.claude/plugins/`: [Find plugins on disk](#find-plugins-on-disk)
* A `--plugin-dir` plugin didn't load, or a same-named plugin loaded instead: [Name conflicts](#name-conflicts)

## Check which stage a plugin reached

An `enabledPlugins` entry becomes a plugin you can use in stages: your settings declare it, Claude Code fetches it to disk, and the running session loads it. When a plugin doesn't behave as a settings file suggests, check which stage it reached:

* **Declared, in settings**: `enabledPlugins` says which plugins should be on, and `extraKnownMarketplaces` says which marketplaces should exist. When you run `claude plugin marketplace add`, Claude Code writes the marketplace to `extraKnownMarketplaces` in your user settings as well as to disk
* **Fetched, on disk under `~/.claude/plugins/`**: the records of what Claude Code has fetched, and the fetched files themselves:
  * `known_marketplaces.json` records each marketplace Claude Code has fetched, with its `source`, `installLocation`, `lastUpdated`, and `autoUpdate`. There is one `known_marketplaces.json` per user, so a marketplace you add in one project is available in every project
  * `installed_plugins.json` records each install with its `scope`, `installPath`, and `version`
  * `cache/` holds the plugin files
* **Loaded, in the running session**: the plugin set Claude Code loaded at startup or at the last `/reload-plugins`. Changes to settings or to disk don't reach this layer until you run `/reload-plugins` or start a new session. That is why `claude plugin update` ends with `Restart to apply changes.` and background updates prompt you with `Run /reload-plugins to apply`

### Plugins and marketplaces that aren't on disk at session start

Plugins load at session start from `installed_plugins.json` and the cache without using the network. After the session starts, Claude Code checks the declared marketplaces in the background:

* **A marketplace that settings declare but `known_marketplaces.json` lacks**: Claude Code clones it, then reloads plugins and downloads enabled plugins that aren't cached yet
* **A declared marketplace whose source changed in settings**: Claude Code re-fetches it from the new source and shows `Plugins changed. Run /reload-plugins to activate.`

An enabled plugin that neither path fetched and that has no usable cache directory shows `Plugin "<name>" not cached at <path>` in the `/plugin` **Errors** tab, and `claude plugin list` adds `— run /plugin to refresh` to the same line. For the fix, see [`Plugin "<name>" not cached at <path>`](/docs/en/plugins/troubleshooting#plugin-not-cached-at).

## Find where a plugin came from

Every plugin has an id of the form `<name>@<origin>`, which is what you see in settings files and in `claude plugin list --json`. The part after `@` tells you where Claude Code found the plugin:

| ID ends in       | How the plugin got there                                                                                                                                                                                | How you turn it on or off                                                                                                                                           |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `@<marketplace>` | You installed it from a marketplace you added                                                                                                                                                           | `"<name>@<marketplace>": true` or `false` under `enabledPlugins` in a settings file                                                                                 |
| `@inline`        | You started Claude Code with `--plugin-dir` or `--plugin-url`, set [`CLAUDE_CODE_PLUGIN_DIRS`](/docs/en/env-vars#variables), or an Agent SDK app passed the `plugins` option. It loads for that session only | On for the session unless the manifest sets `defaultEnabled: false` or a settings file sets `"<name>@inline": false`                                                |
| `@skills-dir`    | You saved a plugin directory that has a `.claude-plugin/plugin.json` under `~/.claude/skills/` or the project's `.claude/skills/`                                                                       | The manifest's `defaultEnabled`, unless a settings file sets `"<name>@skills-dir"` to `true` or `false`                                                             |
| `@synced`        | You or your organization turned it on for your claude.ai account, and Claude Code [downloaded it](#synced-plugins)                                                                                      | On unless the manifest sets `defaultEnabled: false` or a settings file sets `"<name>@synced": false`. A plugin your organization marks as required loads regardless |

For a marketplace plugin, `<name>` is the entry name in `marketplace.json`; for `@inline` and `@skills-dir` it's the `name` in the plugin's manifest.

The origin names in this table are reserved, so no marketplace can be named `inline`, `skills-dir`, or `synced`.

### Entry name and manifest name

A marketplace plugin has two names, and they can differ:

* **The entry name in `marketplace.json`**: the install and enable key. It's what you write in `enabledPlugins`, what the cache directory is named after, and what `claude plugin list` shows
* **The `name` in the manifest**: what the plugin's components are namespaced under, and what [name conflicts](#name-conflicts) compare

### Plugins shared through a repository

To share a plugin through a repository, list it under `enabledPlugins` in `.claude/settings.json` or place it under `.claude/skills/`. Claude Code doesn't scan a project's `.claude/plugins/` directory.

A cloud session doesn't add the marketplaces a repository lists under [`extraKnownMarketplaces`](/docs/en/settings-reference#extraknownmarketplaces), because that requires the workspace trust dialog, which a cloud session never shows.

A project-scope skills-directory plugin loads only from the `.claude/skills/` of the session's [primary working directory](/docs/en/permissions#working-directories), and only after you accept the [workspace trust dialog](/docs/en/permissions#what-runs-before-you-trust-a-folder) for that folder. It doesn't [search parent directories up to the repository root](/docs/en/skills#discovery-from-parent-and-nested-directories) the way plain skills and commands do. If you launch from a subdirectory, a plugin at the repository root doesn't load. Launch from the repository root instead, or [move the session there with `/cd`](/docs/en/permissions#move-the-session-to-another-directory) on v2.1.246 or later.

A project-scope plugin is checked into the repository and reaches every collaborator who clones it. Because that content comes from the repository rather than from you, it loads only after the same trust check that applies to project allow rules in `.claude/settings.json`. Trusting a parent folder or running with `-p` isn't enough. Components that run code are restricted further:

* MCP servers it declares go through the [same per-server approval](/docs/en/mcp) as a project `.mcp.json`
* MCP servers it declares as an [MCP bundle](/docs/en/plugins/manifest-reference#mcpservers), a `.mcpb` or `.dxt` file, or from a file outside the plugin directory are skipped. Declare them inline or in a `.mcp.json` inside the plugin directory
* [Background monitors](/docs/en/plugins/components#monitors) do not load

Personal-scope plugins have none of these restrictions.

For how to write `--plugin-dir` and skills-directory plugins, see [Create plugins](/docs/en/plugins/create).

<h3 id="synced-plugins">
  Plugins synced from claude.ai
</h3>

A plugin you turn on for your claude.ai account also loads in Claude Code, alongside the plugins you install from marketplaces. That includes plugins your organization turns on for its members. Each of these plugins loads as `<name>@synced`, with no marketplace and no [install record](#check-which-stage-a-plugin-reached).

In terminal sessions, a synced plugin's skills, agents, hooks, MCP servers, and LSP servers all load, with the same trust as a marketplace plugin you installed.

For the components Cowork loads, see [Plugins on claude.ai and in Cowork](https://claude.com/docs/plugins/overview) on claude.com.

Synced plugins load in Cowork sessions and in terminal sessions where you sign in with your claude.ai account:

* **[Cowork](https://claude.com/product/cowork)**: Claude Code downloads them into the session's own environment when the session starts
* **Terminal sessions**: each time you start Claude Code, it syncs once in the background, downloading new and updated plugins and removing the ones that you or your organization turned off. Syncing in terminal sessions requires Claude Code v2.1.273 or later

#### Sync timing in terminal sessions

Because the terminal sync runs in the background, it can finish after your session has started. When it adds, updates, or removes a synced plugin in an interactive session, you see `Plugins changed. Run /reload-plugins to activate.` Run `/reload-plugins` to load the change in that session, or leave it for the next time you start Claude Code.

If you enable a plugin on claude.ai while a session is running, the plugin downloads the next time you start Claude Code.

#### Sign-in requirements for terminal sync

In your terminal, plugins sync only in sessions where you sign in with your claude.ai account.

If you signed in on an earlier version of Claude Code, that sign-in doesn't cover plugins until Claude Code renews it in the background. To get access sooner, run `/login` again. Plugin sync then starts the next time you start Claude Code.

#### Control which synced plugins load

You can turn synced plugins off one at a time, except a plugin your organization requires, or turn off every synced plugin on the machine:

* **One plugin**: `claude plugin disable <name>@synced` in your shell and the `/plugin` **Installed** tab in a session both save `"<name>@synced": false` in your user-level [`enabledPlugins`](/docs/en/settings-reference#enabledplugins). To keep the plugin out of a project in every environment, set the same key in the project's committed `.claude/settings.json`
* **Every synced plugin on a machine**: set [`syncClaudeAiPlugins`](/docs/en/settings-reference#syncclaudeaiplugins) to `false` in your user settings, or your organization sets it in [managed settings](/docs/en/managed-settings). Claude Code stops downloading, and the next time you start it, it moves the plugins it already synced to `~/.claude/plugins/.trash/` and no longer loads them. If your organization turns off Skills on claude.ai, plugins stop syncing too
* **A plugin your organization requires**: a plugin that your organization marks as required on claude.ai loads even if you disabled it earlier. `claude plugin disable` refuses it with `Plugin "<name>@synced" is required by your organization and can't be disabled here. Contact your admin to change it.`, and `claude plugin list` marks it `required by your org`

For removing a plugin on claude.ai, see [Manage installed plugins](/docs/en/plugins/install#manage-installed-plugins).

## Find where a plugin is enabled

You can set an `enabledPlugins` entry in any of six sources. The table lists them from lowest precedence to highest, and who each one applies to. For the settings files themselves, see [Settings files and who they affect](/docs/en/settings#where-settings-live).

| Source      | Where you set it                                                                                  | Reaches                                                                                                   |
| :---------- | :------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------- |
| `--add-dir` | `.claude/settings.json` or `.claude/settings.local.json` in a directory you pass with `--add-dir` | This session only. Only a `true` value has an effect, and every other source overrides it                 |
| `user`      | `~/.claude/settings.json`                                                                         | You, in every project                                                                                     |
| `project`   | `.claude/settings.json`                                                                           | Everyone who clones the repository                                                                        |
| `local`     | `.claude/settings.local.json`                                                                     | You, in this repository only                                                                              |
| `flag`      | The `--settings` value you pass at launch                                                         | This session only                                                                                         |
| `managed`   | [Managed settings](/docs/en/managed-settings)                                                          | Every user the policy covers. `true` force-enables and `false` blocks, and no other source overrides them |

These sources merge key by key. For each plugin id, the value that applies is the one from the highest-precedence source that mentions the id. A source that doesn't mention the id leaves the value from the lower-precedence source in effect.

### Disabled in user settings but still loads

If you set a plugin to `false` in `~/.claude/settings.json` and it still loads, a `true` in a higher-precedence source is overriding it. The plugin's row in `claude plugin list` and in `/plugin` shows `Disabled in ~/.claude/settings.json but still loads — project settings enable it, which overrides your user setting`. The message names the source that overrode you: `project`, `project, gitignored` for `.claude/settings.local.json`, `cli flag`, or `managed`.

To opt out of a project-enabled plugin on your machine, set the id to `false` in `.claude/settings.local.json`, which has higher precedence than the project file.

### Enabled in project settings but not installed

When a plugin's only `true` is in the project's `.claude/settings.json`, Claude Code doesn't fetch it onto a machine where it isn't installed, unless its marketplace entry has a [relative-path source](/docs/en/plugins/marketplace-reference#plugin-sources) or a [seed directory](/docs/en/plugins/org#seed-containers-and-ci) already holds it. Instead, the `/plugin` **Errors** tab shows `Plugin "<name>" is enabled in project settings but isn't installed here`.

A relative-path plugin needs no install record because it loads from the marketplace itself.

Claude Code fetches a plugin with an external source only when one of these sources sets it to `true`:

* Your user settings
* A `.claude/settings.local.json` that git doesn't track
* The `--settings` flag
* Managed settings

## Find plugins on disk

Claude Code keeps plugin files and state records under one plugins root, which is `~/.claude/plugins` unless you set [`CLAUDE_CODE_PLUGIN_CACHE_DIR`](/docs/en/env-vars). Every path in the table is relative to that root.

| Path                                                   | What it holds                                                                                                                                                                                                                                                                                                                                                                                                  |
| :----------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cache/<marketplace>/<plugin>/<version>/`              | One directory per installed version of a marketplace plugin. `<plugin>` is the marketplace entry name and `<version>` is the [resolved version](#versions-and-updates). `${CLAUDE_PLUGIN_ROOT}` points at this directory                                                                                                                                                                                       |
| `data/<plugin-id>/`                                    | The plugin's persistent directory, exposed as `${CLAUDE_PLUGIN_DATA}`. For how `<plugin-id>` is formed, see [Path variables and persistent data](/docs/en/plugins/components#path-variables-and-persistent-data). Claude Code creates it when a plugin component first uses it and keeps it across updates. Claude Code deletes it when you uninstall the plugin from its last scope, unless you pass `--keep-data` |
| `marketplaces/<name>/`                                 | The clone or download of a marketplace added from GitHub, another Git host, or a URL. A marketplace added from a local `file` or `directory` source has no copy here, and its `installLocation` in `known_marketplaces.json` is the path you gave                                                                                                                                                              |
| `synced/`                                              | The plugins Claude Code [synced from your claude.ai account](#synced-plugins)                                                                                                                                                                                                                                                                                                                                  |
| `.trash/`                                              | Plugins that the claude.ai sync removed, such as after you turn one off on claude.ai or stop syncing                                                                                                                                                                                                                                                                                                           |
| `installed_plugins.json` and `known_marketplaces.json` | The records of what Claude Code has installed and which marketplaces it has fetched, described under [Check which stage a plugin reached](#check-which-stage-a-plugin-reached). A [marketplace hosted on claude.ai](/docs/en/plugins/install#add-from-claude-ai) is recorded in `known_marketplaces_claudeai.json` instead                                                                                          |
| `flagged-plugins.json`                                 | Plugins Claude Code uninstalled because their marketplace delisted them. They appear in the **Flagged** section of `/plugin`; see [Host a marketplace](/docs/en/plugins/host-marketplace)                                                                                                                                                                                                                           |

Because `${CLAUDE_PLUGIN_ROOT}` points at a version directory, a plugin's root path changes with every version. Keep a plugin's durable files in `${CLAUDE_PLUGIN_DATA}` instead.

### In-place and copied plugins

Claude Code loads some plugins in place from where you keep them and copies the rest into the cache, according to their origin:

* **`--plugin-dir` and skills-directory plugins**: the directory loads in place and is never copied. A `--plugin-url` archive or a `--plugin-dir` `.zip` is extracted into a session temp directory first
* **Relative-path plugins in a marketplace you added from a local directory**: the plugin loads in place from its path inside the marketplace folder. Your edits to the source directory take effect at the next session start or `/reload-plugins`, and you don't need to increase the version. The plugin's hook processes and MCP and LSP servers receive a `CLAUDE_PLUGIN_ROOT` that points at the source directory. For its Node.js package dependencies, see [When the dependency install runs](#when-the-dependency-install-runs)
* **`command`-source plugins in [link mode](/docs/en/plugins/marketplace-reference#command-plugin-source)**: the directory the command printed loads in place, through links in the cache entry
* **Every other marketplace plugin**: Claude Code copies the plugin into `cache/<marketplace>/<plugin>/<version>/` at install and loads that copy. Files outside the plugin directory aren't copied, so when a script inside a copied plugin reads a path above the plugin root, such as `../shared`, it doesn't find them

### Paths that escape the plugin directory

Whether a plugin loads in place or from a cached copy, Claude Code doesn't let it declare components outside its own directory. It rejects a component path that resolves outside the plugin root, whether the path is declared in `plugin.json` or in a marketplace entry:

* **A path that points outside the plugin as written**, such as `../shared-utils`
* **A symlink that leads outside the plugin**, other than [links between plugins within one marketplace](/docs/en/plugins/host-marketplace#share-files-within-a-marketplace-with-symlinks)
* **On macOS and Linux, a path that contains a backslash anywhere in it**, even when the path stays inside the plugin. Components declared with backslash paths therefore load on Windows only, so write component paths with forward slashes, such as `./commands/deploy.md`

A rejected path appears as a [`path escapes plugin directory`](/docs/en/errors#path-escapes-plugin-directory) error, and the plugin loads without that component.

### Cleanup of previous versions

When you update or uninstall a plugin, Claude Code writes an `.orphaned_at` marker into the previous version directory. It removes that directory in a background cleanup 14 days later, so a session that already loaded the old version keeps running.

The sweep runs only while `installed_plugins.json` records at least one install. After you uninstall your last plugin, orphaned directories stay until you install another.

### Node.js package dependencies

When Claude Code copies a plugin into the cache, it also installs the plugin's Node.js package dependencies there, so the plugin's hooks and MCP servers can load them.

This section covers the npm and Bun packages a plugin declares in its own `package.json`. For plugins that depend on other plugins, see [plugin dependency versions](/docs/en/plugins/dependencies).

#### When the dependency install runs

Claude Code runs the install inside the copied version directory each time it creates one:

* When you install a plugin
* When Claude Code updates a plugin to a new version
* At session start when an enabled plugin isn't cached yet, such as on a new machine

For a relative-path plugin [loaded in place](#in-place-and-copied-plugins) from a local-directory marketplace, Claude Code doesn't install the dependencies into the source directory. Install them there yourself, or from a hook into [`${CLAUDE_PLUGIN_DATA}`](/docs/en/plugins/components#path-variables-and-persistent-data).

The install runs only when the plugin's root directory contains both a `package.json` and a supported lockfile. The lockfile decides which command Claude Code runs:

| Lockfile                                     | Command                                          |
| :------------------------------------------- | :----------------------------------------------- |
| `bun.lock` or `bun.lockb`                    | `bun install --frozen-lockfile --ignore-scripts` |
| `npm-shrinkwrap.json` or `package-lock.json` | `npm ci --ignore-scripts`                        |

If a plugin contains more than one of these lockfiles, Claude Code uses the first match, checking in order: `bun.lock`, `bun.lockb`, `npm-shrinkwrap.json`, `package-lock.json`.

Claude Code skips the install for Yarn and pnpm lockfiles and for a `bunfig.toml` beside the Bun lockfile:

* If your plugin has only a `yarn.lock` or `pnpm-lock.yaml`, replace it with an npm lockfile
* If a `bunfig.toml` is in the same directory as the Bun lockfile, remove the `bunfig.toml`, or replace the Bun lockfile with an npm lockfile

Include an npm lockfile to reach the most users. Claude Code runs the matched lockfile's package manager from the user's PATH and doesn't try the other lockfile instead if that package manager is missing.

For a plugin distributed through an npm source, use `npm-shrinkwrap.json`, because npm excludes `package-lock.json` from published packages.

#### Limits on the dependency install

Claude Code constrains this dependency install so that no code from the plugin or its packages executes during it, and bounds how long it can run:

* **Frozen resolution**: Bun and npm install exactly what the lockfile pins, and fail rather than re-resolve versions when `package.json` and the lockfile disagree
* **No lifecycle scripts**: `--ignore-scripts` keeps `preinstall`, `install`, and `postinstall` scripts from running, so dependencies that build native modules in those scripts download but don't compile during this install
* **60-second timeout**: Claude Code stops an install that runs longer and treats it as failed

Claude Code fetches an npm-source plugin before this dependency install, and none of the package's own install scripts run during the fetch. See [npm plugin source](/docs/en/plugins/marketplace-reference#npm-plugin-source).

You can't turn the automatic install off. No setting or environment variable disables it.

In restricted networks, see the [network access requirements](/docs/en/network-config#network-access-requirements) for the hosts to allow.

#### When the dependency install fails or is skipped

A failed or skipped install never blocks the plugin, and each case leaves a different sign:

* A failed install, or one skipped because of a Yarn or pnpm lockfile or a `bunfig.toml`, appears as a warning in the `claude --debug` output
* A plugin with a `package.json` and no lockfile is skipped without a log entry
* A timed-out install can leave a partial `node_modules` tree in the cached copy

When the automatic install can't provide a dependency, install it from a hook into the [persistent data directory](/docs/en/plugins/components#path-variables-and-persistent-data). That includes packages that need their lifecycle scripts to build, Python dependencies, and plugins locked with Yarn or pnpm.

## Versions and updates

If a plugin's author pushed new commits and `claude plugin update` prints `<name> is already at the latest version (<version>).`, the version Claude Code computes for the plugin is unchanged, so nothing changes on disk.

Claude Code computes a version for every plugin it installs, and that version is how it detects an update. `claude plugin update` and background auto-update compute the version again and skip the plugin when it matches what `installed_plugins.json` records.

The version also names the plugin's cache directory.

A manifest that pins `"version"` is one way the computed version stays the same across commits. See [How Claude Code computes the version](#how-claude-code-computes-the-version) for the resolution order.

A plugin [loaded in place](#in-place-and-copied-plugins) from a local-directory marketplace loads its current source files at every session start, whatever its version string says. For a plugin from a [marketplace hosted on claude.ai](/docs/en/plugins/install#add-from-claude-ai), the version claude.ai records for the plugin is its version, and the manifest's `version` isn't read.

### How Claude Code computes the version

For a marketplace you added by source, Claude Code picks the rule by the `source` type of the plugin's marketplace entry. The [marketplace reference](/docs/en/plugins/marketplace-reference#plugin-sources) lists the source types. For every source type in that list except `command`:

1. The `version` field in the plugin's manifest comes first
2. Then the `version` field in the plugin's marketplace entry
3. When neither is set, the version comes from the source type:

| Source type                                                                                | Version when no `version` field is set                                                                                                               |
| :----------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| `github`, `url`, or `git-subdir`                                                           | The commit SHA of the source, shortened to 12 characters. A `git-subdir` version also carries a hash of the subdirectory path                        |
| `archive`                                                                                  | The SHA-256 digest, shortened to 12 characters: the `sha256` pin in the marketplace entry, or the digest of the downloaded file when there is no pin |
| Relative path inside a Git-hosted marketplace                                              | The commit SHA of the installed directory                                                                                                            |
| Local directory, when neither the plugin directory nor its marketplace is a git repository | `unknown`                                                                                                                                            |
| `npm`                                                                                      | `unknown`                                                                                                                                            |

Claude Code doesn't take the version from a repository that encloses the install path, such as a git-managed `~/.claude`.

For a `command` source, Claude Code always derives the version from what the command produced: a 12-character hash on its own, or `<manifest version>-<hash>` when the manifest sets one. The marketplace entry's `version` is ignored for command sources. For what the hash covers, see [Copy mode and link mode](/docs/en/plugins/marketplace-reference#copy-mode-and-link-mode).

Because the manifest comes first, a manifest that pins `"version": "1.0.0"` keeps every user on the cached copy until its author changes the string, however many commits they push. To let users track commits instead, leave `version` out of both the manifest and the entry. [Host a marketplace](/docs/en/plugins/host-marketplace) covers which choice fits which release setup.

### When Claude Code refreshes a marketplace before an install

When you install a plugin, Claude Code looks it up in its local copy of the marketplace catalog. You can run `/plugin install` in a session or `claude plugin install` in your shell, and name the plugin with or without its marketplace. The table shows which of those combinations refresh the local copy.

| Plugin name        | Command                                      | What Claude Code refreshes                                                   |
| :----------------- | :------------------------------------------- | :--------------------------------------------------------------------------- |
| `name@marketplace` | `/plugin install` or `claude plugin install` | The named marketplace, before the lookup                                     |
| `name` alone       | `/plugin install`                            | Only marketplaces that have auto-update on, and only after the lookup misses |
| `name` alone       | `claude plugin install`                      | Nothing. It reads the cached catalogs without refreshing                     |

The refresh before a `name@marketplace` install doesn't depend on the marketplace's auto-update setting or on `DISABLE_AUTOUPDATER`.

When the refresh fails, the install proceeds from the cached catalog and `claude plugin install` reports `marketplace not refreshed`.

Claude Code skips the refresh before a `name@marketplace` install when:

* The marketplace was added from a local `file` or `directory` source, or is defined inline in settings with a [`settings` source](/docs/en/settings-reference#extraknownmarketplaces)
* A [seed directory](/docs/en/env-vars) supplies the marketplace
* Claude Code refreshed the marketplace within the last 30 seconds
* You set `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`
* [Managed settings](/docs/en/plugins/org#restrict-what-users-can-install) block the marketplace, in which case Claude Code also refuses the install

### When auto-update runs

In an interactive session, after you send your first message, Claude Code waits a random delay of up to ten minutes. It then refreshes every marketplace with auto-update on and updates the plugins installed from them on disk.

The running session keeps the versions it loaded, and you see `Plugin updated: <name> · Run /reload-plugins to apply`. Whether or not you reload, the new versions load on your next launch.

#### Which marketplaces and plugins auto-update

Whether a marketplace auto-updates follows the first of these that is set:

1. **`autoUpdate` on its `extraKnownMarketplaces` entry** in a settings file
2. **`autoUpdate` on its `known_marketplaces.json` entry**, which the **Enable auto-update** toggle under `/plugin` **Marketplaces** writes. When a settings file also declares the marketplace under `extraKnownMarketplaces`, the toggle writes `autoUpdate` to that settings entry as well
3. **The default**: on for Anthropic's official marketplaces such as `claude-plugins-official`, off for `knowledge-work-plugins` and `first-party-plugins`, on for [marketplaces added from claude.ai](/docs/en/plugins/install#add-from-claude-ai), and off for every other marketplace

If you set `DISABLE_UPDATES=1`, `DISABLE_AUTOUPDATER=1`, or `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`, the whole pass is off and the **Enable auto-update** toggle is hidden, unless you also set `FORCE_AUTOUPDATE_PLUGINS=1`. The [environment variables reference](/docs/en/env-vars) covers each variable's wider effect.

Auto-update also skips a plugin whose marketplace entry declares a `headersHelper`. [Installs and updates that refuse a command instead of asking](/docs/en/plugins/host-marketplace#installs-and-updates-that-refuse-the-command-instead-of-asking) explains when such a plugin appears in the `/plugin` **Errors** tab and how you update it from there.

When a copied plugin updates mid-session, hook commands, monitors, MCP servers, and LSP servers keep using the previous version's path. Run `/reload-plugins` to switch hooks, MCP servers, and LSP servers to the new path. Monitors require a session restart.

### When a command source re-runs

Plugins with a `command` source don't wait for the [auto-update pass](#when-auto-update-runs). The printed directory reflects the tool's state at the time the command ran, so Claude Code runs the [command you accepted](/docs/en/plugins/host-marketplace#change-the-command-of-a-command-source) again at these times:

* Every time you install or update the plugin
* Once per session for each enabled command-sourced plugin, in the background, shortly after the session starts. This run doesn't depend on the marketplace's auto-update setting or on `DISABLE_AUTOUPDATER`
* At startup or on `/reload-plugins`, when an enabled plugin's installed version is missing from the plugin cache

Claude Code skips the two background runs when you set [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`](/docs/en/env-vars). Explicit installs and updates still run the command with that variable set.

When the command's hashed output has changed, Claude Code installs the result as a new version and reloads it in the running interactive session, switching [the same components that `/reload-plugins` switches](/docs/en/plugins/cli-reference#reload-plugins). You see a notification that the plugin was reloaded.

If reloading in place would invalidate the session's prompt cache, Claude Code instead prompts you to run `/reload-plugins`, which [warns about the cache cost and applies when rerun with `--force`](/docs/en/prompt-caching#enabling-or-disabling-a-plugin).

## Name conflicts

When enabled plugins from different origins share a manifest name, this order decides which one loads, from highest precedence to lowest:

1. A plugin whose id appears in managed settings `enabledPlugins`, as `true` or `false`. A `--plugin-dir` copy whose manifest name matches the id's name part isn't loaded, and you see `--plugin-dir copy of "<name>" ignored: plugin is locked by managed settings`
2. An enabled `--plugin-dir`, `--plugin-url`, or `CLAUDE_CODE_PLUGIN_DIRS` plugin. It replaces a same-named installed marketplace plugin or skills-directory plugin:
   * **An installed marketplace plugin**: replaced silently. `claude plugin list` still shows the marketplace row as enabled, because that row reflects your settings. Only the log Claude Code writes under `~/.claude/debug/` when you start with `--debug` records `Plugin "<name>" from --plugin-dir overrides installed version`
   * **A skills-directory plugin**: replaced with a `/plugin` **Errors** tab row that reads `Not loaded — the name "<name>" is already taken by a session-only plugin (--plugin-dir / --plugin-url), which takes precedence`
3. An installed marketplace plugin. A skills-directory plugin of the same name gets the same `Not loaded` row, naming the installed plugin
4. A skills-directory plugin. Between two of these, the copy under `~/.claude/skills/` loads and the project's `.claude/skills/` copy is dropped, with a row that says which path shadowed it
5. A plugin [synced from claude.ai](#synced-plugins). When an enabled plugin from any other origin matches its name, Claude Code loads that plugin and reports the synced copy as not loaded. To use the claude.ai copy instead, disable your own copy

Because the order compares manifest names, a `--plugin-dir` plugin named `hello-plugin` replaces `hello@example-marketplace` when that plugin's manifest also says `"name": "hello-plugin"`.

### Keep a session-only plugin from loading

To keep a `--plugin-dir` plugin from shadowing anything, or to turn one off when a parent process passes the flag for you, set its id to `false` in any settings file. For a plugin whose manifest name is `hello-plugin`, the entry is `"enabledPlugins": {"hello-plugin@inline": false}`. A disabled session-only plugin doesn't shadow, so the marketplace or skills-directory copy loads instead.

## Next steps

* [Install and manage plugins](/docs/en/plugins/install): the install, enable, disable, and update steps themselves
* [Troubleshoot plugins](/docs/en/plugins/troubleshooting): error messages by the stage that produces them
* [Plugin commands reference](/docs/en/plugins/cli-reference): the flags and commands named on this page
* [Manage plugins for your organization](/docs/en/plugins/org): the managed settings that force-enable or block plugins
