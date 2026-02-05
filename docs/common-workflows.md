> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Common workflows

> Step-by-step guides for exploring codebases, fixing bugs, refactoring, testing, and other everyday tasks with Claude Code.

This page covers practical workflows for everyday development: exploring unfamiliar code, debugging, refactoring, writing tests, creating PRs, and managing sessions. Each section includes example prompts you can adapt to your own projects. For higher-level patterns and tips, see [Best practices](/en/best-practices).

## Understand new codebases

### Get a quick codebase overview

Suppose you've just joined a new project and need to understand its structure quickly.

<Steps>
  <Step title="Navigate to the project root directory">
    ```bash  theme={null}
    cd /path/to/project 
    ```
  </Step>

  <Step title="Start Claude Code">
    ```bash  theme={null}
    claude 
    ```
  </Step>

  <Step title="Ask for a high-level overview">
    ```
    > give me an overview of this codebase 
    ```
  </Step>

  <Step title="Dive deeper into specific components">
    ```
    > explain the main architecture patterns used here 
    ```

    ```
    > what are the key data models?
    ```

    ```
    > how is authentication handled?
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Start with broad questions, then narrow down to specific areas
  * Ask about coding conventions and patterns used in the project
  * Request a glossary of project-specific terms
</Tip>

### Find relevant code

Suppose you need to locate code related to a specific feature or functionality.

<Steps>
  <Step title="Ask Claude to find relevant files">
    ```
    > find the files that handle user authentication 
    ```
  </Step>

  <Step title="Get context on how components interact">
    ```
    > how do these authentication files work together? 
    ```
  </Step>

  <Step title="Understand the execution flow">
    ```
    > trace the login process from front-end to database 
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Be specific about what you're looking for
  * Use domain language from the project
  * Install a [code intelligence plugin](/en/discover-plugins#code-intelligence) for your language to give Claude precise "go to definition" and "find references" navigation
</Tip>

***

## Fix bugs efficiently

Suppose you've encountered an error message and need to find and fix its source.

<Steps>
  <Step title="Share the error with Claude">
    ```
    > I'm seeing an error when I run npm test 
    ```
  </Step>

  <Step title="Ask for fix recommendations">
    ```
    > suggest a few ways to fix the @ts-ignore in user.ts 
    ```
  </Step>

  <Step title="Apply the fix">
    ```
    > update user.ts to add the null check you suggested 
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Tell Claude the command to reproduce the issue and get a stack trace
  * Mention any steps to reproduce the error
  * Let Claude know if the error is intermittent or consistent
</Tip>

***

## Refactor code

Suppose you need to update old code to use modern patterns and practices.

<Steps>
  <Step title="Identify legacy code for refactoring">
    ```
    > find deprecated API usage in our codebase 
    ```
  </Step>

  <Step title="Get refactoring recommendations">
    ```
    > suggest how to refactor utils.js to use modern JavaScript features 
    ```
  </Step>

  <Step title="Apply the changes safely">
    ```
    > refactor utils.js to use ES2024 features while maintaining the same behavior 
    ```
  </Step>

  <Step title="Verify the refactoring">
    ```
    > run tests for the refactored code 
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Ask Claude to explain the benefits of the modern approach
  * Request that changes maintain backward compatibility when needed
  * Do refactoring in small, testable increments
</Tip>

***

## Use specialized subagents

Suppose you want to use specialized AI subagents to handle specific tasks more effectively.

<Steps>
  <Step title="View available subagents">
    ```
    > /agents
    ```

    This shows all available subagents and lets you create new ones.
  </Step>

  <Step title="Use subagents automatically">
    Claude Code automatically delegates appropriate tasks to specialized subagents:

    ```
    > review my recent code changes for security issues
    ```

    ```
    > run all tests and fix any failures
    ```
  </Step>

  <Step title="Explicitly request specific subagents">
    ```
    > use the code-reviewer subagent to check the auth module
    ```

    ```
    > have the debugger subagent investigate why users can't log in
    ```
  </Step>

  <Step title="Create custom subagents for your workflow">
    ```
    > /agents
    ```

    Then select "Create New subagent" and follow the prompts to define:

    * A unique identifier that describes the subagent's purpose (for example, `code-reviewer`, `api-designer`).
    * When Claude should use this agent
    * Which tools it can access
    * A system prompt describing the agent's role and behavior
  </Step>
</Steps>

<Tip>
  Tips:

  * Create project-specific subagents in `.claude/agents/` for team sharing
  * Use descriptive `description` fields to enable automatic delegation
  * Limit tool access to what each subagent actually needs
  * Check the [subagents documentation](/en/sub-agents) for detailed examples
</Tip>

***

## Use Plan Mode for safe code analysis

Plan Mode instructs Claude to create a plan by analyzing the codebase with read-only operations, perfect for exploring codebases, planning complex changes, or reviewing code safely. In Plan Mode, Claude uses [`AskUserQuestion`](/en/settings#tools-available-to-claude) to gather requirements and clarify your goals before proposing a plan.

### When to use Plan Mode

* **Multi-step implementation**: When your feature requires making edits to many files
* **Code exploration**: When you want to research the codebase thoroughly before changing anything
* **Interactive development**: When you want to iterate on the direction with Claude

### How to use Plan Mode

**Turn on Plan Mode during a session**

You can switch into Plan Mode during a session using **Shift+Tab** to cycle through permission modes.

If you are in Normal Mode, **Shift+Tab** first switches into Auto-Accept Mode, indicated by `⏵⏵ accept edits on` at the bottom of the terminal. A subsequent **Shift+Tab** will switch into Plan Mode, indicated by `⏸ plan mode on`. When an [agent team](/en/agent-teams) is active, the cycle also includes Delegate Mode.

**Start a new session in Plan Mode**

To start a new session in Plan Mode, use the `--permission-mode plan` flag:

```bash  theme={null}
claude --permission-mode plan
```

**Run "headless" queries in Plan Mode**

You can also run a query in Plan Mode directly with `-p` (that is, in ["headless mode"](/en/headless)):

```bash  theme={null}
claude --permission-mode plan -p "Analyze the authentication system and suggest improvements"
```

### Example: Planning a complex refactor

```bash  theme={null}
claude --permission-mode plan
```

```
> I need to refactor our authentication system to use OAuth2. Create a detailed migration plan.
```

Claude analyzes the current implementation and create a comprehensive plan. Refine with follow-ups:

```
> What about backward compatibility?
> How should we handle database migration?
```

<Tip>Press `Ctrl+G` to open the plan in your default text editor, where you can edit it directly before Claude proceeds.</Tip>

### Configure Plan Mode as default

```json  theme={null}
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

See [settings documentation](/en/settings#available-settings) for more configuration options.

***

## Work with tests

Suppose you need to add tests for uncovered code.

<Steps>
  <Step title="Identify untested code">
    ```
    > find functions in NotificationsService.swift that are not covered by tests 
    ```
  </Step>

  <Step title="Generate test scaffolding">
    ```
    > add tests for the notification service 
    ```
  </Step>

  <Step title="Add meaningful test cases">
    ```
    > add test cases for edge conditions in the notification service 
    ```
  </Step>

  <Step title="Run and verify tests">
    ```
    > run the new tests and fix any failures 
    ```
  </Step>
</Steps>

Claude can generate tests that follow your project's existing patterns and conventions. When asking for tests, be specific about what behavior you want to verify. Claude examines your existing test files to match the style, frameworks, and assertion patterns already in use.

For comprehensive coverage, ask Claude to identify edge cases you might have missed. Claude can analyze your code paths and suggest tests for error conditions, boundary values, and unexpected inputs that are easy to overlook.

***

## Create pull requests

You can create pull requests by asking Claude directly ("create a pr for my changes") or by using the `/commit-push-pr` skill, which commits, pushes, and opens a PR in one step.

```
> /commit-push-pr
```

If you have a Slack MCP server configured and specify channels in your CLAUDE.md (for example, "post PR URLs to #team-prs"), the skill automatically posts the PR URL to those channels.

For more control over the process, guide Claude through it step-by-step or [create your own skill](/en/skills):

<Steps>
  <Step title="Summarize your changes">
    ```
    > summarize the changes I've made to the authentication module
    ```
  </Step>

  <Step title="Generate a pull request">
    ```
    > create a pr
    ```
  </Step>

  <Step title="Review and refine">
    ```
    > enhance the PR description with more context about the security improvements
    ```
  </Step>
</Steps>

When you create a PR using `gh pr create`, the session is automatically linked to that PR. You can resume it later with `claude --from-pr <number>`.

<Tip>
  Review Claude's generated PR before submitting and ask Claude to highlight potential risks or considerations.
</Tip>

## Handle documentation

Suppose you need to add or update documentation for your code.

<Steps>
  <Step title="Identify undocumented code">
    ```
    > find functions without proper JSDoc comments in the auth module 
    ```
  </Step>

  <Step title="Generate documentation">
    ```
    > add JSDoc comments to the undocumented functions in auth.js 
    ```
  </Step>

  <Step title="Review and enhance">
    ```
    > improve the generated documentation with more context and examples 
    ```
  </Step>

  <Step title="Verify documentation">
    ```
    > check if the documentation follows our project standards 
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Specify the documentation style you want (JSDoc, docstrings, etc.)
  * Ask for examples in the documentation
  * Request documentation for public APIs, interfaces, and complex logic
</Tip>

***

## Work with images

Suppose you need to work with images in your codebase, and you want Claude's help analyzing image content.

<Steps>
  <Step title="Add an image to the conversation">
    You can use any of these methods:

    1. Drag and drop an image into the Claude Code window
    2. Copy an image and paste it into the CLI with ctrl+v (Do not use cmd+v)
    3. Provide an image path to Claude. E.g., "Analyze this image: /path/to/your/image.png"
  </Step>

  <Step title="Ask Claude to analyze the image">
    ```
    > What does this image show?
    ```

    ```
    > Describe the UI elements in this screenshot
    ```

    ```
    > Are there any problematic elements in this diagram?
    ```
  </Step>

  <Step title="Use images for context">
    ```
    > Here's a screenshot of the error. What's causing it?
    ```

    ```
    > This is our current database schema. How should we modify it for the new feature?
    ```
  </Step>

  <Step title="Get code suggestions from visual content">
    ```
    > Generate CSS to match this design mockup
    ```

    ```
    > What HTML structure would recreate this component?
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Use images when text descriptions would be unclear or cumbersome
  * Include screenshots of errors, UI designs, or diagrams for better context
  * You can work with multiple images in a conversation
  * Image analysis works with diagrams, screenshots, mockups, and more
  * When Claude references images (for example, `[Image #1]`), `Cmd+Click` (Mac) or `Ctrl+Click` (Windows/Linux) the link to open the image in your default viewer
</Tip>

***

## Reference files and directories

Use @ to quickly include files or directories without waiting for Claude to read them.

<Steps>
  <Step title="Reference a single file">
    ```
    > Explain the logic in @src/utils/auth.js
    ```

    This includes the full content of the file in the conversation.
  </Step>

  <Step title="Reference a directory">
    ```
    > What's the structure of @src/components?
    ```

    This provides a directory listing with file information.
  </Step>

  <Step title="Reference MCP resources">
    ```
    > Show me the data from @github:repos/owner/repo/issues
    ```

    This fetches data from connected MCP servers using the format @server:resource. See [MCP resources](/en/mcp#use-mcp-resources) for details.
  </Step>
</Steps>

<Tip>
  Tips:

  * File paths can be relative or absolute
  * @ file references add `CLAUDE.md` in the file's directory and parent directories to context
  * Directory references show file listings, not contents
  * You can reference multiple files in a single message (for example, "@file1.js and @file2.js")
</Tip>

***

## Use extended thinking (thinking mode)

[Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) is enabled by default, giving Claude space to reason through complex problems step-by-step before responding. This reasoning is visible in verbose mode, which you can toggle on with `Ctrl+O`.

Additionally, Opus 4.6 introduces adaptive reasoning: instead of a fixed thinking token budget, the model dynamically allocates thinking based on your [effort level](/en/model-config#adjust-effort-level) setting. Extended thinking and adaptive reasoning work together to give you control over how deeply Claude reasons before responding.

Extended thinking is particularly valuable for complex architectural decisions, challenging bugs, multi-step implementation planning, and evaluating tradeoffs between different approaches.

<Note>
  Phrases like "think", "think hard", "ultrathink", and "think more" are interpreted as regular prompt instructions and don't allocate thinking tokens.
</Note>

### Configure thinking mode

Thinking is enabled by default, but you can adjust or disable it.

| Scope                  | How to configure                                                                           | Details                                                                                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Effort level**       | Adjust in `/model` or set [`CLAUDE_CODE_EFFORT_LEVEL`](/en/settings#environment-variables) | Control thinking depth for Opus 4.6: low, medium, high (default). See [Adjust effort level](/en/model-config#adjust-effort-level)                     |
| **Toggle shortcut**    | Press `Option+T` (macOS) or `Alt+T` (Windows/Linux)                                        | Toggle thinking on/off for the current session (all models). May require [terminal configuration](/en/terminal-config) to enable Option key shortcuts |
| **Global default**     | Use `/config` to toggle thinking mode                                                      | Sets your default across all projects (all models).<br />Saved as `alwaysThinkingEnabled` in `~/.claude/settings.json`                                |
| **Limit token budget** | Set [`MAX_THINKING_TOKENS`](/en/settings#environment-variables) environment variable       | Limit the thinking budget to a specific number of tokens (ignored on Opus 4.6 unless set to 0). Example: `export MAX_THINKING_TOKENS=10000`           |

To view Claude's thinking process, press `Ctrl+O` to toggle verbose mode and see the internal reasoning displayed as gray italic text.

### How extended thinking works

Extended thinking controls how much internal reasoning Claude performs before responding. More thinking provides more space to explore solutions, analyze edge cases, and self-correct mistakes.

**With Opus 4.6**, thinking uses adaptive reasoning: the model dynamically allocates thinking tokens based on the [effort level](/en/model-config#adjust-effort-level) you select (low, medium, high). This is the recommended way to tune the tradeoff between speed and reasoning depth.

**With other models**, thinking uses a fixed budget of up to 31,999 tokens from your output budget. You can limit this with the [`MAX_THINKING_TOKENS`](/en/settings#environment-variables) environment variable, or disable thinking entirely via `/config` or the `Option+T`/`Alt+T` toggle.

`MAX_THINKING_TOKENS` is ignored when using Opus 4.6, since adaptive reasoning controls thinking depth instead. The one exception: setting `MAX_THINKING_TOKENS=0` still disables thinking entirely on any model.

<Warning>
  You're charged for all thinking tokens used, even though Claude 4 models show summarized thinking
</Warning>

***

## Resume previous conversations

When starting Claude Code, you can resume a previous session:

* `claude --continue` continues the most recent conversation in the current directory
* `claude --resume` opens a conversation picker or resumes by name
* `claude --from-pr 123` resumes sessions linked to a specific pull request

From inside an active session, use `/resume` to switch to a different conversation.

Sessions are stored per project directory. The `/resume` picker shows sessions from the same git repository, including worktrees.

### Name your sessions

Give sessions descriptive names to find them later. This is a best practice when working on multiple tasks or features.

<Steps>
  <Step title="Name the current session">
    Use `/rename` during a session to give it a memorable name:

    ```
    > /rename auth-refactor
    ```

    You can also rename any session from the picker: run `/resume`, navigate to a session, and press `R`.
  </Step>

  <Step title="Resume by name later">
    From the command line:

    ```bash  theme={null}
    claude --resume auth-refactor
    ```

    Or from inside an active session:

    ```
    > /resume auth-refactor
    ```
  </Step>
</Steps>

### Use the session picker

The `/resume` command (or `claude --resume` without arguments) opens an interactive session picker with these features:

**Keyboard shortcuts in the picker:**

| Shortcut  | Action                                            |
| :-------- | :------------------------------------------------ |
| `↑` / `↓` | Navigate between sessions                         |
| `→` / `←` | Expand or collapse grouped sessions               |
| `Enter`   | Select and resume the highlighted session         |
| `P`       | Preview the session content                       |
| `R`       | Rename the highlighted session                    |
| `/`       | Search to filter sessions                         |
| `A`       | Toggle between current directory and all projects |
| `B`       | Filter to sessions from your current git branch   |
| `Esc`     | Exit the picker or search mode                    |

**Session organization:**

The picker displays sessions with helpful metadata:

* Session name or initial prompt
* Time elapsed since last activity
* Message count
* Git branch (if applicable)

Forked sessions (created with `/rewind` or `--fork-session`) are grouped together under their root session, making it easier to find related conversations.

<Tip>
  Tips:

  * **Name sessions early**: Use `/rename` when starting work on a distinct task—it's much easier to find "payment-integration" than "explain this function" later
  * Use `--continue` for quick access to your most recent conversation in the current directory
  * Use `--resume session-name` when you know which session you need
  * Use `--resume` (without a name) when you need to browse and select
  * For scripts, use `claude --continue --print "prompt"` to resume in non-interactive mode
  * Press `P` in the picker to preview a session before resuming it
  * The resumed conversation starts with the same model and configuration as the original

  How it works:

  1. **Conversation Storage**: All conversations are automatically saved locally with their full message history
  2. **Message Deserialization**: When resuming, the entire message history is restored to maintain context
  3. **Tool State**: Tool usage and results from the previous conversation are preserved
  4. **Context Restoration**: The conversation resumes with all previous context intact
</Tip>

***

## Run parallel Claude Code sessions with Git worktrees

Suppose you need to work on multiple tasks simultaneously with complete code isolation between Claude Code instances.

<Steps>
  <Step title="Understand Git worktrees">
    Git worktrees allow you to check out multiple branches from the same
    repository into separate directories. Each worktree has its own working
    directory with isolated files, while sharing the same Git history. Learn
    more in the [official Git worktree
    documentation](https://git-scm.com/docs/git-worktree).
  </Step>

  <Step title="Create a new worktree">
    ```bash  theme={null}
    # Create a new worktree with a new branch 
    git worktree add ../project-feature-a -b feature-a

    # Or create a worktree with an existing branch
    git worktree add ../project-bugfix bugfix-123
    ```

    This creates a new directory with a separate working copy of your repository.
  </Step>

  <Step title="Run Claude Code in each worktree">
    ```bash  theme={null}
    # Navigate to your worktree 
    cd ../project-feature-a

    # Run Claude Code in this isolated environment
    claude
    ```
  </Step>

  <Step title="Run Claude in another worktree">
    ```bash  theme={null}
    cd ../project-bugfix
    claude
    ```
  </Step>

  <Step title="Manage your worktrees">
    ```bash  theme={null}
    # List all worktrees
    git worktree list

    # Remove a worktree when done
    git worktree remove ../project-feature-a
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Each worktree has its own independent file state, making it perfect for parallel Claude Code sessions
  * Changes made in one worktree won't affect others, preventing Claude instances from interfering with each other
  * All worktrees share the same Git history and remote connections
  * For long-running tasks, you can have Claude working in one worktree while you continue development in another
  * Use descriptive directory names to easily identify which task each worktree is for
  * Remember to initialize your development environment in each new worktree according to your project's setup. Depending on your stack, this might include:
    * JavaScript projects: Running dependency installation (`npm install`, `yarn`)
    * Python projects: Setting up virtual environments or installing with package managers
    * Other languages: Following your project's standard setup process
</Tip>

For automated coordination of parallel sessions with shared tasks and messaging, see [agent teams](/en/agent-teams).

***

## Use Claude as a unix-style utility

### Add Claude to your verification process

Suppose you want to use Claude Code as a linter or code reviewer.

**Add Claude to your build script:**

```json  theme={null}
// package.json
{
    ...
    "scripts": {
        ...
        "lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos. report the filename and line number on one line, and a description of the issue on the second line. do not return any other text.'"
    }
}
```

<Tip>
  Tips:

  * Use Claude for automated code review in your CI/CD pipeline
  * Customize the prompt to check for specific issues relevant to your project
  * Consider creating multiple scripts for different types of verification
</Tip>

### Pipe in, pipe out

Suppose you want to pipe data into Claude, and get back data in a structured format.

**Pipe data through Claude:**

```bash  theme={null}
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

<Tip>
  Tips:

  * Use pipes to integrate Claude into existing shell scripts
  * Combine with other Unix tools for powerful workflows
  * Consider using --output-format for structured output
</Tip>

### Control output format

Suppose you need Claude's output in a specific format, especially when integrating Claude Code into scripts or other tools.

<Steps>
  <Step title="Use text format (default)">
    ```bash  theme={null}
    cat data.txt | claude -p 'summarize this data' --output-format text > summary.txt
    ```

    This outputs just Claude's plain text response (default behavior).
  </Step>

  <Step title="Use JSON format">
    ```bash  theme={null}
    cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json
    ```

    This outputs a JSON array of messages with metadata including cost and duration.
  </Step>

  <Step title="Use streaming JSON format">
    ```bash  theme={null}
    cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json
    ```

    This outputs a series of JSON objects in real-time as Claude processes the request. Each message is a valid JSON object, but the entire output is not valid JSON if concatenated.
  </Step>
</Steps>

<Tip>
  Tips:

  * Use `--output-format text` for simple integrations where you just need Claude's response
  * Use `--output-format json` when you need the full conversation log
  * Use `--output-format stream-json` for real-time output of each conversation turn
</Tip>

***

## Ask Claude about its capabilities

Claude has built-in access to its documentation and can answer questions about its own features and limitations.

### Example questions

```
> can Claude Code create pull requests?
```

```
> how does Claude Code handle permissions?
```

```
> what skills are available?
```

```
> how do I use MCP with Claude Code?
```

```
> how do I configure Claude Code for Amazon Bedrock?
```

```
> what are the limitations of Claude Code?
```

<Note>
  Claude provides documentation-based answers to these questions. For executable examples and hands-on demonstrations, refer to the specific workflow sections above.
</Note>

<Tip>
  Tips:

  * Claude always has access to the latest Claude Code documentation, regardless of the version you're using
  * Ask specific questions to get detailed answers
  * Claude can explain complex features like MCP integration, enterprise configurations, and advanced workflows
</Tip>

***

## Next steps

<CardGroup cols={2}>
  <Card title="Best practices" icon="lightbulb" href="/en/best-practices">
    Patterns for getting the most out of Claude Code
  </Card>

  <Card title="How Claude Code works" icon="gear" href="/en/how-claude-code-works">
    Understand the agentic loop and context management
  </Card>

  <Card title="Extend Claude Code" icon="puzzle-piece" href="/en/features-overview">
    Add skills, hooks, MCP, subagents, and plugins
  </Card>

  <Card title="Reference implementation" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
    Clone our development container reference implementation
  </Card>
</CardGroup>
