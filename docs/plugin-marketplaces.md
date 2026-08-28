> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Create and distribute a plugin marketplace

> Build and host plugin marketplaces to distribute Claude Code extensions across teams and communities.

A **plugin marketplace** is a catalog that lets you distribute plugins to others. Marketplaces provide centralized discovery, version tracking, automatic updates, and support for multiple source types, including git repositories and local paths. This guide shows you how to create your own marketplace to share plugins with your team or community.

Looking to install plugins from an existing marketplace? See [Discover and install prebuilt plugins](/docs/en/discover-plugins).

## Overview

Creating and distributing a marketplace involves:

1. **Create plugins**: build one or more plugins with skills, agents, hooks, MCP servers, or LSP servers. This guide assumes you already have plugins to distribute; see [Create plugins](/docs/en/plugins) for details on how to create them.
2. **Create the marketplace file**: define a `marketplace.json` that lists your plugins and where to find them. See [Create the marketplace file](#create-the-marketplace-file).
3. **Host the marketplace**: push to GitHub, GitLab, or another git host. See [Host and distribute marketplaces](#host-and-distribute-marketplaces).
4. **Share with users**: users add your marketplace with `/plugin marketplace add` and install individual plugins. See [Discover and install plugins](/docs/en/discover-plugins).

Once your marketplace is live, you can update it by pushing changes to your repository. Users refresh their local copy with `/plugin marketplace update`.

## Walkthrough: create a local marketplace

This example creates a marketplace with one plugin: a `quality-review` skill for code reviews. You'll create the directory structure, add a skill, create the plugin manifest and marketplace catalog, then install and test it.

<Steps>
  <Step title="Create the directory structure">
    ```bash theme={null}
    mkdir -p my-marketplace/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/skills/quality-review
    ```
  </Step>

  <Step title="Create the skill">
    Create a `SKILL.md` file that defines what the `quality-review` skill does.

    ```markdown my-marketplace/plugins/quality-review-plugin/skills/quality-review/SKILL.md theme={null}
    ---
    description: Review code for bugs, security, and performance
    ---

    Review the code I've selected or the recent changes for:
    - Potential bugs or edge cases
    - Security concerns
    - Performance issues
    - Readability improvements

    Be concise and actionable.
    ```
  </Step>

  <Step title="Create the plugin manifest">
    Create a `plugin.json` file that describes the plugin. The manifest goes in the `.claude-plugin/` directory.

    ```json my-marketplace/plugins/quality-review-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "quality-review-plugin",
      "description": "Adds a quality-review skill for quick code reviews",
      "version": "1.0.0",
      "author": {
        "name": "Your Name"
      }
    }
    ```

    <Note>
      Setting `version` means users only receive updates when you change this field, so bump it on every release. A plugin with a [`command` source](#command-sources) isn't pinned by this field. If you omit `version`, the version comes from the next source in [version management](/docs/en/plugins-reference#version-management).
    </Note>
  </Step>

  <Step title="Create the marketplace file">
    Create the marketplace catalog that lists your plugin.

    ```json my-marketplace/.claude-plugin/marketplace.json theme={null}
    {
      "name": "my-plugins",
      "owner": {
        "name": "Your Name"
      },
      "plugins": [
        {
          "name": "quality-review-plugin",
          "source": "./plugins/quality-review-plugin",
          "description": "Adds a quality-review skill for quick code reviews"
        }
      ]
    }
    ```
  </Step>

  <Step title="Add and install">
    From the directory that contains `my-marketplace`, start Claude Code and run the following commands. The install command opens a plugin details view where you select an installation scope to confirm the install. Check the install summary: if it reports `Run /reload-plugins to activate.`, run that command.

    ```shell theme={null}
    /plugin marketplace add ./my-marketplace
    /plugin install quality-review-plugin@my-plugins
    ```
  </Step>

  <Step title="Try it out">
    Select some code in your editor and run your new skill. Plugin skills are namespaced with the plugin name.

    ```shell theme={null}
    /quality-review-plugin:quality-review
    ```
  </Step>
</Steps>

To learn more about what plugins can do, including hooks, agents, MCP servers, and LSP servers, see [Plugins](/docs/en/plugins).

<Note>
  **How plugins are installed**: when users install a plugin, Claude Code copies the plugin directory to a cache location, except for a [`command` source in link mode](#copy-mode-and-link-mode), which is used in place. Copied plugins can't reference files outside their directory using paths like `../shared-utils`, because those files won't be copied.

  If you need to share files across plugins, use symlinks. See [Plugin caching and file resolution](/docs/en/plugins-reference#plugin-caching-and-file-resolution) for details.
</Note>

## Create the marketplace file

Create `.claude-plugin/marketplace.json` in your repository root. This file defines your marketplace's name, owner information, and a list of plugins with their sources.

Each plugin entry needs at minimum a `name` and a `source` that tells Claude Code where to fetch it from. See the [full schema](#marketplace-schema) below for all available fields.

```json theme={null}
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting on save",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      }
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Deployment automation tools"
    }
  ]
}
```

## Marketplace schema

### Required fields

| Field     | Type   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Example        |
| :-------- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------- |
| `name`    | string | Marketplace identifier in kebab-case, with no spaces, control characters, or bidirectional-formatting characters. This is public-facing: users see it when installing plugins (for example, `/plugin install my-tool@your-marketplace`). Each user can register only one marketplace per name: when they add a second marketplace with the same name, Claude Code replaces the first. To publish multiple plugins under one marketplace name, list them all in a [single `marketplace.json`](#create-the-marketplace-file). | `"acme-tools"` |
| `owner`   | object | Marketplace maintainer information ([see fields below](#owner-fields))                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                |
| `plugins` | array  | List of available plugins                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | See below      |

<Note>
  **Reserved names**: the following marketplace names are reserved for official Anthropic use and can't be used by third-party marketplaces: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `claude-plugins-community`, `claude-community`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `anthropic-agent-skills`, `knowledge-work-plugins`, `life-sciences`, `claude-for-legal`, `claude-for-financial-services`, `financial-services-plugins`, `first-party-plugins`, `healthcare`. Names that impersonate official marketplaces, such as `official-claude-plugins` or `anthropic-plugins-v2`, are also blocked. Reserving these names prevents a third-party marketplace from presenting itself as an Anthropic-published source.

  Claude Code re-checks reserved names every time it loads a marketplace, not only when you add one. A marketplace that was registered under one of these names before the name became reserved stops loading and reports that it is [registered from an untrusted source](/docs/en/errors#marketplace-is-registered-from-an-untrusted-source). Remove that marketplace and re-add it from the official Anthropic source. A third-party marketplace affected by a newly reserved name loads again as soon as you re-add it under a different name. Before v2.1.205, `first-party-plugins` and `healthcare` weren't reserved, and a marketplace already registered under a reserved name kept loading.
</Note>

### Owner fields

| Field   | Type   | Required | Description                                  |
| :------ | :----- | :------- | :------------------------------------------- |
| `name`  | string | Yes      | Name of the maintainer or team               |
| `email` | string | No       | Contact email for the maintainer             |
| `url`   | string | No       | Website, GitHub profile, or organization URL |

### Optional fields

| Field                                 | Type   | Description                                                                                                                                                                                                                                                                                  |
| :------------------------------------ | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$schema`                             | string | JSON Schema URL for editor autocomplete and validation. Claude Code ignores this field at load time.                                                                                                                                                                                         |
| `description`                         | string | Brief marketplace description                                                                                                                                                                                                                                                                |
| `version`                             | string | Marketplace manifest version                                                                                                                                                                                                                                                                 |
| `metadata.pluginRoot`                 | string | Directory that Claude Code resolves bare plugin source names under. See [Relative paths](#relative-paths). Requires Claude Code v2.1.239 or later.                                                                                                                                           |
| `allowCrossMarketplaceDependenciesOn` | array  | Other marketplaces that plugins in this marketplace may depend on. Dependencies from a marketplace not listed here are blocked at install. See [Depend on a plugin from another marketplace](/docs/en/plugin-dependencies#depend-on-a-plugin-from-another-marketplace).                           |
| `renames`                             | object | Map from a former plugin `name` to its current name, or to `null` if the plugin was removed. Lets existing users migrate automatically when you rename or remove an entry in `plugins`. See [Rename or remove a plugin](#rename-or-remove-a-plugin). Requires Claude Code v2.1.193 or later. |

`description` and `version` are also accepted under `metadata` for backward compatibility.

## Plugin entries

Each plugin entry in the `plugins` array describes a plugin and where to find it. You can include any field from the [plugin manifest schema](/docs/en/plugins-reference#plugin-manifest-schema), such as `description`, `version`, `author`, `commands`, and `hooks`, plus these marketplace-specific fields: `source`, `category`, `tags`, `strict`, `relevance`, `headers`, and `headersHelper`.

### Required fields

| Field    | Type           | Description                                                                                                                                                                                                              |
| :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`   | string         | Plugin identifier in kebab-case, with no spaces, control characters, or bidirectional-formatting characters. This is public-facing: users see it when installing (for example, `/plugin install my-plugin@marketplace`). |
| `source` | string\|object | Where to fetch the plugin from (see [Plugin sources](#plugin-sources) below)                                                                                                                                             |

### Optional plugin fields

**Standard metadata fields:**

| Field            | Type    | Description                                                                                                                                                                                                                                                                                                                                                  |
| :--------------- | :------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `displayName`    | string  | Human-readable name shown in UI surfaces. Falls back to `name` when omitted. May contain spaces and any casing. Not used for namespacing or lookup.                                                                                                                                                                                                          |
| `description`    | string  | Brief plugin description                                                                                                                                                                                                                                                                                                                                     |
| `version`        | string  | Plugin version. If set (here or in `plugin.json`), the plugin is pinned to this string and users only receive updates when it changes. A plugin with a [`command` source](#command-sources) isn't pinned by either field. If set in neither place, the version comes from the next source in [version management](/docs/en/plugins-reference#version-management). |
| `author`         | object  | Plugin author information (`name` required; `email` and `url` optional)                                                                                                                                                                                                                                                                                      |
| `homepage`       | string  | Plugin homepage or documentation URL                                                                                                                                                                                                                                                                                                                         |
| `repository`     | string  | Source code repository URL                                                                                                                                                                                                                                                                                                                                   |
| `license`        | string  | SPDX license identifier (for example, MIT, Apache-2.0)                                                                                                                                                                                                                                                                                                       |
| `keywords`       | array   | Tags for plugin discovery and categorization                                                                                                                                                                                                                                                                                                                 |
| `metadata`       | object  | Free-form object for your own fields, such as entitlement or catalog data. Claude Code doesn't read it. Before v2.1.222, `claude plugin validate` reported the key as an unrecognized field.                                                                                                                                                                 |
| `category`       | string  | Plugin category for organization                                                                                                                                                                                                                                                                                                                             |
| `tags`           | array   | Tags for searchability                                                                                                                                                                                                                                                                                                                                       |
| `strict`         | boolean | Controls whether `plugin.json` is the authority for component definitions (default: true). See [Strict mode](#strict-mode) below.                                                                                                                                                                                                                            |
| `relevance`      | object  | Signals that tell Claude Code when to suggest this plugin to users. Takes effect only for marketplaces an administrator allowlists in managed settings. See [Recommend plugins for your org](/docs/en/plugin-relevance).                                                                                                                                          |
| `defaultEnabled` | boolean | Whether the plugin is enabled after install (default: true). Set to `false` to install the plugin disabled until the user opts in. Takes precedence over the same field in the plugin's `plugin.json`. See [Default enablement](/docs/en/plugins-reference#default-enablement). Requires Claude Code v2.1.154 or later.                                           |

**Component configuration fields:**

| Field        | Type           | Description                                                    |
| :----------- | :------------- | :------------------------------------------------------------- |
| `skills`     | string\|array  | Custom paths to skill directories containing `<name>/SKILL.md` |
| `commands`   | string\|array  | Custom paths to flat `.md` skill files or directories          |
| `agents`     | string\|array  | Custom paths to agent files                                    |
| `hooks`      | string\|object | Custom hooks configuration or path to hooks file               |
| `mcpServers` | string\|object | MCP server configurations or path to MCP config                |
| `lspServers` | string\|object | LSP server configurations or path to LSP config                |

**Archive authentication fields:**

Set these when the entry has an [`archive` source](#zip-archives) on a server that requires credentials.

| Field           | Type   | Description                                                                                                                                                                                                                                                                                         |
| :-------------- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `headers`       | object | HTTP headers Claude Code sends when it downloads this entry's archive. Overrides the marketplace's headers of the same name. Requires Claude Code v2.1.238 or later.                                                                                                                                |
| `headersHelper` | string | Command that prints the HTTP headers for this entry's archive download as one JSON object, for a credential that expires. See [Authenticate archive downloads](#authenticate-archive-downloads). The entry must also set [`"strict": false`](#strict-mode). Requires Claude Code v2.1.238 or later. |

## Plugin sources

Plugin sources tell Claude Code where to get each individual plugin listed in your marketplace. These are set in the `source` field of each plugin entry in `marketplace.json`.

Claude Code copies each installed plugin into the local versioned plugin cache at `~/.claude/plugins/cache`, except for a [`command` source in link mode](#copy-mode-and-link-mode), which Claude Code uses in place. Claude Code also [installs the plugin's eligible Node.js package dependencies](/docs/en/plugins-reference#node-js-package-dependencies) into the cached copy.

| Source        | Type                            | Fields                             | Notes                                                                                                                                                                                                                                               |
| ------------- | ------------------------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Relative path | `string` (e.g. `"./my-plugin"`) | none                               | Local directory within the marketplace repo. Must start with `./`, unless you write a [bare name under `metadata.pluginRoot`](#relative-paths). Claude Code resolves the path relative to the marketplace root, not the `.claude-plugin/` directory |
| `github`      | object                          | `repo`, `ref?`, `sha?`             |                                                                                                                                                                                                                                                     |
| `url`         | object                          | `url`, `ref?`, `sha?`              | Git URL source                                                                                                                                                                                                                                      |
| `git-subdir`  | object                          | `url`, `path`, `ref?`, `sha?`      | Subdirectory within a git repo. Clones sparsely to minimize bandwidth for monorepos                                                                                                                                                                 |
| `npm`         | object                          | `package`, `version?`, `registry?` | Installed via `npm install`                                                                                                                                                                                                                         |
| `archive`     | object                          | `url`, `sha256?`                   | Zip archive downloaded over HTTPS. Works without git or npm on the user's machine. Requires Claude Code v2.1.224 or later                                                                                                                           |
| `command`     | object                          | `command`, `timeout?`, `mode?`     | Plugin directory produced by running a local command, re-run once per session to pick up changes. Requires Claude Code v2.1.229 or later                                                                                                            |

<Note>
  **Marketplace sources vs plugin sources**: These are different concepts that control different things.

  * **Marketplace source**: where to fetch the `marketplace.json` catalog itself. Set when users run `/plugin marketplace add` or in `extraKnownMarketplaces` settings. Git-based marketplace sources support `ref` (branch/tag) but not `sha`.
  * **Plugin source**: where to fetch an individual plugin listed in the marketplace. Set in the `source` field of each plugin entry inside `marketplace.json`. Git-based plugin sources support both `ref` (branch/tag) and `sha` (exact commit).

  For example, a marketplace hosted at `acme-corp/plugin-catalog` (marketplace source) can list a plugin fetched from `acme-corp/code-formatter` (plugin source). The marketplace source and plugin source point to different repositories and are pinned independently.
</Note>

The git-based source types below are `github`, `url`, and `git-subdir`. When both `ref` and `sha` are set on any of them, the `sha` is the effective pin. Claude Code fetches and checks out the pinned commit directly.

On most git hosts, including GitHub, GitLab, and Bitbucket, this means installation succeeds even if the branch or tag named by `ref` has since been deleted upstream, as long as the commit is still reachable from the repository. Some servers, such as AWS CodeCommit, don't support fetching commits by SHA. On those servers the `ref` must still exist and the pinned commit must be reachable from it.

If you distribute plugins through **Organization settings > Plugins**, only some source types are allowed. See [Distribute through organization settings](#distribute-through-organization-settings).

### Relative paths

For plugins in the same repository, use a path starting with `./`:

```json theme={null}
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

Paths resolve relative to the marketplace root, which is the directory containing `.claude-plugin/`. In the example above, `./plugins/my-plugin` points to `<repo>/plugins/my-plugin`, even though `marketplace.json` lives at `<repo>/.claude-plugin/marketplace.json`. Don't use `../` to reference paths outside the marketplace root.

A bare name is a single directory name with no `/`, such as `"formatter"`. To write bare names instead of `./` paths, set [`metadata.pluginRoot`](#optional-fields) to the directory they resolve under. With `"pluginRoot": "./plugins"`, Claude Code resolves `"source": "formatter"` to `./plugins/formatter`. Requires Claude Code v2.1.239 or later.

`metadata.pluginRoot` must itself be a relative path inside the marketplace. Claude Code ignores it for a source that already starts with `./`. A source that contains a `/`, such as `team-a/formatter`, isn't a bare name and still needs the `./` prefix, even when `metadata.pluginRoot` is set.

<Note>
  Claude Code resolves relative paths against a local copy of the marketplace, so they work when users add your marketplace from a git source or a local directory. If users add your marketplace via a direct URL to the `marketplace.json` file, relative paths won't resolve, because Claude Code downloads only that file. For URL-based distribution, use any other [plugin source](#plugin-sources) instead. See [Troubleshooting](#plugins-with-relative-paths-fail-in-url-based-marketplaces) for details.
</Note>

### GitHub repositories

```json theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

You can pin to a specific branch, tag, or commit:

```json theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Field  | Type   | Description                                                           |
| :----- | :----- | :-------------------------------------------------------------------- |
| `repo` | string | Required. GitHub repository in `owner/repo` format                    |
| `ref`  | string | Optional. Git branch or tag (defaults to repository default branch)   |
| `sha`  | string | Optional. Full 40-character git commit SHA to pin to an exact version |

### Git repositories

```json theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

You can pin to a specific branch, tag, or commit:

```json theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Field | Type   | Description                                                                                                                                              |
| :---- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url` | string | Required. Full git repository URL (`https://` or `git@`). The `.git` suffix is optional, so Azure DevOps and AWS CodeCommit URLs without the suffix work |
| `ref` | string | Optional. Git branch or tag (defaults to repository default branch)                                                                                      |
| `sha` | string | Optional. Full 40-character git commit SHA to pin to an exact version                                                                                    |

### Git subdirectories

Use `git-subdir` to point to a plugin that lives inside a subdirectory of a git repository. Claude Code uses a sparse, partial clone to fetch only the subdirectory, minimizing bandwidth for large monorepos.

```json theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin"
  }
}
```

You can pin to a specific branch, tag, or commit:

```json theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

The `url` field also accepts a GitHub shorthand (`owner/repo`) or SSH URLs (`git@github.com:owner/repo.git`).

| Field  | Type   | Description                                                                                              |
| :----- | :----- | :------------------------------------------------------------------------------------------------------- |
| `url`  | string | Required. Git repository URL, GitHub `owner/repo` shorthand, or SSH URL                                  |
| `path` | string | Required. Subdirectory path within the repo containing the plugin (for example, `"tools/claude-plugin"`) |
| `ref`  | string | Optional. Git branch or tag (defaults to repository default branch)                                      |
| `sha`  | string | Optional. Full 40-character git commit SHA to pin to an exact version                                    |

### npm packages

Plugins distributed as npm packages are installed using `npm install`. This works with any package on the public npm registry or a private registry your team hosts.

```json theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin"
  }
}
```

To pin to a specific version, add the `version` field:

```json theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "2.1.0"
  }
}
```

To install from a private or internal registry, add the `registry` field:

```json theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

| Field      | Type   | Description                                                                                  |
| :--------- | :----- | :------------------------------------------------------------------------------------------- |
| `package`  | string | Required. Package name or scoped package (for example, `@org/plugin`)                        |
| `version`  | string | Optional. Version or version range (for example, `2.1.0`, `^2.0.0`, `~1.5.0`)                |
| `registry` | string | Optional. Custom npm registry URL. Defaults to the system npm registry (typically npmjs.org) |

### Zip archives

Use `archive` to distribute a plugin as a zip file that Claude Code downloads over HTTPS, so installs work without git or npm on the user's machine. Host the file on any static file server or artifact repository, such as an S3 bucket, an Artifactory generic repository, or nginx. Requires Claude Code v2.1.224 or later. On versions v2.1.120 through v2.1.223, installing the plugin fails with `This plugin uses a source type your Claude Code version does not support. Update Claude Code and try again.`; on older versions, a marketplace containing an `archive` entry fails to load entirely.

This entry installs the plugin from a zip file on an artifact server:

```json theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "archive",
    "url": "https://artifacts.example.com/claude-plugins/my-plugin-2.1.0.zip"
  }
}
```

When you build the zip, you can zip the plugin's contents directly or zip the plugin folder itself. Claude Code looks for `.claude-plugin/` at the top of the archive, then inside a single top-level folder, so both layouts install:

```text theme={null}
my-plugin.zip          my-plugin.zip
├── .claude-plugin/    └── my-plugin/
│   └── plugin.json        ├── .claude-plugin/
└── commands/              │   └── plugin.json
                           └── commands/
```

Claude Code doesn't look deeper than one folder, so a plugin nested further down fails to install. Claude Code refuses archives larger than 256 MiB.

To pin the exact file, add a `sha256` field with the archive's digest:

```json theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "archive",
    "url": "https://artifacts.example.com/claude-plugins/my-plugin-2.1.0.zip",
    "sha256": "6bfa50e3d2e00c052b46abe51fff89346ac803e45771f76dcf6df1ab74cca5e1"
  }
}
```

If the downloaded file doesn't match the pin, Claude Code refuses the install and reports [`Plugin archive integrity check failed`](/docs/en/errors#plugin-archive-integrity-check-failed).

Archive sources accept these fields:

| Field    | Type   | Description                                                                                                                                                                                                                |
| :------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`    | string | Required. HTTPS URL of the zip archive. Claude Code rejects `http://` URLs, along with loopback, link-local, and cloud-metadata hosts. Every redirect hop must satisfy the same rules, or Claude Code refuses the download |
| `sha256` | string | Optional. SHA-256 digest of the archive as 64 hex characters, uppercase or lowercase. Claude Code verifies every download against it and refuses the install on a mismatch                                                 |

The `sha256` digest also serves as the plugin's version when neither `plugin.json` nor the marketplace entry declares one. See [Version management](/docs/en/plugins-reference#version-management). If you declare a `version`, that version string is the update signal, so after changing the zip and its digest, bump the version too, or users keep the cached copy.

#### Authenticate archive downloads

To authenticate an archive download, such as a download from a private registry, set the HTTP headers Claude Code sends with it. Set `headers` on the `url` source you registered the marketplace from, such as an [`extraKnownMarketplaces`](/docs/en/settings-reference#extraknownmarketplaces) entry. On Claude Code v2.1.238 or later, you can set it on the plugin's entry instead, beside `source`.

If the value you would put in `headers` is short-lived, such as a token your registry mints on request, set a `headersHelper` command in the same place instead. Claude Code runs the command and sends the JSON object it prints as that place's headers. Requires Claude Code v2.1.238 or later.

The place you choose decides which downloads get the headers and when Claude Code runs the command:

| Place                    | Downloads that get the headers                                                             | When Claude Code runs a `headersHelper` set there                                                                                                                   |
| :----------------------- | :----------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Marketplace `url` source | Archive downloads on the marketplace URL's origin, meaning the same scheme, host, and port | Before each fetch of the marketplace's `marketplace.json` and before each archive download on that origin. Claude Code reuses one run's output for up to 60 seconds |
| Plugin entry             | That entry's download only                                                                 | Only when a user installs or updates that one plugin by itself and [accepts the command](#how-users-accept-a-headershelper-command)                                 |

Where both places set a header of the same name, Claude Code sends the entry's value. Within one place, a header the command prints overrides a header of the same name listed in `headers`.

##### Add a headersHelper to a plugin entry

This entry sets `headersHelper` beside `source`. It also sets `"strict": false`, which Claude Code requires of a `marketplace.json` entry that sets `headersHelper`. With [`"strict": false`](#strict-mode), the marketplace entry is the plugin's entire definition, so a user can review what the plugin contains before accepting the command:

```json theme={null}
{
  "name": "my-plugin",
  "description": "Formatting commands for internal services",
  "strict": false,
  "commands": "./commands",
  "source": {
    "source": "archive",
    "url": "https://registry.example.com/plugins/my-plugin-2.1.0.zip"
  },
  "headersHelper": "/opt/bin/mint-registry-token.sh"
}
```

To check the entry, run `claude plugin install my-plugin@your-marketplace`. Claude Code shows you the command and the archive URL, and downloads the zip after you accept.

Before v2.1.238, Claude Code downloaded an entry's archive without its `headers` or `headersHelper`, so an install that relied on them failed with `HTTP 401 while downloading plugin archive from`, followed by the URL, with the registry's status code in place of 401.

#### Write the headersHelper command

Whether you set `headersHelper` on a marketplace's `url` source or on a plugin entry, write the command to meet these requirements:

* **Command text**: at most 500 characters of printable ASCII, with no run of four or more spaces.
* **Output**: print one JSON object of header names and string values on stdout, then exit 0 within 10 seconds.
* **Shell and working directory**: Claude Code runs the command through `sh`, or `cmd.exe` on Windows, from the configuration directory, `~/.claude` or [`CLAUDE_CONFIG_DIR`](/docs/en/env-vars#variables). Give an absolute path or a command on `PATH`, because a relative path resolves against that directory, not the user's project.
* **Variables Claude Code removes**: from the environment of a command set in a `marketplace.json` entry or in a project's `.claude/settings.json` or `.claude/settings.local.json`, Claude Code removes every variable whose name contains a word such as `TOKEN`, `SECRET`, `KEY`, or `AUTH`, including `ANTHROPIC_API_KEY`. Claude Code doesn't apply this removal to a command set in user settings, a `--settings` file, or managed settings.
* **Variables Claude Code sets**: `CLAUDE_CODE_MARKETPLACE_URL` and `CLAUDE_CODE_MARKETPLACE_NAME` for a `url` source's command, and `CLAUDE_CODE_PLUGIN_NAME` and `CLAUDE_CODE_PLUGIN_ARCHIVE_URL` for an entry's command. `CLAUDE_CODE_MARKETPLACE_NAME` is unset on the first fetch after a user adds a marketplace by URL, because that fetch is what supplies the name.

A command that mints a bearer token prints an object like this one:

```json theme={null}
{"Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9"}
```

#### When Claude Code skips a headersHelper command or drops its output

Claude Code doesn't run a `headersHelper` command, or drops headers that came from `headers` or from the command's output, in these situations:

* **Command fails**: if the command exits non-zero, runs past 10 seconds, or prints anything other than a JSON object of string values, Claude Code doesn't make the fetch or download it ran the command for.
* **Marketplace URL doesn't start with `https://`**: Claude Code doesn't run that `url` source's command and sends only the headers listed in its `headers` field.
* **Redirect leaves the origin**: when a download is redirected off the archive URL's origin, Claude Code drops the `headers` values and command output of both the marketplace `url` source and the plugin entry.
* **Entry sets a routing or identity header**: Claude Code drops request-routing and client-identity names such as `Host`, `Cookie`, and `X-Forwarded-*` from an entry's `headers` and command output, and keeps authentication names such as `Authorization`. Claude Code filters every `marketplace.json` entry this way, and an [inline settings entry](/docs/en/settings-reference#extraknownmarketplaces) depending on which file declares it.
* **Command set in an `--add-dir` directory's settings**: Claude Code ignores it, on a `url` source and on an [inline plugin entry](/docs/en/settings-reference#extraknownmarketplaces) alike, and sends only that file's `headers`.
* **Managed settings block the command**: setting [`disableCommandPluginSources`](/docs/en/settings-reference#disablecommandpluginsources) to `true` blocks `headersHelper` commands, and [`allowManagedHooksOnly`](/docs/en/settings-reference#allowmanagedhooksonly) blocks them too unless `disableCommandPluginSources` is explicitly `false`. Under either block, Claude Code still runs the command for a marketplace that managed settings themselves declare.

#### How users accept a headersHelper command

A user accepts a plugin entry's command each time they install or update that one plugin by itself, from the plugin's own view in `/plugin` or with `claude plugin install` or `claude plugin update`. Claude Code shows the command and the archive URL, and runs the command only after the user accepts. In a non-interactive shell, pass [`--yes`](/docs/en/plugins-reference#plugin-install) to accept it.

Claude Code runs only the command it showed, for the archive URL it showed. If the entry's command or archive URL changed in between, Claude Code refuses the install or update. A change in the query string alone doesn't count.

##### Installs and updates that refuse the command instead of asking

On any operation other than a single-plugin install or update, Claude Code neither runs an entry's command nor downloads its archive, so the plugin stays at its installed version or stays uninstalled. What the user sees depends on the operation:

* **Installing several plugins at once, from a plugin suggestion, or as another plugin's dependency**: Claude Code refuses the plugin that has the command and points the user at that plugin's own view in `/plugin`. The other plugins in a bulk install still install. A plugin that depends on the refused plugin fails to install until the user installs the refused plugin by itself.
* **Background auto-update, or session start for a plugin whose archive was never downloaded**: Claude Code lists the plugin in the `/plugin` Errors tab so the user knows to install or update it by hand. An auto-update that finds the entry still advertises the installed version lists nothing.

##### When a marketplace `url` source's command runs

A marketplace `url` source's `headersHelper` is declared in a settings file, such as an [`extraKnownMarketplaces`](/docs/en/settings-reference#extraknownmarketplaces) entry, rather than in the catalog the marketplace publishes, so Claude Code doesn't ask the user to accept it on each install or update. The settings file that declares it decides when Claude Code runs it:

| Settings file                                                                 | When Claude Code runs the command                                                                                                                                                                                                            |
| :---------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| User settings, a `--settings` file, or a managed settings file on the machine | Without asking, including during a background marketplace refresh                                                                                                                                                                            |
| A project's `.claude/settings.json` or `.claude/settings.local.json`          | Only after the user accepts the [workspace trust dialog](/docs/en/permissions#what-runs-before-you-trust-a-folder) for that folder itself. A `-p` or SDK session doesn't count as accepting it, and neither does trust granted to a parent folder |
| Server-managed settings                                                       | Only after the user approves the delivered settings in the [security approval dialog](/docs/en/server-managed-settings#security-approval-dialogs)                                                                                                 |

In a `-p` or SDK session, Claude Code can't show the security approval dialog. It applies the other delivered settings, but the marketplace fetch, and any archive download that needs the command, fails until a user has approved in an interactive session.

For an [inline plugin entry](/docs/en/settings-reference#extraknownmarketplaces) in one of these files, Claude Code requires the same folder trust or settings approval as for a marketplace-level command in that file, and the user also accepts the entry's command on each install or update.

### Command sources

Use `command` when a locally installed tool produces the plugin directory, such as an IDE that renders its plugin for the currently selected toolchain. Claude Code runs the command when the user installs the plugin and re-runs it in the background once per session, so your users pick up the tool's changed output without reinstalling. Requires Claude Code v2.1.229 or later. On v2.1.120 through v2.1.228, installing the plugin fails with `This plugin uses a source type your Claude Code version does not support. Update Claude Code and try again.`, and on older versions the whole marketplace fails to load.

This entry installs the plugin from whatever directory the tool prints:

```json theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "command",
    "command": "my-tool claude-plugin-path"
  }
}
```

Claude Code runs the command through the platform shell, `sh` on macOS and Linux or `cmd.exe` on Windows, from the user's home directory. The command must print exactly one line on stdout and exit with code 0. That line is the absolute path of a directory that contains the complete plugin by the time the command exits, and the path may change between runs.

Claude Code stops a command that runs longer than `timeout` seconds, and the install or update fails. Claude Code also refuses the printed path in these cases, and the install or update fails the same way:

* The directory has no plugin content at its top level, such as a `.claude-plugin/` directory or a `skills/`, `commands/`, `agents/`, or `hooks/` directory
* The directory is the one Claude Code was started in, or one of its parents
* On Windows, the path is a UNC path

Command sources accept these fields:

| Field     | Type   | Description                                                                                                                                                                                                                                                          |
| :-------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `command` | string | Required. Shell command that prints the plugin directory's absolute path as a single line on stdout and exits 0. Must be printable ASCII, at most 500 characters, with no runs of four or more spaces, so users can review the whole command they're asked to accept |
| `timeout` | number | Optional. Whole number of seconds to wait for the command before giving up (default: 60, maximum: 600)                                                                                                                                                               |
| `mode`    | string | Optional. `"copy"` (default) copies the printed directory into the plugin cache. `"link"` uses the printed directory in place. See [Copy mode and link mode](#copy-mode-and-link-mode)                                                                               |

#### Copy mode and link mode

With the default `"mode": "copy"`, Claude Code copies the printed directory into the versioned plugin cache and derives the [plugin version](/docs/en/plugins-reference#version-management) from a hash of the directory's contents. Your tool can delete or rewrite the directory after the command exits, and a re-run that produces identical content counts as up to date. Claude Code refuses to install a directory larger than 256 MiB or containing more than 20,000 entries.

Set `"mode": "link"` for large plugin directories that shouldn't be copied, such as a rendered SDK export. Claude Code fills the plugin's cache entry with a link to each top-level entry of the printed directory and uses the files in place, so nothing is copied, file contents aren't hashed, and the size limits don't apply. The install fails if a top-level entry is a symlink that points outside the printed directory. Claude Code also skips the [Node.js package dependency install](/docs/en/plugins-reference#node-js-package-dependencies) for a link-mode plugin, so print a directory that already contains any `node_modules` the plugin needs.

Keep the printed directory in place for as long as the plugin stays installed, because Claude Code loads the plugin through those links at every startup. Claude Code derives the [plugin version](/docs/en/plugins-reference#version-management) from the printed directory's real path and its top-level entries, not the files inside, so print a different path to signal new content. In a session started in the printed directory or anywhere below it, Claude Code doesn't load the plugin at all.

Claude Code doesn't support link mode on Windows and refuses to install a link-mode plugin there. Declare `"mode": "copy"` instead.

#### How users accept the command

Claude Code runs your command on the user's machine, so it binds every run to the user's explicit acceptance:

* When users install the plugin from its details screen in `/plugin`, or install or update it with `claude plugin install` or `claude plugin update` in an interactive terminal, Claude Code shows them the exact command string first and records the accepted command for that installation. A `claude plugin update` that can proceed on the recorded acceptance of the same command shows nothing. In a non-interactive shell, such as a provisioning script, pass `--yes` to `claude plugin install` or `claude plugin update` to accept the command it prints.
* Every other path runs only the command the user already accepted. This includes updates started from `/plugin` and the background runs described in [When Claude Code re-runs the command](#when-claude-code-re-runs-the-command). When none was accepted, Claude Code refuses to run the command and tells the user how to review it. Claude Code never installs a command-sourced plugin as a dependency of another plugin, so users install it themselves first.
* If you change the entry's `command`, or switch its `mode`, users keep the version they already have and Claude Code stops re-running the command. In interactive sessions, the `/plugin` Errors tab shows the new command until the user reviews and accepts it by running `claude plugin update <plugin>@<marketplace>`.

Administrators can block command sources across an organization with the managed setting [`disableCommandPluginSources`](/docs/en/settings-reference#disablecommandpluginsources). If an organization sets [`allowManagedHooksOnly`](/docs/en/settings-reference#allowmanagedhooksonly), Claude Code blocks command sources by default.

#### When Claude Code re-runs the command

The printed directory reflects the tool's state at the time the command ran, so Claude Code runs the command again at these times:

* Every time the user installs or updates the plugin
* Once per session for each enabled command-sourced plugin, in the background, shortly after the session starts. This run doesn't go through marketplace auto-update, so it doesn't depend on the marketplace's [auto-update setting](/docs/en/discover-plugins#configure-auto-updates)
* At startup or on `/reload-plugins`, when an enabled plugin's installed version is missing from the plugin cache

Claude Code skips the two background runs when the user sets [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`](/docs/en/env-vars). Explicit installs and updates still run the command with that variable set.

When the command's hashed output has changed, Claude Code installs the result as a new version and reloads it in the running interactive session, switching [the same components that `/reload-plugins` switches](/docs/en/plugins-reference#environment-variables). The user sees a notification that the plugin was reloaded. If reloading in place would invalidate the session's prompt cache, Claude Code instead prompts the user to run `/reload-plugins`, which [warns about the cache cost and applies when rerun with `--force`](/docs/en/prompt-caching#enabling-or-disabling-a-plugin).

### Advanced plugin entries

This example shows a plugin entry using many of the optional fields, including custom paths for commands, agents, hooks, and MCP servers:

```json theme={null}
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Enterprise workflow automation tools",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "enterprise@example.com"
  },
  "homepage": "https://docs.example.com/plugins/enterprise-tools",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity",
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": ["./agents/security-reviewer.md", "./agents/compliance-checker.md"],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "enterprise-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  },
  "strict": false
}
```

Key things to notice:

* **`commands` and `agents`**: you can specify multiple directories or individual files. Paths are relative to the plugin root.
* **`${CLAUDE_PLUGIN_ROOT}`**: use this variable in hook commands and MCP server configs to reference files within the plugin's installation directory.
  * See the [substitution table](/docs/en/plugins-reference#environment-variables) for which config fields substitute it per server type
  * For dependencies or state that should survive plugin updates, use [`${CLAUDE_PLUGIN_DATA}`](/docs/en/plugins-reference#persistent-data-directory) instead
* **`strict: false`**: since this is set to false, the plugin doesn't need its own `plugin.json`. The marketplace entry defines everything. See [Strict mode](#strict-mode) below.

By default, a plugin's skills load from the `skills/` directory under its `source`. Paths listed in the `skills` field add to that scan:

```json theme={null}
"skills": ["./skills/", "./extra-skills/"]
```

When several plugin entries share one `skills/` folder at the marketplace root (`source: "./"`), list specific subdirectories instead so each entry loads only its own skills:

```json theme={null}
"source": "./",
"skills": ["./skills/code-review", "./skills/docs"]
```

With a marketplace-root `source`, the listed paths are the complete set for that entry, and other directories in the shared `skills/` folder don't load. Listing `./skills/` itself, or the plugin root, keeps the full scan. If none of the listed paths exist, the default scan runs instead.

### Strict mode

The `strict` field controls whether `plugin.json` is the authority for component definitions (skills, agents, hooks, MCP servers, output styles).

| Value            | Behavior                                                                                                                                                         |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `true` (default) | `plugin.json` is the authority. The marketplace entry can supplement it with additional components, and both sources are merged.                                 |
| `false`          | The marketplace entry is the entire definition. If the plugin also has a `plugin.json` that declares components, that's a conflict and the plugin fails to load. |

**When to use each mode:**

* **`strict: true`**: the plugin has its own `plugin.json` and manages its own components. The marketplace entry can add extra skills or hooks on top. This is the default and works for most plugins.
* **`strict: false`**: the marketplace operator wants full control. The plugin repo provides raw files, and the marketplace entry defines which of those files are exposed as skills, agents, hooks, etc. Useful when the marketplace restructures or curates a plugin's components differently than the plugin author intended.

## Host and distribute marketplaces

### Host on GitHub (recommended)

GitHub is the recommended way to host and distribute a marketplace:

1. **Create a repository**: set up a new repository for your marketplace
2. **Add marketplace file**: create `.claude-plugin/marketplace.json` with your plugin definitions
3. **Share with teams**: users add your marketplace with `/plugin marketplace add owner/repo`

**Benefits**: built-in version control, issue tracking, and team collaboration features.

### Host on other git services

Any git hosting service works, such as GitLab, Bitbucket, and self-hosted servers. Users add with the full repository URL:

```shell theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### Private repositories

Claude Code supports installing plugins from private repositories. If you distribute your marketplace through [**Organization settings > Plugins**](https://claude.ai/admin-settings/plugins) instead, your git credentials aren't involved: organization sync reads the marketplace repository through the Claude GitHub App or your organization's GitHub Enterprise App, and a plugin source it can't authenticate to must be public. See [Distribute through organization settings](#distribute-through-organization-settings) for the full rules.

#### Commands you run

When you run `/plugin marketplace add`, `/plugin install`, `/plugin update`, or `/plugin marketplace update`, Claude Code uses your existing git credential helpers, so HTTPS access via `gh auth login`, macOS Keychain, or `git-credential-store` works the same as in your terminal. SSH access works as long as the host is already in your `known_hosts` file and the key is loaded in `ssh-agent`, since Claude Code suppresses interactive SSH prompts for the host fingerprint and key passphrase. GitHub `owner/repo` shorthand sources clone over SSH by default; set [`CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`](/docs/en/env-vars#variables) to clone them over HTTPS instead.

#### Background auto-updates

By default, the background refresh disables git credential helpers for its `git pull`, so the pull can't authenticate to private repositories over HTTPS even when a helper is configured. SSH remotes aren't affected: a key loaded in `ssh-agent` authenticates background pulls the same way as the commands you run. When the background pull fails, Claude Code falls back to re-cloning the marketplace from scratch. The re-clone does use your stored git credentials, but it can [time out on large repositories](#git-operations-time-out), so private-marketplace auto-updates may fail intermittently.

Two settings make private marketplaces behave predictably:

* Set `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1` to keep the existing clone when the background pull fails, instead of deleting and re-cloning. Your plugins keep working from the last synced state, and manual updates with `/plugin marketplace update` still pull with your credentials.
* Configure a git credential helper, for example with `gh auth setup-git` for GitHub, so the re-clone fallback can authenticate without prompting.

Setting a provider token such as `GITHUB_TOKEN` in your environment doesn't by itself enable background authentication. Tokens take effect only through a configured credential helper, for example the `gh` CLI's helper, which reads `GH_TOKEN` and `GITHUB_TOKEN`.

To make the background pull itself authenticate over HTTPS, configure a global git URL rewrite. The rewrite embeds a token in the remote URL, so it takes effect even though the background pull disables credential helpers, and a successful pull skips the re-clone fallback. The following example rewrites the marketplace repository's URL to include an access token:

```bash theme={null}
git config --global url."https://x-access-token:YOUR_TOKEN@github.com/acme-corp/plugins".insteadOf "https://github.com/acme-corp/plugins"
```

Scope the rewrite to the marketplace repository or organization path. A rewrite whose base is only the host applies to every fetch and push to that host on the machine and overrides your normal credentials, including pushes to your own repositories.

Each provider expects a different username in the rewritten URL, and the same path scoping applies to every provider. For self-hosted servers, replace the hostname with your server's hostname:

| Provider  | Rewritten URL form                                                |
| :-------- | :---------------------------------------------------------------- |
| GitHub    | `https://x-access-token:YOUR_TOKEN@github.com/acme-corp/plugins`  |
| GitLab    | `https://oauth2:YOUR_TOKEN@gitlab.com/acme-corp/plugins`          |
| Bitbucket | `https://x-token-auth:YOUR_TOKEN@bitbucket.org/acme-corp/plugins` |

The rewrite stores the token in plaintext in your gitconfig, so use a token with read-only access to the marketplace repository.

<Note>
  In CI/CD environments, configure a git credential helper before installing plugins from private repositories. On GitHub Actions, export a token with read access to the marketplace repository as `GH_TOKEN`, then run `gh auth setup-git`. The default workflow token can only access the workflow's own repository, so a private marketplace in another repository needs a personal access token or app token. A global URL rewrite configured in the pipeline also authenticates the background pull directly.
</Note>

### Distribute through organization settings

If you distribute plugins through [**Organization settings > Plugins**](https://claude.ai/admin-settings/plugins) on a Team or Enterprise plan, these source rules apply:

* The marketplace repository must be private or internal. Organization sync reads it through the Claude GitHub App or your organization's GitHub Enterprise App.
* Each plugin source must be of type `github`, `url`, or `git-subdir`, or a [relative path](#relative-paths) that starts with `./`. If you list a plugin by bare name under `metadata.pluginRoot`, organization sync rejects it as an unsupported source, so write the path out, such as `./plugins/deploy-tools`.
* A plugin source can be private in two cases:
  * A github.com source that shares the marketplace repository's owner
  * A source on your organization's GitHub Enterprise host with the GHE App installed on the repository
* Organization sync fetches every other source without credentials, so github.com repositories under a different owner and repositories on other hosts, such as GitLab or Bitbucket, must be public.

See [Manage plugins for your organization](https://support.claude.com/en/articles/13837433) for the admin workflow.

To include private plugins, place the plugin folders inside the marketplace repository and reference them with a [relative path](#relative-paths). Organization sync packages each plugin during distribution, so users never need access to a separate source repository.

For example, this `marketplace.json` plugin entry references a plugin you committed at `plugins/deploy-tools` in the marketplace repository:

```json theme={null}
{
  "name": "deploy-tools",
  "source": "./plugins/deploy-tools"
}
```

#### Keep executables out of the top-level bin directory

Don't include a top-level `bin/` directory in any plugin you distribute through organization settings. claude.ai rejects a plugin that has one, whether the plugin arrives by marketplace sync or by direct upload:

* **Marketplace sync**: organization sync rejects that plugin and syncs the rest of the marketplace. The error message starts with `Plugin contains a top-level bin/ directory`.
* **Direct upload**: if you upload the plugin in [**Organization settings > Plugins**](https://claude.ai/admin-settings/plugins) instead, claude.ai rejects the upload with the same message.

Keep executables in another directory, such as `scripts/`, and reference them as `${CLAUDE_PLUGIN_ROOT}/scripts/<name>` from your [skills, hooks, or MCP server configs](/docs/en/plugins-reference#environment-variables).

### Require marketplaces for your team

You can configure your repository so Claude Code adds your marketplace for team members once they [trust the project folder](/docs/en/permissions#what-runs-before-you-trust-a-folder), with no separate prompt. Add your marketplace to `.claude/settings.json`:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

You can also specify which plugins should be enabled by default:

```json theme={null}
{
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

For full configuration options, see [Plugin settings](/docs/en/settings-reference#plugin-settings).

<Note>
  If you use a local `directory` or `file` source with a relative path, the path resolves against your repository's main checkout. When you run Claude Code from a git worktree, the path still points at the main checkout, so all worktrees share the same marketplace location. Marketplace state is stored once per user in `~/.claude/plugins/known_marketplaces.json`, not per project.
</Note>

### Pre-populate plugins for containers

For container images and CI environments, you can pre-populate a plugins directory at build time so Claude Code starts with marketplaces and plugins already available, without cloning anything at runtime. Set the `CLAUDE_CODE_PLUGIN_SEED_DIR` environment variable to point at this directory.

To layer multiple seed directories, separate paths with `:` on Unix or `;` on Windows. Claude Code searches each directory in order and uses the first seed that contains a given marketplace or plugin cache.

The seed directory mirrors the structure of `~/.claude/plugins`:

```
$CLAUDE_CODE_PLUGIN_SEED_DIR/
  known_marketplaces.json
  marketplaces/<name>/...
  cache/<marketplace>/<plugin>/<version>/...
```

To build a seed directory, run Claude Code once during image build, install the plugins you need, then copy the resulting `~/.claude/plugins` directory into your image and point `CLAUDE_CODE_PLUGIN_SEED_DIR` at it.

To skip the copy step, set `CLAUDE_CODE_PLUGIN_CACHE_DIR` to your target seed path during the build so plugins install directly there:

```bash theme={null}
CLAUDE_CODE_PLUGIN_CACHE_DIR=/opt/claude-seed claude plugin marketplace add your-org/plugins
CLAUDE_CODE_PLUGIN_CACHE_DIR=/opt/claude-seed claude plugin install my-tool@your-plugins
```

Then set `CLAUDE_CODE_PLUGIN_SEED_DIR=/opt/claude-seed` in your container's runtime environment so Claude Code reads from the seed on startup.

At startup, Claude Code registers marketplaces found in the seed's `known_marketplaces.json` into the primary configuration, and uses plugin caches found under `cache/` in place without re-cloning. This works in both interactive mode and non-interactive mode with the `-p` flag.

Behavior details:

* **Read-only**: the seed directory is never written to. Auto-updates are disabled for seed marketplaces since git pull would fail on a read-only filesystem.
* **Seed entries take precedence**: marketplaces declared in the seed overwrite any matching entries in the user's configuration on each startup. To opt out of a seed plugin, use `/plugin disable` rather than removing the marketplace.
* **Path resolution**: Claude Code locates marketplace content by probing `$CLAUDE_CODE_PLUGIN_SEED_DIR/marketplaces/<name>/` at runtime, not by trusting paths stored inside the seed's JSON. This means the seed works correctly even when mounted at a different path than where it was built.
* **Mutation is blocked**: running `/plugin marketplace remove` or `/plugin marketplace update` against a seed-managed marketplace fails with guidance to ask your administrator to update the seed image.
* **Composes with settings**: if `extraKnownMarketplaces` or `enabledPlugins` declare a marketplace that already exists in the seed, Claude Code uses the seed copy instead of cloning.

### Managed marketplace restrictions

For organizations requiring strict control over plugin sources, administrators can restrict which plugin marketplaces users are allowed to add using the [`strictKnownMarketplaces`](/docs/en/settings-reference#strictknownmarketplaces) setting in managed settings. To also reject the CLI flags that sideload plugins, agents, and MCP servers for a single run, pair it with [`disableSideloadFlags`](/docs/en/settings-reference#disablesideloadflags). To allowlist which marketplaces' plugins can appear as contextual install suggestions, set [`pluginSuggestionMarketplaces`](/docs/en/settings-reference#pluginsuggestionmarketplaces).

`strictKnownMarketplaces` matches the marketplace a plugin comes from, not the entries inside it, so users can still install a plugin with a [`command` source](#command-sources) from an allowed marketplace. To block command sources as well, set [`disableCommandPluginSources`](/docs/en/settings-reference#disablecommandpluginsources).

When `strictKnownMarketplaces` is configured in managed settings, the restriction behavior depends on the value:

| Value               | Behavior                                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------------ |
| Undefined (default) | No restrictions. Users can add any marketplace                                                   |
| Empty array `[]`    | Complete lockdown. Blocks every marketplace source, including the official Anthropic marketplace |
| List of sources     | Allowlist enforced. Users can add only marketplaces that match an entry                          |

#### Common configurations

Disable all marketplace additions, including the official Anthropic marketplace:

```json theme={null}
{
  "strictKnownMarketplaces": []
}
```

Allow only the official Anthropic marketplace. Matching for a single-repository entry is exact, so this entry doesn't cover `ref` or `path` variants of the same repository:

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "anthropics/claude-plugins-official"
    }
  ]
}
```

With this entry, Claude Code keeps an already-registered official marketplace available and, on a fresh machine, registers the marketplace automatically the first time you start Claude Code interactively.

Automatic registration doesn't cover every machine. It most commonly misses:

* Non-interactive environments that run before the machine's first interactive launch.
* Machines where Claude Code already ran interactively under a policy that blocked the marketplace, such as the empty-array lockdown. Claude Code records the blocked attempt and doesn't retry after the policy changes.

On these machines, add the marketplace to [`extraKnownMarketplaces`](/docs/en/settings-reference#extraknownmarketplaces) in the same `managed-settings.json` so Claude Code registers it automatically, or run `claude plugin marketplace add anthropics/claude-plugins-official`.

Allow specific marketplaces only:

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    }
  ]
}
```

Allow every marketplace repository under a GitHub organization with an [owner-wildcard](/docs/en/settings-reference#owner-wildcards) entry. Owner wildcards require Claude Code v2.1.223 or later.

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/*"
    }
  ]
}
```

Allow all marketplaces from an internal git server using regex pattern matching on the host. This is the recommended approach for [GitHub Enterprise Server](/docs/en/github-enterprise-server#plugin-marketplaces-on-ghes) or self-hosted GitLab instances:

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

Allow filesystem-based marketplaces from a specific directory using regex pattern matching on the path:

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "pathPattern",
      "pathPattern": "^/opt/approved/"
    }
  ]
}
```

Use `".*"` as the `pathPattern` to allow any filesystem path while still controlling network sources with `hostPattern`.

<Note>
  `strictKnownMarketplaces` restricts what users can add, but doesn't register marketplaces on its own. To register an allowed marketplace for users automatically, add it to [`extraKnownMarketplaces`](/docs/en/settings-reference#extraknownmarketplaces) in the same `managed-settings.json`.

  The official Anthropic marketplace is the only one Claude Code registers on its own, and only when the allowlist allows it. Automatic registration also misses some machines, such as non-interactive environments and machines where an earlier policy blocked it. To cover those machines, add the official marketplace to `extraKnownMarketplaces` as well. For the two settings side by side, see the [`strictKnownMarketplaces` reference](/docs/en/settings-reference#strictknownmarketplaces).
</Note>

#### How restrictions work

Restrictions are checked before any network or filesystem operation. The check runs on marketplace add and on plugin install, update, refresh, and auto-update. If a marketplace was added before the policy was configured and its source no longer matches the allowlist, Claude Code refuses to install or update plugins from it. The same enforcement applies to `blockedMarketplaces`.

To block every marketplace repository under a GitHub owner, use the owner-wildcard form in a `blockedMarketplaces` entry: `{ "source": "github", "repo": "untrusted-org/*" }`. Requires Claude Code v2.1.223 or later. For the matching rules, which differ between the blocklist and the allowlist, see [Owner wildcards](/docs/en/settings-reference#owner-wildcards).

When a user adds an `https://` repository URL that Claude Code [clones rather than fetches](/docs/en/discover-plugins#add-from-other-git-hosts), such as a bare `github.com` or `gitlab.com` repository URL, Claude Code also checks it against the `url` entries in `blockedMarketplaces`. Claude Code blocks the addition if an entry names the same URL. In that comparison, Claude Code ignores the `.git` suffix and any ref the user appends after `#`. Requires Claude Code v2.1.232 or later. Before v2.1.232, Claude Code matched a `url` entry only against a URL it fetched as a hosted `marketplace.json` file.

The allowlist uses exact matching for most source types, apart from owner-wildcard `github` entries. For a marketplace to be allowed, all specified fields must match:

* For GitHub sources: `repo` is required, either naming one repository or using the owner-wildcard form `owner/*` to cover every repository under that owner. For how wildcard entries match, including the case rules, see [Owner wildcards](/docs/en/settings-reference#owner-wildcards). For single-repository entries, `ref` must match exactly or be absent from both the marketplace source and the allowlist entry, and the same rule applies to `path`
* For URL sources: the full URL must match exactly
* For `hostPattern` sources: the marketplace host is matched against the regex pattern
* For `pathPattern` sources: the marketplace's filesystem path is matched against the regex pattern

The allowlist's exact matching treats URLs that differ only by a trailing slash, a `.git` suffix, or the `ssh://` and `https://` scheme as different values. If your organization's marketplace can be cloned by more than one URL form, prefer a `hostPattern` entry over a literal URL so the `https://`, `ssh://`, and `user@host:path` forms all match.

Because `strictKnownMarketplaces` is set in [managed settings](/docs/en/managed-settings), individual users and project configurations can't override these restrictions.

For complete configuration details including all supported source types and comparison with `extraKnownMarketplaces`, see the [strictKnownMarketplaces reference](/docs/en/settings-reference#strictknownmarketplaces).

### Version resolution and release channels

Plugin versions determine cache paths and update detection: if the resolved version matches what a user already has, `/plugin update` and auto-update skip the plugin. For git-based sources, if you omit `version`, Claude Code uses the source's resolved commit SHA, so users get an update whenever that commit changes; this is the simplest setup for internal or actively developed plugins. See [Version management](/docs/en/plugins-reference#version-management) for the full resolution order, including `archive` sources.

<Warning>
  Setting `version` pins the plugin for every source type except [`command`](#command-sources), whose version always includes a hash of what the command produced. If you declare `"version": "1.0.0"` in `plugin.json` and push new commits without changing that string, existing users of those sources keep the cached copy, because Claude Code sees the same version. Bump the field on every release, or omit it to fall back to the resolved version.

  Avoid setting `version` in both `plugin.json` and the marketplace entry. Claude Code always uses the `plugin.json` value without warning, so a stale manifest version can mask a version you set in `marketplace.json`.
</Warning>

#### Set up release channels

To support "stable" and "latest" release channels for your plugins, you can set up two marketplaces that point to different refs or SHAs of the same repo. You can then give each user group its own marketplace through managed settings in one of two ways:

* Deploy separate [endpoint-managed settings](/docs/en/managed-settings#delivery-mechanisms), such as a managed settings file or an MDM profile, to each group's devices. [How Claude Code combines managed sources](/docs/en/managed-settings#precedence-within-the-managed-tier) says whether the per-group file or profile applies on a device that also has an organization-wide source.
* Define one [Claude apps gateway policy](/docs/en/claude-apps-gateway-config#managed) per group. The gateway applies the first policy whose match rule fits a user, so order the policies so that each user reaches their group's policy. A group policy's `extraKnownMarketplaces` replaces the catch-all policy's map rather than merging with it, so list every marketplace the group needs in the group's policy, not only its channel marketplace.

Server-managed settings from the admin console [apply to every user in your organization](/docs/en/server-managed-settings#current-limitations), so they can't carry a per-group assignment.

<Warning>
  Each channel must resolve to a different version. If you use explicit versions, `plugin.json` must declare a different `version` at each pinned ref. If you omit `version`, the distinct commit SHAs already distinguish the channels. If two refs resolve to the same version string, Claude Code treats them as identical and skips the update.
</Warning>

##### Example

```json theme={null}
{
  "name": "stable-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "stable"
      }
    }
  ]
}
```

```json theme={null}
{
  "name": "latest-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "latest"
      }
    }
  ]
}
```

##### Assign channels to user groups

Assign each marketplace to its user group through the per-group endpoint-managed settings or gateway policy described under [Set up release channels](#set-up-release-channels). For example, the stable group receives:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "stable-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/stable-tools"
      }
    }
  }
}
```

The early-access group receives `latest-tools` instead:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "latest-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/latest-tools"
      }
    }
  }
}
```

#### Pin dependency versions

A plugin can constrain its dependencies to a semver range so that updates to a dependency don't break the dependent plugin. See [Constrain plugin dependency versions](/docs/en/plugin-dependencies) for the `{plugin-name}--v{version}` git-tag convention, range syntax, and how multiple constraints on the same dependency are combined.

### Rename or remove a plugin

A plugin's `name` is its stable identifier. Users reference it in `enabledPlugins`, `pluginConfigs`, and `/plugin install` commands, so changing it breaks every existing install. To change the label shown in the UI without breaking installs, set [`displayName`](#optional-plugin-fields) and keep `name` unchanged.

If you must change a plugin's `name`, or you remove a plugin from the `plugins` array, add a top-level `renames` entry so existing users migrate instead of seeing a `plugin-not-found` error. Automatic migration requires Claude Code v2.1.193 or later. Map each former name to its current name, or to `null` if the plugin no longer exists. The following example renames `formatter` to `code-formatter` and records that `legacy-linter` was removed:

```json theme={null}
{
  "name": "acme-tools",
  "owner": { "name": "Acme" },
  "plugins": [
    { "name": "code-formatter", "source": "./plugins/code-formatter" }
  ],
  "renames": {
    "formatter": "code-formatter",
    "legacy-linter": null
  }
}
```

When a user starts Claude Code with the old name still in their settings, Claude Code follows the `renames` map:

* If the entry points to a new name, Claude Code loads the plugin under its new name and shows a one-line notice such as `Renamed to "code-formatter" in the "acme-tools" marketplace`. It then rewrites the old key to the new key in the user, project, and local settings scopes for both `enabledPlugins` and `pluginConfigs`, so the notice appears once.
* For a `null` entry, Claude Code drops the old key and the notice reports that the plugin was removed from the marketplace.
* If the renamed plugin uses a remote source such as `github` or `npm`, Claude Code reports `plugin-cache-miss` after the rename and the user must run `/plugin install` once to fetch it under the new name.

Treat `renames` as append-only history: keep old entries in place even after you expect every user to have migrated. Claude Code follows chains, so if you later rename `code-formatter` to `formatter-pro`, add a second entry rather than editing the first. A user who still has the original `formatter` enabled then resolves through both entries to `formatter-pro`.

Run `claude plugin validate .` after editing the map; it rejects any entry whose chain forms a cycle or doesn't terminate at `null` or a name listed in `plugins`.

<Note>
  Managed and policy settings are read-only to Claude Code, so plugins enabled there can't be rewritten automatically. The renamed plugin still loads each session, but the rename notice recurs until an administrator updates `enabledPlugins` in the managed settings file to use the new name. The same applies to plugins enabled through other read-only sources such as `--add-dir`.
</Note>

Earlier versions of Claude Code ignore the `renames` field and report `plugin-not-found` for the old name.

## Validation and testing

Test your marketplace before sharing.

From your marketplace directory, validate the JSON syntax:

```bash theme={null}
claude plugin validate .
```

Or from within Claude Code:

```shell theme={null}
/plugin validate .
```

Add the marketplace for testing:

```shell theme={null}
/plugin marketplace add ./path/to/marketplace
```

Install a test plugin to verify everything works:

```shell theme={null}
/plugin install test-plugin@marketplace-name
```

For complete plugin testing workflows, see [Test your plugins locally](/docs/en/plugins#test-your-plugins-locally). For technical troubleshooting, see [Plugins reference](/docs/en/plugins-reference).

## Manage marketplaces from the CLI

Claude Code provides non-interactive `claude plugin marketplace` subcommands for scripting and automation. These are equivalent to the `/plugin marketplace` commands available inside an interactive session.

### Plugin marketplace add

Add a marketplace from a GitHub repository, git URL, remote URL, or local path.

```bash theme={null}
claude plugin marketplace add <source> [options]
```

**Arguments:**

* `<source>`: GitHub `owner/repo` shorthand, git URL, remote URL to a `marketplace.json` file, or local directory path. To pin to a branch or tag, append `@ref` to the GitHub shorthand or `#ref` to a git URL

A URL must include its scheme. As of Claude Code v2.1.196, a host typed without one, such as `gitlab.example.com/team/plugins`, is rejected as an invalid `owner/repo` shorthand and the error tells you to add `https://` or use `./` for a local path. Earlier versions misread it as a GitHub repository path and fail at clone time with a GitHub not-found error.

**Options:**

| Option                | Description                                                                                                                                         | Default |
| :-------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- | :------ |
| `--scope <scope>`     | Where to declare the marketplace: `user`, `project`, or `local`. See [Plugin installation scopes](/docs/en/plugins-reference#plugin-installation-scopes) | `user`  |
| `--sparse <paths...>` | Limit checkout to specific directories via git sparse-checkout. Useful for monorepos                                                                |         |

Add a marketplace from GitHub using `owner/repo` shorthand:

```bash theme={null}
claude plugin marketplace add acme-corp/claude-plugins
```

Pin to a specific branch or tag with `@ref`:

```bash theme={null}
claude plugin marketplace add acme-corp/claude-plugins@v2.0
```

Add from a git URL on a non-GitHub host:

```bash theme={null}
claude plugin marketplace add https://gitlab.example.com/team/plugins.git
```

Add from a remote URL that serves the `marketplace.json` file directly:

```bash theme={null}
claude plugin marketplace add https://example.com/marketplace.json
```

Add from a local directory for testing:

```bash theme={null}
claude plugin marketplace add ./my-marketplace
```

Declare the marketplace at project scope so it is shared with your team via `.claude/settings.json`:

```bash theme={null}
claude plugin marketplace add acme-corp/claude-plugins --scope project
```

For a monorepo, limit the checkout to the directories that contain plugin content:

```bash theme={null}
claude plugin marketplace add acme-corp/monorepo --sparse .claude-plugin plugins
```

### Plugin marketplace list

List all configured marketplaces.

```bash theme={null}
claude plugin marketplace list [options]
```

**Options:**

| Option   | Description    |
| :------- | :------------- |
| `--json` | Output as JSON |

With `--json`, each entry includes `name`, `source`, an `installLocation` field with the local cache path where the marketplace is stored, and source-specific fields: `repo` for GitHub sources, `url` for git and URL sources, and `path` for local sources. GitHub and git sources also include a `ref` field when the marketplace was added with a pinned branch or tag.

### Plugin marketplace remove

Remove a configured marketplace. The alias `rm` is also accepted.

```bash theme={null}
claude plugin marketplace remove <name> [options]
```

**Arguments:**

* `<name>`: marketplace name to remove, as shown by `claude plugin marketplace list`. This is the `name` from `marketplace.json`, not the source you passed to `add`

**Options:**

| Option            | Description                                                                                                                                                                                                                                                                                                                                                                                                        | Default      |
| :---------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------- |
| `--scope <scope>` | Restrict removal to a single settings scope: `user`, `project`, or `local`. See [Plugin installation scopes](/docs/en/plugins-reference#plugin-installation-scopes). When omitted, the declaration is removed from every editable scope. When given, only that scope's declaration is removed; the shared state, cache, and installed plugin data are preserved when the marketplace is still declared in another scope | (all scopes) |

<Warning>
  Removing a marketplace from its last remaining scope also uninstalls any plugins you installed from it. To refresh a marketplace without losing installed plugins, use `claude plugin marketplace update` instead.
</Warning>

### Plugin marketplace update

Refresh marketplaces from their sources to retrieve new plugins and version changes. A marketplace added with a branch or tag `ref` updates to the latest commit of that ref, not the repository's default branch.

```bash theme={null}
claude plugin marketplace update [name]
```

**Arguments:**

* `[name]`: marketplace name to update, as shown by `claude plugin marketplace list`. Updates all marketplaces if omitted

Both `remove` and `update` fail when run against a seed-managed marketplace, which is read-only. When updating all marketplaces, seed-managed entries are skipped and other marketplaces still update. To change seed-provided plugins, ask your administrator to update the seed image. See [Pre-populate plugins for containers](#pre-populate-plugins-for-containers).

## Troubleshooting

### Marketplace not loading

**Symptoms**: Can't add marketplace or see plugins from it

**Solutions**:

* Verify the marketplace URL is accessible
* Check that `.claude-plugin/marketplace.json` exists at the specified path
* Ensure JSON syntax is valid using `claude plugin validate .` or `/plugin validate .` from the marketplace directory. To check skill, agent, and command frontmatter, see [Validate a plugin or a directory without a manifest](#validate-a-plugin-or-a-directory-without-a-manifest)
* For private repositories, confirm you have access permissions

### Marketplace validation errors

Run `claude plugin validate .` or `/plugin validate .` from your marketplace directory to check for issues. When pointed at a marketplace directory, the validator checks `marketplace.json` for schema errors, duplicate plugin names, and source path traversal. For each entry whose `source` is a local path, it also validates that plugin's own `plugin.json` and warns when the entry's `version` doesn't match the one in `plugin.json`. Problems found in a plugin's `plugin.json` are prefixed with the entry index, in the form `plugins[2] plugin.json →`.

As of Claude Code v2.1.196, the per-entry pass also:

* includes plugins whose `source` is `.`
* runs when `marketplace.json` is outside a `.claude-plugin` directory, resolving sources against the file's own directory
* reports each entry's problems even when another part of the file has schema errors

Earlier versions skip plugins at the marketplace root and only descend from a `.claude-plugin/marketplace.json`.

From a marketplace directory, Claude Code doesn't open the plugins' skill, agent, command, or hook files. To find errors in those files, see [Validate a plugin or a directory without a manifest](#validate-a-plugin-or-a-directory-without-a-manifest). The table below lists the most common errors from a marketplace directory, with the cause and fix for each:

| Error                                                                                                    | Cause                                                                                                                               | Solution                                                                                                                                                          |
| :------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `No manifest found in directory. Expected .claude-plugin/marketplace.json or .claude-plugin/plugin.json` | The directory you named has no `.claude-plugin/marketplace.json` or `plugin.json`, and no skill, agent, or command files to check   | Run from the marketplace root, or create `.claude-plugin/marketplace.json` with the required fields                                                               |
| `Invalid JSON syntax: Unexpected token...`                                                               | JSON syntax error in marketplace.json                                                                                               | Check for missing commas, extra commas, or unquoted strings                                                                                                       |
| `Duplicate plugin name "x" found in marketplace`                                                         | Two plugins share the same name                                                                                                     | Give each plugin a unique `name` value                                                                                                                            |
| `plugins[0].source: Path contains ".."`                                                                  | Source path contains `..`                                                                                                           | Use paths relative to the marketplace root without `..`. See [Relative paths](#relative-paths)                                                                    |
| `Marketplace name cannot contain control or bidirectional-formatting characters`                         | The marketplace `name` contains a Unicode bidirectional-formatting character or a control character, such as an escape or a newline | Remove the character from the name. Before v2.1.247, these characters produced the `Marketplace name impersonates an official Anthropic/Claude marketplace` error |
| `Plugin name cannot contain control or bidirectional-formatting characters`                              | A plugin `name` contains a Unicode bidirectional-formatting character or a control character, such as an escape or a newline        | Remove the character from the name. Before v2.1.247, Claude Code didn't run this check                                                                            |

**Warnings** (non-blocking):

* `Marketplace has no plugins defined`: add at least one plugin to the `plugins` array
* `No marketplace description provided`: add a top-level `description` to help users understand your marketplace
* `Plugin name "x" is not kebab-case`: rename to lowercase letters, digits, and hyphens only (for example, `my-plugin`). Claude Code accepts other forms, but the claude.ai marketplace sync rejects them.
* `Marketplace name "x" is reserved in Claude Desktop`: the marketplace is named `org`, `org-provisioned`, or `unknown`, in any casing. Claude Code accepts these names, but Claude Desktop's managed marketplace sync rejects the whole marketplace. Rename the marketplace. Before v2.1.221, `claude plugin validate` didn't run this check.
* `Marketplace name "x" is not accepted by Claude Desktop` or `Plugin name "x" is not accepted by Claude Desktop`: Claude Desktop accepts names of up to 128 characters made of letters, digits, `.`, `_`, and `-`, starting with a letter or digit. Claude Code accepts other forms, but Claude Desktop's managed marketplace sync rejects a marketplace whose name fails the check and silently drops a plugin entry whose name does. Rename the marketplace or plugin. Before v2.1.221, `claude plugin validate` didn't run these checks.

#### Validate a plugin or a directory without a manifest

To find skill, agent, and command files whose frontmatter doesn't parse, run `claude plugin validate` and name the directory that holds them. Claude Code doesn't look outside the directory you name. Every run except one against a plugin that has a `plugin.json` requires Claude Code v2.1.233 or later.

##### Pick the directory to name

Claude Code checks different files depending on which directory you name. Find what you want to check in the first column, and run that row's command:

| To check                                                                                     | Run                                                                                             | Claude Code checks                                                                                                                                                       |
| :------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A plugin that has a `plugin.json`                                                            | `claude plugin validate ./plugins/my-plugin`                                                    | `plugin.json`, `hooks/hooks.json`, and the `skills`, `agents`, and `commands` directories at the plugin root                                                             |
| One directory of skills, agents, or commands, such as a plugin that has no `plugin.json` yet | `claude plugin validate .claude/skills`, `~/.claude/agents`, or `./my-plugin/agents`            | Every skill, agent, or command file in that directory                                                                                                                    |
| A folder whose skill is its root `SKILL.md`                                                  | `claude plugin validate ./skills`, naming the `skills` directory that holds the folder          | Each folder's root `SKILL.md`. The holding directory must be named `skills`; a folder under another name, such as `plugins/`, has no run that checks its root `SKILL.md` |
| A project's three directories at once                                                        | `claude plugin validate .claude`, or the project root when it has no `.claude-plugin/` manifest | `.claude/skills`, `.claude/agents`, and `.claude/commands`                                                                                                               |
| Your user-level directories                                                                  | `claude plugin validate ~/.claude`                                                              | `~/.claude/skills`, `~/.claude/agents`, and `~/.claude/commands`                                                                                                         |

##### Check a plugin whose skill is its root `SKILL.md`

When you run `claude plugin validate` against a plugin directory, Claude Code doesn't check a `SKILL.md` at the plugin root. When the plugin sits in a directory named `skills`, run the command twice:

* Name that `skills` directory to check the plugin's root `SKILL.md`.
* Name the plugin directory to check the rest.

When the plugin sits under another name, such as `plugins/`, the `skills`-directory run isn't available, and no run checks its root `SKILL.md`.

##### Check files behind symlinks

When you run `claude plugin validate`, Claude Code doesn't follow symlinks inside the directory you name. What it does depends on where the link is:

* **A linked `skills`, `agents`, or `commands` directory under the plugin or `.claude` root**: Claude Code warns that nothing in it was read.
* **A linked entry inside a `skills`, `agents`, or `commands` directory**: Claude Code skips it and warns, per directory, how many entries it skipped that a session would load.
* **The `skills`, `agents`, or `commands` directory you name is itself a symlink, or its parent `.claude` directory is**: Claude Code reports an error and checks nothing in it. Name the real directory instead.

In two skills cases, the run passes with warnings. To check the linked files, run again and name a directory that holds them directly:

* **A plugin whose `skills` directory [links to a sibling plugin's skills](/docs/en/plugins-reference#share-files-within-a-marketplace-with-symlinks)**: name the sibling plugin's directory.
* **A [symlinked skill entry](/docs/en/skills#where-skills-live) in `~/.claude/skills` or `.claude/skills`**: Claude Code follows the entry in a session. To check it, name a directory called `skills` that holds the real folder.

##### Read the validation results

A clean run ends with `Validation passed`.

`No manifest found in directory` means Claude Code found no `plugin.json` or `marketplace.json` there, and no skill, agent, or command file in the directories it probes under it. Name the `skills`, `agents`, or `commands` directory that holds your files instead.

Two of the errors Claude Code reports from these runs, with the fix for each:

* `YAML frontmatter failed to parse: ...`: fix the YAML in the frontmatter block of the skill, agent, or command file. Until you do, a session reads no frontmatter fields from the file
* `Invalid JSON syntax: ...` on `hooks/hooks.json`: fix the JSON syntax. Until you do, a session loads the plugin without the hooks in that file. Claude Code reports this error only in a plugin run

In a plugin run, Claude Code also warns about a `CLAUDE.md` at the plugin root. For paths you set through the [component path fields](/docs/en/plugins-reference#component-path-fields) in `plugin.json`, Claude Code checks that each path exists but doesn't read the files there.

### Plugin installation failures

**Symptoms**: Marketplace appears but plugin installation fails

**Solutions**:

* Verify plugin source URLs are accessible
* Check that plugin directories contain required files
* For GitHub sources, ensure repositories are public or you have access
* Test plugin sources manually by cloning/downloading
* If the source pins both `ref` and `sha`, a deleted upstream branch or tag doesn't block installation on most git hosts, including GitHub, GitLab, and Bitbucket. On servers that don't support fetching commits by SHA, such as AWS CodeCommit, the `ref` must still exist and the pinned commit must be reachable from it. If the install still fails, confirm the pinned commit still exists in the repository

### Private repository authentication fails

**Symptoms**: Authentication errors when installing plugins from private repositories

**Solutions**:

For manual installation and updates:

* Verify you're authenticated with your git provider (for example, run `gh auth status` for GitHub)
* Check that your credential helper is configured: `git config --global credential.helper`
* Run `git ls-remote <marketplace-url>` to test whether git can authenticate on its own. If git asks for a username or password, store the credential first: for GitHub over HTTPS, run `gh auth setup-git`, and for SSH remotes, load your key into `ssh-agent`

For background auto-updates:

* By default, background refreshes disable git credential helpers for the pull, so the pull can't authenticate over HTTPS. SSH remotes with a key loaded in `ssh-agent` still authenticate. A failed pull triggers a re-clone from scratch, which uses your stored credentials but may time out on large repositories
* Set `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1` to keep the existing clone when the background pull fails
* Configure a git credential helper, for example `gh auth setup-git`, so the re-clone fallback can authenticate
* If the re-clone times out on a large repository, increase the limit with [`CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`](#git-operations-time-out)
* Configure a [git URL rewrite](#private-repositories) scoped to the marketplace repository so the background pull authenticates directly
* Or update private marketplaces manually with `/plugin marketplace update <name>`, which uses your credentials

### Marketplace updates fail in offline environments

**Symptoms**: Marketplace `git pull` fails in the background and Claude Code repeatedly attempts a re-clone that can't succeed.

**Cause**: By default, when a `git pull` fails, Claude Code attempts a re-clone from scratch. In offline or airgapped environments, re-cloning fails the same way, and the restore of the previous cache afterward is best-effort. The refresh runs in the background after startup, so it doesn't delay startup, but each session repeats the failed attempts and each git operation can wait out the [120-second timeout](#git-operations-time-out).

**Solution**: Set `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1` to skip the re-clone attempt and keep using the existing cache when the pull fails:

```bash theme={null}
export CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1
```

For fully offline deployments where the repository will never be reachable, use [`CLAUDE_CODE_PLUGIN_SEED_DIR`](#pre-populate-plugins-for-containers) to pre-populate the plugins directory at build time instead.

### Git operations time out

**Symptoms**: Plugin installation or marketplace updates fail with a timeout error like "Git clone timed out after 120s" or "Git pull timed out after 120s".

**Cause**: Claude Code uses a 120-second timeout for all git operations, including cloning plugin repositories and pulling marketplace updates. Large repositories or slow network connections may exceed this limit.

**Solution**: Increase the timeout using the `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` environment variable. The value is in milliseconds:

```bash theme={null}
export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000  # 5 minutes
```

### Plugins with relative paths fail in URL-based marketplaces

**Symptoms**: Added a marketplace via URL (such as `https://example.com/marketplace.json`), but plugins with relative path sources like `"./plugins/my-plugin"` fail to install with "path not found" errors.

**Cause**: adding a URL-based marketplace downloads only the `marketplace.json` file itself, and Claude Code doesn't fetch plugin files by relative path from that server. Relative paths in the marketplace entry reference files on the remote server that were not downloaded.

**Solutions**:

* **Use external sources**: change plugin entries to any [plugin source](#plugin-sources) other than a relative path:
  ```json theme={null}
  { "name": "my-plugin", "source": { "source": "github", "repo": "owner/repo" } }
  ```
* **Use a Git-based marketplace**: Host your marketplace in a Git repository and add it with the git URL. Git-based marketplaces clone the entire repository, making relative paths work correctly.

### Files not found after installation

**Symptoms**: Plugin installs but references to files fail, especially files outside the plugin directory

**Cause**: Plugins are copied to a cache directory rather than used in place, except for a [`command` source in link mode](#copy-mode-and-link-mode). Paths that reference files outside a copied plugin's directory (such as `../shared-utils`) won't work because those files aren't copied.

**Solutions**: See [Plugin caching and file resolution](/docs/en/plugins-reference#plugin-caching-and-file-resolution) for workarounds including symlinks and directory restructuring.

For additional debugging tools and common issues, see [Debugging and development tools](/docs/en/plugins-reference#debugging-and-development-tools).

## See also

* [Discover and install prebuilt plugins](/docs/en/discover-plugins) - Installing plugins from existing marketplaces
* [Plugins](/docs/en/plugins) - Creating your own plugins
* [Plugins reference](/docs/en/plugins-reference) - Complete technical specifications and schemas
* [Plugin settings](/docs/en/settings-reference#plugin-settings) - Plugin configuration options
* [strictKnownMarketplaces reference](/docs/en/settings-reference#strictknownmarketplaces) - Managed marketplace restrictions
