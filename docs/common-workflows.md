> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Common workflows

> Step-by-step guides for exploring codebases, fixing bugs, refactoring, testing, and other everyday tasks with Claude Code.

This page collects short recipes for everyday development. For higher-level guidance on prompting and context management, see [Best practices](/en/best-practices).

This page covers:

* [Prompt recipes](#prompt-recipes) for exploring code, fixing bugs, refactoring, testing, PRs, and documentation
* [Resume previous conversations](#resume-previous-conversations) so a task can span multiple sittings
* [Run parallel sessions with worktrees](#run-parallel-sessions-with-worktrees) so concurrent edits don't collide
* [Plan before editing](#plan-before-editing) to review changes before they touch disk
* [Delegate research to subagents](#delegate-research-to-subagents) to keep your main context clean
* [Pipe Claude into scripts](#pipe-claude-into-scripts) for CI and batch processing

## Prompt recipes

These are prompt patterns for everyday tasks like exploring unfamiliar code, debugging, refactoring, writing tests, and creating PRs. Each works in any Claude Code surface; adapt the wording to your project.

### Understand new codebases

#### Get a quick codebase overview

Suppose you've just joined a new project and need to understand its structure quickly.

<Steps>
  <Step title="Navigate to the project root directory">
    ```bash theme={null}
    cd /path/to/project 
    ```
  </Step>

  <Step title="Start Claude Code">
    ```bash theme={null}
    claude 
    ```
  </Step>

  <Step title="Ask for a high-level overview">
    ```text theme={null}
    give me an overview of this codebase
    ```
  </Step>

  <Step title="Dive deeper into specific components">
    ```text theme={null}
    explain the main architecture patterns used here
    ```

    ```text theme={null}
    what are the key data models?
    ```

    ```text theme={null}
    how is authentication handled?
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Start with broad questions, then narrow down to specific areas
  * Ask about coding conventions and patterns used in the project
  * Request a glossary of project-specific terms
</Tip>

#### Find relevant code

Suppose you need to locate code related to a specific feature or functionality.

<Steps>
  <Step title="Ask Claude to find relevant files">
    ```text theme={null}
    find the files that handle user authentication
    ```
  </Step>

  <Step title="Get context on how components interact">
    ```text theme={null}
    how do these authentication files work together?
    ```
  </Step>

  <Step title="Understand the execution flow">
    ```text theme={null}
    trace the login process from front-end to database
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

### Fix bugs efficiently

Suppose you've encountered an error message and need to find and fix its source.

<Steps>
  <Step title="Share the error with Claude">
    ```text theme={null}
    I'm seeing an error when I run npm test
    ```
  </Step>

  <Step title="Ask for fix recommendations">
    ```text theme={null}
    suggest a few ways to fix the @ts-ignore in user.ts
    ```
  </Step>

  <Step title="Apply the fix">
    ```text theme={null}
    update user.ts to add the null check you suggested
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

### Refactor code

Suppose you need to update old code to use modern patterns and practices.

<Steps>
  <Step title="Identify legacy code for refactoring">
    ```text theme={null}
    find deprecated API usage in our codebase
    ```
  </Step>

  <Step title="Get refactoring recommendations">
    ```text theme={null}
    suggest how to refactor utils.js to use modern JavaScript features
    ```
  </Step>

  <Step title="Apply the changes safely">
    ```text theme={null}
    refactor utils.js to use ES2024 features while maintaining the same behavior
    ```
  </Step>

  <Step title="Verify the refactoring">
    ```text theme={null}
    run tests for the refactored code
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

### Work with tests

Suppose you need to add tests for uncovered code.

<Steps>
  <Step title="Identify untested code">
    ```text theme={null}
    find functions in NotificationsService.swift that are not covered by tests
    ```
  </Step>

  <Step title="Generate test scaffolding">
    ```text theme={null}
    add tests for the notification service
    ```
  </Step>

  <Step title="Add meaningful test cases">
    ```text theme={null}
    add test cases for edge conditions in the notification service
    ```
  </Step>

  <Step title="Run and verify tests">
    ```text theme={null}
    run the new tests and fix any failures
    ```
  </Step>
</Steps>

Claude can generate tests that follow your project's existing patterns and conventions. When asking for tests, be specific about what behavior you want to verify. Claude examines your existing test files to match the style, frameworks, and assertion patterns already in use.

For comprehensive coverage, ask Claude to identify edge cases you might have missed. Claude can analyze your code paths and suggest tests for error conditions, boundary values, and unexpected inputs that are easy to overlook.

***

### Create pull requests

You can create pull requests by asking Claude directly ("create a pr for my changes"), or guide Claude through it step-by-step:

<Steps>
  <Step title="Summarize your changes">
    ```text theme={null}
    summarize the changes I've made to the authentication module
    ```
  </Step>

  <Step title="Generate a pull request">
    ```text theme={null}
    create a pr
    ```
  </Step>

  <Step title="Review and refine">
    ```text theme={null}
    enhance the PR description with more context about the security improvements
    ```
  </Step>
</Steps>

When you create a PR using `gh pr create`, the session is automatically linked to that PR. To return to it later, run `claude --from-pr <number>` or paste the PR URL into the [`/resume` picker](/en/sessions#use-the-session-picker) search.

<Tip>
  Review Claude's generated PR before submitting and ask Claude to highlight potential risks or considerations.
</Tip>

### Handle documentation

Suppose you need to add or update documentation for your code.

<Steps>
  <Step title="Identify undocumented code">
    ```text theme={null}
    find functions without proper JSDoc comments in the auth module
    ```
  </Step>

  <Step title="Generate documentation">
    ```text theme={null}
    add JSDoc comments to the undocumented functions in auth.js
    ```
  </Step>

  <Step title="Review and enhance">
    ```text theme={null}
    improve the generated documentation with more context and examples
    ```
  </Step>

  <Step title="Verify documentation">
    ```text theme={null}
    check if the documentation follows our project standards
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

### Work in notes and non-code folders

Claude Code works in any directory. Run it inside a notes vault, a documentation folder, or any collection of markdown files to search, edit, and reorganize content the same way you would code.

The `.claude/` directory and `CLAUDE.md` sit alongside other tools' config directories without conflict. Claude reads files fresh on each tool call, so it sees edits you make in another application the next time it reads that file.

***

### Work with images

Suppose you need to work with images in your codebase, and you want Claude's help analyzing image content.

<Steps>
  <Step title="Add an image to the conversation">
    You can use any of these methods:

    1. Drag and drop an image into the Claude Code window
    2. Copy an image and paste it into the CLI with ctrl+v (Do not use cmd+v)
    3. Provide an image path to Claude. E.g., "Analyze this image: /path/to/your/image.png"
  </Step>

  <Step title="Ask Claude to analyze the image">
    ```text theme={null}
    What does this image show?
    ```

    ```text theme={null}
    Describe the UI elements in this screenshot
    ```

    ```text theme={null}
    Are there any problematic elements in this diagram?
    ```
  </Step>

  <Step title="Use images for context">
    ```text theme={null}
    Here's a screenshot of the error. What's causing it?
    ```

    ```text theme={null}
    This is our current database schema. How should we modify it for the new feature?
    ```
  </Step>

  <Step title="Get code suggestions from visual content">
    ```text theme={null}
    Generate CSS to match this design mockup
    ```

    ```text theme={null}
    What HTML structure would recreate this component?
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

### Reference files and directories

Use @ to quickly include files or directories without waiting for Claude to read them.

<Steps>
  <Step title="Reference a single file">
    ```text theme={null}
    Explain the logic in @src/utils/auth.js
    ```

    This includes the full content of the file in the conversation.
  </Step>

  <Step title="Reference a directory">
    ```text theme={null}
    What's the structure of @src/components?
    ```

    This provides a directory listing with file information.
  </Step>

  <Step title="Reference MCP resources">
    ```text theme={null}
    Show me the data from @github:repos/owner/repo/issues
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

### Run Claude on a schedule

Suppose you want Claude to handle a task automatically on a recurring basis, like reviewing open PRs every morning, auditing dependencies weekly, or checking for CI failures overnight.

Pick a scheduling option based on where you want the task to run:

| Option                                                 | Where it runs                     | Best for                                                                                                                                                                                                 |
| :----------------------------------------------------- | :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Routines](/en/routines)                               | Anthropic-managed infrastructure  | Tasks that should run even when your computer is off. Can also trigger on API calls or GitHub events in addition to a schedule. Configure at [claude.ai/code/routines](https://claude.ai/code/routines). |
| [Desktop scheduled tasks](/en/desktop-scheduled-tasks) | Your machine, via the desktop app | Tasks that need direct access to local files, tools, or uncommitted changes.                                                                                                                             |
| [GitHub Actions](/en/github-actions)                   | Your CI pipeline                  | Tasks tied to repo events like opened PRs, or cron schedules that should live alongside your workflow config.                                                                                            |
| [`/loop`](/en/scheduled-tasks)                         | The current CLI session           | Quick polling while a session is open. Tasks stop when you start a new conversation; `--resume` and `--continue` restore unexpired ones.                                                                 |

<Tip>
  When writing prompts for scheduled tasks, be explicit about what success looks like and what to do with results. The task runs autonomously, so it can't ask clarifying questions. For example: "Review open PRs labeled `needs-review`, leave inline comments on any issues, and post a summary in the `#eng-reviews` Slack channel."
</Tip>

***

### Ask Claude about its capabilities

Claude has built-in access to its documentation and can answer questions about its own features and limitations.

#### Example questions

```text theme={null}
can Claude Code create pull requests?
```

```text theme={null}
how does Claude Code handle permissions?
```

```text theme={null}
what skills are available?
```

```text theme={null}
how do I use MCP with Claude Code?
```

```text theme={null}
how do I configure Claude Code for Amazon Bedrock?
```

```text theme={null}
what are the limitations of Claude Code?
```

<Note>
  Claude provides documentation-based answers to these questions. For hands-on demonstrations, run `/powerup` for interactive lessons with animated demos, or refer to the specific workflow sections above.
</Note>

<Tip>
  Tips:

  * Claude always has access to the latest Claude Code documentation, regardless of the version you're using
  * Ask specific questions to get detailed answers
  * Claude can explain complex features like MCP integration, enterprise configurations, and advanced workflows
</Tip>

***

## Resume previous conversations

When a task spans multiple sittings, pick up where you left off instead of re-explaining context. Claude Code saves every conversation locally.

```bash theme={null}
claude --continue
```

This resumes the most recent session in the current directory; if there isn't one yet, it prints `No conversation found to continue` and exits. Use `claude --resume` to choose from a list, or `/resume` from inside a running session. See [Manage sessions](/en/sessions) for naming, branching, and the full picker reference.

## Run parallel sessions with worktrees

Work on a feature in one terminal while Claude fixes a bug in another, without the edits colliding. Each worktree is a separate checkout on its own branch.

```bash theme={null}
claude --worktree feature-auth
```

Run the same command with a different name in a second terminal to start an isolated parallel session. See [Worktrees](/en/worktrees) for cleanup, `.worktreeinclude`, and non-git VCS support.

## Plan before editing

For changes you want to review before they touch disk, switch to plan mode. Claude reads files and proposes a plan but makes no edits until you approve.

```bash theme={null}
claude --permission-mode plan
```

You can also press `Shift+Tab` mid-session to toggle into plan mode. See [Plan mode](/en/permission-modes#analyze-before-you-edit-with-plan-mode) for the approval flow and editing the plan in your text editor.

## Delegate research to subagents

Exploring a large codebase fills your context with file reads. Delegate the exploration so only the findings come back.

```text theme={null}
use a subagent to investigate how our auth system handles token refresh
```

The subagent reads files in its own context window and reports a summary. See [Subagents](/en/sub-agents) for defining custom agents with their own tools and prompts.

## Pipe Claude into scripts

Run Claude non-interactively for CI, pre-commit hooks, or batch processing. Stdin and stdout work like any Unix tool.

```bash theme={null}
git log --oneline -20 | claude -p "summarize these recent commits"
```

See [Non-interactive mode](/en/headless) for output formats, permission flags, and fan-out patterns.

## Next steps

<CardGroup cols={2}>
  <Card title="Best practices" icon="lightbulb" href="/en/best-practices">
    Patterns for getting the most out of Claude Code
  </Card>

  <Card title="Manage sessions" icon="rotate-left" href="/en/sessions">
    Resume, name, and branch conversations
  </Card>

  <Card title="Worktrees" icon="code-branch" href="/en/worktrees">
    Run isolated parallel sessions
  </Card>

  <Card title="Extend Claude Code" icon="puzzle-piece" href="/en/features-overview">
    Add skills, hooks, MCP, subagents, and plugins
  </Card>
</CardGroup>
