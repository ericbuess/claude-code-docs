> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Recommend plugins for your org

> Add a relevance block to marketplace plugin entries so Claude Code suggests them when a user's work matches, and allowlist the marketplace in managed settings.

Claude Code can suggest installing a plugin from your organization's marketplace when a user's session matches signals you define for that plugin. Signals include the working directory, files Claude has read, and commands Claude has run. You define them by adding a `relevance` block to the plugin's entry in `marketplace.json`.

A marketplace operator writes the `relevance` entries. An administrator then allowlists the marketplace in managed settings. Users see no suggestions from a marketplace until it's allowlisted.

<Note>
  These cases are covered on other pages:

  * **You want to install plugins**: see [Install and manage plugins](/docs/en/plugins/install)
  * **You want to turn suggestions off**: see [Understand how plugin relevance works](#understand-how-plugin-relevance-works)
</Note>

Start with the sections for your role:

* **Marketplace operators**: read [how suggestions work](#understand-how-plugin-relevance-works), then [add relevance to a plugin entry](#add-relevance-to-a-plugin-entry) and [validate your marketplace](#validate-your-marketplace)
* **Administrators**: [enable suggestions in managed settings](#enable-suggestions-in-managed-settings)

## Understand how plugin relevance works

Each plugin entry in `marketplace.json` can include a `relevance` object. The object names a topic and one or more signals. A signal is a pattern that Claude Code tests against the current session, such as the working directory or files Claude has read.

Signal matching happens locally on the user's machine and adds no network traffic. Claude Code doesn't report which signals matched or their values to Anthropic or to the marketplace operator.

When a signal matches and the plugin isn't already installed, Claude Code suggests the plugin in these places:

* **Spinner tip**: a message with the `/plugin install` command appears below the spinner while Claude is responding.
* **Session-start notification**: if a `cwd` signal matches the working directory, a one-line notification appears before the user sends a first message.
* **`/plugin` Discover tab**: the plugin is pinned to the top of the Discover list.

[Preview what the user sees](#preview-what-the-user-sees) shows the exact text of each and how often they repeat.

Claude Code never installs the plugin automatically. The user always confirms.

The spinner tip and the session-start notification both stop appearing when the user or project sets [`spinnerTipsEnabled`](/docs/en/settings-reference#spinnertipsenabled) to `false`, or when a [`spinnerTipsOverride`](/docs/en/settings-reference#spinnertipsoverride) with `excludeDefault` replaces the built-in tips. The Discover-tab pin isn't affected by either setting.

## Add relevance to a plugin entry

Add a `relevance` object to the plugin's entry in your `marketplace.json`. The following example declares that the `terraform-helpers` plugin is relevant when Claude reads a `.tf` file or runs `terraform`:

```json theme={null}
{
  "name": "your-marketplace",
  "owner": { "name": "Your Org" },
  "plugins": [
    {
      "name": "terraform-helpers",
      "source": "./plugins/terraform-helpers",
      "description": "Your organization's Terraform conventions and helpers",
      "relevance": {
        "topic": "Terraform",
        "signals": {
          "cli": ["terraform"],
          "filesRead": ["**/*.tf"]
        }
      }
    }
  ]
}
```

While none of its signals match, the plugin keeps its normal position in the Discover list and doesn't appear as a spinner tip.

To check the block before publishing, [validate your marketplace](#validate-your-marketplace).

## Field reference

The `relevance` object and its nested `signals` object accept the fields in the following tables.

Older clients still load a marketplace that uses `relevance` fields they don't recognize, because unknown fields under `relevance` and `relevance.signals` are ignored at load time. A recognized field whose value exceeds its limit in the [field reference](#field-reference) invalidates the whole plugin entry, and users can't install that plugin from the marketplace until you fix it; `claude plugin validate` reports the same limits.

### `relevance`

| Field     | Type   | Description                                                                                                                                                             |
| :-------- | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `topic`   | string | Optional. The phrase that fills "Working with *topic*?" in the spinner tip. Defaults to the plugin name with each hyphen segment capitalized. Maximum 64 characters.    |
| `signals` | object | Matchers that determine when the plugin is relevant. Claude Code suggests the plugin only if at least one signal is set. See [`relevance.signals`](#relevance-signals). |

The `topic` is often the product name, for example `Terraform`. Use a domain such as `design` when the plugin name doesn't sound natural as a topic.

### `relevance.signals`

The `signals` object accepts the following fields.

| Field          | Type             | Description                                                                                                                                                                                                                                 | Limit                                                                                        |
| :------------- | :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------- |
| `cwd`          | array of strings | Glob patterns matched against the session's working directory. See [working directory matching](#working-directory-matching).                                                                                                               | 10 patterns of 256 characters each                                                           |
| `cli`          | array of strings | Command names from shell commands Claude has run this session, for example `["terraform"]`. Exact match. See [command name matching](#command-name-matching).                                                                               | 10 entries of 64 characters each                                                             |
| `hosts`        | array of strings | Hostnames seen in `http://` or `https://` URLs in Bash commands this session, for example `["registry.terraform.io"]`. Bare lowercase hostname only: no scheme, port, or path. Exact case-insensitive match.                                | 20 entries of 128 characters each                                                            |
| `filesRead`    | array of strings | Glob patterns matched against the paths of files Claude has read this session, for example `["**/*.tf"]`. Forward-slash normalized and case-insensitive.                                                                                    | 10 patterns of 256 characters each                                                           |
| `manifestDeps` | array of objects | Dependencies declared in package manifests Claude has read this session. Each entry is `{ "file": "...", "pattern": "..." }`, where both values are regular expressions. See [manifest dependency matching](#manifest-dependency-matching). | 10 entries, each value at most 256 characters. Manifest files larger than 512 KB are skipped |

The `filesRead` and `manifestDeps` signals also match against files Claude has written or edited this session and against the project's auto-loaded `CLAUDE.md` memory files.

#### Working directory matching

`cwd` is the only signal that can match at session start, before the user sends a first message.

Claude Code matches each `cwd` pattern as follows:

* The pattern is matched against the working directory as an absolute path. When the session is inside a git repository, it's also matched against the working directory's path relative to the repository root.
* Matching is forward-slash normalized and case-insensitive.
* Every pattern matches the directory itself and everything under it, so `infra`, `infra/`, and `infra/**` behave identically.

#### Command name matching

Claude Code records one command name for each shell command Claude runs: the first token after any leading environment variable assignments and `sudo`. Compound commands contribute only their leading command, so `cd infra && terraform plan` records `cd`, not `terraform`.

#### Manifest dependency matching

Each `manifestDeps` entry pairs two JavaScript `RegExp` source strings:

* `file`: matched case-insensitively against the manifest file's path. The path is typically absolute, so anchor the pattern at the end rather than the start. Paths aren't separator-normalized for this signal, so Windows paths use backslashes.
* `pattern`: matched case-sensitively against that file's contents.

The following example uses `manifestDeps` to suggest your plugin once Claude has read a `package.json` that depends on your SDK's npm package, named `your-sdk` here.

```json theme={null}
{
  "name": "your-plugin",
  "source": "./plugins/your-plugin",
  "relevance": {
    "signals": {
      "manifestDeps": [
        {
          "file": "[/\\\\]package\\.json$",
          "pattern": "\"your-sdk\"\\s*:"
        }
      ]
    }
  }
}
```

In this example, the `file` pattern uses `[/\\\\]` so it matches both forward-slash and backslash path separators, and `\\.` so the dot is literal. In JSON, each backslash in the regular expression is written twice.

## Validate your marketplace

In your shell, run `claude plugin validate` against your marketplace directory to check the `relevance` block before publishing:

```bash theme={null}
claude plugin validate ./my-marketplace
```

The validator reports errors and warnings on the `relevance` block, including these:

* Reports unknown keys under `relevance` and `relevance.signals` as warnings
* Flags a `relevance` value that isn't an object
* Rejects a `signals.hosts` entry that includes a scheme, port, or path

Each finding prints with the path of the field it concerns, and the output ends with `Validation passed`, `Validation passed with warnings`, or `Validation failed`.

## Enable suggestions in managed settings

Users see no suggestions from a marketplace until an administrator allowlists it in [managed settings](/docs/en/plugins/org), even when its `marketplace.json` declares `relevance`.

To allowlist a marketplace, edit your managed settings as follows:

* Add the marketplace name to `pluginSuggestionMarketplaces`.
* For any marketplace other than the official Anthropic marketplace, also declare the marketplace source, either as that name's entry in [`extraKnownMarketplaces`](/docs/en/plugins/org#require-a-marketplace-and-its-plugins) or as an entry in [`strictKnownMarketplaces`](/docs/en/plugins/org#allowlist-with-strictknownmarketplaces).

On a machine where the marketplace isn't registered, or is registered under the allowlisted name from a different source, no suggestions from it appear. The source check stops an unrelated source from registering under an allowlisted name to get its plugins suggested across your org.

The following `managed-settings.json` registers an org marketplace from a GitHub repository and enables its suggestions:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "your-marketplace": {
      "source": {
        "source": "github",
        "repo": "your-org/your-marketplace"
      }
    }
  },
  "pluginSuggestionMarketplaces": ["your-marketplace"]
}
```

The official marketplace's name can only register from the official Anthropic source, so it needs no source declaration. For the official marketplace, allowlist the name alone:

```json theme={null}
{
  "pluginSuggestionMarketplaces": ["claude-plugins-official"]
}
```

## Preview what the user sees

When a plugin's `relevance` signal matches during a session, the tip below the spinner reads:

```text theme={null}
Working with Terraform? Install the terraform-helpers plugin:
/plugin install terraform-helpers@your-marketplace
```

When a `cwd` signal matches at session start, the one-line notification reads:

```text theme={null}
plugin suggestion: terraform-helpers@your-marketplace · /plugin
```

In the `/plugin` Discover tab, the plugin is pinned above the other results with an annotation that names the matching signal, such as `suggested for this directory` or `suggested for terraform commands`.

Claude Code limits how often it suggests a given plugin:

* The suggestion appears at most once every three sessions across the spinner tip and the session-start notification combined.
* The session-start notification stops appearing once the spinner tip and the notification have shown the plugin a combined total of two times.
* Neither the spinner tip nor the session-start notification repeats once the plugin is installed.
* The Discover tab pins the plugin the first time the user opens the tab while the plugin's signals match. Claude Code records that in `~/.claude.json`, so every later time the user opens `/plugin` on that machine, the plugin appears in normal order.

## See also

* [Host a marketplace](/docs/en/plugins/host-marketplace): run the marketplace that hosts your plugins
* [Marketplace reference](/docs/en/plugins/marketplace-reference#plugin-entries): every field a plugin entry accepts
* [Recommend your plugin from your CLI](/docs/en/plugins/cli-hints): prompt users from your own CLI instead of from Claude Code's session signals
* [Manage plugins for your organization](/docs/en/plugins/org): `extraKnownMarketplaces`, `strictKnownMarketplaces`, and the rest of the plugin policy keys
