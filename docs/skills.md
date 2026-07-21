> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Extend Claude with skills

> Create, manage, and share skills to extend Claude's capabilities in Claude Code. Includes custom commands and bundled skills.

Skills extend what Claude can do. Create a `SKILL.md` file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you can invoke one directly with `/skill-name`.

Create a skill when you keep pasting the same instructions, checklist, or multi-step procedure into chat, or when a section of CLAUDE.md has grown into a procedure rather than a fact. Unlike CLAUDE.md content, a skill's body loads only when it's used, so long reference material costs almost nothing until you need it.

<Note>
  For built-in commands like `/help` and `/compact`, and bundled skills like `/debug` and `/code-review`, see the [commands reference](/docs/en/commands).

  **Custom commands have been merged into skills.** A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Your existing `.claude/commands/` files keep working. Skills add optional features: a directory for supporting files, frontmatter to [control whether you or Claude invokes them](#control-who-invokes-a-skill), and the ability for Claude to load them automatically when relevant.
</Note>

Claude Code skills follow the [Agent Skills](https://agentskills.io) open standard, which works across multiple AI tools. Claude Code extends the standard with additional features like [invocation control](#control-who-invokes-a-skill), [subagent execution](#run-skills-in-a-subagent), and [dynamic context injection](#inject-dynamic-context).

## Bundled skills

Claude Code includes a set of bundled skills that are available in every session unless disabled with the [`disableBundledSkills`](/docs/en/settings#available-settings) setting, including `/doctor`, `/code-review`, `/batch`, `/debug`, `/loop`, and `/claude-api`. Unlike most built-in commands, which execute fixed logic directly, bundled skills are prompt-based: they give Claude detailed instructions and let it orchestrate the work using its tools. You invoke them the same way as any other skill, by typing `/` followed by the skill name.

The [`/doctor`](/docs/en/commands#all-commands) setup checkup is the one exception to `disableBundledSkills` in Claude Code v2.1.205 and later: it stays typable when the setting is on. To hide it, set the `DISABLE_DOCTOR_COMMAND` environment variable or a [`skillOverrides`](#override-skill-visibility-from-settings) entry of `"doctor": "off"`. Before v2.1.205, `/doctor` was a built-in command rather than a bundled skill.

Bundled skills are listed alongside built-in commands in the [commands reference](/docs/en/commands), marked **Skill** in the Purpose column.

### Run and verify your app

Three bundled skills work together to launch your app and confirm changes against the running app instead of just tests:

| Skill                  | Purpose                                                                                                           |
| :--------------------- | :---------------------------------------------------------------------------------------------------------------- |
| `/run`                 | Launch and drive your app to see a change working                                                                 |
| `/verify`              | Build and run your app to confirm a code change does what it should, without falling back to tests or type checks |
| `/run-skill-generator` | Teach `/run` and `/verify` how to build and launch your project                                                   |

{/* min-version: 2.1.145 */}All three skills require Claude Code v2.1.145 or later. Check your version with `claude --version` or the `/status` command.

`/run` and `/verify` work without setup. They infer the launch from your project type (CLI, server, TUI, browser-driven) and from what's in your README, `package.json`, or `Makefile`. That inference gets unreliable for projects that need anything beyond a standard launch: a database, an env file, a graphical session, a multi-step build.

`/run-skill-generator` records the recipe instead. It gets your app running from a clean environment, captures what worked (the install commands, the env vars, the launch script), and commits it as a per-project skill at `.claude/skills/run-<name>/`. After that, `/run`, `/verify`, and any other agent in the repo follow the recorded recipe instead of rediscovering it. Run `/run-skill-generator` once per project, and again if the build or launch process changes.

## Getting started

### Create your first skill

This example creates a skill that summarizes the uncommitted changes in your git repository and flags anything risky. It pulls the live diff into the prompt before Claude reads it, so the response is grounded in your actual working tree rather than what Claude can guess from open files. Claude loads the skill automatically when you ask about your changes, or you can invoke it directly with `/summarize-changes`.

<Steps>
  <Step title="Create the skill directory">
    Create a directory for the skill in your personal skills folder. Personal skills are available across all your projects.

    ```bash theme={null}
    mkdir -p ~/.claude/skills/summarize-changes
    ```
  </Step>

  <Step title="Write SKILL.md">
    Every skill needs a `SKILL.md` file with two parts: YAML frontmatter between `---` markers that tells Claude when to use the skill, and markdown content with the instructions Claude follows when the skill runs. The directory name becomes the command you type, and the `description` helps Claude decide when to load the skill automatically.

    Save this to `~/.claude/skills/summarize-changes/SKILL.md`:

    ```yaml theme={null}
    ---
    description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
    ---

    ## Current changes

    !`git diff HEAD`

    ## Instructions

    Summarize the changes above in two or three bullet points, then list any risks you notice such as missing error handling, hardcoded values, or tests that need updating. If the diff is empty, say there are no uncommitted changes.
    ```

    The `` !`git diff HEAD` `` line uses [dynamic context injection](#inject-dynamic-context): Claude Code runs the command and replaces the line with its output before Claude sees the skill content, so the instructions arrive with the current diff already inlined.
  </Step>

  <Step title="Test the skill">
    Open a git project, make a small edit to any file, and start Claude Code by running `claude`. You can test the skill two ways.

    **Let Claude invoke it automatically** by asking something that matches the description:

    ```text theme={null}
    What did I change?
    ```

    **Or invoke it directly** with the skill name:

    ```text theme={null}
    /summarize-changes
    ```

    Either way, Claude should respond with a short summary of your edit and a list of risks.
  </Step>
</Steps>

### Where skills live

Where you store a skill determines who can use it:

| Location   | Path                                                | Applies to                     |
| :--------- | :-------------------------------------------------- | :----------------------------- |
| Enterprise | See [managed settings](/docs/en/settings#settings-files) | All users in your organization |
| Personal   | `~/.claude/skills/<skill-name>/SKILL.md`            | All your projects              |
| Project    | `.claude/skills/<skill-name>/SKILL.md`              | This project only              |
| Plugin     | `<plugin>/skills/<skill-name>/SKILL.md`             | Where plugin is enabled        |

When skills share the same name across levels, enterprise overrides personal, and personal overrides project. A skill at any of these levels also overrides a bundled skill with the same name. For example, a `code-review` skill in your project's `.claude/skills/` replaces the bundled `/code-review`. Plugin skills use a `plugin-name:skill-name` namespace, so they cannot conflict with other levels. If you have files in `.claude/commands/`, those work the same way, but if a skill and a command share the same name, the skill takes precedence.

Skills also load from nested `.claude/skills/` directories below your working directory. When Claude reads or edits a file in a subdirectory, skills from that subdirectory's `.claude/skills/` become available. This lets a monorepo package provide its own skills that apply when working on that package, even if the session started at the repo root.

If a nested skill shares a name with another skill, both stay available. For example, with a `deploy` skill at the project root and another in `apps/web/.claude/skills/`:

* The nested one appears under a directory-qualified name, `apps/web:deploy`.
* Its description says which directory it applies to.
* Claude picks the variant that matches the files it is working on.

Typing `/deploy` runs the project-root skill. Type the qualified name `/apps/web:deploy` to run the nested variant explicitly.

When you or Claude invoke the unqualified name, the project-root skill loads, and Claude Code appends a list of the directory-qualified variants to its content with an instruction to also invoke any variant whose directory holds the files Claude is working on. A nested skill therefore still applies to work in its directory when only the unqualified name is invoked. Requires Claude Code v2.1.203 or later.

A `<skill-name>` entry in the enterprise, personal, or project locations can be a symlink to a directory elsewhere on disk. Claude Code follows the symlink and reads `SKILL.md` from the target directory, and if the same target is reachable from more than one location, Claude Code loads the skill once. Plugin skills handle symlinks differently; see [Share files within a marketplace with symlinks](/docs/en/plugins-reference#share-files-within-a-marketplace-with-symlinks).

<Note>
  Add a `.claude-plugin/plugin.json` to a skill folder and it loads as a [plugin](/docs/en/plugins-reference#skills-directory-plugins) named `<name>@skills-dir`, so it can bundle agents, hooks, and MCP servers. In a project's `.claude/skills/`, this requires accepting the workspace trust dialog first.
</Note>

#### Live change detection

Claude Code watches skill directories for file changes. Adding, editing, or removing a skill under `~/.claude/skills/`, the project `.claude/skills/`, or a `.claude/skills/` inside an `--add-dir` directory takes effect within the current session without restarting. Creating a top-level skills directory that did not exist when the session started requires restarting Claude Code so the new directory can be watched.

<Note>
  Live change detection covers `SKILL.md` text only. For a skill folder that is also a [plugin](/docs/en/plugins-reference#skills-directory-plugins), changes to `hooks/`, `.mcp.json`, `agents/`, and `output-styles/` need `/reload-plugins` to take effect.
</Note>

#### Automatic discovery from parent and nested directories

Project skills load from `.claude/skills/` in your starting directory and in every parent directory up to the repository root, so starting Claude in a subdirectory still picks up skills defined at the root. When you work with files in subdirectories below your starting directory, Claude Code also discovers skills from nested `.claude/skills/` directories on demand. For example, if you're editing a file in `packages/frontend/`, Claude Code also looks for skills in `packages/frontend/.claude/skills/`. This supports monorepo setups where packages have their own skills.

Each skill is a directory with `SKILL.md` as the entrypoint:

```text theme={null}
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/
│   └── sample.md      # Example output showing expected format
└── scripts/
    └── validate.sh    # Script Claude can execute
```

The `SKILL.md` contains the main instructions and is required. Other files are optional and let you build more powerful skills: templates for Claude to fill in, example outputs showing the expected format, scripts Claude can execute, or detailed reference documentation. Reference these files from your `SKILL.md` so Claude knows what they contain and when to load them. See [Add supporting files](#add-supporting-files) for more details.

<Note>
  Files in `.claude/commands/` still work and support the same [frontmatter](#frontmatter-reference). Skills are recommended since they support additional features like supporting files.
</Note>

#### Skills from additional directories

The `--add-dir` flag and `/add-dir` command [grant file access](/docs/en/permissions#additional-directories-grant-file-access-not-configuration) rather than configuration discovery, but skills are an exception: `.claude/skills/` within an added directory is loaded automatically. This exception applies only to `--add-dir` and `/add-dir`. The `permissions.additionalDirectories` setting in `settings.json` grants file access only and does not load skills. See [Live change detection](#live-change-detection) for how edits are picked up during a session.

Other `.claude/` configuration such as commands and output styles is not loaded from additional directories. See the [exceptions table](/docs/en/permissions#additional-directories-grant-file-access-not-configuration) for the complete list of what is and isn't loaded, and the recommended ways to share configuration across projects.

<Note>
  CLAUDE.md files from `--add-dir` directories are not loaded by default. To load them, set `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`. See [Load from additional directories](/docs/en/memory#load-from-additional-directories).
</Note>

#### Skills in Cowork and cloud sessions

[Cowork](https://claude.com/product/cowork) sessions and [cloud sessions](/docs/en/claude-code-on-the-web#the-cloud-environment), including [routines](/docs/en/routines), don't read `~/.claude/skills/` on your machine. Both interactive and scheduled Cowork sessions load the skills enabled for your claude.ai account, synced at session start; manage them from **Customize** in the Desktop app sidebar or from the skills settings on claude.ai. Cloud sessions additionally load project skills committed to the cloned repository's `.claude/skills/`.

If a skill exists only in `~/.claude/skills/` on your machine, Claude Code reports that the skill was not found when a [routine](/docs/en/routines) invokes it, because each routine run starts as a fresh remote session. To make a personal skill available in these sessions:

* For Cowork and cloud sessions, enable the skill for your claude.ai account.
* For cloud sessions, you can instead commit the skill to the repository's `.claude/skills/`, or ship it in a plugin declared in the repository's `.claude/settings.json`. Repo-declared plugins [install at session start](/docs/en/claude-code-on-the-web#what’s-available-in-cloud-sessions); plugins enabled only in your user settings don't transfer.

[Desktop scheduled tasks](/docs/en/desktop-scheduled-tasks) are different: they run locally on your machine and load skills from the same locations as any other local session.

## Configure skills

Skills are configured through YAML frontmatter at the top of `SKILL.md` and the markdown content that follows.

### Types of skill content

Skill files can contain any instructions, but thinking about how you want to invoke them helps guide what to include:

**Reference content** adds knowledge Claude applies to your current work. Conventions, patterns, style guides, domain knowledge. This content runs inline so Claude can use it alongside your conversation context.

```yaml theme={null}
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

**Task content** gives Claude step-by-step instructions for a specific action, like deployments, commits, or code generation. These are often actions you want to invoke directly with `/skill-name` rather than letting Claude decide when to run them. Add `disable-model-invocation: true` to prevent Claude from triggering it automatically. The example below adds `context: fork`, which runs the skill in its own subagent context; see [Run skills in a subagent](#run-skills-in-a-subagent).

```yaml theme={null}
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

Your `SKILL.md` can contain anything, but thinking through how you want the skill invoked (by you, by Claude, or both) and where you want it to run (inline or in a subagent) helps guide what to include. For complex skills, you can also [add supporting files](#add-supporting-files) to keep the main skill focused.

Keep the body itself concise. Once a skill loads, its content [stays in context across turns](#skill-content-lifecycle), so every line is a recurring token cost. State what to do rather than narrating how or why, and apply the same conciseness test you would for [CLAUDE.md content](/docs/en/best-practices#write-an-effective-claude-md).

### Frontmatter reference

Beyond the markdown content, you can configure skill behavior using YAML frontmatter fields between `---` markers at the top of your `SKILL.md` file:

```yaml theme={null}
---
name: my-skill
description: What this skill does
disable-model-invocation: true
allowed-tools: Read Grep
---

Your skill instructions here...
```

All fields are optional. Only `description` is recommended so Claude knows when to use the skill.

| Field                      | Required    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| :------------------------- | :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                     | No          | Display name shown in skill listings. Defaults to the directory name. See [How a skill gets its command name](#how-a-skill-gets-its-command-name) for how this differs from the name you type to invoke the skill.                                                                                                                                                                                                                                       |
| `description`              | Recommended | What the skill does and when to use it. Claude uses this to decide when to apply the skill. If omitted, uses the first paragraph of markdown content. Put the key use case first: the combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing to reduce context usage.                                                                                                                                       |
| `when_to_use`              | No          | Additional context for when Claude should invoke the skill, such as trigger phrases or example requests. Appended to `description` in the skill listing and counts toward the 1,536-character cap.                                                                                                                                                                                                                                                       |
| `argument-hint`            | No          | Hint shown during autocomplete to indicate expected arguments. Example: `[issue-number]` or `[filename] [format]`.                                                                                                                                                                                                                                                                                                                                       |
| `arguments`                | No          | Named positional arguments for [`$name` substitution](#available-string-substitutions) in the skill content. Accepts a space-separated string or a YAML list. Names map to argument positions in order.                                                                                                                                                                                                                                                  |
| `disable-model-invocation` | No          | Set to `true` to prevent Claude from automatically loading this skill. Use for workflows you want to trigger manually with `/name`. Also prevents the skill from being [preloaded into subagents](/docs/en/sub-agents#preload-skills-into-subagents). {/* min-version: 2.1.196 */}As of v2.1.196, also prevents the skill from running when a [scheduled task](/docs/en/scheduled-tasks) fires with the skill as its prompt. Default: `false`.                     |
| `user-invocable`           | No          | Set to `false` to hide from the `/` menu. Use for background knowledge users shouldn't invoke directly. Default: `true`.                                                                                                                                                                                                                                                                                                                                 |
| `allowed-tools`            | No          | Tools Claude can use without asking permission during the turn that invokes this skill. The grant clears when you send your next message. Accepts a space- or comma-separated string, or a YAML list. See [Pre-approve tools for a skill](#pre-approve-tools-for-a-skill).                                                                                                                                                                               |
| `disallowed-tools`         | No          | Tools removed from Claude's available pool while this skill is active. Use for autonomous skills that should never call certain tools, such as `AskUserQuestion` for a background loop. Accepts a space- or comma-separated string, or a YAML list. The restriction clears when you send your next message. Like deny rules, the field can't remove [`EndConversation`](/docs/en/tools-reference#endconversation-tool-behavior) while any other tool remains. |
| `model`                    | No          | Model to use when this skill is active. The override applies for the rest of the current turn and is not saved to settings; the session model resumes on your next prompt. Accepts the same values as [`/model`](/docs/en/model-config), or `inherit` to keep the active model. A value excluded by your organization's [`availableModels`](/docs/en/model-config#restrict-model-selection) allowlist is not used and the session keeps its current model.         |
| `effort`                   | No          | [Effort level](/docs/en/model-config#adjust-effort-level) when this skill is active. Overrides the session effort level. Default: inherits from session. Options: `low`, `medium`, `high`, `xhigh`, `max`; available levels depend on the model.                                                                                                                                                                                                              |
| `context`                  | No          | Set to `fork` to run in a forked subagent context. See [Run skills in a subagent](#run-skills-in-a-subagent).                                                                                                                                                                                                                                                                                                                                            |
| `agent`                    | No          | Which subagent type to use when `context: fork` is set.                                                                                                                                                                                                                                                                                                                                                                                                  |
| `hooks`                    | No          | Hooks scoped to this skill's lifecycle. See [Hooks in skills and agents](/docs/en/hooks#hooks-in-skills-and-agents) for configuration format.                                                                                                                                                                                                                                                                                                                 |
| `paths`                    | No          | Glob patterns that limit when this skill is activated. Accepts a comma-separated string or a YAML list. When set, Claude loads the skill automatically only when working with files matching the patterns. Uses the same format as [path-specific rules](/docs/en/memory#path-specific-rules).                                                                                                                                                                |
| `shell`                    | No          | Shell to use for `` !`command` `` and ` ```! ` blocks in this skill. Accepts `bash` (default) or `powershell`. Setting `powershell` runs inline shell commands via PowerShell when the [PowerShell tool](/en/tools-reference#powershell-tool) is enabled: it's on by default on Windows without Git Bash, and `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` enables it elsewhere.                                                                                  |

#### How a skill gets its command name

The command you type to invoke a skill comes from where the skill file lives. The frontmatter `name` field sets the display label shown in skill listings and, except for a plugin-root `SKILL.md`, does not change what you type after `/`.

The table below shows where the command name comes from for each layout:

| Skill location                                                                                     | Command name source                                                                | Example                                                                                                                              |
| :------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| Skill directory under `~/.claude/skills/` or `.claude/skills/`                                     | Directory name                                                                     | `.claude/skills/deploy-staging/SKILL.md` → `/deploy-staging`                                                                         |
| [Nested](#where-skills-live) `.claude/skills/` directory, when the name clashes with another skill | Subdirectory path relative to the working directory, then the skill directory name | `apps/web/.claude/skills/deploy/SKILL.md` → `/apps/web:deploy`                                                                       |
| File under `.claude/commands/`                                                                     | File name without extension                                                        | `.claude/commands/deploy.md` → `/deploy`                                                                                             |
| Plugin `skills/` subdirectory                                                                      | Directory name, namespaced by plugin                                               | `my-plugin/skills/review/SKILL.md` → `/my-plugin:review`                                                                             |
| Plugin root `SKILL.md`                                                                             | Frontmatter `name`, with the plugin directory name as a fallback                   | `my-plugin/SKILL.md` with `name: review` → `/my-plugin:review`. See [Path behavior rules](/docs/en/plugins-reference#path-behavior-rules) |

The plugin-root case is the one place where `name` does set the command name, because there is no skill directory to take it from. If `name` is not set in the frontmatter, the plugin's directory name is used instead.

#### Available string substitutions

Skills support string substitution for dynamic values in the skill content:

| Variable                | Description                                                                                                                                                                                                                                                                                                 |
| :---------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$ARGUMENTS`            | All arguments passed when invoking the skill. If `$ARGUMENTS` is not present in the content, arguments are appended as `ARGUMENTS: <value>`.                                                                                                                                                                |
| `$ARGUMENTS[N]`         | Access a specific argument by 0-based index, such as `$ARGUMENTS[0]` for the first argument.                                                                                                                                                                                                                |
| `$N`                    | Shorthand for `$ARGUMENTS[N]`, such as `$0` for the first argument or `$1` for the second.                                                                                                                                                                                                                  |
| `$name`                 | Named argument declared in the [`arguments`](#frontmatter-reference) frontmatter list. Names map to positions in order, so with `arguments: [issue, branch]` the placeholder `$issue` expands to the first argument and `$branch` to the second.                                                            |
| `${CLAUDE_SESSION_ID}`  | The current session ID. Useful for logging, creating session-specific files, or correlating skill output with sessions.                                                                                                                                                                                     |
| `${CLAUDE_EFFORT}`      | The current effort level: `low`, `medium`, `high`, `xhigh`, or `max`. Ultracode is not a distinct level and reports as `xhigh`. Use this to adapt skill instructions to the active effort setting.                                                                                                          |
| `${CLAUDE_SKILL_DIR}`   | The directory containing the skill's `SKILL.md` file. For plugin skills, this is the skill's subdirectory within the plugin, not the plugin root. Use this in bash injection commands to reference scripts or files bundled with the skill, regardless of the current working directory.                    |
| `${CLAUDE_PROJECT_DIR}` | The project root directory. This is the same path [hooks](/docs/en/hooks#reference-scripts-by-path) and MCP servers receive as `CLAUDE_PROJECT_DIR`. Use this to reference project-local scripts or files, such as `${CLAUDE_PROJECT_DIR}/.claude/hooks/helper.sh`, independent of where the skill is installed. |

Claude Code substitutes `${CLAUDE_SKILL_DIR}` and `${CLAUDE_PROJECT_DIR}` in two places: the skill's markdown content, and Bash rules in the [`allowed-tools`](#frontmatter-reference) frontmatter. Using the same variable in both places lets a skill run a bundled script without a permission prompt. The following skill shows the pattern:

```yaml theme={null}
---
name: render-chart
description: Render a chart from a CSV file
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *)
---

Run `${CLAUDE_SKILL_DIR}/scripts/render.sh <csv-file>` to render the chart.
```

If this skill is installed at `~/.claude/skills/render-chart/`, both occurrences of `${CLAUDE_SKILL_DIR}` expand to that directory. The `allowed-tools` rule then matches the exact command the skill body tells Claude to run, so the script runs without prompting.

The `allowed-tools` substitution for `${CLAUDE_SKILL_DIR}` requires Claude Code v2.1.129 or later. On earlier versions the rule stays a literal `${CLAUDE_SKILL_DIR}` string and never matches, so the command still prompts for permission.

The `${CLAUDE_PROJECT_DIR}` substitution requires Claude Code v2.1.196 or later.

Indexed arguments use shell-style quoting, so wrap multi-word values in quotes to pass them as a single argument. For example, `/my-skill "hello world" second` makes `$0` expand to `hello world` and `$1` to `second`. The `$ARGUMENTS` placeholder always expands to the full argument string as typed.

An indexed placeholder with no corresponding argument, such as `$2` when only one argument was passed, stays in the content unchanged. A named placeholder from the [`arguments`](#frontmatter-reference) frontmatter with no matching argument expands to an empty string.

To include a literal `$` before a digit, `ARGUMENTS`, or a declared argument name, such as `$1.00` in prose, escape it with a backslash: `\$1.00`. A backslash before any other `$` is left unchanged. Only a single backslash directly before the token escapes it. A doubled backslash such as `\\$1` leaves both backslashes in place, and `$1` still expands to the argument value.

**Example using substitutions:**

```yaml theme={null}
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

### Add supporting files

Skills can include multiple files in their directory. This keeps `SKILL.md` focused on the essentials while letting Claude access detailed reference material only when needed. Large reference docs, API specifications, or example collections don't need to load into context every time the skill runs.

```text theme={null}
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

Reference supporting files from `SKILL.md` so Claude knows what each file contains and when to load it:

```markdown theme={null}
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

<Tip>Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files.</Tip>

### Control who invokes a skill

By default, both you and Claude can invoke any skill. You can type `/skill-name` to invoke it directly, and Claude can load it automatically when relevant to your conversation. Two frontmatter fields let you restrict this:

* **`disable-model-invocation: true`**: Only you can invoke the skill. Use this for workflows with side effects or that you want to control timing, like `/commit`, `/deploy`, or `/send-slack-message`. You don't want Claude deciding to deploy because your code looks ready.

* **`user-invocable: false`**: Only Claude can invoke the skill. Use this for background knowledge that isn't actionable as a command. A `legacy-system-context` skill explains how an old system works. Claude should know this when relevant, but `/legacy-system-context` isn't a meaningful action for users to take.

This example creates a deploy skill that only you can trigger. If you set `disable-model-invocation: true`, Claude can't run the skill automatically:

```yaml theme={null}
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

Here's how the two fields affect invocation and context loading:

| Frontmatter                      | You can invoke | Claude can invoke | When loaded into context                                     |
| :------------------------------- | :------------- | :---------------- | :----------------------------------------------------------- |
| (default)                        | Yes            | Yes               | Description always in context, full skill loads when invoked |
| `disable-model-invocation: true` | Yes            | No                | Description not in context, full skill loads when you invoke |
| `user-invocable: false`          | No             | Yes               | Description always in context, full skill loads when invoked |

<Note>
  In a regular session, skill descriptions are loaded into context so Claude knows what's available, but full skill content only loads when invoked. [Subagents with preloaded skills](/docs/en/sub-agents#preload-skills-into-subagents) work differently: the full skill content is injected at startup.
</Note>

### Skill content lifecycle

When you or Claude invoke a skill, the rendered `SKILL.md` content enters the conversation as a single message and stays there for the rest of the session. This persistence applies to the skill's instructions, not its permissions: an [`allowed-tools`](#pre-approve-tools-for-a-skill) grant clears when you send your next message. Claude Code does not re-read the skill file on later turns, so write guidance that should apply throughout a task as standing instructions rather than one-time steps.

When Claude re-invokes a skill whose rendered content is identical to the copy already in context, Claude Code adds a short note that the skill is already loaded rather than a second copy of the content. When the rendered content differs, because the arguments changed or a [dynamic context](#inject-dynamic-context) command produced new output, Claude Code appends the full content again. Before v2.1.202, every re-invocation appended another full copy of the skill's instructions.

[Auto-compaction](/docs/en/how-claude-code-works#when-context-fills-up) carries invoked skills forward within a token budget. When the conversation is summarized to free context, Claude Code re-attaches the most recent invocation of each skill after the summary, keeping the first 5,000 tokens of each. Re-attached skills share a combined budget of 25,000 tokens. Claude Code fills this budget starting from the most recently invoked skill, so older skills can be dropped entirely after compaction if you have invoked many in one session.

If a skill seems to stop influencing behavior after the first response, the content is usually still present and the model is choosing other tools or approaches. Strengthen the skill's `description` and instructions so the model keeps preferring it, or use [hooks](/docs/en/hooks) to enforce behavior deterministically. If the skill is large or you invoked several others after it, re-invoke it after compaction to restore the full content.

### Pre-approve tools for a skill

The `allowed-tools` field grants permission for the listed tools during the turn that invokes the skill, so Claude can use them without prompting you for approval. The grant clears when you send your next message, even though the skill content [stays in context](#skill-content-lifecycle); invoking the skill again re-applies it for that turn. It does not restrict which tools are available: every tool remains callable, and your [permission settings](/docs/en/permissions) still govern tools that are not listed. To pre-approve tools for the whole session rather than a single turn, add allow rules to those permission settings instead.

For skills checked into a project's `.claude/skills/` directory, `allowed-tools` takes effect after you accept the workspace trust dialog for that folder, the same as permission rules in `.claude/settings.json`. Review project skills before trusting a repository, since a skill can grant itself broad tool access.

This skill lets Claude run git commands without per-use approval whenever you invoke it:

```yaml theme={null}
---
name: commit
description: Stage and commit the current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

To remove tools from Claude's available pool while a skill is active, list them in `disallowed-tools` in the skill's frontmatter. The restriction clears when you send your next message. Like deny rules, the field can't remove [`EndConversation`](/docs/en/tools-reference#endconversation-tool-behavior) while any other tool remains. To block tools across all skills and prompts, add deny rules in your [permission settings](/docs/en/permissions).

### Pass arguments to skills

Both you and Claude can pass arguments when invoking a skill. Arguments are available via the `$ARGUMENTS` placeholder.

This skill fixes a GitHub issue by number. The `$ARGUMENTS` placeholder gets replaced with whatever follows the skill name:

```yaml theme={null}
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

When you run `/fix-issue 123`, Claude receives "Fix GitHub issue 123 following our coding standards..."

If you invoke a skill with arguments but the skill doesn't include `$ARGUMENTS`, Claude Code appends `ARGUMENTS: <your input>` to the end of the skill content so Claude still sees what you typed.

You can also stack several skills at the start of one message. {/* min-version: 2.1.199 */}As of v2.1.199, typing `/code-review /fix-issue 123` loads both skills and passes the trailing text `123` as `$ARGUMENTS` to each of them. In earlier versions, only the first skill loaded and received `/fix-issue 123` as literal argument text.

Claude Code expands the first skill plus up to five more stacked after it. Expansion stops at the first token that isn't an inline user-invocable skill, so a skill that runs as a [forked subagent](#run-skills-in-a-subagent) or one whose arguments may themselves start with a slash command, such as `/loop`, also ends the run there; that token and everything after it become the argument text for every expanded skill.

To access individual arguments by position, use `$ARGUMENTS[N]` or the shorter `$N`:

```yaml theme={null}
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $ARGUMENTS[0] component from $ARGUMENTS[1] to $ARGUMENTS[2].
Preserve all existing behavior and tests.
```

Running `/migrate-component SearchBar React Vue` replaces `$ARGUMENTS[0]` with `SearchBar`, `$ARGUMENTS[1]` with `React`, and `$ARGUMENTS[2]` with `Vue`. The same skill using the `$N` shorthand:

```yaml theme={null}
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

## Advanced patterns

### Inject dynamic context

The `` !`<command>` `` syntax runs shell commands before the skill content is sent to Claude. The command output replaces the placeholder, so Claude receives actual data, not the command itself.

This skill summarizes a pull request by fetching live PR data with the GitHub CLI. The `` !`gh pr diff` `` and other commands run first, and their output gets inserted into the prompt:

```yaml theme={null}
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

When this skill runs:

1. Each `` !`<command>` `` executes immediately (before Claude sees anything)
2. The output replaces the placeholder in the skill content
3. Claude receives the fully-rendered prompt with actual PR data

This is preprocessing, not something Claude executes. Claude only sees the final result.

Substitution runs once over the original file. Command output is inserted as plain text and is not re-scanned for further `` !`<command>` `` placeholders, so a command cannot emit a placeholder for a later pass to expand.

The inline form is only recognized when `!` appears at the start of a line or immediately after whitespace. If `!` follows another character, as in `` KEY=!`cmd` ``, the placeholder is left as literal text and the command does not run.

For multi-line commands, use a fenced code block opened with ` ```! ` instead of the inline form:

````markdown theme={null}
## Environment
```!
node --version
npm --version
git status --short
```
````

To disable this behavior for skills and custom commands from user, project, plugin, or [additional-directory](#skills-from-additional-directories) sources, set `"disableSkillShellExecution": true` in [settings](/docs/en/settings). Each command is replaced with `[shell command execution disabled by policy]` instead of being run. Bundled and managed skills are not affected. This setting is most useful in [managed settings](/docs/en/permissions#managed-settings), where users cannot override it.

<Tip>
  To request deeper reasoning when a skill runs, include `ultrathink` anywhere in the skill content. See [Use ultrathink for one-off deep reasoning](/docs/en/model-config#use-ultrathink-for-one-off-deep-reasoning).
</Tip>

### Run skills in a subagent

Add `context: fork` to your frontmatter when you want a skill to run in isolation. The skill content becomes the prompt that drives the subagent. It won't have access to your conversation history.

<Warning>
  `context: fork` only makes sense for skills with explicit instructions. If your skill contains guidelines like "use these API conventions" without a task, the subagent receives the guidelines but no actionable prompt, and returns without meaningful output.
</Warning>

Skills and [subagents](/docs/en/sub-agents) work together in two directions:

| Approach                     | System prompt            | Task                        | Also loads                                          |
| :--------------------------- | :----------------------- | :-------------------------- | :-------------------------------------------------- |
| Skill with `context: fork`   | From agent type          | SKILL.md content            | CLAUDE.md, except when the agent is Explore or Plan |
| Subagent with `skills` field | Subagent's markdown body | Claude's delegation message | Preloaded skills + CLAUDE.md                        |

With `context: fork`, you write the task in your skill and pick an agent type to execute it. The built-in Explore and Plan agents [skip CLAUDE.md and git status](/docs/en/sub-agents#what-loads-at-startup) to keep their context small, so a forked skill using `agent: Explore` sees only the SKILL.md content and the agent's own system prompt. For the inverse, where you define a custom subagent that uses skills as reference material, see [Subagents](/docs/en/sub-agents#preload-skills-into-subagents).

#### Example: Research skill using Explore agent

This skill runs research in a forked Explore agent. The skill content becomes the task, and the agent provides read-only tools optimized for codebase exploration:

```yaml theme={null}
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

When this skill runs:

1. A new isolated context is created
2. The subagent receives the skill content as its prompt ("Research \$ARGUMENTS thoroughly...")
3. The `agent` field determines the execution environment (model, tools, and permissions)
4. Results are summarized and returned to your main conversation

The `agent` field specifies which subagent configuration to use. Options include built-in agents (`Explore`, `Plan`, `general-purpose`) or any custom subagent from `.claude/agents/`. If omitted, uses `general-purpose`.

### Restrict Claude's skill access

By default, Claude can invoke any skill that doesn't have `disable-model-invocation: true` set. Skills that define `allowed-tools` grant Claude access to those tools without per-use approval during the turn that invokes the skill; the grant clears when you send your next message. Your [permission settings](/docs/en/permissions) still govern baseline approval behavior for all other tools. A few built-in commands are also available through the Skill tool, including `/init`, `/review`, and `/security-review`. Other built-in commands such as `/compact` are not.

Three ways to control which skills Claude can invoke:

**Disable all skills** by denying the Skill tool in `/permissions`:

```text theme={null}
# Add to deny rules:
Skill
```

**Allow or deny specific skills** using [permission rules](/docs/en/permissions):

```text theme={null}
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

Permission syntax: `Skill(name)` for exact match, `Skill(name *)` for prefix match with any arguments.

**Hide individual skills** by adding `disable-model-invocation: true` to their frontmatter. This removes the skill from Claude's context entirely.

<Note>
  The `user-invocable` field only controls menu visibility, not Skill tool access. Use `disable-model-invocation: true` to block programmatic invocation.
</Note>

### Override skill visibility from settings

The `skillOverrides` setting controls skill visibility from your [settings](/docs/en/settings) instead of the skill's own frontmatter. Use it for skills whose SKILL.md you don't want to edit, such as ones checked into a shared project repo. The `/skills` menu writes it for you: highlight a skill and press `Space` to cycle states, then `Enter` to save to `.claude/settings.local.json`.

Each key is a skill name and each value is one of four states:

| Value                   | Listed to Claude     | In `/` menu |
| :---------------------- | :------------------- | :---------- |
| `"on"`                  | Name and description | Yes         |
| `"name-only"`           | Name only            | Yes         |
| `"user-invocable-only"` | Hidden               | Yes         |
| `"off"`                 | Hidden               | Hidden      |

The `/skills` menu labels the `"user-invocable-only"` state `user-only`.

As of v2.1.199, `"off"` also hides the skill from the command lists advertised to [Remote Control](/docs/en/remote-control) clients and to [Agent SDK](/docs/en/agent-sdk/slash-commands) callers, not only the terminal `/` menu. Invoking a hidden skill by its full name still returns the `skillOverrides` error instead of running it.

A skill that is absent from `skillOverrides` is treated as `"on"`. The example below collapses one skill to its name and turns another off entirely:

```json theme={null}
{
  "skillOverrides": {
    "legacy-context": "name-only",
    "deploy": "off"
  }
}
```

Plugin skills are not affected by `skillOverrides`. Manage those through `/plugin` instead.

## Evaluate and iterate on a skill

Seeing a skill trigger tells you Claude found it, not that it did what you intended. To know a skill is working, measure two things separately: whether Claude invokes it on the prompts it should, and whether the output matches what you expect when it does.

The check for both is a baseline comparison. Collect a few realistic prompts, run each one in a fresh session with the skill available and again with it [disabled](#override-skill-visibility-from-settings), and compare the results. A fresh session matters because leftover context from authoring the skill will mask gaps in the written instructions.

### Run evals with skill-creator

The [`skill-creator` plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator) automates the comparison loop inside Claude Code. Install it from the official marketplace:

```text theme={null}
/plugin install skill-creator@claude-plugins-official
```

If Claude Code reports `Marketplace "claude-plugins-official" not found`, add the marketplace with `/plugin marketplace add anthropics/claude-plugins-official`. If it reports that the plugin is not found in the marketplace, your local copy is outdated: refresh it with `/plugin marketplace update claude-plugins-official`. Then retry the install.

After installing, run `/reload-plugins` to make the plugin's skills available in the current session. Then ask Claude to evaluate an existing skill, for example `evaluate my summarize-changes skill with skill-creator`. The plugin walks you through writing test cases and runs the loop:

* **Test cases**: stores prompts, input files, and expected behavior in `evals/evals.json` inside the skill directory
* **Isolated runs**: spawns a [subagent](/docs/en/sub-agents) per test case so each run starts with a clean context, and records token count and duration
* **Grading**: checks each assertion against the output and writes pass or fail with evidence to `grading.json`
* **Benchmark**: aggregates pass rate, time, and tokens for with-skill versus without-skill into `benchmark.json` so you can compare the pass-rate improvement against the token and time overhead
* **Version comparison**: runs a blind A/B between two versions of the skill so you can confirm an edit is an improvement before committing it
* **Description tuning**: generates should-trigger and should-not-trigger prompts, measures the hit rate, and proposes description edits when the skill activates on the wrong requests
* **Review viewer**: opens an HTML report where you inspect each output and record qualitative feedback that the next iteration reads

For the eval file format and the full iteration workflow, see [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills) on agentskills.io. For background on the benchmark and comparison modes, see the [skill-creator announcement](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills).

## Share skills

Skills can be distributed at different scopes depending on your audience:

* **Project skills**: Commit `.claude/skills/` to version control
* **Plugins**: Create a `skills/` directory in your [plugin](/docs/en/plugins)
* **Managed**: Deploy organization-wide through [managed settings](/docs/en/settings#settings-files)

### Generate visual output

Skills can bundle and run scripts in any language, giving Claude capabilities beyond what's possible in a single prompt. One powerful pattern is generating visual output: interactive HTML files that open in your browser for exploring data, debugging, or creating reports.

This example creates a codebase explorer: an interactive tree view where you can expand and collapse directories, see file sizes at a glance, and identify file types by color.

Create the Skill directory:

```bash theme={null}
mkdir -p ~/.claude/skills/codebase-visualizer/scripts
```

Save this to `~/.claude/skills/codebase-visualizer/SKILL.md`. The description tells Claude when to activate this Skill, and the instructions tell Claude to run the bundled script. The script path uses [`${CLAUDE_SKILL_DIR}`](#available-string-substitutions) so it resolves correctly whether the skill is installed at the personal, project, or plugin level:

````yaml theme={null}
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase. Use when exploring a new repo, understanding project structure, or identifying large files.
allowed-tools: Bash(python3 *)
---

# Codebase Visualizer

Generate an interactive HTML tree view that shows your project's file structure with collapsible directories.

## Usage

Run the visualization script from your project root:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/visualize.py .
```

This creates `codebase-map.html` in the current directory and opens it in your default browser.

## What the visualization shows

- **Collapsible directories**: Click folders to expand/collapse
- **File sizes**: Displayed next to each file
- **Colors**: Different colors for different file types
- **Directory totals**: Shows aggregate size of each folder
````

Save this to `~/.claude/skills/codebase-visualizer/scripts/visualize.py`. This script scans a directory tree and generates a self-contained HTML file with:

* A **summary sidebar** showing file count, directory count, total size, and number of file types
* A **bar chart** breaking down the codebase by file type (top 8 by size)
* A **collapsible tree** where you can expand and collapse directories, with color-coded file type indicators

The script requires Python 3 but uses only built-in libraries, so there are no packages to install:

```python expandable theme={null}
#!/usr/bin/env python3
"""Generate an interactive collapsible tree visualization of a codebase."""

import json
import sys
import webbrowser
from html import escape
from pathlib import Path
from collections import Counter

IGNORE = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}

def scan(path: Path, stats: dict) -> dict:
    result = {"name": path.name, "children": [], "size": 0}
    try:
        for item in sorted(path.iterdir()):
            if item.name in IGNORE or item.name.startswith('.'):
                continue
            if item.is_file():
                size = item.stat().st_size
                ext = item.suffix.lower() or '(no ext)'
                result["children"].append({"name": item.name, "size": size, "ext": ext})
                result["size"] += size
                stats["files"] += 1
                stats["extensions"][ext] += 1
                stats["ext_sizes"][ext] += size
            elif item.is_dir():
                stats["dirs"] += 1
                child = scan(item, stats)
                if child["children"]:
                    result["children"].append(child)
                    result["size"] += child["size"]
    except PermissionError:
        pass
    return result

def generate_html(data: dict, stats: dict, output: Path) -> None:
    ext_sizes = stats["ext_sizes"]
    total_size = sum(ext_sizes.values()) or 1
    sorted_exts = sorted(ext_sizes.items(), key=lambda x: -x[1])[:8]
    colors = {
        '.js': '#f7df1e', '.ts': '#3178c6', '.py': '#3776ab', '.go': '#00add8',
        '.rs': '#dea584', '.rb': '#cc342d', '.css': '#264de4', '.html': '#e34c26',
        '.json': '#6b7280', '.md': '#083fa1', '.yaml': '#cb171e', '.yml': '#cb171e',
        '.mdx': '#083fa1', '.tsx': '#3178c6', '.jsx': '#61dafb', '.sh': '#4eaa25',
    }
    lang_bars = "".join(
        f'<div class="bar-row"><span class="bar-label">{ext}</span>'
        f'<div class="bar" style="width:{(size/total_size)*100}%;background:{colors.get(ext,"#6b7280")}"></div>'
        f'<span class="bar-pct">{(size/total_size)*100:.1f}%</span></div>'
        for ext, size in sorted_exts
    )
    def fmt(b):
        if b < 1024: return f"{b} B"
        if b < 1048576: return f"{b/1024:.1f} KB"
        return f"{b/1048576:.1f} MB"

    html = f'''<!DOCTYPE html>
<html><head>
  <meta charset="utf-8"><title>Codebase Explorer</title>
  <style>
    body {{ font: 14px/1.5 system-ui, sans-serif; margin: 0; background: #1a1a2e; color: #eee; }}
    .container {{ display: flex; height: 100vh; }}
    .sidebar {{ width: 280px; background: #252542; padding: 20px; border-right: 1px solid #3d3d5c; overflow-y: auto; flex-shrink: 0; }}
    .main {{ flex: 1; padding: 20px; overflow-y: auto; }}
    h1 {{ margin: 0 0 10px 0; font-size: 18px; }}
    h2 {{ margin: 20px 0 10px 0; font-size: 14px; color: #888; text-transform: uppercase; }}
    .stat {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #3d3d5c; }}
    .stat-value {{ font-weight: bold; }}
    .bar-row {{ display: flex; align-items: center; margin: 6px 0; }}
    .bar-label {{ width: 55px; font-size: 12px; color: #aaa; }}
    .bar {{ height: 18px; border-radius: 3px; }}
    .bar-pct {{ margin-left: 8px; font-size: 12px; color: #666; }}
    .tree {{ list-style: none; padding-left: 20px; }}
    details {{ cursor: pointer; }}
    summary {{ padding: 4px 8px; border-radius: 4px; }}
    summary:hover {{ background: #2d2d44; }}
    .folder {{ color: #ffd700; }}
    .file {{ display: flex; align-items: center; padding: 4px 8px; border-radius: 4px; }}
    .file:hover {{ background: #2d2d44; }}
    .size {{ color: #888; margin-left: auto; font-size: 12px; }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }}
  </style>
</head><body>
  <div class="container">
    <div class="sidebar">
      <h1>📊 Summary</h1>
      <div class="stat"><span>Files</span><span class="stat-value">{stats["files"]:,}</span></div>
      <div class="stat"><span>Directories</span><span class="stat-value">{stats["dirs"]:,}</span></div>
      <div class="stat"><span>Total size</span><span class="stat-value">{fmt(data["size"])}</span></div>
      <div class="stat"><span>File types</span><span class="stat-value">{len(stats["extensions"])}</span></div>
      <h2>By file type</h2>
      {lang_bars}
    </div>
    <div class="main">
      <h1>📁 {escape(data["name"])}</h1>
      <ul class="tree" id="root"></ul>
    </div>
  </div>
  <script>
    const data = {json.dumps(data)};
    const colors = {json.dumps(colors)};
    function fmt(b) {{ if (b < 1024) return b + ' B'; if (b < 1048576) return (b/1024).toFixed(1) + ' KB'; return (b/1048576).toFixed(1) + ' MB'; }}
    function esc(s) {{ return s.replace(/[&<>"']/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[c])); }}
    function render(node, parent) {{
      if (node.children) {{
        const det = document.createElement('details');
        det.open = parent === document.getElementById('root');
        det.innerHTML = `<summary><span class="folder">📁 ${{esc(node.name)}}</span><span class="size">${{fmt(node.size)}}</span></summary>`;
        const ul = document.createElement('ul'); ul.className = 'tree';
        node.children.sort((a,b) => (b.children?1:0)-(a.children?1:0) || a.name.localeCompare(b.name));
        node.children.forEach(c => render(c, ul));
        det.appendChild(ul);
        const li = document.createElement('li'); li.appendChild(det); parent.appendChild(li);
      }} else {{
        const li = document.createElement('li'); li.className = 'file';
        li.innerHTML = `<span class="dot" style="background:${{colors[node.ext]||'#6b7280'}}"></span>${{esc(node.name)}}<span class="size">${{fmt(node.size)}}</span>`;
        parent.appendChild(li);
      }}
    }}
    data.children.forEach(c => render(c, document.getElementById('root')));
  </script>
</body></html>'''
    output.write_text(html)

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    stats = {"files": 0, "dirs": 0, "extensions": Counter(), "ext_sizes": Counter()}
    data = scan(target, stats)
    out = Path('codebase-map.html')
    generate_html(data, stats, out)
    print(f'Generated {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')
```

To test, open Claude Code in any project and ask "Visualize this codebase." Claude runs the script, which prints the generated file's path, such as `Generated /path/to/codebase-map.html`, and opens it in your browser. If you work in a headless environment where no browser opens, the printed path confirms the script succeeded.

This pattern works for any visual output: dependency graphs, test coverage reports, API documentation, or database schema visualizations. The bundled script does the work while Claude handles orchestration.

## Troubleshooting

### Skill not triggering

If Claude doesn't use your skill when expected:

1. Check the description includes keywords users would naturally say
2. Verify the skill appears in `What skills are available?`
3. Try rephrasing your request to match the description more closely
4. Invoke it directly with `/skill-name` if the skill is user-invocable

If the frontmatter YAML is malformed, Claude Code loads the skill body with empty metadata, so `/skill-name` still works but Claude has no `description` to match against. Run with `--debug` to see the parse error.

### Skill triggers too often

If Claude uses your skill when you don't want it:

1. Make the description more specific
2. Add `disable-model-invocation: true` if you only want manual invocation

### Skill descriptions are cut short

Claude Code loads a listing of skill names and descriptions into context so Claude knows what's available. The listing always contains every skill name, but if you have many skills, Claude Code shortens descriptions to fit the listing's character budget, which can strip the keywords Claude needs to match your request. The budget scales at 1% of the model's context window. When the listing overflows, Claude Code drops descriptions starting with the skills you invoke least, so the skills you use most keep their full text.

Run `/doctor` for an estimate of the listing's context cost and its biggest contributors. When the listing exceeds its budget, Claude Code also writes a warning to the debug log, visible with [`--debug`](/docs/en/cli-reference#cli-flags).

The Skills row in `/context` reports the size of the listing after the budget is applied, so it matches what the model receives. Before v2.1.196, the row counted the full text of every description and could show a value several times larger than the configured budget.

To raise the budget, set the [`skillListingBudgetFraction`](/docs/en/settings#available-settings) setting (e.g. `0.02` = 2%) or the `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable to a fixed character count. To free budget for other skills, set low-priority entries to `"name-only"` in [`skillOverrides`](#override-skill-visibility-from-settings) so they list without a description. You can also trim the `description` and `when_to_use` text at the source: put the key use case first, since each entry's combined text is capped at 1,536 characters regardless of budget. The cap is configurable with [`skillListingMaxDescChars`](/docs/en/settings#available-settings).

## Related resources

* **[Debug your configuration](/docs/en/debug-your-config)**: diagnose why a skill isn't appearing or triggering
* **[Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)**: the eval file format and iteration workflow on agentskills.io
* **[Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)**: writing guidance that applies across Claude products
* **[Subagents](/docs/en/sub-agents)**: delegate tasks to specialized agents
* **[Plugins](/docs/en/plugins)**: package and distribute skills with other extensions
* **[Hooks](/docs/en/hooks)**: automate workflows around tool events
* **[Memory](/docs/en/memory)**: manage CLAUDE.md files for persistent context
* **[Commands](/docs/en/commands)**: reference for built-in commands and bundled skills
* **[Permissions](/docs/en/permissions)**: control tool and skill access
* **[Claude Tag skills](https://claude.com/docs/claude-tag/admins/skills-repo)**: project skills committed to a repo also load when that repo is used in a Claude Tag channel
