> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Manage Claude Code plugins for your organization

> Control which plugins Claude Code installs and allows across your organization through managed settings.

Managed settings let you decide which plugins Claude Code installs and allows on every machine in your organization. Users can't override them. You deliver them either as [server-managed settings](/docs/en/server-managed-settings) from the claude.ai admin console or as endpoint-managed settings through MDM or a `managed-settings.json` file. Most controls on this page take effect only from managed settings.

This page is for administrators, and the settings here govern Claude Code.

<Note>
  These cases are covered on other pages:

  * **Installing plugins for yourself**: start at [Install plugins](/docs/en/plugins/install)
  * **Controlling which plugins members can use in claude.ai and Cowork**: see [Manage plugins for your organization](https://support.claude.com/en/articles/13837433) in the help center
  * **The plugins page in claude.ai's admin settings**: [**Organization settings > Plugins & skills**](https://claude.ai/admin-settings/skills?tab=inventory) turns plugins on for members' claude.ai accounts, and those reach Claude Code as [synced plugins](/docs/en/plugins/loading#synced-plugins). It doesn't set any of the keys on this page
</Note>

The sections follow the order most rollouts take: [require plugins](#pre-install-and-require-plugins) for everyone or per repository, [seed containers and CI](#seed-containers-and-ci), [restrict](#restrict-what-users-can-install) what users can add on their own, [set update policy](#set-update-policy), then [audit](#audit-and-review) what's installed. To review every policy key in one place, see the [control matrix](#control-matrix).

## Pre-install and require plugins

A marketplace is a catalog of plugins that Claude Code fetches from a git repository, a URL, or a local path. Once you register a marketplace on a machine, Claude Code can install plugins from it.

To install plugins for a fleet, set two keys together in [managed settings](/docs/en/managed-settings), the policy file or server-delivered policy that every machine in your organization reads: `extraKnownMarketplaces` registers a marketplace on each machine, and `enabledPlugins` names the plugins to install and enable from it. [Choose a delivery mechanism](#choose-a-delivery-mechanism) covers how managed settings reach each machine.

### Choose a delivery mechanism

Managed settings reach a machine through one of three delivery mechanisms:

* **Server-managed settings**: set the plugin keys as JSON at [**Organization settings > Claude Code > Managed settings**](https://claude.ai/admin-settings/claude-code). Requires an [Owner role](/docs/en/server-managed-settings#access-control) in your Claude organization. A cloud session fetches these settings before it installs plugins.
* **MDM policies**: on macOS, deliver a plist whose top-level keys are the settings keys. On Windows, store the whole JSON document as a string in a registry value. The plist domain and the registry key are in [Where each mechanism stores the policy](/docs/en/managed-settings#where-each-mechanism-stores-the-policy).
* **Managed settings file**: place a `managed-settings.json` at the platform's system path. You can also add files to the `managed-settings.d/` drop-in directory beside it. The file paths per platform are in [Where each mechanism stores the policy](/docs/en/managed-settings#where-each-mechanism-stores-the-policy), and the drop-in merge rules are in [Split a file-based policy across teams](/docs/en/managed-settings#split-a-file-based-policy-across-teams).

Use server-managed settings if you have a Claude for Teams or Enterprise organization on claude.ai and your devices aren't all under MDM. Otherwise use an MDM policy or the managed settings file. For the trade-off, see [Choose between server-managed and endpoint-managed settings](/docs/en/server-managed-settings#choose-between-server-managed-and-endpoint-managed-settings).

#### Which managed source applies on a machine

By default, only one of these three sources applies on a machine. Claude Code uses the first that delivers a policy key, checking server-managed settings first, then MDM policies, then the managed settings file. If server-managed settings deliver even one unrelated policy key, Claude Code ignores the plugin keys in an MDM policy or managed settings file on that machine, apart from the [keys it reads from every source](/docs/en/managed-settings#keys-read-from-every-admin-source).

To apply every source instead, set [`managedSourcesBehavior`](/docs/en/managed-settings#compose-every-managed-source) to `"merge"`.

[How Claude Code combines managed sources](/docs/en/managed-settings#how-claude-code-combines-managed-sources) also lists the keys Claude Code reads from every source in both modes.

### Require a marketplace and its plugins

Add the marketplace under `extraKnownMarketplaces`, keyed by the marketplace's own `name` from its `marketplace.json`. Then add each plugin under `enabledPlugins` as `plugin-name@marketplace-name`. Each marketplace entry carries a `source` object with a `source` field naming the type, such as `github`. This managed settings example registers an organization marketplace and force-enables two plugins from it:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "your-marketplace": {
      "source": { "source": "github", "repo": "your-org/your-marketplace" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": {
    "code-formatter@your-marketplace": true,
    "deploy-helper@your-marketplace": true
  }
}
```

After the settings reach a machine, Claude Code registers the marketplace and installs the two plugins at the start of the user's next session. Users see them in `/plugin`, and disabling one at their own scope doesn't stop it from loading, because managed settings take precedence over every other scope.

To block a plugin at every scope and hide it from the marketplace listing, set it to `false` in the managed `enabledPlugins` instead.

Adjust the `autoUpdate` and `source` fields for your marketplace:

* **`autoUpdate`**: `true` keeps the marketplace and its plugins refreshing in the background, and `false` turns that off. See [Set update policy](#set-update-policy).
* **`source`**: `github` is one of several source types. A `git` source takes a `url` for GitLab or an internal host, and a `url` source takes the address of a hosted `marketplace.json`. Every source shape is in the [marketplace reference](/docs/en/plugins/marketplace-reference).

If the marketplace is a private git repository, each user needs read access to it. The clone of a git-based marketplace runs with git on the user's machine, using stored credentials and no prompts. For users without git-host accounts, use a [seed](#seed-containers-and-ci) instead.

A managed entry also overrides a same-name marketplace entry or `--plugin-dir` copy from another source:

* **Marketplaces**: a managed marketplace entry replaces a lower-precedence entry with the same name, and the two entries' fields don't merge.
* **`--plugin-dir` copies**: `--plugin-dir` loads a plugin from a local directory for one session. For what happens when that copy's name matches a plugin your managed `enabledPlugins` names, see [Name conflicts](/docs/en/plugins/loading#name-conflicts).

Anthropic's official marketplace `claude-plugins-official` needs no `extraKnownMarketplaces` entry when `enabledPlugins` sets one of its plugins to `true`. That `name@claude-plugins-official` entry declares the marketplace by itself, wherever these keys apply. If you enable none of its plugins and still want it registered on every machine, give it an explicit entry, as [Allow the official marketplace and your own](#allow-the-official-marketplace-and-your-own) does.

### Require plugins per repository

To cover one repository's contributors instead of your whole fleet, set `extraKnownMarketplaces` and `enabledPlugins` in that repository's `.claude/settings.json`. The `extraKnownMarketplaces` entries apply only in a folder the contributor has trusted, and in an untrusted folder Claude Code ignores them without a message:

* **Interactive sessions**: Claude Code registers the marketplace only after the contributor accepts the [workspace trust dialog](/docs/en/permissions#what-runs-before-you-trust-a-folder) for that folder.
* **[Non-interactive `-p` runs](/docs/en/headless)**: the entries apply only in a folder whose trust the user already accepted interactively, or whose `hasTrustDialogAccepted` flag you set in `~/.claude.json`.

A plugin that the marketplace lists by a relative path loads from the marketplace copy once the repository's `extraKnownMarketplaces` entries apply. A plugin whose marketplace entry points at an external source instead, such as the plugin's own GitHub repository, doesn't install from the repository's settings alone. Each contributor sees `Plugin "<name>" is enabled in project settings but isn't installed` until they run `claude plugin install <name>@<marketplace> --scope project`, as [Install plugins](/docs/en/plugins/install) describes.

If you use a local `directory` or `file` source with a relative path, the path resolves against your repository's main checkout. When you run Claude Code from a git worktree, the path still points at the main checkout, so all worktrees share the same marketplace location.

To roll out a bundle of plugins with dependencies, put the bundle plugin in `enabledPlugins`, as [Plugin dependencies](/docs/en/plugins/dependencies) describes.

### When each surface applies the plugin keys

The table shows when each kind of Claude Code session applies `extraKnownMarketplaces` and `enabledPlugins`, from managed settings and from a repository's `.claude/settings.json`. For the Desktop app and the IDE extensions, see [Install a plugin](/docs/en/plugins/install#install-a-plugin).

| Surface               | Managed `extraKnownMarketplaces` and `enabledPlugins`                                                                                                                                                                                                                                                                               | Repository `.claude/settings.json`                                                           |
| :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- |
| Terminal, interactive | Applied at session start on every machine that receives the settings                                                                                                                                                                                                                                                                | `extraKnownMarketplaces` applied after trust; `enabledPlugins` applied at session start      |
| `-p` and CI           | Applied at session start, with installs running in the background                                                                                                                                                                                                                                                                   | `extraKnownMarketplaces` in trusted folders only; `enabledPlugins` applied                   |
| Cloud sessions        | In an Anthropic-hosted environment, only server-managed settings reach the session, which waits for them before it installs plugins. MDM policies and managed settings files stay on the user's machine. For a self-hosted environment, see [Where and when a policy applies](/docs/en/managed-settings#where-and-when-a-policy-applies) | See the **Cloud session** tab under [Install a plugin](/docs/en/plugins/install#install-a-plugin) |

In a `-p` or CI run, marketplaces and plugins install in the background, so a plugin can be missing from the first turn. Set `CLAUDE_CODE_SYNC_PLUGIN_INSTALL=1` to make the run wait for the install before its first query.

### Confirm the rollout

Check that the marketplace and plugins arrived on a machine or in a CI run:

* **On one machine**: start Claude Code and run `/plugin`. The marketplace and the plugins are listed.
* **In CI**: run `claude -p` with `--output-format stream-json --verbose`. The `init` event lists the loaded plugins under `plugins`.

## Seed containers and CI

For container images and CI runners that can't clone at runtime, pre-populate a plugins directory at build time and point `CLAUDE_CODE_PLUGIN_SEED_DIR` at it. Claude Code registers the seed's marketplaces at startup and loads plugin caches from the seed in place, without cloning.

A seed also serves users who have no git-host account.

<Note>
  In CI/CD environments, configure a git credential helper before installing plugins from private repositories. On GitHub Actions, export a token with read access to the marketplace repository as `GH_TOKEN`, then run `gh auth setup-git`. The default workflow token can only access the workflow's own repository, so a private marketplace in another repository needs a personal access token or app token.
</Note>

<Steps>
  <Step title="Install into the seed at build time">
    Set `CLAUDE_CODE_PLUGIN_CACHE_DIR` to the seed path so the marketplace and plugins install there instead of `~/.claude/plugins`:

    ```bash theme={null}
    CLAUDE_CODE_PLUGIN_CACHE_DIR=/opt/claude-seed claude plugin marketplace add your-org/your-marketplace
    CLAUDE_CODE_PLUGIN_CACHE_DIR=/opt/claude-seed claude plugin install code-formatter@your-marketplace
    ```

    The seed has the same layout as `~/.claude/plugins`: `known_marketplaces.json`, `marketplaces/<name>/`, and `cache/<marketplace>/<plugin>/<version>/`. You can mount the seed at a different path than you built it at.
  </Step>

  <Step title="Point the runtime at the seed">
    Set `CLAUDE_CODE_PLUGIN_SEED_DIR=/opt/claude-seed` in the container's environment. To use several seeds, separate their paths with `:` on Unix or `;` on Windows. Claude Code uses the first seed that contains a given marketplace or plugin cache.
  </Step>

  <Step title="Enable the plugins">
    The plugins in a seed aren't enabled on their own. Set `enabledPlugins` for each seed plugin you want loaded, in managed settings or in the repository's `.claude/settings.json`.
  </Step>
</Steps>

To verify a seed, run `claude -p` with `--output-format stream-json --verbose` in the image. In the `init` event's `plugins` list, each loaded plugin's `path` is under the seed, such as `/opt/claude-seed/cache/your-marketplace/code-formatter/1.0.0`.

Seed marketplaces follow these rules:

* **Read-only**: Claude Code never writes to the seed and forces `autoUpdate` off for seed marketplaces.
* **Seed entries take precedence**: on each startup, a marketplace declared in the seed overwrites the user's entry of the same name. Users opt out of a seed plugin with `claude plugin disable`, not by removing the marketplace.
* **Update and remove fail**: `claude plugin marketplace update <name>` and `remove` without `--scope` on a seed marketplace fail with a message that names the seed directory.
* **Policy still applies**: the [allowlist and blocklist](#restrict-what-users-can-install) check a seed marketplace's recorded source too. Allow the source you built the seed from.

For fleets with no outbound git access, combine a seed with `directory` or `file` marketplace sources on a shared mount. Set `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` as well, which also turns off [plugin auto-update](/docs/en/plugins/loading#when-auto-update-runs). If a proxy is available, see [Proxy configuration](/docs/en/network-config#proxy-configuration) for the variables to set.

## Restrict what users can install

The managed `strictKnownMarketplaces` allowlist and `blockedMarketplaces` blocklist decide which marketplace sources plugins may come from. A marketplace's source is the git repository, URL, or local path that Claude Code fetches it from. Both lists match the source of the marketplace a plugin comes from, not the plugin's own entry inside that marketplace.

For the common lockdown, which allows the official marketplace and your own, see [Allow the official marketplace and your own](#allow-the-official-marketplace-and-your-own). Pair it with [`disableSideloadFlags`](#control-matrix) so users can't load plugins from a local directory or URL either.

Both lists apply before anything downloads and again at session start:

* **Before a download**: the lists apply when a user adds a marketplace and on every install, update, refresh, and auto-update.
* **At session start**: the lists apply again to plugins that are already installed, so an installed plugin whose marketplace source no longer matches doesn't load. `/plugin` lists it with `Marketplace "<name>" is not in the allowed marketplace list` or `Marketplace "<name>" is blocked by enterprise policy`.

Where the two lists are enforced depends on where you set them:

* **The claude.ai admin console**: Claude Code enforces both lists in the sessions that [read server-managed settings](/docs/en/managed-settings#where-and-when-a-policy-applies). claude.ai also checks them when anyone in your organization adds a new marketplace from a git repository on claude.ai, or from **Customize** in the Claude Desktop app outside its Code tab. That covers a marketplace a member adds for their own account and one added for the whole organization under [**Organization settings > Plugins**](https://claude.ai/admin-settings/plugins). claude.ai refuses a repository that the allowlist doesn't admit or that the blocklist names. It doesn't re-check a marketplace that was added in either place before you set the lists, and it doesn't check uploaded plugins.
* **A managed settings file, OS-level policy, or other managed source**: Claude Code enforces both lists where it reads that source. claude.ai doesn't read it.

While any allowlist is set, or a blocklist names any source other than [`skills-dir`](#blocklist-with-blockedmarketplaces), a plugin whose marketplace Claude Code can't find doesn't load. `/plugin` shows the policy error for it rather than a not-found error. The common case is a stale `enabledPlugins` entry for a marketplace nobody registered.

### Control matrix

The table lists each plugin policy key, what it enforces, and what it can't do.

| Key                                                                      | What it enforces                                                                                                                                                                                                                                                        | What it can't do                                                                                                                                                                                                     |
| :----------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `strictKnownMarketplaces`                                                | Allowlist of marketplace sources. `[]` blocks every source, including the official marketplace. Alias: `allowedMarketplaces`                                                                                                                                            | Doesn't register a marketplace, restrict entries inside an allowed marketplace, or block `--plugin-dir`                                                                                                              |
| `blockedMarketplaces`                                                    | Blocklist of marketplace sources, checked before the allowlist                                                                                                                                                                                                          | Doesn't block a marketplace already registered from a source it doesn't match                                                                                                                                        |
| `syncClaudeAiPlugins`                                                    | Set `false` to stop Claude Code downloading and loading the plugins [synced from claude.ai](/docs/en/plugins/loading#synced-plugins) for each user's account. Requires Claude Code v2.1.273 or later                                                                         | Doesn't turn off one synced plugin. For that, set `"<name>@synced": false` in [`enabledPlugins`](/docs/en/settings-reference#enabledplugins)                                                                              |
| `enabledPlugins`                                                         | `true` force-enables, `false` blocks at every scope and hides the plugin                                                                                                                                                                                                | Doesn't install a plugin whose marketplace isn't registered or allowed                                                                                                                                               |
| `disableSideloadFlags`                                                   | Rejects `--plugin-dir`, `--plugin-url`, `--agents`, the Agent SDK `plugins` option, and non-SDK `--mcp-config` at startup, and rejects folders named in the [`CLAUDE_CODE_PLUGIN_DIRS`](/docs/en/env-vars#variables) variable the same way                                   | Doesn't restrict `.mcp.json`, `claude mcp add`, or SDK-provided servers. Pair it with [`allowedMcpServers`](/docs/en/managed-mcp)                                                                                         |
| `disableCommandPluginSources`                                            | Blocks plugins with a `command` source from installing, updating, or loading. A `command` source is one whose plugin directory is produced by running a command on the machine. When unset, it takes the value of `allowManagedHooksOnly`                               | Doesn't affect other source types                                                                                                                                                                                    |
| `allowManagedHooksOnly`                                                  | Restricts which hooks run. See [`allowManagedHooksOnly`](/docs/en/settings-reference#allowmanagedhooksonly)                                                                                                                                                                  | Doesn't trust hooks from plugins users enable themselves                                                                                                                                                             |
| `strictPluginOnlyCustomization`                                          | Blocks skills, agents, hooks, and MCP servers that don't come from a plugin, managed settings, or Claude Code's built-ins. Set `true` to cover all four types, or an array of `skills`, `agents`, `hooks`, and `mcp` values such as `["skills", "hooks"]` to cover some | Doesn't restrict which plugins users install. Pair it with `strictKnownMarketplaces`                                                                                                                                 |
| `pluginSuggestionMarketplaces`                                           | Marketplaces whose plugins may appear as install suggestions. See [Recommend plugins](#recommend-plugins)                                                                                                                                                               | Doesn't affect the built-in tips                                                                                                                                                                                     |
| `pluginTrustMessage`                                                     | Appends your text to the trust warning that `/plugin` shows before a plugin installs                                                                                                                                                                                    | Doesn't change the warning's own text                                                                                                                                                                                |
| `allowedChannelPlugins`                                                  | Replaces the default list of plugins allowed to push channel messages. Requires `channelsEnabled: true`                                                                                                                                                                 | See [Restrict which channel plugins can run](/docs/en/channels#restrict-which-channel-plugins-can-run)                                                                                                                    |
| [`CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL=1`](/docs/en/env-vars) | Stops interactive terminal sessions from auto-registering the official marketplace                                                                                                                                                                                      | Doesn't remove a marketplace already registered. The allowlist and blocklist gate the same auto-registration without it. A machine that started once with it set doesn't resume auto-registration after you unset it |

Every key in the table is a managed setting, apart from `enabledPlugins`, `syncClaudeAiPlugins`, and `CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL`:

* **`enabledPlugins`**: you can set it in any scope, and managed settings lock it.
* **`syncClaudeAiPlugins`**: each user can also set it in their own user or local settings. See its [scope in the settings reference](/docs/en/settings-reference#syncclaudeaiplugins).
* **`CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL`**: this is an environment variable that you deliver through the managed `env` block shown under [Turn updates off for the whole fleet](#turn-updates-off-for-the-whole-fleet).

Each settings key here has an entry in the [settings reference](/docs/en/settings-reference).

#### Aliases for the marketplace keys

`strictKnownMarketplaces` can also be spelled `allowedMarketplaces`, and `extraKnownMarketplaces` can also be spelled `additionalMarketplaces`.

* **Version**: the aliases require Claude Code v2.1.232 or later, and older clients ignore them. In a file that a mixed fleet reads, keep the canonical names.
* **Both spellings set**: when a file sets both spellings, the canonical key's value applies.

### Allowlist with `strictKnownMarketplaces`

Set the allowlist to a list of these source objects. Most entries match exactly, `hostPattern` and `pathPattern` entries match as regular expressions, and `github` owner wildcards match by owner:

* **`github`**: `{ "source": "github", "repo": "your-org/approved-plugins" }`, with optional `ref` and `path`.
* **`github` owner wildcard**: `{ "source": "github", "repo": "your-org/*" }` matches every repository under that owner. The `*` must stand for the whole repository name. Claude Code ignores entries such as `*/plugins` and `your-org/tools-*` as invalid, so they match nothing. Requires Claude Code v2.1.223 or later.
* **`git`**: `{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }`, with optional `ref` and `path`.
* **`url`**: `{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }`, with optional `headers`.
* **`file` and `directory`**: `{ "source": "file", "path": "/opt/marketplace/marketplace.json" }` or `{ "source": "directory", "path": "/opt/marketplace/plugins" }`, with absolute paths.
* **`hostPattern`**: `{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }`, matched against the host of `github`, `git`, and `url` sources. The pattern matches anywhere in the hostname, so anchor it with `^` and `$` as shown to match the whole host. A `github` source always counts as `github.com`. Use a `hostPattern` entry for a GitHub Enterprise Server or GitLab host where developers create their own marketplaces. The [GHES page](/docs/en/github-enterprise-server#allowlist-ghes-marketplaces-in-managed-settings) has the worked example.
* **`pathPattern`**: `{ "source": "pathPattern", "pathPattern": "^/opt/approved/" }`, matched against the `path` of `file` and `directory` sources. The pattern matches anywhere in the path, so start it with `^` to pin a directory prefix. `".*"` allows every local path.
* **`skills-dir`**: `{ "source": "skills-dir" }` keeps [skills-directory plugins](#keep-skills-directory-plugins-loading) loading while an allowlist is set, and matches no marketplace.

#### How entries match

A `url` entry matches on its `url` value; `headers` aren't compared. For `github` and `git` entries, the `repo` or `url`, the `ref`, and the `path` must all match, or be absent on both sides:

* An entry without `ref` doesn't cover a source with `ref: "main"`.
* An entry for `your-org/your-marketplace` doesn't cover a `git` URL that clones the same repository.
* A trailing slash, a `.git` suffix, or `ssh://` in place of `https://` is a different value. When a marketplace can be cloned by more than one URL, prefer a `hostPattern` entry.

Owner-wildcard entries follow the exact rules for `ref` and match any `path` inside the repository unless the entry pins one. Wildcard matching is case-sensitive on the allowlist.

#### Keep skills-directory plugins loading

Skills-directory plugins are the plugins users keep under `~/.claude/skills/` or a project's `.claude/skills/` in folders that carry a `.claude-plugin/plugin.json`. If you set any allowlist without a `{ "source": "skills-dir" }` entry, they stop loading. Plain [skills](/docs/en/skills), meaning a `SKILL.md` without that manifest, keep loading.

#### Marketplaces hosted on claude.ai

The allowlist and blocklist match a [marketplace hosted on claude.ai](/docs/en/plugins/install#add-from-claude-ai) by its host. To allow or block one, add a `hostPattern` entry that matches `claude.ai` to `strictKnownMarketplaces` or `blockedMarketplaces`. On the allowlist, such an entry admits your organization's claude.ai marketplaces and the claude.ai default marketplaces, but not a marketplace made of a member's own claude.ai uploads or one whose scope claude.ai didn't state. Requires Claude Code v2.1.273 or later.

#### Lock every source out

An empty allowlist, `[]`, locks every marketplace source out, including the official marketplace.

This lockdown doesn't cover the plugins [synced from claude.ai](/docs/en/plugins/loading#synced-plugins), which Claude Code downloads from each user's account rather than from a marketplace. To stop those as well, set [`syncClaudeAiPlugins`](/docs/en/settings-reference#syncclaudeaiplugins) to `false` in managed settings, or turn off Skills for your organization on claude.ai.

### Blocklist with `blockedMarketplaces`

`blockedMarketplaces` takes the same source objects as [`strictKnownMarketplaces`](#allowlist-with-strictknownmarketplaces) and is checked first, so a source on both lists is blocked. Blocklist matching is wider than allowlist matching:

* Git URLs are canonicalized, so the `git@` and `https://` forms, `.git` suffixes, and trailing slashes of one `github.com` repository all match the same entry.
* A `github` entry also blocks the equivalent `git` URL, and the other way around.
* For an `owner/*` entry, the owner comparison is case-insensitive.
* An entry without `ref` or `path` blocks every ref and path of the repositories it matches.

This entry blocks every repository under one GitHub owner:

```json theme={null}
{
  "blockedMarketplaces": [
    { "source": "github", "repo": "untrusted-org/*" }
  ]
}
```

The `url` entries in `blockedMarketplaces` also apply when a user adds an `https://` repository URL that Claude Code [clones rather than fetches](/docs/en/plugins/cli-reference#plugin-marketplace-add), such as a bare `github.com` or `gitlab.com` repository URL. The user can't add that URL if an entry names it. The match ignores the `.git` suffix and any ref the user appends after `#`. Requires Claude Code v2.1.232 or later.

A `{ "source": "skills-dir" }` entry here stops [skills-directory plugins](#keep-skills-directory-plugins-loading) from loading, from both `~/.claude/skills/` and a project's `.claude/skills/`.

A blocklist that names only that entry doesn't count as an active restriction, so it doesn't [stop plugins whose marketplace Claude Code can't find](#restrict-what-users-can-install) from loading.

### Allow the official marketplace and your own

Most organizations allow the official marketplace and their own, and register both so every machine has them. This managed settings policy allows both marketplaces, registers both, force-enables two plugins, and rejects `--plugin-dir`:

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "anthropics/claude-plugins-official" },
    { "source": "github", "repo": "your-org/*" },
    { "source": "skills-dir" }
  ],
  "extraKnownMarketplaces": {
    "claude-plugins-official": {
      "source": { "source": "github", "repo": "anthropics/claude-plugins-official" }
    },
    "your-marketplace": {
      "source": { "source": "github", "repo": "your-org/your-marketplace" }
    }
  },
  "enabledPlugins": {
    "code-formatter@your-marketplace": true,
    "deploy-helper@your-marketplace": true
  },
  "disableSideloadFlags": true
}
```

On a machine with this policy, adding any source outside the list, for example `/plugin marketplace add https://example.com/other-marketplace.git`, fails with a message containing `is blocked by enterprise policy` followed by the allowed sources. `claude --plugin-dir ./x` exits with a message naming `disableSideloadFlags`.

The `{ "source": "skills-dir" }` entry keeps [skills-directory plugins](#keep-skills-directory-plugins-loading) loading under this allowlist. Remove that entry and they stop loading.

Register both marketplaces with explicit `extraKnownMarketplaces` entries, as this policy does, rather than relying on the allowlist or on the official marketplace registering itself:

* **The allowlist doesn't register anything**: an `extraKnownMarketplaces` entry does, and it must itself pass the allowlist. Claude Code refuses to register a managed marketplace whose source the allowlist doesn't match.
* **The official marketplace registers itself only in an interactive terminal session**: even there, it registers only when the allowlist permits it. A `-p` run or a terminal attached to a cloud session never registers it.
* **A blocked attempt is remembered**: if a machine ever ran under a policy that blocked the official marketplace, Claude Code records the blocked attempt and doesn't retry after the policy changes. An `[]` lockdown is one such policy. That machine registers it again only through an `extraKnownMarketplaces` entry such as the one in this policy, an `enabledPlugins` entry for one of its plugins, or a manual `/plugin marketplace add`.

## Set update policy

You can set update policy per marketplace, for the whole fleet, or per user group through release channels.

### Turn auto-update on or off per marketplace

Plugin auto-update runs in the background after startup for marketplaces that have it turned on. For which marketplaces have it on by default, see [When auto-update runs](/docs/en/plugins/loading#when-auto-update-runs). To decide for the fleet, set `"autoUpdate": true` or `false` on a managed `extraKnownMarketplaces` entry:

* If the managed entry sets the field, Claude Code refuses the user's `/plugin` toggle with an error that starts `Auto-update for '<name>' is set by`.
* If the managed entry leaves the field unset, the user's toggle persists.

### Turn updates off for the whole fleet

To turn plugin auto-update off for every marketplace, set `DISABLE_AUTOUPDATER` in the managed `env` block, as this example does. The same variable also stops Claude Code's own updates:

```json theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

To stop Claude Code's own updates but keep plugin auto-update, add `"FORCE_AUTOUPDATE_PLUGINS": "1"` to the same block. The other [environment variables that stop plugin auto-update](/docs/en/plugins/loading#when-auto-update-runs) work the same way.

`DISABLE_AUTOUPDATER` doesn't cover plugins with a [`command` source](/docs/en/plugins/marketplace-reference#command-plugin-source). Claude Code re-runs each enabled one's command every session and installs the output when it changed. For what stops those runs, see [When a command source re-runs](/docs/en/plugins/loading#when-a-command-source-re-runs).

### Assign release channels to user groups

To run stable and early-access channels, host two marketplaces that point at different refs of the same plugins. Then give each user group its own marketplace through either separate endpoint-managed settings or a gateway policy. Server-managed settings from the admin console [apply to every user in your organization](/docs/en/server-managed-settings#current-limitations), so they can't assign different settings to different groups.

* Deploy separate [endpoint-managed settings](/docs/en/managed-settings#delivery-mechanisms), such as a managed settings file or an MDM profile, to each group's devices. To check whether the per-group file or profile applies on a device that also has an organization-wide source, see [How Claude Code combines managed sources](/docs/en/managed-settings#precedence-within-the-managed-tier).
* Define one [Claude apps gateway policy](/docs/en/claude-apps-gateway-config#managed) per group. The gateway applies the first policy whose match rule fits a user, so order the policies so that each user reaches their group's policy. That policy's `extraKnownMarketplaces` map doesn't merge with any other policy's, so list every marketplace the group needs in it, not only its channel marketplace.

With either mechanism, the stable group receives this configuration:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "stable-tools": {
      "source": { "source": "github", "repo": "your-org/stable-tools" }
    }
  }
}
```

The early-access group receives `latest-tools` instead. To set up the two marketplaces, see [Run release channels](/docs/en/plugins/host-marketplace#run-release-channels).

## Recommend plugins

Marketplace owners can attach `relevance` signals to entries so Claude Code suggests the plugin when a project matches.

Suggestions from a marketplace appear only when it's registered on the user's machine, you list its name in `pluginSuggestionMarketplaces` in managed settings, and you declare its source in the same policy. Declare the source either as the marketplace's `extraKnownMarketplaces` entry or as an allowlist entry. The official marketplace needs only the name. See [Enable suggestions in managed settings](/docs/en/plugins/relevance#enable-suggestions-in-managed-settings).

## Audit and review

OpenTelemetry events and the Analytics API tell you what your fleet installs and runs.

For what a plugin can run on a machine and what each trust tier permits, read [Plugin security](/docs/en/plugins/security) before you approve a marketplace.

### OpenTelemetry events

`claude_code.plugin_installed` records each install, and `claude_code.plugin_loaded` records each enabled plugin at session start. Both events redact or omit third-party plugin and marketplace names unless you set `OTEL_LOG_TOOL_DETAILS=1`, as [Redacted plugin names in your backend](/docs/en/plugins/measure#redacted-plugin-names-in-your-backend) shows. Field lists are under [Plugin installed event](/docs/en/monitoring-usage#plugin-installed-event) and [Plugin loaded event](/docs/en/monitoring-usage#plugin-loaded-event).

### Analytics API

On the Enterprise plan, `GET /v1/organizations/analytics/plugins` returns per-plugin, per-day install and invocation counts across Claude Code and Cowork. You can group the counts by user or RBAC group. Plugin activity that reaches Anthropic without a plugin name appears in one aggregate `third-party` row. See the [endpoint reference](https://platform.claude.com/docs/en/api/admin/analytics/plugins/list) and [Access data programmatically](/docs/en/analytics#access-data-programmatically) for the key it needs.

## Plan for what managed settings can't enforce

These requests from security reviews have no dedicated key in the current settings schema. The nearest existing controls are:

* **Per-user or per-group targeting**: every plugin key applies to every user who receives the settings. Server-managed settings deliver one configuration per organization. For per-group policy, use separate endpoint-managed settings or gateway policies, as under [Assign release channels to user groups](#assign-release-channels-to-user-groups).
* **Restricting entries inside an allowed marketplace**: the allowlist matches marketplace sources. To block one plugin from an allowed marketplace, set it to `false` in managed `enabledPlugins`.
* **Hiding `/plugin`**: no key disables the command. The nearest equivalent combines an allowlist naming only your marketplace, managed `enabledPlugins` entries for the plugins you supply, and `disableSideloadFlags`.
* **Gating `--plugin-dir` through the allowlist**: the allowlist doesn't cover `--plugin-dir`. `disableSideloadFlags` does.
* **Enforcing the claude.ai plugin toggles through these keys**: [**Organization settings > Plugins & skills**](https://claude.ai/admin-settings/skills?tab=inventory) doesn't set the keys on this page. What members and your organization turn on there reaches the CLI as [synced plugins](/docs/en/plugins/loading#synced-plugins), which have their own controls.

## Troubleshoot policy

If plugin policy doesn't behave as expected on a machine, check for these symptoms first:

* **The managed file didn't parse**: when a `managed-settings.json` isn't valid JSON, Claude Code refuses to start and prints [an error naming the file](/docs/en/errors#managed-settings-document-could-not-be-parsed). A file that parses but has one invalid entry keeps the rest of its policy. See [Invalid entries in managed settings](/docs/en/managed-settings#invalid-entries-in-managed-settings).
* **The managed source didn't load**: run `/status` and look for `Enterprise managed settings` in the `Setting sources` line. If it's missing, the source didn't load.
* **A user reports `blocked by enterprise policy`**: the message names the marketplace or its source. For an allowlist, it also lists the allowed sources. The user-facing entries are on [Troubleshoot plugins](/docs/en/plugins/troubleshooting).
* **A plugin the user disabled in `~/.claude/settings.json` still loads**: another settings source re-enabled it, such as a managed `enabledPlugins` entry that force-enables it. `/plugin` and `claude plugin list` show `Disabled in ~/.claude/settings.json but still loads` with that settings source.

## Next steps

* [Marketplace reference](/docs/en/plugins/marketplace-reference#marketplace-sources): the `source` values `extraKnownMarketplaces`, `strictKnownMarketplaces`, and `blockedMarketplaces` accept
* [Host and maintain a marketplace](/docs/en/plugins/host-marketplace): run the marketplace your policy points at
* [Plugin security and trust](/docs/en/plugins/security): what a plugin can do on a machine and how to review one before installing
* [Server-managed settings](/docs/en/server-managed-settings): deliver these keys from the claude.ai admin console
* [Troubleshoot plugins](/docs/en/plugins/troubleshooting#blocked-by-your-organization): the messages users see when policy blocks them
