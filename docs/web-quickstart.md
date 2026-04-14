> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Get started with Claude Code on the web

> Run Claude Code in the cloud from your browser or phone. Connect a GitHub repository, submit a task, and review the PR without local setup.

<Note>
  Claude Code on the web is in research preview for Pro, Max, and Team users, and for Enterprise users with premium seats or Chat + Claude Code seats.
</Note>

Claude Code on the web runs on Anthropic-managed cloud infrastructure instead of your machine. Submit tasks from [claude.ai/code](https://claude.ai/code) in your browser or the Claude mobile app.

You'll need a GitHub repository to [get started](#connect-github-and-create-an-environment). Claude clones it into an isolated virtual machine, makes changes, and pushes a branch for you to review. Sessions persist across devices, so a task you start on your laptop is ready to review from your phone later.

Claude Code on the web works well for:

* **Parallel tasks**: run several independent tasks at once, each in its own session and branch, without managing multiple worktrees
* **Repos you don't have locally**: Claude clones the repo fresh every session, so you don't need it checked out
* **Tasks that don't need frequent steering**: submit a well-defined task, do something else, and review the result when Claude is done
* **Code questions and exploration**: understand a codebase or trace how a feature is implemented without a local checkout

For work that needs your local config, tools, or environment, running Claude Code locally or using [Remote Control](/en/remote-control) is a better fit.

## How sessions run

When you submit a task:

1. **Clone and prepare**: your repository is cloned to an Anthropic-managed VM, and your [setup script](/en/claude-code-on-the-web#setup-scripts) runs if configured.
2. **Configure network**: internet access is set based on your environment's [access level](/en/claude-code-on-the-web#access-levels).
3. **Work**: Claude analyzes code, makes changes, runs tests, and checks its work. You can watch and steer throughout, or step away and come back when it's done.
4. **Push the branch**: when Claude reaches a stopping point, it pushes its branch to GitHub. You review the diff, leave inline comments, create a PR, or send another message to keep going.

The session doesn't close when the branch is pushed. PR creation and further edits all happen within the same conversation.

## Compare ways to run Claude Code

Claude Code behaves the same everywhere. What changes is where code executes and whether your local config is available. The Desktop app offers both local and cloud sessions, so its answers below depend on which you choose:

|                                              | On the web                                                                                                      | Remote Control               | Terminal CLI           | Desktop app                 |
| :------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- | :--------------------------- | :--------------------- | :-------------------------- |
| **Code runs on**                             | Anthropic cloud VM                                                                                              | Your machine                 | Your machine           | Your machine or cloud VM    |
| **You chat from**                            | claude.ai or mobile app                                                                                         | claude.ai or mobile app      | Your terminal          | The Desktop UI              |
| **Uses your local config**                   | No, repo only                                                                                                   | Yes                          | Yes                    | Yes for local, no for cloud |
| **Requires GitHub**                          | Yes, or [bundle a local repo](/en/claude-code-on-the-web#send-local-repositories-without-github) via `--remote` | No                           | No                     | Only for cloud sessions     |
| **Keeps running if you disconnect**          | Yes                                                                                                             | While terminal stays open    | No                     | Depends on session type     |
| **[Permission modes](/en/permission-modes)** | Auto accept edits, Plan                                                                                         | Ask, Auto accept edits, Plan | All modes              | Depends on session type     |
| **Network access**                           | Configurable per environment                                                                                    | Your machine's network       | Your machine's network | Depends on session type     |

See the [terminal quickstart](/en/quickstart), [Desktop app](/en/desktop), or [Remote Control](/en/remote-control) docs to set those up.

## Connect GitHub and create an environment

Setup is a one-time process. If you already use the GitHub CLI, you can [do this from your terminal](#connect-from-your-terminal) instead of the browser.

<Steps>
  <Step title="Visit claude.ai/code">
    Go to [claude.ai/code](https://claude.ai/code) and sign in with your Anthropic account.
  </Step>

  <Step title="Install the Claude GitHub App">
    After signing in, claude.ai/code prompts you to connect GitHub. Follow the prompt to install the Claude GitHub App and grant it access to your repositories. Cloud sessions work with existing GitHub repositories, so to start a new project, [create an empty repository on GitHub](https://github.com/new) first.
  </Step>

  <Step title="Create your environment">
    After connecting GitHub, you'll be prompted to create a cloud environment. The environment controls what network access Claude has during sessions and what runs when a new session is created. See [Installed tools](/en/claude-code-on-the-web#installed-tools) for what's available without any configuration.

    The form has these fields:

    * **Name**: a display label. Useful when you have multiple environments for different projects or access levels.
    * **Network access**: controls what the session can reach on the internet. The default, `Trusted`, allows connections to [common package registries](/en/claude-code-on-the-web#default-allowed-domains) like npm, PyPI, and RubyGems while blocking general internet access.
    * **Environment variables**: optional variables available in every session, in `.env` format. Don't wrap values in quotes, since quotes are stored as part of the value. These are visible to anyone who can edit this environment.
    * **Setup script**: an optional Bash script that runs before Claude Code launches when a new session is created. Use it to install system tools the cloud VM doesn't include, like `apt install -y gh`, or to start services your project needs. See [Setup scripts](/en/claude-code-on-the-web#setup-scripts) for examples and debugging tips.

    For a first project, leave the defaults and click **Create environment**. You can [edit it later or create additional environments](/en/claude-code-on-the-web#configure-your-environment) for different projects.
  </Step>
</Steps>

### Connect from your terminal

If you already use the GitHub CLI (`gh`), you can set up Claude Code on the web without opening a browser. This requires the [Claude Code CLI](/en/quickstart). `/web-setup` reads your local `gh` token, links it to your Claude account, and creates a default cloud environment if you don't have one.

<Note>
  Organizations with [Zero Data Retention](/en/zero-data-retention) enabled cannot use `/web-setup` or other cloud session features. If the GitHub CLI isn't installed or authenticated, `/web-setup` opens the browser onboarding flow instead.
</Note>

<Steps>
  <Step title="Authenticate with the GitHub CLI">
    In your shell, authenticate the GitHub CLI if you haven't already:

    ```bash theme={null}
    gh auth login
    ```
  </Step>

  <Step title="Sign in to Claude">
    In the Claude Code CLI, run `/login` to sign in with your claude.ai account. Skip this step if you're already signed in.
  </Step>

  <Step title="Run /web-setup">
    In the Claude Code CLI, run:

    ```text theme={null}
    /web-setup
    ```

    This syncs your `gh` token to your Claude account. If you don't have a cloud environment yet, `/web-setup` creates one with Trusted network access and no setup script. You can [edit the environment or add variables](/en/claude-code-on-the-web#configure-your-environment) afterward. Once `/web-setup` completes, you can start cloud sessions from your terminal with [`--remote`](/en/claude-code-on-the-web#from-terminal-to-web) or set up recurring tasks with [`/schedule`](/en/routines).
  </Step>
</Steps>

## Start a task

With GitHub connected and an environment created, you're ready to submit tasks.

<Steps>
  <Step title="Select a repository and branch">
    From [claude.ai/code](https://claude.ai/code) or the Code tab in the Claude mobile app, click the repository selector below the input box and choose a repository for Claude to work in. Each repository shows a branch selector. Change it to start Claude from a feature branch instead of the default. You can add multiple repositories to work across them in one session.
  </Step>

  <Step title="Choose a permission mode">
    The mode dropdown next to the input defaults to **Auto accept edits**, where Claude makes changes and pushes a branch without stopping for approval. Switch to **Plan mode** if you want Claude to propose an approach and wait for your go-ahead before editing files. Cloud sessions don't offer Ask permissions, Auto mode, or Bypass permissions. See [Permission modes](/en/permission-modes) for the full list.
  </Step>

  <Step title="Describe the task and submit">
    Type a description of what you want and press Enter. Be specific:

    * Name the file or function: "Add a README with setup instructions" or "Fix the failing auth test in `tests/test_auth.py`" is better than "fix tests"
    * Paste error output if you have it
    * Describe the expected behavior, not just the symptom

    Claude clones the repositories, runs your setup script if configured, and starts working. Each task gets its own session and its own branch, so you don't need to wait for one to finish before starting another.
  </Step>
</Steps>

## Review and iterate

When Claude finishes, review the changes, leave feedback on specific lines, and keep going until the diff looks right.

<Steps>
  <Step title="Open the diff view">
    A diff indicator shows lines added and removed across the session, for example `+42 -18`. Select it to open the diff view, with a file list on the left and changes on the right.
  </Step>

  <Step title="Leave inline comments">
    Select any line in the diff, type your feedback, and press Enter. Comments queue up until you send your next message, then they're bundled with it. Claude sees "at `src/auth.ts:47`, don't catch the error here" alongside your main instruction, so you don't have to describe where the problem is.
  </Step>

  <Step title="Create a pull request">
    When the diff looks right, select **Create PR** at the top of the diff view. You can open it as a full PR, a draft, or jump to GitHub's compose page with a generated title and description.
  </Step>

  <Step title="Keep iterating after the PR">
    The session stays live after the PR is created. Paste CI failure output or reviewer comments into the chat and ask Claude to address them. To have Claude monitor the PR automatically, see [Auto-fix pull requests](/en/claude-code-on-the-web#auto-fix-pull-requests).
  </Step>
</Steps>

## Troubleshoot setup

### No repositories appear after connecting GitHub

The Claude GitHub App needs explicit access to each repository you want to use. On github.com, open **Settings → Applications → Claude → Configure** and verify your repo is listed under **Repository access**. Private repositories need the same authorization as public ones.

### The page only shows a GitHub login button

Cloud sessions require a connected GitHub account. Connect via the browser flow above, or run `/web-setup` from your terminal if you use the GitHub CLI. If you'd rather not connect GitHub at all, see [Remote Control](/en/remote-control) to run Claude Code on your own machine and monitor it from the web.

### "Not available for the selected organization"

Enterprise organizations may need an admin to enable Claude Code on the web. Contact your Anthropic account team.

### `/web-setup` returns "Unknown command"

`/web-setup` runs inside the Claude Code CLI, not your shell. Launch `claude` first, then type `/web-setup` at the prompt.

If you typed it inside Claude Code and still see the error, your CLI is older than v2.1.80 or you're authenticated with an API key or third-party provider instead of a claude.ai subscription. Run `claude update`, then `/login` to sign in with your claude.ai account.

### "Could not create a cloud environment" or "No cloud environment available" when using `--remote` or ultraplan

Remote-session features create a default cloud environment automatically if you don't have one. If you see "Could not create a cloud environment", automatic creation failed. {/* max-version: 2.1.100 */}If you see "No cloud environment available", your CLI predates automatic creation. In either case, run `/web-setup` in the Claude Code CLI to create one manually, or visit [claude.ai/code](https://claude.ai/code) and follow the **Create your environment** step above.

### Setup script failed

The setup script exited with a non-zero status, which blocks the session from starting. Common causes:

* A package install failed because the registry isn't in your [network access level](/en/claude-code-on-the-web#access-levels). `Trusted` covers most package managers; `None` blocks them all.
* The script references a file or path that doesn't exist in a fresh clone.
* A command that works locally needs a different invocation on Ubuntu.

To debug, add `set -x` at the top of the script to see which command failed. For non-critical commands, append `|| true` so they don't block session start.

### Session keeps running after closing the tab

This is by design. Closing the tab or navigating away doesn't stop the session. It continues running in the background until Claude finishes the current task, then idles. From the sidebar, you can [archive a session](/en/claude-code-on-the-web#archive-sessions) to hide it from your list, or [delete it](/en/claude-code-on-the-web#delete-sessions) to remove it permanently.

## Next steps

Now that you can submit and review tasks, these pages cover what comes next: starting cloud sessions from your terminal, scheduling recurring work, and giving Claude standing instructions.

* [Use Claude Code on the web](/en/claude-code-on-the-web): the full reference, including teleporting sessions to your terminal, setup scripts, environment variables, and network config
* [Routines](/en/routines): automate work on a schedule, via API call, or in response to GitHub events
* [CLAUDE.md](/en/memory): give Claude persistent instructions and context that load at the start of every session
* Install the Claude mobile app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) or [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) to monitor sessions from your phone. From the Claude Code CLI, `/mobile` shows a QR code.
