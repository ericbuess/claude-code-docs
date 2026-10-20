> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Common workflows

> Step-by-step guides for exploring codebases, fixing bugs, refactoring, testing, and other everyday tasks with Claude Code.

This page collects short recipes for everyday development. For higher-level guidance on prompting and context management, see [Best practices](/docs/en/best-practices).

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

For configuring Claude Code in a monorepo or large codebase, see [Monorepos and large repos](/docs/en/large-codebases).

#### Get a quick codebase overview

Suppose you've just joined a new project and need to understand its structure quickly.

**1. Navigate to the project root directory**

```bash theme={null}
cd /path/to/project 
```

Replace `/path/to/project` with the path to your project.

**2. Start Claude Code**

```bash theme={null}
claude 
```

**3. Ask for a high-level overview**

```text wrap theme={null}
give me an overview of this codebase
```

**4. Dive deeper into specific components**

```text wrap theme={null}
explain the main architecture patterns used here
```

```text wrap theme={null}
what are the key data models?
```

```text wrap theme={null}
how is authentication handled?
```

> [!TIP]
>
> Tips:
>
> * Start with broad questions, then narrow down to specific areas
> * Ask about coding conventions and patterns used in the project
> * Request a glossary of project-specific terms

#### Find relevant code

Suppose you need to locate code related to a specific feature or functionality.

**1. Ask Claude to find relevant files**

```text wrap theme={null}
find the files that handle user authentication
```

**2. Get context on how components interact**

```text wrap theme={null}
how do these authentication files work together?
```

**3. Understand the execution flow**

```text wrap theme={null}
trace the login process from front-end to database
```

> [!TIP]
>
> Tips:
>
> * Be specific about what you're looking for
> * Use domain language from the project
> * Install a [code intelligence plugin](/docs/en/plugins/code-intelligence) for your language to give Claude precise "go to definition" and "find references" navigation

***

### Fix bugs efficiently

Suppose you've encountered an error message and need to find and fix its source.

**1. Share the error with Claude**

```text wrap theme={null}
I'm seeing an error when I run npm test
```

**2. Ask for fix recommendations**

```text wrap theme={null}
suggest a few ways to fix the @ts-ignore in user.ts
```

**3. Apply the fix**

```text wrap theme={null}
update user.ts to add the null check you suggested
```

> [!TIP]
>
> Tips:
>
> * Tell Claude the command to reproduce the issue and get a stack trace
> * Mention any steps to reproduce the error
> * Let Claude know if the error is intermittent or consistent

***

### Refactor code

Suppose you need to update old code to use modern patterns and practices.

