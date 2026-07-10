> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Recommend plugins for your org

> Add a relevance block to marketplace plugin entries so Claude Code suggests them when a user's work matches.

If you operate a plugin marketplace for your organization, you can have Claude Code suggest specific plugins to users based on what they are working on. Add a `relevance` block to a plugin's entry in `marketplace.json`, then allowlist the marketplace in managed settings. When a user's session matches one of the declared signals, Claude Code surfaces an install suggestion for that plugin.

Marketplace-declared suggestions are opt-in per marketplace through [managed settings](/en/settings#settings-files). No marketplace's `relevance` declarations produce suggestions until an administrator adds it to the allowlist, including the official Anthropic marketplace. Claude Code also includes one built-in suggestion that is independent of this allowlist; that tip and all marketplace-declared tips are disabled when [`spinnerTipsEnabled`](/en/settings#available-settings) is set to `false`.

{/* min-version: 2.1.152 */}This feature requires Claude Code v2.1.152 or later. Older clients ignore the `relevance` field.

This page is for marketplace operators and enterprise administrators. If you are looking to install plugins, see [Discover and install plugins](/en/discover-plugins).

## How it works

Each plugin entry in `marketplace.json` can carry a `relevance` object. The object names a topic and one or more signals. A signal is a pattern that Claude Code tests against the current session, such as the working directory or files Claude has read.

Signal matching happens locally on the user's machine. The matching adds no network traffic and does not report which signals matched, or their values, to Anthropic or to the marketplace operator.

When a signal matches and the plugin is not already installed, Claude Code shows the plugin in three places:

* **Spinner tip**: a "Working with *topic*? Install the *plugin* plugin" message with the `/plugin install` command appears below the spinner while Claude is responding.
* **Session-start suggestion**: {/* min-version: 2.1.153 */}if the `cwd` signal matches the working directory, a one-line `plugin suggestion: <name>@<marketplace> · /plugin` notification appears before the first turn. This surface requires Claude Code v2.1.153 or later.
* **`/plugin` Discover tab**: {/* min-version: 2.1.154 */}the plugin is pinned to the top of the Discover list with an annotation such as "suggested for this directory" or "suggested for stripe commands". This surface requires Claude Code v2.1.154 or later.

The spinner tip and the session-start notification are part of the spinner-tips system. Both are disabled when the user or project sets `spinnerTipsEnabled` to `false`, or when a custom `spinnerTipsOverride` is configured with `excludeDefault`. The Discover-tab pin is independent of tip settings.

Claude Code never installs a plugin automatically. The user always confirms.

## Add relevance to a plugin entry

Add a `relevance` object to the plugin's entry in your `marketplace.json`. The following example declares that the `terraform-helpers` plugin is relevant when Claude reads a `.tf` file or when Claude runs `terraform`:

```json theme={null}
{
  "name": "acme-corp-plugins",
  "owner": { "name": "Acme Platform Team" },
  "plugins": [
    {
      "name": "terraform-helpers",
      "source": "./plugins/terraform-helpers",
      "description": "Acme conventions and helpers for Terraform",
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

A plugin with a `relevance` block but no matching signal behaves like any other marketplace entry. It appears in the Discover list in its normal position and never surfaces as a spinner tip.

## Field reference

### `relevance`

| Field     | Type   | Description                                                                                                                                                                                                                                                                                                                                                       |
| :-------- | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `topic`   | string | Optional. The phrase that fills "Working with *topic*?" in the spinner tip. Often the product name, for example `Stripe`. Use a domain such as `design` when the plugin name does not read naturally as a topic. Defaults to the plugin name with each hyphen segment capitalized. The session-start notification does not use this value. Maximum 64 characters. |
| `signals` | object | Matchers that determine when the plugin is relevant. At least one signal is required for the plugin to be suggestible. See the table below.                                                                                                                                                                                                                       |

### `relevance.signals`

| Field          | Type             | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| :------------- | :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cwd`          | array of strings | {/* min-version: 2.1.153 */}Glob patterns matched against the session's working directory. Matched as an absolute path and, when inside a git repository, as a path relative to the repository root. Forward-slash normalized and case-insensitive. Every pattern matches the directory itself and everything under it, so `infra`, `infra/`, and `infra/**` behave identically. This is the only signal that can match at session start, before the first turn. Maximum 10 patterns of 256 characters each.                                                                                                                                                                                                                                                                                                   |
| `cli`          | array of strings | Command names from shell commands Claude has run this session, for example `["stripe"]`. Applies on every platform: commands run on Windows through PowerShell or Git Bash are recorded the same way. Claude Code records one command name per shell tool invocation: the first token after any leading environment variable assignments and `sudo`. Compound commands contribute only their leading command, so `cd infra && terraform plan` records `cd`, not `terraform`. Exact match. Maximum 10 entries of 64 characters each.                                                                                                                                                                                                                                                                            |
| `hosts`        | array of strings | Hostnames seen in `http://` or `https://` URLs in Bash commands this session, for example `["api.stripe.com"]`. Bare lowercase hostname only: no scheme, port, or path. Exact case-insensitive match. Maximum 20 entries of 128 characters each.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `filesRead`    | array of strings | {/* min-version: 2.1.153 */}Glob patterns matched against the paths of files Claude has read this session, for example `["**/*.tf"]`. Forward-slash normalized and case-insensitive. Maximum 10 patterns of 256 characters each.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `manifestDeps` | array of objects | Dependencies declared in package manifests Claude has read this session. Each entry is `{ "file": "...", "pattern": "..." }`, where `file` is a regular expression matched against the manifest file's path as recorded in session state, typically an absolute path, and `pattern` is a regular expression matched against that file's contents. Anchor `file` at the end, for example `[/\\\\]package\\.json$` in JSON-escaped form, because a start-anchored pattern never matches an absolute path. Paths are not separator-normalized for this signal, so Windows paths use backslashes. Manifest files larger than 512 KB are skipped. Both values are JavaScript `RegExp` source strings of at most 256 characters. `file` matches case-insensitively. `pattern` is case-sensitive. Maximum 10 entries. |

The `cli`, `hosts`, `filesRead`, and `manifestDeps` signals need session history, so they can only match on the spinner tip and the Discover tab. Only `cwd` can match at session start. The `filesRead` and `manifestDeps` signals test the session's recorded file state, which also includes files Claude has written or edited and auto-loaded `CLAUDE.md` memory files.

The following example uses `manifestDeps` to suggest a Stripe plugin once Claude has read a `package.json` that depends on `stripe`. The `file` pattern uses `[/\\\\]` so it matches both forward-slash and backslash path separators, and `\\.` so the dot is literal. In JSON, each backslash in the regular expression is written twice.

```json theme={null}
{
  "name": "stripe-helpers",
  "source": "./plugins/stripe-helpers",
  "relevance": {
    "topic": "Stripe",
    "signals": {
      "manifestDeps": [
        {
          "file": "[/\\\\]package\\.json$",
          "pattern": "\"stripe\"\\s*:"
        }
      ]
    }
  }
}
```

<Note>
  Unknown fields under `relevance` and `relevance.signals` are ignored at load time so older Claude Code clients continue to load your marketplace. Run `claude plugin validate` to surface them as warnings.
</Note>

## Enable suggestions in managed settings

Declaring `relevance` in `marketplace.json` is not enough on its own. An administrator must allowlist the marketplace in [managed settings](/en/settings#settings-files) before its suggestions appear to users.

Add the marketplace name to `pluginSuggestionMarketplaces`. For any marketplace other than the official Anthropic marketplace, also declare the marketplace source in the same managed settings, either as that name's entry in `extraKnownMarketplaces` or as an entry in `strictKnownMarketplaces`. The allowlisted name is ignored if the marketplace registered on the machine came from a different source. This prevents an unrelated source from registering under an allowlisted name to have its plugins suggested across your org.

The following `managed-settings.json` registers an org marketplace from a GitHub repository and enables its suggestions:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-corp-plugins": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    }
  },
  "pluginSuggestionMarketplaces": ["acme-corp-plugins"]
}
```

The official marketplace is exempt from the source-declaration requirement because its name can only register from the official Anthropic source. Allowlisting the name alone is sufficient:

```json theme={null}
{
  "pluginSuggestionMarketplaces": ["claude-plugins-official"]
}
```

See the [settings reference](/en/settings) for `pluginSuggestionMarketplaces` and [`extraKnownMarketplaces`](/en/settings#extraknownmarketplaces) for full configuration details.

## What the user sees

When a signal matches during a session, the spinner tip reads:

```text theme={null}
Working with Terraform? Install the terraform-helpers plugin:
/plugin install terraform-helpers@acme-corp-plugins
```

At session start, a matching `cwd` signal surfaces the one-line notification:

```text theme={null}
plugin suggestion: terraform-helpers@acme-corp-plugins · /plugin
```

A given plugin's suggestion appears at most once every three sessions across the spinner tip and the session-start notification combined, and neither repeats once the plugin is installed. The session-start notification additionally stops appearing after the suggestion has been shown twice.

{/* min-version: 2.1.154 */}In the `/plugin` Discover tab, the plugin is pinned above the other results with an annotation that names the matching signal, such as `suggested for this directory` or `suggested for terraform commands`. The Discover tab pins a given plugin once; later visits list it in normal order. The Discover-tab pin requires Claude Code v2.1.154 or later. On v2.1.152 only the spinner tip appears; the session-start notification is added in v2.1.153.

## Validate your marketplace

Run `claude plugin validate` against your marketplace directory to check the `relevance` block before publishing:

```
claude plugin validate ./my-marketplace
```

The validator reports unknown keys under `relevance` and `relevance.signals` as warnings, flags a `relevance` value that is not an object, and rejects a `signals.hosts` entry that includes a scheme, port, or path.

## See also

* [Create and distribute a plugin marketplace](/en/plugin-marketplaces): build the marketplace that hosts your plugins
* [Recommend your plugin from your CLI](/en/plugin-hints): prompt users from your own CLI instead of from Claude Code's session signals
* [Settings](/en/settings): full reference for `pluginSuggestionMarketplaces` and `extraKnownMarketplaces`
