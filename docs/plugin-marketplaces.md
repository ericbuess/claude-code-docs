> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Create and distribute a plugin marketplace

> Build and host plugin marketplaces to distribute Claude Code extensions across teams and communities.

A **plugin marketplace** is a catalog that lets you distribute plugins to others. Marketplaces provide centralized discovery, version tracking, automatic updates, and support for multiple source types, including git repositories and local paths. This guide shows you how to create your own marketplace to share plugins with your team or community.

Looking to install plugins from an existing marketplace? See [Discover and install prebuilt plugins](/en/discover-plugins).

## Overview

Creating and distributing a marketplace involves:

1. **Create plugins**: build one or more plugins with skills, agents, hooks, MCP servers, or LSP servers. This guide assumes you already have plugins to distribute; see [Create plugins](/en/plugins) for details on how to create them.
2. **Create the marketplace file**: define a `marketplace.json` that lists your plugins and where to find them. See [Create the marketplace file](#create-the-marketplace-file).
3. **Host the marketplace**: push to GitHub, GitLab, or another git host. See [Host and distribute marketplaces](#host-and-distribute-marketplaces).
4. **Share with users**: users add your marketplace with `/plugin marketplace add` and install individual plugins. See [Discover and install plugins](/en/discover-plugins).

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
      "version": "1.0.0"
    }
    ```

    <Note>
      Setting `version` means users only receive updates when you change this field, so bump it on every release. If you omit `version` and host this marketplace in git, every commit automatically counts as a new version. See [Version resolution](#version-resolution-and-release-channels) to choose the right approach.
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
    Add the marketplace and install the plugin.

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

To learn more about what plugins can do, including hooks, agents, MCP servers, and LSP servers, see [Plugins](/en/plugins).

<Note>
  **How plugins are installed**: when users install a plugin, Claude Code copies the plugin directory to a cache location. This means plugins can't reference files outside their directory using paths like `../shared-utils`, because those files won't be copied.

  If you need to share files across plugins, use symlinks. See [Plugin caching and file resolution](/en/plugins-reference#plugin-caching-and-file-resolution) for details.
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

| Field     | Type   | Description                                                                                                                                                                                                                                                                                                                                                                                                                           | Example        |
| :-------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------- |
| `name`    | string | Marketplace identifier (kebab-case, no spaces). This is public-facing: users see it when installing plugins (for example, `/plugin install my-tool@your-marketplace`). Each user can register only one marketplace per name: adding a second marketplace with the same name replaces the first. To publish multiple plugins under one marketplace name, list them all in a [single `marketplace.json`](#create-the-marketplace-file). | `"acme-tools"` |
| `owner`   | object | Marketplace maintainer information ([see fields below](#owner-fields))                                                                                                                                                                                                                                                                                                                                                                |                |
| `plugins` | array  | List of available plugins                                                                                                                                                                                                                                                                                                                                                                                                             | See below      |

<Note>
  **Reserved names**: the following marketplace names are reserved for official Anthropic use and can't be used by third-party marketplaces: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `claude-plugins-community`, `claude-community`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `anthropic-agent-skills`, `knowledge-work-plugins`, `life-sciences`, `claude-for-legal`, `claude-for-financial-services`, `financial-services-plugins`, `first-party-plugins`, `healthcare`. Names that impersonate official marketplaces, such as `official-claude-plugins` or `anthropic-plugins-v2`, are also blocked. Reserving these names prevents a third-party marketplace from presenting itself as an Anthropic-published source.

  Claude Code re-checks reserved names every time it loads a marketplace, not only when you add one. A marketplace that was registered under one of these names before the name became reserved stops loading and reports that it is [registered from an untrusted source](/en/errors#marketplace-is-registered-from-an-untrusted-source). Remove that marketplace and re-add it from the official Anthropic source. A third-party marketplace affected by a newly reserved name loads again as soon as you re-add it under a different name. Before v2.1.205, `first-party-plugins` and `healthcare` weren't reserved, and a marketplace already registered under a reserved name kept loading.
</Note>

### Owner fields

| Field   | Type   | Required | Description                      |
| :------ | :----- | :------- | :------------------------------- |
| `name`  | string | Yes      | Name of the maintainer or team   |
| `email` | string | No       | Contact email for the maintainer |

### Optional fields

| Field                                 | Type   | Description                                                                                                                                                                                                                                                                                                              |
| :------------------------------------ | :----- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$schema`                             | string | JSON Schema URL for editor autocomplete and validation. Claude Code ignores this field at load time.                                                                                                                                                                                                                     |
| `description`                         | string | Brief marketplace description                                                                                                                                                                                                                                                                                            |
| `version`                             | string | Marketplace manifest version                                                                                                                                                                                                                                                                                             |
| `metadata.pluginRoot`                 | string | Base directory prepended to relative plugin source paths (for example, `"./plugins"` lets you write `"source": "formatter"` instead of `"source": "./plugins/formatter"`)                                                                                                                                                |
| `allowCrossMarketplaceDependenciesOn` | array  | Other marketplaces that plugins in this marketplace may depend on. Dependencies from a marketplace not listed here are blocked at install. See [Depend on a plugin from another marketplace](/en/plugin-dependencies#depend-on-a-plugin-from-another-marketplace).                                                       |
| `renames`                             | object | {/* min-version: 2.1.193 */}Map from a former plugin `name` to its current name, or to `null` if the plugin was removed. Lets existing users migrate automatically when you rename or remove an entry in `plugins`. See [Rename or remove a plugin](#rename-or-remove-a-plugin). Requires Claude Code v2.1.193 or later. |

`description` and `version` are also accepted under `metadata` for backward compatibility.

## Plugin entries

Each plugin entry in the `plugins` array describes a plugin and where to find it. You can include any field from the [plugin manifest schema](/en/plugins-reference#plugin-manifest-schema), such as `description`, `version`, `author`, `commands`, and `hooks`, plus these marketplace-specific fields: `source`, `category`, `tags`, `strict`, and `relevance`.

### Required fields

| Field    | Type           | Description                                                                                                                                            |
| :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`   | string         | Plugin identifier (kebab-case, no spaces). This is public-facing: users see it when installing (for example, `/plugin install my-plugin@marketplace`). |
| `source` | string\|object | Where to fetch the plugin from (see [Plugin sources](#plugin-sources) below)                                                                           |

### Optional plugin fields

**Standard metadata fields:**

| Field            | Type    | Description                                                                                                                                                                                                                                                                                                                                    |
| :--------------- | :------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `displayName`    | string  | {/* min-version: 2.1.143 */}Human-readable name shown in UI surfaces. Falls back to `name` when omitted. May contain spaces and any casing. Not used for namespacing or lookup. Requires Claude Code v2.1.143 or later.                                                                                                                        |
| `description`    | string  | Brief plugin description                                                                                                                                                                                                                                                                                                                       |
| `version`        | string  | Plugin version. If set (here or in `plugin.json`), the plugin is pinned to this string and users only receive updates when it changes. Omit to fall back to the git commit SHA. See [Version resolution](#version-resolution-and-release-channels).                                                                                            |
| `author`         | object  | Plugin author information (`name` required, `email` optional)                                                                                                                                                                                                                                                                                  |
| `homepage`       | string  | Plugin homepage or documentation URL                                                                                                                                                                                                                                                                                                           |
| `repository`     | string  | Source code repository URL                                                                                                                                                                                                                                                                                                                     |
| `license`        | string  | SPDX license identifier (for example, MIT, Apache-2.0)                                                                                                                                                                                                                                                                                         |
| `keywords`       | array   | Tags for plugin discovery and categorization                                                                                                                                                                                                                                                                                                   |
| `category`       | string  | Plugin category for organization                                                                                                                                                                                                                                                                                                               |
| `tags`           | array   | Tags for searchability                                                                                                                                                                                                                                                                                                                         |
| `strict`         | boolean | Controls whether `plugin.json` is the authority for component definitions (default: true). See [Strict mode](#strict-mode) below.                                                                                                                                                                                                              |
| `relevance`      | object  | {/* min-version: 2.1.152 */}Signals that tell Claude Code when to suggest this plugin to users. Takes effect only for marketplaces an administrator allowlists in managed settings. See [Recommend plugins for your org](/en/plugin-relevance). Requires Claude Code v2.1.152 or later.                                                        |
| `defaultEnabled` | boolean | {/* min-version: 2.1.154 */}Whether the plugin is enabled after install (default: true). Set to `false` to install the plugin disabled until the user opts in. Takes precedence over the same field in the plugin's `plugin.json`. See [Default enablement](/en/plugins-reference#default-enablement). Requires Claude Code v2.1.154 or later. |

**Component configuration fields:**

| Field        | Type           | Description                                                    |
| :----------- | :------------- | :------------------------------------------------------------- |
| `skills`     | string\|array  | Custom paths to skill directories containing `<name>/SKILL.md` |
| `commands`   | string\|array  | Custom paths to flat `.md` skill files or directories          |
| `agents`     | string\|array  | Custom paths to agent files                                    |
| `hooks`      | string\|object | Custom hooks configuration or path to hooks file               |
| `mcpServers` | string\|object | MCP server configurations or path to MCP config                |
| `lspServers` | string\|object | LSP server configurations or path to LSP config                |

## Plugin sources

Plugin sources tell Claude Code where to fetch each individual plugin listed in your marketplace. These are set in the `source` field of each plugin entry in `marketplace.json`.

After Claude Code clones or downloads a plugin to the local machine, it copies the plugin into the local versioned plugin cache at `~/.claude/plugins/cache`.

| Source        | Type                            | Fields                             | Notes                                                                                                                                             |
| ------------- | ------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Relative path | `string` (e.g. `"./my-plugin"`) | none                               | Local directory within the marketplace repo. Must start with `./`. Resolved relative to the marketplace root, not the `.claude-plugin/` directory |
| `github`      | object                          | `repo`, `ref?`, `sha?`             |                                                                                                                                                   |
| `url`         | object                          | `url`, `ref?`, `sha?`              | Git URL source                                                                                                                                    |
| `git-subdir`  | object                          | `url`, `path`, `ref?`, `sha?`      | Subdirectory within a git repo. Clones sparsely to minimize bandwidth for monorepos                                                               |
| `npm`         | object                          | `package`, `version?`, `registry?` | Installed via `npm install`                                                                                                                       |

<Note>
  **Marketplace sources vs plugin sources**: These are different concepts that control different things.

  * **Marketplace source**: where to fetch the `marketplace.json` catalog itself. Set when users run `/plugin marketplace add` or in `extraKnownMarketplaces` settings. Supports `ref` (branch/tag) but not `sha`.
  * **Plugin source**: where to fetch an individual plugin listed in the marketplace. Set in the `source` field of each plugin entry inside `marketplace.json`. Supports both `ref` (branch/tag) and `sha` (exact commit).

  For example, a marketplace hosted at `acme-corp/plugin-catalog` (marketplace source) can list a plugin fetched from `acme-corp/code-formatter` (plugin source). The marketplace source and plugin source point to different repositories and are pinned independently.
</Note>

The git-based source types below are `github`, `url`, and `git-subdir`. When both `ref` and `sha` are set on any of them, the `sha` is the effective pin. Claude Code fetches and checks out the pinned commit directly.

On most git hosts, including GitHub, GitLab, and Bitbucket, this means installation succeeds even if the branch or tag named by `ref` has since been deleted upstream, as long as the commit is still reachable from the repository. Some servers, such as AWS CodeCommit, don't support fetching commits by SHA. On those servers the `ref` must still exist and the pinned commit must be reachable from it.

### Relative paths

For plugins in the same repository, use a path starting with `./`:

```json theme={null}
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

Paths resolve relative to the marketplace root, which is the directory containing `.claude-plugin/`. In the example above, `./plugins/my-plugin` points to `<repo>/plugins/my-plugin`, even though `marketplace.json` lives at `<repo>/.claude-plugin/marketplace.json`. Don't use `../` to reference paths outside the marketplace root.

<Note>
  Relative paths resolve against a local copy of the marketplace, so they work when users add your marketplace from a git source or a local directory. If users add your marketplace via a direct URL to the `marketplace.json` file, relative paths won't resolve, because only that file is downloaded. For URL-based distribution, use GitHub, npm, or git URL sources instead. See [Troubleshooting](#plugins-with-relative-paths-fail-in-url-based-marketplaces) for details.
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
* **`${CLAUDE_PLUGIN_ROOT}`**: use this variable in hooks and MCP server configs to reference files within the plugin's installation directory. This is necessary because plugins are copied to a cache location when installed. For dependencies or state that should survive plugin updates, use [`${CLAUDE_PLUGIN_DATA}`](/en/plugins-reference#persistent-data-directory) instead.
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

Claude Code supports installing plugins from private repositories. For manual installation and updates, Claude Code uses your existing git credential helpers, so HTTPS access via `gh auth login`, macOS Keychain, or `git-credential-store` works the same as in your terminal. SSH access works as long as the host is already in your `known_hosts` file and the key is loaded in `ssh-agent`, since Claude Code suppresses interactive SSH prompts for the host fingerprint and key passphrase.

Background auto-updates work differently. By default, the background refresh disables git credential helpers for its `git pull`, so the pull can't authenticate to private repositories over HTTPS even when a helper is configured. SSH remotes aren't affected: a key loaded in `ssh-agent` authenticates background pulls the same way as manual operations. When the background pull fails, Claude Code falls back to re-cloning the marketplace from scratch. The re-clone does use your stored git credentials, but it can [time out on large repositories](#git-operations-time-out), so private-marketplace auto-updates may fail intermittently.

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

### Test locally before distribution

Test your marketplace locally before sharing:

```shell theme={null}
/plugin marketplace add ./my-marketplace
/plugin install quality-review-plugin@my-plugins
```

For the full range of add commands (GitHub, Git URLs, local paths, remote URLs), see [Add marketplaces](/en/discover-plugins#add-marketplaces).

### Require marketplaces for your team

You can configure your repository so team members are automatically prompted to install your marketplace when they trust the project folder. Add your marketplace to `.claude/settings.json`:

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

For full configuration options, see [Plugin settings](/en/settings#plugin-settings).

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

For organizations requiring strict control over plugin sources, administrators can restrict which plugin marketplaces users are allowed to add using the [`strictKnownMarketplaces`](/en/settings#strictknownmarketplaces) setting in managed settings. To also reject the CLI flags that sideload plugins, agents, and MCP servers for a single run, pair it with [`disableSideloadFlags`](/en/settings#available-settings).

When `strictKnownMarketplaces` is configured in managed settings, the restriction behavior depends on the value:

| Value               | Behavior                                                         |
| ------------------- | ---------------------------------------------------------------- |
| Undefined (default) | No restrictions. Users can add any marketplace                   |
| Empty array `[]`    | Complete lockdown. Users can't add any new marketplaces          |
| List of sources     | Users can only add marketplaces that match the allowlist exactly |

#### Common configurations

Disable all marketplace additions:

```json theme={null}
{
  "strictKnownMarketplaces": []
}
```

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

Allow all marketplaces from an internal git server using regex pattern matching on the host. This is the recommended approach for [GitHub Enterprise Server](/en/github-enterprise-server#plugin-marketplaces-on-ghes) or self-hosted GitLab instances:

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
  `strictKnownMarketplaces` restricts what users can add, but doesn't register marketplaces on its own. To make allowed marketplaces available automatically without users running `/plugin marketplace add`, pair it with [`extraKnownMarketplaces`](/en/settings#extraknownmarketplaces) in the same `managed-settings.json`. See [Using both together](/en/settings#strictknownmarketplaces).
</Note>

#### How restrictions work

Restrictions are checked before any network or filesystem operation. The check runs on marketplace add and on plugin install, update, refresh, and auto-update. If a marketplace was added before the policy was configured and its source no longer matches the allowlist, Claude Code refuses to install or update plugins from it. The same enforcement applies to `blockedMarketplaces`.

The allowlist uses exact matching for most source types. For a marketplace to be allowed, all specified fields must match exactly:

* For GitHub sources: `repo` is required, and `ref` or `path` must also match if specified in the allowlist
* For URL sources: the full URL must match exactly
* For `hostPattern` sources: the marketplace host is matched against the regex pattern
* For `pathPattern` sources: the marketplace's filesystem path is matched against the regex pattern

Exact matching doesn't normalize URLs: a trailing slash, `.git` suffix, or `ssh://` versus `https://` form are treated as different values. If your organization's marketplace can be cloned by more than one URL form, prefer a `hostPattern` entry over a literal URL so all forms match.

Because `strictKnownMarketplaces` is set in [managed settings](/en/settings#settings-files), individual users and project configurations can't override these restrictions.

For complete configuration details including all supported source types and comparison with `extraKnownMarketplaces`, see the [strictKnownMarketplaces reference](/en/settings#strictknownmarketplaces).

### Version resolution and release channels

Plugin versions determine cache paths and update detection: if the resolved version matches what a user already has, `/plugin update` and auto-update skip the plugin.

Claude Code resolves a plugin's version from the first of these that is set:

1. `version` in the plugin's `plugin.json`
2. `version` in the plugin's marketplace entry
3. The git commit SHA of the plugin's source

For the git-based source types `github`, `url`, `git-subdir`, and relative paths inside a git-hosted marketplace, you can omit `version` entirely and every new commit is treated as a new version. This is the simplest setup for internal or actively-developed plugins.

<Warning>
  Setting `version` pins the plugin. If `plugin.json` declares `"version": "1.0.0"`, pushing new commits without changing that string does nothing for existing users, because Claude Code sees the same version and keeps the cached copy. Bump the field on every release, or omit it to use the commit SHA.

  Avoid setting `version` in both `plugin.json` and the marketplace entry. Claude Code always uses the `plugin.json` value without warning, so a stale manifest version can mask a version you set in `marketplace.json`.
</Warning>

#### Set up release channels

To support "stable" and "latest" release channels for your plugins, you can set up two marketplaces that point to different refs or SHAs of the same repo. You can then assign the two marketplaces to different user groups through [managed settings](/en/settings#settings-files).

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

Assign each marketplace to the appropriate user group through managed settings. For example, the stable group receives:

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

A plugin can constrain its dependencies to a semver range so that updates to a dependency don't break the dependent plugin. See [Constrain plugin dependency versions](/en/plugin-dependencies) for the `{plugin-name}--v{version}` git-tag convention, range syntax, and how multiple constraints on the same dependency are combined.

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

Validate your marketplace JSON syntax:

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

For complete plugin testing workflows, see [Test your plugins locally](/en/plugins#test-your-plugins-locally). For technical troubleshooting, see [Plugins reference](/en/plugins-reference).

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
| `--scope <scope>`     | Where to declare the marketplace: `user`, `project`, or `local`. See [Plugin installation scopes](/en/plugins-reference#plugin-installation-scopes) | `user`  |
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

With `--json`, each entry includes `name`, `source`, and source-specific fields: `repo` for GitHub sources, `url` for git and URL sources, and `path` for local sources. GitHub and git sources also include a `ref` field when the marketplace was added with a pinned branch or tag.

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
| `--scope <scope>` | Restrict removal to a single settings scope: `user`, `project`, or `local`. See [Plugin installation scopes](/en/plugins-reference#plugin-installation-scopes). When omitted, the declaration is removed from every editable scope. When given, only that scope's declaration is removed; the shared state, cache, and installed plugin data are preserved when the marketplace is still declared in another scope | (all scopes) |

<Warning>
  Removing a marketplace from its last remaining scope also uninstalls any plugins you installed from it. To refresh a marketplace without losing installed plugins, use `claude plugin marketplace update` instead.
</Warning>

### Plugin marketplace update

Refresh marketplaces from their sources to retrieve new plugins and version changes.

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
* Ensure JSON syntax is valid using `claude plugin validate` or `/plugin validate`. To check skill, agent, and command frontmatter, run the command against each plugin directory
* For private repositories, confirm you have access permissions

### Marketplace validation errors

Run `claude plugin validate .` or `/plugin validate .` from your marketplace directory to check for issues. When pointed at a marketplace directory, the validator checks `marketplace.json` for schema errors, duplicate plugin names, and source path traversal. For each entry whose `source` is a local path, it also validates that plugin's own `plugin.json` and warns when the entry's `version` doesn't match the one in `plugin.json`. Problems found in a plugin's `plugin.json` are prefixed with the entry index, in the form `plugins[2] plugin.json →`.

As of Claude Code v2.1.196, the per-entry pass also:

* includes plugins whose `source` is `.`
* runs when `marketplace.json` is outside a `.claude-plugin` directory, resolving sources against the file's own directory
* reports each entry's problems even when another part of the file has schema errors

Earlier versions skip plugins at the marketplace root and only descend from a `.claude-plugin/marketplace.json`.

To validate an individual plugin's `plugin.json` and its skill, agent, command, and hook files, run the command against the plugin directory itself, for example `claude plugin validate ./plugins/my-plugin`. Common errors:

| Error                                             | Cause                                           | Solution                                                                                                                                    |
| :------------------------------------------------ | :---------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `File not found: .claude-plugin/marketplace.json` | Missing manifest                                | Create `.claude-plugin/marketplace.json` with required fields                                                                               |
| `Invalid JSON syntax: Unexpected token...`        | JSON syntax error in marketplace.json           | Check for missing commas, extra commas, or unquoted strings                                                                                 |
| `Duplicate plugin name "x" found in marketplace`  | Two plugins share the same name                 | Give each plugin a unique `name` value                                                                                                      |
| `plugins[0].source: Path contains ".."`           | Source path contains `..`                       | Use paths relative to the marketplace root without `..`. See [Relative paths](#relative-paths)                                              |
| `YAML frontmatter failed to parse: ...`           | Invalid YAML in a skill, agent, or command file | Fix the YAML syntax in the frontmatter block. At runtime this file loads with no metadata. Reported only when validating a plugin directory |
| `Invalid JSON syntax: ...` (hooks.json)           | Malformed `hooks/hooks.json`                    | Fix JSON syntax. A malformed `hooks/hooks.json` prevents the entire plugin from loading. Reported only when validating a plugin directory   |

**Warnings** (non-blocking):

* `Marketplace has no plugins defined`: add at least one plugin to the `plugins` array
* `No marketplace description provided`: add a top-level `description` to help users understand your marketplace
* `Plugin name "x" is not kebab-case`: the plugin name contains uppercase letters, spaces, or special characters. Rename to lowercase letters, digits, and hyphens only (for example, `my-plugin`). Claude Code accepts other forms, but the claude.ai marketplace sync rejects them.

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
* Check that your credential helper is configured correctly: `git config --global credential.helper`
* Try cloning the repository manually to verify your credentials work

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

With this variable set, Claude Code retains the stale marketplace clone on `git pull` failure and continues using the last-known-good state. For fully offline deployments where the repository will never be reachable, use [`CLAUDE_CODE_PLUGIN_SEED_DIR`](#pre-populate-plugins-for-containers) to pre-populate the plugins directory at build time instead.

### Git operations time out

**Symptoms**: Plugin installation or marketplace updates fail with a timeout error like "Git clone timed out after 120s" or "Git pull timed out after 120s".

**Cause**: Claude Code uses a 120-second timeout for all git operations, including cloning plugin repositories and pulling marketplace updates. Large repositories or slow network connections may exceed this limit.

**Solution**: Increase the timeout using the `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` environment variable. The value is in milliseconds:

```bash theme={null}
export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000  # 5 minutes
```

### Plugins with relative paths fail in URL-based marketplaces

**Symptoms**: Added a marketplace via URL (such as `https://example.com/marketplace.json`), but plugins with relative path sources like `"./plugins/my-plugin"` fail to install with "path not found" errors.

**Cause**: URL-based marketplaces only download the `marketplace.json` file itself. They don't download plugin files from the server. Relative paths in the marketplace entry reference files on the remote server that were not downloaded.

**Solutions**:

* **Use external sources**: Change plugin entries to use GitHub, npm, or git URL sources instead of relative paths:
  ```json theme={null}
  { "name": "my-plugin", "source": { "source": "github", "repo": "owner/repo" } }
  ```
* **Use a Git-based marketplace**: Host your marketplace in a Git repository and add it with the git URL. Git-based marketplaces clone the entire repository, making relative paths work correctly.

### Files not found after installation

**Symptoms**: Plugin installs but references to files fail, especially files outside the plugin directory

**Cause**: Plugins are copied to a cache directory rather than used in-place. Paths that reference files outside the plugin's directory (such as `../shared-utils`) won't work because those files aren't copied.

**Solutions**: See [Plugin caching and file resolution](/en/plugins-reference#plugin-caching-and-file-resolution) for workarounds including symlinks and directory restructuring.

For additional debugging tools and common issues, see [Debugging and development tools](/en/plugins-reference#debugging-and-development-tools).

## See also

* [Discover and install prebuilt plugins](/en/discover-plugins) - Installing plugins from existing marketplaces
* [Plugins](/en/plugins) - Creating your own plugins
* [Plugins reference](/en/plugins-reference) - Complete technical specifications and schemas
* [Plugin settings](/en/settings#plugin-settings) - Plugin configuration options
* [strictKnownMarketplaces reference](/en/settings#strictknownmarketplaces) - Managed marketplace restrictions
