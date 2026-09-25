> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Publish and distribute a plugin

> Publish a Claude Code plugin through your own marketplace or Anthropic's community marketplace, with a pre-release checklist and how users get updates.

Publishing a Claude Code plugin means listing it in a marketplace, a JSON catalog that lists plugins and where to fetch each one, so that other people can install it by name and receive your updates. You can run your own marketplace or submit your plugin to Anthropic's community marketplace. To share a plugin without publishing it, send people the plugin's directory or a `.zip` of it to load themselves.

This page is for the author of a working plugin who is ready to share it.

<Note>
  These cases are covered on other pages:

  * **Your plugin isn't finished yet**: start with [Create a plugin](/docs/en/plugins/create)
  * **You maintain a CLI or SDK with a plugin in an official marketplace**: see [Recommend your plugin from your CLI](/docs/en/plugins/cli-hints)
</Note>

Start with [Choose how to distribute](#choose-how-to-distribute) to compare the distribution options. If you already know your route, go to [Prepare your plugin for release](#prepare-your-plugin-for-release), then follow your route's section for what to tell your users and how they receive your updates.

## Choose how to distribute

Choose a distribution option based on who needs to install the plugin:

| Route                                                                     | Who can install                                                                     | What you need                                                                                  | Do users get your updates automatically? |
| :------------------------------------------------------------------------ | :---------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- | :--------------------------------------- |
| [No marketplace](#share-a-plugin-without-a-marketplace)                   | The people you send the plugin folder or a `.zip` of it                             | The plugin's folder                                                                            | None. They load the copy you sent        |
| [Your own marketplace](#publish-through-your-own-marketplace)             | Anyone who can reach the repository, which can be a private one your team can clone | A git repository or other host with a `.claude-plugin/marketplace.json` that lists your plugin | Off                                      |
| [Anthropic's community marketplace](#submit-to-the-community-marketplace) | Anyone who adds `anthropics/claude-plugins-community`                               | A submission through the plugin directory submission form                                      | Off                                      |

Auto-update is a per-marketplace setting on the user's side that fetches new versions in the background.

## Prepare your plugin for release

The name, the version, validation, and an install from a marketplace decide whether a release works for the people who install it. Check them before the first release and again before each later one.

<Steps>
  <Step title="Choose a permanent name">
    Users install, enable, and configure your plugin by `name@marketplace`, so a renamed plugin is a different plugin to every existing install. Choose a kebab-case name such as `deploy-helper`, because `claude plugin validate` warns on other forms, and treat it as permanent. Set `displayName` in `plugin.json` for the label users see.
  </Step>

  <Step title="Decide how you'll version">
    If you set `version` in `plugin.json` and later push commits without changing it, `claude plugin update` prints `<name> is already at the latest version (1.0.0).` and users keep the old copy. Either increment `version` on every release, or omit it in a git-hosted marketplace so Claude Code uses the commit SHA instead. See [Versions and updates](/docs/en/plugins/loading#versions-and-updates).
  </Step>

  <Step title="Validate">
    In your shell, run `claude plugin validate --strict ./your-plugin`. A clean run prints `✔ Validation passed`.

    * **In CI**: keep `--strict`, which also fails the run with exit code 1 on warnings such as an unknown manifest field or a missing `version`. Drop `--strict` if you chose to omit `version` in the previous step.
    * **Paths**: validation reports component paths that don't start with `./`. Inside hook commands and MCP server configs, refer to files as `${CLAUDE_PLUGIN_ROOT}/...`. See [path rules](/docs/en/plugins/manifest-reference#path-rules).
  </Step>

  <Step title="Install it from a local marketplace">
    In your shell, add a local marketplace that lists the plugin with `claude plugin marketplace add ./path-to-marketplace`, install the plugin from it, and start a session to confirm it loads.

    * For the smallest marketplace that works, see [Create a marketplace](/docs/en/plugins/create-marketplace).
    * To know whether an install loads your source directory or a cached copy, see [In-place and copied plugins](/docs/en/plugins/loading#in-place-and-copied-plugins).
  </Step>

  <Step title="Fill in the metadata users see">
    Set `description`, `author`, `homepage`, and `repository` in `plugin.json`, and add a `README.md` at the plugin root. `homepage` must parse as a URL. The [manifest reference](/docs/en/plugins/manifest-reference#fields) lists every field.
  </Step>

  <Step title="Run your eval suite">
    If you have an eval suite, run `claude plugin eval` in your shell. It runs the plugin's test cases and scores the results, which catches regressions when you change the plugin. See [Test plugins with evals](/docs/en/plugin-evals).
  </Step>
</Steps>

## Share a plugin without a marketplace

If the plugin is in a git repository, people can clone it and load the checkout, or start Claude Code from their shell with `--plugin-url` pointed at a `.zip` you attach to a release. To get your next version they pull or download again. If it isn't in a repository, send them the directory or a `.zip` of it. They load it in one of two ways:

* **For one session**: they start Claude Code from their shell with `claude --plugin-dir ./deploy-helper`, where the path is the clone, the unzipped folder, or the `.zip` itself. See [Flags that load a plugin for one session](/docs/en/plugins/cli-reference#flags-that-load-a-plugin-for-one-session).
* **For every session**: they move the plugin directory, with its `.claude-plugin/plugin.json`, under `~/.claude/skills/` so Claude Code [loads it in every session](/docs/en/plugins/loading#find-where-a-plugin-came-from).

Adding a `.claude-plugin/marketplace.json` to that same repository is what lets people install by name and update with a command; see [Publish through your own marketplace](#publish-through-your-own-marketplace).

### Ship a plugin with your own tool

If you maintain a CLI or SDK, publish the plugin in a marketplace and have your installer or post-install message run or print the two commands a user needs: `claude plugin marketplace add <source>`, then `claude plugin install <name>@<marketplace>`. For in-session discovery when someone uses your tool, see [Recommend your plugin from your CLI](/docs/en/plugins/cli-hints).

## Publish through your own marketplace

Your own marketplace is a `.claude-plugin/marketplace.json` file that lists your plugin, added to a git repository. Once the file is in the repository, the plugin is published, with no submission form. You can keep the file in the plugin's own repository or in a separate one.

### Add the marketplace file to your repository

To publish from the plugin's own repository, save the marketplace file beside `plugin.json` in `.claude-plugin/`, with one entry whose `source` is `"./"`, the repository root. Give the entry the same `name` as `plugin.json`, per [Keep the entry name and the manifest name the same](/docs/en/plugins/create-marketplace#keep-the-entry-name-and-the-manifest-name-the-same):

```json .claude-plugin/marketplace.json theme={null}
{
  "name": "your-marketplace",
  "owner": { "name": "Your Name" },
  "plugins": [
    { "name": "deploy-helper", "source": "./" }
  ]
}
```

In your shell, run `claude plugin validate .` in the repository to check the file before you push.

[Create a marketplace](/docs/en/plugins/create-marketplace) covers the layout with several plugins in one repository.

### Control who can install

Anyone who can clone the repository can install from it, so if the repository is private, the marketplace is private too. For hosts other than a git repository, see [Host a marketplace](/docs/en/plugins/host-marketplace). To reach everyone at a company, including people who don't use git, see [Roll out to a whole company](/docs/en/plugins/host-marketplace#roll-out-to-a-whole-company).

### Tell users how to install

Tell your users to add the marketplace and then install the plugin from their shell, replacing the source and names with yours:

* Add the marketplace once: `claude plugin marketplace add your-org/your-marketplace`, where the argument is a GitHub `owner/repo` shorthand, a URL, or a path
* Install the plugin: `claude plugin install deploy-helper@your-marketplace`
* Or do both from inside a session: `/plugin install deploy-helper --marketplace your-org/your-marketplace`. Requires Claude Code v2.1.275 or later. See [Add a marketplace and install in one command](/docs/en/plugins/install#add-a-marketplace-and-install-in-one-command)

### Ship updates to users

Users receive a release when they ask for it or when auto-update is on for your marketplace:

* **On request**: `claude plugin update deploy-helper@your-marketplace` in the user's shell refreshes the marketplace and installs the new copy when your plugin's version has changed
* **Auto-update**: off by default for your marketplace. See [Turn on auto-update](/docs/en/plugins/host-marketplace#turn-on-auto-update). Once on, it does the same as `claude plugin update` on a delay after the session starts

[Install plugins](/docs/en/plugins/install) covers the user-side commands, and [when auto-update runs](/docs/en/plugins/loading#when-auto-update-runs) covers the timing.

## Submit to the community marketplace

Anthropic's community marketplace, `claude-community`, is the public marketplace that lists plugins submitted through the plugin directory submission form.

Users add the community marketplace in a Claude Code session with `/plugin marketplace add anthropics/claude-plugins-community` and install from it as `@claude-community`.

For how the community marketplace differs from the official marketplace, see [Anthropic's marketplaces](/docs/en/plugins/anthropic-marketplaces).

To submit your plugin to the community marketplace, use one of the in-app forms:

* **claude.ai**: [claude.ai/admin-settings/directory/submissions/plugins/new](https://claude.ai/admin-settings/directory/submissions/plugins/new)
* **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

The claude.ai form requires a Team or Enterprise organization and the Directory permission, which Owners hold by default. Individual authors who aren't part of a Team or Enterprise organization can use the Console form instead.

In your shell, run `claude plugin validate ./your-plugin` locally before you submit, replacing `./your-plugin` with the path to your plugin directory. When validation passes, Claude Code prints `✔ Validation passed`, or `✔ Validation passed with warnings` if there are warnings. Warnings don't fail validation; add `--strict` to treat them as errors.

Listed plugins appear in the [`anthropics/claude-plugins-community`](https://github.com/anthropics/claude-plugins-community) catalog, in nearly every case pinned to a specific commit SHA.

There can be a delay between submitting and your plugin appearing in `marketplace.json`. To check whether your plugin is installable yet, search for its name in the [community catalog](https://github.com/anthropics/claude-plugins-community/blob/main/.claude-plugin/marketplace.json).

The official marketplace, `claude-plugins-official`, doesn't take submissions through these forms. If you work with an Anthropic partner contact, ask them about an official-marketplace listing.

## Ship updates, renames, and removals

### Release a new version

If you publish through your own marketplace and your `plugin.json` sets `version`, increment it and push. Users who run `claude plugin update` or have auto-update on then receive the new version, as described under [Ship updates to users](#ship-updates-to-users).

### Tag a release

Tag the release in git when other plugins declare a version range on yours, because those ranges resolve against tags. Otherwise you don't need a tag.

To tag, run `claude plugin tag` in your shell from the plugin directory. It creates a `{name}--v{version}` tag. Add `--push` to send the tag to `origin`. The [`plugin tag` reference](/docs/en/plugins/cli-reference#plugin-tag) lists its flags.

### Rename or remove a plugin

Never change a published plugin's `name`. After a rename, users who already installed it lose the plugin, because their install is recorded under the old name. A `renames` entry in your marketplace file migrates them instead. Change `displayName` when you want a different label.

If a rename is unavoidable, use the marketplace file's `renames` map so that existing installs migrate instead of failing with [`Plugin "<name>" not found in marketplace`](/docs/en/plugins/troubleshooting#plugin-not-found-in-marketplace). To remove a plugin from the marketplace, or for the full `renames` details, see [Rename or remove a plugin](/docs/en/plugins/host-marketplace#rename-or-remove-a-plugin) on the hosting page. The [marketplace reference](/docs/en/plugins/marketplace-reference#top-level-fields) has the field.

## Declare dependencies

If your plugin needs another plugin from the same marketplace to be enabled, list it in the `dependencies` array of `plugin.json`. Each entry is a bare name or an object with a semver `version` range. When a user installs your plugin, Claude Code installs and enables the dependency too.

[Plugin dependencies](/docs/en/plugins/dependencies) covers the range syntax, cross-marketplace dependencies, and how users prune dependencies they no longer need.

## Next steps

* [Host and maintain a marketplace](/docs/en/plugins/host-marketplace): release new versions and keep users up to date
* [Plugin dependencies](/docs/en/plugins/dependencies): declare and version the plugins yours relies on
* [Recommend your plugin from your CLI](/docs/en/plugins/cli-hints): prompt Claude Code users of your CLI to install the plugin
* [Measure plugin cost and usage](/docs/en/plugins/measure): see what your plugin costs in context and whether people use it
