# Claude Code overview

> Learn about Claude Code, Anthropic's agentic coding tool that lives in your terminal and helps you turn ideas into code faster than ever before.

## Get started in 30 seconds

Prerequisites:

* A [Claude.ai](https://claude.ai) (recommended) or [Claude Console](https://console.anthropic.com/) account

**Install Claude Code:**

<Tabs>
  <Tab title="macOS/Linux">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```
  </Tab>

  <Tab title="Windows">
    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="NPM">
    ```bash  theme={null}
    npm install -g @anthropic-ai/claude-code
    ```

    Requires [Node.js 18+](https://nodejs.org/en/download/)
  </Tab>
</Tabs>

**Start using Claude Code:**

```bash  theme={null}
cd your-project
claude
```

You'll be prompted to log in on first use. That's it! [Continue with Quickstart (5 mins) →](/en/quickstart)

<Tip>
  See [advanced setup](/en/setup) for installation options or [troubleshooting](/en/troubleshooting) if you hit issues.
</Tip>

<Note>
  **New VS Code Extension (Beta)**: Prefer a graphical interface? Our new [VS Code extension](/en/vs-code) provides an easy-to-use native IDE experience without requiring terminal familiarity. Simply install from the marketplace and start coding with Claude directly in your sidebar.
</Note>

## What Claude Code does for you

* **Build features from descriptions**: Tell Claude what you want to build in plain English. It will make a plan, write the code, and ensure it works.
* **Debug and fix issues**: Describe a bug or paste an error message. Claude Code will analyze your codebase, identify the problem, and implement a fix.
* **Navigate any codebase**: Ask anything about your team's codebase, and get a thoughtful answer back. Claude Code maintains awareness of your entire project structure, can find up-to-date information from the web, and with [MCP](/en/mcp) can pull from external datasources like Google Drive, Figma, and Slack.
* **Automate tedious tasks**: Fix fiddly lint issues, resolve merge conflicts, and write release notes. Do all this in a single command from your developer machines, or automatically in CI.

## Why developers love Claude Code

* **Works in your terminal**: Not another chat window. Not another IDE. Claude Code meets you where you already work, with the tools you already love.
* **Takes action**: Claude Code can directly edit files, run commands, and create commits. Need more? [MCP](/en/mcp) lets Claude read your design docs in Google Drive, update your tickets in Jira, or use *your* custom developer tooling.
* **Unix philosophy**: Claude Code is composable and scriptable. `tail -f app.log | claude -p "Slack me if you see any anomalies appear in this log stream"` *works*. Your CI can run `claude -p "If there are new text strings, translate them into French and raise a PR for @lang-fr-team to review"`.
* **Enterprise-ready**: Use the Claude API, or host on AWS or GCP. Enterprise-grade [security](/en/security), [privacy](/en/data-usage), and [compliance](https://trust.anthropic.com/) is built-in.

## Next steps

<CardGroup>
  <Card title="Quickstart" icon="rocket" href="/en/quickstart">
    See Claude Code in action with practical examples
  </Card>

  <Card title="Common workflows" icon="graduation-cap" href="/en/common-workflows">
    Step-by-step guides for common workflows
  </Card>

  <Card title="Troubleshooting" icon="wrench" href="/en/troubleshooting">
    Solutions for common issues with Claude Code
  </Card>

  <Card title="IDE setup" icon="laptop" href="/en/vs-code">
    Add Claude Code to your IDE
  </Card>
</CardGroup>

## Additional resources

<CardGroup>
  <Card title="Build with the Agent SDK" icon="code-branch" href="https://docs.claude.com/enhttps://docs.claude.com/en/api/agent-sdk/overview">
    Create custom AI agents with the Claude Agent SDK
  </Card>

  <Card title="Host on AWS or GCP" icon="cloud" href="/en/third-party-integrations">
    Configure Claude Code with Amazon Bedrock or Google Vertex AI
  </Card>

  <Card title="Settings" icon="gear" href="/en/settings">
    Customize Claude Code for your workflow
  </Card>

  <Card title="Commands" icon="terminal" href="/en/cli-reference">
    Learn about CLI commands and controls
  </Card>

  <Card title="Reference implementation" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
    Clone our development container reference implementation
  </Card>

  <Card title="Security" icon="shield" href="/en/security">
    Discover Claude Code's safeguards and best practices for safe usage
  </Card>

  <Card title="Privacy and data usage" icon="lock" href="/en/data-usage">
    Understand how Claude Code handles your data
  </Card>
</CardGroup>
