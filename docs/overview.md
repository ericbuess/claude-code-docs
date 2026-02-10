> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code overview

> Claude Code is an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools. Available in your terminal, IDE, desktop app, and browser.

Claude Code is an agentic coding tool that reads your codebase, edits files, and runs commands. It works in your terminal, IDE, browser, and as a desktop app.

## Get started

Choose your environment to get started. Most surfaces require a [Claude subscription](https://claude.com/pricing) or [Anthropic Console](https://console.anthropic.com/) account. The Terminal CLI and VS Code also support [third-party providers](/en/third-party-integrations).

<Tabs>
  <Tab title="Terminal">
    The full-featured CLI for working with Claude Code directly in your terminal. Edit files, run commands, and manage your entire project from the command line.

    To install Claude Code, use one of the following methods:

    <Tabs>
      <Tab title="Native Install (Recommended)">
        **macOS, Linux, WSL:**

        ```bash  theme={null}
        curl -fsSL https://claude.ai/install.sh | bash
        ```

        **Windows PowerShell:**

        ```powershell  theme={null}
        irm https://claude.ai/install.ps1 | iex
        ```

        **Windows CMD:**

        ```batch  theme={null}
        curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
        ```

        <Info>
          Native installations automatically update in the background to keep you on the latest version.
        </Info>
      </Tab>

      <Tab title="Homebrew">
        ```sh  theme={null}
        brew install --cask claude-code
        ```

        <Info>
          Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
        </Info>
      </Tab>

      <Tab title="WinGet">
        ```powershell  theme={null}
        winget install Anthropic.ClaudeCode
        ```

        <Info>
          WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
        </Info>
      </Tab>
    </Tabs>

    Then start Claude Code in any project:

    ```bash  theme={null}
    cd your-project
    claude
    ```

    You'll be prompted to log in on first use. That's it! [Continue with the Quickstart →](/en/quickstart)

    <Tip>
      See [advanced setup](/en/setup) for installation options, manual updates, or uninstallation instructions. Visit [troubleshooting](/en/troubleshooting) if you hit issues.
    </Tip>
  </Tab>

  <Tab title="VS Code">
    The VS Code extension provides inline diffs, @-mentions, plan review, and conversation history directly in your editor.

    * [Install for VS Code](vscode:extension/anthropic.claude-code)
    * [Install for Cursor](cursor:extension/anthropic.claude-code)

    Or search for "Claude Code" in the Extensions view (`Cmd+Shift+X` on Mac, `Ctrl+Shift+X` on Windows/Linux). After installing, open the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`), type "Claude Code", and select **Open in New Tab**.

    [Get started with VS Code →](/en/vs-code#get-started)
  </Tab>

  <Tab title="Desktop app">
    A standalone app for running Claude Code outside your IDE or terminal. Review diffs visually, run multiple sessions side by side, and kick off cloud sessions.

    Download and install:

    * [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) (Intel and Apple Silicon)
    * [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) (x64)

    After installing, launch Claude, sign in, and click the **Code** tab to start coding.

    [Learn more about the desktop app →](/en/desktop#installation-and-setup)
  </Tab>

  <Tab title="Web">
    Run Claude Code in your browser with no local setup. Kick off long-running tasks and check back when they're done, work on repos you don't have locally, or run multiple tasks in parallel. Available on desktop browsers and the Claude iOS app.

    Start coding at [claude.ai/code](https://claude.ai/code).

    [Get started on the web →](/en/claude-code-on-the-web#getting-started)
  </Tab>

  <Tab title="JetBrains">
    A plugin for IntelliJ IDEA, PyCharm, WebStorm, and other JetBrains IDEs with interactive diff viewing and selection context sharing.

    Install the [Claude Code plugin](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) from the JetBrains Marketplace and restart your IDE.

    [Get started with JetBrains →](/en/jetbrains)
  </Tab>
</Tabs>

## What you can do

Here are some of the ways you can use Claude Code:

<AccordionGroup>
  <Accordion title="Automate the work you keep putting off" icon="wand-magic-sparkles">
    Claude Code handles the tedious tasks that eat up your day: writing tests for untested code, fixing lint errors across a project, resolving merge conflicts, updating dependencies, and writing release notes.

    ```bash  theme={null}
    claude "write tests for the auth module, run them, and fix any failures"
    ```
  </Accordion>

  <Accordion title="Build features and fix bugs" icon="hammer">
    Describe what you want in plain language. Claude Code plans the approach, writes the code across multiple files, and verifies it works.

    For bugs, paste an error message or describe the symptom. Claude Code traces the issue through your codebase, identifies the root cause, and implements a fix. See [common workflows](/en/common-workflows) for more examples.
  </Accordion>

  <Accordion title="Create commits and pull requests" icon="code-branch">
    Claude Code works directly with git. It stages changes, writes commit messages, creates branches, and opens pull requests.

    ```bash  theme={null}
    claude "commit my changes with a descriptive message"
    ```

    In CI, you can automate code review and issue triage with [GitHub Actions](/en/github-actions) or [GitLab CI/CD](/en/gitlab-ci-cd).
  </Accordion>

  <Accordion title="Connect your tools with MCP" icon="plug">
    The [Model Context Protocol (MCP)](/en/mcp) is an open standard for connecting AI tools to external data sources. With MCP, Claude Code can read your design docs in Google Drive, update tickets in Jira, pull data from Slack, or use your own custom tooling.
  </Accordion>

  <Accordion title="Customize with instructions, skills, and hooks" icon="sliders">
    [`CLAUDE.md`](/en/claude-md) is a markdown file you add to your project root that Claude Code reads at the start of every session. Use it to set coding standards, architecture decisions, preferred libraries, and review checklists.

    Create [custom slash commands](/en/skills) to package repeatable workflows your team can share, like `/review-pr` or `/deploy-staging`.

    [Hooks](/en/hooks) let you run shell commands before or after Claude Code actions, like auto-formatting after every file edit or running lint before a commit.
  </Accordion>

  <Accordion title="Run agent teams and build custom agents" icon="users">
    Spawn [multiple Claude Code agents](/en/sub-agents) that work on different parts of a task simultaneously. A lead agent coordinates the work, assigns subtasks, and merges results.

    For fully custom workflows, the [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) lets you build your own agents powered by Claude Code's tools and capabilities, with full control over orchestration, tool access, and permissions.
  </Accordion>

  <Accordion title="Pipe, script, and automate with the CLI" icon="terminal">
    Claude Code is composable and follows the Unix philosophy. Pipe logs into it, run it in CI, or chain it with other tools:

    ```bash  theme={null}
    # Monitor logs and get alerted
    tail -f app.log | claude -p "Slack me if you see any anomalies"

    # Automate translations in CI
    claude -p "translate new strings into French and raise a PR for review"

    # Bulk operations across files
    git diff main --name-only | claude -p "review these changed files for security issues"
    ```

    See the [CLI reference](/en/cli-reference) for the full set of commands and flags.
  </Accordion>

  <Accordion title="Work from anywhere" icon="globe">
    Start a task on your laptop and pick it up on your phone. [Claude Code on the web](/en/claude-code-on-the-web) and the [Claude iOS app](https://apps.apple.com/app/claude-by-anthropic/id6473753684) run sessions on cloud infrastructure, so you can kick off work from anywhere without a local dev environment.

    You can also route coding tasks straight from team chat: mention `@Claude` in [Slack](/en/slack) with a bug report or feature request, and get a pull request back.
  </Accordion>
</AccordionGroup>

## Use Claude Code everywhere

Each surface connects to the same underlying Claude Code engine, so your CLAUDE.md files, settings, and MCP servers work across all of them.

Beyond the [Terminal](/en/quickstart), [VS Code](/en/vs-code), [JetBrains](/en/jetbrains), [Desktop](/en/desktop), and [Web](/en/claude-code-on-the-web) environments above, Claude Code integrates with CI/CD, chat, and browser workflows:

| I want to...                                  | Best option                                                                                                        |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Start a task locally, continue on mobile      | [Web](/en/claude-code-on-the-web) or [Claude iOS app](https://apps.apple.com/app/claude-by-anthropic/id6473753684) |
| Automate PR reviews and issue triage          | [GitHub Actions](/en/github-actions) or [GitLab CI/CD](/en/gitlab-ci-cd)                                           |
| Route bug reports from Slack to pull requests | [Slack](/en/slack)                                                                                                 |
| Debug live web applications                   | [Chrome](/en/chrome)                                                                                               |
| Build custom agents for your own workflows    | [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)                                                |

## Next steps

Once you've installed Claude Code, these guides help you go deeper.

* [Quickstart](/en/quickstart): walk through your first real task, from exploring a codebase to committing a fix
* Level up with [best practices](/en/best-practices) and [common workflows](/en/common-workflows)
* [Settings](/en/settings): customize Claude Code for your workflow
* [Troubleshooting](/en/troubleshooting): solutions for common issues
* [code.claude.com](https://code.claude.com/): demos, pricing, and product details
