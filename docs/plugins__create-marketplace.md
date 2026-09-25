> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Create a marketplace

> Build a plugin marketplace from a marketplace.json file and test it locally before you host it.

A plugin marketplace is a directory or repository with a `.claude-plugin/marketplace.json` file that lists your plugins and where to fetch each one. You push the directory to a git host, and anyone with access registers it in Claude Code with one command and installs your plugins from it.

Create your own marketplace when you want a group you choose, such as your team or your organization, to install your plugins and keep receiving your updates from a catalog you control. The repository can be private, it can list as many plugins as you like, and an administrator can [require it on every machine](/docs/en/plugins/org).

<Note>
  These cases are covered on other pages:

  * **Sharing one plugin with a few people**: send them the plugin's directory or a `.zip` of it. See [Share a plugin without a marketplace](/docs/en/plugins/publish#share-a-plugin-without-a-marketplace).
  * **Offering a plugin to everyone**: submit it to Anthropic's community marketplace. See [Submit to the community marketplace](/docs/en/plugins/publish#submit-to-the-community-marketplace).
  * **Using a plugin yourself**: load it with `--plugin-dir` or save it in your skills directory. See [Develop without a marketplace](/docs/en/plugins/create#develop-without-a-marketplace).
</Note>

Start with [Create a marketplace](#create-a-marketplace) to build one on your own machine and install a plugin from it, then [add more plugin entries](#add-plugin-entries).

## Create a marketplace

The following steps create a marketplace on your machine, add a plugin to it, register it in Claude Code, and install the plugin from it. That is the whole loop, and it's the same loop your users go through once you host the marketplace somewhere they can reach. Run every command in your shell, from the directory where you want `my-marketplace/` created.

You need a plugin to list. The example uses `my-first-plugin` from [Create your first plugin](/docs/en/plugins/create#create-your-first-plugin), a plugin with one skill that you run as `/my-first-plugin:hello`; build it first if you don't have a plugin yet. To use a plugin of your own instead, substitute its directory and its `name` wherever the steps say `my-first-plugin`. For what a plugin directory can contain, see the [plugin directory explorer](/docs/en/plugins/components#explore-the-plugin-directory).

<Steps>
  <Step title="Set up the marketplace directory">
    A marketplace is a directory with a `.claude-plugin/marketplace.json` file, plus the plugins it lists. Create the marketplace directory and its `.claude-plugin/` folder, then copy your plugin in under `plugins/`:

    ```bash theme={null}
    mkdir -p my-marketplace/.claude-plugin my-marketplace/plugins
    cp -r my-first-plugin my-marketplace/plugins/
    ```

    Check that the plugin is valid where it now sits, so that any later error is about the marketplace and not the plugin:

    ```bash theme={null}
    claude plugin validate ./my-marketplace/plugins/my-first-plugin
    ```

    The last line of the output reads `✔ Validation passed`.
  </Step>

  <Step title="Create the marketplace file">
    Save `marketplace.json` at `my-marketplace/.claude-plugin/marketplace.json`. The file requires a `name`, an `owner`, and a `plugins` array.

    Each object in `plugins` is a plugin entry and needs a `name` and a `source`. Write the entry's `source` as a path from the marketplace root. The root is `my-marketplace/`, the directory that contains `.claude-plugin/`.

    ```json my-marketplace/.claude-plugin/marketplace.json theme={null}
    {
      "name": "my-marketplace",
      "description": "Plugins for my team",
      "owner": {
        "name": "Your Name"
      },
      "plugins": [
        {
          "name": "my-first-plugin",
          "source": "./plugins/my-first-plugin",
          "description": "A greeting plugin to learn the basics"
        }
      ]
    }
    ```
  </Step>

  <Step title="Validate the marketplace">
    Run `claude plugin validate` on the marketplace directory to check the JSON syntax, the required fields, and each plugin entry in its `.claude-plugin/marketplace.json`.

    ```bash theme={null}
    claude plugin validate ./my-marketplace
    ```

    For the file as written in step 2, the last line of the output reads `✔ Validation passed`.
  </Step>

  <Step title="Add the marketplace and install the plugin">
    Register the directory as a marketplace.

    ```bash theme={null}
    claude plugin marketplace add ./my-marketplace
    ```

    The command prints `✔ Successfully added marketplace: my-marketplace (declared in user settings)`, which means the marketplace is recorded in your user settings file.

    Install the plugin. The install id is the entry's `name`, an `@`, and the marketplace `name`.

    ```bash theme={null}
    claude plugin install my-first-plugin@my-marketplace
    ```

    The command prints `✔ Successfully installed plugin: my-first-plugin@my-marketplace (scope: user)`.

    Inside a session, `/plugin marketplace add ./my-marketplace` registers the marketplace the same way. `/plugin install my-first-plugin@my-marketplace` opens the plugin's details in the `/plugin` panel, where you install it. For that flow, see [Install and manage plugins](/docs/en/plugins/install).
  </Step>

  <Step title="Confirm the plugin loaded">
    List installed plugins.

    ```bash theme={null}
    claude plugin list
    ```

    The output lists `my-first-plugin@my-marketplace` with `Status: ✔ enabled`.

    To see what the plugin loaded, show its details.

    ```bash theme={null}
    claude plugin details my-first-plugin
    ```

    The `Component inventory` section reads `Skills (1)  hello`.

    To run the skill, start a session and enter `/my-first-plugin:hello`. Claude greets you. The command has the plugin's name as a prefix, as every plugin skill's name does.
  </Step>
</Steps>

## Add plugin entries

Every plugin you distribute is one object in the `plugins` array of `marketplace.json`. To add a second plugin, add a second object. These fields cover most entries:

* `name`: the identifier people type before `@` when they install. It can't contain spaces.
* `source`: where Claude Code fetches the plugin from. Write a relative path string for a plugin inside the marketplace directory, as in [the walkthrough](#create-a-marketplace), or a source object for a plugin outside it. See [Choose a plugin source](#choose-a-plugin-source).
* `description`: the line people see next to the plugin when they browse your marketplace in `/plugin`.

For the full field list, see [Plugin entries](/docs/en/plugins/marketplace-reference#plugin-entries).

An entry can also set any [`plugin.json`](/docs/en/plugins/manifest-reference) field. For when an entry's `plugin.json` fields apply to a plugin that has its own `plugin.json`, see [Entry and plugin.json](/docs/en/plugins/marketplace-reference#entry-and-plugin-json).

## Rules for plugin entries

Most failed installs from a new marketplace come from a relative path written from the wrong directory, or from an entry name that differs from the `name` in the plugin's `plugin.json`.

### Write relative paths from the marketplace root

The marketplace root is the directory that contains `.claude-plugin/`. In [the walkthrough](#create-a-marketplace), that's `my-marketplace/`, so the entry's `source` is `"./plugins/my-first-plugin"`. The path doesn't start inside `.claude-plugin/`, so don't use `..` to leave it.

A path with `..` and a path to a missing directory fail at different commands:

* **A path with `..`**: `claude plugin validate` reports the entry as invalid. The message begins `Path contains "..": ./../plugins/my-first-plugin`.
* **A path to a directory that doesn't exist**: `claude plugin validate` passes. `claude plugin install` fails with `Source path does not exist: <path>`, and `<path>` is the absolute location Claude Code checked.

### Keep the entry name and the manifest name the same

A marketplace plugin has an entry `name` in `marketplace.json` and a `name` in its own `plugin.json`, called the manifest name. Each name appears in different places:

* **Entry name**: the install id, `<entry-name>@<marketplace>`. It's what people type to install, what `claude plugin list` shows, and the key Claude Code writes under [`enabledPlugins`](/docs/en/settings-reference#enabledplugins) in their settings file.
* **Manifest name**: the prefix on the plugin's skills, and the name `claude plugin details` takes.

When the two names differ and someone installs by the manifest name, Claude Code reports `Plugin "<manifest-name>" not found in marketplace "<marketplace>"`. Keep the two names the same. For more on how Claude Code uses the two names, see [Plugin loading reference](/docs/en/plugins/loading#find-where-a-plugin-came-from).

## Choose a plugin source

Each plugin entry in `marketplace.json` has a `source` that tells Claude Code where to fetch that one plugin. Pick the source by where the plugin's files are stored. The table lists the sources most marketplace owners use.

| Source        | Use it when                                                               | Minimal `source` value                                                                    |
| :------------ | :------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------- |
| Relative path | The plugin's files are inside the marketplace directory itself            | `"./plugins/my-first-plugin"`                                                             |
| `github`      | The plugin is a GitHub repository of its own                              | `{ "source": "github", "repo": "your-org/my-first-plugin" }`                              |
| `git-subdir`  | The plugin is a subdirectory of some other repository, such as a monorepo | `{ "source": "git-subdir", "url": "your-org/monorepo", "path": "tools/my-first-plugin" }` |

In a `git-subdir` source, `url` takes a git URL or an `owner/repo` GitHub shorthand.

A plugin can also come from one of these source types:

* `url`: a git repository by URL, on any host
* `archive`: a zip file downloaded over HTTPS
* `npm`: an npm package
* `command`: a directory produced by running a command on the machine where the plugin is installed

For the fields of every source type, and for pinning a git-based source to a `ref` or `sha`, see [Plugin sources](/docs/en/plugins/marketplace-reference#plugin-sources).

## Validate and test

As you add plugins, run `claude plugin validate ./my-marketplace` in your shell after every edit, and install from the marketplace on your own machine before you share it. Validation and installation catch different problems.

### Problems that validation reports

`claude plugin validate` reads only files inside the marketplace directory. It reports:

* JSON syntax errors, as `json: Invalid JSON syntax: <reason>`
* Missing required fields, such as `owner: Invalid input`
* A marketplace name with spaces, non-ASCII characters, or a form that imitates an official Anthropic marketplace, such as `claude-official`
* A relative `source` that contains `..`
* Unknown fields at the top level or in a plugin entry, as warnings
* Problems in the `plugin.json` of each relative-path plugin, as `plugins[N] plugin.json → <field>: <message>`

For every message `validate` can print, see [Validation messages](/docs/en/plugins/marketplace-reference#validation-messages). For its flags and exit codes, see [`plugin validate`](/docs/en/plugins/cli-reference#plugin-validate).

### Problems that surface when you add or install

Problems that `claude plugin validate` doesn't report appear when you add the marketplace or install from it:

* **When you add the marketplace**: the exact [official marketplace names](/docs/en/plugins/marketplace-reference#reserved-names), such as `claude-plugins-official`, pass validation. When you add a marketplace with one of those names, Claude Code refuses it with a message that starts `The name '<name>' is reserved for official Anthropic marketplaces`.
* **When you install a plugin**:
  * Claude Code first fetches a `github`, `git-subdir`, or other remote source when you install the plugin, so a wrong `repo` or `path` appears then.
  * A relative `source` whose directory doesn't exist also fails at install, with `Source path does not exist: <path>`.

### Test an edit to a plugin

In [the walkthrough](#create-a-marketplace), you added `my-marketplace` from a local directory with a relative-path `source`. With that setup, Claude Code reads the plugin's files directly from `my-marketplace/plugins/`. Your edits take effect at the next session start or when you run `/reload-plugins` in a session, with no change to the plugin's `version`.

People who install from your hosted marketplace get a copy in the plugin cache instead. For how they receive a new version, see [Keep users up to date](/docs/en/plugins/host-marketplace#keep-users-up-to-date).

### Remove the marketplace to start over

To remove everything and start over, run `claude plugin marketplace remove my-marketplace` in your shell. The command removes the marketplace and uninstalls its plugins.

## Host your marketplace

Once you can install a plugin from the marketplace on your own machine, as in [Create a marketplace](#create-a-marketplace), push the marketplace directory to a git host.

Your teammates then run `claude plugin marketplace add <owner>/<repo>` in their shell for a GitHub repository, or the same command with the repository URL. They then install a plugin by name as in [the walkthrough](#create-a-marketplace).

For private-repository access, updates, versioning, and renaming or removing entries, see [Host and maintain a marketplace](/docs/en/plugins/host-marketplace).

## Next steps

* [Host and maintain a marketplace](/docs/en/plugins/host-marketplace): pick a host, keep users up to date, and rename or remove plugins safely
* [Marketplace reference](/docs/en/plugins/marketplace-reference): `marketplace.json` fields and source types
* [Manage plugins for your organization](/docs/en/plugins/org): require your marketplace and its plugins on every machine
* [Suggest plugins by relevance](/docs/en/plugins/relevance): have Claude Code suggest a plugin from your marketplace when a session matches
