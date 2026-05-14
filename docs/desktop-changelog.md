> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Desktop changelog

> Release notes for Claude Code on Desktop, covering new features, improvements, and bug fixes by Desktop app version.

This page covers Claude Code-specific changes in the Desktop app. For changes to the Claude Code CLI bundled inside the app, see the [CLI changelog](/en/changelog).

<Update label="1.7196.0" description="May 12, 2026">
  * Fixed auto-update hanging indefinitely on Relaunch to Update when popout windows refused to close.
  * Fixed local sessions failing to start after a corrupted bundled Claude Code binary was cached.
  * Fixed the credential helper opening duplicate browser sign-in tabs when starting a new conversation.
  * Fixed Code tab PR status icons showing the wrong state for merged, merge-queued, and draft pull requests.
  * Fixed Quick Entry dropping characters entered with a Korean, Japanese, or Chinese input method.
  * Added an "Also delete files on disk" option to the scheduled task delete dialog; checking it removes the task's `SKILL.md` file and associated data from `~/.claude/scheduled-tasks/`.
  * Added support for mouse back and forward buttons for navigating the chat view.

  **3P managed deployments**

  * Added an organization banner across the top of the app window, configured by IT administrators.
</Update>

<Update label="1.6889.0" description="May 8, 2026">
  * Added MCP App widget rendering in Code tab sessions.
  * Added an OS notification when a Code session finishes a task and you aren't currently viewing it.
  * Added automatic detection and re-download of corrupted Claude Code CLI binaries on macOS.
  * Added support for scheduled tasks to modify their own schedule or prompt during a run using the `update_scheduled_task` MCP tool.
  * Updated the list of available MCP tools to reload automatically when the local MCP configuration changes.
  * Updated PR auto-fix to post a reply on each review thread it addresses and mark the thread resolved.
  * Improved SSH session startup speed by preconnecting saved SSH configurations at app launch.
  * Fixed pasting a code block into a busy terminal; the app now opens a new terminal tab when the existing one has a process running.
  * Fixed PR bar issues in Code sessions: each row now shows its own diff, and the sidebar status icon updates when a PR is merged.
  * Fixed garbled scrollback, such as stray `%` marks and half-wrapped prompts, when opening the terminal pane after running a code block.
  * Fixed Code session links opening with overlapping window controls when reached via Handoff or share links.
  * Fixed git commit signing failing in local sessions when the signing key is held by 1Password or Secretive.
  * Fixed locally installed plugins disappearing from sessions after the plugin registry file became corrupted by concurrent writes.
  * Fixed scheduled tasks running with auto-approve echoing tool-use suggestions into the session.
  * Fixed SSH plugin sync so a single problematic plugin no longer blocks sync for the rest.

  **3P managed deployments**

  * Added support for stdio-transport local MCP servers via the `managedMcpServers` managed-settings key; the connector detail panel now shows the command and arguments, and environment variable values are masked outside the admin Setup screen.
  * Added a managed-settings option to disable `claude://` deep-link handling.
  * Added support for customizing model display names in the model picker via `labelOverride`.
  * Fixed per-tool MCP server policies set by administrators not being enforced in all session types.
</Update>

<Update label="1.6608.0" description="May 7, 2026">
  * Fixed scheduled tasks failing to run when a previous run was stuck waiting on a permission prompt.
  * Fixed scheduled tasks repeatedly retrying a failed run instead of waiting for the next scheduled time.
  * Fixed scheduled-task history incorrectly showing "computer asleep" for runs skipped due to a concurrency limit.
  * Added per-plugin auto-install for organization-provisioned plugins via the plugin manifest.
  * Added Unarchive to the Code session context menu; sending a message in an archived session now restores it automatically.
  * Added a warning when archiving a Code session that has uncommitted changes in its worktree.
  * Added a warning when quitting or restarting the app while local Code sessions are running.
  * Added csh and tcsh login shell support when connecting to remote SSH hosts.
  * Fixed folder permission rules failing to match when the connected folder is a drive root.
  * Fixed Windows installs leaving an empty folder under `%LOCALAPPDATA%`.
</Update>

<Update label="1.6259.0" description="May 5, 2026">
  * Code sessions now default the working directory to the home folder when none is configured.
  * `settings.json` project settings now cascade from the SSH host for SSH Code sessions.
  * "Always allow" tool permissions now persist across app restarts and display their scope.
  * Added automatic detection and re-download of corrupted Claude Code CLI binaries on Windows.
  * The PR bar now shows stacked and sibling pull requests alongside the branch's own PR.
  * Messages sent while a turn is running are now queued rather than dropped.
  * Opening a Code session link on iOS now continues the session on macOS via Handoff.
</Update>

<Update label="1.5354.0" description="April 29, 2026">
  * Disabling the org Skills toggle in the admin console now removes the skill management tools `list_skills`, `save_skill`, and `propose_skills` from Code sessions.
  * The preview pane now opens automatically when a session's working directory is a symlink.
  * Improved login-shell PATH extraction for more reliable tool discovery.
</Update>

<Update label="1.5220.0" description="April 28, 2026">
  * Added a multi-tab terminal pane; click **+** in the terminal pane header to open a second tab, or right-click a folder in the chat to choose **Open in terminal**.
  * Fixed worktree pool re-lease creating a fresh worktree on checkout failure instead of re-using an existing one.
  * Fixed rewind selecting the wrong assistant message after a previous rewind created a fork.
</Update>

<Update label="1.5186.0" description="April 28, 2026">
  * Added `list_sessions`, `search_session_transcripts`, and `archive_session` MCP tools for managing Code sessions from within a session.
  * Improved SSH wake-path reliability and surfaced `ProxyCommand` stderr output for easier debugging.
  * Fixed login-shell PATH extraction for fish shell users. It was returning a newline-separated list instead of a colon-separated one.
  * Fixed the SSH remote control socket directory permissions so `~/.claude/remote` is no longer world-traversable.
  * PR review bodies and issue comments are now forwarded to the auto-fix engine.
  * Added a category-driven error UI for Code sessions that groups failures by type and surfaces actionable recovery steps.
</Update>
