> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Manage Claude's memory

> Learn how to manage Claude Code's memory across sessions with different memory locations and best practices.

Claude Code has two kinds of memory that persist across sessions:

* **Auto memory**: Claude automatically saves useful context like project patterns, key commands, and your preferences. This persists across sessions.
* **CLAUDE.md files**: Markdown files you write and maintain with instructions, rules, and preferences for Claude to follow.

Both are loaded into Claude's context at the start of every session, though auto memory loads only the first 200 lines of its main file.

## Determine memory type

Claude Code offers several memory locations in a hierarchical structure, each serving a different purpose:

| Memory Type                | Location                                                                                                                                                        | Purpose                                             | Use Case Examples                                                    | Shared With                     |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------- |
| **Managed policy**         | • macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br />• Linux: `/etc/claude-code/CLAUDE.md`<br />• Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | Organization-wide instructions managed by IT/DevOps | Company coding standards, security policies, compliance requirements | All users in organization       |
| **Project memory**         | `./CLAUDE.md` or `./.claude/CLAUDE.md`                                                                                                                          | Team-shared instructions for the project            | Project architecture, coding standards, common workflows             | Team members via source control |
| **Project rules**          | `./.claude/rules/*.md`                                                                                                                                          | Modular, topic-specific project instructions        | Language-specific guidelines, testing conventions, API standards     | Team members via source control |
| **User memory**            | `~/.claude/CLAUDE.md`                                                                                                                                           | Personal preferences for all projects               | Code styling preferences, personal tooling shortcuts                 | Just you (all projects)         |
| **Project memory (local)** | `./CLAUDE.local.md`                                                                                                                                             | Personal project-specific preferences               | Your sandbox URLs, preferred test data                               | Just you (current project)      |
| **Auto memory**            | `~/.claude/projects/<project>/memory/`                                                                                                                          | Claude's automatic notes and learnings              | Project patterns, debugging insights, architecture notes             | Just you (per project)          |

CLAUDE.md files in the directory hierarchy above the working directory are loaded in full at launch. CLAUDE.md files in child directories load on demand when Claude reads files in those directories. Auto memory loads only the first 200 lines of `MEMORY.md`. More specific instructions take precedence over broader ones.

<Note>
  CLAUDE.local.md files are automatically added to .gitignore, making them ideal for private project-specific preferences that shouldn't be checked into version control.
</Note>

## Auto memory

Auto memory is a persistent directory where Claude records learnings, patterns, and insights as it works. Unlike CLAUDE.md files that contain instructions you write for Claude, auto memory contains notes Claude writes for itself based on what it discovers during sessions.

<Note>
  Auto memory is being rolled out gradually. If you aren't seeing auto memory, you can opt in by setting `CLAUDE_CODE_DISABLE_AUTO_MEMORY=0` in your environment.
</Note>

### What Claude remembers

As Claude works, it may save things like:

* Project patterns: build commands, test conventions, code style preferences
* Debugging insights: solutions to tricky problems, common error causes
* Architecture notes: key files, module relationships, important abstractions
* Your preferences: communication style, workflow habits, tool choices

### Where auto memory is stored

Each project gets its own memory directory at `~/.claude/projects/<project>/memory/`. The `<project>` path is derived from the git repository root, so all subdirectories within the same repo share one auto memory directory. Git worktrees get separate memory directories. Outside a git repo, the working directory is used instead.

The directory contains a `MEMORY.md` entrypoint and optional topic files:

```text  theme={null}
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Concise index, loaded into every session
├── debugging.md       # Detailed notes on debugging patterns
├── api-conventions.md # API design decisions
└── ...                # Any other topic files Claude creates
```

`MEMORY.md` acts as an index of the memory directory. Claude reads and writes files in this directory throughout your session, using `MEMORY.md` to keep track of what's stored where.

### How it works

* The first 200 lines of `MEMORY.md` are loaded into Claude's system prompt at the start of every session. Content beyond 200 lines is not loaded automatically, and Claude is instructed to keep it concise by moving detailed notes into separate topic files.
* Topic files like `debugging.md` or `patterns.md` are not loaded at startup. Claude reads them on demand using its standard file tools when it needs the information.
* Claude reads and writes memory files during your session, so you'll see memory updates happen as you work.

### Manage auto memory

Auto memory files are markdown files you can edit at any time. Use `/memory` to open the file selector, which includes your auto memory entrypoint alongside your CLAUDE.md files.

To ask Claude to save something specific, tell it directly: "remember that we use pnpm, not npm" or "save to memory that the API tests require a local Redis instance".

When neither variable is set, auto memory follows the gradual rollout. The variable name uses double-negative logic: `DISABLE=0` means "don't disable" and forces auto memory on.

```bash  theme={null}
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1  # Force off
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=0  # Force on
```

## CLAUDE.md imports

CLAUDE.md files can import additional files using `@path/to/import` syntax. The following example imports 3 files:

