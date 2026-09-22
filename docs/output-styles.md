> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Output styles

> Change Claude Code's role, tone, and response format with a built-in output style such as Concise or Explanatory, or write a custom style.

An output style is a set of instructions that sets Claude's role, tone, and response format for every response in a session. Claude Code includes four built-in styles besides its default, and you can write your own.

Use an output style to change the way Claude responds and works with you for a whole session, so you don't repeat the request in each prompt. For example, a built-in style can make responses shorter, add an explanation of each change, or have Claude start work without asking routine questions. A custom style can also turn Claude into something other than a software engineer, such as a writing assistant or a data analyst.

* To use a built-in style, pick one from the [built-in output styles](#built-in-output-styles) and [switch to it](#change-your-output-style).
* To write your own instructions, [create a custom output style](#create-a-custom-output-style).

<Note>
  An output style gives Claude instructions to follow. It doesn't guarantee that something always happens or never happens. Some needs fit a different feature:

  * For what Claude should know about your project, use [CLAUDE.md](/docs/en/memory).
  * For something that has to happen every time, such as formatting after each edit or blocking a command, use a [hook](/docs/en/hooks-guide).
  * For skills, subagents, and the other options, see [Choose between an output style and other features](#choose-between-an-output-style-and-other-features).
</Note>

## Built-in output styles

Claude Code starts in the [**Default**](#default) style, its standard instructions for completing software engineering tasks. Each of the four other built-in styles keeps those instructions and adds its own.

This table shows what each style changes about a session and when it fits:

| Style                       | What changes                                                                                              | Use it when                                                                                                    |
| :-------------------------- | :-------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------- |
| [Proactive](#proactive)     | Claude starts work right away and makes reasonable assumptions rather than asking about routine decisions | You want Claude to keep working through routine decisions, and you'll correct course if an assumption is wrong |
| [Concise](#concise)         | Responses lead with the result and leave out preamble, narration, and recaps                              | Default responses are longer than you want                                                                     |
| [Explanatory](#explanatory) | Claude adds short `Insight` blocks that explain the choices behind the code it writes                     | You're getting to know a codebase or want the reasoning along with the change                                  |
| [Learning](#learning)       | Claude explains its choices and leaves small pieces of code for you to write yourself                     | You want hands-on coding practice while the task still gets done                                               |

### Default

Default means no output style is selected. Claude Code adds no style instructions, and Claude works from Claude Code's standard system prompt, which is written for software engineering tasks.

`default` appears in the `/output-style` list with the other styles, so you [select it the same way](#change-your-output-style).

### Proactive

In the Proactive style, Claude starts implementing as soon as you send a task. It makes reasonable assumptions about routine decisions rather than stopping to ask, and it doesn't switch to plan mode unless you ask for a plan. You can redirect it at any point.

The style's instructions also tell Claude to check with you in the conversation before an action that deletes data or changes a shared or production system. That check is an instruction Claude follows and is separate from permission prompts.

Switching to the Proactive style doesn't change your [permission mode](/docs/en/permission-modes). Your permission mode still decides which tool calls run without asking you, so permission prompts appear the same way they did before you switched.

### Concise

In the Concise style, the first sentence of a response states what happened or what the answer is. Claude leaves out the lead-in, the step-by-step narration, and the closing recap, and answers a simple question in one to three sentences. It does the engineering work as thoroughly as in the Default style. Requires Claude Code v2.1.237 or later.

Claude still writes at full length in these cases:

* **Anything you ask for**: when you ask for an explanation or more detail, Claude answers in full.
* **Anything you need in order to act safely**: error reports, failing test output, security warnings, and confirmations for destructive actions keep their complete content.

### Explanatory

In the Explanatory style, Claude does the task the way it does in the Default style and adds short explanations of why it made the choices it made. Each explanation appears in the conversation, before or after the code it's about, in a block labeled `Insight`. The explanations aren't written into your files as comments.

An `Insight` block carries two or three points about your codebase or the code Claude wrote, such as this one after adding an API endpoint:

```text theme={null}
★ Insight ─────────────────────────────────────
- Every route in this repo goes through the withAuth wrapper, so the new endpoint gets session checks without its own middleware.
- Rate limits are set per route in limits.ts, which is why this change adds an entry there rather than a global default.
─────────────────────────────────────────────────
```

### Learning

In the Learning style, Claude adds the same `Insight` blocks as the [Explanatory style](#explanatory) and also asks you to write some of the code. Claude handles routine implementation itself. When it reaches a piece with a real design decision, such as error handling, a data structure, or business logic with more than one valid approach, it leaves a few lines for you.

Claude marks the spot with a `TODO(human)` comment in the file, then sends a request that says what's already built, what to write, and what to weigh:

```text theme={null}
● Learn by Doing

Context: The upload form is in place and calls validateFile() before accepting a file. Size and type checks work for images, but the switch statement has no handling for documents yet.

Your Task: In upload.js, implement the case "document" branch inside validateFile(). Look for TODO(human).

Guidance: Decide on a size limit for documents and whether the file extension has to match the MIME type. Return {valid: boolean, error?: string}.
```

Claude then stops and waits. Write your code at the `TODO(human)` comment and tell Claude when you're done. Claude responds with one `Insight` about your code and continues the task.

## Change your output style

Pick a style with the command, a menu, or a settings file. The command and both menus save your choice to `.claude/settings.local.json` at the [local project level](/docs/en/settings).

* **`/output-style` command**: run `/output-style <style>` to switch, for example `/output-style concise`. With no argument, the command lists the styles you can pick and marks the current one.

  The command also works in [non-interactive mode](/docs/en/headless) and Agent SDK sessions, and from the mobile app or web via [Remote Control](/docs/en/remote-control#limitations), where you can list and select only [built-in styles](#built-in-output-styles). Requires Claude Code v2.1.269 or later.
* **Terminal menu**: run `/config` and select **Output style** to pick a style from a menu.
* **VS Code extension**: open the [command menu](/docs/en/vs-code#use-the-prompt-box) with `/` and select **Output styles** to pick a style, including your custom styles. Requires Claude Code v2.1.257 or later.
* **Desktop app**: set the `outputStyle` field in a settings file, for example `.claude/settings.local.json`, the file the terminal menu writes. When you run `/config` there, Claude Code [opens **Settings > Claude Code**](/docs/en/desktop#what’s-not-available-in-desktop) rather than a menu.

To set a style without the menu, edit the `outputStyle` field directly in a settings file:

```json theme={null}
{
  "outputStyle": "Explanatory"
}
```

The value is case-sensitive, so write the built-in names as `Proactive`, `Concise`, `Explanatory`, and `Learning`. A value that doesn't match a style name exactly, such as `explanatory`, gives you the Default style. The `/output-style` command ignores case.

To make a style your default across projects, set `outputStyle` in `~/.claude/settings.json`. A project's own settings files [take precedence](/docs/en/settings#settings-precedence) over that value.

When you switch styles mid-session, Claude uses the new style starting with your next message. For what that first message costs in prompt caching, see [Changing output style](/docs/en/prompt-caching#changing-output-style). Before v2.1.251, the new style applied only after you ran `/clear` or started a new session.

## Create a custom output style

A custom output style is a Markdown file: frontmatter for metadata, then the instructions for Claude.

In the VS Code extension, you can also create the file from the [**Output styles** menu](/docs/en/vs-code#use-the-prompt-box) rather than writing it by hand. This requires Claude Code v2.1.261 or later.

<Steps>
  <Step title="Create a Markdown file">
    Save it at one of three levels. The file name becomes the style name unless you set `name` in the frontmatter.

    * User: `~/.claude/output-styles`
    * Project: `.claude/output-styles`
    * Managed policy: `.claude/output-styles` inside the [managed settings directory](/docs/en/managed-settings#delivery-mechanisms)

    Project output styles load from every `.claude/output-styles/` between the working directory and the repository root. When more than one of these nested directories defines a style with the same name, Claude Code uses the one closest to the working directory.
  </Step>

  <Step title="Add frontmatter and instructions">
    Decide whether to keep Claude Code's software engineering instructions. Set `keep-coding-instructions: true` if you're changing how Claude communicates but still want it coding the same way. Leave it out if Claude won't be doing software engineering.

    This example leads every explanation with a diagram while keeping Claude's coding behavior:

    ```markdown theme={null}
    ---
    name: Diagrams first
    description: Lead every explanation with a diagram
    keep-coding-instructions: true
    ---

    When explaining code, architecture, or data flow, start with a Mermaid diagram showing the structure, then explain in prose.

    ## Diagram conventions

    Use `flowchart TD` for control flow and `sequenceDiagram` for request paths. Keep diagrams under 15 nodes.
    ```
  </Step>

  <Step title="Switch to your style">
    Run `/output-style <style>` in the terminal, or run `/config` and select your style under **Output style**. Claude uses the new style starting with your next message. In the terminal, Claude Code reads style files when it starts, so if you create or edit one during a running session, restart Claude Code to pick up the change.
  </Step>
</Steps>

[Plugins](/docs/en/plugins-reference) can also ship output styles in an `output-styles/` directory.

<h3 id="frontmatter">
  Frontmatter reference
</h3>

Configure an output style with YAML [frontmatter](/docs/en/glossary#frontmatter) between `---` markers at the top of the file. All fields are optional, and field names use lowercase words separated by hyphens. A misspelled field is ignored without an error. If the YAML doesn't parse, the style still loads under its file name with no fields set; run `claude --debug` to see the parse error.

| Field                      | Required | Description                                                                                                                                                                                                                                                                                |
| :------------------------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                     | No       | Name of the output style, shown in the `/config` picker. Default: the file name                                                                                                                                                                                                            |
| `description`              | No       | Description of the output style, shown in the `/config` picker                                                                                                                                                                                                                             |
| `keep-coding-instructions` | No       | Set to `true` to keep Claude Code's built-in software engineering instructions alongside your style. Default: `false`                                                                                                                                                                      |
| `force-for-plugin`         | No       | Plugin output styles only. Set to `true` to apply this style automatically whenever the plugin is enabled, without requiring users to select it. Overrides the user's `outputStyle` setting. If multiple enabled plugins set this, Claude Code uses the first one loaded. Default: `false` |

<span id="comparisons-to-related-features" />

## Choose between an output style and other features

An output style applies to every response in a session. It's an instruction Claude follows, so nothing enforces it. When what you want is narrower than every response, or has to happen without fail, another feature fits better.

This table matches what you want to the feature that does it:

| You want                                                                                                   | Use                                                               | Why it fits                                                                                                  |
| :--------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| Every response in a certain voice, length, or format, or Claude in a different role                        | An output style                                                   | It applies to the whole session, and you switch styles with one command                                      |
| Claude to know your project's conventions, commands, and structure                                         | [CLAUDE.md](/docs/en/memory)                                           | It holds what Claude should know about the codebase, and it stays loaded whichever style you pick            |
| Instructions for one kind of task, such as a release checklist or a review procedure                       | A [skill](/docs/en/skills)                                             | Claude loads it only when you invoke it or the task matches, so it doesn't shape unrelated responses         |
| Something to happen every time without exception, such as formatting after each edit or blocking a command | A [hook](/docs/en/hooks-guide)                                         | Claude Code runs a hook itself at a lifecycle event, so it doesn't depend on Claude following an instruction |
| A helper with its own instructions, model, and tools for a focused task                                    | A [subagent](/docs/en/sub-agents)                                      | It runs in a separate context with its own system prompt and returns a summary to your conversation          |
| An addition to Claude's instructions that you pass when you start Claude Code                              | [`--append-system-prompt`](/docs/en/cli-reference#system-prompt-flags) | It appends to the system prompt without removing anything                                                    |

These features combine. For example, you can use CLAUDE.md for what Claude should know, an output style for how it responds, and a hook for anything that has to be guaranteed. [Extend Claude Code](/docs/en/features-overview) compares the rest of the extension features.

## How output styles work

An output style changes the instructions Claude Code gives Claude.

* Claude Code sends the active style's instructions with every request.
* Custom output styles leave out Claude Code's built-in software engineering instructions, such as how to scope changes, write comments, and verify work, unless `keep-coding-instructions` is set to `true`.

Output styles apply to the main conversation and to a [fork](/docs/en/sub-agents#fork-the-current-conversation), which inherits the parent's full conversation and system prompt. Other [subagents run their own system prompt](/docs/en/sub-agents#what-loads-at-startup), so styles don't change how they respond.

Token usage depends on the style. A style's instructions add input tokens, though prompt caching reduces this cost after the first request in a session.

The built-in Explanatory and Learning styles produce longer responses than Default by design, which increases output tokens. The Concise style does the opposite by instructing Claude to keep responses short by default. For custom styles, output token usage depends on what your instructions tell Claude to produce.

## Related resources

* [Settings](/docs/en/settings): where the `outputStyle` field lives and how settings precedence works
* [Permission modes](/docs/en/permission-modes): how the Proactive style compares to auto mode
* [Plugins](/docs/en/plugins): package and distribute output styles alongside skills, hooks, and agents
* [Debug your configuration](/docs/en/debug-your-config): diagnose why an output style isn't taking effect
