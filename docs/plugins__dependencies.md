> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Plugin dependencies

> Declare the plugins your plugin depends on, with version ranges such as ^1.2, and see how Claude Code installs, resolves, and prunes them.

A plugin dependency is another plugin that your plugin relies on, such as one whose MCP server or skill it calls. Each dependency tracks the latest version its marketplace provides unless you declare a version constraint, a semantic-version range such as `^2.0` or `~2.1.0` that you've tested against.

This page is for plugin authors who declare dependencies in `plugin.json` and for marketplace maintainers who tag releases.

<Note>
  These cases are covered on other pages:

  * **Installing a plugin that has dependencies**: see [Manage installed plugins](/docs/en/plugins/install#manage-installed-plugins)
  * **Reading a dependency error**: see [Dependency errors](/docs/en/plugins/troubleshooting#dependency-errors)
  * **Declaring the npm and Bun packages that your plugin's own code needs**: see [Node.js package dependencies](/docs/en/plugins/loading#node-js-package-dependencies)
</Note>

To add a constraint, start at [Declare a dependency with a version constraint](#declare-a-dependency-with-a-version-constraint). If you maintain a plugin that others depend on, [tag your releases](#tag-plugin-releases-for-version-resolution) so their constraints can resolve.

## Declare dependencies

<span id="decide-whether-to-constrain-dependency-versions" />Without a version constraint, a dependency moves to each new release its marketplace publishes the next time users update. If that release renames an MCP tool your plugin calls, your plugin breaks for everyone who updates.

With a constraint such as `~2.1.0` on a dependency from a git-backed source, users who have your plugin installed keep receiving `2.1.x` patches of the dependency and never move to `2.2`. To upgrade on your own schedule, test against a newer release and then publish a new version of your plugin with a wider constraint.

### Declare a dependency with a version constraint

List dependencies in the `dependencies` array of your plugin's `.claude-plugin/plugin.json`. The following manifest declares one unversioned dependency and one constrained dependency:

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

An entry can be a string: the plugin name alone, such as `"audit-logger"` in this manifest, or `"name@marketplace"` to resolve it in another marketplace. With a bare string, your plugin depends on whatever version that plugin's marketplace provides.

To set a version constraint, use an object with these fields, each a string:

| Field         | Description                                                                                                                                                                                                                                                                                      |
| :------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | The dependency's plugin name, as it appears in its marketplace entry. Claude Code looks it up in the same marketplace as the declaring plugin unless you set `marketplace`. Required.                                                                                                            |
| `version`     | A [semantic-version range](https://github.com/npm/node-semver#ranges) such as `~2.1.0`, `^2.0`, `>=1.4`, or `=2.1.0`. The dependency installs at the highest git tag that satisfies this range, so the dependency's maintainer must [tag releases](#tag-plugin-releases-for-version-resolution). |
| `marketplace` | A different marketplace to resolve `name` in. An allowlist controls cross-marketplace dependencies, described in [Depend on a plugin from another marketplace](#depend-on-a-plugin-from-another-marketplace).                                                                                    |

A range doesn't match pre-release versions such as `2.0.0-beta.1` unless you opt in with a pre-release suffix such as `^2.0.0-0`.

### Bundle plugins for a team

To let engineers install a curated set of plugins with one command, publish a plugin whose manifest contains a `name` and a `dependencies` array. A plugin manifest needs only `name`, so this is a valid plugin, and installing it installs every dependency.

For example, a platform team can publish role-specific bundles in an internal marketplace so engineers run one `claude plugin install` instead of installing each plugin separately:

```json .claude-plugin/plugin.json theme={null}
{
  "name": "backend-standard",
  "version": "1.0.0",
  "description": "Standard plugin set for backend engineers",
  "dependencies": [
    "secrets-vault",
    "deploy-kit",
    { "name": "db-migrate", "version": "^3.0" },
    "oncall-runbook"
  ]
}
```

To add a plugin to the standard set later, publish a new `backend-standard` version with the extra dependency. When the marketplace doesn't [auto-update by default](/docs/en/plugins/loading#which-marketplaces-and-plugins-auto-update), engineers either turn on auto-update for the marketplace or update manually:

* **Turn on auto-update for the marketplace**: the next auto-update moves the bundle to the new version and installs any dependencies it adds.
* **Update manually**: run `claude plugin update backend-standard` in a shell, then `/reload-plugins` in an open session to install the newly added dependencies.

For the engineer-side steps, see [Keep plugins updated](/docs/en/plugins/install#keep-plugins-updated).

To deploy a bundle to everyone in an organization, an administrator adds it to `enabledPlugins` in managed settings. See [Pre-install and require plugins](/docs/en/plugins/org#pre-install-and-require-plugins).

### Depend on a plugin from another marketplace

By default, Claude Code doesn't install a dependency from a different marketplace than the declaring plugin's own, unless the user already has that dependency installed and enabled at the same scope. This default prevents one marketplace from silently installing plugins from a source the user hasn't reviewed.

To allow the install, add the target marketplace's name to `allowCrossMarketplaceDependenciesOn` in the root marketplace's `marketplace.json`. The root marketplace is the one that hosts the plugin the user is installing. Only the root marketplace's allowlist applies.

The following `marketplace.json` allows `deploy-kit` to depend on a plugin from `your-shared-marketplace`:

```json .claude-plugin/marketplace.json theme={null}
{
  "name": "your-marketplace",
  "owner": { "name": "Your Org" },
  "allowCrossMarketplaceDependenciesOn": ["your-shared-marketplace"],
  "plugins": [
    {
      "name": "deploy-kit",
      "source": "./deploy-kit",
      "dependencies": [
        { "name": "audit-logger", "marketplace": "your-shared-marketplace" }
      ]
    }
  ]
}
```

If `allowCrossMarketplaceDependenciesOn` is missing or doesn't include the target marketplace, Claude Code doesn't install the dependency. When the dependency is declared in the marketplace entry, the install itself is refused with a message that starts `Dependency "audit-logger@your-shared-marketplace" (required by deploy-kit@your-marketplace) is in marketplace "your-shared-marketplace", which is not in the allowlist` and names the field to set. When it's declared in `plugin.json`, the install completes without the dependency and your plugin then fails to load.

The allowlist check doesn't apply to a dependency that is already enabled. If a user installs `audit-logger` from `your-shared-marketplace` themselves first, at the same scope, `deploy-kit` then installs without any change to the allowlist.

### Test a plugin and its dependency locally

If you're developing a plugin and the plugin it depends on at the same time, start Claude Code from your shell and load both with [`--plugin-dir`](/docs/en/plugins/cli-reference#flags-that-load-a-plugin-for-one-session):

```bash theme={null}
claude --plugin-dir ./my-dependency --plugin-dir ./my-plugin
```

The local copy of the dependency satisfies your plugin's dependency entry, so you don't need to install the dependency from its marketplace.

* **No `version` needed**: the local `plugin.json` doesn't need a `version` either, because a [version constraint](#declare-a-dependency-with-a-version-constraint) isn't checked against a local copy.
* **Entries that name a marketplace**: an entry that names a marketplace also matches the local copy on Claude Code v2.1.242 or later.

Until you install the dependency from its marketplace, your plugin stops loading whenever the local copy is disabled or absent:

* **You disabled the local copy**: your plugin is disabled at the next plugin load, with an error that ends `is disabled — enable it or remove the dependency`. When the error names the dependency as `<name>@inline`, that identifier refers to the `--plugin-dir` copy.
* **You started a session without the dependency's `--plugin-dir` flag**: the error reports the dependency as not installed. Pass the flag again, or install the dependency from its marketplace.

When both plugins are in one parent folder, you can pass that folder to `--plugin-dir` once. If the folder isn't itself a plugin, Claude Code loads each child folder that has a `.claude-plugin/plugin.json`. Requires Claude Code v2.1.265 or later.

<h2 id="tag-plugin-releases-for-version-resolution">
  Release a plugin that others depend on
</h2>

If you maintain a plugin that other plugins depend on with a version constraint, tag its releases so those constraints can resolve. A constraint resolves against git tags on the repository that hosts the plugin. Tag the repository that the plugin's [plugin source](/docs/en/plugins/marketplace-reference#plugin-sources) in `marketplace.json` points at:

* **`github`, `url`, or `git-subdir` source**: the plugin's own repository, so the plugin's author creates the tags
* **Relative path such as `./plugins/secrets-vault`**: the marketplace repository, so the marketplace maintainer creates the tags

### Create a release tag

Tag each release as `<plugin-name>--v<version>`, where `<version>` matches the `version` field in that commit's `plugin.json`. The plugin-name prefix lets one marketplace repository host several plugins with independent version histories.

Create the tag from the plugin directory, with an `origin` remote configured to receive the pushed tag, using [`claude plugin tag`](/docs/en/plugins/cli-reference#plugin-tag):

```bash theme={null}
claude plugin tag --push
```

The command builds the tag name from the plugin's manifest. Before creating the tag, it runs these checks:

* Validates the plugin
* Checks that `plugin.json` and the marketplace entry agree on the version, when the plugin directory is inside a marketplace checkout
* Requires a clean working tree under the plugin directory
* Refuses if the tag already exists

A successful run prints `Created tag secrets-vault--v2.1.0`. With `--push`, it also prints `Pushed to origin`. Without `--push`, it prints the `git push` command to run yourself.

Pass `--dry-run` to see the plan without creating anything.

The [`claude plugin tag` reference](/docs/en/plugins/cli-reference#plugin-tag) lists the remaining flags.

You can also run `git tag secrets-vault--v2.1.0` directly, as long as you keep the `version` in `plugin.json` and in the marketplace entry in sync yourself.

### Constrain a dependency that has a non-git source

Tag-based resolution applies only to git-backed sources. For a dependency with an `npm`, `archive`, or `command` [plugin source](/docs/en/plugins/marketplace-reference#plugin-sources), the constraint doesn't control which version is fetched. It's still checked when the plugin loads, and the dependent plugin is disabled if the installed version doesn't satisfy it.

For `npm`, `archive`, and `command` sources, the version checked is the `version` in the dependency's `plugin.json`. Set one there before you constrain that dependency, because a `plugin.json` that sets no version satisfies no constraint.

Claude Code never installs a dependency with a `command` source itself, so users [install it first](/docs/en/plugins/marketplace-reference#command-plugin-source). It also never runs a dependency's [`headersHelper`](/docs/en/plugins/host-marketplace#authenticate-archive-downloads), so users also install a dependency whose marketplace entry sets one before they install your plugin.

Besides `claude plugin install`, these operations also install any missing declared dependency, and the `command` and `headersHelper` limits apply to them too:

* `/reload-plugins`
* Auto-update of the dependent plugin's marketplace
* Re-running `claude plugin install` on the dependent plugin
* `claude plugin marketplace add`

## How dependencies behave for your users

These sections describe how Claude Code resolves, checks, and combines the constraints you declare once your plugin is installed alongside others.

### How a constraint resolves against tags

When a user installs a plugin that declares `{ "name": "secrets-vault", "version": "~2.1.0" }`, the dependency installs from the highest `secrets-vault--v` tag that satisfies `~2.1.0` on the repository that hosts `secrets-vault`. When no tag satisfies the range, the install either fails or uses the marketplace's current copy:

* **Plugin with its own repository**: the install fails with a message containing `Dependency "secrets-vault@your-marketplace" has no git tag satisfying`.
* **Plugin referenced by a relative path**: the install uses the marketplace's current copy instead, and the constraint is checked when the plugin loads. If that copy is outside the range, the dependent plugin stays disabled and `claude plugin list` shows `Requires "secrets-vault@your-marketplace" ~2.1.0, installed 3.0.0`.

For a plugin the marketplace references by a relative path, a marketplace you added as a local folder path also resolves constraints against that folder's git tags, when the folder is a git repository. This requires Claude Code v2.1.196 or later. A local folder that isn't a git repository has no tags, so Claude Code installs the dependency from the folder's current contents instead.

### Confirm the resolved version

To confirm which version a constraint resolved to, run `claude plugin list` in your shell. A tag-resolved dependency shows its version with a 12-character commit suffix, such as `2.1.0-8713c5b11005`.

Constraint checks use the tag's version rather than the `version` in `plugin.json`, even if `plugin.json` at that commit lags behind.

If you force-move a tag to a different commit, the next install fetches that commit's content instead of reusing a stale cached copy. See [Versions and updates](/docs/en/plugins/loading#versions-and-updates) for how a plugin's version becomes its cache key.

### Combine constraints from several plugins

When several installed plugins constrain the same dependency, the dependency resolves to the highest version that satisfies all of their ranges. Common combinations resolve like this:

| Plugin A requires | Plugin B requires | Result                                                                                                                          |
| :---------------- | :---------------- | :------------------------------------------------------------------------------------------------------------------------------ |
| `^2.0`            | `>=2.1`           | One install at the highest `2.x` tag at or above `2.1.0`. Both plugins load.                                                    |
| `~2.1`            | `~3.0`            | Installing plugin B fails with a `has conflicting version requirements` message. Plugin A and the dependency stay as they were. |
| `=2.1.0`          | none              | The dependency stays at `2.1.0`. Auto-update skips newer versions while plugin A is installed.                                  |

Auto-update fetches a constrained dependency at the highest git tag that satisfies every installed plugin's range, rather than at the marketplace's latest version. If the installed plugins' ranges don't overlap, auto-update leaves that dependency at its current version, and the `/plugin` **Errors** tab shows an entry naming the constraining plugin. If they overlap but no tag falls in the range, auto-update fetches the marketplace's current copy and skips the update when that copy's `version` falls outside any installed plugin's range.

When a user uninstalls the last plugin that constrains a dependency, the dependency is no longer constrained to a version range and resumes tracking its marketplace entry on the next update.

## See also

* [`claude plugin prune`](/docs/en/plugins/cli-reference#plugin-prune): remove auto-installed dependencies no plugin needs anymore
* [Host a marketplace](/docs/en/plugins/host-marketplace): release channels and recommending other plugins