```
See @README for project overview and @package.json for available npm commands for this project.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

Both relative and absolute paths are allowed. Relative paths resolve relative to the file containing the import, not the working directory. For private per-project preferences that shouldn't be checked into version control, prefer `CLAUDE.local.md`: it is automatically loaded and added to `.gitignore`.

If you work across multiple git worktrees, `CLAUDE.local.md` only exists in one. Use a home-directory import instead so all worktrees share the same personal instructions:

```
# Individual Preferences
- @~/.claude/my-project-instructions.md
```

<Warning>
  The first time Claude Code encounters external imports in a project, it shows an approval dialog listing the specific files. Approve to load them; decline to skip them. This is a one-time decision per project: once declined, the dialog does not resurface and the imports remain disabled.
</Warning>

To avoid potential collisions, imports are not evaluated inside markdown code spans and code blocks.

```
This code span will not be treated as an import: `@anthropic-ai/claude-code`
```

Imported files can recursively import additional files, with a max-depth of 5 hops. You can see what memory files are loaded by running `/memory` command.

## How Claude looks up memories

Claude Code reads memories recursively: starting in the cwd, Claude Code recurses up to (but not including) the root directory */* and reads any CLAUDE.md or CLAUDE.local.md files it finds. This is especially convenient when working in large repositories where you run Claude Code in *foo/bar/*, and have memories in both *foo/CLAUDE.md* and *foo/bar/CLAUDE.md*.

Claude will also discover CLAUDE.md nested in subtrees under your current working directory. Instead of loading them at launch, they are only included when Claude reads files in those subtrees.

### Load memory from additional directories

The `--add-dir` flag gives Claude access to additional directories outside your main working directory. By default, CLAUDE.md files from these directories are not loaded.

To also load memory files (CLAUDE.md, .claude/CLAUDE.md, and .claude/rules/\*.md) from additional directories, set the `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` environment variable:

```bash  theme={null}
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

## Directly edit memories with `/memory`

Use the `/memory` command during a session to open any memory file in your system editor for more extensive additions or organization.

## Set up project memory

Suppose you want to set up a CLAUDE.md file to store important project information, conventions, and frequently used commands. Project memory can be stored in either `./CLAUDE.md` or `./.claude/CLAUDE.md`.

Bootstrap a CLAUDE.md for your codebase with the following command:

```
> /init
```

<Tip>
  Tips:

  * Include frequently used commands (build, test, lint) to avoid repeated searches
  * Document code style preferences and naming conventions
  * Add important architectural patterns specific to your project
  * CLAUDE.md memories can be used for both instructions shared with your team and for your individual preferences.
</Tip>

## Modular rules with `.claude/rules/`

For larger projects, you can organize instructions into multiple files using the `.claude/rules/` directory. This allows teams to maintain focused, well-organized rule files instead of one large CLAUDE.md.

### Basic structure

Place markdown files in your project's `.claude/rules/` directory:

```
your-project/
├── .claude/
│   ├── CLAUDE.md           # Main project instructions
│   └── rules/
│       ├── code-style.md   # Code style guidelines
│       ├── testing.md      # Testing conventions
│       └── security.md     # Security requirements
```

All `.md` files in `.claude/rules/` are automatically loaded as project memory, with the same priority as `.claude/CLAUDE.md`.

### Path-specific rules

Rules can be scoped to specific files using YAML frontmatter with the `paths` field. These conditional rules only apply when Claude is working with files matching the specified patterns.

```markdown  theme={null}
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
- Include OpenAPI documentation comments
```

Rules without a `paths` field are loaded unconditionally and apply to all files.

### Glob patterns

The `paths` field supports standard glob patterns:

| Pattern                | Matches                                  |
| ---------------------- | ---------------------------------------- |
| `**/*.ts`              | All TypeScript files in any directory    |
| `src/**/*`             | All files under `src/` directory         |
| `*.md`                 | Markdown files in the project root       |
| `src/components/*.tsx` | React components in a specific directory |

You can specify multiple patterns:

```markdown  theme={null}
---
paths:
  - "src/**/*.ts"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

Brace expansion is supported for matching multiple extensions or directories:

```markdown  theme={null}
---
paths:
  - "src/**/*.{ts,tsx}"
  - "{src,lib}/**/*.ts"
---

# TypeScript/React Rules
```

This expands `src/**/*.{ts,tsx}` to match both `.ts` and `.tsx` files.

### Subdirectories

Rules can be organized into subdirectories for better structure:

```
.claude/rules/
├── frontend/
│   ├── react.md
│   └── styles.md
├── backend/
│   ├── api.md
│   └── database.md
└── general.md
```

All `.md` files are discovered recursively.

### Symlinks

The `.claude/rules/` directory supports symlinks, allowing you to share common rules across multiple projects:

```bash  theme={null}
# Symlink a shared rules directory
ln -s ~/shared-claude-rules .claude/rules/shared

# Symlink individual rule files
ln -s ~/company-standards/security.md .claude/rules/security.md
```

Symlinks are resolved and their contents are loaded normally. Circular symlinks are detected and handled gracefully.

### User-level rules

You can create personal rules that apply to all your projects in `~/.claude/rules/`:

```
~/.claude/rules/
├── preferences.md    # Your personal coding preferences
└── workflows.md      # Your preferred workflows
```

User-level rules are loaded before project rules, giving project rules higher priority.

<Tip>
  Best practices for `.claude/rules/`:

  * **Keep rules focused**: Each file should cover one topic (e.g., `testing.md`, `api-design.md`)
  * **Use descriptive filenames**: The filename should indicate what the rules cover
  * **Use conditional rules sparingly**: Only add `paths` frontmatter when rules truly apply to specific file types
  * **Organize with subdirectories**: Group related rules (e.g., `frontend/`, `backend/`)
</Tip>

## Organization-level memory management

Organizations can deploy centrally managed CLAUDE.md files that apply to all users.

To set up organization-level memory management:

1. Create the managed memory file at the **Managed policy** location shown in the [memory types table above](#determine-memory-type).

2. Deploy via your configuration management system (MDM, Group Policy, Ansible, etc.) to ensure consistent distribution across all developer machines.

## Memory best practices

* **Be specific**: "Use 2-space indentation" is better than "Format code properly".
* **Use structure to organize**: Format each individual memory as a bullet point and group related memories under descriptive markdown headings.
* **Review periodically**: Update memories as your project evolves to ensure Claude is always using the most up to date information and context.
