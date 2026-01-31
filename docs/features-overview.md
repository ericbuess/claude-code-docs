> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Extend Claude Code

> Understand when to use CLAUDE.md, Skills, subagents, hooks, MCP, and plugins.

Claude Code combines a model that reasons about your code with [built-in tools](/en/how-claude-code-works#tools) for file operations, search, execution, and web access. The built-in tools cover most coding tasks. This guide covers the extension layer: features you add to customize what Claude knows, connect it to external services, and automate workflows.

<Note>
  For how the core agentic loop works, see [How Claude Code works](/en/how-claude-code-works).
</Note>

**New to Claude Code?** Start with [CLAUDE.md](/en/memory) for project conventions. Add other extensions as you need them.

## Overview

Extensions plug into different parts of the agentic loop:

* **[CLAUDE.md](/en/memory)** adds persistent context Claude sees every session
* **[Skills](/en/skills)** add reusable knowledge and invocable workflows
* **[MCP](/en/mcp)** connects Claude to external services and tools
* **[Subagents](/en/sub-agents)** run their own loops in isolated context, returning summaries
* **[Hooks](/en/hooks)** run outside the loop entirely as deterministic scripts
* **[Plugins](/en/plugins)** and **[marketplaces](/en/plugin-marketplaces)** package and distribute these features

[Skills](/en/skills) are the most flexible extension. A skill is a markdown file containing knowledge, workflows, or instructions. You can invoke skills with a slash command like `/deploy`, or Claude can load them automatically when relevant. Skills can run in your current conversation or in an isolated context via subagents.

## Match features to your goal

Features range from always-on context that Claude sees every session, to on-demand capabilities you or Claude can invoke, to background automation that runs on specific events. The table below shows what's available and when each one makes sense.

| Feature       | What it does                                               | When to use it                                         | Example                                                                          |
| ------------- | ---------------------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------- |
| **CLAUDE.md** | Persistent context loaded every conversation               | Project conventions, "always do X" rules               | "Use pnpm, not npm. Run tests before committing."                                |
| **Skill**     | Instructions, knowledge, and workflows Claude can use      | Reusable content, reference docs, repeatable tasks     | `/review` runs your code review checklist; API docs skill with endpoint patterns |
| **Subagent**  | Isolated execution context that returns summarized results | Context isolation, parallel tasks, specialized workers | Research task that reads many files but returns only key findings                |
| **MCP**       | Connect to external services                               | External data or actions                               | Query your database, post to Slack, control a browser                            |
| **Hook**      | Deterministic script that runs on events                   | Predictable automation, no LLM involved                | Run ESLint after every file edit                                                 |

**[Plugins](/en/plugins)** are the packaging layer. A plugin bundles skills, hooks, subagents, and MCP servers into a single installable unit. Plugin skills are namespaced (like `/my-plugin:review`) so multiple plugins can coexist. Use plugins when you want to reuse the same setup across multiple repositories or distribute to others via a **[marketplace](/en/plugin-marketplaces)**.

### Compare similar features

Some features can seem similar. Here's how to tell them apart.

<Tabs>
  <Tab title="Skill vs Subagent">
    Skills and subagents solve different problems:

    * **Skills** are reusable content you can load into any context
    * **Subagents** are isolated workers that run separately from your main conversation

    | Aspect          | Skill                                          | Subagent                                                         |
    | --------------- | ---------------------------------------------- | ---------------------------------------------------------------- |
    | **What it is**  | Reusable instructions, knowledge, or workflows | Isolated worker with its own context                             |
    | **Key benefit** | Share content across contexts                  | Context isolation. Work happens separately, only summary returns |
    | **Best for**    | Reference material, invocable workflows        | Tasks that read many files, parallel work, specialized workers   |

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

    **Rule of thumb:** Keep CLAUDE.md under \~500 lines. If it's growing, move reference content to skills.
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
</Tabs>

### Understand how features layer

Features can be defined at multiple levels: user-wide, per-project, via plugins, or through managed policies. You can also nest CLAUDE.md files in subdirectories or place skills in specific packages of a monorepo. When the same feature exists at multiple levels, here's how they layer:

* **CLAUDE.md files** are additive: all levels contribute content to Claude's context simultaneously. Files from your working directory and above load at launch; subdirectories load as you work in them. When instructions conflict, Claude uses judgment to reconcile them, with more specific instructions typically taking precedence. See [how Claude looks up memories](/en/memory#how-claude-looks-up-memories).
* **Skills and subagents** override by name: when the same name exists at multiple levels, one definition wins based on priority (managed > user > project for skills; managed > CLI flag > project > user > plugin for subagents). Plugin skills are [namespaced](/en/plugins#add-skills-to-your-plugin) to avoid conflicts. See [skill discovery](/en/skills#where-skills-live) and [subagent scope](/en/sub-agents#choose-the-subagent-scope).
* **MCP servers** override by name: local > project > user. See [MCP scope](/en/mcp#scope-hierarchy-and-precedence).
* **Hooks** merge: all registered hooks fire for their matching events regardless of source. See [hooks](/en/hooks).

### Combine features

Each extension solves a different problem: CLAUDE.md handles always-on context, skills handle on-demand knowledge and workflows, MCP handles external connections, subagents handle isolation, and hooks handle automation. Real setups combine them based on your workflow.

For example, you might use CLAUDE.md for project conventions, a skill for your deployment workflow, MCP to connect to your database, and a hook to run linting after every edit. Each feature handles what it's best at.

| Pattern                | How it works                                                                     | Example                                                                                            |
| ---------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Skill + MCP**        | MCP provides the connection; a skill teaches Claude how to use it well           | MCP connects to your database, a skill documents your schema and query patterns                    |
| **Skill + Subagent**   | A skill spawns subagents for parallel work                                       | `/review` skill kicks off security, performance, and style subagents that work in isolated context |
| **CLAUDE.md + Skills** | CLAUDE.md holds always-on rules; skills hold reference material loaded on demand | CLAUDE.md says "follow our API conventions," a skill contains the full API style guide             |
| **Hook + MCP**         | A hook triggers external actions through MCP                                     | Post-edit hook sends a Slack notification when Claude modifies critical files                      |

## Understand context costs

Every feature you add consumes some of Claude's context. Too much can fill up your context window, but it can also add noise that makes Claude less effective; skills may not trigger correctly, or Claude may lose track of your conventions. Understanding these trade-offs helps you build an effective setup.

### Context cost by feature

Each feature has a different loading strategy and context cost:

| Feature         | When it loads             | What loads                                    | Context cost                                 |
| --------------- | ------------------------- | --------------------------------------------- | -------------------------------------------- |
| **CLAUDE.md**   | Session start             | Full content                                  | Every request                                |
| **Skills**      | Session start + when used | Descriptions at start, full content when used | Low (descriptions every request)\*           |
| **MCP servers** | Session start             | All tool definitions and schemas              | Every request                                |
| **Subagents**   | When spawned              | Fresh context with specified skills           | Isolated from main session                   |
| **Hooks**       | On trigger                | Nothing (runs externally)                     | Zero, unless hook returns additional context |

\*By default, skill descriptions load at session start so Claude can decide when to use them. Set `disable-model-invocation: true` in a skill's frontmatter to hide it from Claude entirely until you invoke it manually. This reduces context cost to zero for skills you only trigger yourself.

### Understand how features load

Each feature loads at different points in your session. The tabs below explain when each one loads and what goes into context.

<img src="https://mintcdn.com/claude-code/ELkJZG54dIaeldDC/images/context-loading.svg?fit=max&auto=format&n=ELkJZG54dIaeldDC&q=85&s=bd2e24b8e6a99b31ecfffb63f5b23bf5" alt="Context loading: CLAUDE.md and MCP load at session start and stay in every request. Skills load descriptions at start, full content on invocation. Subagents get isolated context. Hooks run externally." data-og-width="720" width="720" data-og-height="410" height="410" data-path="images/context-loading.svg" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/ELkJZG54dIaeldDC/images/context-loading.svg?w=280&fit=max&auto=format&n=ELkJZG54dIaeldDC&q=85&s=aebaadd1f484f285dd9cb4e0ea6d49b9 280w, https://mintcdn.com/claude-code/ELkJZG54dIaeldDC/images/context-loading.svg?w=560&fit=max&auto=format&n=ELkJZG54dIaeldDC&q=85&s=030c9b46126d750de315612560082727 560w, https://mintcdn.com/claude-code/ELkJZG54dIaeldDC/images/context-loading.svg?w=840&fit=max&auto=format&n=ELkJZG54dIaeldDC&q=85&s=6c73f8b0389da4f3190843140c810fe9 840w, https://mintcdn.com/claude-code/ELkJZG54dIaeldDC/images/context-loading.svg?w=1100&fit=max&auto=format&n=ELkJZG54dIaeldDC&q=85&s=9844c55d08d2c386672447f2e8518669 1100w, https://mintcdn.com/claude-code/ELkJZG54dIaeldDC/images/context-loading.svg?w=1650&fit=max&auto=format&n=ELkJZG54dIaeldDC&q=85&s=21a9522d0e4bd10ced146aab850ede76 1650w, https://mintcdn.com/claude-code/ELkJZG54dIaeldDC/images/context-loading.svg?w=2500&fit=max&auto=format&n=ELkJZG54dIaeldDC&q=85&s=d318525915aee1a1a6a4215cfaa61fb9 2500w" />

<Tabs>
  <Tab title="CLAUDE.md">
    **When:** Session start

    **What loads:** Full content of all CLAUDE.md files (managed, user, and project levels).

    **Inheritance:** Claude reads CLAUDE.md files from your working directory up to the root, and discovers nested ones in subdirectories as it accesses those files. See [How Claude looks up memories](/en/memory#how-claude-looks-up-memories) for details.

    <Tip>Keep CLAUDE.md under \~500 lines. Move reference material to skills, which load on-demand.</Tip>
  </Tab>

  <Tab title="Skills">
    Skills are extra capabilities in Claude's toolkit. They can be reference material (like an API style guide) or invocable workflows you trigger with `/<name>` (like `/deploy`). Some are built-in; you can also create your own. Claude uses skills when appropriate, or you can invoke one directly.

    **When:** Depends on the skill's configuration. By default, descriptions load at session start and full content loads when used. For user-only skills (`disable-model-invocation: true`), nothing loads until you invoke them.

    **What loads:** For model-invocable skills, Claude sees names and descriptions in every request. When you invoke a skill with `/<name>` or Claude loads it automatically, the full content loads into your conversation.

    **How Claude chooses skills:** Claude matches your task against skill descriptions to decide which are relevant. If descriptions are vague or overlap, Claude may load the wrong skill or miss one that would help. To tell Claude to use a specific skill, invoke it with `/<name>`. Skills with `disable-model-invocation: true` are invisible to Claude until you invoke them.

    **Context cost:** Low until used. User-only skills have zero cost until invoked.

    **In subagents:** Skills work differently in subagents. Instead of on-demand loading, skills passed to a subagent are fully preloaded into its context at launch. Subagents don't inherit skills from the main session; you must specify them explicitly.

    <Tip>Use `disable-model-invocation: true` for skills with side effects. This saves context and ensures only you trigger them.</Tip>
  </Tab>

  <Tab title="MCP servers">
    **When:** Session start.

    **What loads:** All tool definitions and JSON schemas from connected servers.

    **Context cost:** [Tool search](/en/mcp#scale-with-mcp-tool-search) (enabled by default) loads MCP tools up to 10% of context and defers the rest until needed.

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

    **What loads:** Nothing by default. Hooks run as external scripts.

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
