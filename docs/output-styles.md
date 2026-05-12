> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Output styles

> Adapt Claude Code for uses beyond software engineering

Output styles change how Claude responds, not what Claude knows. They modify the system prompt to set role, tone, and output format while keeping core capabilities like running scripts, reading and writing files, and tracking TODOs. Use one when you keep re-prompting for the same voice or format every turn, or when you want Claude to act as something other than a software engineer.

For instructions about your project, conventions, or codebase, use [CLAUDE.md](/en/memory) instead.

## Built-in output styles

Claude Code's **Default** output style is the existing system prompt, designed
to help you complete software engineering tasks efficiently.

There are three additional built-in output styles:

* **Proactive**: Claude executes immediately, makes reasonable assumptions
  instead of pausing for routine decisions, and prefers action over planning.
  This applies the same guidance as
  [auto mode](/en/permission-modes#eliminate-prompts-with-auto-mode) without
  changing your permission mode, so you still see permission prompts before
  tools run.

* **Explanatory**: Provides educational "Insights" in between helping you
  complete software engineering tasks. Helps you understand implementation
  choices and codebase patterns.

* **Learning**: Collaborative, learn-by-doing mode where Claude will not only
  share "Insights" while coding, but also ask you to contribute small, strategic
  pieces of code yourself. Claude Code will add `TODO(human)` markers in your
  code for you to implement.

## How output styles work

Output styles directly modify Claude Code's system prompt.

* Custom output styles exclude instructions for coding (such as verifying code
  with tests), unless `keep-coding-instructions` is true.
* All output styles have their own custom instructions added to the end of the
  system prompt.
* All output styles trigger reminders for Claude to adhere to the output style
  instructions during the conversation.

Token usage depends on the style. Adding instructions to the system prompt
increases input tokens, though prompt caching reduces this cost after the first
request in a session. The built-in Explanatory and Learning styles produce
longer responses than Default by design, which increases output tokens. For
custom styles, output token usage depends on what your instructions tell Claude
to produce.

## Change your output style

Run `/config` and select **Output style** to pick a style from a menu. Your
selection is saved to `.claude/settings.local.json` at the
[local project level](/en/settings).

To set a style without the menu, edit the `outputStyle` field directly in a
settings file:

```json theme={null}
{
  "outputStyle": "Explanatory"
}
```

Because the output style is set in the system prompt at session start,
changes take effect the next time you start a new session. This keeps the system
prompt stable throughout a conversation so prompt caching can reduce latency and
cost.

## Create a custom output style

Custom output styles are Markdown files with frontmatter and the text that will
be added to the system prompt:

```markdown theme={null}
---
name: My Custom Style
description:
  A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

You can save these files at three levels:

* User: `~/.claude/output-styles`
* Project: `.claude/output-styles`
* Managed policy: `.claude/output-styles` inside the [managed settings directory](/en/settings#settings-files)

[Plugins](/en/plugins-reference) can also ship output styles in an `output-styles/` directory.

### Frontmatter

Output style files support frontmatter for specifying metadata:

| Frontmatter                | Purpose                                                                                                                                                                                                                                      | Default                 |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------- |
| `name`                     | Name of the output style, if not the file name                                                                                                                                                                                               | Inherits from file name |
| `description`              | Description of the output style, shown in the `/config` picker                                                                                                                                                                               | None                    |
| `keep-coding-instructions` | Whether to keep the parts of Claude Code's system prompt related to coding.                                                                                                                                                                  | false                   |
| `force-for-plugin`         | Plugin output styles only: apply this style automatically whenever the plugin is enabled, without requiring users to select it. Overrides the user's `outputStyle` setting. If multiple enabled plugins set this, the first one loaded wins. | false                   |

## Comparisons to related features

### Output Styles vs. CLAUDE.md vs. --append-system-prompt

Choose based on whether Claude should stop acting as a coding assistant or keep
its default role and learn more. Output styles replace the software-engineering
parts of Claude Code's system prompt with your own role and voice, so use one
when Claude should adopt a different identity, like a writing editor or a
data-analysis assistant. CLAUDE.md and `--append-system-prompt` both keep
Claude Code's default identity and add to it, so use them when Claude should
remain a coding assistant that also follows your project conventions or extra
instructions.

The mechanisms differ as well. Output styles edit the system prompt directly.
CLAUDE.md adds its contents as a user message after the system prompt.
`--append-system-prompt` appends content to the end of the system prompt without
removing anything.

### Output Styles vs. [Agents](/en/sub-agents)

Use an output style to change how the main conversation responds in every
session. Use a [subagent](/en/sub-agents) when you want a separately scoped
helper that the main conversation delegates to. Output styles affect only the
system prompt of the main agent loop. Agents handle specific tasks and can carry
their own model, tools, and context about when to invoke them.

### Output Styles vs. [Skills](/en/skills)

Output styles modify how Claude responds (formatting, tone, structure) and are always active once selected. Skills are task-specific prompts that you invoke with `/skill-name` or that Claude loads automatically when relevant. Use output styles for consistent formatting preferences; use skills for reusable workflows and tasks.
