> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Plugin manifest reference

> Complete reference for plugin.json: every field with its type and default, accepted path forms, and the userConfig and environment variable schemas.

A plugin manifest is the `plugin.json` file in a plugin's `.claude-plugin/` directory. It carries the plugin's metadata and the [`userConfig`](#user-configuration) values that Claude Code prompts the user for. It also declares any component that you define inline or keep outside its [default location](#standard-layout).

This reference is for plugin creators, and for marketplace owners who put component fields in a marketplace entry.

<Note>
  These cases are covered on other pages:

  * **Learning to build a plugin**: start with [Create a plugin](/docs/en/plugins/create)
  * **What each component does at runtime**: see [Plugin components](/docs/en/plugins/components)
</Note>

Start at the section that matches what you're looking up:

* A field: the [Fields table](#fields) gives each field's type, whether it's required, its default, and what it accepts. [Path rules](#path-rules) covers the `./` prefix and containment for every component path
* A `userConfig` option or a `channels` entry: the [User configuration](#user-configuration) and [Channels](#channels) schemas
* `${CLAUDE_PLUGIN_ROOT}` or another variable a plugin can reference: [Environment variables](#environment-variables)
* Where each component's files go: [Standard layout](#standard-layout)
* A message from `claude plugin validate`: the [troubleshooting page](/docs/en/plugins/troubleshooting) lists each message with its fix and links to the relevant sections on this page

## Manifest file

The manifest is optional. Without it, Claude Code loads the components it finds in the [standard layout](#standard-layout). The plugin name then comes from the marketplace entry, or from the directory name when you load the plugin with `--plugin-dir`.

Write a manifest when you want metadata, a component outside its default directory, `userConfig`, or an inline component definition.

Save the manifest at `.claude-plugin/plugin.json` under the plugin root. Put every other plugin file at the plugin root, not inside `.claude-plugin/`. That includes `skills/`, `commands/`, and `hooks/`.

The following example sets most of the keys in the [Fields table](#fields). It passes validation in a plugin directory that contains each referenced path.

```json theme={null}
{
  "name": "deploy-tools",
  "displayName": "Deploy Tools",
  "version": "1.2.0",
  "description": "Deployment commands, a review agent, and a status monitor",
  "author": {
    "name": "Example Team",
    "email": "dev@example.com",
    "url": "https://example.com"
  },
  "homepage": "https://example.com/docs/deploy-tools",
  "repository": "https://github.com/example/deploy-tools",
  "license": "MIT",
  "keywords": ["deployment", "ci"],
  "defaultEnabled": true,
  "dependencies": ["secrets-vault"],
  "metadata": { "catalogId": "cat-123" },
  "skills": ["./extra-skills/"],
  "commands": {
    "status": {
      "source": "./commands/status.md",
      "description": "Show the current deployment status"
    },
    "about": {
      "content": "Explain what the deploy-tools plugin provides.",
      "description": "Describe this plugin"
    }
  },
  "agents": ["./agents/reviewer.md"],
  "hooks": "./config/extra-hooks.json",
  "mcpServers": {
    "deploy-api": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"]
    }
  },
  "lspServers": "./.lsp.json",
  "outputStyles": "./styles/",
  "experimental": {
    "themes": "./themes/",
    "monitors": "./config/monitors.json"
  },
  "userConfig": {
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "Token for the deployment API",
      "sensitive": true
    }
  }
}
```

### Unrecognized fields

An unrecognized top-level key is stripped, and an unrecognized key inside a `userConfig` option, `channels` entry, `lspServers` config, or `monitors` entry is rejected:

* **Top-level fields**: the field is stripped and the plugin loads. `claude plugin validate` reports each unrecognized top-level field as a warning
* **Strict objects**: `userConfig` options, `channels` entries, `lspServers` configs, and `monitors` entries are strict. An unknown key inside one is an error, and the plugin doesn't load

### Validate the manifest

`claude plugin validate` is the authoritative check for a manifest. Run it from your shell against the plugin directory:

```bash theme={null}
claude plugin validate ./my-plugin
```

The command reports one of these results:

* **`Validation passed`**: the manifest loads
* **`Validation passed with warnings`**: the manifest loads, but the validator found something to fix, such as an unknown top-level field that Claude Code strips, a `name` that isn't kebab-case, or a missing `version`, `description`, or `author`. Pass `--strict` to turn warnings into failures in CI
* **`Validation failed`**: the manifest has a type mismatch, a path that is missing or escapes the plugin root, or an unknown key inside a `userConfig` option, `channels` entry, `lspServers` config, or `monitors` entry. Claude Code reports the same problem when it loads the plugin

## Fields

The table lists the top-level keys in `plugin.json`. `name` is the only required key. Where a field name is a link, the linked section has its full rules.

For component keys such as `commands` and `hooks`, [Component path forms](#component-path-forms) shows each accepted shape with an example, and every path follows the [path rules](#path-rules) for the `./` prefix, extensions, and containment.

| Field                                | Type                             | Description                                                                                                                                                                                                                                                                                                      |
| :----------------------------------- | :------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$schema`                            | String                           | JSON Schema URL for editor autocomplete. Claude Code ignores it at load time                                                                                                                                                                                                                                     |
| [`name`](#name)                      | String                           | Plugin identifier, required. Use kebab-case. Every component is namespaced under it                                                                                                                                                                                                                              |
| [`displayName`](#displayname)        | String                           | Name shown in UI in place of `name`                                                                                                                                                                                                                                                                              |
| [`version`](#version)                | String                           | Version string. Setting it keeps users on that version until you change it                                                                                                                                                                                                                                       |
| `description`                        | String                           | Short explanation of what the plugin provides                                                                                                                                                                                                                                                                    |
| `author`                             | Object                           | `name`, which is required, plus optional `email` and `url`                                                                                                                                                                                                                                                       |
| `homepage`                           | String                           | Documentation URL. Must parse as a URL, or the plugin fails to load                                                                                                                                                                                                                                              |
| `repository`                         | String                           | Source repository URL. Not validated                                                                                                                                                                                                                                                                             |
| `license`                            | String                           | SPDX identifier such as `MIT` or `Apache-2.0`                                                                                                                                                                                                                                                                    |
| `keywords`                           | Array of strings                 | Discovery tags                                                                                                                                                                                                                                                                                                   |
| [`metadata`](#metadata)              | Object                           | Free-form object for your own data. Claude Code doesn't read it                                                                                                                                                                                                                                                  |
| [`defaultEnabled`](#defaultenabled)  | Boolean                          | Whether the plugin starts enabled when the user hasn't set it. Defaults to `true`                                                                                                                                                                                                                                |
| [`dependencies`](#dependencies)      | Array of strings or objects      | Plugins that must be enabled for this one to work                                                                                                                                                                                                                                                                |
| [`settings`](#settings)              | Object                           | Settings Claude Code applies while the plugin is enabled. Only `agent` and `subagentStatusLine` take effect                                                                                                                                                                                                      |
| [`userConfig`](#user-configuration)  | Object                           | Values Claude Code prompts the user for when the plugin is enabled                                                                                                                                                                                                                                               |
| [`channels`](#channels)              | Array of objects                 | Message channels the plugin provides, each bound to one of its MCP servers                                                                                                                                                                                                                                       |
| `skills`                             | Path, or array of paths          | Directories to scan for skills, each a directory of `<name>/SKILL.md` folders or one folder holding `SKILL.md` directly. `"."` names the plugin root. Adds to the default `skills/` scan                                                                                                                         |
| [`commands`](#commands)              | Path, array of paths, or object  | Flat `.md` command files, directories of them, or an object map of command name to `source` or `content`. Replaces the default `commands/` scan                                                                                                                                                                  |
| `agents`                             | Path, or array of paths          | Agent `.md` files. Directories aren't accepted. Replaces the default `agents/` scan                                                                                                                                                                                                                              |
| [`hooks`](#hooks)                    | Path, object, or array of either | `.json` hook files or inline hook config. Loaded together with `hooks/hooks.json`                                                                                                                                                                                                                                |
| [`mcpServers`](#mcpservers)          | Path, object, or array of either | `.json` MCP config files, `.mcpb` or `.dxt` bundles, or inline server configs keyed by name. Loaded together with `.mcp.json`; a server name declared later replaces an earlier one                                                                                                                              |
| [`lspServers`](#lspservers)          | Path, object, or array of either | `.json` LSP config files or inline server configs keyed by name. Loaded together with `.lsp.json`                                                                                                                                                                                                                |
| `outputStyles`                       | Path, or array of paths          | Output style files or directories. Replaces the default `output-styles/` scan                                                                                                                                                                                                                                    |
| `workflows`                          | Path, or array of paths          | [Workflow](/docs/en/workflows#distribute-a-workflow-in-a-plugin) `.js` files or directories. Replaces the default `workflows/` scan                                                                                                                                                                                   |
| `experimental`                       | Object                           | Container for `themes`, `monitors`, and `evals`, whose manifest shape may still change                                                                                                                                                                                                                           |
| `experimental.themes`                | Path, or array of paths          | Theme files or directories. Replaces the default `themes/` scan. A top-level `themes` key still loads, with a `claude plugin validate` warning                                                                                                                                                                   |
| [`experimental.monitors`](#monitors) | Path, or inline array            | A `.json` file holding the monitors array, or the array itself. Defaults to `monitors/monitors.json`. A top-level `monitors` key still loads, with a `claude plugin validate` warning. Monitors run only in interactive sessions, and not on Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry |
| `experimental.evals`                 | Path, or array of paths          | Directory that holds the plugin's [eval cases](/docs/en/plugin-evals#use-a-different-eval-directory) when it isn't the default `evals/`. `claude plugin eval --eval-dir` overrides it                                                                                                                                 |

In the Type column, a path is a string relative to the plugin root, such as `"./custom/commands"`.

### `name`

The plugin identifier. It must be non-empty, with no spaces, `@`, `:`, path separators, control characters, or bidirectional-formatting characters; use kebab-case.

Claude Code namespaces every component under it, so an agent `reviewer` in plugin `deploy-tools` appears as `deploy-tools:reviewer`.

### `displayName`

The name shown in UI in place of `name`. It may contain spaces and any casing, and it isn't used for namespacing or lookup.

For a marketplace-installed plugin, a `displayName` on the [marketplace entry](/docs/en/plugins/marketplace-reference#plugin-entries) takes precedence over this value.

### `version`

A version string, not checked against semver. Setting it pins the plugin to that version until you change it; see [Versions and updates](/docs/en/plugins/loading#versions-and-updates). A plugin with a [`command` source](/docs/en/plugins/marketplace-reference), a plugin from a [marketplace hosted on claude.ai](/docs/en/plugins/install#add-from-claude-ai), and a plugin [loaded in place](/docs/en/plugins/loading#find-plugins-on-disk) from a marketplace added as a local directory aren't pinned by this field.

### `metadata`

A free-form object for your own data, such as catalog or entitlement fields. Claude Code doesn't read it. Requires Claude Code v2.1.222 or later.

### `defaultEnabled`

Whether the plugin starts enabled when the user hasn't set it in [`enabledPlugins`](/docs/en/settings-reference#enabledplugins). Defaults to `true`. A plugin that an enabled plugin depends on starts enabled regardless. The same field in the marketplace entry overrides this one.

Once a user's `enabledPlugins` entry is written, it persists across plugin updates, so changing `defaultEnabled` in a later release doesn't change the setting for an existing user.

### `dependencies`

Plugins that must be enabled for this one to work. Each entry is `"name"`, `"name@marketplace"`, or `{ "name": "...", "marketplace": "...", "version": "..." }`. Bare names resolve against this plugin's own marketplace. See [dependency constraints](/docs/en/plugins/dependencies).

### `settings`

Settings Claude Code applies while the plugin is enabled. Only `agent` and `subagentStatusLine` take effect; other keys are dropped at load. A `settings.json` at the plugin root takes precedence over this key. See [Default settings](/docs/en/plugins/components#default-settings).

## Component path forms

Every component key accepts a path relative to the plugin root. `hooks`, `mcpServers`, `lspServers`, and `experimental.monitors` also accept inline configuration, `commands` also accepts an object map, and `mcpServers` also accepts MCP bundle paths and URLs. The examples that follow show each accepted shape once. For what each component does at runtime, see [Plugin components](/docs/en/plugins/components).

### Path-only fields

`agents`, `skills`, `outputStyles`, `workflows`, and `experimental.themes` take one path or an array of paths. `agents` entries must be `.md` files, and `skills` entries must be directories. The other three accept a directory or a file.

```json theme={null}
{
  "agents": ["./custom-agents/reviewer.md", "./custom-agents/tester.md"],
  "skills": ["./extra-skills/", "."],
  "outputStyles": "./styles/"
}
```

### `commands`

`commands` takes a path, an array of paths, or an object map. A path names a flat `.md` command file or a directory. In the object map, each key becomes the command name after the plugin prefix. For example, `"about"` in plugin `deploy-tools` runs as `/deploy-tools:about`.

Each value sets exactly one of `source` or `content`, and an entry that sets both or neither fails validation. The other fields in this table are optional:

| Field          | Type             | Description                                                      |
| :------------- | :--------------- | :--------------------------------------------------------------- |
| `source`       | string           | Path to the command's Markdown file, relative to the plugin root |
| `content`      | string           | Inline Markdown for the command body, instead of `source`        |
| `description`  | string           | Description shown for the command                                |
| `argumentHint` | string           | Argument hint shown after the command name, such as `[file]`     |
| `model`        | string           | Default model for the command                                    |
| `allowedTools` | array of strings | Tools the command may use without prompting                      |

This map declares one command from a file and one from inline content:

```json theme={null}
{
  "commands": {
    "status": { "source": "./commands/status.md", "argumentHint": "[env]" },
    "about": { "content": "Explain what this plugin provides." }
  }
}
```

### `hooks`

`hooks` takes a `.json` file path, an inline hooks object in the same shape as [`hooks` in `settings.json`](/docs/en/hooks#configuration), or an array mixing both. For hook events and handler fields, see the [hooks reference](/docs/en/hooks#hook-events).

Claude Code merges whatever you declare with `hooks/hooks.json` when that file exists.

```json theme={null}
{
  "hooks": [
    "./config/extra-hooks.json",
    {
      "PostToolUse": [
        {
          "matcher": "Write|Edit",
          "hooks": [
            { "type": "command", "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/format.sh" }
          ]
        }
      ]
    }
  ]
}
```

### `mcpServers`

`mcpServers` takes a `.json` file path, an MCP bundle path or URL, an inline map, or an array mixing them. For server config fields, see [plugin-provided MCP servers](/docs/en/mcp#plugin-provided-mcp-servers).

Claude Code loads `.mcp.json` at the plugin root first, then each declared shape in order. A server name declared later replaces an earlier one.

An `mcpServers` value takes one of these shapes:

| Shape             | Example value                                                                          | What Claude Code does                                                                                       |
| :---------------- | :------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------- |
| `.json` file path | `"./mcp/servers.json"`                                                                 | Reads the file as an `mcpServers` map                                                                       |
| MCP bundle path   | `"./bundle.mcpb"`                                                                      | Extracts the `.mcpb` or `.dxt` bundle into `.mcpb-cache/` under the plugin root and reads its server config |
| MCP bundle URL    | `"https://example.com/server.mcpb"`                                                    | Downloads the bundle into `.mcpb-cache/`, then reads it                                                     |
| Inline map        | `{ "deploy-api": { "command": "node", "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"] } }` | Uses the map as server configs keyed by name                                                                |

A bundle path or URL must end in `.mcpb` or `.dxt`. Any other extension fails validation.

### `lspServers`

`lspServers` takes a `.json` file path, an inline map of server name to config, or an array of either.

Claude Code loads `.lsp.json` at the plugin root first, then each declared config in order. A server name declared later replaces an earlier one.

Each server config is a strict object with these fields. An unknown key fails validation.

| Field                   | Required | Description                                                                                                                                                              |
| :---------------------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `command`               | Yes      | Language server binary. No spaces unless the value starts with `/`; put arguments in `args`                                                                              |
| `extensionToLanguage`   | Yes      | Map of file extension to LSP language ID, at least one entry. Keys start with a dot, such as `".go"`                                                                     |
| `args`                  | No       | Arguments passed to the server                                                                                                                                           |
| `transport`             | No       | Communication transport: `stdio` (default) or `socket`. Claude Code accepts `socket` but runs every server over stdio, so the stdout protocol rules apply to all servers |
| `env`                   | No       | Environment variables for the server process                                                                                                                             |
| `initializationOptions` | No       | Options sent in the initialize request                                                                                                                                   |
| `settings`              | No       | Settings sent by `workspace/didChangeConfiguration`                                                                                                                      |
| `workspaceFolder`       | No       | Workspace folder path for the server                                                                                                                                     |
| `startupTimeout`        | No       | Milliseconds to wait for startup, a positive integer                                                                                                                     |
| `shutdownTimeout`       | No       | Milliseconds to wait for a graceful shutdown, a positive integer. When the timeout elapses, Claude Code terminates the server process. When unset, no timeout applies    |
| `restartOnCrash`        | No       | Whether to restart the server after it crashes. Defaults to `true`. Set to `false` to leave a crashed server stopped instead of restarting it                            |
| `maxRestarts`           | No       | Restart attempts before giving up, zero or more                                                                                                                          |
| `diagnostics`           | No       | Whether to push diagnostics into context after edits. Defaults to `true`                                                                                                 |

This inline config runs `gopls` for `.go` files:

```json theme={null}
{
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": { ".go": "go" }
    }
  }
}
```

For the language servers Anthropic publishes as plugins and how the servers behave at runtime, see [Code intelligence](/docs/en/plugins/code-intelligence).

### `monitors`

`experimental.monitors` takes a `.json` file path or the inline array. When you omit the key, Claude Code loads `monitors/monitors.json` if it exists.

Each entry is a strict object with these fields.

| Field         | Required | Description                                                                                                                                                        |
| :------------ | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | Yes      | Identifier unique within the plugin                                                                                                                                |
| `command`     | Yes      | Shell command Claude Code runs as a persistent background process in the session working directory                                                                 |
| `description` | Yes      | Short summary shown in the task panel and notification summaries                                                                                                   |
| `when`        | No       | With `"always"`, the default, the monitor starts at session start and on plugin reload. With `"on-skill-invoke:<skill>"`, it starts the first time that skill runs |

This inline array declares one monitor that starts the first time the `deploy` skill runs:

```json theme={null}
{
  "experimental": {
    "monitors": [
      {
        "name": "deploy-status",
        "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/poll-deploy.sh",
        "description": "Deployment status changes",
        "when": "on-skill-invoke:deploy"
      }
    ]
  }
}
```

A monitor `command` can't reference `${user_config.*}`. See [Fields that run through a shell](#fields-that-run-through-a-shell).

## Path rules

Every component path in a manifest is relative to the plugin root and must start with `./`. A path such as `commands/foo.md` fails validation. `skills` and `mcpServers` each accept one form outside that rule:

* **`skills`**: also accepts `"."`. Both `"."` and `"./"` denote the plugin root. Before v2.1.221, `"."` failed manifest validation, so use `"./"` when the plugin must load on earlier versions
* **`mcpServers`**: also accepts an `https://` bundle URL

### Containment and existence

Every component path must resolve inside the plugin root and must exist. `claude plugin validate` doesn't check the `outputStyles`, `lspServers`, `monitors`, or `themes` paths, so a bad path in those fields fails only when the plugin loads:

* **Containment**: a path that resolves outside the plugin root doesn't load, and the `/plugin` **Errors** tab shows `<component> path escapes plugin directory: <path>`. A path containing `..` is the usual case, and `claude plugin validate` reports it as `Path contains ".." which could be a path traversal attempt`
* **Existence**: a path that doesn't exist doesn't load, and the `/plugin` **Errors** tab shows `<component> path not found: <path>`. `claude plugin validate` reports it as `Path not found`

### How each key combines with its default location

Each component key either replaces its default location, adds to it, or merges with it:

* **Replaces the default**: `commands`, `agents`, `outputStyles`, `workflows`, `experimental.themes`, `experimental.monitors`. When you set `commands`, the default `commands/` directory isn't scanned. To keep the default and add more, list it explicitly: `"commands": ["./commands/", "./extras/"]`
* **Adds to the default**: `skills`. The `skills/` directory is still scanned, and the listed directories load alongside it
* **Merges**: `hooks`, `mcpServers`, `lspServers`. The default file loads first, and what the manifest declares merges into it, as described under [Component path forms](#component-path-forms)

If a plugin has a default folder such as `commands/` and also sets the manifest key that replaces it, Claude Code loads the manifest paths and not the folder. `claude plugin list` and the `/plugin` interface then show the warning `Default <folder>/ folder is ignored because the manifest sets "<key>"`.

To avoid the warning, set the key to a path inside that folder: `"commands": ["./commands/deploy.md"]` names a file in the default folder and produces no warning.

## User configuration

`userConfig` declares values Claude Code prompts the user for when the plugin is enabled, so users don't edit `settings.json` themselves.

Keys are identifiers made of letters, digits, and underscores, and can't start with a digit.

Each value is a strict object with these fields. An unknown key fails validation.

| Field         | Required | Description                                                                                                                                                                               |
| :------------ | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`        | Yes      | One of `string`, `number`, `boolean`, `directory`, or `file`                                                                                                                              |
| `title`       | Yes      | Label shown in the configuration dialog                                                                                                                                                   |
| `description` | Yes      | Help text shown beneath the field                                                                                                                                                         |
| `required`    | No       | If `true`, the configuration dialog doesn't accept an empty value                                                                                                                         |
| `default`     | No       | Value used when the user provides nothing: a string, number, boolean, or array of strings                                                                                                 |
| `options`     | No       | For `string`, the values the field accepts, shown as a picker in `/config`. See [Limit a field to fixed options](#limit-a-field-to-fixed-options). Requires Claude Code v2.1.271 or later |
| `multiple`    | No       | For `string`, allows an array of strings                                                                                                                                                  |
| `sensitive`   | No       | If `true`, masks input and stores the value in secure storage instead of `settings.json`                                                                                                  |
| `min` / `max` | No       | Bounds for `number`                                                                                                                                                                       |

Each option of each enabled plugin also appears as a row in the `/config` panel, except `sensitive` options and `multiple` lists. The `/config` rows require Claude Code v2.1.269 or later.

This `userConfig` declares an endpoint and a masked token:

```json theme={null}
{
  "userConfig": {
    "api_endpoint": {
      "type": "string",
      "title": "API endpoint",
      "description": "Your team's API endpoint"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "API authentication token",
      "sensitive": true
    }
  }
}
```

### Limit a field to fixed options

Set `options` on a `userConfig` field to make users pick its value from a fixed list.

To limit a `tone` field to three options, list them in `options` and set `default` to one of them:

```json theme={null}
{
  "userConfig": {
    "tone": {
      "type": "string",
      "title": "Tone",
      "description": "Voice for generated replies",
      "options": ["neutral", "warm", "formal"],
      "default": "neutral"
    }
  }
}
```

If you declare `options` on any field, users on Claude Code versions before v2.1.271 can't load the plugin.

`options` applies to a `string` field that isn't `multiple` or `sensitive`. Set `default` to one of the listed values, or set `required: true` so the user must pick one. Each option is a plain label of 1 to 64 characters, and `claude plugin validate`, which you run in your shell, reports anything else it rejects. A plugin whose `options` break these rules fails to load.

### Where values are stored

Non-sensitive values are saved under [`pluginConfigs`](/docs/en/settings-reference#pluginconfigs) in the user's `settings.json`. Sensitive values go to the platform's secure credential store instead. The [settings page](/docs/en/settings-reference#pluginconfigs) lists which settings files `pluginConfigs` is read from.

### Reference a saved value

Reference a saved value where the plugin needs it, in one of two forms:

* **`${user_config.KEY}`**: substituted in MCP server config, LSP server config, [exec-form](/docs/en/hooks#exec-form-and-shell-form) hook `args`, and skill and agent content. In skill and agent content, only non-sensitive values are substituted, and a sensitive value there becomes a placeholder
* **`CLAUDE_PLUGIN_OPTION_<KEY>`**: exported to hook processes for every option, with `<KEY>` uppercased. A shell-form hook reads `$CLAUDE_PLUGIN_OPTION_API_TOKEN` for `api_token`

### Fields that run through a shell

Shell-form hook commands, monitor commands, and MCP [`headersHelper`](/docs/en/mcp#use-dynamic-headers-for-custom-authentication) reject `${user_config.*}`. A component that references it in one of these fields fails with an [error](/docs/en/errors#plugin-command-references-user-config) instead of running, because the field's value is passed to a shell that would re-parse the substituted value.

The table shows how the value can reach each of these fields instead.

| Field                    | How the value can reach it                                                                                                                                                                                                    |
| :----------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Shell-form hook commands | Use [exec form](/docs/en/hooks#exec-form-and-shell-form) with `args`, or read `CLAUDE_PLUGIN_OPTION_<KEY>` from the hook's environment                                                                                             |
| Monitor commands         | Not through Claude Code. Monitor processes don't receive `CLAUDE_PLUGIN_OPTION_<KEY>`, so the monitor script has to obtain the value on its own                                                                               |
| MCP `headersHelper`      | Not through Claude Code. The helper's environment carries `CLAUDE_PLUGIN_ROOT`, `CLAUDE_CODE_MCP_SERVER_NAME`, and `CLAUDE_CODE_MCP_SERVER_URL` but no option values, so the helper script has to obtain the value on its own |

## Channels

`channels` declares the message channels a plugin provides, such as a bridge to a chat app. When you declare one, Claude Code can prompt for the channel's configuration when the plugin is enabled. For how the server injects messages, see the [channels reference](/docs/en/channels-reference#package-as-a-plugin).

Each entry is a strict object bound to one of the plugin's MCP servers, with these fields:

| Field         | Required | Description                                                                                                                                                                   |
| :------------ | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `server`      | Yes      | Key of the MCP server in this plugin's `mcpServers` that the channel binds to                                                                                                 |
| `displayName` | No       | Name shown in the configuration dialog title. Defaults to the server name                                                                                                     |
| `userConfig`  | No       | Options to prompt for, in the same shape as [top-level `userConfig`](#user-configuration). Saved values substitute into `${user_config.KEY}` references in the server's `env` |

This manifest binds a channel to the plugin's `telegram` MCP server and prompts for a bot token that substitutes into the server's `env`:

```json theme={null}
{
  "mcpServers": {
    "telegram": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": { "BOT_TOKEN": "${user_config.bot_token}" }
    }
  },
  "channels": [
    {
      "server": "telegram",
      "displayName": "Telegram",
      "userConfig": {
        "bot_token": {
          "type": "string",
          "title": "Bot token",
          "description": "Telegram bot token",
          "sensitive": true
        }
      }
    }
  ]
}
```

## Environment variables

Claude Code provides three path variables to plugin components. Reference them as `${NAME}` in the fields listed under [Where each variable resolves](#where-each-variable-resolves), and read them as environment variables in the processes that receive them.

| Variable                | Resolves to                                                                                                                                                                                             | Use it for                                                                |
| :---------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------ |
| `${CLAUDE_PLUGIN_ROOT}` | Absolute path of the plugin's installed version                                                                                                                                                         | Scripts, binaries, and config files bundled with the plugin               |
| `${CLAUDE_PLUGIN_DATA}` | `~/.claude/plugins/data/<id>/`, created on first reference and kept across plugin updates. `<id>` is the plugin identifier with every character other than a letter, digit, `_`, or `-` replaced by `-` | Installed dependencies such as `node_modules`, generated code, and caches |
| `${CLAUDE_PROJECT_DIR}` | The project root                                                                                                                                                                                        | Project-local scripts and config files                                    |

`${CLAUDE_PLUGIN_ROOT}` changes when the plugin updates, so don't write state there. For where the root moves and when the old directory is cleaned up, see the [loading page](/docs/en/plugins/loading).

When you uninstall the plugin from the last place it's installed, the `${CLAUDE_PLUGIN_DATA}` directory is deleted unless you pass [`--keep-data`](/docs/en/plugins/cli-reference).

### Where each variable resolves

In each plugin component, `${...}` references resolve inline in specific fields, and some components also receive the variables in their process environment:

| Plugin component                  | Fields where `${...}` resolves              | Exported to the process                                                                            |
| :-------------------------------- | :------------------------------------------ | :------------------------------------------------------------------------------------------------- |
| Hook commands                     | Anywhere in `command` and `args`            | `CLAUDE_PLUGIN_ROOT`, `CLAUDE_PLUGIN_DATA`, `CLAUDE_PROJECT_DIR`, and `CLAUDE_PLUGIN_OPTION_<KEY>` |
| Monitor commands                  | Anywhere in `command`                       | Not exported                                                                                       |
| MCP `stdio` servers               | `command`, `args`, `env`                    | `CLAUDE_PLUGIN_ROOT`, `CLAUDE_PLUGIN_DATA`                                                         |
| MCP `http`, `sse`, `ws` servers   | `url`, `headers`, `headersHelper`           | Not applicable                                                                                     |
| LSP servers                       | `command`, `args`, `env`, `workspaceFolder` | `CLAUDE_PLUGIN_ROOT`, `CLAUDE_PLUGIN_DATA`, `CLAUDE_PROJECT_DIR`                                   |
| Skill, command, and agent content | Anywhere in the Markdown body               | Not applicable                                                                                     |

The variables aren't present in the environment of commands Claude runs through the Bash tool, in the main session or in a subagent. In skill, command, and agent content, write the `${...}` reference in the Markdown body instead, and Claude Code substitutes the path inline when it loads the content.

### Quoting and path separators

Keep each substituted path a single argument:

* **Hook commands**: use [exec form](/docs/en/hooks#exec-form-and-shell-form) with `args` so each path is one argument with no quoting
* **Shell-form hooks and monitor commands**: wrap the variable in double quotes so a path with spaces stays one word

This shell-form hook runs a script bundled with the plugin:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

On Windows, the substituted paths use forward slashes so a shell doesn't read backslashes as escapes.

## Standard layout

Each component type has a default location under the plugin root, used when the manifest doesn't point elsewhere.

| Component     | Default location             | Contents                                                                                                                                                                                                                                                                                                                       |
| :------------ | :--------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Manifest      | `.claude-plugin/plugin.json` | Plugin metadata and configuration. Optional                                                                                                                                                                                                                                                                                    |
| Skills        | `skills/`                    | One `<name>/SKILL.md` per skill. A plugin with `SKILL.md` at its root, no `skills/`, and no `skills` key loads as a single skill                                                                                                                                                                                               |
| Commands      | `commands/`                  | Flat Markdown command files. Prefer `skills/` for new plugins                                                                                                                                                                                                                                                                  |
| Agents        | `agents/`                    | Agent Markdown files. Subfolders are part of the [agent name](/docs/en/plugins/components#agents)                                                                                                                                                                                                                                   |
| Hooks         | `hooks/hooks.json`           | Hook configuration                                                                                                                                                                                                                                                                                                             |
| MCP servers   | `.mcp.json`                  | MCP server definitions                                                                                                                                                                                                                                                                                                         |
| LSP servers   | `.lsp.json`                  | LSP server configurations                                                                                                                                                                                                                                                                                                      |
| Output styles | `output-styles/`             | Output style Markdown files                                                                                                                                                                                                                                                                                                    |
| Workflows     | `workflows/`                 | Workflow `.js` files                                                                                                                                                                                                                                                                                                           |
| Themes        | `themes/`                    | Theme JSON files                                                                                                                                                                                                                                                                                                               |
| Monitors      | `monitors/monitors.json`     | The monitors array                                                                                                                                                                                                                                                                                                             |
| Executables   | `bin/`                       | Files here are on the Bash tool's `PATH` while the plugin is enabled, so Claude runs them as bare commands. claude.ai and Cowork don't install a plugin that has this directory, including one you [distribute through claude.ai organization settings](/docs/en/plugins/host-marketplace#distribute-through-organization-settings) |
| Settings      | `settings.json`              | `agent` and `subagentStatusLine` defaults applied while the plugin is enabled                                                                                                                                                                                                                                                  |

A plugin that uses every default location, plus a `scripts/` folder that its hooks call, is laid out like this:

```text theme={null}
deploy-tools/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── deploy/
│       └── SKILL.md
├── commands/
│   └── status.md
├── agents/
│   └── reviewer.md
├── hooks/
│   └── hooks.json
├── monitors/
│   └── monitors.json
├── output-styles/
│   └── terse.md
├── themes/
│   └── dracula.json
├── workflows/
│   └── release-audit.js
├── bin/
│   └── deploy-tool
├── scripts/
│   └── format.sh
├── settings.json
├── .mcp.json
└── .lsp.json
```

To click through this layout and read what each file does, open the [plugin explorer](/docs/en/plugins/components#explore-the-plugin-directory).

A `CLAUDE.md` at the plugin root isn't loaded as context, and `claude plugin validate` warns when it finds one. To include instructions that load into Claude's context, put them in a skill.

## Marketplace entries and the manifest

A [marketplace entry](/docs/en/plugins/marketplace-reference) accepts every field on this page alongside [its own fields](/docs/en/plugins/marketplace-reference#plugin-entries), including `strict`.

The `strict` field decides whether the entry may add components to a plugin that has its own `plugin.json`. It defaults to `true`.

### How entry fields combine with `plugin.json`

The entry either serves as the manifest, adds components to it, or conflicts with it:

* **No `plugin.json`**: the entry is the manifest, regardless of `strict`. Entry `hooks` loads only in the inline object form. For a file path or array there, the `/plugin` **Errors** tab shows a `not yet supported in a marketplace entry` error
* **`plugin.json` present, `strict` unset or `true`**: Claude Code loads the manifest and appends the entry's `commands`, `agents`, `skills`, `outputStyles`, and `themes` to it. For `hooks`, the entry's matchers for an event replace the manifest's matchers for that same event, and events only the manifest declares keep theirs
* **`plugin.json` present, `strict: false`**: an entry that declares any of `commands`, `agents`, `skills`, `hooks`, `outputStyles`, or `themes` is a conflict, and the plugin fails to load with `Plugin <name> has conflicting manifests`

When a [marketplace entry whose `source` is the marketplace root](/docs/en/plugins/marketplace-reference) lists specific `skills` subdirectories, only those subdirectories load, and the plugin's default `skills/` directory isn't scanned. A `skills` key in the manifest instead [adds to the default](#how-each-key-combines-with-its-default-location).

### Metadata precedence

Some metadata fields have a fixed precedence regardless of `strict`:

* **`defaultEnabled` and display fields**: the entry's `defaultEnabled` and its [display fields](/docs/en/plugins/marketplace-reference#entry-and-plugin-json) such as `displayName` override the manifest's
* **`version`**: the manifest's `version` overrides the entry's
* **`name`**: when the entry lists the plugin under a different `name` than the manifest, `enabledPlugins` uses the entry name, and components are namespaced under the manifest name

For the full precedence table, see [Strict mode](/docs/en/plugins/marketplace-reference).

## Next steps

* [Add components to a plugin](/docs/en/plugins/components): what each component does at runtime, with an example that validates
* [Marketplace reference](/docs/en/plugins/marketplace-reference): the entry fields a marketplace can set for your plugin
* [Plugin commands reference](/docs/en/plugins/cli-reference#plugin-validate): `claude plugin validate` flags and output
* [Troubleshoot plugins](/docs/en/plugins/troubleshooting#claude-plugin-validate-reports-errors): each validation message with its fix
