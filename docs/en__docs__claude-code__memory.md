# Manage Claude's memory

> Learn how to manage Claude Code's memory across sessions with different memory locations and best practices.

Claude Code can remember your preferences across sessions, like style guidelines and common commands in your workflow.

## Determine memory type

Claude Code offers four memory locations in a hierarchical structure, each serving a different purpose:

| Memory Type                | Location                                                                                                                                                | Purpose                                             | Use Case Examples                                                    | Shared With                     |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------- |
| **Enterprise policy**      | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br />Linux: `/etc/claude-code/CLAUDE.md`<br />Windows: `C:\ProgramData\ClaudeCode\CLAUDE.md` | Organization-wide instructions managed by IT/DevOps | Company coding standards, security policies, compliance requirements | All users in organization       |
| **Project memory**         | `./CLAUDE.md` or `./.claude/CLAUDE.md`                                                                                                                  | Team-shared instructions for the project            | Project architecture, coding standards, common workflows             | Team members via source control |
| **User memory**            | `~/.claude/CLAUDE.md`                                                                                                                                   | Personal preferences for all projects               | Code styling preferences, personal tooling shortcuts                 | Just you (all projects)         |
| **Project memory (local)** | `./CLAUDE.local.md`                                                                                                                                     | Personal project-specific preferences               | *(Deprecated, see below)* Your sandbox URLs, preferred test data     | Just you (current project)      |

All memory files are automatically loaded into Claude Code's context when launched. Files higher in the hierarchy take precedence and are loaded first, providing a foundation that more specific memories build upon.

## CLAUDE.md imports

CLAUDE.md files can import additional files using `@path/to/import` syntax. The following example imports 3 files:

```
See @README for project overview and @package.json for available npm commands for this project.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

Both relative and absolute paths are allowed. In particular, importing files in user's home dir is a convenient way for your team members to provide individual instructions that are not checked into the repository. Previously CLAUDE.local.md served a similar purpose, but is now deprecated in favor of imports since they work better across multiple git worktrees.

```
# Individual Preferences
- @~/.claude/my-project-instructions.md
```

To avoid potential collisions, imports are not evaluated inside markdown code spans and code blocks.

```
This code span will not be treated as an import: `@anthropic-ai/claude-code`
```

Imported files can recursively import additional files, with a max-depth of 5 hops. You can see what memory files are loaded by running `/memory` command.

## How Claude looks up memories

Claude Code reads memories recursively: starting in the cwd, Claude Code recurses up to (but not including) the root directory */* and reads any CLAUDE.md or CLAUDE.local.md files it finds. This is especially convenient when working in large repositories where you run Claude Code in *foo/bar/*, and have memories in both *foo/CLAUDE.md* and *foo/bar/CLAUDE.md*.

Claude will also discover CLAUDE.md nested in subtrees under your current working directory. Instead of loading them at launch, they are only included when Claude reads files in those subtrees.

## Quickly add memories with the `#` shortcut

The fastest way to add a memory is to start your input with the `#` character:

```
# Always use descriptive variable names
```

You'll be prompted to select which memory file to store this in.

## Directly edit memories with `/memory`

Use the `/memory` slash command during a session to open any memory file in your system editor for more extensive additions or organization.

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

## Organization-level memory management

Enterprise organizations can deploy centrally managed CLAUDE.md files that apply to all users.

To set up organization-level memory management:

1. Create the enterprise memory file in the appropriate location for your operating system:

* macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
* Linux/WSL: `/etc/claude-code/CLAUDE.md`
* Windows: `C:\ProgramData\ClaudeCode\CLAUDE.md`

2. Deploy via your configuration management system (MDM, Group Policy, Ansible, etc.) to ensure consistent distribution across all developer machines.

## Memory best practices

* **Be specific**: "Use 2-space indentation" is better than "Format code properly".
* **Use structure to organize**: Format each individual memory as a bullet point and group related memories under descriptive markdown headings.
* **Review periodically**: Update memories as your project evolves to ensure Claude is always using the most up to date information and context.
