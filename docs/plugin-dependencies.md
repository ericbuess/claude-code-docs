> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Constrain plugin dependency versions

> Declare version constraints on plugin dependencies so your plugin keeps working when an upstream plugin ships a breaking change.

A plugin can depend on other plugins by listing them in `plugin.json` or in its marketplace entry. By default, a dependency tracks the latest available version, so an upstream release can change the dependency under your plugin without warning. Version constraints let you hold a dependency at a tested version range until you choose to move.

When you install a plugin that declares dependencies, Claude Code resolves and installs them automatically and lists which dependencies were added at the end of the install output. If a dependency later goes missing, `/reload-plugins` and the background plugin auto-update install it automatically, provided its marketplace is already in your configured marketplaces. Dependencies from a marketplace you have not added are left unresolved.

This guide is for plugin authors who declare dependencies in `plugin.json` and for marketplace maintainers who tag releases. To install plugins that have dependencies, see [Discover and install plugins](/en/discover-plugins). For the full manifest schema, see the [Plugins reference](/en/plugins-reference).

<Note>
  Dependency version constraints require Claude Code v2.1.110 or later.
</Note>

## Why constrain dependency versions

Consider an internal marketplace where two teams publish plugins. The platform team maintains `secrets-vault`, an MCP server that wraps a secrets backend. The deploy team maintains `deploy-kit`, which calls `secrets-vault` to fetch credentials during deploys.

`deploy-kit` is tested against `secrets-vault` v2.1.0. Without a version constraint, the next time the platform team tags a release that renames an MCP tool, auto-update moves every engineer's `secrets-vault` to the new version and `deploy-kit` breaks.

With a version constraint, `deploy-kit` declares that it needs `secrets-vault` in the `~2.1.0` range. Engineers with `deploy-kit` installed stay on the highest matching `2.1.x` patch. The deploy team upgrades on their own schedule by publishing a new `deploy-kit` version with a wider constraint.

## Declare a dependency with a version constraint

List dependencies in the `dependencies` array of your plugin's `.claude-plugin/plugin.json`. Each entry is either a plugin name or an object with a version constraint.

The following manifest declares one unversioned dependency and one constrained dependency:

