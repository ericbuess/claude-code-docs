> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Marketplace reference

> Complete reference for marketplace.json fields, plugin entries, and the plugin and marketplace source objects, with where each is valid.

`marketplace.json` is the file that defines a plugin marketplace. It contains the marketplace's name, its owner, and one entry per plugin. Each entry's plugin source says where Claude Code fetches that plugin from.

A marketplace source is a separate object that says where Claude Code fetches the marketplace file itself. You write one in settings, or Claude Code builds one when you run `claude plugin marketplace add`.

This reference is for marketplace maintainers who need an exact field name or value, and for administrators who need to know which `source` values are valid in [`extraKnownMarketplaces`](/docs/en/settings-reference#extraknownmarketplaces), [`strictKnownMarketplaces`](/docs/en/settings-reference#strictknownmarketplaces), and [`blockedMarketplaces`](/docs/en/plugins/org#restrict-what-users-can-install).

<Note>
  These cases are covered on other pages:

  * **Building or hosting a marketplace**: see [Create a marketplace](/docs/en/plugins/create-marketplace) and [Host and maintain a marketplace](/docs/en/plugins/host-marketplace)
  * **Allowlist and blocklist recipes**: see [Manage plugins for your organization](/docs/en/plugins/org)
</Note>

Find the section for what you're writing or reading:

* **The marketplace file**: [Top-level fields](#top-level-fields) and [Plugin entries](#plugin-entries)
* **An entry's `source`**: [Plugin sources](#plugin-sources)
* **A `source` object in settings**: [Marketplace sources](#marketplace-sources)
* **Output from [`claude plugin validate <path>`](/docs/en/plugins/cli-reference)**: [Validation messages](#validation-messages), which maps each message to the field it names

## Marketplace file

Save the marketplace file at `.claude-plugin/marketplace.json` in your marketplace's directory. If you keep the file somewhere else in the repository, users have to declare the marketplace in [`extraKnownMarketplaces`](/docs/en/settings-reference#extraknownmarketplaces) with `path` set on its source, because `claude plugin marketplace add` has no option for it.

The directory that contains `.claude-plugin/` is called the marketplace root, and every relative plugin source resolves from it, not from `.claude-plugin/`.

Each user registers one marketplace per `name`, so a user can't have two marketplaces with the same name registered at once.

Claude Code ignores an unknown top-level key or plugin-entry key rather than rejecting it, so a typo loads silently. `claude plugin validate` reports each unknown key as a warning.

### Reserved names

You can't give your marketplace any of the following names:

* **Official marketplace names**: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `anthropic-agent-skills`, `life-sciences`, `knowledge-work-plugins`, `claude-for-legal`, `claude-for-financial-services`, `financial-services-plugins`, `first-party-plugins`, and `claude-tag-plugins`. Reserved unless the marketplace comes from a `github` or `git` [marketplace source](#marketplace-sources) under `github.com/anthropics/`.
* **Community marketplace names**: `claude-community`, `claude-plugins-community`, and `healthcare`. Reserved under the same rule as the official names.
* **Plugin directory names**: `anthropic-plugin-directory` and `claude-plugin-directory`. Reserved under the same rule as the official names.
* **Names that impersonate an official marketplace**: names such as `official-claude-plugins` or `claude-plugins-v2`, and any name containing a non-ASCII character. The error is `Marketplace name impersonates an official Anthropic/Claude marketplace`. A control or bidirectional-formatting character in a name also reports `Marketplace name cannot contain control or bidirectional-formatting characters`.
* <span id="reserved-name-spellings" />**Another spelling of a reserved name**: a name that differs from a reserved name only by a trailing dot, or by a symbol other than an underscore in place of a hyphen, so `claude.code.plugins` counts as `claude-code-plugins`. `claude plugin validate` accepts such a name; adding the marketplace fails with [`is another spelling of "<reserved>", a reserved marketplace name`](/docs/en/errors#marketplace-name-is-another-spelling-of-a-reserved-name), and a marketplace already registered under one stops loading. This check requires Claude Code v2.1.280 or later.
* **Names Claude Code uses for plugins that don't come from a marketplace**: `inline` for plugins loaded with [`--plugin-dir`](/docs/en/cli-reference), `builtin` for built-in plugins, `skills-dir` for plugins auto-loaded from [`.claude/skills/`](/docs/en/skills), and `synced` for plugins synced from your claude.ai account. `claude-plugin-test` is also reserved. `skills-dir` also appears as `{"source": "skills-dir"}` in `strictKnownMarketplaces` and `blockedMarketplaces`, described under [Source values valid only in policy lists](#source-values-valid-only-in-policy-lists).
* **`npm`, `pip`, `uv`, `cargo`, `github`, and `gh`**: reserved in any casing. This check requires Claude Code v2.1.275 or later.
* **Names starting with `claudeai-`**: reserved for marketplaces hosted on claude.ai. `claude plugin marketplace add` refuses any other marketplace that uses one with `Cannot add marketplace "<name>": names starting with "claudeai-" are reserved for marketplaces hosted on claude.ai`.

## Top-level fields

The table lists every key Claude Code reads from `marketplace.json`. `name`, `owner`, and `plugins` are required.

| Field                                      | Type             | Description                                                                                                                                                                                                                                                            |
| :----------------------------------------- | :--------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                                     | string           | Marketplace identifier. No spaces, control characters, or bidirectional-formatting characters, no `/` or `\`, no `..`, and not `.`. See [Reserved names](#reserved-names). Users type it after `@` when they install a plugin                                          |
| `owner`                                    | object           | Maintainer information. `name` is required; `email` and `url` are optional                                                                                                                                                                                             |
| `plugins`                                  | array            | [Plugin entries](#plugin-entries). Each entry is validated on its own, so one invalid entry doesn't fail the marketplace                                                                                                                                               |
| `$schema`                                  | string           | JSON Schema URL for editor autocomplete. Ignored at load time                                                                                                                                                                                                          |
| `description`                              | string           | Marketplace description shown to users. `claude plugin validate` warns when it's missing                                                                                                                                                                               |
| `version`                                  | string           | Marketplace manifest version                                                                                                                                                                                                                                           |
| `metadata.description`, `metadata.version` | string           | Alternate location for `description` and `version`                                                                                                                                                                                                                     |
| `metadata.pluginRoot`                      | string           | Directory that bare plugin source names resolve under. See [Relative path plugin source](#relative-path-plugin-source). Requires Claude Code v2.1.239 or later                                                                                                         |
| `forceRemoveDeletedPlugins`                | boolean          | When `true`, a plugin you remove from `plugins` is uninstalled on users' machines. See [Host and maintain a marketplace](/docs/en/plugins/host-marketplace)                                                                                                                 |
| `allowCrossMarketplaceDependenciesOn`      | array of strings | Marketplace names whose plugins may be installed as dependencies of this marketplace's plugins. When you install a plugin, only the list in that plugin's own marketplace applies, for its whole dependency chain. See [Plugin dependencies](/docs/en/plugins/dependencies) |
| `renames`                                  | object           | Map from a former plugin `name` to its current name, or to `null` for a plugin you removed. Requires Claude Code v2.1.193 or later. See [Host and maintain a marketplace](/docs/en/plugins/host-marketplace)                                                                |

## Plugin entries

Each object in the top-level `plugins` array of `marketplace.json` names a plugin and says where to fetch it. `name` and `source` are required.

An entry also accepts every [`plugin.json` field](/docs/en/plugins/manifest-reference), such as `description`, `version`, `author`, `commands`, and `hooks`. For when those fields apply, see [How an entry combines with plugin.json](#entry-and-plugin-json).

The table lists the entry's own fields and the manifest fields whose meaning changes in an entry.

| Field            | Type             | Description                                                                                                                                                                                                                                                                                                       |
| :--------------- | :--------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`           | string           | Plugin identifier, with no spaces, control characters, or bidirectional-formatting characters. Users type it before `@` when they install, even when the plugin's own `plugin.json` sets a different `name`                                                                                                       |
| `source`         | string or object | Where to fetch the plugin. See [Plugin sources](#plugin-sources)                                                                                                                                                                                                                                                  |
| `description`    | string           | Shown in [`/plugin`](/docs/en/plugins/install) listings and details                                                                                                                                                                                                                                                    |
| `version`        | string           | Version string for the plugin. When `plugin.json` also sets `version`, `plugin.json` takes precedence and `claude plugin validate` warns. See [Plugin loading reference](/docs/en/plugins/loading)                                                                                                                     |
| `category`       | string           | Free-form category for organizing the catalog                                                                                                                                                                                                                                                                     |
| `tags`           | array of strings | Free-form tags for search                                                                                                                                                                                                                                                                                         |
| `strict`         | boolean          | Default `true`. Whether `plugin.json` is the definitive source for the plugin's components. See [Strict mode](#strict-mode)                                                                                                                                                                                       |
| `relevance`      | object           | Signals that tell Claude Code when to suggest the plugin. See [Recommend plugins for your org](/docs/en/plugins/relevance)                                                                                                                                                                                             |
| `dependencies`   | array            | Plugins that must be enabled for this one to work. Each item is `"name"`, `"name@marketplace"`, or an object. See [Plugin dependencies](/docs/en/plugins/dependencies)                                                                                                                                                 |
| `defaultEnabled` | boolean          | Default `true`. Whether the plugin starts enabled when the user hasn't set it in [`enabledPlugins`](/docs/en/settings-reference#enabledplugins). The entry value takes precedence over `plugin.json`                                                                                                                   |
| `displayName`    | string           | Human-readable name shown in the UI. When neither the entry nor the plugin's `plugin.json` sets one, users see the plugin's `name`                                                                                                                                                                                |
| `metadata`       | object           | Free-form object for your own fields. Claude Code doesn't read it. Requires Claude Code v2.1.222 or later                                                                                                                                                                                                         |
| `headers`        | object           | HTTP headers Claude Code sends when it downloads this entry's [archive](#archive-plugin-source). A header set here replaces a header of the same name from the marketplace source's [`headers`](#fields-by-type). Requires Claude Code v2.1.238 or later                                                          |
| `headersHelper`  | string           | Command that prints this entry's archive-download headers as one JSON object, for a credential that expires. The entry must also set [`"strict": false`](#strict-mode). Requires Claude Code v2.1.238 or later. See [Authenticate archive downloads](/docs/en/plugins/host-marketplace#authenticate-archive-downloads) |

<h3 id="entry-and-plugin-json">
  How an entry combines with plugin.json
</h3>

The entry's fields apply differently to a fetched plugin that has its own `.claude-plugin/plugin.json` and to one that doesn't:

* **No `plugin.json`**: the entry is the manifest regardless of `strict`. Every manifest field in the entry applies, including [`mcpServers`, `lspServers`, `userConfig`, and `channels`](/docs/en/plugins/manifest-reference).
* **`plugin.json` present**: `plugin.json` is the manifest. [Strict mode](#strict-mode) decides whether the entry's six component fields, `commands`, `agents`, `skills`, `hooks`, `outputStyles`, and `themes`, are combined with it or rejected as a conflict. Entry `mcpServers`, `lspServers`, `userConfig`, and `channels` don't apply. Declare them in `plugin.json`.

#### Hooks in an entry

Write entry `hooks` as an inline object that maps hook event names to matcher arrays. If you write a file path or an array instead, `claude plugin validate` passes it. Those hooks never run, and Claude Code reports a `not yet supported in a marketplace entry` error for the plugin. Put file-based hooks in the plugin's own [`hooks/hooks.json`](/docs/en/plugins/components) or `plugin.json`.

#### Display fields

Both the entry and the plugin's own `plugin.json` can set the display fields `displayName`, `description`, `author`, `homepage`, `repository`, `license`, and `keywords`. Users see these values in plugin listings and details, before and after install:

* For a field you set on the entry, users see the entry's value, even when `plugin.json` sets a different one.
* For a field the entry leaves unset, users see the `plugin.json` value.

Before install, Claude Code can read `plugin.json` only for entries with a [relative-path source](#relative-path-plugin-source), whose plugin files are inside the marketplace itself. For an entry with any other source type, users see only the entry's own fields until they install the plugin.

### Strict mode

`strict` decides what happens when the fetched plugin has its own `plugin.json` and the entry also declares any of the [component fields](#entry-and-plugin-json): `commands`, `agents`, `skills`, `hooks`, `outputStyles`, or `themes`. With `strict: true`, the default, Claude Code appends the entry's component fields to `plugin.json`, except `hooks`, whose matchers replace the manifest's per event. With `strict: false`, an entry that declares any component field is a conflict, and the plugin fails to load. The table shows each combination of `strict`, `plugin.json`, and the entry's component fields.

| `strict`            | `plugin.json` | Entry component fields | Result                                                                                                                                                                                                                              |
| :------------------ | :------------ | :--------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| any                 | absent        | any                    | The entry is the manifest                                                                                                                                                                                                           |
| `true`, the default | present       | any                    | `plugin.json` is the authority. Claude Code appends the entry's component fields to it, except `hooks`, whose matchers [replace the manifest's per event](/docs/en/plugins/manifest-reference#how-entry-fields-combine-with-plugin-json) |
| `false`             | present       | none                   | `plugin.json` is the manifest, as with `true`                                                                                                                                                                                       |
| `false`             | present       | one or more            | Conflict. The plugin fails to load with `Plugin <name> has conflicting manifests: both plugin.json and marketplace entry specify components`                                                                                        |

## Plugin sources

A plugin entry's `source` says where Claude Code fetches that one plugin from. It's either a relative path string or an object whose own `source` key names the type, so an entry looks like `"source": { "source": "github", "repo": "your-org/formatter" }`.

The table lists each plugin source type and its fields.

| Type          | Fields                           | Notes                                                                                                                                                                                                                          |
| :------------ | :------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Relative path | the string itself                | A directory inside the marketplace, resolved from the marketplace root. Must start with `./`, unless you write a [bare name under `metadata.pluginRoot`](#relative-path-plugin-source). `"."` on its own means the root itself |
| `github`      | `repo`, `ref`, `sha`             | GitHub repository in `owner/repo` form                                                                                                                                                                                         |
| `url`         | `url`, `ref`, `sha`              | Any git repository by URL                                                                                                                                                                                                      |
| `git-subdir`  | `url`, `path`, `ref`, `sha`      | One subdirectory of a git repository, fetched with a sparse partial clone                                                                                                                                                      |
| `npm`         | `package`, `version`, `registry` | npm package, fetched with your npm client and unpacked without running install scripts                                                                                                                                         |
| `archive`     | `url`, `sha256`                  | Zip archive over HTTPS. Requires Claude Code v2.1.224 or later                                                                                                                                                                 |
| `command`     | `command`, `timeout`, `mode`     | Directory printed by a command Claude Code runs on the user's machine. Requires Claude Code v2.1.229 or later                                                                                                                  |

The names `url` and `github` are also [marketplace source](#marketplace-sources) types, where `url` means a direct link to a `marketplace.json` file rather than a git repository. `git` exists only as a marketplace source, and `npm` exists as both. `git-subdir`, `archive`, and `command` exist only as plugin sources.

Use a relative path for a plugin in a subdirectory of the marketplace repository itself. Use `git-subdir` for a subdirectory of some other repository.

`github`, `url`, and `git-subdir` sources share the `ref` and `sha` fields:

* **`ref`**: a branch or tag. Defaults to the repository's default branch.
* **`sha`**: a full 40-character lowercase commit SHA. When you set both `ref` and `sha`, Claude Code checks out `sha`. On most git hosts, including GitHub, GitLab, and Bitbucket, this means installation succeeds even if the branch or tag named by `ref` has since been deleted upstream, as long as the commit is still reachable from the repository. Some servers, such as AWS CodeCommit, don't support fetching commits by SHA. On those servers the `ref` must still exist and the pinned commit must be reachable from it.

For how each type is fetched, cached, and versioned, see [Plugin loading reference](/docs/en/plugins/loading).

### Relative path plugin source

The path resolves from the marketplace root. `./plugins/formatter` is `<root>/plugins/formatter` even though the marketplace file is in `<root>/.claude-plugin/`.

A path containing `..` fails validation. On macOS and Linux, Claude Code refuses an entry path that contains a backslash anywhere after the leading `./`, so write the path with forward slashes.

```json theme={null}
{ "name": "formatter", "source": "./plugins/formatter" }
```

A relative path resolves only when Claude Code has the marketplace's files, so check the [marketplace source](#marketplace-sources) type:

* **`github`, `git`, `file`, and `directory`**: Claude Code has the marketplace's files.
* **`url`**: Claude Code fetches only `marketplace.json`, so relative paths can't resolve. Give each plugin an object source instead, such as `github` or `git-subdir`.
* **`settings`**: relative paths are rejected outright.

#### Bare names under pluginRoot

A bare name is a single directory name with no `/`, such as `"formatter"`. To write bare names instead of `./` paths, set [`metadata.pluginRoot`](#top-level-fields) to the directory they resolve under. With `"pluginRoot": "./plugins"`, `"source": "formatter"` resolves to `./plugins/formatter`. Requires Claude Code v2.1.239 or later.

`metadata.pluginRoot` has these limits:

* It must itself be a relative path inside the marketplace.
* It has no effect on a source that already starts with `./`.
* A source that contains a `/`, such as `team-a/formatter`, isn't a bare name and still needs the `./` prefix, even when `metadata.pluginRoot` is set.

### github plugin source

`repo` takes `owner/repo`. `ref` and `sha` are optional.

```json theme={null}
{
  "name": "formatter",
  "source": {
    "source": "github",
    "repo": "your-org/formatter",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

### url plugin source

`url` is a full git URL: `https://`, `http://`, `file://`, or `git@`. A `.git` suffix isn't required, so Azure DevOps and AWS CodeCommit URLs work as written. This type doesn't take `owner/repo` shorthand.

```json theme={null}
{
  "name": "formatter",
  "source": {
    "source": "url",
    "url": "https://gitlab.example.com/your-group/formatter.git",
    "ref": "main"
  }
}
```

### git-subdir plugin source

`url` accepts a full git URL or GitHub `owner/repo` shorthand. `path` is the subdirectory that holds the plugin, and Claude Code downloads only that subdirectory.

```json theme={null}
{
  "name": "formatter",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/your-org/monorepo.git",
    "path": "tools/formatter"
  }
}
```

### npm plugin source

An `npm` source takes these fields:

* `package`: a package name, or a scoped name such as `@your-org/formatter`
* `version`: a version or range
* `registry`: a registry URL for a package that isn't on the default registry

Claude Code fetches the package with your npm client. The package's install scripts, such as `preinstall` or `postinstall`, never run, and its dependencies aren't installed during the fetch. If the package has a supported lockfile beside its `package.json`, Claude Code installs those [Node.js package dependencies](/docs/en/plugins/loading#node-js-package-dependencies) in a separate step, also with scripts disabled.

```json theme={null}
{
  "name": "formatter",
  "source": {
    "source": "npm",
    "package": "@your-org/formatter",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

### archive plugin source

`url` must use `https://` and can't point at a loopback, link-local, or cloud-metadata host.

The plugin root may be at the top of the zip or one directory down.

`sha256` is the archive's digest as 64 hex characters, uppercase or lowercase. When you set it, Claude Code refuses a download that doesn't match.

```json theme={null}
{
  "name": "formatter",
  "source": {
    "source": "archive",
    "url": "https://artifacts.example.com/formatter-2.0.0.zip",
    "sha256": "6bfa50e3d2e00c052b46abe51fff89346ac803e45771f76dcf6df1ab74cca5e1"
  }
}
```

### command plugin source

Use a `command` source when a tool installed on the user's machine produces the plugin directory, such as an IDE that renders its plugin for the toolchain the user has selected. Claude Code runs the command when the user installs or updates the plugin, and [again once per session](/docs/en/plugins/loading#when-a-command-source-re-runs), so users get the tool's changed output without reinstalling.

A `command` source takes these fields:

* `command`: a shell command that prints the plugin directory's absolute path as one line and exits 0. Claude Code shows users the whole string for review before it runs. Write it as printable ASCII, at most 500 characters, with no run of four or more spaces.
* `timeout`: a whole number of seconds from 1 to 600. Defaults to 60.
* `mode`: `copy`, the default, or `link`. See [Copy mode and link mode](#copy-mode-and-link-mode).

```json theme={null}
{
  "name": "formatter",
  "source": {
    "source": "command",
    "command": "my-tool claude-plugin-path",
    "timeout": 120
  }
}
```

For how users accept the command, see [Install from your shell](/docs/en/plugins/install#install-from-your-shell). For what users see after you change it, see [Change the command of a command source](/docs/en/plugins/host-marketplace#change-the-command-of-a-command-source). Administrators turn command sources off with [`disableCommandPluginSources`](/docs/en/settings-reference#disablecommandpluginsources).

#### What the command must do

Write the command to meet these requirements:

* **Shell and working directory**: Claude Code runs the command through `sh`, or through `cmd.exe` on Windows, from the user's home directory. Give an absolute path or a command on `PATH`.
* **Output**: print exactly one line on stdout, the absolute path of the plugin directory, and exit 0 within `timeout` seconds.
* **Directory contents**: the directory holds the complete plugin by the time the command exits. The path can differ from one run to the next.

#### Output that fails the install or update

The install or update fails when the command exits non-zero, runs longer than `timeout`, or prints anything other than one absolute path. It also fails when the printed directory is one of these:

* **No plugin content**: the printed directory has no plugin content at its top level, such as a `.claude-plugin/` directory or a `skills/`, `commands/`, `agents/`, or `hooks/` directory.
* **The session's own directory**: the printed directory is the one Claude Code was started in, or one of its parents.
* **A network path**: on Windows, the printed path is a UNC path.
* **Too large to copy**: in copy mode, the directory is larger than 256 MiB or has more than 20,000 entries.

#### Copy mode and link mode

`mode` decides whether Claude Code copies the printed directory or uses it in place:

* **`copy`**: Claude Code copies the directory into the plugin cache and derives the [plugin version](/docs/en/plugins/loading#how-claude-code-computes-the-version) from a hash of the copied files. Your tool can delete or rewrite the directory after the command exits. A re-run that produces identical files counts as up to date.
* **`link`**: Claude Code fills the plugin's cache entry with a link to each top-level entry of the printed directory and loads the files in place. Nothing is copied, file contents aren't hashed, and the size limits don't apply. Use it for a directory too large to copy, such as a rendered SDK export.

A link-mode plugin has these requirements:

* **Keep the directory in place**: Claude Code loads the plugin through the links at every startup, so the printed directory must stay where it is for as long as the plugin stays installed.
* **Print a different path to signal new content**: the version comes from the printed directory's real path and its top-level entries, not from the files inside them.
* **Keep top-level symlinks inside the directory**: the install fails if a top-level entry is a symlink that points outside the printed directory.
* **Include `node_modules`**: Claude Code skips the [Node.js package dependency install](/docs/en/plugins/loading#node-js-package-dependencies) for a link-mode plugin, so print a directory that already contains the packages the plugin needs.
* **Sessions started inside the directory**: a session started in the printed directory or anywhere below it doesn't load the plugin.
* **Not on Windows**: Claude Code refuses to install a link-mode plugin on Windows. Declare `"mode": "copy"` there.

## Marketplace sources

A marketplace source says where Claude Code fetches a `marketplace.json` from. The CLI builds one for you when you add a marketplace, and you write one yourself in settings:

* **[`claude plugin marketplace add`](/docs/en/plugins/cli-reference)**: Claude Code builds the source from the string you pass.
* **[`extraKnownMarketplaces`](/docs/en/settings-reference#extraknownmarketplaces)**: you write the source yourself as the `source` object.
* **[`strictKnownMarketplaces`](/docs/en/settings-reference#strictknownmarketplaces) and [`blockedMarketplaces`](/docs/en/plugins/org#restrict-what-users-can-install)**: administrators write sources in these two policy lists. `strictKnownMarketplaces` is the allowlist and `blockedMarketplaces` is the blocklist.

The type names `url`, `git`, and `github` mean something different in a marketplace source than in a [plugin source](#plugin-sources):

| Type name | As a marketplace source                                                                       | As a plugin source                                                       |
| :-------- | :-------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------- |
| `url`     | A direct link to a `marketplace.json` file, with fields `url`, `headers`, and `headersHelper` | A git repository to clone, with fields `url`, `ref`, and `sha`           |
| `git`     | A git repository to clone, with fields `url`, `ref`, `path`, and `sparsePaths`                | Doesn't exist                                                            |
| `github`  | A GitHub repository, with fields `repo`, `ref`, `path`, and `sparsePaths`                     | A GitHub repository, with fields `repo`, `ref`, and `sha`, and no `path` |

The table lists every marketplace source type with its fields, the `claude plugin marketplace add` input that produces it, and what it does in each of the three settings keys.

| Type          | Fields                               | `marketplace add` input                                                                                                                                | `extraKnownMarketplaces`                                     | `strictKnownMarketplaces`                                                                                                                                                                                            | `blockedMarketplaces`                                                  |
| :------------ | :----------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `url`         | `url`, `headers`, `headersHelper`    | An `http://` or `https://` URL that doesn't match a git form                                                                                           | Loads                                                        | Allows the same URL                                                                                                                                                                                                  | Blocks the same URL                                                    |
| `github`      | `repo`, `ref`, `path`, `sparsePaths` | `owner/repo`, `owner/repo@ref`, or `owner/repo#ref`                                                                                                    | Loads                                                        | Allows the same `repo`, `ref`, and `path`. `repo` may be `owner/*`                                                                                                                                                   | Blocks the same, and a `git` URL to the same repository                |
| `git`         | `url`, `ref`, `path`, `sparsePaths`  | A `user@host:path` URL, or an `https://` URL that ends in `.git`, contains `/_git/`, or names a github.com or gitlab.com repository. `#ref` pins a ref | Loads                                                        | Allows the same URL, `ref`, and `path`                                                                                                                                                                               | Blocks the same, and other spellings of the same github.com repository |
| `npm`         | `package`                            | Not produced                                                                                                                                           | Fails to load: `NPM marketplace sources not yet implemented` | Parses but matches nothing, because nothing registers an `npm` marketplace                                                                                                                                           | Parses but matches nothing                                             |
| `file`        | `path`                               | A path to a `.json` file                                                                                                                               | Loads                                                        | Allows the same path                                                                                                                                                                                                 | Blocks the same path                                                   |
| `directory`   | `path`                               | A path to a directory                                                                                                                                  | Loads                                                        | Allows the same path                                                                                                                                                                                                 | Blocks the same path                                                   |
| `settings`    | `name`, `plugins`, `owner`           | Not produced                                                                                                                                           | Loads                                                        | Allows an entry with the same `name` and identical `plugins`                                                                                                                                                         | Blocks the same `name`                                                 |
| `skills-dir`  | none                                 | Not produced                                                                                                                                           | Fails to load: `Unsupported marketplace source type`         | Keeps [skills-directory plugins](/docs/en/plugins/org#keep-skills-directory-plugins-loading) loading while an allowlist is set. See [Source values valid only in policy lists](#source-values-valid-only-in-policy-lists) | Stops skills-directory plugins from loading                            |
| `hostPattern` | `hostPattern`                        | Not produced                                                                                                                                           | Fails to load: `Unsupported marketplace source type`         | Allows `github`, `git`, and `url` sources whose host matches                                                                                                                                                         | Blocks those sources                                                   |
| `pathPattern` | `pathPattern`                        | Not produced                                                                                                                                           | Fails to load: `Unsupported marketplace source type`         | Allows `file` and `directory` sources whose `path` matches                                                                                                                                                           | Blocks those sources                                                   |

### Fields by type

The table lists each marketplace source field that has a default, a constraint, or a meaning specific to its type.

| Field           | Types           | Description                                                                                                                                                                                                                                               |
| :-------------- | :-------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`           | `url`           | Link to the `marketplace.json` file. Claude Code downloads only that file, so the marketplace's plugins can't use [relative-path sources](#relative-path-plugin-source)                                                                                   |
| `url`           | `git`           | The git repository to clone                                                                                                                                                                                                                               |
| `headers`       | `url`           | Map of HTTP headers Claude Code sends with the fetch, for authenticated hosts                                                                                                                                                                             |
| `headersHelper` | `url`           | Command that prints headers whose values are too short-lived to list in `headers`. Requires Claude Code v2.1.238 or later. See [Authenticate archive downloads](/docs/en/plugins/host-marketplace#authenticate-archive-downloads)                              |
| `repo`          | `github`        | In `marketplace add` and `extraKnownMarketplaces`, `repo` must name one repository. `marketplace add` rejects `owner/*` as not a valid `owner/repo` shorthand; in `extraKnownMarketplaces` Claude Code takes it literally and the clone fails             |
| `ref`           | `github`, `git` | Branch or tag. Defaults to the repository's default branch                                                                                                                                                                                                |
| `path`          | `github`, `git` | The marketplace file's path inside the repository. Defaults to `.claude-plugin/marketplace.json`                                                                                                                                                          |
| `path`          | `file`          | The marketplace file itself. Claude Code reads it in place and takes the directory two levels up as the marketplace root, so keep the file at `<root>/.claude-plugin/marketplace.json`                                                                    |
| `path`          | `directory`     | The marketplace root, the directory that contains `.claude-plugin/marketplace.json`                                                                                                                                                                       |
| `sparsePaths`   | `github`, `git` | Array of directories for a sparse checkout, such as `[".claude-plugin", "plugins"]`. `claude plugin marketplace add --sparse` sets it                                                                                                                     |
| `skipLfs`       | `github`, `git` | Accepted and has no effect. See [Keep plugin files out of Git LFS](/docs/en/plugins/host-marketplace#keep-plugin-files-out-of-git-lfs)                                                                                                                         |
| `name`          | `settings`      | Must equal the `extraKnownMarketplaces` key and can't be a [reserved name](#reserved-names)                                                                                                                                                               |
| `plugins`       | `settings`      | The inline catalog, with no hosted file. Each item takes `name`, `source`, `description`, `version`, `strict`, `headers`, and `headersHelper`. Write each item's `source` as an object type, because a relative path has no repository to resolve against |

### Source values valid only in policy lists

`hostPattern`, `pathPattern`, `skills-dir`, and the `owner/*` form of `repo` are valid only in the two policy lists, `strictKnownMarketplaces` and `blockedMarketplaces`:

* **`hostPattern` and `pathPattern`**: regular expressions Claude Code tests against a source before it fetches from it.
* **`skills-dir`**: not a source. If you set `strictKnownMarketplaces` at all, [skills-directory plugins](/docs/en/plugins/org#keep-skills-directory-plugins-loading) stop loading until you add `{"source": "skills-dir"}` to that list.
* **`owner/*`**: as a `github` `repo` value, matches every repository under exactly that GitHub owner. Requires Claude Code v2.1.223 or later.

For match order, exact-`ref` semantics, and recipes, see [Manage plugins for your organization](/docs/en/plugins/org).

### Source objects in settings

An `extraKnownMarketplaces` value is a map from marketplace name to an object with `source`. This entry registers a marketplace from a git repository at its `main` branch:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "your-marketplace": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/your-org/your-marketplace.git",
        "ref": "main"
      }
    }
  }
}
```

`strictKnownMarketplaces` and `blockedMarketplaces` are arrays of source objects. This allowlist admits one GitHub owner and one internal host:

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "your-org/*" },
    { "source": "hostPattern", "hostPattern": "^git\\.example\\.com$" }
  ]
}
```

## Validation messages

`claude plugin validate <path>` takes the marketplace root or the marketplace file itself. It prints errors and warnings. For exit codes and `--strict`, see [plugin validate](/docs/en/plugins/cli-reference#plugin-validate).

A message names a plugin entry by its index, written as `plugins.1.source` or `plugins[1].source`.

A message prefixed with an entry index and `plugin.json →`, such as `plugins[2] plugin.json →`, is about that plugin's own files. [`claude plugin validate` reports errors](/docs/en/plugins/troubleshooting#claude-plugin-validate-reports-errors) lists those messages with their fixes.

Warnings that mention Claude Desktop flag names that Claude Code accepts but Claude Desktop rejects, because Claude Desktop's name rules are stricter.

The table maps marketplace-level messages to the field each is about.

| Message                                                                                                                                                                                             | Level   | Field                                                                                                                |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------- |
| `Marketplace must have a name`                                                                                                                                                                      | Error   | `name` is empty                                                                                                      |
| `Marketplace name cannot contain spaces. Use kebab-case (e.g., "my-marketplace")`                                                                                                                   | Error   | `name`                                                                                                               |
| `Marketplace name cannot contain path separators (/ or \), ".." sequences, or be "."`                                                                                                               | Error   | `name`                                                                                                               |
| `Marketplace name impersonates an official Anthropic/Claude marketplace`                                                                                                                            | Error   | `name`. See [Reserved names](#reserved-names)                                                                        |
| `Marketplace name cannot contain control or bidirectional-formatting characters`                                                                                                                    | Error   | `name` contains a control character, such as an escape or a newline, or a Unicode bidirectional-formatting character |
| `Marketplace name "inline" is reserved for --plugin-dir session plugins`, and the `builtin`, `skills-dir`, `synced`, `claude-plugin-test`, `npm`, `pip`, `uv`, `cargo`, `github`, and `gh` variants | Error   | `name`                                                                                                               |
| `Author name cannot be empty`                                                                                                                                                                       | Error   | `owner.name`                                                                                                         |
| `Plugin name cannot contain spaces. Use kebab-case (e.g., "my-plugin")`                                                                                                                             | Error   | `plugins[i].name`                                                                                                    |
| `Plugin name cannot contain control or bidirectional-formatting characters`                                                                                                                         | Error   | `plugins[i].name`                                                                                                    |
| `Duplicate plugin name "x" found in marketplace`                                                                                                                                                    | Error   | Two entries share a `name`                                                                                           |
| `plugins.i.source: Invalid input`                                                                                                                                                                   | Error   | The entry's `source` matches no type. See [Invalid input on a source](#invalid-input-on-a-source)                    |
| `plugins[i].source: Path contains "..": <path>`                                                                                                                                                     | Error   | A relative `source` that escapes the marketplace root                                                                |
| `source.source: 'unsupported' is a parse-time placeholder and cannot be authored`                                                                                                                   | Error   | `plugins[i].source`                                                                                                  |
| `Plugin "x" sets headersHelper but is not "strict": false`                                                                                                                                          | Error   | `plugins[i].headersHelper`, on an `archive` entry                                                                    |
| `chain does not resolve (<reason>) — target must be a name in plugins[], a key in renames, or null`                                                                                                 | Error   | `renames.<old>`                                                                                                      |
| `target "x" is not a valid plugin name (PluginIdSchema)`                                                                                                                                            | Error   | `renames.<old>`                                                                                                      |
| `Unknown field 'x'. Claude Code ignores it at load time.`                                                                                                                                           | Warning | The named key at the top level, under `metadata`, in an entry, or under an entry's `relevance`                       |
| `Marketplace has no plugins defined`                                                                                                                                                                | Warning | `plugins` is empty                                                                                                   |
| `Plugin "x" sets headers/headersHelper, which only apply to "archive" sources; they have no effect on this entry.`                                                                                  | Warning | `plugins[i].headers` or `plugins[i].headersHelper`, on an entry whose `source` isn't `archive`                       |
| `Plugin "x" fetches its archive with a headersHelper but sets no sha256 pin`                                                                                                                        | Warning | `plugins[i].source.sha256`                                                                                           |
| `Header "x" is a request-routing/identity header that catalog entries may not set; Claude Code drops it at download time.`                                                                          | Warning | `plugins[i].headers.<name>`                                                                                          |
| `Local source "x" is or traverses a symlink, so <path> was not read`                                                                                                                                | Warning | `plugins[i].source`                                                                                                  |
| `No marketplace description provided. Adding a description helps users understand what this marketplace offers`                                                                                     | Warning | `description`                                                                                                        |
| `Entry declares version "x" but <path>/plugin.json says "y". At install time, plugin.json wins`                                                                                                     | Warning | `plugins[i].version`, on a relative-path entry                                                                       |
| `'relevance' must be an object containing topic and signals; got <type>. It will be ignored at load time.`                                                                                          | Warning | `plugins[i].relevance`                                                                                               |
| `'metadata' must be a free-form object; got <type>. It will be ignored at load time.`                                                                                                               | Warning | `plugins[i].metadata`                                                                                                |
| `'experimental' must be an object containing component declarations; got <type>. It will be ignored at load time.`                                                                                  | Warning | `plugins[i].experimental`                                                                                            |
| `Marketplace name "x" is reserved in Claude Desktop`                                                                                                                                                | Warning | `name` is `org`, `org-provisioned`, or `unknown`. Claude Desktop rejects the marketplace                             |
| `Marketplace name "x" is not accepted by Claude Desktop (letters, digits, ".", "_", "-"; must start alphanumeric; max 128 chars)`                                                                   | Warning | `name`. Claude Desktop rejects the marketplace                                                                       |
| `Plugin name "x" is not accepted by Claude Desktop (letters, digits, ".", "_", "-"; must start alphanumeric; max 128 chars)`                                                                        | Warning | `plugins[i].name`. Claude Desktop drops the entry                                                                    |

### Invalid input on a source

`Invalid input` on a `source` means the object matched no source type. Check for these causes:

* A relative path that doesn't start with `./`, other than `"."` or a [bare name under `metadata.pluginRoot`](#relative-path-plugin-source)
* An `npm` `package` containing `..`
* A `source` type that isn't one of the [plugin sources](#plugin-sources)
* A known type with a required field missing or of the wrong type, such as `github` without `repo`

### Failures that validation doesn't catch

`claude plugin validate` doesn't report every failure. An entry `hooks` written as a file path or array passes validation, and the error appears only when the plugin loads, as [Hooks in an entry](#hooks-in-an-entry) describes. Errors fetching a `source` also appear only after install, not in validation.

[`claude plugin list`](/docs/en/plugins/cli-reference) shows a plugin that failed to load with its error, and [Troubleshoot plugins](/docs/en/plugins/troubleshooting) covers the load-time strings.

## Next steps

* [Create a marketplace](/docs/en/plugins/create-marketplace): build a marketplace from these fields and install from it locally
* [Host and maintain a marketplace](/docs/en/plugins/host-marketplace): where to put the file and how users receive changes
* [Plugin manifest reference](/docs/en/plugins/manifest-reference): the `plugin.json` fields an entry can override
* [Manage plugins for your organization](/docs/en/plugins/org): allowlist and blocklist recipes that use these source values
