> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Host and maintain a marketplace

> Publish a plugin marketplace where users can reach it, grant access to a private one, and release updates and renames without breaking installs.

Hosting a marketplace means putting your `marketplace.json` catalog where other people can add it with `/plugin marketplace add`, install its plugins, and keep receiving your changes after you push.

This page is for the person who operates a marketplace.

<Note>
  These cases are covered on other pages:

  * **You haven't written the catalog file yet**: start with [Create a marketplace](/docs/en/plugins/create-marketplace)
  * **You're an admin requiring, restricting, or pre-installing marketplaces across your organization's machines**: read [Manage plugins for your organization](/docs/en/plugins/org)
</Note>

Start with [Host your marketplace](#host-your-marketplace) to pick a host and the command your users run. Read [Keep users up to date](#keep-users-up-to-date) before your first release. Read [Rename or remove a plugin](#rename-or-remove-a-plugin) before you change a plugin's `name`.

## Host your marketplace

You can host the marketplace on GitHub, on another git host, as a hosted `marketplace.json` URL, or in a directory on a shared filesystem. Send your users the add command for your host and tell them what they need on their machine:

| Host                                                             | Users run, in a Claude Code session                                    | What users need                                                                                                                                |
| :--------------------------------------------------------------- | :--------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| GitHub                                                           | `/plugin marketplace add your-org/your-marketplace`                    | `git`, and for a private repository the access described under [Grant access to a private marketplace](#grant-access-to-a-private-marketplace) |
| GitLab, Bitbucket, GitHub Enterprise Server, or another git host | `/plugin marketplace add https://gitlab.example.com/team/plugins.git`  | `git`, and access to the host from their machine. Send the full URL, because `owner/repo` shorthand always means github.com                    |
| A hosted `marketplace.json` URL                                  | `/plugin marketplace add https://plugins.example.com/marketplace.json` | HTTPS access to the URL. Users don't need `git` for the catalog itself                                                                         |
| A directory on a shared filesystem                               | `/plugin marketplace add /Volumes/shared/claude-plugins`               | Read access to the path                                                                                                                        |

To pin a branch or tag of a GitHub or git-URL marketplace, tell users to append `#<ref>`, as in `your-org/your-marketplace#stable`. The [plugin commands reference](/docs/en/plugins/cli-reference#plugin-marketplace-add) lists every form the command accepts.

A successful add prints `Successfully added marketplace: your-marketplace`. Claude Code takes that name from the `name` field in your `marketplace.json`, not from the repository name.

Users then install a plugin by its entry's `name` and the marketplace's `name`, as in `/plugin install code-formatter@your-marketplace`.

### Register the marketplace for everyone in a repository

To share the marketplace with everyone who works in one repository, run `claude plugin marketplace add your-org/your-marketplace --scope project` there once from your shell and commit the `.claude/settings.json` it writes. Claude Code then registers the marketplace for each teammate who [trusts the folder](/docs/en/plugins/org#require-plugins-per-repository).

### Avoid relative-path entries in a URL-hosted marketplace

When users add your marketplace as a bare `marketplace.json` URL, Claude Code downloads only that file. An entry in your `plugins` array whose `source` is a relative path such as `./plugins/formatter` then fails at install with [`its marketplace entry path does not stay inside the marketplace directory`](/docs/en/plugins/troubleshooting#plugins-with-relative-paths-fail-in-url-based-marketplaces). Give every entry a source that can be fetched on its own, such as a `github` repository or an `archive` URL, or host the marketplace in a git repository so Claude Code clones the whole tree.

### Edit plugins in place on a shared directory

When users add your marketplace from a shared directory, Claude Code reads plugins with relative-path sources directly from that directory instead of copying them. Users see your edits when they next start a session or run `/reload-plugins`, without an update step or a version bump.

### Keep plugin files out of Git LFS

Keep the files your plugins need out of [Git LFS](https://git-lfs.com). When users add a marketplace hosted in a git repository, or install a git-based plugin it lists, Claude Code clones that marketplace or plugin repository onto their machine. The clone never downloads LFS content, so LFS-tracked files arrive as pointer files.

### Share files within a marketplace with symlinks

To share files between your plugin and other parts of the same marketplace, create symbolic links inside your plugin directory. When Claude Code copies the plugin into its cache, it handles each symlink by where the target resolves:

* **Within the plugin's own directory**: the symlink is preserved as a relative symlink in the cache, so it keeps resolving to the copied target at runtime.
* **Elsewhere within the same marketplace**: the symlink is dereferenced. The target's content is copied into the cache in its place. This lets a meta-plugin's `skills/` directory link to skills defined by other plugins in the marketplace.
* **Outside the marketplace**: the symlink is skipped for security.

For plugins installed from a local path, or from a [`command` source](/docs/en/plugins/marketplace-reference#command-plugin-source) whose `mode` is the default `copy`, Claude Code preserves only symlinks that resolve within the plugin's own directory and skips all others.

The following command creates a link from inside a marketplace plugin to a shared skill defined by a sibling plugin. On Windows, use `mklink /D` from an elevated Command Prompt or enable Developer Mode:

```bash theme={null}
ln -s ../../shared-plugin/skills/foo ./skills/foo
```

## Distribute through organization settings

On a Team or Enterprise plan, you can also distribute the marketplace through [**Organization settings > Plugins & skills**](https://claude.ai/admin-settings/skills?tab=inventory) on claude.ai instead of hosting it somewhere users add it themselves. Organization sync reads the repository through your organization's GitHub or GitLab connection on claude.ai, so your users' git credentials aren't involved.

Organization sync is stricter about the repository than `/plugin marketplace add` is:

* **Marketplace repository**: on github.com and gitlab.com, it must be private or internal
* **Plugin sources**: organization sync accepts only some [source types](/docs/en/plugins/marketplace-reference#plugin-sources)
* **Top-level `bin/` directory**: claude.ai rejects a plugin that has one and syncs the rest of the marketplace. The error message starts with `Plugin contains a top-level bin/ directory`. Keep executables in another directory, such as `scripts/`, and reference them as `${CLAUDE_PLUGIN_ROOT}/scripts/<name>` from your hooks or MCP server configs

[Sync your organization's plugins from a repository](https://claude.com/docs/plugins/org-sync) on claude.com lists the accepted sources, the GitLab setup, and the `bin/` error, and [Manage plugins for your organization](https://claude.com/docs/plugins/admin) covers the admin workflow.

## Grant access to a private marketplace

When a user adds, installs from, or updates your marketplace, Claude Code runs `git` on their machine with interactive prompts turned off and relies on whatever credentials that machine already holds. Claude Code has no git token of its own, and `marketplace.json` has no field for one.

You choose whether the clone runs over SSH or HTTPS by the form of the add command you send users:

* **GitHub `owner/repo`**: Claude Code probes `ssh -T git@github.com` and clones over SSH when the probe succeeds. If the probe fails, or the SSH clone itself fails, it clones over HTTPS. Users on machines without a GitHub SSH key can set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` to skip the probe and clone over HTTPS.
* **`git@host:path.git`**: SSH.
* **`https://example.com/repo.git`**: HTTPS.

Tell users what each protocol needs on their machine:

* **SSH**: the key must work without a passphrase prompt, for example because it's loaded in `ssh-agent`. The host must already be in `known_hosts`.
* **HTTPS**: Claude Code leaves the user's git credential helper enabled but forbids it from prompting. A credential the helper already stores works; one it would have to ask for fails. On GitHub, `gh auth login` followed by `gh auth setup-git` stores one.

For a GitHub Enterprise Server host, users need git access to that host from their machine. See [Plugin marketplaces on GHES](/docs/en/github-enterprise-server#plugin-marketplaces-on-ghes) for what each Claude Code surface needs to reach a GHES-hosted marketplace.

If you distribute through **Organization settings > Plugins & skills** on claude.ai instead, your users' git credentials aren't involved. See [Distribute through organization settings](#distribute-through-organization-settings).

### Serve users who have no git-host account

Users without a git-host account can add a marketplace you serve as a `marketplace.json` URL or from a shared directory, but they can install only the plugins whose entry sources they can also reach. An entry that points at a private `github` repository still fails at install for them, because Claude Code fetches it with the same non-interactive `git` it uses for a git-hosted marketplace.

These entry sources need no git account:

* **`archive`**: a zip downloaded over HTTPS. Users need neither `git` nor an account, only network access to the URL. Requires Claude Code v2.1.224 or later. Pin each archive with `sha256` so Claude Code refuses a changed download. To send credentials with the download, see [Authenticate archive downloads](#authenticate-archive-downloads).
* **A public git repository**: Claude Code clones a public `url` or `git-subdir` source over HTTPS without credentials when the entry gives an `https://` URL. For a `github` source, or a `git-subdir` source written as `owner/repo`, users without a GitHub SSH key set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`.

For a team on one network, a `directory` marketplace on a shared filesystem also works without git accounts. Users need only read access to the path.

### What background auto-update does with credentials

Background auto-update is Claude Code's unattended refresh of marketplaces and installed plugins after a session starts. It's off for your marketplace until a user or admin turns it on, as covered under [Keep users up to date](#keep-users-up-to-date).

When it's on for a private marketplace, the background check for new commits uses the user's configured git credential helpers and never prompts. Each kind of remote and helper gives a different result:

* **SSH remotes**: a key loaded in `ssh-agent` authenticates the check.
* **HTTPS remotes with a stored credential**: a helper that can supply a stored credential without prompting authenticates the check. Git Credential Manager, the macOS Keychain helper, and `git-credential-store` work this way once they hold a credential for the host.
* **HTTPS remotes with a helper that needs to prompt**: the helper can't answer in the background. The update fails quietly and the existing checkout stays in place, so the user's plugins keep working from the last synced state.

After the check, Claude Code does one of the following:

* **The checkout is up to date**: Claude Code leaves it as it is.
* **The check finds new commits, or fails because it can't reach or authenticate to the remote**: Claude Code clones the marketplace again and replaces the existing checkout with the new clone. If that clone fails, the existing checkout stays in place. The re-clone can [time out on large repositories](/docs/en/plugins/troubleshooting#git-clone-timed-out-after-120s).

To keep a private marketplace current, a user can do either of the following:

* **Store a credential**: sign in to the credential helper first so it holds a credential for the host. For GitHub, run `gh auth login`, then `gh auth setup-git`.
* **Keep the checkout on failure**: if the user sets `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1`, Claude Code keeps the existing checkout without attempting the re-clone when the background check can't reach or authenticate to the remote. Plugins keep working from the last synced state.

If a user sets `GITHUB_TOKEN` or another provider token in the environment, that alone doesn't authenticate the background check. A token takes effect through a credential helper, such as the `gh` CLI's helper, which reads `GH_TOKEN` and `GITHUB_TOKEN`.

## Roll out to a whole company

Rolling a plugin out to a company involves you as the marketplace owner, an administrator who controls managed settings, and each person who uses Claude Code. You can run the rollout without the administrator, in which case each person adds the marketplace and installs the plugin themselves.

| Who                        | What they do                                                                                                                                                          | Where it's covered                                                                                                                                        |
| :------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| You, the marketplace owner | Keep the catalog in a repository only the company can read, send the add command for your host, and say what each person needs on their machine                       | [Host your marketplace](#host-your-marketplace) and [Grant access to a private marketplace](#grant-access-to-a-private-marketplace)                       |
| An administrator           | Registers the marketplace and turns its plugins on for everyone with `extraKnownMarketplaces` and `enabledPlugins` in managed settings, and sets `autoUpdate` there   | [Require a marketplace and its plugins](/docs/en/plugins/org#require-a-marketplace-and-its-plugins) and [Set update policy](/docs/en/plugins/org#set-update-policy) |
| Each person                | Needs read access to a private git repository, with credentials already stored on their machine. Without an administrator, they also run the add and install commands | [Add a private marketplace](/docs/en/plugins/install#add-a-private-marketplace)                                                                                |

For people who have no git-host account, these sections each cover one way to reach them:

* **Entry sources that need no git account**: [Serve users who have no git-host account](#serve-users-who-have-no-git-host-account)
* **A pre-populated plugins directory**: [Seed containers and CI](/docs/en/plugins/org#seed-containers-and-ci), which also serves users who have no git-host account
* **claude.ai organization settings**: [Distribute through organization settings](#distribute-through-organization-settings), where your users' git credentials aren't involved

## Keep users up to date

Your changes reach users through background auto-update, once it's turned on for your marketplace, or when users update the plugin themselves. In both cases a user gets a new copy of a plugin only when its computed version changes, as described under [Release a new version](#release-a-new-version).

### Turn on auto-update

Background auto-update is off for your marketplace by default, and `marketplace.json` has no field to turn it on. A user or an admin turns it on:

* **Tell users to turn it on**: each user goes to **Marketplaces** in `/plugin`, selects your marketplace, and selects **Enable auto-update**.
* **Ask an admin to set it**: if an admin sets `"autoUpdate": true` on your marketplace's `extraKnownMarketplaces` entry in managed settings, it's on for everyone who receives those settings. See [Set update policy](/docs/en/plugins/org#set-update-policy).

Without auto-update, users receive your changes when they run `/plugin marketplace update <name>` in a session or `claude plugin update <plugin>@<name>` in the shell.

For what users see when an update reaches them, see [When auto-update runs](/docs/en/plugins/loading#when-auto-update-runs).

### Release a new version

To release a new version to users, change the plugin's `version`. Users get a new copy only when the plugin's computed version differs from the one they have. That version comes from `plugin.json` first, then from the marketplace entry, per [Versions and updates](/docs/en/plugins/loading#versions-and-updates).

A plugin that users [load in place](/docs/en/plugins/loading#find-plugins-on-disk) from a marketplace they added as a local directory isn't controlled by `version`. It loads your current files at every session start, whatever its version string says.

For every install other than an in-place load or one from a `command` source, either increase `version` on each release or omit it:

* **Bump `version` on each release**: users stay on their cached copy until the string changes. If you set `"version": "1.0.0"` and push new commits without changing it, users don't receive them.
* **Omit `version`**: users track your commits instead. Leave `version` out of both `plugin.json` and the marketplace entry.

Don't set `version` in both `plugin.json` and the marketplace entry. If you do, Claude Code uses the `plugin.json` value without warning, and `claude plugin validate` reports the mismatch as `Entry declares version "<a>" but <path>/plugin.json says "<b>"`.

### Hold users on one version

One marketplace serves one version of each plugin at a time, so you hold users on a version by choosing what each entry points at:

* **`ref` and `sha` on the plugin entry**: `ref` names a branch or tag and `sha` names a commit for a `github`, `url`, or `git-subdir` source. See [Plugin sources](/docs/en/plugins/marketplace-reference#plugin-sources).
* **`#<ref>` on the add command**: users who add `your-org/your-marketplace#stable` get that branch or tag of the catalog. For two release lines at once, see [Run release channels](#run-release-channels).
* **`<plugin>--v<version>` tags**: a dependency's version range resolves against these tags. See [Release a plugin that others depend on](/docs/en/plugins/dependencies#tag-plugin-releases-for-version-resolution).

[Release a new version](#release-a-new-version) says when a changed entry reaches users.

### Change the command of a command source

If you change the `command` of a [`command` source](/docs/en/plugins/marketplace-reference#command-plugin-source), or switch its `mode`, each user has to accept the new command before Claude Code runs it. Claude Code runs only the exact command a user accepted when they installed or last updated the plugin.

After a user's copy of your marketplace picks up the change, that user sees the following:

* **No more background runs**: the [once-per-session run](/docs/en/plugins/loading#when-a-command-source-re-runs) of the command stops for that user, so the tool's new output doesn't reach them.
* **An entry in the `/plugin` Errors tab**: the entry shows the new command and the `claude plugin update` command to run.

Tell users to run the `claude plugin update` command that entry shows, in a terminal. Claude Code shows them the new command and asks them to accept it.

## Run release channels

To offer stable and early-access tracks, host two marketplaces whose entries point at different refs of the same plugin, and let each user add the one they want. Claude Code has no release-channel concept, and one marketplace serves one version of each plugin at a time.

Give the two `marketplace.json` files different `name` values. Claude Code identifies a marketplace by its `name`, so a user can't have two marketplaces with the same name registered at once.

With these two catalogs, users who add `stable-tools` install `code-formatter` from the `stable` branch, and users who add `latest-tools` install it from `latest`:

```json theme={null}
{
  "name": "stable-tools",
  "owner": { "name": "Your Org" },
  "plugins": [
    { "name": "code-formatter", "source": { "source": "github", "repo": "your-org/code-formatter", "ref": "stable" } }
  ]
}
```

```json theme={null}
{
  "name": "latest-tools",
  "owner": { "name": "Your Org" },
  "plugins": [
    { "name": "code-formatter", "source": { "source": "github", "repo": "your-org/code-formatter", "ref": "latest" } }
  ]
}
```

Give the two refs different `plugin.json` versions, or omit `version` so the commit SHA distinguishes them. Updates are detected by comparing versions, so a ref that moves without a version change leaves users on the cached copy.

To assign the channels to user groups instead of letting users choose, an admin gives each group the matching `extraKnownMarketplaces` entry, as described under [Set update policy](/docs/en/plugins/org#set-update-policy).

## Rename or remove a plugin

A plugin's `name` is its identifier. Users reference it in the `enabledPlugins` and `pluginConfigs` settings keys and in `/plugin install`, so changing it breaks every existing install.

To change the label users see in `/plugin` without breaking anything, set `displayName` in `plugin.json` and keep `name` unchanged.

### Migrate users with a renames map

When you must change a `name`, add a top-level `renames` map to `marketplace.json` so Claude Code migrates existing users instead of reporting [`Plugin "<name>" not found in marketplace`](/docs/en/plugins/troubleshooting#plugin-not-found-in-marketplace). Do the same when you remove an entry from `plugins`. Automatic migration requires Claude Code v2.1.193 or later.

Map each former name to its current name, or to `null` when the plugin is gone. This marketplace renames `formatter` to `code-formatter` and records that `legacy-linter` was removed:

```json theme={null}
{
  "name": "your-marketplace",
  "owner": { "name": "Your Org" },
  "plugins": [
    { "name": "code-formatter", "source": "./plugins/code-formatter" }
  ],
  "renames": {
    "formatter": "code-formatter",
    "legacy-linter": null
  }
}
```

After you push, a user who still has the old name enabled sees one of these results:

* **Renamed entry**: the plugin loads under its new name. `claude plugin list` and the plugin's details under `/plugin` show `Renamed to "code-formatter" in the "your-marketplace" marketplace` once, and Claude Code rewrites the old key to the new one in `enabledPlugins` and `pluginConfigs` in the user, project, and local settings scopes.
* **`null` entry**: the old key is dropped from those scopes and the user sees `Removed from the "your-marketplace" marketplace`.
* **Enabled in managed settings**: the plugin still loads under its new name, but Claude Code can't rewrite managed settings, so the notice recurs until an admin updates `enabledPlugins` there.

For a marketplace users added from a git repository or URL, a renamed plugin reports [`Plugin "<name>" not cached at <path>`](/docs/en/plugins/troubleshooting#plugin-not-cached-at) until the user runs `/plugin install code-formatter@your-marketplace` once in a session.

Treat `renames` as append-only history. Keep old entries after everyone has migrated. When you rename again, add a second entry rather than editing the first, because Claude Code follows the chain from the oldest name.

In your shell, run `claude plugin validate .` after editing the map. It rejects a chain that cycles or that ends anywhere other than `null` or a name in `plugins`, with `renames.<name>: chain does not resolve`.

### Uninstall removed plugins from users' machines

To uninstall a removed plugin from users' machines rather than leave a copy behind, set `"forceRemoveDeletedPlugins": true` at the top level of `marketplace.json`. Without the field, a removed plugin stays installed and reports `Plugin "<name>" not found in marketplace` when a session loads it. With it, Claude Code does the following at each session start:

1. Compares what users installed from your marketplace against the entries and the `renames` map, and treats any plugin that is neither listed nor renamed as removed.
2. Uninstalls each removed plugin from the user, project, and local scopes. Plugins that only managed settings installed stay in place.
3. Lists each removed plugin under a **Flagged** heading in `/plugin` with the status `Removed from marketplace`.

## Authenticate archive downloads

To authenticate an [`archive`](/docs/en/plugins/marketplace-reference#archive-plugin-source) download, such as a download from a private registry, set the HTTP headers Claude Code sends with it. You can set `headers` in either of these places:

* **The marketplace's `url` source**: the `url` source you registered the marketplace from, such as an [`extraKnownMarketplaces`](/docs/en/settings-reference#extraknownmarketplaces) entry.
* **The plugin's entry**: on Claude Code v2.1.238 or later, you can set it on the plugin's `marketplace.json` entry instead, beside `source`.

In either place, set a `headersHelper` command instead of `headers` when the value is short-lived, such as a token your registry generates on request. Claude Code runs the command and sends the JSON object it prints as that place's headers. Requires Claude Code v2.1.238 or later.

The [marketplace reference](/docs/en/plugins/marketplace-reference#plugin-entries) lists the `headers` and `headersHelper` entry fields.

The place you choose decides which downloads get the headers and when Claude Code runs the command:

| Place                    | Downloads that get the headers                                                             | When Claude Code runs a `headersHelper` set there                                                                                                                   |
| :----------------------- | :----------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Marketplace `url` source | Archive downloads on the marketplace URL's origin, meaning the same scheme, host, and port | Before each fetch of the marketplace's `marketplace.json` and before each archive download on that origin. Claude Code reuses one run's output for up to 60 seconds |
| Plugin entry             | That entry's download only                                                                 | Only when a user installs or updates that one plugin by itself and [accepts the command](#how-users-accept-a-headershelper-command)                                 |

Where both places set a header of the same name, Claude Code sends the entry's value. Within one place, a header the command prints overrides a header of the same name listed in `headers`.

### Add a headersHelper to a plugin entry

This entry sets `headersHelper` beside `source`. It also sets [`"strict": false`](/docs/en/plugins/marketplace-reference#strict-mode), which Claude Code requires of a `marketplace.json` entry that sets `headersHelper`:

```json theme={null}
{
  "name": "my-plugin",
  "description": "Formatting commands for internal services",
  "strict": false,
  "source": {
    "source": "archive",
    "url": "https://registry.example.com/plugins/my-plugin-2.1.0.zip"
  },
  "headersHelper": "/opt/bin/mint-registry-token.sh"
}
```

To check the entry, run `claude plugin install my-plugin@your-marketplace` in your shell. Claude Code shows you the command and the archive URL, and downloads the zip after you accept.

### Write the headersHelper command

Whether you set `headersHelper` on a marketplace's `url` source or on a plugin entry, write the command to meet these requirements:

* **Command text**: at most 500 characters of printable ASCII, with no run of four or more spaces.
* **Output**: print one JSON object of header names and string values on stdout, then exit 0 within 10 seconds.
* **Shell and working directory**: Claude Code runs the command through `sh`, or through `cmd.exe` on Windows. The working directory is the configuration directory, which is `~/.claude` or [`CLAUDE_CONFIG_DIR`](/docs/en/env-vars#variables). Give an absolute path or a command on `PATH`, because a relative path resolves against that directory, not the user's project.
* **Variables Claude Code removes**: when the command is set in a `marketplace.json` entry, or in a project's `.claude/settings.json` or `.claude/settings.local.json`, Claude Code removes from the environment every variable whose name looks like a credential, by the [same rule it applies to an MCP `headersHelper`](/docs/en/mcp#which-variables-a-helper-can-read). `ANTHROPIC_API_KEY` and `MY_REGISTRY_TOKEN` are both removed, so have the command read its credential from a file or a credential store. This removal doesn't apply to a command set in user settings, a `--settings` file, or managed settings.
* **Variables Claude Code sets**: `CLAUDE_CODE_MARKETPLACE_URL` and `CLAUDE_CODE_MARKETPLACE_NAME` for a `url` source's command, and `CLAUDE_CODE_PLUGIN_NAME` and `CLAUDE_CODE_PLUGIN_ARCHIVE_URL` for an entry's command. `CLAUDE_CODE_MARKETPLACE_NAME` is unset on the first fetch after a user adds a marketplace by URL, because that fetch is what supplies the name.

A command that mints a bearer token prints an object like this one:

```json theme={null}
{"Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9"}
```

### When Claude Code skips a headersHelper command or drops its output

A `headersHelper` command doesn't run, or headers from `headers` or from the command's output are dropped, when one of the following applies:

* **Command fails**: if the command exits non-zero, runs past 10 seconds, or prints anything other than a JSON object of string values, the fetch or download the command was run for doesn't happen.
* **Marketplace URL doesn't start with `https://`**: that `url` source's command doesn't run, and requests carry only the headers listed in its `headers` field.
* **Redirect leaves the origin**: when a download is redirected off the archive URL's origin, the redirected request carries no `headers` values or command output from either the marketplace `url` source or the plugin entry.
* **Entry sets a routing or identity header**: Claude Code drops request-routing and client-identity names such as `Host`, `Cookie`, and `X-Forwarded-*` from an entry's `headers` and command output, and keeps authentication names such as `Authorization`. Every `marketplace.json` entry is filtered this way. For an inline plugin entry in settings, see [`extraKnownMarketplaces`](/docs/en/settings-reference#extraknownmarketplaces).
* **Command set in an `--add-dir` directory's settings**: the command is ignored, on a `url` source and on an [inline plugin entry](/docs/en/settings-reference#extraknownmarketplaces) alike, and only that file's `headers` are sent.
* **Managed settings block the command**: setting [`disableCommandPluginSources`](/docs/en/settings-reference#disablecommandpluginsources) to `true` blocks `headersHelper` commands, and [`allowManagedHooksOnly`](/docs/en/settings-reference#allowmanagedhooksonly) blocks them too unless `disableCommandPluginSources` is explicitly `false`. Under either block, Claude Code still runs the command for a marketplace that managed settings themselves declare.

### How users accept a headersHelper command

A user accepts a plugin entry's command each time they install or update that one plugin by itself. They do that from the plugin's own view in `/plugin`, or with `claude plugin install` or `claude plugin update`. Claude Code shows the command and the archive URL, and runs the command only after the user accepts.

In a non-interactive shell, pass [`--yes`](/docs/en/plugins/cli-reference#plugin-install) to accept the command. To accept only the command that a previous `--json` run displayed, pass [`--accept-command`](/docs/en/plugins/cli-reference#plugin-install) with the `sha256` the run reported.

Claude Code runs only the command it showed, for the archive URL it showed. If the entry's command or archive URL changed in between, Claude Code refuses the install or update. A change in the query string alone doesn't count.

<h3 id="installs-and-updates-that-refuse-the-command-instead-of-asking">
  Installs and updates that refuse a command instead of asking
</h3>

On any operation other than a single-plugin install or update, Claude Code neither runs an entry's command nor downloads its archive. The plugin stays at its installed version or stays uninstalled, and the user sees one of these results:

* **Installing several plugins at once, from a plugin suggestion, or as another plugin's dependency**: Claude Code refuses the plugin that has the command and directs the user to that plugin's own view in `/plugin`. The other plugins in a bulk install still install. A plugin that depends on the refused plugin fails to install until the user installs the refused plugin by itself.
* **Background auto-update, or session start for a plugin whose archive was never downloaded**: Claude Code lists the plugin in the `/plugin` Errors tab so the user knows to install or update it themselves.

<h3 id="when-a-marketplace-url-sources-command-runs">
  When a marketplace `url` source's command runs
</h3>

You declare a marketplace `url` source's `headersHelper` in a settings file, such as an [`extraKnownMarketplaces`](/docs/en/settings-reference#extraknownmarketplaces) entry, rather than in the catalog the marketplace publishes. Claude Code therefore doesn't ask the user to accept it on each install or update. Instead, the settings file that declares it decides when Claude Code runs it:

| Settings file                                                                 | When Claude Code runs the command                                                                                                                                                                                                            |
| :---------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| User settings, a `--settings` file, or a managed settings file on the machine | Without asking, including during a background marketplace refresh                                                                                                                                                                            |
| A project's `.claude/settings.json` or `.claude/settings.local.json`          | Only after the user accepts the [workspace trust dialog](/docs/en/permissions#what-runs-before-you-trust-a-folder) for that folder itself. A `-p` or SDK session doesn't count as accepting it, and neither does trust granted to a parent folder |
| Server-managed settings                                                       | In an interactive session, only after the user approves the delivered settings in the [security approval dialog](/docs/en/server-managed-settings#security-approval-dialogs)                                                                      |

For an [inline plugin entry](/docs/en/settings-reference#extraknownmarketplaces) in one of these files, Claude Code requires the same folder trust or settings approval as for a marketplace-level command in that file, and the user also accepts the entry's command on each install or update.

## Depend on and recommend other plugins

An entry can declare dependencies on other plugins.

* **Version ranges**: a dependency can carry a semver range.
* **Cross-marketplace dependencies**: a dependency from another marketplace installs only when your marketplace lists that marketplace in `allowCrossMarketplaceDependenciesOn`.

For version ranges, the `<plugin>--v<version>` git-tag convention they resolve against, and cross-marketplace trust, see [Plugin dependencies](/docs/en/plugins/dependencies).

To have Claude Code suggest a plugin when a project matches it, add a `relevance` block to the entry with the signals that identify the project. Users see suggestions from your marketplace only when an admin lists it in `pluginSuggestionMarketplaces`. For the signals and the enablement step, see [Plugin relevance](/docs/en/plugins/relevance).

## Work around what a marketplace can't do

Some things owners ask for have no field in `marketplace.json`. Here is the nearest option for each:

* **Restrict what else users install**: the marketplace allowlist is a managed setting, `strictKnownMarketplaces`. See [Restrict what users can install](/docs/en/plugins/org#restrict-what-users-can-install).
* **Install or enable a plugin without the user asking**: no entry field installs a plugin. Managed `enabledPlugins` does that for a fleet; see [Pre-install and require plugins](/docs/en/plugins/org#pre-install-and-require-plugins).
* **Show different entries to different users**: entries carry no audience field, and every user who adds the marketplace sees the whole catalog. Host separate marketplaces for separate audiences.
* **Mark a plugin deprecated**: there is no deprecation state. The option is to remove the entry, map its name to `null` in `renames`, and optionally set `forceRemoveDeletedPlugins`.
* **Turn on auto-update for your users**: each user turns it on under **Marketplaces** in `/plugin`, or an admin sets `autoUpdate` in managed settings. See [Turn on auto-update](#turn-on-auto-update).
* **Carry git credentials**: no marketplace field holds a git token. Access to a git-hosted marketplace or plugin follows the user's git setup, per [Grant access to a private marketplace](#grant-access-to-a-private-marketplace). For `archive` sources, an entry can set [`headers` or `headersHelper`](#authenticate-archive-downloads) instead.

## Next steps

* [Marketplace reference](/docs/en/plugins/marketplace-reference): `marketplace.json` fields, source types, and validation messages
* [Manage plugins for your organization](/docs/en/plugins/org): require, restrict, or seed your marketplace across your organization's machines
* [Plugin dependencies](/docs/en/plugins/dependencies): tag releases so plugins that depend on yours can resolve versions
* [Troubleshoot plugins](/docs/en/plugins/troubleshooting): the errors your users see when adding or updating from your marketplace
