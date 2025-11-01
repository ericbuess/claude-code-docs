# Output styles

> [DEPRECATED] Adapt Claude Code for uses beyond software engineering

<Warning>
  Output styles are **DEPRECATED.**  On **November 5, 2025** or later, we'll
  stop supporting the output styles feature. Use `--system-prompt-file`,
  `--system-prompt`, `--append-system-prompt`, CLAUDE.md, or [plugins](/en/docs/claude-code/plugins) instead.
  For **Explanatory** output style users, you can reference the ([explanatory-output-style
  plugin](https://github.com/anthropics/claude-code/tree/main/plugins/explanatory-output-style)
  in our public repository.)
</Warning>

## Deprecation timeline

As of **November 5, 2025**, Claude Code will:

* Stop supporting the output styles feature
* Remove the `/output-style` command and related functionality

## Alternative for Custom Output Styles

Use `--system-prompt-file` to start a Claude Code session with your own system
prompt. You can also use `--system-prompt` to pass in a string to use as the system prompt, or
`--append-system-prompt` to add to the default Claude Code system prompt.

## Alternative for Explanatory Output Style: explanatory-output-style Plugin

Plugins provide more powerful and flexible ways to customize Claude Code's
behavior. The
[`explanatory-output-style` plugin](https://github.com/anthropics/claude-code/tree/main/plugins/explanatory-output-style)
recreates the deprecated Explanatory output style functionality.

### Example: Explanatory Output Style Plugin

The `explanatory-output-style` plugin uses a SessionStart hook to inject
additional context that encourages Claude to provide educational insights.
Here's what it does:

* Provides educational insights about implementation choices
* Explains codebase patterns and decisions
* Balances task completion with learning opportunities

### Installing a plugin

To install a plugin like `explanatory-output-style`:

```shell Add the marketplace (if not already added) theme={null}
/plugin marketplace add anthropics/claude-code
```

```shell Install the plugin theme={null}
/plugin install explanatory-output-style@claude-code-plugins
```

```shell Restart Claude Code to activate the plugin theme={null}
/exit
```

```shell Disable the plugin theme={null}
/plugin manage explanatory-output-style@claude-code-plugins

1. Press enter when you see claude-code-marketplace
2. Press space when you see explanatory-output-style to toggle enabled
3. Press down to "Apply changes", then press enter
    You should see "Disabled 1 plugin. Restart Claude Code to apply changes."

/exit
```

For more details on plugins, see the
[Plugins documentation](/en/docs/claude-code/plugins).

***

## Reference: Original output styles documentation

<Note>
  The content below is preserved for reference only. Output styles are
  deprecated and will be removed on November 5, 2025. Please migrate to plugins,
  hooks, or subagents.
</Note>

Output styles allow you to use Claude Code as any type of agent while keeping
its core capabilities, such as running local scripts, reading/writing files, and
tracking TODOs.

### Built-in output styles

Claude Code's **Default** output style is the existing system prompt, designed
to help you complete software engineering tasks efficiently.

There are two additional built-in output styles focused on teaching you the
codebase and how Claude operates:

* **Explanatory**: Provides educational "Insights" in between helping you
  complete software engineering tasks. Helps you understand implementation
  choices and codebase patterns.

* **Learning**: Collaborative, learn-by-doing mode where Claude will not only
  share "Insights" while coding, but also ask you to contribute small, strategic
  pieces of code yourself. Claude Code will add `TODO(human)` markers in your
  code for you to implement.

### How output styles work

Output styles directly modify Claude Code's system prompt.

* Non-default output styles exclude instructions specific to code generation and
  efficient output normally built into Claude Code (such as responding concisely
  and verifying code with tests).
* Instead, these output styles have their own custom instructions added to the
  system prompt.

### Change your output style

You can either:

* Run `/output-style` to access the menu and select your output style (this can
  also be accessed from the `/config` menu)

* Run `/output-style [style]`, such as `/output-style explanatory`, to directly
  switch to a style

These changes apply to the [local project level](/en/docs/claude-code/settings)
and are saved in `.claude/settings.local.json`.

You can also create your own output style Markdown files and save them either at
the user level (`~/.claude/output-styles`) or the project level
(`.claude/output-styles`).

### Comparisons to related features

#### Output Styles vs. CLAUDE.md vs. System Prompt Flags

Output styles completely "turn off" the parts of Claude Code's default system
prompt specific to software engineering.

**CLAUDE.md** adds the contents as a user message *following* Claude Code's default system
prompt, rather than modifying the system prompt itself.

**System prompt CLI flags** provide different levels of control:

* `--append-system-prompt`: Appends text to the end of the default system prompt
* `--system-prompt`: Replaces the entire default system prompt with custom text
* `--system-prompt-file`: Loads a custom system prompt from a file

See the [CLI reference](/en/docs/claude-code/cli-reference#system-prompt-flags) for detailed guidance on when to use each flag.

#### Output Styles vs. [Agents](/en/docs/claude-code/sub-agents)

Output styles directly affect the main agent loop and only affect the system
prompt. Agents are invoked to handle specific tasks and can include additional
settings like the model to use, the tools they have available, and some context
about when to use the agent.

#### Output Styles vs. [Custom Slash Commands](/en/docs/claude-code/slash-commands)

You can think of output styles as “stored system prompts” and custom slash
commands as “stored prompts”.
