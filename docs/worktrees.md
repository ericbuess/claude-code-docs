> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Run parallel sessions with worktrees

> Isolate parallel Claude Code sessions in separate git worktrees so changes don't collide. Covers the `--worktree` flag, subagent isolation, `.worktreeinclude`, cleanup, and non-git VCS hooks.

A [git worktree](https://git-scm.com/docs/git-worktree) is a separate working directory with its own files and branch, sharing the same repository history and remote as your main checkout. Running each Claude Code session in its own worktree means edits in one session never touch files in another, so one session can build a feature while a second fixes a bug.

<Note>
  Worktrees require a git repository; for other version control systems, [configure hooks to replace the git logic](#non-git-version-control). In the [desktop app](/en/desktop#work-in-parallel-with-sessions), every new session gets its own worktree automatically.
</Note>

Worktrees are one of several ways to run Claude in parallel. They isolate file edits, while [subagents](/en/sub-agents) and [agent teams](/en/agent-teams) coordinate the work itself. See [Run agents in parallel](/en/agents) to compare the approaches, or skip ahead to [Isolate subagents with worktrees](#isolate-subagents-with-worktrees) to use worktrees and subagents together.

Most sessions need only the first two sections: [start Claude in a worktree](#start-claude-in-a-worktree), then [clean up when you exit](#clean-up-worktrees). Return to the rest of the page when you need to [resume a session](#resume-a-worktree-session), [change how worktrees are created](#customize-worktree-creation), or [debug a failure](#troubleshooting).

## Start Claude in a worktree

Pass `--worktree` or `-w` with a name to create an isolated worktree and start Claude in it. By default, the worktree is created under `.claude/worktrees/<name>/` at your repository root, on a new branch named `worktree-<name>`:

```bash theme={null}
claude --worktree feature-auth
```

Run the command again with a different name in another terminal to start a second isolated session. If you omit the name, Claude generates one such as `bright-running-fox`.

Interactive runs require [workspace trust](/en/security): if you haven't run Claude in the directory before, run `claude` once there to accept the trust dialog, or `--worktree` exits with an error prompting you to. Non-interactive runs with `-p` skip the trust check, so `claude -p --worktree` proceeds without it.

<Tip>
  Add `.claude/worktrees/` to your `.gitignore` so worktree contents don't appear as untracked files in your main checkout.
</Tip>

### Set up the worktree environment

A worktree is a fresh checkout, so initialize your development environment there: ask Claude to install dependencies, or run your project's setup yourself in the worktree directory under `.claude/worktrees/`. To carry gitignored files such as `.env` into every new worktree automatically, add a [`.worktreeinclude` file](#copy-gitignored-files-into-worktrees).

### Ask Claude to create a worktree

You can also ask Claude to "work in a worktree" during a session, and it creates one with the [`EnterWorktree`](/en/tools-reference) tool. Once in a worktree, Claude can switch directly to another one under `.claude/worktrees/` by calling `EnterWorktree` with the target path; the previous worktree stays on disk untouched.

When Claude enters a path outside the repository's `.claude/worktrees/` directory, Claude Code asks for your approval first, because the move takes the session's working directory, write access, and project configuration such as `CLAUDE.md` and settings to that location. An `EnterWorktree` [permission rule](/en/permissions) or choosing "don't ask again" doesn't suppress this prompt; only `bypassPermissions` mode skips it. Before v2.1.206, Claude could enter any existing worktree path without asking.

## Clean up worktrees

When you exit an interactive worktree session, Claude checks the worktree for work that removal would delete: changed or untracked files, and new commits.

* **The worktree is clean**: for an unnamed session, Claude removes the worktree and its branch automatically. A [named](/en/sessions#name-your-sessions) session prompts you first so you can keep the worktree for later
* **The worktree has work in it**: Claude prompts you to keep or remove the worktree. Keeping preserves the directory and branch so you can return later. Removing deletes the worktree directory and its branch, along with all the work in them

Non-interactive runs with `-p` have no exit prompt, so Claude doesn't clean up their worktrees. Remove them with `git worktree remove`.

On Windows, removing a worktree doesn't delete files outside it. If a folder inside the worktree is really a link to somewhere else, such as an NTFS junction or a directory symlink, Claude Code deletes only the link and keeps the folder it points to. Before v2.1.205, removing a worktree with a link nested in a subdirectory could delete the folder it pointed to.

## Resume a worktree session

When you resume a session that was inside a worktree, Claude Code returns the session to that worktree. This holds for interactive resumes, for `--continue` and `--resume` in [non-interactive mode](/en/headless) with `-p`, and for the Agent SDK. Back inside the worktree, Claude can still exit it with the [`ExitWorktree`](/en/tools-reference) tool.

A resume that forks the session with `--fork-session` starts in the directory you launched Claude from and leaves the original session's worktree untouched. If the worktree directory no longer exists, the session resumes in the directory you launched Claude from.

<Note>
  Before v2.1.212, a non-interactive resume stayed in the starting directory and `ExitWorktree` reported that there was no active worktree session to exit.
</Note>

{/* min-version: 2.1.198 */}When Claude enters or exits a worktree that Claude Code created with git, the transcript follows: Claude Code records the session under the session's new working directory, the same way [`/cd`](/en/commands) does, so `/desktop` and `--resume` find it there. Exiting moves it back the same way. A worktree created by a [`WorktreeCreate` hook](#non-git-version-control) keeps its transcript at the launch directory. Requires Claude Code v2.1.198 or later.

## Isolate subagents with worktrees

Subagents can run in their own worktrees so parallel edits don't conflict. Ask Claude to "use worktrees for your agents", or make the isolation permanent for a [custom subagent](/en/sub-agents#supported-frontmatter-fields) by adding `isolation: worktree` to its frontmatter.

This subagent in `.claude/agents/` always runs in its own worktree:

```markdown theme={null}
---
name: refactorer
description: Applies mechanical refactors across many files
isolation: worktree
---

Apply the requested refactor across every affected file, then run the tests
and report the results.
```

Each subagent gets a temporary worktree that Claude Code removes automatically when the subagent finishes without changes; a worktree with changes stays on disk until the [periodic sweep below](#clean-up-subagent-and-background-session-worktrees) can remove it without losing work.

Subagent worktrees use the same [base branch](#choose-the-base-branch) as `--worktree`, so they branch from your repository's default branch unless `worktree.baseRef` is set to `"head"`.

### Clean up subagent and background-session worktrees

A periodic sweep removes worktrees that Claude created for subagents and [background sessions](/en/agent-view#how-file-edits-are-isolated) once they are older than your [`cleanupPeriodDays`](/en/settings#available-settings) setting. The sweep skips a worktree that still holds work: changed or untracked files, or unpushed commits. It never removes worktrees you create with `--worktree`.

While an agent is running, Claude runs `git worktree lock` on its worktree so that concurrent cleanup cannot remove it. The lock is released when the agent finishes.

{/* min-version: 2.1.210 */}The sweep also releases a lock Claude Code set for a session whose process has exited, so a killed background session doesn't leave its worktree permanently locked. The sweep never releases a lock you set yourself with `git worktree lock`. Before v2.1.210, a lock left by a killed session stayed in place until you ran `git worktree unlock`.

To clean up a worktree that the sweep keeps, run `git worktree remove`, adding `--force` if the worktree has uncommitted changes or untracked files.

## Customize worktree creation

Claude Code's defaults for creating worktrees cover most sessions: it creates them under `.claude/worktrees/`, branches them from your repository's default branch, and checks out only tracked files. The options in this section change those defaults.

### Choose the base branch

New worktrees branch from the repository's default branch, so most sessions don't need this setting. Set `worktree.baseRef` in [settings](/en/settings#worktree-settings) to branch from your current work instead. The setting accepts two values:

* `"fresh"` (default): branch from the repository's default branch on the remote, usually `main`, so the worktree starts from a clean tree matching the remote.
* `"head"`: branch from your current local `HEAD`, so the worktree carries your unpushed commits and feature-branch state. Use this when isolating subagents that need to operate on in-progress work. Inside a worktree, `"head"` resolves to that worktree's `HEAD`, not the main checkout's.

You can't set `worktree.baseRef` to a branch name. To start a worktree from a specific existing branch, [create it with git directly](#manage-worktrees-manually).

For a `"fresh"` base, Claude Code keeps `origin/HEAD` current: when the repository hasn't been fetched in the last 24 hours, it fetches the default branch, capped at five seconds, and uses the locally cached ref if the fetch fails. If no remote is configured, or `origin/HEAD` isn't cached locally and can't be fetched, the worktree falls back to your current local `HEAD`. Before v2.1.208, a fresh worktree used whatever `origin/HEAD` was already cached locally.

This example makes every new worktree branch from your current work:

```json theme={null}
{
  "worktree": {
    "baseRef": "head"
  }
}
```

### Branch from a pull request

To branch from a specific pull request, pass `--worktree` the PR number prefixed with `#`, or a full GitHub pull request URL. Claude Code fetches `pull/<number>/head` from `origin` and creates the worktree at `.claude/worktrees/pr-<number>`. Quote the argument so your shell doesn't treat `#` as the start of a comment:

```bash theme={null}
claude --worktree "#1234"
```

### Copy gitignored files into worktrees

A worktree is a fresh checkout, so untracked files like `.env` or `.env.local` from your main repository are not present. To copy them automatically when Claude creates a worktree, add a `.worktreeinclude` file to your project root.

The file uses `.gitignore` syntax. Only files that match a pattern and are also gitignored are copied, so tracked files are never duplicated.

This `.worktreeinclude` copies two env files and a secrets config into each new worktree:

```text .worktreeinclude theme={null}
.env
.env.local
config/secrets.json
```

This applies to every worktree Claude Code creates with git: `--worktree` worktrees, [subagent worktrees](#isolate-subagents-with-worktrees), and parallel sessions in the [desktop app](/en/desktop#work-in-parallel-with-sessions). With a [`WorktreeCreate` hook](#non-git-version-control), copy the files inside the hook script.

### Reuse a worktree name

Passing `--worktree` a name whose directory already exists opens that existing worktree instead of creating a new one.

With the default `"fresh"` [base](#choose-the-base-branch), a reopened worktree resets to the repository's default branch instead of continuing at its old tip when all of the following hold:

* It has no uncommitted changes or untracked files.
* It is still on the branch Claude Code created for it.
* It has no commits of its own, or its pull request was merged and its remote branch deleted.

Claude Code detects the merged case from git state alone: the remote branch the worktree pushed to no longer exists, and every commit in the worktree is already on the default branch.

Anything else reopens at the old tip: a worktree that fails any of the conditions, one whose state can't be verified, and any reuse when `worktree.baseRef` is `"head"` or the name is a pull request number. Before v2.1.208, a reused name always reopened the old worktree at its old tip.

### Replace worktree creation with a hook

Configure a [`WorktreeCreate` hook](/en/hooks#worktreecreate) to replace the default `git worktree` logic entirely, including placing worktrees somewhere other than `.claude/worktrees/`. For a complete example, see [Non-git version control](#non-git-version-control).

## What worktrees share with the main checkout

A worktree gets its own files and branch, but it shares the repository's `.git` directory, project-scope plugins, and saved permission approvals with the main checkout:

* **The repository's `.git` directory**: git commands in a worktree write to the main repository's shared `.git` directory, and [sandboxing](/en/sandboxing#filesystem-isolation) allows those writes, so commands such as `git commit` work from inside a worktree with the sandbox enabled.
* {/* min-version: 2.1.200 */}**Plugins**: plugins installed at [project scope](/en/plugins-reference#plugin-installation-scopes) from the main checkout also load in worktrees of the same repository, so you don't need to reinstall them per worktree. Requires Claude Code v2.1.200 or later.
* {/* min-version: 2.1.211 */}**Permission approvals**: choosing "Yes, don't ask again" for a Bash command in a worktree session saves the rule to the main checkout's `.claude/settings.local.json`, so it applies in the main checkout and in every other worktree of the repository, and it survives the worktree's removal. Before v2.1.211, an approval granted in a worktree was saved inside that worktree, didn't apply elsewhere, and was lost when the worktree was removed. See [where approvals are saved](/en/permissions#permission-system).

All three apply whether you create the worktree with `--worktree`, with `git worktree add`, or through the [desktop app](/en/desktop#work-in-parallel-with-sessions).

## Manage worktrees manually

Create worktrees with Git directly when you need to check out a specific existing branch or place the worktree outside the repository.

Create a worktree on a new branch:

```bash theme={null}
git worktree add ../project-feature-a -b feature-a
```

Create a worktree from an existing branch:

```bash theme={null}
git worktree add ../project-bugfix bugfix-123
```

Start Claude in the worktree:

```bash theme={null}
cd ../project-feature-a
claude
```

List your worktrees:

```bash theme={null}
git worktree list
```

Remove one when you're done with it:

```bash theme={null}
git worktree remove ../project-feature-a
```

See the [Git worktree documentation](https://git-scm.com/docs/git-worktree) for the full command reference.

## Non-git version control

Worktree isolation uses git by default. For SVN, Perforce, Mercurial, or other systems, configure [`WorktreeCreate` and `WorktreeRemove` hooks](/en/hooks#worktreecreate) to provide custom creation and cleanup logic. Because the hook replaces the default git behavior, [`.worktreeinclude`](#copy-gitignored-files-into-worktrees) is not processed when you use `--worktree`. Copy any local configuration files inside your hook script instead.

This `WorktreeCreate` hook reads the worktree name from the JSON on stdin with `jq`, checks out a fresh SVN working copy, and prints the directory path so Claude Code can use it as the session's working directory. Add the configuration to your [`settings.json`](/en/settings#settings-files):

```json theme={null}
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

Pair it with a `WorktreeRemove` hook to clean up when the session ends. See the [hooks reference](/en/hooks#worktreecreate) for the input schema and a removal example.

## Troubleshooting

The errors below occur when Claude Code creates a worktree or enters one at startup.

### Claude Code can't enter the worktree at startup

When Claude Code can't enter the worktree directory at startup, it prints an error naming the path and exits with code 1. This can happen when a [`WorktreeCreate` hook](/en/hooks#worktreecreate) prints something other than the directory it created, or when the directory was deleted after it was set up. Before v2.1.205, this crashed the session, and with `-p` it stalled for about 30 seconds before exiting with code 0.

### Worktree creation fails on a symlinked path

Claude Code refuses to create a worktree when `.claude`, `.claude/worktrees`, or the worktree directory itself is a symlink, and the error names the symlinked path. Remove the symlink and retry. Before v2.1.212, if the repository already contained a committed symlink at one of those paths, worktree creation followed it and could create files outside the repository.

## See also

Worktrees handle file isolation. The related pages below cover delegating work into those isolated checkouts and switching between the sessions you create:

* [Subagents](/en/sub-agents): delegate work to isolated agents within a session
* [Agent teams](/en/agent-teams): coordinate multiple Claude sessions automatically
* [Manage sessions](/en/sessions): name, resume, and switch between conversations
* [Desktop parallel sessions](/en/desktop#work-in-parallel-with-sessions): worktree-backed sessions in the desktop app
