> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Troubleshoot plugins

> Fix plugin errors in Claude Code. Find the exact message you saw, grouped by stage from where /plugin runs through install and org policy.

This page lists error messages and symptoms for Claude Code plugins and for marketplaces, the catalogs Claude Code installs plugins from. Each entry gives the cause, one fix, and what you see once the fix works.

Where a message names a plugin or marketplace, the entry shows a placeholder such as `<name>` instead.

Use this page whether you install plugins, build them, host a marketplace, or administer plugins for an organization.

<Note>
  These cases are covered on other pages:

  * **Why scopes, the cache, and precedence behave the way they do**: read [Plugin loading reference](/docs/en/plugins/loading)
  * **Looking up a flag, field, or command**: use the [plugin commands reference](/docs/en/plugins/cli-reference), the [manifest reference](/docs/en/plugins/manifest-reference), or the [marketplace reference](/docs/en/plugins/marketplace-reference)
</Note>

Search for the exact message you saw. Each message is listed under the stage that produces it, which isn't always the command you ran. For example, an install can fail because a marketplace is missing, so that message is under [Add a marketplace](#add-a-marketplace).

## Find where `/plugin` runs

`/plugin` is a command you type inside a running Claude Code terminal session, and it opens an interactive panel. The entries in this section cover the places where you can type it but it can't run, and the command spellings that don't exist.

<h3 id="plugin-isnt-available-in-this-environment">
  `/plugin isn't available in this environment`
</h3>

You typed `/plugin` somewhere other than a Claude Code terminal session, and Claude replied with this line instead of opening anything.

You get this reply in a session that has no terminal to draw the `/plugin` panel in: [non-interactive mode](/docs/en/headless) with `claude -p`, the Agent SDK, the Claude desktop app's Code tab, the VS Code extension panel, and the browser at claude.ai/code.

In the VS Code extension panel, only a `/plugin` line with something after it, such as `/plugin install <plugin>@<marketplace>`, gets this reply. `/plugin` or `/plugins` typed alone opens the **Manage plugins** dialog.

Install the plugin from the surface you're on instead:

