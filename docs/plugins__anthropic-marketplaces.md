> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Anthropic's marketplaces

> Anthropic's official, community, and demo plugin marketplaces for Claude Code: their names, repositories, how you add each, and where to browse their plugins.

Anthropic publishes three general-purpose plugin marketplaces for Claude Code: [official](https://github.com/anthropics/claude-plugins-official), [community](https://github.com/anthropics/claude-plugins-community), and [demo](https://github.com/anthropics/claude-code). Each is a catalog of plugins in its own GitHub repository. When you install a plugin from one of them in a Claude Code session, you type the marketplace's name after `@`, as in `/plugin install commit-commands@claude-plugins-official`.

Use this page to distinguish the three marketplaces and to find where to check whether the official one holds a given plugin.

<Note>
  These cases are covered on other pages:

  * **How to install a plugin**: see [Install plugins](/docs/en/plugins/install)
  * **A failed install**: see [Troubleshoot plugins](/docs/en/plugins/troubleshooting)
</Note>

Go to the part of the page you need:

* To distinguish the three marketplaces by repository, marketplace name, and how you get each one, see [Anthropic's marketplaces](#anthropic’s-marketplaces).
* To find a plugin in the official marketplace, see [Find plugins in the official marketplace](#find-plugins-in-the-official-marketplace).

## Anthropic's marketplaces

A marketplace is a catalog of plugins that a repository defines in its `.claude-plugin/marketplace.json` file. The official, community, and demo marketplaces each come from their own GitHub repository. Anthropic also publishes topic-specific marketplaces, such as `anthropics/skills` and `anthropics/knowledge-work-plugins`, which you add in a Claude Code session with `/plugin marketplace add <owner>/<repo>`.

This table gives each marketplace's repository and marketplace name, which is what you type after `@` when you install a plugin from that marketplace. The community marketplace's name is `claude-community`, not its repository name.

|                  | Official                                                                                                                                                                                                                                                                                                                                                                                   | Community                                                                                              | Demo                                                                                      |
| :--------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------- |
| Repository       | [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official)                                                                                                                                                                                                                                                                                              | [`anthropics/claude-plugins-community`](https://github.com/anthropics/claude-plugins-community)        | [`anthropics/claude-code`](https://github.com/anthropics/claude-code/tree/main/plugins)   |
| Marketplace name | `claude-plugins-official`                                                                                                                                                                                                                                                                                                                                                                  | `claude-community`                                                                                     | `claude-code-plugins`                                                                     |
| What's in it     | Plugins Anthropic maintains, plus plugins from partners and other authors                                                                                                                                                                                                                                                                                                                  | Third-party plugins that their authors submitted to Anthropic                                          | A small set of example plugins that show what a plugin can contain                        |
| How you get it   | Claude Code adds it the first time you start an interactive terminal session, unless a [managed policy](/docs/en/plugins/org#allow-the-official-marketplace-and-your-own) or `CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL` blocks it. See [Marketplace `claude-plugins-official` not found](/docs/en/plugins/troubleshooting#marketplace-claude-plugins-official-not-found) if it's missing | You add it in a Claude Code session with `/plugin marketplace add anthropics/claude-plugins-community` | You add it in a Claude Code session with `/plugin marketplace add anthropics/claude-code` |

If you wrote a plugin and want other people to install it, see [Publish a plugin](/docs/en/plugins/publish), which covers your own marketplace and submitting to the community marketplace.

### The demo marketplace in `anthropics/claude-code`

If a tutorial or an older set of instructions tells you to run `/plugin marketplace add anthropics/claude-code`, that adds the demo marketplace, named `claude-code-plugins`. It isn't the official marketplace, which Claude Code already added for you.

Most of the demo marketplace's plugins are also in the official marketplace under the same names. For example, `code-review`, `feature-dev`, `commit-commands`, and `security-guidance` are in both. Install those from `claude-plugins-official` so you don't have two copies installed.

## Find plugins in the official marketplace

The official marketplace, `claude-plugins-official`, is the one Claude Code adds for you. Most of what it lists comes from partners and other authors rather than from Anthropic: tool vendors publish plugins that connect Claude Code to their services, and Anthropic maintains a smaller set of its own, such as `commit-commands`, `code-review`, `feature-dev`, and the [language server plugins](/docs/en/plugins/code-intelligence). The catalog changes often, so this page doesn't list it.

To see what's in it, use the **Discover** tab of `/plugin` in a Claude Code session, which you can search, or browse [Claude Marketplace](https://claude.com/marketplace/plugins) on the web.

## Browse and install from Anthropic's marketplaces

You can search Anthropic's marketplaces for a plugin in Claude Code, on the web, or on GitHub:

* **In Claude Code, by browsing**: run `/plugin` in an interactive session. Its **Discover** tab lists the plugins from the marketplaces you've added.
* **In Claude Code, by name**: run `/plugin install <name>` in a session, which looks the name up in the marketplaces you've added. If the plugin is in one of them, its details open in the `/plugin` panel, and nothing installs until you choose an [installation scope](/docs/en/plugins/install#install-a-plugin) and confirm there. If it isn't, you see `Plugin "<name>" not found in any marketplace`.
* **On the web**: search the full catalog on [Claude Marketplace](https://claude.com/marketplace/plugins), which shows install counts and marks some plugins **Anthropic verified**.
* **On GitHub**: open `.claude-plugin/marketplace.json` in the marketplace's repository, such as [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official). That file is the catalog itself.

To install from the desktop app or from a script, or to see what a cloud session loads, see [Install plugins](/docs/en/plugins/install).

### Add the community or demo marketplace

The community and demo marketplaces aren't registered until you add them in a Claude Code session:

* **Community**: run `/plugin marketplace add anthropics/claude-plugins-community`, then install with the `@claude-community` suffix.
* **Demo**: run `/plugin marketplace add anthropics/claude-code`, then install with the `@claude-code-plugins` suffix.

If `claude-plugins-official` isn't on the **Marketplaces** tab of `/plugin`, add it the same way with `/plugin marketplace add anthropics/claude-plugins-official`.

For `not found` errors and marketplaces that won't add, see [Troubleshoot plugins](/docs/en/plugins/troubleshooting#install-a-plugin).

## Third-party marketplaces

Many popular plugins aren't in any Anthropic marketplace. They're in their authors' own marketplaces, usually a GitHub repository with a `.claude-plugin/marketplace.json` at its root.

Anthropic doesn't review third-party marketplaces, so read [Plugin security and trust](/docs/en/plugins/security) before you add one.

To use a third-party marketplace, add its repository in a Claude Code session with `/plugin marketplace add <owner>/<repo>`, then install with `/plugin install <plugin>@<marketplace-name>`. The marketplace name is the `name` field of that `marketplace.json`, and Claude Code prints it once it has added the marketplace.

For other ways to add a marketplace, see [Add a marketplace](/docs/en/plugins/install#add-a-marketplace).

## Next steps

* [Install and manage plugins](/docs/en/plugins/install): install a plugin from one of these marketplaces and choose a scope
* [Plugin security and trust](/docs/en/plugins/security): what a plugin can do on your machine and how to review one before you install it
* [Code intelligence plugins](/docs/en/plugins/code-intelligence): install one of the official marketplace's language-server plugins
* [Create a marketplace](/docs/en/plugins/create-marketplace): run your own marketplace alongside Anthropic's
