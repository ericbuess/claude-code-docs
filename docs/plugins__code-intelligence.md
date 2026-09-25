> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code intelligence plugins

> Install a language server plugin so Claude sees type errors after edits and navigates code by symbol, and answer the LSP plugin recommendation dialog.

A code intelligence plugin gives Claude the live diagnostics and go-to-definition that your editor has, so Claude catches type errors and missing imports that its own edits introduce before you run your build, and finds definitions and references by symbol instead of by text search.

Each plugin connects Claude Code to a language server for one language through the Language Server Protocol (LSP). You install the plugin from Anthropic's official marketplace and the language server binary on your machine.

<Note>
  Code intelligence plugins work in terminal sessions. In [cloud sessions](/docs/en/claude-code-on-the-web), Claude Code doesn't start plugin language servers, so Claude gets no diagnostics or code navigation there. To write your own language server plugin, or to connect a language server that has no plugin, see [LSP servers in plugin components](/docs/en/plugins/components#lsp-servers).
</Note>

To get started, find your language in the table under [Install a code intelligence plugin](#install-a-code-intelligence-plugin). The plugins in that table come from Anthropic's [official plugin marketplace](/docs/en/plugins/anthropic-marketplaces).

If you already saw an **LSP plugin recommendation** dialog, see [Accept or dismiss the recommendation dialog](#accept-or-dismiss-the-recommendation-dialog) for what each choice does.

## Install a code intelligence plugin

A code intelligence plugin tells Claude Code which command starts the language server and which file extensions it handles. It doesn't include the language server. Install the language server binary first, then the plugin, then confirm the server starts.

<Steps>
  <Step title="Install the language server binary">
    Find your language in the table below and install the binary in its row. If your language isn't listed, see [Add a language without an official plugin](#add-a-language-without-an-official-plugin).

    | Language                  | Plugin                                                                                                           | Binary                          |
    | :------------------------ | :--------------------------------------------------------------------------------------------------------------- | :------------------------------ |
    | C/C++                     | [`clangd-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/clangd-lsp)               | `clangd`                        |
    | C#                        | [`csharp-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/csharp-lsp)               | `csharp-ls`                     |
    | Go                        | [`gopls-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/gopls-lsp)                 | `gopls`                         |
    | Java                      | [`jdtls-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/jdtls-lsp)                 | `jdtls`                         |
    | Kotlin                    | [`kotlin-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/kotlin-lsp)               | `kotlin-lsp`                    |
    | Liquid                    | [`liquid-lsp`](https://github.com/Shopify/liquid-skills/tree/main/plugins/liquid-lsp)                            | `shopify`, from the Shopify CLI |
    | Lua                       | [`lua-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/lua-lsp)                     | `lua-language-server`           |
    | PHP                       | [`php-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/php-lsp)                     | `intelephense`                  |
    | Python                    | [`pyright-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pyright-lsp)             | `pyright-langserver`            |
    | Ruby                      | [`ruby-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ruby-lsp)                   | `ruby-lsp`                      |
    | Rust                      | [`rust-analyzer-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/rust-analyzer-lsp) | `rust-analyzer`                 |
    | Swift                     | [`swift-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/swift-lsp)                 | `sourcekit-lsp`                 |
    | TypeScript and JavaScript | [`typescript-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/typescript-lsp)       | `typescript-language-server`    |

    Anthropic maintains every plugin in the table except `liquid-lsp`, which Shopify maintains and the official marketplace lists.

    To find the command that installs the binary, follow the plugin's link in the table to its README. For TypeScript, that command is `npm install -g typescript-language-server typescript`.

    After you install the binary, confirm it's on the `PATH` of the shell you start `claude` from, for example with `which typescript-language-server`, or `Get-Command typescript-language-server` in PowerShell.
  </Step>

  <Step title="Install the plugin">
    To install the plugin listed for your language in the step 1 table, run `/plugin install` in a Claude Code session, replacing `typescript-lsp` with that plugin's name:

    ```
    /plugin install typescript-lsp@claude-plugins-official
    ```

    A confirmation message says whether the plugin is active now or needs `/reload-plugins`. If the install fails with `Marketplace "claude-plugins-official" not found`, see the [troubleshooting entry for that error](/docs/en/plugins/troubleshooting#marketplace-claude-plugins-official-not-found). To control where the plugin is installed, or to run the install from your shell instead of inside Claude Code, see [Install plugins](/docs/en/plugins/install).
  </Step>

  <Step title="Confirm the server starts">
    The language server starts the first time Claude edits a file with one of the plugin's extensions. To see it work, ask Claude to introduce a type error in a file of that language and then fix it. Then check the conversation for a diagnostics line:

    * **A diagnostics line appears**: `Found N new diagnostic issues in M files (ctrl+o to expand)` under the edit that introduced the error means the server started.
    * **No diagnostics line appears**: run `/plugin` and open the **Errors** tab. A row reading `Executable not found in $PATH: "<binary>"` names the binary to install. If the tab has no such row, see [Troubleshoot code intelligence](#troubleshoot-code-intelligence).

    After you install a missing binary, Claude Code tries again the next time Claude edits a matching file. If you installed the binary into a directory that isn't on the `PATH` of the shell you started `claude` from, start a new session from a shell where it is.
  </Step>
</Steps>

## See what Claude gains

With a language server running, Claude gains diagnostics and code navigation:

* **Diagnostics after edits**: each time Claude edits or writes a file the server handles, Claude gets the errors and warnings the server reports. It sees a type error, missing import, or syntax error it introduced without running a compiler.
* **Code navigation**: Claude gets an `LSP` tool that looks up symbols through the server instead of searching text for them. The tool is read-only. For what Claude can look up with the tool and how permissions apply to it, see [LSP tool behavior](/docs/en/tools-reference#lsp-tool-behavior).

### Read the diagnostics yourself

After Claude edits a file the server handles, the conversation shows only the `Found N new diagnostic issues` summary. To read the issues themselves, press **Ctrl+O**.

## Accept or dismiss the recommendation dialog

If a language server binary is already on your `PATH` and the plugin that uses it isn't installed, Claude Code offers to install the plugin for you in a dialog titled **LSP plugin recommendation**.

### When the recommendation dialog appears

The **LSP plugin recommendation** dialog can appear after Claude edits a file. These conditions decide whether it appears and which plugin it offers:

* **A plugin matches the file**: one of the marketplaces you've added, or the official marketplace Claude Code registered for you, lists a code intelligence plugin for that file's extension, and the plugin's binary is installed.
* **Official first**: when more than one marketplace offers a plugin for the extension, the dialog offers the official marketplace's plugin.
* **Once per session**: the dialog appears at most once in a session, for the first matching file Claude edits.
* **Not for cloud sessions**: the dialog never appears when your terminal is attached to a cloud session, such as one you started with [`claude --cloud`](/docs/en/claude-code-on-the-web#from-terminal-to-cloud).

### Respond to the recommendation dialog

The **LSP plugin recommendation** dialog names the plugin and offers these choices:

* **Yes, install**: Claude Code installs the plugin for your user account and prints `<plugin> installed · restart to apply`. Start a new session to load the server.
* **No, not now**: the dialog closes, and a later session can offer the plugin again. Pressing **Esc** does the same.
* **Never for this plugin**: the dialog stops appearing for that plugin and still appears for others.
* **Disable all LSP recommendations**: the dialog stops appearing for every language.

If you don't choose an option, Claude Code closes it after 30 seconds and counts that as ignored. The count is kept across sessions. After five ignored dialogs, Claude Code stops recommending plugins, the same as if you'd chosen **Disable all LSP recommendations**.

### Turn recommendations back on

The **LSP plugin recommendation** dialog stops appearing after you choose **Disable all LSP recommendations** or ignore it five times.

* **Disabled or ignored five times**: to turn it back on in either case, remove the `lspRecommendationDisabled` and `lspRecommendationIgnoredCount` keys from `~/.claude.json`, Claude Code's own configuration file.
* **Never for this plugin**: if you chose **Never for this plugin** and want that plugin offered again, remove its `name@marketplace` id from the `lspRecommendationNeverPlugins` list in the same file.

## Troubleshoot code intelligence

The plugins troubleshooting page covers the symptoms specific to code intelligence plugins under [Language server doesn't start, uses too much memory, or reports wrong diagnostics](/docs/en/plugins/troubleshooting#language-server-doesnt-start):

* **The language server doesn't start**: you see `Executable not found in $PATH` in the **Errors** tab of `/plugin`, or Claude never reports diagnostics for the language.
* **High memory use**: memory use increases while the server indexes the project.
* **False positive diagnostics in a monorepo**: diagnostics report imports as unresolved when they aren't.

## Add a language without an official plugin

If your language isn't in the [table of official plugins](#install-a-code-intelligence-plugin), you can still connect a language server.

1. Write a plugin with an `.lsp.json` file that names the server command and the file extensions it handles.
2. Then load the plugin with [`--plugin-dir`](/docs/en/plugins/cli-reference#flags-that-load-a-plugin-for-one-session) or publish it to a marketplace.

For the file's fields and a worked example, see [LSP servers in plugin components](/docs/en/plugins/components#lsp-servers).

## Next steps

* [LSP servers in plugin components](/docs/en/plugins/components#lsp-servers): write the `.lsp.json` for a language server that has no official plugin
* [Install and manage plugins](/docs/en/plugins/install): scopes, updates, and uninstalling
* [Troubleshoot plugins](/docs/en/plugins/troubleshooting): load errors beyond the language-server ones on this page
* [Find plugins in the official marketplace](/docs/en/plugins/anthropic-marketplaces#find-plugins-in-the-official-marketplace): where to browse the rest of the official marketplace
