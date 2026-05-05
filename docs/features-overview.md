> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Extend Claude Code

> Understand when to use CLAUDE.md, Skills, subagents, hooks, MCP, and plugins.

Claude Code combines a model that reasons about your code with [built-in tools](/en/how-claude-code-works#tools) for file operations, search, execution, and web access. The built-in tools cover most coding tasks. This guide covers the extension layer: features you add to customize what Claude knows, connect it to external services, and automate workflows.

<Note>
  For how the core agentic loop works, see [How Claude Code works](/en/how-claude-code-works).
</Note>

**New to Claude Code?** Start with [CLAUDE.md](/en/memory) for project conventions, then add other extensions [as specific triggers come up](#build-your-setup-over-time).

## Overview

Extensions plug into different parts of the agentic loop:

* **[CLAUDE.md](/en/memory)** adds persistent context Claude sees every session
* **[Skills](/en/skills)** add reusable knowledge and invocable workflows
* **[MCP](/en/mcp)** connects Claude to external services and tools
* **[Subagents](/en/sub-agents)** run their own loops in isolated context, returning summaries
* **[Agent teams](/en/agent-teams)** coordinate multiple independent sessions with shared tasks and peer-to-peer messaging
* **[Hooks](/en/hooks-guide)** fire on lifecycle events and can run a script, HTTP request, prompt, or subagent
* **[Plugins](/en/plugins)** and **[marketplaces](/en/plugin-marketplaces)** package and distribute these features

[Skills](/en/skills) are the most flexible extension. A skill is a markdown file containing knowledge, workflows, or instructions. You can invoke skills with a command like `/deploy`, or Claude can load them automatically when relevant. Skills can run in your current conversation or in an isolated context via subagents.

## Match features to your goal

Features range from always-on context that Claude sees every session, to on-demand capabilities you or Claude can invoke, to background automation that runs on specific events. The table below shows what's available and when each one makes sense.

| Feature                            | What it does                                                  | When to use it                                                                  | Example                                                                         |
| ---------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **CLAUDE.md**                      | Persistent context loaded every conversation                  | Project conventions, "always do X" rules                                        | "Use pnpm, not npm. Run tests before committing."                               |
| **Skill**                          | Instructions, knowledge, and workflows Claude can use         | Reusable content, reference docs, repeatable tasks                              | `/deploy` runs your deployment checklist; API docs skill with endpoint patterns |
| **Subagent**                       | Isolated execution context that returns summarized results    | Context isolation, parallel tasks, specialized workers                          | Research task that reads many files but returns only key findings               |
| **[Agent teams](/en/agent-teams)** | Coordinate multiple independent Claude Code sessions          | Parallel research, new feature development, debugging with competing hypotheses | Spawn reviewers to check security, performance, and tests simultaneously        |
| **MCP**                            | Connect to external services                                  | External data or actions                                                        | Query your database, post to Slack, control a browser                           |
| **Hook**                           | Script, HTTP request, prompt, or subagent triggered by events | Automation that must run on every matching event                                | Run ESLint after every file edit                                                |

**[Plugins](/en/plugins)** are the packaging layer. A plugin bundles skills, hooks, subagents, and MCP servers into a single installable unit. Plugin skills are namespaced (like `/my-plugin:review`) so multiple plugins can coexist. Use plugins when you want to reuse the same setup across multiple repositories or distribute to others via a **[marketplace](/en/plugin-marketplaces)**.

### Build your setup over time

You don't need to configure everything up front. Each feature has a recognizable trigger, and most teams add them in roughly this order:

| Trigger                                                                          | Add                                             |
| :------------------------------------------------------------------------------- | :---------------------------------------------- |
| Claude gets a convention or command wrong twice                                  | Add it to [CLAUDE.md](/en/memory)               |
| You keep typing the same prompt to start a task                                  | Save it as a user-invocable [skill](/en/skills) |
| You paste the same playbook or multi-step procedure into chat for the third time | Capture it as a [skill](/en/skills)             |
| You keep copying data from a browser tab Claude can't see                        | Connect that system as an [MCP server](/en/mcp) |
| A side task floods your conversation with output you won't reference again       | Route it through a [subagent](/en/sub-agents)   |
| You want something to happen every time without asking                           | Write a [hook](/en/hooks-guide)                 |
| A second repository needs the same setup                                         | Package it as a [plugin](/en/plugins)           |

The same triggers tell you when to update what you already have. A repeated mistake or a recurring review comment is a CLAUDE.md edit, not a one-off correction in chat. A workflow you keep tweaking by hand is a skill that needs another revision.

### Compare similar features

Some features can seem similar. Here's how to tell them apart.

<Tabs>
  <Tab title="Skill vs Subagent">
    Skills and subagents solve different problems:

    * **Skills** are reusable content you can load into any context
    * **Subagents** are isolated workers that run separately from your main conversation

    | Aspect                                          | Skill                                          | Subagent                                                         |
    | ----------------------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------- |
    | **What it is**                                  | Reusable instructions, knowledge, or workflows | Isolated worker with its own context                             |
    | **Key benefit**                                 | Share content across contexts                  | Context isolation. Work happens separately, only summary returns |
    | **[Context window](/en/context-window) impact** | Adds to your main window                       | Uses a separate window with its own input and output tokens      |
    | **Best for**                                    | Reference material, invocable workflows        | Tasks that read many files, parallel work, specialized workers   |

    **Skills can be reference or action.** Reference skills provide knowledge Claude uses throughout your session (like your API style guide). Action skills tell Claude to do something specific (like `/deploy` that runs your deployment workflow).

    **Use a subagent** when you need context isolation or when your context window is getting full. The subagent might read dozens of files or run extensive searches, but your main conversation only receives a summary. Since subagent work doesn't consume your main context, this is also useful when you don't need the intermediate work to remain visible. Custom subagents can have their own instructions and can preload skills.

    **They can combine.** A subagent can preload specific skills (`skills:` field). A skill can run in isolated context using `context: fork`. See [Skills](/en/skills) for details.
  </Tab>

  <Tab title="CLAUDE.md vs Skill">
    Both store instructions, but they load differently and serve different purposes.

    | Aspect                    | CLAUDE.md                    | Skill                                   |
    | ------------------------- | ---------------------------- | --------------------------------------- |
    | **Loads**                 | Every session, automatically | On demand                               |
    | **Can include files**     | Yes, with `@path` imports    | Yes, with `@path` imports               |
    | **Can trigger workflows** | No                           | Yes, with `/<name>`                     |
    | **Best for**              | "Always do X" rules          | Reference material, invocable workflows |

    **Put it in CLAUDE.md** if Claude should always know it: coding conventions, build commands, project structure, "never do X" rules.

    **Put it in a skill** if it's reference material Claude needs sometimes (API docs, style guides) or a workflow you trigger with `/<name>` (deploy, review, release).

    **Rule of thumb:** Keep CLAUDE.md under 200 lines. If it's growing, move reference content to skills or split into [`.claude/rules/`](/en/memory#organize-rules-with-claude/rules/) files.
  </Tab>

  <Tab title="CLAUDE.md vs Rules vs Skills">
    All three store instructions, but they load differently:

    | Aspect       | CLAUDE.md                           | `.claude/rules/`                                   | Skill                                    |
    | ------------ | ----------------------------------- | -------------------------------------------------- | ---------------------------------------- |
    | **Loads**    | Every session                       | Every session, or when matching files are opened   | On demand, when invoked or relevant      |
    | **Scope**    | Whole project                       | Can be scoped to file paths                        | Task-specific                            |
    | **Best for** | Core conventions and build commands | Language-specific or directory-specific guidelines | Reference material, repeatable workflows |

    **Use CLAUDE.md** for instructions every session needs: build commands, test conventions, project architecture.

    **Use rules** to keep CLAUDE.md focused. Rules with [`paths` frontmatter](/en/memory#path-specific-rules) only load when Claude works with matching files, saving context.

    **Use skills** for content Claude only needs sometimes, like API documentation or a deployment checklist you trigger with `/<name>`.
  </Tab>

  <Tab title="Subagent vs Agent team">
    Both parallelize work, but they're architecturally different:

    * **Subagents** run inside your session and report results back to your main context
    * **Agent teams** are independent Claude Code sessions that communicate with each other

    | Aspect            | Subagent                                         | Agent team                                          |
    | ----------------- | ------------------------------------------------ | --------------------------------------------------- |
    | **Context**       | Own context window; results return to the caller | Own context window; fully independent               |
    | **Communication** | Reports results back to the main agent only      | Teammates message each other directly               |
    | **Coordination**  | Main agent manages all work                      | Shared task list with self-coordination             |
    | **Best for**      | Focused tasks where only the result matters      | Complex work requiring discussion and collaboration |
    | **Token cost**    | Lower: results summarized back to main context   | Higher: each teammate is a separate Claude instance |

    **Use a subagent** when you need a quick, focused worker: research a question, verify a claim, review a file. The subagent does the work and returns a summary. Your main conversation stays clean.

    **Use an agent team** when teammates need to share findings, challenge each other, and coordinate independently. Agent teams are best for research with competing hypotheses, parallel code review, and new feature development where each teammate owns a separate piece.

    **Transition point:** If you're running parallel subagents but hitting context limits, or if your subagents need to communicate with each other, agent teams are the natural next step.

    <Note>
      Agent teams are experimental and disabled by default. See [agent teams](/en/agent-teams) for setup and current limitations.
    </Note>
  </Tab>

  <Tab title="MCP vs Skill">
    MCP connects Claude to external services. Skills extend what Claude knows, including how to use those services effectively.

    | Aspect         | MCP                                                  | Skill                                                   |
    | -------------- | ---------------------------------------------------- | ------------------------------------------------------- |
    | **What it is** | Protocol for connecting to external services         | Knowledge, workflows, and reference material            |
    | **Provides**   | Tools and data access                                | Knowledge, workflows, reference material                |
    | **Examples**   | Slack integration, database queries, browser control | Code review checklist, deploy workflow, API style guide |

    These solve different problems and work well together:

    **MCP** gives Claude the ability to interact with external systems. Without MCP, Claude can't query your database or post to Slack.

    **Skills** give Claude knowledge about how to use those tools effectively, plus workflows you can trigger with `/<name>`. A skill might include your team's database schema and query patterns, or a `/post-to-slack` workflow with your team's message formatting rules.

    Example: An MCP server connects Claude to your database. A skill teaches Claude your data model, common query patterns, and which tables to use for different tasks.
  </Tab>

  <Tab title="Hook vs Skill">
    A hook fires on a lifecycle event; a skill is loaded into context for Claude to apply.

    | Aspect           | Hook                                                                              | Skill                                                                 |
    | ---------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
    | **Runs**         | A shell command, HTTP request, LLM prompt, or subagent                            | Instructions Claude reads and follows                                 |
    | **Triggered by** | [Lifecycle events](/en/hooks#hook-events) such as `PostToolUse` or `SessionStart` | You typing `/<name>`, or Claude matching the description to your task |
    | **Determinism**  | Always fires on its event; the trigger is guaranteed                              | Claude interprets the instructions; outcome can vary                  |
    | **Context cost** | Zero unless the hook returns output                                               | Description loads each session; full content loads when used          |
    | **Best for**     | Linting after edits, blocking unsafe commands, logging, notifications             | Workflows that need reasoning, reference material, multi-step tasks   |

    **Use a hook** when the action must happen the same way every time and doesn't need Claude to think. For example: format on save, reject `rm -rf /`, post a Slack message when a session ends.

    **Use a skill** when Claude should decide how to apply the steps, or when the content is knowledge rather than a script. For example: a `/release` checklist, your API style guide, a debugging playbook.

    **Put guardrails in hooks.** An instruction like "never edit `.env`" in CLAUDE.md or a skill is a request, not a guarantee. A `PreToolUse` hook that blocks the edit is enforcement. If a rule must hold every time, make it a hook rather than a prompt instruction.

    **Hook output lands in context.** A `PostToolUse` hook that runs your linter feeds results back as text Claude reads; a `/fix-lint` skill tells Claude how to resolve them.
  </Tab>
</Tabs>

### Understand how features layer

Features can be defined at multiple levels: user-wide, per-project, via plugins, or through managed policies. You can also nest CLAUDE.md files in subdirectories or place skills in specific packages of a monorepo. When the same feature exists at multiple levels, here's how they layer:

* **CLAUDE.md files** are additive: all levels contribute content to Claude's context simultaneously. Files from your working directory and above load at launch; subdirectories load as you work in them. When instructions conflict, Claude uses judgment to reconcile them, with more specific instructions typically taking precedence. See [how CLAUDE.md files load](/en/memory#how-claude-md-files-load).
* **Skills and subagents** override by name: when the same name exists at multiple levels, one definition wins based on priority (managed > user > project for skills; managed > CLI flag > project > user > plugin for subagents). Plugin skills are [namespaced](/en/plugins#add-skills-to-your-plugin) to avoid conflicts. See [skill discovery](/en/skills#where-skills-live) and [subagent scope](/en/sub-agents#choose-the-subagent-scope).
* **MCP servers** override by name: local > project > user. See [MCP scope](/en/mcp#scope-hierarchy-and-precedence).
* **Hooks** merge: all registered hooks fire for their matching events regardless of source. See [hooks](/en/hooks).

### Combine features

Each extension solves a different problem: CLAUDE.md handles always-on context, skills handle on-demand knowledge and workflows, MCP handles external connections, subagents handle isolation, and hooks handle automation. Real setups combine them based on your workflow.

For example, you might use CLAUDE.md for project conventions, a skill for your deployment workflow, MCP to connect to your database, and a hook to run linting after every edit. Each feature handles what it's best at.

| Pattern                | How it works                                                                     | Example                                                                                           |
| ---------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Skill + MCP**        | MCP provides the connection; a skill teaches Claude how to use it well           | MCP connects to your database, a skill documents your schema and query patterns                   |
| **Skill + Subagent**   | A skill spawns subagents for parallel work                                       | `/audit` skill kicks off security, performance, and style subagents that work in isolated context |
| **CLAUDE.md + Skills** | CLAUDE.md holds always-on rules; skills hold reference material loaded on demand | CLAUDE.md says "follow our API conventions," a skill contains the full API style guide            |
| **Hook + MCP**         | A hook triggers external actions through MCP                                     | Post-edit hook sends a Slack notification when Claude modifies critical files                     |

## Understand context costs

Every feature you add consumes some of Claude's context. Too much can fill up your context window, but it can also add noise that makes Claude less effective; skills may not trigger correctly, or Claude may lose track of your conventions. Understanding these trade-offs helps you build an effective setup. For an interactive view of how these features combine in a running session, see [Explore the context window](/en/context-window).

### Context cost by feature

Each feature has a different loading strategy and context cost:

| Feature         | When it loads             | What loads                                    | Context cost                                 |
| --------------- | ------------------------- | --------------------------------------------- | -------------------------------------------- |
| **CLAUDE.md**   | Session start             | Full content                                  | Every request                                |
| **Skills**      | Session start + when used | Descriptions at start, full content when used | Low (descriptions every request)\*           |
| **MCP servers** | Session start             | Tool names; full schemas on demand            | Low until a tool is used                     |
| **Subagents**   | When spawned              | Fresh context with specified skills           | Isolated from main session                   |
| **Hooks**       | On trigger                | Nothing (runs externally)                     | Zero, unless hook returns additional context |

\*By default, skill descriptions load at session start so Claude can decide when to use them. Set `disable-model-invocation: true` in a skill's frontmatter to hide it from Claude entirely until you invoke it manually. This reduces context cost to zero for skills you only trigger yourself.

### Understand how features load

Each feature loads at different points in your session. The tabs below explain when each one loads and what goes into context.

<img src="https://mintcdn.com/claude-code/6yTCYq1p37ZB8-CQ/images/context-loading.svg?fit=max&auto=format&n=6yTCYq1p37ZB8-CQ&q=85&s=5a58ce953a35a2412892015e2ad6cb67" alt="Context loading: CLAUDE.md loads at session start and stays in every request. MCP tool names load at start with full schemas deferred until use. Skills load descriptions at start, full content on invocation. Subagents get isolated context. Hooks run externally." width="720" height="410" data-path="images/context-loading.svg" />

<Tabs>
  <Tab title="CLAUDE.md">
    **When:** Session start

    **What loads:** Full content of all CLAUDE.md files (managed, user, and project levels).

    **Inheritance:** Claude reads CLAUDE.md files from your working directory up to the root, and discovers nested ones in subdirectories as it accesses those files. See [How CLAUDE.md files load](/en/memory#how-claude-md-files-load) for details.

    <Tip>Keep CLAUDE.md under 200 lines. Move reference material to skills, which load on-demand.</Tip>
  </Tab>

  <Tab title="Skills">
    Skills are extra capabilities in Claude's toolkit. They can be reference material (like an API style guide) or invocable workflows you trigger with `/<name>` (like `/deploy`). Claude Code includes [bundled skills](/en/commands) like `/simplify`, `/batch`, and `/debug` that work out of the box. You can also create your own. Claude uses skills when appropriate, or you can invoke one directly.

    **When:** Depends on the skill's configuration. By default, descriptions load at session start and full content loads when used. For user-only skills (`disable-model-invocation: true`), nothing loads until you invoke them.

    **What loads:** For model-invocable skills, Claude sees names and descriptions in every request. When you invoke a skill with `/<name>` or Claude loads it automatically, the full content loads into your conversation.

    **How Claude chooses skills:** Claude matches your task against skill descriptions to decide which are relevant. If descriptions are vague or overlap, Claude may load the wrong skill or miss one that would help. To tell Claude to use a specific skill, invoke it with `/<name>`. Skills with `disable-model-invocation: true` are invisible to Claude until you invoke them.

    **Context cost:** Low until used. User-only skills have zero cost until invoked.

    **In subagents:** Skills work differently in subagents. Instead of on-demand loading, skills passed to a subagent are fully preloaded into its context at launch. Subagents don't inherit skills from the main session; you must specify them explicitly.

    <Tip>Use `disable-model-invocation: true` for skills with side effects. This saves context and ensures only you trigger them.</Tip>
  </Tab>

  <Tab title="MCP servers">
    **When:** Session start.

    **What loads:** Tool names from connected servers. Full JSON schemas stay deferred until Claude needs a specific tool.

    **Context cost:** [Tool search](/en/mcp#scale-with-mcp-tool-search) is on by default, so idle MCP tools consume minimal context.

    **Reliability note:** MCP connections can fail silently mid-session. If a server disconnects, its tools disappear without warning. Claude may try to use a tool that no longer exists. If you notice Claude failing to use an MCP tool it previously could access, check the connection with `/mcp`.

    <Tip>Run `/mcp` to see token costs per server. Disconnect servers you're not actively using.</Tip>
  </Tab>

  <Tab title="Subagents">
    **When:** On demand, when you or Claude spawns one for a task.

    **What loads:** Fresh, isolated context containing:

    * The system prompt (shared with parent for cache efficiency)
    * Full content of skills listed in the agent's `skills:` field
    * CLAUDE.md and git status (inherited from parent)
    * Whatever context the lead agent passes in the prompt

    **Context cost:** Isolated from main session. Subagents don't inherit your conversation history or invoked skills.

    <Tip>Use subagents for work that doesn't need your full conversation context. Their isolation prevents bloating your main session.</Tip>
  </Tab>

  <Tab title="Hooks">
    **When:** On trigger. Hooks fire at specific lifecycle events like tool execution, session boundaries, prompt submission, permission requests, and compaction. See [Hooks](/en/hooks) for the full list.

    **What loads:** Nothing by default. Hooks execute outside the main conversation.

    **Context cost:** Zero, unless the hook returns output that gets added as messages to your conversation.

    <Tip>Hooks are ideal for side effects (linting, logging) that don't need to affect Claude's context.</Tip>
  </Tab>
</Tabs>

## Learn more

Each feature has its own guide with setup instructions, examples, and configuration options.

<CardGroup cols={2}>
  <Card title="CLAUDE.md" icon="file-lines" href="/en/memory">
    Store project context, conventions, and instructions
  </Card>

  <Card title="Skills" icon="brain" href="/en/skills">
    Give Claude domain expertise and reusable workflows
  </Card>

  <Card title="Subagents" icon="users" href="/en/sub-agents">
    Offload work to isolated context
  </Card>

  <Card title="Agent teams" icon="network" href="/en/agent-teams">
    Coordinate multiple sessions working in parallel
  </Card>

  <Card title="MCP" icon="plug" href="/en/mcp">
    Connect Claude to external services
  </Card>

  <Card title="Hooks" icon="bolt" href="/en/hooks-guide">
    Automate workflows with hooks
  </Card>

  <Card title="Plugins" icon="puzzle-piece" href="/en/plugins">
    Bundle and share feature sets
  </Card>

  <Card title="Marketplaces" icon="store" href="/en/plugin-marketplaces">
    Host and distribute plugin collections
  </Card>
</CardGroup>