For porting an entire codebase to a new language, see [how Anthropic runs large-scale code migrations with Claude Code](https://claude.com/blog/ai-code-migration) on the blog.

**1. Identify legacy code for refactoring**

```text wrap theme={null}
find deprecated API usage in our codebase
```

**2. Get refactoring recommendations**

```text wrap theme={null}
suggest how to refactor utils.js to use modern JavaScript features
```

**3. Apply the changes safely**

```text wrap theme={null}
refactor utils.js to use ES2024 features while maintaining the same behavior
```

**4. Verify the refactoring**

```text wrap theme={null}
run tests for the refactored code
```

> [!TIP]
>
> Tips:
>
> * Ask Claude to explain the benefits of the modern approach
> * Request that changes maintain backward compatibility when needed
> * Do refactoring in small, testable increments

***

### Work with tests

Suppose you need to add tests for uncovered code.

**1. Identify untested code**

```text wrap theme={null}
find functions in NotificationsService.swift that are not covered by tests
```

**2. Generate test scaffolding**

```text wrap theme={null}
add tests for the notification service
```

**3. Add meaningful test cases**

```text wrap theme={null}
add test cases for edge conditions in the notification service
```

**4. Run and verify tests**

```text wrap theme={null}
run the new tests and fix any failures
```

Claude can generate tests that follow your project's existing patterns and conventions. When asking for tests, be specific about what behavior you want to verify. Claude examines your existing test files to match the style, frameworks, and assertion patterns already in use.

To improve coverage, ask Claude to identify edge cases you might have missed. Claude can analyze your code paths and suggest tests for error conditions, boundary values, and unexpected inputs that are often overlooked.

***

### Create pull requests

You can create pull requests by asking Claude directly ("create a pr for my changes"), or guide Claude through it step-by-step:

**1. Summarize your changes**

```text wrap theme={null}
summarize the changes I've made to the authentication module
```

**2. Generate a pull request**

```text wrap theme={null}
create a pr
```

**3. Review and refine**

```text wrap theme={null}
enhance the PR description with more context about the security improvements
```

To find the session later, run `claude --from-pr 1234` with your own PR number, which opens the session picker filtered to sessions linked to that PR, or paste the PR URL into the [`/resume` picker](/docs/en/sessions#use-the-session-picker) search. Claude Code links the session to the PR when Claude creates it with `gh pr create` or `glab mr create`, and when Claude [works on an existing PR](/docs/en/agent-view#pull-request-status).

> [!TIP]
>
> Review Claude's generated PR before submitting and ask Claude to highlight potential risks or considerations.

### Handle documentation

Suppose you need to add or update documentation for your code.

**1. Identify undocumented code**

```text wrap theme={null}
find functions without proper JSDoc comments in the auth module
```

**2. Generate documentation**

```text wrap theme={null}
add JSDoc comments to the undocumented functions in auth.js
```

**3. Review and enhance**

```text wrap theme={null}
improve the generated documentation with more context and examples
```

**4. Verify documentation**

```text wrap theme={null}
check if the documentation follows our project standards
```

> [!TIP]
>
> Tips:
>
> * Specify the documentation style you want (JSDoc, docstrings, etc.)
> * Ask for examples in the documentation
> * Request documentation for public APIs, interfaces, and complex logic

***

### Work in notes and non-code folders

Claude Code works in any directory. Run it inside a notes vault, a documentation folder, or any collection of markdown files to search, edit, and reorganize content the same way you would code.

The `.claude/` directory and `CLAUDE.md` sit alongside other tools' config directories without conflict. Claude reads files fresh on each tool call, so it sees edits you make in another application the next time it reads that file.

***

### Work with images

Suppose you need to work with images in your codebase, and you want Claude's help analyzing image content.

**1. Add an image to the conversation**

You can use any of these methods:

1. Drag and drop an image into the Claude Code window
2. Copy an image and paste it into the CLI with `Ctrl+V`, or with [`Alt+V` on Windows and WSL](/docs/en/interactive-mode#general-controls)
3. Provide an image path to Claude, for example "Analyze this image: /path/to/your/image.png"

**2. Ask Claude to analyze the image**

```text wrap theme={null}
What does this image show?
```

```text wrap theme={null}
Describe the UI elements in this screenshot
```

```text wrap theme={null}
Are there any problematic elements in this diagram?
```

**3. Use images for context**

```text wrap theme={null}
Here's a screenshot of the error. What's causing it?
```

```text wrap theme={null}
This is our current database schema. How should we modify it for the new feature?
```

**4. Get code suggestions from visual content**

```text wrap theme={null}
Generate CSS to match this design mockup
```

```text wrap theme={null}
What HTML structure would recreate this component?
```

> [!TIP]
>
> Tips:
>
> * Use images when text descriptions would be unclear or cumbersome
> * Include screenshots of errors, UI designs, or diagrams for better context
> * You can work with multiple images in a conversation
> * Image analysis works with diagrams, screenshots, mockups, and more
> * When Claude references images (for example, `[Image #1]`), `Cmd+Click` (Mac) or `Ctrl+Click` (Windows/Linux) the link to open the image in your default viewer

***

### Reference files and directories

Use @ to quickly include files or directories without waiting for Claude to read them.

**1. Reference a single file**

```text wrap theme={null}
Explain the logic in @src/utils/auth.js
```

This includes the content of the file in the conversation when it fits the [Read tool](/docs/en/tools-reference#read-tool-behavior)'s token limit, 25,000 tokens by default. A text file larger than 256KB isn't included.

**2. Reference a directory**

```text wrap theme={null}
What's the structure of @src/components?
```

**3. Reference MCP resources**

```text wrap theme={null}
Show me the data from @github:repos/owner/repo/issues
```

This fetches data from connected MCP servers using the format @server:resource. See [MCP resources](/docs/en/mcp#use-mcp-resources) for details.

> [!TIP]
>
> Tips:
>
> * File paths can be relative or absolute
> * Type `@` to open a path suggestion menu, then press Enter or Tab to accept the highlighted path and Enter again to send the message
> * @ file references add `CLAUDE.md` in the file's directory and parent directories to context
> * Directory references show file listings, not contents
> * You can reference multiple files in a single message (for example, "@file1.js and @file2.js")

To stop `@` references from including file contents and directory listings in your message, set [`CLAUDE_CODE_DISABLE_FILE_MENTIONS=1`](/docs/en/env-vars#variables) in your shell or user settings. Claude then receives the paths you referenced with a note to read them using its file tools. The variable requires Claude Code v2.1.299 or later, and Claude Code ignores it in project and local settings.

***

### Run Claude on a schedule

Suppose you want Claude to handle a task automatically on a recurring basis, like reviewing open PRs every morning, auditing dependencies weekly, or checking for CI failures overnight.

Pick a scheduling option based on where you want the task to run:

| Option | Where it runs | Best for |
| :- | :- | :- |
| [Cloud scheduled tasks](/docs/en/routines) | Cloud, Anthropic-managed by default | Tasks that should run even when your computer is off. Can also trigger on API calls or GitHub events in addition to a schedule. Configure at [claude.ai/code/routines](https://claude.ai/code/routines). |
| [Desktop scheduled tasks](/docs/en/desktop-scheduled-tasks) | Your machine, via the desktop app | Tasks that need direct access to local files, tools, or uncommitted changes. |
| [GitHub Actions](/docs/en/github-actions) | Your CI pipeline | Tasks tied to repo events like opened PRs, or cron schedules that should live alongside your workflow config. |
| [`/loop`](/docs/en/scheduled-tasks) | The current CLI session | Quick polling while a session is open. `--resume` and `--continue` restore unexpired fixed-interval loops. |

> [!TIP]
>
> When writing prompts for scheduled tasks, be explicit about what success looks like and what to do with results. The task runs autonomously, so it can't ask clarifying questions. For example: "Review open PRs labeled `needs-review`, leave inline comments on any issues, and post a summary in the `#eng-reviews` Slack channel."

***

### Ask Claude about its capabilities

Claude can answer questions about its own features and limitations. It looks up the answers in the current Claude Code documentation, so they aren't limited to the version you're running.

#### Example questions

```text wrap theme={null}
can Claude Code create pull requests?
```

```text wrap theme={null}
how does Claude Code handle permissions?
```

```text wrap theme={null}
what skills are available?
```

```text wrap theme={null}
how do I use MCP with Claude Code?
```

```text wrap theme={null}
how do I configure Claude Code for Amazon Bedrock?
```

```text wrap theme={null}
what are the limitations of Claude Code?
```

> [!NOTE]
>
> Claude provides documentation-based answers to these questions. For hands-on demonstrations, run `/powerup` for interactive lessons with animated demos, or refer to the specific workflow sections above.

> [!TIP]
>
> Tips:
>
> * Ask specific questions to get detailed answers
> * Claude can explain complex features like MCP integration, enterprise configurations, and advanced workflows

***

## Resume previous conversations

When a task spans multiple sittings, pick up where you left off instead of re-explaining context. Claude Code saves every conversation locally.

```bash theme={null}
claude --continue
```

This resumes the most recent session in the current directory; if there isn't one yet, it prints `No conversation found to continue` and exits. Use `claude --resume` to choose from a list, or `/resume` from inside a running session. See [Manage sessions](/docs/en/sessions) for naming, branching, and the full picker reference.

## Run parallel sessions with worktrees

Work on a feature in one terminal while Claude fixes a bug in another, without the edits colliding. Each [git worktree](https://git-scm.com/docs/git-worktree) is a separate checkout on its own branch, created from an existing commit, so the repository needs at least one commit first.

```bash theme={null}
claude --worktree feature-auth
```

Run the same command with a different name in a second terminal to start an isolated parallel session. In a repository with no commits, the command fails with `Failed to resolve base branch "HEAD": git rev-parse failed`. See [Worktrees](/docs/en/worktrees) for cleanup, `.worktreeinclude`, and non-git VCS support. To monitor parallel sessions from one screen instead of separate terminals, see [background agents](/docs/en/agent-view).

## Plan before editing

For changes you want to review before they touch disk, switch to plan mode. Claude reads files and proposes a plan but makes no edits until you approve. The status bar shows `⏸ plan mode on` while plan mode is active.

```bash theme={null}
claude --permission-mode plan
```

You can also press `Shift+Tab` mid-session until the status bar shows `⏸ plan mode on`. See [Plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) for the approval flow and editing the plan in your text editor.

## Delegate research to subagents

Exploring a large codebase fills your context with file reads. Delegate the exploration so only the findings come back.

```text wrap theme={null}
use a subagent to investigate how our auth system handles token refresh
```

The subagent reads files in its own context window and reports a summary. See [Subagents](/docs/en/sub-agents) for defining custom agents with their own tools and prompts.

## Pipe Claude into scripts

Run Claude non-interactively for CI, pre-commit hooks, or batch processing. Stdin and stdout work like any Unix tool.

```bash theme={null}
git log --oneline -20 | claude -p "summarize these recent commits"
```

See [Non-interactive mode](/docs/en/headless) for output formats, permission flags, and fan-out patterns.

## Next steps

> **[Best practices](/docs/en/best-practices)**
>
> Patterns for getting the most out of Claude Code

> **[Manage sessions](/docs/en/sessions)**
>
> Resume, name, and branch conversations

> **[Worktrees](/docs/en/worktrees)**
>
> Run isolated parallel sessions

> **[Extend Claude Code](/docs/en/features-overview)**
>
> Add skills, hooks, MCP, subagents, and plugins
