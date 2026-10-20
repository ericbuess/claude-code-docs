> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 30 · July 20–24, 2026

> Opus 5 becomes the default Opus model, Claude Code Desktop adds an iOS Simulator pane, and the Claude Security plugin scans your code for vulnerabilities.

Releases [v2.1.214 → v2.1.219](/docs/en/changelog#2-1-214)
3 features · July 20–24

Claude Opus 5
new model

Claude Opus 5 is the new default Opus model in Claude Code. It's the default on Max, Team Premium, Enterprise pay-as-you-go, and the Anthropic API, and on Claude Platform on AWS, Amazon Bedrock, and Google Cloud's Agent Platform. On the Anthropic API and on Max, Team, and Enterprise plans, Opus 5 runs with a [1M-token context window](/docs/en/model-config#extended-context); on Amazon Bedrock and Google Cloud's Agent Platform, select the 1M model variant. Fast mode moves to Opus 5 at \$10/\$50 per MTok. Requires v2.1.219 or later.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/N3yEaTYPXMXFrF6k/images/whats-new/opus-5.mp4?fit=max&auto=format&n=N3yEaTYPXMXFrF6k&q=85&s=8536b1cb3180e539008f39930403e47b" />

Switch to Opus 5 by name, or pick it from the model picker:

```text Claude Code theme={null}
> /model claude-opus-5
```

[Model configuration](/docs/en/model-config#available-models)

iOS Simulator in Claude Code Desktop
Desktop

Claude Code Desktop on macOS gets an iOS Simulator pane, in public beta on Pro, Max, and Team plans. When Claude builds, launches, or checks your app in a simulator, the pane opens next to the conversation and streams the device screen live, so you can watch Claude tap through the app to verify its changes or drive the device yourself. Requires Xcode with the iOS platform installed, and Claude Desktop v1.24012.0 or later.

![Claude Code Desktop with the iOS Simulator pane showing an iPhone app next to the conversation](https://mintcdn.com/claude-code/N3yEaTYPXMXFrF6k/images/whats-new/ios-simulator.jpg?fit=max\&auto=format\&n=N3yEaTYPXMXFrF6k\&q=85\&s=6c88418ed14ed0fb12cc1af75b17f2ee)

Ask Claude to run or test your app, and the pane opens when the app launches:

```text Claude Code theme={null}
> Build the app and run it in the simulator to check the onboarding flow.
```

[Test iOS apps in the simulator](/docs/en/desktop-ios-simulator#run-your-app-in-the-simulator)

Claude Security plugin
plugin

The Claude Security plugin runs a multi-agent vulnerability scan of your codebase inside a Claude Code session: agents map your architecture, build a threat model, hunt for vulnerabilities, and independently review every finding before writing the report to a `CLAUDE-SECURITY-<timestamp>/` directory. Scan a whole repository or only a branch's diff, a pull request, or a single commit, then turn the findings you choose into reviewed patches that you apply yourself.

Install the plugin from the official Anthropic marketplace, run `/reload-plugins`, then start a scan with `/claude-security`:

```text Claude Code theme={null}
> /plugin install claude-security@claude-plugins-official
```

[Scan and fix your codebase](/docs/en/claude-security#scan-and-fix-your-codebase)

Other wins

[`/code-review`](/docs/en/code-review-local) now runs as a background subagent with its own context window, so review work stays out of your conversation and the findings arrive when it completes`/verify`, `/code-review`, and `/deep-research` run only when you invoke them; Claude no longer launches them on its own[Emoji shortcodes](/docs/en/interactive-mode#emoji-shortcodes) autocomplete in the prompt input: type `:heart:` to insert an emoji, or two or more characters after `:` for suggestions; turn it off with `emojiCompletionEnabled`Skills with `context: fork` [run in the background](/docs/en/skills#run-skills-in-a-subagent) by default, and `background: false` in the skill's frontmatter waits for the result in the same turnA session runs up to 20 subagents concurrently by default; change the [limit](/docs/en/sub-agents#concurrent-subagent-limit) with `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS``--max-budget-usd` now enforces the cap on subagents: once spend reaches it, Claude can't start more and running background subagents stopNew [`sandbox.filesystem.disabled`](/docs/en/sandboxing#disable-filesystem-isolation) setting skips filesystem isolation while keeping network egress controlIn auto mode, the checks for dangerous `rm` commands, background jobs, and suspicious Windows paths no longer open permission dialogs; the auto-mode classifier adjudicates them insteadBash permission checks fail closed on more shell forms, including file-descriptor redirects, Zsh variable subscripts in `[[ ]]` comparisons, `help` and `man` invocations that could run unsafe options, and commands over 10,000 characters[Fast mode](/docs/en/fast-mode) no longer supports Opus 4.7: `/fast` now applies to Opus 5 and Opus 4.8Long-running tool calls emit a periodic progress heartbeat instead of going silent

[Full changelog for v2.1.214–v2.1.219 →](/docs/en/changelog#2-1-214)