```json .claude-plugin/plugin.json theme={null}
{
  "name": "deploy-kit",
  "version": "3.1.0",
  "dependencies": [
    "audit-logger",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

An entry can be a bare string with only the plugin name, like `"audit-logger"` in the example above, which depends on whatever version that plugin's marketplace provides. For more control, use an object with these fields:

| Field         | Type   | Description                                                                                                                                                                                                                                                             |
| :------------ | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | string | Plugin name. Resolves within the same marketplace as the declaring plugin. Required.                                                                                                                                                                                    |
| `version`     | string | A [semver range](https://github.com/npm/node-semver#ranges) such as `~2.1.0`, `^2.0`, `>=1.4`, or `=2.1.0`. The dependency is fetched at the highest tagged version that satisfies this range.                                                                          |
| `marketplace` | string | A different marketplace to resolve `name` in. Cross-marketplace dependencies are blocked unless the target marketplace is listed in [`allowCrossMarketplaceDependenciesOn`](#depend-on-a-plugin-from-another-marketplace) in the root marketplace's `marketplace.json`. |

The `version` field accepts any expression supported by Node's `semver` package, including caret, tilde, hyphen, and comparator ranges. Pre-release versions such as `2.0.0-beta.1` are excluded unless your range opts in with a pre-release suffix like `^2.0.0-0`.

## Depend on a plugin from another marketplace

By default, Claude Code refuses to auto-install a dependency that lives in a different marketplace than the plugin declaring it. This prevents one marketplace from silently pulling in plugins from a source you have not reviewed.

To allow it, the maintainer of the root marketplace adds the target marketplace name to `allowCrossMarketplaceDependenciesOn` in `marketplace.json`. The root marketplace is the one that hosts the plugin the user is installing; only its allowlist is consulted, so trust does not chain through intermediate marketplaces.

The following `marketplace.json` allows `deploy-kit` to depend on a plugin from `acme-shared`:

```json .claude-plugin/marketplace.json theme={null}
{
  "name": "acme-tools",
  "owner": { "name": "Acme" },
  "allowCrossMarketplaceDependenciesOn": ["acme-shared"],
  "plugins": [
    {
      "name": "deploy-kit",
      "source": "./deploy-kit",
      "dependencies": [
        { "name": "audit-logger", "marketplace": "acme-shared" }
      ]
    }
  ]
}
```

If the field is missing or does not include the target marketplace, install fails with a `cross-marketplace` error naming the field to set. Users can still install the dependency manually first, which satisfies the constraint without changing the allowlist.

## Tag plugin releases for version resolution

Version constraints resolve against git tags on the marketplace repository. For Claude Code to find a dependency's available versions, the upstream plugin's releases must be tagged using a specific naming convention.

Tag each release as `{plugin-name}--v{version}`, where `{version}` matches the `version` field in that commit's `plugin.json`.

```bash theme={null}
git tag secrets-vault--v2.1.0
git push origin secrets-vault--v2.1.0
```

The plugin name prefix lets one marketplace repository host multiple plugins with independent version lines. The `--v` separator is parsed as a prefix match on the full plugin name, so plugin names that contain hyphens are handled correctly.

When you install a plugin that declares `{ "name": "secrets-vault", "version": "~2.1.0" }`, Claude Code lists the marketplace's tags, filters to those starting with `secrets-vault--v`, and fetches the highest version satisfying `~2.1.0`. If no matching tag exists, the dependent plugin is disabled with an error listing the available versions.

<Note>
  For `npm` marketplace sources, the constraint does not control which version is fetched, since tag-based resolution applies only to git-backed sources. The constraint is still checked at load time, and the dependent plugin is disabled with `dependency-version-unsatisfied` if the installed version does not satisfy it.
</Note>

## How constraints interact

When several installed plugins constrain the same dependency, Claude Code intersects their ranges and resolves the dependency to the highest version that satisfies all of them. The table below shows how common combinations resolve.

| Plugin A requires | Plugin B requires | Result                                                                                          |
| :---------------- | :---------------- | :---------------------------------------------------------------------------------------------- |
| `^2.0`            | `>=2.1`           | One install at the highest `2.x` tag at or above `2.1.0`. Both plugins load.                    |
| `~2.1`            | `~3.0`            | Install of plugin B fails with `range-conflict`. Plugin A and the dependency stay as they were. |
| `=2.1.0`          | none              | The dependency stays at `2.1.0`. Auto-update skips newer versions while plugin A is installed.  |

Auto-update checks each constrained dependency against every installed plugin's range before applying an update. If the marketplace moves a dependency to a version outside any range, the update is skipped and the skip message names the constraining plugin.

When you uninstall the last plugin that constrains a dependency, the dependency is no longer held and resumes tracking its marketplace entry on the next update.

## Resolve dependency errors

Dependency problems surface in `claude plugin list`, in the `/plugin` interface, and in `/doctor`. The affected plugin is disabled until you resolve the error. The most common errors and their fixes are listed below.

| Error                            | Meaning                                                                                                                                                                                                                           | How to resolve                                                                                                                                                         |
| :------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `range-conflict`                 | The version requirements for a dependency cannot be combined. The error message names the cause: no version satisfies all of the ranges, a range is not valid semver syntax, or the combined ranges are too complex to intersect. | Uninstall or update one of the conflicting plugins, fix any invalid `version` string, simplify long `\|\|` chains, or ask the upstream author to widen its constraint. |
| `dependency-version-unsatisfied` | The installed dependency's version is outside this plugin's declared range.                                                                                                                                                       | Run `claude plugin install <dependency>@<marketplace>` to re-resolve the dependency against all current constraints.                                                   |
| `no-matching-tag`                | The dependency's repository has no `{name}--v*` tag satisfying the range.                                                                                                                                                         | Check that the upstream has tagged releases using the convention above, or relax your range.                                                                           |

To check for these errors programmatically, run `claude plugin list --json` and read the `errors` field on each plugin.

## See also

* [Create plugins](/en/plugins): build plugins with skills, agents, and hooks
* [Create and distribute a plugin marketplace](/en/plugin-marketplaces): host plugins for your team
* [Plugins reference](/en/plugins-reference#plugin-manifest-schema): the full `plugin.json` schema
* [Version management](/en/plugins-reference#version-management): semantic versioning guidance for plugin releases
