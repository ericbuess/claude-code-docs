# Claude Code overview

> Learn about Claude Code, the agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster through natural language commands.

By integrating directly with your development environment, Claude Code streamlines your workflow without requiring additional servers or complex setup.

## Basic usage

To install Claude Code, use NPM:

```bash
npm install -g @anthropic-ai/claude-code
```

For more detailed installation instructions, see [Set up Claude Code](/en/docs/claude-code/setup).

To run Claude Code, simply call the `claude` CLI:

```bash
claude
```

You can then prompt Claude directly from the interactive Claude Code REPL session.

For more usage instructions, see [Quickstart](/en/docs/claude-code/quickstart).

## Why Claude Code?

### Accelerate development

Use Claude Code to accelerate development with the following key capabilities:

* Editing files and fixing bugs across your codebase
* Answering questions about your code's architecture and logic
* Executing and fixing tests, linting, and other commands
* Searching through git history, resolving merge conflicts, and creating commits and PRs
* Browsing documentation and resources from the internet using web search

Claude Code provides a comprehensive set of [tools](/en/docs/claude-code/settings#tools-available-to-claude) for interacting with your development environment, including file operations, code search, web browsing, and more. Understanding these tools helps you leverage Claude Code's full capabilities.

### Security and privacy by design

Your code's security is paramount. Claude Code's architecture ensures:

* **Direct API connection**: Your queries go straight to Anthropic's API without intermediate servers
* **Works where you work**: Operates directly in your terminal
* **Understands context**: Maintains awareness of your entire project structure
* **Takes action**: Performs real operations like editing files and creating commits

### Enterprise integration

Claude Code seamlessly integrates with enterprise AI platforms. You can connect to [Amazon Bedrock or Google Vertex AI](/en/docs/claude-code/third-party-integrations) for secure, compliant deployments that meet your organization's requirements.

## Next steps

<CardGroup>
  <Card title="Setup" icon="download" href="/en/docs/claude-code/setup">
    Install and authenticate Claude Code
  </Card>

  <Card title="Quickstart" icon="rocket" href="/en/docs/claude-code/quickstart">
    See Claude Code in action with practical examples
  </Card>

  <Card title="Commands" icon="terminal" href="/en/docs/claude-code/cli-reference">
    Learn about CLI commands and controls
  </Card>

  <Card title="Configuration" icon="gear" href="/en/docs/claude-code/settings">
    Customize Claude Code for your workflow
  </Card>
</CardGroup>

## Additional resources

<CardGroup>
  <Card title="Common workflows" icon="graduation-cap" href="/en/docs/claude-code/common-workflows">
    Step-by-step guides for common workflows
  </Card>

  <Card title="Troubleshooting" icon="wrench" href="/en/docs/claude-code/troubleshooting">
    Solutions for common issues with Claude Code
  </Card>

  <Card title="Bedrock & Vertex integrations" icon="cloud" href="/en/docs/claude-code/bedrock-vertex-proxies">
    Configure Claude Code with Amazon Bedrock or Google Vertex AI
  </Card>

  <Card title="Reference implementation" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
    Clone our development container reference implementation.
  </Card>
</CardGroup>
