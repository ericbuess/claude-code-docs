> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Create a Claude Code plugin

> Build your first Claude Code plugin from an empty directory, test it without a marketplace, and convert an existing .claude/ setup.

A plugin is a directory of skills, agents, hooks, and MCP servers, plus a `plugin.json` file, called the manifest, that names the plugin. Claude Code loads the directory as one unit, so you can share it with teammates, install it in several projects, or publish it to a marketplace.

This page is for people writing their own plugins.

<Note>
  These cases are covered on other pages:

  * **Installing someone else's plugin**: see [Install plugins](/docs/en/plugins/install)
  * **Not sure you need a plugin**: see [Decide whether you need a plugin](/docs/en/plugins/overview#decide-whether-you-need-a-plugin) on the overview
  * **Your plugin's users are on claude.ai or in Cowork**: the same folder installs there with a different subset of components. See [Plugin structure and testing](https://claude.com/docs/plugins/build) and the [component support table](https://claude.com/docs/plugins/platform-support#compare-component-support-by-app)
</Note>

Start from the section that matches what you already have:

* **Nothing yet**: follow [Create your first plugin](#create-your-first-plugin), then [Develop without a marketplace](#develop-without-a-marketplace) and [Test and debug](#test-and-debug).
* **Files under `.claude/` already**: do the first-plugin walkthrough once to learn the layout, then follow [Convert an existing `.claude/` setup](#convert-an-existing-claude-setup).

## Decide when to use a plugin

Skills, agents, hooks, and MCP servers all work standalone in your project or home directory. Keep that standalone setup while it serves one project or only you. Make a plugin when you want to share the setup with teammates, install it in several projects, or publish versioned releases.

When you move standalone skills, agents, hooks, and MCP config into a plugin, their location and names change:

* **Where the files go**: under the plugin's own directory, called the plugin root, as `skills/`, `agents/`, `hooks/hooks.json`, and `.mcp.json`.
* **How they're named**: plugin skills and agents get the plugin name as a prefix, such as `/my-plugin:hello`, so two plugins can each provide a `hello` skill without colliding.

To move an existing setup into a plugin, see [Convert an existing `.claude/` setup](#convert-an-existing-claude-setup).

## Create your first plugin

In this walkthrough, you create a plugin whose only component is one skill, a greeting, and run it with `--plugin-dir`, which loads a plugin for one session without installing it. A plugin can hold any mix of [components](/docs/en/plugins/components), such as skills, agents, hooks, and MCP servers, and none is required; one skill is the smallest example that shows the layout.

You need Claude Code [installed and signed in](/docs/en/quickstart#step-1-install-claude-code).

Open a terminal in the directory where you want to keep the plugin, such as `~/projects`, and run the commands in these steps from it. You can keep a plugin anywhere, because you pass its path to Claude Code when you start a session.

<Steps>
  <Step title="Create the plugin directory">
    Create the plugin directory, with a `.claude-plugin/` folder inside it to hold the manifest:

    ```bash theme={null}
    mkdir -p my-first-plugin/.claude-plugin
    ```
  </Step>

  <Step title="Write the manifest">
    The [manifest](/docs/en/plugins/manifest-reference) is a JSON file named `plugin.json` that tells Claude Code the plugin's name and describes it. Save this one as `my-first-plugin/.claude-plugin/plugin.json`:

    ```json my-first-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "my-first-plugin",
      "description": "A greeting plugin to learn the basics",
      "version": "1.0.0",
      "author": {
        "name": "Your Name"
      }
    }
    ```

    The four fields do this:

    * **`name`**: required. It identifies the plugin and becomes the prefix on every skill and agent the plugin provides. Don't put spaces in it.
    * **`description`**: the text users see for the plugin in `/plugin`.
    * **`version`**: optional. Setting it keeps users on that version until you change it; [Release a new version](/docs/en/plugins/host-marketplace#release-a-new-version) says when to set or omit it.
    * **`author`**: who to credit. `name` is required inside it; `email` and `url` are optional.

    Every other field is on the [manifest reference](/docs/en/plugins/manifest-reference#fields).

    Only `plugin.json` goes inside `.claude-plugin/`. The skill you add next goes directly under `my-first-plugin/`, next to that folder.
  </Step>

  <Step title="Add a skill">
    This plugin's one component is a skill. Each skill is a directory under `skills/` that contains a `SKILL.md` file. Create the skill's directory:

    ```bash theme={null}
    mkdir -p my-first-plugin/skills/hello
    ```

    Then create `my-first-plugin/skills/hello/SKILL.md` with this content:

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    name: hello
    description: Greet the user with a friendly message
    disable-model-invocation: true
    ---

    Greet the user warmly and ask how you can help them today.
    ```

    The `disable-model-invocation: true` line means Claude doesn't run the skill on its own, so only you trigger it. Remove that line from a skill you want Claude to run on its own. The skill's command combines the plugin name and the skill's name, so you run this one as `/my-first-plugin:hello`. For the other frontmatter fields, see the [skill frontmatter reference](/docs/en/skills#frontmatter-reference).
  </Step>

  <Step title="Validate the plugin">
    Check the manifest and the skill's frontmatter before you run anything:

    ```bash theme={null}
    claude plugin validate ./my-first-plugin
    ```

    The command prints the manifest path it checked and `✔ Validation passed`. If it prints `✘ Validation failed` instead, each line above that result line names the field to fix. Look up each message under [`claude plugin validate` reports errors](/docs/en/plugins/troubleshooting#claude-plugin-validate-reports-errors).
  </Step>

  <Step title="Run Claude Code with the plugin">
    Start a session with the plugin loaded:

    ```bash theme={null}
    claude --plugin-dir ./my-first-plugin
    ```

    Once Claude Code starts, run the skill:

    ```text theme={null}
    /my-first-plugin:hello
    ```

    Claude replies with a greeting.
  </Step>
</Steps>

The plugin loads only in sessions you start with `--plugin-dir`. To keep working on it without the flag, or to test a `.zip` build, see [Develop without a marketplace](#develop-without-a-marketplace).

To have Claude scaffold and check a larger plugin with you, [install](/docs/en/plugins/install#install-a-plugin) Anthropic's `plugin-dev` plugin from the `claude-plugins-official` marketplace, which adds skills and agents for writing components such as skills, hooks, and MCP servers and for validating the finished plugin. Once it's installed, run `/plugin-dev:create-plugin` followed by a description of the plugin you want, and Claude walks you through designing, creating, and validating it.

<h3 id="share-the-plugin">
  Share your plugin
</h3>

A plugin you built with [Create your first plugin](#create-your-first-plugin) exists only on your machine. When it's ready for other people, there are three ways to get it to them:

* **Send it to a few people directly**: give them the plugin's directory or a `.zip` of it, and nothing needs to be published. See [Share a plugin without a marketplace](/docs/en/plugins/publish#share-a-plugin-without-a-marketplace).
* **List it in your own marketplace**: teammates add your marketplace once and install the plugin by name, and they receive your updates. See [Publish through your own marketplace](/docs/en/plugins/publish#publish-through-your-own-marketplace).
* **Submit it to Anthropic's directory**: after it passes review, people can add it on claude.ai and in Cowork, and it reaches Claude Code through their account. See [Submit to Anthropic's directory](/docs/en/plugins/publish#submit-to-anthropics-directory).

### Plugin layout

Each kind of [component](/docs/en/plugins/components), such as skills, agents, hooks, and MCP servers, goes in a fixed directory under the plugin root, which is the directory you pass to `--plugin-dir`. Add only the directories you use. To click through a complete plugin directory and read what each file does, open the [plugin explorer](/docs/en/plugins/components#explore-the-plugin-directory).

The table lists the directories most plugins start with, and the [full layout](/docs/en/plugins/manifest-reference#standard-layout) lists the rest.

| Location                     | Contents                                                                                                                          |
| :--------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| `.claude-plugin/plugin.json` | The manifest. When you load a plugin with `--plugin-dir` and it has no manifest, Claude Code names the plugin after its directory |
| `skills/`                    | One `<name>/SKILL.md` directory per skill                                                                                         |
| `commands/`                  | Flat Markdown files, the older form of skills. Use `skills/` for new plugins                                                      |
| `agents/`                    | One Markdown file per subagent                                                                                                    |
| `hooks/hooks.json`           | Hook configuration: a top-level `"hooks"` key whose value has the same shape as `hooks` in a settings file                        |
| `.mcp.json`                  | MCP server definitions                                                                                                            |

<Warning>
  Only `plugin.json` goes inside `.claude-plugin/`. Components saved there don't load.

  The plugin root is the plugin's own directory, not `~/.claude/` itself. A `.mcp.json` saved at `~/.claude/.mcp.json` doesn't load.
</Warning>

## Develop without a marketplace

You don't need a [marketplace](/docs/en/plugins/overview#get-plugins-from-a-marketplace) to run a plugin you're writing. Load it directly from disk or a URL instead:

* [`--plugin-dir`](#load-a-directory-or-archive-for-one-session): loads a directory or `.zip` archive for one session.
* [`--plugin-url`](#fetch-an-archive-from-a-url-for-one-session): fetches a `.zip` archive from a URL for one session.
* [`claude plugin init`](#scaffold-a-plugin-that-loads-every-session): scaffolds a plugin under `~/.claude/skills/` that loads every session.

If two plugins loaded in different ways share a name, see [Name conflicts](/docs/en/plugins/loading#name-conflicts) for which one Claude Code keeps.

<h3 id="load-a-directory-or-archive-for-one-session">
  Load a plugin for one session
</h3>

You can load a plugin for a single session in three ways: from a directory or `.zip` archive on disk with `--plugin-dir`, from a URL with `--plugin-url`, or from an environment variable when you can't add a flag. Each plugin loads for that session only, and nothing is written to your settings for it. When you edit the plugin's files during the session, run `/reload-plugins` to load the changes.

#### From a directory or `.zip`

When you start `claude` from your shell, pass `--plugin-dir` with the plugin's root directory or a `.zip` archive of it. Repeat the flag to load several plugins:

```bash theme={null}
claude --plugin-dir ./my-first-plugin --plugin-dir ./other-plugin.zip
```

<h4 id="load-a-folder-of-plugins">
  From a folder of plugins
</h4>

To load several plugins from one place, pass a folder that holds them, such as `--plugin-dir ./plugins`. Loading a folder of plugins requires Claude Code v2.1.265 or later.

If the folder has no `.claude-plugin/` directory and no plugin components at its top level, Claude Code treats it as a folder of plugins. Each immediate subfolder that has a `.claude-plugin/plugin.json` manifest then loads as a separate plugin. Everything else in the folder is skipped without an error, including a subfolder that has no manifest. If a plugin in the folder doesn't load, check that its subfolder has a `.claude-plugin/plugin.json`.

In an interactive session, you can also add and remove plugins in the folder after startup:

* A subfolder you add loads as a new plugin once its manifest exists.
* When you remove a subfolder, its plugin unloads.

A message appears in the session for each of these changes. If loading or unloading a plugin mid-conversation would [invalidate the prompt cache](/docs/en/prompt-caching#enabling-or-disabling-a-plugin), the change is held instead, and the message tells you to run `/reload-plugins` to apply it.

<h4 id="fetch-an-archive-from-a-url-for-one-session">
  From a URL
</h4>

When you start `claude` from your shell, pass `--plugin-url` with the address of a `.zip` archive, such as a build artifact your CI publishes:

```bash theme={null}
claude --plugin-url https://example.com/my-first-plugin.zip
```

Claude Code downloads the archive at startup. To load several, repeat the flag or pass the URLs space-separated in one quoted argument.

Point the flag only at archives you control or trust.

If Claude Code can't fetch the archive, or the archive is invalid, it starts without the plugin and records a plugin load error that you can review in the `/plugin` manager's **Errors** tab.

#### From an environment variable

To load plugins in a session where you can't add the `--plugin-dir` flag, list their absolute paths in the [`CLAUDE_CODE_PLUGIN_DIRS`](/docs/en/env-vars#variables) environment variable instead. Claude Code loads each path as it loads a `--plugin-dir` path. These plugins load in addition to any you pass with `--plugin-dir`. [Project and local settings can't set this variable](/docs/en/settings-reference#variables-claude-code-ignores-in-env). `CLAUDE_CODE_PLUGIN_DIRS` requires Claude Code v2.1.280 or later.

Managed settings can turn off `--plugin-dir` and `CLAUDE_CODE_PLUGIN_DIRS`. See [Flags that load a plugin for one session](/docs/en/plugins/cli-reference#flags-that-load-a-plugin-for-one-session). To test a plugin together with a plugin it depends on, see [Test a plugin and its dependency locally](/docs/en/plugins/dependencies#test-a-plugin-and-its-dependency-locally).

<h3 id="scaffold-a-plugin-that-loads-every-session">
  Make a plugin load in every session
</h3>

Your personal skills directory is `~/.claude/skills/`. Claude Code loads any folder there that contains a `.claude-plugin/plugin.json` as a plugin in every session, with no flag and no install step. `claude plugin init` scaffolds one of these plugins for you.

#### Scaffold the plugin with `claude plugin init`

`claude plugin init` writes a starter plugin under `~/.claude/skills/`. Requires Claude Code v2.1.157 or later. Scaffold one from your shell:

```bash theme={null}
claude plugin init my-tool
```

The command creates `~/.claude/skills/my-tool/` with a `.claude-plugin/plugin.json` and a root `SKILL.md`. It prints `✔ Created plugin "my-tool" at ~/.claude/skills/my-tool` followed by `It will auto-load next session as my-tool@skills-dir. Run /reload-plugins to load it now.`

Pass `--with skills` to have `claude plugin init` scaffold a skill under `skills/` for you. The other `--with` values are on the [plugin commands reference](/docs/en/plugins/cli-reference#plugin-init).

<h4 id="skill-names-in-a-scaffolded-plugin">
  Name the plugin's skills
</h4>

The root skill at `~/.claude/skills/my-tool/SKILL.md` is also a personal skill, so you invoke it as `/my-tool`, not `/my-tool:my-tool`. Skills you add under `skills/` inside the plugin get the plugin-name prefix, such as `/my-tool:example`.

#### Stop loading the plugin

To stop loading a scaffolded plugin, delete its directory, or run `claude plugin disable my-tool@skills-dir` in your shell with the `my-tool@skills-dir` name that `claude plugin init` printed. In the ID `my-tool@skills-dir`, `skills-dir` stands where a marketplace name would, because the plugin loads from your skills directory rather than from a marketplace.

<h4 id="load-a-plugin-for-everyone-in-one-repository">
  Share the plugin through a repository
</h4>

`claude plugin init` writes the plugin to your personal skills directory at `~/.claude/skills/`, so it loads for you in every project. To make a plugin load for everyone in one repository, create the same layout yourself at `<project>/.claude/skills/<name>/`, including its `.claude-plugin/plugin.json`. See [Plugins shared through a repository](/docs/en/plugins/loading#plugins-shared-through-a-repository) for the conditions under which Claude Code loads it.

## Test and debug

When a change to your plugin doesn't show up, work through these checks in order. Each one tells you what Claude Code did with the plugin:

1. In your shell, run `claude plugin validate <path>`. It checks the manifest and the frontmatter of every skill, agent, and command file, and exits `0` on `Validation passed`. Add `--strict` to fail on warnings too. Exit codes and directory handling are on the [plugin commands reference](/docs/en/plugins/cli-reference#plugin-validate).
2. In the running session, run `/reload-plugins` to apply edits you made on disk. It prints one `Reloaded:` line with counts. Then confirm a skill loaded by typing its `/plugin-name:skill` command, or by finding the plugin in the `/plugin` **Installed** tab.
3. In the same session, run `/plugin`. The **Installed** tab lists your plugin and, in the plugin's details, the components Claude Code found. The **Errors** tab lists what failed to load and why, such as a path in your manifest that doesn't exist.
4. Back in your shell, run `claude plugin list`. It prints session-only and skills-directory plugins in their own sections with `Status: ✔ loaded` or the load error. To include the plugin you're developing, pass `--plugin-dir` with its path before `plugin list`.

To check an MCP server, run `/mcp` in the session to see the server's status. When the server is healthy, `/mcp` lists it as connected. If it isn't, see [MCP servers that don't start](/docs/en/plugins/troubleshooting#invalid-mcp-server-config-for-and-mcp-servers-that-dont-start).

To check a hook, trigger the event it matches. For example, ask Claude to edit a file to trigger a `PostToolUse` hook. Then read the [debug log](/docs/en/hooks#debug-hooks), which shows which hooks matched, their exit codes, and their output.

The next sections cover the failures you're most likely to hit while developing, and the [troubleshooting page](/docs/en/plugins/troubleshooting#build-a-plugin) has the full entry for each.

### A component path isn't found

The **Errors** tab of `/plugin` shows `<component> path not found: <path>`, for example `commands path not found`. A component path in your manifest, such as `commands`, `skills`, `agents`, or `hooks`, points at nothing. Fix the path or create the directory, then run `/reload-plugins` in the session. See [`commands path not found`](/docs/en/plugins/troubleshooting#commands-path-not-found).

### `--plugin-dir` at a marketplace root doesn't load the plugins under `plugins/`

`--plugin-dir` takes the plugin's root directory, the one that contains `.claude-plugin/plugin.json` and the component directories such as `skills/`. If you point it at a marketplace root instead, Claude Code doesn't read `marketplace.json`, so a plugin under `plugins/` doesn't load, and you see no error. Point the flag at one plugin's folder, or add the marketplace. See [the troubleshooting entry](/docs/en/plugins/troubleshooting#plugin-dir-loads-a-plugin-with-no-components).

### The plugin loads but its skills are missing

The `skills/` directory is inside `.claude-plugin/`, or a `skills` entry in the manifest points at a file. Move `skills/` to the plugin root, point each `skills` entry at a directory that contains `SKILL.md`, and run `/reload-plugins` in the session. See [Plugin loads but its skills are missing](/docs/en/plugins/troubleshooting#plugin-loads-but-its-skills-are-missing).

### The `userConfig` dialog never appears

The dialog for your plugin's [`userConfig`](/docs/en/plugins/components#user-configuration) options is part of installing through `/plugin` in a session. Loading with `--plugin-dir` doesn't show it, and neither does `claude plugin install` in the shell. With the plugin loaded, run `/plugin configure <plugin-name>` in the session to open it. See [The `userConfig` dialog never appears](/docs/en/plugins/troubleshooting#the-userconfig-dialog-never-appears).

### Check that the plugin changes Claude's behavior

A plugin that loads without errors can still fail to steer Claude the way you intend. `claude plugin eval`, which you run in your shell, runs your test cases with and without the plugin and scores the difference. See [Test plugins with evals](/docs/en/plugin-evals), starting with [Create your first eval suite](/docs/en/plugin-evals#create-your-first-eval-suite).

<h2 id="convert-an-existing-claude-setup">
  Convert an existing `.claude/` setup
</h2>

If you already have skills, agents, or hooks under a project's `.claude/` directory, you can move them into a plugin without rewriting them.

Run the commands in these steps from the project root, which is the directory that contains `.claude/`, because the `cp` paths are relative to it.

<Steps>
  <Step title="Create the plugin structure">
    Create the plugin directory and its `.claude-plugin/` folder alongside `.claude/`. You can move the plugin anywhere afterwards.

    ```bash theme={null}
    mkdir -p my-plugin/.claude-plugin
    ```

    Create `my-plugin/.claude-plugin/plugin.json`:

    ```json my-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "my-plugin",
      "description": "Migrated from standalone configuration",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Copy your existing files">
    Copy each configuration directory you have to the plugin root, and skip the command for any directory you don't have.

    ```bash theme={null}
    cp -r .claude/commands my-plugin/
    ```

    ```bash theme={null}
    cp -r .claude/agents my-plugin/
    ```

    ```bash theme={null}
    cp -r .claude/skills my-plugin/
    ```

    Run `ls -a my-plugin` to confirm that each directory you copied appears next to `.claude-plugin`.
  </Step>

  <Step title="Move your hooks">
    If you have hooks in `.claude/settings.json` or `.claude/settings.local.json`, create a hooks directory:

    ```bash theme={null}
    mkdir -p my-plugin/hooks
    ```

    Create `my-plugin/hooks/hooks.json` and copy the `hooks` object from your settings file into it. The format is the same.

    This example shows the shape with one hook that runs a linter on each file Claude writes or edits. Replace the example with your own `hooks` object.

    ```json my-plugin/hooks/hooks.json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }]
          }
        ]
      }
    }
    ```
  </Step>

  <Step title="Test the migrated plugin">
    Load the plugin for a session:

    ```bash theme={null}
    claude --plugin-dir ./my-plugin
    ```

    Check each component under its new name:

    * **Skills**: run `/my-plugin:deploy` for a skill that was `/deploy`.
    * **Subagents**: ask Claude to use the `my-plugin:reviewer` agent for an agent that was `reviewer`.
    * **Hooks**: trigger the event each hook matches.

    If something is missing, work through [Test and debug](#test-and-debug).
  </Step>
</Steps>

While the originals are still under `.claude/`, they stay loaded alongside the plugin's copies:

* **Skills and agents**: the two sets don't collide, because the plugin's skills and agents carry the `my-plugin:` prefix. `/deploy` and `/my-plugin:deploy` both work, and Claude sees `reviewer` and `my-plugin:reviewer` as two subagents.
* **Hooks**: hooks have no prefix, so a hook that is in both your settings file and `hooks/hooks.json` runs twice each time its event fires.

After you've confirmed the plugin works, delete the originals from `.claude/` and remove the `hooks` object from your settings file.

## Next steps

* [Plugin components](/docs/en/plugins/components): add agents, hooks, MCP servers, LSP servers, and user configuration to your plugin
* [Test plugins with evals](/docs/en/plugin-evals): write eval cases and run them with `claude plugin eval` to check how reliably the plugin guides Claude's behavior
* [Publish a plugin](/docs/en/plugins/publish): version it, put it in a marketplace, and submit it for review
* [Plugin structure and testing](https://claude.com/docs/plugins/build): the same plugin folder installs on claude.ai and in Cowork. Some components are Claude Code-only, and the [component support table](https://claude.com/docs/plugins/platform-support#compare-component-support-by-app) lists which load on each surface
* [Plugin manifest reference](/docs/en/plugins/manifest-reference): every `plugin.json` field, path rule, and directory
* [Skills](/docs/en/skills): write the skills your plugin provides
* [Anthropic's plugins in the claude-code repository](https://github.com/anthropics/claude-code/tree/main/plugins): complete worked examples of the layout on this page, such as `feature-dev` and `code-review`