* **Claude desktop app, local or SSH session**: click the **+** button next to the prompt, then **Plugins**, then **Add plugin** to open the [plugin browser](/docs/en/desktop#install-plugins)
* **VS Code extension**: use the **VS Code** tab under [Install a plugin](/docs/en/plugins/install#install-a-plugin)
* **Claude Code on the web, or a desktop cloud session**: a cloud session has no plugin browser. See the **Cloud session** tab under [Install a plugin](/docs/en/plugins/install#install-a-plugin) for what a cloud session loads
* **A terminal you have access to**: run `claude` and type `/plugin` there, or run `claude plugin install <plugin>@<marketplace>` in your shell without starting a session

When a terminal install works, `/plugin` prints an install summary that starts with `✓ Installed <plugin>.` and `claude plugin install` prints `Successfully installed plugin: <plugin>@<marketplace>`.

<h3 id="zsh-no-such-file-or-directory-plugin">
  `zsh: no such file or directory: /plugin`
</h3>

You typed `/plugin ...` at a shell prompt, and the shell reported that no file named `/plugin` exists. Bash reports `bash: /plugin: No such file or directory`.

`/plugin` is a command you type inside a Claude Code session, not at the shell prompt. Start a session and type the same command there:

```shell theme={null}
claude
```

Then, at the Claude Code prompt:

```text theme={null}
/plugin install <plugin>@<marketplace>
```

A successful install prints a summary that starts with `✓ Installed <plugin>.` If the install itself then fails, its message is under [Add a marketplace](#add-a-marketplace) or [Install a plugin](#install-a-plugin).

To install from the shell without starting a session, run `claude plugin install <plugin>@<marketplace>` instead.

<h3 id="the-term-plugin-is-not-recognized-as-the-name-of-a-cmdlet">
  `The term '/plugin' is not recognized as the name of a cmdlet`
</h3>

You typed `/plugin ...` at a PowerShell prompt, and `/plugin` is a Claude Code command, not a program. Bash and Zsh report [their own form of this error](#zsh-no-such-file-or-directory-plugin).

Use either of these instead:

* Run `claude`, then type `/plugin` at the Claude Code prompt
* Run `claude plugin install <plugin>@<marketplace>` in PowerShell without starting a session

<h3 id="claude-command-not-found-after-claude-plugin">
  `claude: command not found` after `claude plugin ...`
</h3>

You ran `claude plugin install ...` in your shell, and the shell couldn't find `claude` at all. On Windows the message is `'claude' is not recognized as the name of a cmdlet` or `'claude' is not recognized as an internal or external command`.

The cause isn't the plugin command. Either Claude Code isn't installed, or its install directory isn't on your `PATH` in this shell. Follow [`command not found: claude` after installation](/docs/en/troubleshoot-install#command-not-found-claude-after-installation), then retry the plugin command.

<h3 id="unknown-command-and-command-spellings-that-dont-exist">
  `Unknown command` and command spellings that don't exist
</h3>

You typed a plugin command you saw somewhere and got `Unknown command: /<name>` in a session, or `error: unknown command '<name>'` or `error: unknown option '<flag>'` from the `claude` binary in your shell.

Several command spellings are in use that Claude Code doesn't have. The table below maps each one to the real command. The [plugin commands reference](/docs/en/plugins/cli-reference) lists every subcommand and flag.

| You typed                                  | What Claude Code says                                                        | Use instead                                                                                                                          |
| :----------------------------------------- | :--------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| `claude plugin add <source>`               | `error: unknown command 'add'`                                               | `claude plugin marketplace add <source>` to add a marketplace, or `claude plugin install <plugin>@<marketplace>` to install a plugin |
| `claude plugin install <plugin> --project` | `error: unknown option '--project'`                                          | `claude plugin install <plugin>@<marketplace> --scope project`                                                                       |
| `/install <plugin>`                        | `Unknown command: /install`                                                  | `/plugin install <plugin>@<marketplace>`                                                                                             |
| `/plugin add <source>`                     | The `/plugin` panel opens on the **Discover** tab                            | `/plugin marketplace add <source>`                                                                                                   |
| `marketplace.anthropic.com` as a source    | `Invalid marketplace source format. Try: owner/repo, https://..., or ./path` | `anthropics/claude-plugins-official` for the official marketplace                                                                    |

These spellings look wrong but work:

* `claude plugins` is an alias of `claude plugin`
* `claude plugin remove` is an alias of `claude plugin uninstall`
* `/plugins` and `/marketplace` in a session open the same panel as `/plugin`

## Add a marketplace

A marketplace is a catalog you add to Claude Code from a git repository, a URL, or a local path. These entries cover the messages you get when adding one fails or a later refresh fails.

<h3 id="marketplace-claude-plugins-official-not-found">
  `Marketplace "claude-plugins-official" not found`
</h3>

You ran `/plugin install <plugin>@claude-plugins-official` in a session, and Claude Code reported that it has no marketplace by that name.

The official marketplace isn't registered on this machine yet. Claude Code normally registers it on its own the first time you start an interactive terminal session. It hasn't run yet if you've only used Claude Code through the VS Code extension, and it skips or defers that step:

* When a policy blocks the source
* When `CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL` is set
* After a failed attempt that's waiting to retry

The `claude plugin` shell commands never register it for you.

Add it, then retry the install:

```text theme={null}
/plugin marketplace add anthropics/claude-plugins-official
```

Claude Code prints `Successfully added marketplace: claude-plugins-official`, and `/plugin marketplace list` shows the marketplace with its source.

For any other marketplace name in this message, see [`Marketplace "<name>" not found`](#marketplace-not-found).

The same string also appears in the `/plugin` **Errors** tab, the panel's list of load failures, when a plugin listed in your settings names a marketplace you haven't added.

<h3 id="marketplace-not-found">
  `Marketplace "<name>" not found`
</h3>

You ran `/plugin install <plugin>@<name>` in a session, often from an install line someone sent you, and Claude Code reported that it has no marketplace by that name.

If the name starts with `claudeai-`, the marketplace is hosted on claude.ai, and you add it by name from your shell with `claude plugin marketplace add --claudeai <name>`. See [Add a marketplace from claude.ai](/docs/en/plugins/install#add-from-claude-ai).

For any other name, an install line names a marketplace but doesn't say where the marketplace is hosted, and Claude Code has no index to look a marketplace name up in. Ask whoever sent the line for the marketplace's source, which is a GitHub `owner/repo`, a git URL, or a path. Then [add the marketplace](/docs/en/plugins/install#add-a-marketplace) and run the install line again.

A marketplace someone sends you is third-party, so [review the plugin before you install it](/docs/en/plugins/security#review-a-plugin-before-you-install).

If you already added the marketplace, check the spelling against `/plugin marketplace list`.

<h3 id="invalid-marketplace-source-format">
  `Invalid marketplace source format`
</h3>

You ran `/plugin marketplace add <source>` or `claude plugin marketplace add <source>`, and Claude Code replied `Invalid marketplace source format. Try: owner/repo, https://..., or ./path`.

Claude Code accepts a source in one of these forms:

* A GitHub `owner/repo` shorthand
* An `https://` or `http://` URL
* A `user@host:path` SSH URL
* A local path starting with `./`, `../`, `/`, or `~`

A bare name such as `claude-plugins-official` matches none of them. Neither does a bare hostname such as `marketplace.anthropic.com`.

Retype the source in one of the accepted forms:

```text theme={null}
/plugin marketplace add anthropics/claude-plugins-official
```

Claude Code prints `Successfully added marketplace: <name>` when the add works.

<h3 id="is-not-a-valid-github-owner-repo-shorthand">
  `'<source>' is not a valid GitHub owner/repo shorthand`
</h3>

You passed a source with a slash that isn't `owner/repo`, such as `github.com/owner/repo` or a `gitlab.example.com/group/project` path. Claude Code refused it with this message and a list of accepted forms.

The `owner/repo` shorthand is GitHub-only and has to follow GitHub's naming rules, so a hostname or an extra path segment fails. Pass the source in the form that matches where the marketplace is hosted:

* **A repository on any host**: the full clone URL
* **A hosted `marketplace.json`**: its `https://` URL
* **A local checkout**: `./path` or an absolute path

For example, to add the official marketplace by its clone URL, in a session:

```text theme={null}
/plugin marketplace add https://github.com/anthropics/claude-plugins-official.git
```

A successful add prints `Successfully added marketplace: <name>`.

<h3 id="path-does-not-exist">
  `Path does not exist: <path>`
</h3>

You passed a local path to `marketplace add`, and nothing exists at that path. A relative path resolves against your current directory.

Check the resolved path in the message. Then run the command from the directory the relative path starts from, or pass an absolute path to the marketplace directory. A successful add prints `Successfully added marketplace: <name>`.

Claude Code accepts a directory that contains `.claude-plugin/marketplace.json`, or a path to a `.json` file. A path to any other file fails with `File path must point to a .json file (marketplace.json)`.

<h3 id="marketplace-file-not-found-at-claude-plugin-marketplace-json">
  `Marketplace file not found at <path>/.claude-plugin/marketplace.json`
</h3>

Claude Code cloned or downloaded the marketplace but found no `marketplace.json` at the expected path inside it. The add command reports it as `Failed to add marketplace: Marketplace file not found at ...`.

The default location is `.claude-plugin/marketplace.json` at the repository root, and the [marketplace reference](/docs/en/plugins/marketplace-reference) lists the accepted locations.

The fix differs for the owner and for everyone else:

* **You own the marketplace**: put the file at that location and re-add the marketplace
* **Someone else hosts it**: ask the owner for the exact source they publish

<h3 id="ssh-authentication-failed-or-https-authentication-failed">
  `SSH authentication failed` or `HTTPS authentication failed`
</h3>

You added or updated a marketplace from a git repository, and the clone failed with `Failed to clone marketplace repository:` followed by one of these lines.

First check the repository itself: a misspelled `owner/repo`, a repository that doesn't exist, or a private repository you can't see also ends in this message. Open the repository URL in your browser, or run `git ls-remote <url>` in your terminal, to confirm it exists and you have access.

If the repository is right, the cause is credentials. Claude Code runs git with interactive prompts disabled, so it can't ask you for a password, a key passphrase, or a credential the way your terminal would. If git needs to prompt, you see `fatal: Cannot prompt because user interactivity has been disabled` or `terminal prompts disabled` in the original error. Only credentials that already work non-interactively succeed:

* **SSH**: `ssh -T git@<host>` must succeed without prompting for a passphrase, and the host must already be in `known_hosts`
* **HTTPS**: your credential helper must hold a token for the host. For GitHub, run `gh auth login` and `gh auth setup-git`. For another host, store a personal access token in your git credential helper. Test with `git ls-remote <url>`

Once `git ls-remote` succeeds in your terminal without a prompt, run the add or update again. A successful add prints `Successfully added marketplace: <name>`. A successful update prints `Successfully updated marketplace: <name>` from your shell, or `✔ Updated 1 marketplace` in a session.

To make Claude Code skip SSH for GitHub `owner/repo` sources, set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`. Without it, Claude Code clones those sources over SSH when an SSH key for `github.com` looks configured, and falls back to HTTPS when the SSH clone fails.

For what background auto-updates can and can't do with your credentials, see [What background auto-update does with credentials](/docs/en/plugins/host-marketplace#what-background-auto-update-does-with-credentials).

<h3 id="ssh-host-key-is-not-in-your-known-hosts-file">
  `SSH host key is not in your known_hosts file`
</h3>

You added a marketplace over SSH from a host you've never connected to, and the clone failed with this line and a `ssh -T git@<host>` hint. For a host whose key changed, the message is `SSH host key has changed` with a `ssh-keygen -R <host>` hint instead.

Claude Code clones with `StrictHostKeyChecking=yes`, so it refuses a host whose key you haven't accepted yet rather than accepting the key automatically. Connect once from your terminal to accept the fingerprint, then retry:

```shell theme={null}
ssh -T git@github.com
```

For a public repository, add the marketplace by its `https://` URL instead to avoid SSH entirely.

<h3 id="command-git-not-found-or-is-in-an-unsafe-location">
  `Command 'git' not found or is in an unsafe location`
</h3>

On Windows, you added a marketplace and Claude Code reported `Failed to clone marketplace repository: Command 'git' not found or is in an unsafe location (current directory)`.

Claude Code looks for `git` on your `PATH` and refuses to run one found only in the current directory. To fix it, install Git and retry:

<Steps>
  <Step title="Install Git for Windows">
    Install Git for Windows so that `git` is on your `PATH`.
  </Step>

  <Step title="Open a new terminal">
    Open a new terminal so the updated `PATH` applies.
  </Step>

  <Step title="Confirm git runs">
    Confirm `git --version` prints a version.
  </Step>

  <Step title="Retry the add">
    Run the `marketplace add` command again.
  </Step>
</Steps>

<h3 id="git-clone-timed-out-after-120s">
  `Git clone timed out after 120s`
</h3>

You added or updated a marketplace, and it failed with `Git clone timed out after 120s`, followed by a hint to set `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`.

Cloning a marketplace, and re-cloning one to update it, gets 120 seconds by default. For a large repository or a slow connection, raise the limit. The value is in milliseconds:

<Tabs>
  <Tab title="Bash or Zsh">
    ```bash theme={null}
    export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000
    ```
  </Tab>

  <Tab title="PowerShell">
    ```powershell theme={null}
    $env:CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS = "300000"
    ```
  </Tab>
</Tabs>

Then retry in the same shell.

If the repository is a monorepo, limit the checkout to the directories you name with `claude plugin marketplace add <source> --sparse <paths>`.

<h3 id="marketplace-updates-keep-failing-offline">
  Marketplace updates keep failing offline
</h3>

You work in an environment where the marketplace's git host is unreachable, and every session repeats a failed refresh in the background. Your existing checkout of the marketplace stays in place and startup isn't delayed.

Each session, for a marketplace with [auto-update on](/docs/en/plugins/loading#which-marketplaces-and-plugins-auto-update), Claude Code checks the marketplace's git host for new commits in the background. When that check can't reach the host, it tries to clone the marketplace again, and offline that clone fails too.

Set this variable to skip the re-clone attempt and keep using the existing checkout when the check can't reach the host:

<Tabs>
  <Tab title="Bash or Zsh">
    ```bash theme={null}
    export CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1
    ```
  </Tab>

  <Tab title="PowerShell">
    ```powershell theme={null}
    $env:CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE = "1"
    ```
  </Tab>
</Tabs>

With the variable set, Claude Code skips the re-clone only for a checkout that already contains `.claude-plugin/marketplace.json`. A marketplace that was never cloned or whose clone stopped partway still gets the clone attempt, so add it once while online.

For a fully offline deployment, pre-populate the plugins directory at image build time with `CLAUDE_CODE_PLUGIN_SEED_DIR` instead, following [Seed containers and CI](/docs/en/plugins/org#seed-containers-and-ci).

<h3 id="marketplace-add-fails-on-a-github-enterprise-server-host">
  Marketplace add fails on a GitHub Enterprise Server host
</h3>

You added a marketplace from a GitHub Enterprise Server (GHES) URL and got a policy error, or you added it from claude.ai and got a GitHub access error.

Both cases are on the GHES page:

* [A policy error](/docs/en/github-enterprise-server#marketplace-add-fails-with-a-policy-error) means your organization restricted marketplace sources and an admin needs to add a `hostPattern` for the host
* [A GitHub access error on claude.ai](/docs/en/github-enterprise-server#marketplace-add-on-claude-ai-fails-with-a-github-access-error) means your own GitHub Enterprise account isn't connected yet

## Install a plugin

You added a marketplace and ran an install, and the install stopped with a message instead of installing anything. These entries cover those messages. They also cover the related messages that appear later in the `/plugin` **Errors** tab, or as an empty **Discover** tab, when a plugin or its marketplace can't be found, read, or trusted.

<h3 id="plugin-not-found-in-marketplace">
  `Plugin "<name>" not found in marketplace "<marketplace>"`
</h3>

You ran `/plugin install <name>@<marketplace>` or `claude plugin install <name>@<marketplace>`, and the plugin name isn't in the copy of that marketplace's catalog on your machine.

`claude plugin install` in your shell prints the same message when you haven't added the marketplace at all. If `claude plugin marketplace update <marketplace>` then answers `Marketplace '<marketplace>' not found`, [add the marketplace](#add-a-marketplace) first.

<h4 id="the-message-ends-with-a-refresh-hint">
  `not found in marketplace` with a refresh hint
</h4>

The hint reads `Your local copy may be out of date — try claude plugin marketplace update <marketplace>` or `The marketplace couldn't be refreshed (...)`. Claude Code didn't refresh the marketplace before the lookup, such as when you're offline, so your copy of the catalog may be stale. Refresh with the marketplace's name, then install again:

```text theme={null}
/plugin marketplace update <marketplace>
```

`claude plugin marketplace update` prints `Successfully updated marketplace: <name>`, and `/plugin marketplace update` shows `✔ Updated 1 marketplace`. If the retried install prints the same message, check the name as [`not found in marketplace` with no hint](#the-message-has-no-hint) describes. [When Claude Code refreshes a marketplace before an install](/docs/en/plugins/loading#when-claude-code-refreshes-a-marketplace-before-an-install) lists the other cases where the refresh doesn't run.

<h4 id="the-message-has-no-hint">
  `not found in marketplace` with no hint
</h4>

The name is the likeliest problem. Open `/plugin`, go to **Discover**, and copy the name from the list.

Before v2.1.232, Claude Code refreshed the named marketplace only after the lookup missed, and only when auto-update was on for it.

<h3 id="plugin-not-found-in-any-marketplace">
  `Plugin "<name>" not found in any marketplace`
</h3>

You ran `/plugin install <name>` with no `@marketplace`, and no registered marketplace has that plugin. `claude plugin install <name>` reports `Plugin "<name>" not found in any configured marketplace`.

Without a marketplace name, `claude plugin install` searches the catalogs it already has and doesn't refresh them first, and `/plugin install` refreshes only marketplaces that have auto-update on. Name the marketplace, and Claude Code refreshes it before looking the plugin up:

```text theme={null}
/plugin install <name>@<marketplace>
```

When the install works, you see `✓ Installed <plugin>.` in a session, or `Successfully installed plugin: <plugin>@<marketplace>` from `claude plugin install`.

If you don't know which marketplace lists the plugin, run `/plugin marketplace list` for the marketplaces you have, and browse **Discover** in `/plugin` for the plugin name.

<h3 id="plugin-is-already-installed-globally">
  `Plugin '<name>@<marketplace>' is already installed globally`
</h3>

You ran `/plugin install` for a plugin that's already installed at user scope or by managed settings, and Claude Code refused with `Use '/plugin' to manage existing plugins.` If you typed the plugin name without `@<marketplace>`, the message omits `globally`.

The plugin is already available in every project, so there's nothing to add. To change its [scope](/docs/en/plugins/install), enable or disable it, or configure it, open `/plugin` and go to **Installed**.

A plugin installed only at project or local scope doesn't trigger this message. Claude Code lets you install it at user scope as well, so it's available in other projects.

`claude plugin install` in your shell prints a different message. For a plugin already installed at the target scope, it prints `Plugin "<name>@<marketplace>" is already installed (scope: user)` and exits 0. If its cache directory is missing, the same command re-downloads it.

<h3 id="this-plugin-uses-a-source-type-your-claude-code-version-does-not-suppo">
  `This plugin uses a source type your Claude Code version does not support`
</h3>

You installed a plugin whose marketplace entry uses a source type this version of Claude Code can't fetch, and Claude Code stopped with this message and `Update Claude Code and try again.`

Update Claude Code, then retry the install. Source types are on the [marketplace reference](/docs/en/plugins/marketplace-reference).

<h3 id="plugin-archive-integrity-check-failed">
  `Plugin archive integrity check failed`
</h3>

You installed a plugin that's distributed as a zip archive, and Claude Code refused it with this line and `The archive was not installed.` The plugin's marketplace entry uses an [`archive` source](/docs/en/plugins/marketplace-reference) with a `sha256` pin, and the downloaded file's digest doesn't match the pin.

The full message looks like this:

```text theme={null}
Plugin archive integrity check failed for https://artifacts.example.com/claude-plugins/my-plugin.zip: expected sha256 6bfa50e3d2e00c052b46abe51fff89346ac803e45771f76dcf6df1ab74cca5e1, got ac52220c0914ef8ca6a602e4a7362f88d30fb021110f72a6d15b68c3fe7df2b7. The archive was not installed. Verify the sha256 in the marketplace entry, or that the URL serves the intended file.
```

The fix differs for the publisher and the installer:

* **You publish the plugin**: recompute the digest of the exact file the URL serves and update the `sha256` in the marketplace entry. Use `shasum -a 256 my-plugin.zip`, or `Get-FileHash -Algorithm SHA256 my-plugin.zip` in PowerShell
* **You install the plugin**: run `/plugin marketplace update <name>` in a session to refresh the catalog in case the entry was corrected, then retry the install. If the digests still disagree after the refresh, ask the marketplace owner which file they pinned before installing

<h3 id="marketplace-is-registered-from-an-untrusted-source">
  `Marketplace "<name>" is registered from an untrusted source`
</h3>

A marketplace you added earlier stopped loading, and so did its plugins. This line appears in the `/plugin` **Errors** tab or on the next refresh.

The marketplace is registered under a name that is [reserved for official Anthropic marketplaces](/docs/en/plugins/marketplace-reference), but its registered source isn't an `anthropics` GitHub repository. Reserved names are re-checked every time a marketplace loads or refreshes, so the marketplace and the plugins installed from it stop loading.

The full message names the reserved name and the fix:

```text theme={null}
Marketplace "claude-community" is registered from an untrusted source: The name 'claude-community' is reserved for official Anthropic marketplaces. Only repositories from 'github.com/anthropics/' can use this name. To fix it, remove the marketplace and re-add it from the official source.
```

The fix differs for users and publishers:

* **You use the marketplace**: in your shell, run `claude plugin marketplace remove <name>`, then add the marketplace again from the official `github.com/anthropics` repository
* **You publish a third-party marketplace that used the name before it became reserved**: rename it and ask users to re-add it from your source

Before v2.1.205, Claude Code checked the name only when you added the marketplace, so an entry registered before its name became reserved kept loading.

<h3 id="plugin-has-a-corrupt-manifest-file-or-has-an-invalid-manifest-file">
  `Plugin <name> has a corrupt manifest file` or `has an invalid manifest file`
</h3>

Claude Code fetched the plugin, then failed to read its `.claude-plugin/plugin.json`. In the shell, the `<name>` in this line can be a temporary directory name; the `Failed to install plugin "<name>@<marketplace>"` prefix carries the plugin's real name. The wording says which check failed:

* **`corrupt manifest file`, followed by `JSON parse error:`**: the file isn't valid JSON
* **`invalid manifest file`, followed by `Validation errors:`**: the file parses but fails the schema, such as `name: Invalid input` for a missing required field

`claude plugin install` reports either as `Failed to install plugin "<name>@<marketplace>":` and exits with code 1.

The plugin's author has to fix the file, and the plugin can't be installed until then:

* **If that's you**: run `claude plugin validate <plugin-directory>` in your shell to see the same error with the offending path, then fix the file
* **If it isn't you**: report the message to the marketplace owner

<h3 id="plugin-directory-not-found-at-path">
  `Plugin directory not found at path: <path>`
</h3>

The **Errors** tab in `/plugin` shows this for an enabled plugin that its marketplace lists by a relative path, such as `./plugins/my-plugin`, when no directory exists at that path inside the marketplace. If you maintain the marketplace, correct the entry's `source` path or restore the folder. Otherwise, report the message to the marketplace owner.

`Marketplace directory not found at path: <path>` means the marketplace's own directory is missing instead. For a marketplace you added from a local path, that directory moved or was deleted. Restore it, or remove the marketplace and add it again from its new location.

<h3 id="no-plugins-available-or-no-marketplaces-configured">
  `No plugins available` or `No marketplaces configured`
</h3>

You opened `/plugin` and the **Discover** tab is empty, or `claude plugin marketplace list` printed `No marketplaces configured`.

No marketplace is registered, so there's no catalog to show. In a session, add the official marketplace, `anthropics/claude-plugins-official`:

```text theme={null}
/plugin marketplace add anthropics/claude-plugins-official
```

Claude Code prints `Successfully added marketplace: claude-plugins-official`, and **Discover** lists its plugins. The [Anthropic marketplaces](/docs/en/plugins/anthropic-marketplaces) page lists the other marketplaces you can add.

<h3 id="marketplace-is-already-added-from-a-different-source">
  `Marketplace "<name>" is already added from a different source`
</h3>

You confirmed adding a marketplace through [`/plugin install <plugin> --marketplace <source>`](/docs/en/plugins/install#add-a-marketplace-and-install-in-one-command), and the catalog Claude Code fetched from that source has the same name as a marketplace you already added from a different source. Claude Code keeps the existing marketplace instead of replacing it, and the plugin isn't installed.

The full message looks like this:

```text theme={null}
Marketplace "acme-tools" is already added from a different source (github:acme/plugins). To use this source instead, remove that marketplace first with /plugin marketplace remove acme-tools.
```

Choose which source you want:

* **The marketplace you already added**: install from it by name with `/plugin install <plugin>@<name>`
* **The new source**: run `/plugin marketplace remove <name>`, then retry the install

<h3 id="cannot-add-marketplace-its-network-source-differs">
  `Cannot add marketplace "<name>": its network source differs from the one declared for it in settings`
</h3>

You ran `marketplace add`, and the catalog at that source has the same name as a marketplace that a settings file already declares under [`extraKnownMarketplaces`](/docs/en/settings-reference#extraknownmarketplaces) with a different source. Claude Code refuses the add and registers nothing.

The message ends with the fix: the source must match the one declared for this name in settings, or you change the declaration. Compare the source you passed against the `extraKnownMarketplaces` entry for that name, including its `ref`, `path`, and `headers`, then do one of these:

* **Use the declared source**: add the marketplace from the source the settings entry names
* **Use the new source**: edit or remove the `extraKnownMarketplaces` entry, then add the marketplace again. If managed settings declare it, ask your administrator

<h3 id="failed-to-install-from-the-plugin-menu">
  `Failed to install: <plugin> (<reason>)`
</h3>

You selected plugins to install in the `/plugin` menu, none of them installed, and the menu closed with this summary of what failed.

Some reasons, such as git's output after a failed clone, show only their first line. When such a reason was shortened, the summary ends with `Installing a plugin from its details (Enter) in /plugin shows its full error.`

What to do depends on whether the summary shortened the reason:

* Fix what the reason in parentheses names
* When the reason was shortened, run `/plugin`, select the plugin on the **Discover** tab, and press **Enter** to install it from its details. If the install fails there, the details view shows the whole error

<h3 id="could-not-move-the-new-copy-of-this-plugin-version">
  `Could not move the new copy of this plugin version into <path>`
</h3>

When you install a plugin, Claude Code downloads a fresh copy of its files and moves it into that version's folder in the [plugin cache](/docs/en/plugins/loading#find-plugins-on-disk). This message means the move failed, usually because another program was using the folder while the install ran. The file-system code appears in parentheses:

```text theme={null}
Could not move the new copy of this plugin version into /home/user/.claude/plugins/cache/acme-tools/formatter/1.2.0: the new copy or the version folder stayed busy while the install ran (ENOTEMPTY) — usually a scanner still reading the freshly downloaded files, another program using that folder, or another process re-creating it. The previously installed copy was moved back. Run the install again once other Claude Code sessions or programs using that folder have finished.
```

The message says what happened to the copy that was installed before, which tells you whether the plugin still works:

* `The previously installed copy was moved back`: the version you had is still installed
* `had to be removed first`, `was not moved back`, or `could not be moved back`: that plugin version isn't installed until an install succeeds
* No such sentence: there was no earlier copy, so the version isn't installed yet

On Windows, when another program holds the installed copy itself, the message instead says that copy `could not be replaced` and that `It was not replaced and the new copy was discarded`, so the version you had is still installed.

A `Left on disk` list names set-aside folders inside the cache. A later install of that version or a plugin cache cleanup removes them, so you don't need to delete them.

To fix the install:

* Close other Claude Code sessions, editors, and terminals that are using the plugin's folder under `~/.claude/plugins/cache`, then run the install again
* When the message says to check the plugin cache folder's permissions, restore your write permission on the folder it names and free disk space, then run the install again

<h3 id="dependency-errors">
  Dependency errors
</h3>

A plugin that declares dependencies can fail to install, or install and stay disabled, when a dependency can't be satisfied. The message reaches you at install time or at load time:

* **During install**: the refusal comes back as the install's error message
* **When the plugin loads**: the problem appears in `claude plugin list` and the `/plugin` **Errors** tab, and Claude Code keeps the affected plugin disabled until you resolve it

The table lists each message and its fix. To declare dependencies as an author, see [Plugin dependencies](/docs/en/plugins/dependencies).

| Message                                                                                         | Meaning                                                                                           | How to resolve                                                                                                                                                                                                                                                      |
| :---------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Dependency "<dep>" is not installed`                                                           | A declared dependency isn't installed.                                                            | Install it in your shell with `claude plugin install <dep>@<marketplace>`, or uninstall the plugin. If the dependency's marketplace isn't registered yet, add it and run `/reload-plugins` in your session, which installs the missing dependencies it can resolve. |
| `Dependency "<dep>" is disabled`                                                                | The dependency is installed but turned off.                                                       | Enable the dependency, or uninstall the plugin that needs it.                                                                                                                                                                                                       |
| `Requires "<dep>" <range>, installed <version>`                                                 | The installed dependency's version is outside the plugin's declared range.                        | Update the dependency to a version in the range, or uninstall the plugin.                                                                                                                                                                                           |
| `<Plugin or Dependency> "<name>" has conflicting version requirements`                          | No version satisfies every range that pins it. The message lists the ranges.                      | Uninstall or update one of the conflicting plugins, or ask the upstream author to widen its constraint.                                                                                                                                                             |
| `... has version requirements too complex to intersect` or `has an invalid version requirement` | A range isn't valid semver, or the combined ranges can't be intersected.                          | Fix the invalid range or simplify long `\|\|` chains.                                                                                                                                                                                                               |
| `... has no git tag satisfying <range>`                                                         | The dependency's repository has no `<name>--v*` tag in the range.                                 | Check that the upstream tags releases with that convention, or relax the range.                                                                                                                                                                                     |
| `Dependency "<dep>" (required by <plugin>) is in <marketplace>, which is not in the allowlist`  | The dependency is in a different marketplace, and cross-marketplace resolution is off by default. | Install the dependency yourself at the same scope, in your shell with `claude plugin install <dep>@<marketplace>` plus the `--scope` you're installing the plugin at, then retry.                                                                                   |

To see these programmatically, run `claude plugin list --json` in your shell. Plugins with problems carry an `errors` field with the messages and an `errorDetails` field with a `type` for each: the first two rows are `dependency-unsatisfied` and the third is `dependency-version-unsatisfied`.

## Plugin installed but not working

The install succeeded, but the plugin's skills, hooks, or servers aren't doing anything. Start with [Plugin doesn't appear or its skills don't show up](#plugin-doesnt-appear-or-its-skills-dont-show-up), which tells you where Claude Code reports what it loaded, then match the message.

<h3 id="plugin-doesnt-appear-or-its-skills-dont-show-up">
  Plugin doesn't appear or its skills don't show up
</h3>

You installed a plugin and typed `/` expecting its skills, or asked Claude to use it, and nothing happened.

Check the plugin's state before changing anything:

<Steps>
  <Step title="Confirm the plugin is installed and enabled">
    Run `/plugin` and open **Installed**. Confirm the plugin is listed and enabled. `claude plugin list` in your shell prints the same list with each plugin's version, scope, and `Status: ✔ enabled`.
  </Step>

  <Step title="Read the Errors tab">
    Open the **Errors** tab in the same panel. Each entry pairs a message with a guidance line. Most messages in the rest of this section come from that tab.
  </Step>

  <Step title="Reload if you installed during this session">
    If the plugin is installed and error-free but you installed it during this session, run `/reload-plugins`. It prints `Reloaded:` with counts of plugins, skills, agents, hooks, and servers. When something failed it adds `N errors during load. Run /plugin for details.`
  </Step>
</Steps>

If the plugin loads with no error and its skills still don't appear, the next step differs for your own plugin and for someone else's:

* **A plugin you're building**: see [Plugin loads but its skills are missing](#plugin-loads-but-its-skills-are-missing)
* **A plugin someone else published**: open **Installed** in `/plugin` and open the plugin's details pane, which lists what the plugin contains. A plugin that lists no skills there has none to offer when you type `/`

<h3 id="run-reload-plugins-to-activate">
  `Run /reload-plugins to activate.`
</h3>

The install summary in `/plugin` ended with `Run /reload-plugins to activate.` instead of `Plugin is now active.`

Claude Code didn't activate the plugin during the install, either because activating it would [invalidate the prompt cache](/docs/en/prompt-caching#enabling-or-disabling-a-plugin) or because the activation attempt failed.

You don't need to type the command. The panel closes and Claude Code runs `/reload-plugins` for you, or queues it until the response that's streaming finishes.

Read what that reload prints:

* **`Reloaded:` with counts of plugins, skills, agents, hooks, and servers**: the plugin is now active. When something failed to load, the line adds `N errors during load. Run /plugin for details.`
* **`This reload changes MCP tools (...) — your next message will re-read the whole conversation instead of using the cache. Run /reload-plugins --force to apply.`**: the reload would add or remove a plugin MCP server, or the `LSP` tool, and invalidate your prompt cache. For the LSP case the line starts `This reload adds the LSP tool` or `This reload removes the LSP tool`. Run it with `--force` to activate the plugin anyway, or start a new session

Before v2.1.268, an install that didn't activate during the install stayed pending until you ran `/reload-plugins` yourself.

Before v2.1.246, the skills count in that summary included only a plugin's `commands/` entries, so a reload could load a plugin's `SKILL.md` skills and still report `0 skills`.

<h3 id="plugin-not-cached-at">
  `Plugin "<name>" not cached at <path>`
</h3>

The **Errors** tab shows this line with the guidance `Run /plugin to refresh the plugin cache`. Claude Code has an install record for the plugin, but the directory the record points at is missing, for example after you cleared the cache.

Reinstall the plugin from your shell. `claude plugin install <name>@<marketplace>` re-downloads a plugin whose install directory is missing even though its record exists:

```shell theme={null}
claude plugin install <name>@<marketplace>
```

Then run `/reload-plugins` in your session. The **Errors** tab entry disappears and the plugin is back under **Installed**.

<h3 id="a-plugin-you-disabled-still-loads">
  `Disabled in ~/.claude/settings.json but still loads`
</h3>

You set a plugin to `false` in `~/.claude/settings.json`, and its row in `claude plugin list` or `/plugin` shows this message followed by the source that enables it, such as `— project settings enable it, which overrides your user setting`. A `true` in that higher-precedence source is overriding your user setting.

To opt out of a project-enabled plugin on your machine, set the id to `false` in `.claude/settings.local.json`, which has higher precedence than the project file. For the other sources the message can name, see [Disabled in user settings but still loads](/docs/en/plugins/loading#disabled-in-user-settings-but-still-loads).

If `claude plugin list` instead marks the plugin `required by your org`, no settings file is involved: your organization marks that synced plugin as required on claude.ai, and it loads even if you disabled it earlier. See [Plugins synced from claude.ai](/docs/en/plugins/loading#synced-plugins).

<h3 id="plugin-is-enabled-in-project-settings-but-isnt-installed-here">
  `Plugin "<name>" is enabled in project settings but isn't installed here`
</h3>

The **Errors** tab shows this line for a plugin your project's `.claude/settings.json` enables, with the guidance `Run claude plugin install <name>@<marketplace> --scope project to install it for this project`.

A repository's settings can enable a plugin for everyone who opens it, but they don't install it. When the plugin comes from an external source such as a GitHub repository or an npm package, Claude Code doesn't download it until you install it yourself. Run the command from the guidance line in your shell, then reload:

```shell theme={null}
claude plugin install <name>@<marketplace> --scope project
```

After you run `/reload-plugins` in your session, the **Errors** tab entry is gone and the plugin is listed under **Installed**.

If your organization pre-installs plugins for you, it does so through managed settings instead. See [Pre-install and require plugins](/docs/en/plugins/org#pre-install-and-require-plugins).

<h3 id="failed-to-load-hooks-from-and-hooks-that-dont-fire">
  `Failed to load hooks from <path>` and hooks that don't fire
</h3>

A plugin's hooks don't run. Either the **Errors** tab shows a load failure for them, the hooks load and you see `<Event> hook error` notices in the transcript, or a hook loads without error and never fires.

#### Hooks fail to load

The **Errors** tab shows one of these messages:

* **`Failed to load hooks from <path>: <reason>`**: `hooks/hooks.json` isn't valid JSON or fails the hooks schema. The reason names the parse or validation error. Fix the file. To catch a JSON syntax problem in `hooks/hooks.json` before you publish the plugin, run `claude plugin validate <plugin-directory>` in your shell
* **`hooks path not found: <path>`**: the manifest's `hooks` field names a file that doesn't exist at that path relative to the plugin root. Fix the path or add the file

#### `hook error` notices in the transcript

A notice of the form `... hook error: Failed with non-blocking status code: <stderr>` means the hook ran and its command failed. For example, `Stop hook error: Failed with non-blocking status code: /bin/sh: node: command not found` means the shell Claude Code spawned couldn't find `node`. Install it, or make sure it's on the `PATH` of the terminal you start `claude` from.

For any other error, run the hook's command yourself from the plugin directory to see the full output, or capture the full stderr with [debug logging](/docs/en/hooks#debug-hooks).

#### Hook loads but never fires

If a hook loads without error but never fires, check its definition and then watch it run:

<Steps>
  <Step title="Check the event name">
    Event names are case-sensitive, so confirm yours matches exactly, for example `PostToolUse`.
  </Step>

  <Step title="Check the matcher">
    Confirm the hook's `matcher` matches the tool name.
  </Step>

  <Step title="Trigger the event on purpose">
    For a `PostToolUse` hook, ask Claude to edit a file.
  </Step>

  <Step title="Read the debug log">
    Open the [debug log](/docs/en/hooks#debug-hooks), which records which hooks matched. A hook that ran shows up there with its exit code.
  </Step>
</Steps>

<h3 id="invalid-mcp-server-config-for-and-mcp-servers-that-dont-start">
  `Invalid MCP server config for "<server>"` and MCP servers that don't start
</h3>

A plugin bundles an MCP server, and the **Errors** tab shows `Invalid MCP server config for "<server>": <error>`, or the server is listed but `/mcp` never shows it connected.

#### `Invalid MCP server config for "<server>": <error>`

The server's configuration passes the schema check, but Claude Code can't resolve it for this session. The text after the colon names the cause and decides the fix:

* **`Missing environment variables: <names>`**: set those variables in the shell you start Claude Code from, then start a new session
* **`URL is unset or invalid`**: a `${user_config.*}` option that the URL uses isn't set. Run `/plugin configure <plugin>` to set it
* **`has an invalid MCP url`** or **`headersHelper for MCP server '<server>' references ${user_config.*}`**: the plugin's own configuration is at fault. Fix the `url` or `headersHelper` in your plugin's MCP configuration, or report it to the plugin's author if the plugin isn't yours. The `headersHelper` case has its own entry under [plugin command references user\_config](/docs/en/errors#plugin-command-references-user-config)

#### Server is configured but never connects

Run `/mcp` to see the server's status. When the server is healthy, `/mcp` lists it as connected.

To read the error the server printed while starting, run `claude --debug` and open the log at `~/.claude/debug/<session-id>.txt`. The `--debug` flag doesn't print to the terminal.

A server entry in `.mcp.json` that fails the schema doesn't appear in the **Errors** tab. Claude Code drops that server and records `Invalid MCP server config for <server> in <path>` only in that debug log. To find the entry without loading the plugin, run `claude plugin validate` in your shell on the plugin directory, which reports it as an error.

Before v2.1.281, `claude plugin validate` didn't check `.mcp.json`.

#### Server works with `--plugin-dir` but fails after install

You're the plugin's author, and the server starts when you load the plugin from its source directory with `--plugin-dir` but fails once the plugin is installed.

Claude Code copies an installed plugin into its cache, so a path that only works from the source directory breaks. Write paths inside the plugin with `${CLAUDE_PLUGIN_ROOT}`.

For paths that reach outside the plugin directory, see [Files the plugin references outside its directory aren't found](#files-the-plugin-references-outside-its-directory-arent-found).

<h3 id="language-server-doesnt-start">
  Language server doesn't start, uses too much memory, or reports wrong diagnostics
</h3>

You installed a [code intelligence plugin](/docs/en/plugins/code-intelligence) and Claude isn't seeing diagnostics, or the language server is using too much memory or reporting errors that aren't real.

#### Language server doesn't start

The plugin connects to a language server binary you install separately, and Claude Code spawns it by command name from your `PATH`.

The `/plugin` **Errors** tab shows the failure with its reason, such as `Executable not found in $PATH: "<binary>"`, and `claude --debug` logs it as `LSP server <name> failed to start: <reason>`.

Install the binary and confirm it's on the `PATH` of the terminal you start `claude` from, for example with `which typescript-language-server`. Then start a new session.

#### Language server uses too much memory

Language servers such as `rust-analyzer` and `pyright` index the whole project. Disable the plugin with `/plugin disable <plugin>` in a session and rely on Claude's built-in search tools instead.

#### False positive diagnostics in a monorepo

A language server that isn't configured for the workspace can report unresolved imports for internal packages. There's nothing to fix on the Claude Code side, and the diagnostics don't stop Claude from editing code.

## Build a plugin

You're developing a plugin and loading it with `--plugin-dir` or installing it from a local marketplace. These entries cover the failures you hit while developing a plugin. For the checks to run after each change, see [Test and debug](/docs/en/plugins/create#test-and-debug).

Two failures that also reach a plugin's users have their entries under [Plugin installed but not working](#plugin-installed-but-not-working):

* **A hook that doesn't fire**: see [hooks that don't fire](#failed-to-load-hooks-from-and-hooks-that-dont-fire)
* **An MCP server that doesn't start**: see [MCP servers that don't start](#invalid-mcp-server-config-for-and-mcp-servers-that-dont-start)

<h3 id="commands-path-not-found">
  `commands path not found: <path>`
</h3>

The **Errors** tab shows `commands path not found: <absolute path>` with the guidance `Check that the path in your manifest or marketplace config is correct`. The same message appears for `skills`, `agents`, and `hooks`.

Claude Code resolved a path from your `plugin.json` or marketplace entry against the plugin root and found nothing there. The path in the message is the absolute path it checked, so compare it with what's on disk. Fix the path or create the directory, then run `/reload-plugins`.

Paths in the manifest are relative to the plugin root and start with `./`. A path that resolves outside the plugin root is reported as `<component> path escapes plugin directory` instead and is dropped.

<h3 id="plugin-dir-loads-a-plugin-with-no-components">
  `--plugin-dir` at a marketplace root doesn't load the plugins under `plugins/`
</h3>

You started `claude --plugin-dir <path>` and see no error, but the plugin's skills, agents, and hooks aren't there.

`--plugin-dir` takes the plugin's root directory, the one that contains `.claude-plugin/plugin.json` and the component directories such as `skills/`. If you point it at a marketplace root instead, Claude Code doesn't read `marketplace.json`, so a plugin under `plugins/` doesn't load, and you see no error. Before v2.1.281, Claude Code loaded a marketplace root as one empty plugin named after that directory. Point the flag at the plugin directory itself:

```shell theme={null}
claude --plugin-dir ./my-marketplace/plugins/my-plugin
```

Then open **Installed** in `/plugin`, where the plugin's details pane lists its components.

<h3 id="files-the-plugin-references-outside-its-directory-arent-found">
  Files the plugin references outside its directory aren't found
</h3>

A plugin works from its source directory with `--plugin-dir` but fails after install, with errors about a path such as `../shared-utils`.

Claude Code copies an installed plugin into its cache and loads it from there, so a path that reaches outside the plugin's own directory points at nothing in the cache. Move the shared files inside the plugin directory, or reference them through a symlink inside it. For where the cache is and how paths resolve, see [Find plugins on disk](/docs/en/plugins/loading#find-plugins-on-disk).

<h3 id="claude-plugin-root-shows-forward-slashes-on-windows">
  `${CLAUDE_PLUGIN_ROOT}` shows forward slashes on Windows
</h3>

On Windows, a plugin hook receives `${CLAUDE_PLUGIN_ROOT}` as `C:/Users/you/...` rather than `C:\Users\you\...`, and a script that expected backslashes breaks.

Claude Code runs shell-form hooks through Git Bash on Windows and substitutes the plugin root in the forward-slash Win32 form on purpose. Bash builtins, MSYS tools, and native Windows binaries all accept that form.

If your script needs backslashes, switch the hook to one of the forms that keep native paths, described under [exec form and shell form](/docs/en/hooks#exec-form-and-shell-form):

* An exec-form hook, which spawns the process directly with an `args` array
* A hook with `"shell": "powershell"`

<h3 id="plugin-loads-but-its-skills-are-missing">
  Plugin loads but its skills are missing
</h3>

Your plugin is listed under **Installed** with no errors, but its skills aren't offered when you type `/`.

Skills load from `skills/` at the plugin root and commands from `commands/` at the plugin root. Only `plugin.json` belongs inside `.claude-plugin/`, and a `skills/` directory inside `.claude-plugin/` isn't scanned. Move the directories to the plugin root and run `/reload-plugins`. Afterward, the plugin's details pane in `/plugin` lists the skills, and typing `/` offers them.

Each skill is a directory containing `SKILL.md`. A `skills` entry in the manifest that points at a `SKILL.md` file rather than its directory is reported as `path is a file; skills entries must be directories containing SKILL.md`.

<h3 id="skill-loads-but-claude-never-invokes-the-skill">
  Skill loads but Claude never invokes the skill
</h3>

Your plugin's skill runs when you type its `/<plugin>:<skill>` command, but Claude never invokes it in response to a plain request.

Check these causes in order:

* **The skill sets `disable-model-invocation: true`**: with that field set, only you can invoke the skill. The template skill in [Create your first plugin](/docs/en/plugins/create#create-your-first-plugin) sets it. Remove the line from a skill you want Claude to invoke on its own. [Control who invokes a skill](/docs/en/skills#control-who-invokes-a-skill) covers the field
* **The description doesn't match how people ask**: work through the checks in [Skill not triggering](/docs/en/skills#skill-not-triggering)
* **The description is truncated**: when many skills are installed, Claude Code shortens descriptions to fit the listing's character budget, which can strip the keywords Claude needs to match a request. See [Skill descriptions are cut short](/docs/en/skills#skill-descriptions-are-cut-short)

To measure how often the skill triggers across realistic prompts rather than checking one at a time, write an eval case with a [`tool_used: Skill` grader](/docs/en/plugin-evals#create-your-first-eval-suite) and run it with `claude plugin eval` after each description change.

<h3 id="is-not-a-plugin-or-skill-folder">
  `<directory> is not a plugin or skill folder` from `claude plugin eval init`
</h3>

You ran `claude plugin eval init` from a directory that isn't a plugin's root, such as your home directory or the root of a repository that keeps the plugin in a subdirectory. `init` writes the suite under the working directory, so it stops instead of creating an `evals/` directory the plugin would never see.

Change to the plugin's root, the directory that holds `.claude-plugin/plugin.json` or the skill's `SKILL.md`, and run the command again. To scaffold the suite somewhere else on purpose, pass `--eval-dir`. See [Test plugins with evals](/docs/en/plugin-evals).

<h3 id="the-userconfig-dialog-never-appears">
  The `userConfig` dialog never appears
</h3>

Your plugin declares `userConfig` options, but no configuration dialog appears when you install it.

The interactive install shows the dialog, and the shell command takes the values as flags instead:

* **`/plugin install` in a session, or the Discover tab in `/plugin`**: the dialog is part of this interactive install
* **`claude plugin install` in your shell**: never prompts for `userConfig` values. It saves any `--config KEY=VALUE` values you pass, and when options remain unset it prints `N userConfig options not yet set — run /plugin configure <plugin>@<marketplace> in Claude Code, or pass --config KEY=VALUE.` When any of the unset options is required, `(M required)` follows `not yet set`.

If you installed from the shell, pass the values with `--config`, one flag per option:

```shell theme={null}
claude plugin install my-plugin@my-marketplace --config api_url=https://example.com
```

When every option is set, the install output carries no `not yet set` line. To open the dialog afterwards instead, run `/plugin configure my-plugin@my-marketplace` in a session.

If you pass a `--config` key the manifest doesn't declare, the plugin still installs, and the command prints `⚠ Installed, but --config not applied: --config key "<key>" isn't declared in this plugin's userConfig.` followed by the keys the plugin does declare.

<h3 id="claude-plugin-validate-reports-errors">
  `claude plugin validate` reports errors
</h3>

You ran `claude plugin validate <path>`, or `/plugin validate <path>` in a session, and it printed `Found N errors` and `Validation failed`, then exited with code 1.

The validator reads the manifest at the path you give it: `.claude-plugin/plugin.json` for a plugin directory, or `.claude-plugin/marketplace.json` for a marketplace directory. For a marketplace, it prefixes problems in an entry's own manifest with the entry index, as `plugins[1] plugin.json → json: ...`.

The table covers the messages that stop validation and two warnings, `No frontmatter block found` and `Unknown field '<key>'`, which stop it only when you pass `--strict`. Other warnings, such as a missing description, aren't listed.

| Message                                                                                                  | Cause                                                                    | Fix                                                                                                        |
| :------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- |
| `File not found: <path>`                                                                                 | The path has no manifest, or doesn't exist.                              | Run the command against the plugin or marketplace root, the directory that contains `.claude-plugin/`.     |
| `No manifest found in directory. Expected .claude-plugin/marketplace.json or .claude-plugin/plugin.json` | The directory has no `.claude-plugin/` manifest.                         | Create the manifest, or point at the right directory.                                                      |
| `Invalid JSON syntax: <parse error>`                                                                     | The manifest, or `hooks/hooks.json`, isn't valid JSON.                   | Fix the JSON. Until you fix `hooks/hooks.json`, a session loads the plugin without the hooks in that file. |
| `Path not found: <path>. The runtime loader will report this as a load failure.`                         | A component path in the manifest doesn't exist.                          | Fix the path or create the directory.                                                                      |
| `Path contains ".." which could be a path traversal attempt: <path>`                                     | A component path escapes the plugin directory.                           | Use paths inside the plugin root.                                                                          |
| `Path is a file; skills entries must be directories containing SKILL.md`                                 | A `skills` entry points at `SKILL.md` instead of its directory.          | Point at the parent directory, or `.` for a root-level `SKILL.md`.                                         |
| `No frontmatter block found` or `YAML frontmatter failed to parse: <error>`                              | A skill, agent, or command file has missing or invalid YAML frontmatter. | Add or fix the frontmatter between `---` delimiters. Reported when validating a plugin directory.          |
| `Unknown field '<key>'`                                                                                  | The manifest has a field the schema doesn't define.                      | Remove it, or use the name the message suggests. Claude Code ignores unknown fields at load time.          |

Run the command again after each fix until it prints no errors.

`plugin.json` fields are on the [manifest reference](/docs/en/plugins/manifest-reference), and marketplace-level messages are under [Marketplace validation errors](#marketplace-validation-errors).

<h3 id="plugin-has-conflicting-manifests">
  `Plugin <name> has conflicting manifests`
</h3>

The plugin fails to load with `Plugin <name> has conflicting manifests: both plugin.json and marketplace entry specify components.`

The plugin has its own `plugin.json`, and its marketplace entry sets `strict: false` while also declaring any of `commands`, `agents`, `skills`, `hooks`, `outputStyles`, or `themes`. Remove those fields from the entry, or set `strict: true` in the entry so Claude Code appends them to `plugin.json`. See [Strict mode](/docs/en/plugins/marketplace-reference#strict-mode).

<h3 id="warning-no-commands-found-in-plugin-custom-directory">
  `Warning: No commands found in plugin <name> custom directory`
</h3>

When the plugin loads, the `claude --debug` log at `~/.claude/debug/<session-id>.txt` records `Warning: No commands found in plugin <name> custom directory: <path>. Expected .md files or SKILL.md in subdirectories.` Nothing appears in the session or the **Errors** tab.

The `commands` path in the manifest exists but holds no `.md` files and no `SKILL.md` in a subdirectory. Add the command files, or remove the path from the manifest.

## Host a marketplace

You publish a marketplace and a user reports an error, or your own validation fails. These entries are for the marketplace owner.

<h3 id="plugins-with-relative-paths-fail-in-url-based-marketplaces">
  Plugins with relative paths fail in URL-based marketplaces
</h3>

Users added your marketplace with an `https://example.com/marketplace.json` URL. Installs of plugins whose `source` is a relative path, such as `./plugins/my-plugin`, fail with `its marketplace entry path does not stay inside the marketplace directory`. Already-installed plugins fail to load with `Plugin source path refused`. Both messages have an [error reference entry](/docs/en/errors#marketplace-entry-path-does-not-stay-inside-the-marketplace-directory).

When a user adds a URL-based marketplace, Claude Code downloads only the `marketplace.json` file itself. It doesn't fetch plugin files by relative path from that server, so a relative path in an entry points at a directory that was never fetched. Give each entry a source Claude Code can fetch on its own, such as a GitHub repository:

```json theme={null}
{ "name": "my-plugin", "source": { "source": "github", "repo": "owner/repo" } }
```

Alternatively, host the marketplace in a git repository and tell users to add it with the repository URL. For a git source, Claude Code clones the whole repository, so relative paths resolve. Source types are on the [marketplace reference](/docs/en/plugins/marketplace-reference).

<h3 id="marketplace-validation-errors">
  Marketplace validation errors
</h3>

You ran `claude plugin validate .` from your marketplace directory and it reported errors or warnings on the marketplace file itself.

`claude plugin validate` also validates each entry whose `source` is a local path and warns when the entry's `version` disagrees with the plugin's own manifest.

The table lists the marketplace-level messages. Entry-level messages are the plugin messages under [`claude plugin validate` reports errors](#claude-plugin-validate-reports-errors), prefixed with `plugins[N] plugin.json →`.

| Message                                                                                                                   | Kind    | Fix                                                                                                                                 |
| :------------------------------------------------------------------------------------------------------------------------ | :------ | :---------------------------------------------------------------------------------------------------------------------------------- |
| `Duplicate plugin name "<name>" found in marketplace`                                                                     | Error   | Give each plugin a unique `name`.                                                                                                   |
| `Path contains "..": <path>` under `plugins[N].source`                                                                    | Error   | Use paths relative to the marketplace root without `..` segments.                                                                   |
| `Marketplace name cannot contain control or bidirectional-formatting characters`                                          | Error   | Remove the character from the name, such as an escape or a newline.                                                                 |
| `Plugin name cannot contain control or bidirectional-formatting characters`                                               | Error   | Remove the character from the plugin `name`.                                                                                        |
| `Marketplace has no plugins defined`                                                                                      | Warning | Add at least one entry to `plugins`.                                                                                                |
| `No marketplace description provided`                                                                                     | Warning | Add a top-level `description`.                                                                                                      |
| `Plugin name "<name>" is not kebab-case` under `plugins[N] plugin.json → name`                                            | Warning | Rename to lowercase letters, digits, and hyphens. Claude Code accepts other forms, but the claude.ai marketplace sync rejects them. |
| `Entry declares version "<a>" but <path>/plugin.json says "<b>"`                                                          | Warning | Update the entry to match `plugin.json`, which is authoritative at install time.                                                    |
| `Marketplace name "<name>" is reserved in Claude Desktop`                                                                 | Warning | Rename the marketplace. Claude Desktop's managed marketplace sync rejects `org`, `org-provisioned`, and `unknown` in any casing.    |
| `Marketplace name "<name>" is not accepted by Claude Desktop` or `Plugin name "<name>" is not accepted by Claude Desktop` | Warning | Rename to at most 128 characters of letters, digits, `.`, `_`, and `-`, starting with a letter or digit.                            |

Before v2.1.247, a marketplace name containing control or bidirectional-formatting characters was reported only as `Marketplace name impersonates an official Anthropic/Claude marketplace`.

## Blocked by your organization

Your organization deploys managed settings that restrict plugins, and a command was refused with a policy message. These entries name the setting behind each refusal so you know what to ask your administrator for. For the admin side, see [Manage plugins for your organization](/docs/en/plugins/org).

<h3 id="marketplace-source-is-blocked-by-enterprise-policy">
  `Marketplace source '<source>' is blocked by enterprise policy`
</h3>

You ran `/plugin marketplace add`, `update`, or an install, and Claude Code refused with this line. For a GitHub or git source, the host follows the source in parentheses, as in `'github:owner/repo' (github.com)`.

Your administrator set `blockedMarketplaces` or `strictKnownMarketplaces` in managed settings, and this source isn't permitted. Ask your administrator to allow the source, or add one of the allowed sources the message lists.

Match the rest of the message to see what kind of policy blocked the source:

* **`Allowed sources: <list>`**: the block comes from the `strictKnownMarketplaces` allowlist rather than the `blockedMarketplaces` blocklist
* **`No external marketplaces are allowed.`**: the `strictKnownMarketplaces` allowlist is empty
* **A `Tip:` that the shorthand assumes github.com**: the allowlist permits a git host by hostname, and the `owner/repo` shorthand you passed points at github.com. If the repository lives on your internal host, add it again with its full URL, such as `git@your-git-host.com:owner/repo.git`

A marketplace you added before the policy became more restrictive stops refreshing too, because the policy applies on every refresh.

<h3 id="marketplace-is-not-in-the-allowed-marketplace-list">
  `Marketplace "<name>" is not in the allowed marketplace list`
</h3>

The **Errors** tab shows this line, or `Marketplace "<name>" is blocked by enterprise policy`, for a marketplace you already have registered.

The same managed settings that block a [marketplace source](#marketplace-source-is-blocked-by-enterprise-policy) apply at load time. `strictKnownMarketplaces` doesn't include this marketplace, or `blockedMarketplaces` names it, so Claude Code stops loading it and its plugins. For the allowlist variant, the guidance line shows the allowed sources, or `Contact your administrator to configure allowed marketplace sources`. For the blocklist variant it reads `This marketplace source is explicitly blocked by your administrator`.

<h3 id="plugin-is-blocked-by-your-organizations-policy-and-cannot-be-installed">
  `Plugin "<name>" is blocked by your organization's policy and cannot be installed`
</h3>

An install was refused with this line, an enable with the same line ending `cannot be enabled`, or an install or update with one naming the reason: `Plugin "<name>" is from marketplace "<marketplace>", which is blocked by your organization's policy`, or `Plugin "<name>" depends on "<dep>", which is blocked by your organization's policy`.

Managed settings block this plugin, its marketplace, or a dependency it needs. Ask your administrator which entry applies. A blocked dependency means the plugin can't install until the dependency's marketplace is allowed.

<h3 id="plugin-dir-is-disabled-by-your-organizations-managed-settings-disables">
  `--plugin-dir is disabled by your organization's managed settings (disableSideloadFlags)`
</h3>

You started `claude` with `--plugin-dir`, `--plugin-url`, `--agents`, or `--mcp-config`. Claude Code exited with this message and `Plugins, custom agents, and MCP servers can only be loaded from sources your administrator has approved.`

Your administrator set `disableSideloadFlags` in managed settings, which turns off the flags that load plugins, agents, and servers from arbitrary paths. Load the plugin from an approved marketplace instead, or ask your administrator to remove the setting.

A related message in the `/plugin` **Errors** tab is `--plugin-dir copy of "<name>" ignored: plugin is locked by managed settings`. Managed settings enable or disable that plugin by name, and Claude Code ignores your `--plugin-dir` copy of it so the flag can't override the policy.

<h3 id="plugins-from-claude-skills-are-blocked-by-your-organizations-managed-s">
  `Plugins from ~/.claude/skills/ are blocked by your organization's managed settings`
</h3>

You ran `claude plugin init` or `claude plugin enable`, and it stopped with this line. The message names `strictKnownMarketplaces or blockedMarketplaces` and asks your administrator to add `{"source":"skills-dir"}` to `strictKnownMarketplaces` or remove it from `blockedMarketplaces`.

The `skills-dir` source stands for plugins Claude Code loads from your `~/.claude/skills/` directory. Ask your administrator to make the change the message names.

<h3 id="command-sourced-plugins-are-disabled-by-your-organizations-managed-set">
  `Command-sourced plugins are disabled by your organization's managed settings`
</h3>

You installed or updated a plugin with a `command` source, and it stopped with this line and `The plugin was not installed or updated and its command was not run.`

Your administrator set `disableCommandPluginSources`, so Claude Code refuses to run the marketplace-declared command that produces the plugin. Setting `allowManagedHooksOnly` alone has the same effect when `disableCommandPluginSources` is unset. Ask your administrator whether the plugin can be published from a source type the policy allows.

<h3 id="marketplace-is-seed-managed">
  `Marketplace '<name>' is seed-managed`
</h3>

You ran `claude plugin marketplace update <name>`, and it failed with `Marketplace '<name>' is seed-managed (<dir>)` and a hint to ask your admin.

An operator pre-populated this marketplace through `CLAUDE_CODE_PLUGIN_SEED_DIR`, and Claude Code treats a seed-managed marketplace as read-only. A bulk `marketplace update` skips it and updates the others.

To change the marketplace's content, ask the person who maintains the seed image to update it. For the procedure, see [Seed containers and CI](/docs/en/plugins/org#seed-containers-and-ci).

## Next steps

* [Plugin loading reference](/docs/en/plugins/loading): why scopes, the cache, and precedence behave the way they do
* [Plugin commands reference](/docs/en/plugins/cli-reference): flags, defaults, output, and exit codes for the `claude plugin` commands
* [Install and manage plugins](/docs/en/plugins/install): the install steps from the start
* [Manage plugins for your organization](/docs/en/plugins/org#troubleshoot-policy): policy-side troubleshooting for administrators
