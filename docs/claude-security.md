> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Scan your codebase for vulnerabilities

> Install the Claude Security plugin to scan your codebase for vulnerabilities in a Claude Code session and turn findings into patches you review and apply.

The Claude Security plugin runs a multi-agent vulnerability scan of your codebase inside a Claude Code session. [By default](#choose-a-scan-effort), when you scan a whole repository, Claude agents map your architecture, hunt for vulnerabilities, and independently review every finding before writing the report.

Use the plugin to scan a whole repository or [only a set of changes](#scan-only-your-changes), such as a branch's diff, a pull request's diff, or a single commit. Then turn the findings you choose into patches that you review and apply yourself. Scan only code that you own or have permission to test.

Run a scan in your session, your shell, or GitHub Actions:

* **In your session**: [scan and fix your codebase](#scan-and-fix-your-codebase) with [whichever models you have access to in Claude Code](#models-and-providers)
* **From your shell**: use the [`claude-security` command](#scan-from-your-shell)
* **In GitHub Actions**: add the plugin's job to [scan pull requests](#scan-pull-requests-in-github-actions)

A scan in your session or shell counts toward your [usage](https://code.claude.com/docs/en/costs.md), and a scan in GitHub Actions counts toward the account that owns the job's model credential.

> [!NOTE]
>
> If you want a managed service that monitors your repositories, or want to run scans on [Claude Mythos](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5), see the [Claude Security](https://claude.com/product/claude-security) product, available on the Enterprise plan.

The plugin is also distinct from review tools already in Claude Code: the [security guidance plugin](https://code.claude.com/docs/en/security-guidance.md) reviews code as Claude writes it, and [Code Review](https://code.claude.com/docs/en/code-review.md) reviews pull requests. For how the layers stack, see [How the plugin fits with other security tools](#how-the-plugin-fits-with-other-security-tools).

## Prerequisites

To run the plugin, you need:

* A paid plan, Anthropic API access, or a [third-party provider](#models-and-providers), for the [dynamic workflows](https://code.claude.com/docs/en/workflows.md) the scan uses to orchestrate its agents. On Pro, turn them on from the Dynamic workflows row in `/config`.
* Python 3.9 or later available on your `PATH` as `python3`. Check with `python3 --version`. The plugin's tooling uses only the Python standard library.
* Linux, macOS, or Windows.
* Git, for change scans and for turning findings into patches; those jobs don't support other version control systems. A full scan works in any directory, with or without version control.

## Models and providers

The plugin makes no model calls of its own, so a scan in your session needs no separate API key or provider setting.

* **Model**: the agents that hunt for vulnerabilities, verify findings, and write and review patches run on [your session's model](https://code.claude.com/docs/en/sub-agents.md#choose-a-model). To change it, run [`/model`](https://code.claude.com/docs/en/model-config#setting-your-model) in your session before you start a scan. A few supporting steps use the [`sonnet` alias](https://code.claude.com/docs/en/model-config#model-aliases) instead.
* **Provider**: scans run on a paid plan, with Anthropic API access, or on a [third-party provider](https://code.claude.com/docs/en/third-party-integrations.md) such as [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md), [Google Cloud's Agent Platform](https://code.claude.com/docs/en/google-vertex-ai.md), or [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry.md).

On a third-party provider, the `sonnet` alias can resolve to a different version than it does on the Anthropic API. If your account can't use that version, [pin your model versions](https://code.claude.com/docs/en/model-config.md#pin-models-for-third-party-deployments), including `ANTHROPIC_DEFAULT_SONNET_MODEL`.

[Automatic model fallback](https://code.claude.com/docs/en/model-config.md#automatic-model-fallback) re-runs a request that a model's safeguards flag. On Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry, the request can end with a refusal message instead, depending on [how your deployment is set up](https://code.claude.com/docs/en/model-config.md#enable-fallback-on-bedrock-agent-platform-and-foundry).

## Install the plugin

In the VS Code extension or the desktop app, install it by following [Install a plugin](https://code.claude.com/docs/en/plugins/install.md#install-a-plugin).

In a terminal, start Claude Code by running `claude`, then enter this at its prompt to install from the [official Anthropic marketplace](https://code.claude.com/docs/en/plugins/anthropic-marketplaces.md):

```text theme={null}
/plugin install claude-security@claude-plugins-official
```

The command opens the plugin's details, where you choose an [installation scope](https://code.claude.com/docs/en/plugins/install.md#install-a-plugin) to start the install. Choose user scope to have the plugin in every project.

If the install fails, match the message Claude Code reports:

* `Marketplace "claude-plugins-official" not found`: add the marketplace with `/plugin marketplace add anthropics/claude-plugins-official`, then retry the install.
* `Plugin "claude-security" not found in marketplace "claude-plugins-official"`: your local copy of the marketplace catalog may be out of date. Refresh it with `/plugin marketplace update claude-plugins-official`, then retry the install. If the retry prints the same message, see [Plugin not found in marketplace](https://code.claude.com/docs/en/plugins/troubleshooting.md#plugin-not-found-in-marketplace).

Check the install summary. If it reports `Run /reload-plugins to apply.`, see [Apply plugin changes without restarting](https://code.claude.com/docs/en/plugins/cli-reference.md#reload-plugins) to activate the plugin in your current session.

Once the plugin is active, you're ready to [scan and fix your codebase](#scan-and-fix-your-codebase).

### Update the plugin

If a command or option doesn't work, [check](https://code.claude.com/docs/en/plugins/install.md#install-a-plugin) that you have version 0.13.0 or later of the plugin.

To update the plugin yourself, see [Update plugins now](https://code.claude.com/docs/en/plugins/install.md#update-plugins-now). Claude Code also [updates the plugin automatically](https://code.claude.com/docs/en/plugins/install.md#keep-plugins-updated) unless auto-update is turned off.

### Uninstall the plugin

To remove the plugin, uninstall it from the `/plugin` menu, or run `claude plugin uninstall claude-security` in your terminal.

## Scan and fix your codebase

At the Claude Code prompt, `/claude-security` opens a menu of jobs, such as scanning the codebase, scanning a set of changes, and suggesting patches. The happy path runs a full scan, then turns its findings into patches:

**1. Start from a clean working tree**

If you want patches later, commit all your changes and untracked files, or stash them with `git stash -u` from your shell until the scan ends.

**2. Open the Claude Security menu**

Start Claude Code in your repository, run `/claude-security`, and pick **Scan codebase**.

**3. Choose what to scan**

The plugin reads your repository first, then offers the whole repository or a focused area. Pick the whole repository, or answer "I don't know" and the plugin picks a sensible default for your repository's size.

**4. Confirm the run**

A scan may take a while, may use a significant number of tokens, and needs Claude Code left open while it completes. Nothing runs until you confirm.

**5. Read the report**

When the scan starts in a terminal session, the plugin's [live view](#watch-a-running-scan), on by default, opens with a live map of the code. You can also follow each stage with [`/workflows`](https://code.claude.com/docs/en/workflows#watch-the-run) in the terminal. Results are written to a timestamped directory in the folder where you started Claude Code, described in [Read the scan results](#read-the-scan-results).

**6. Turn findings into patches**

Run `/claude-security` again and pick **Suggest patches**, then choose which findings to address. Reviewed patches are written to the report's `patches/` folder; [Fix findings](#fix-findings) covers how each patch is built and reviewed, and what to check afterward.

**7. Apply the patches you accept**

Read each patch's [note](#patches-are-never-applied-automatically), then apply the patch from your shell at the root of your repository with `git apply`, in its own pull request. Patches aren't applied automatically.

You can also ask for a job directly, as arguments to the command, such as `/claude-security scan my branch`. Or ask in plain language, such as "scan the whole repo with the Claude Security plugin". The plugin works best in [auto mode](https://code.claude.com/docs/en/permission-modes.md), which lets the scan proceed without a permission prompt at each step.

### Watch a running scan

When you start a scan in a terminal session, the plugin's [mod](https://code.claude.com/docs/en/plugins/mods/overview.md) opens a live view of the scan in a pane or a band above the prompt. You need Claude Code v2.1.292 or later.

* **Close it**: press `Ctrl+X X` to shrink the pane to a band, and again to hide the band
* **Reopen it**: enter `/claude-security-view` while the scan runs
* **Turn it off**: enter `/plugin configure claude-security` and change **Live scan view**

### Continue a stopped scan

If a scan in your session stops before it writes its report, you can continue it, unless the session says that safeguards stopped one of the scan's agents. In that case, start a new scan instead.

To continue, leave your checkout and the scan's `CLAUDE-SECURITY-<timestamp>/` directory unchanged, and enter `/claude-security continue the scan` in the session that ran it. If you closed that session, [resume it](https://code.claude.com/docs/en/sessions.md#resume-a-session) first.

### Scan only your changes

When your branch has commits its base doesn't, the `/claude-security` menu offers to scan only that diff, so you can check a branch before merging. Before a change scan, commit the edits you want scanned and stash the rest with `git stash -u`, or run a [full scan](#scan-and-fix-your-codebase), which reads the working tree.

To scan one of your open pull requests or a single commit, check it out from your shell first, then ask at the Claude Code prompt:

* **Pull request**: run `git checkout feature-auth`, naming the pull request's branch, then `/claude-security scan my branch`
* **Single commit**: run `git checkout abc1234`, then `/claude-security scan commit abc1234`

### Scope large repositories

On a large repository, scan one area at a time instead of the whole tree. Pick one of the focused scopes the plugin offers, such as your API layer or your authentication code, and the run sizes itself to what you pick. The report's coverage section states what was and wasn't examined. Run another scan on a different area anytime.

### Choose a scan effort

Scan effort sets how deep a scan goes. Your findings go through the same independent verification at `low`, `medium`, and `high`.

* **`low`**: a quick first look. It skips the architecture map when you scan your codebase.
* **`medium`**: the default.
* **`high`**: what `medium` does, plus more hunting for vulnerabilities in the same code.

Name the scan effort in your request at the Claude Code prompt, such as for a part of your codebase or for your changes:

* **Part of your codebase**: `/claude-security scan my public API code at high`
* **Your changes**: `/claude-security scan my branch at high`

If a scan of a large repository finds less than you expect, choose `high` scan effort, scan a second time, or do both. Each can report findings that one `medium` scan doesn't.

A codebase scan can cost a lot of tokens, and the cost grows with the size of the repository, the scan effort, and the model. To spend less, scan a [smaller area](#scope-large-repositories), choose `low`, or [change the model](#models-and-providers) before you start.

### Run a more thorough change scan

Replace the [scan effort](#choose-a-scan-effort) with `--change-scan-effort high`, such as `/claude-security scan my branch --change-scan-effort high`. More agents read the change than at `high` scan effort, so the scan takes longer and costs several times as much. Its report also lists vulnerabilities older than the change.

### Tell a scan about your system

To give a scan facts about your system, name up to 10 files in the folder that you scan or type your own notes.

Give them in your request, or when the scan asks:

```text theme={null}
/claude-security scan this repository, and read docs/arch.md first
```

Give only notes and files that are up to date and that you trust, because a wrong statement can hide a vulnerability. Keep your README and `SECURITY.md` up to date too, because the scan weighs what they say about trusted users and intended behavior.

To [get patches](#scan-and-fix-your-codebase) from this scan, commit the files that you name instead of stashing them.

### Read the scan results

After a scan in your session, find its results in a timestamped `CLAUDE-SECURITY-<timestamp>/` directory in the folder where you started Claude Code:

* **`CLAUDE-SECURITY-RESULTS.md`**: the report, with each finding's ID, such as `F1`, plus its impact, exploit scenario, severity, confidence, and recommendation
* **`CLAUDE-SECURITY-RESULTS.jsonl`**: the same findings in machine-readable form, one JSON object per line
* **`CLAUDE-SECURITY-RESULTS.sarif`**: the same findings as a [SARIF 2.1.0](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html) log for GitHub code scanning and any other tool that reads the standard. The scan classifies findings under their [CWE](https://cwe.mitre.org/) weakness categories
* **`CLAUDE-SECURITY-REVISION-<commit>.json`**: the revision stamp, recording which commit was scanned, at what [scan effort](#choose-a-scan-effort), whether uncommitted changes were part of the scanned tree, and how thoroughly the run was verified. A scan outside version control stamps `UNVERSIONED` in place of the commit

That directory is the only change a scan makes to your checkout, and it carries its own `.gitignore`, so a stray `git add` doesn't sweep a report into a commit. Some packaging and deploy tools don't read that file, so move report directories out while you package or deploy. To keep a report in history for an audit trail, delete that one `.gitignore` file and commit the directory.

Findings only appear in the report after independent verifier agents analyze them, which keeps reports short and worth reading. Scans are nondeterministic: two scans of the same code can surface different findings. Run scans regularly.

## Fix findings

Start the fix flow by picking **Suggest patches** from the `/claude-security` menu, or ask in plain language, such as "fix finding F3", then pick which findings from the report to address. Each patch is drafted in a scratch copy of your repository. An agent can still edit your own files by mistake, so run `git status` when the job ends.

Before delivery, an agent independent of the one that wrote the patch reviews it. It runs your project's tests when it can, and reads the diff on its own terms for anything new it might introduce.

That review has to vouch that the patch:

* Addresses its one finding
* Introduces no new vulnerability
* Leaves behavior otherwise unchanged

When the review can't vouch for all three, the plugin writes a short note explaining why instead of a patch.

### Patch from an older report

You can still use a scan's report after new commits, but only if the scanned commit is in your current history. If it isn't, take the fresh scan that the plugin offers.

### Patches are never applied automatically

Applying a patch is your decision. Patches are written to the report's `patches/` folder, one `F<n>.patch` per patched finding with a note beside it explaining the change. Ask Claude to apply one and open a pull request, or apply it from your shell at the root of your repository.

Read the patch's note, `F<n>.md`, first, because it has the exact command, such as:

```bash theme={null}
git -C "$(git rev-parse --show-toplevel)" apply CLAUDE-SECURITY-<timestamp>/patches/F1.patch
```

Apply each patch in its own pull request so it can be reviewed and tested on its own. If `git apply` refuses a patch, read its note.

## Triage findings you already have

Vulnerability Triage checks whether the findings in a list hold up against your code. The list can be a SARIF 2.1.0 file from another scanner, or the `CLAUDE-SECURITY-<timestamp>/` directory of an earlier scan. Triage only a list from a source that you trust.

If you want patches later, leave nothing uncommitted or untracked but the list itself. Start Claude Code in the directory that the findings' file paths are relative to, usually your repository's root.

Then enter the command with the list's path:

```text theme={null}
/claude-security triage results.sarif
```

The report is `FINDINGS-TRIAGE.md`, in a new `CLAUDE-SECURITY-<timestamp>/` directory. Findings that the triage rejects are under **Not validated**. Check that section yourself, because the triage is more likely to reject a real finding that your list describes in only a few words. `FINDINGS-TRIAGE.sarif` beside the report is your list with the verdicts added.

To turn the report's valid findings into patches, accept the offer at the end of the triage. If you commit, pull, or switch branches first, start a new triage. See [Fix findings](#fix-findings) for what to check after a patch job.

## Create a threat model

The `/claude-security:threat-model` command drafts a threat model, a file that you can give to later scans.

Start Claude Code at the root of your repository and enter:

```text theme={null}
/claude-security:threat-model
```

Claude reads your code and any scan report, then asks about your system and what else it may read: folders, your [connectors](https://code.claude.com/docs/en/mcp.md), or text that you paste.

> [!WARNING]
>
> If you let Claude read your connectors, its search terms leave your machine, and they can include words from that report. Claude can be misled by what it reads there, or by text that you paste.

When Claude shows a draft:

1. Check it before you choose **Yes** to save it as `.claude-security/threat-model.md`, because a wrong statement can hide a vulnerability from a later scan.
2. If there's a scan report, choose whether Claude writes `CLAUDE-SECURITY-PRECONDITIONS.md` in the report's folder. That file says whether each finding's preconditions are `met`, `not met`, or `not shown` in the sources that Claude read.
3. When Claude finishes, enter [`/clear`](https://code.claude.com/docs/en/commands#all-commands) before you run another command of the plugin.

To be sure that a scan reads the threat model, [name it in your request](#tell-a-scan-about-your-system).

## Analyze your attack surface

An attack surface analysis examines the parts of your project that an attacker can reach, and proposes changes to shrink that attack surface.

Start Claude Code at the root of your repository, in [auto mode](https://code.claude.com/docs/en/permission-modes.md#switch-permission-modes) where it's [available](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode), and enter:

```text theme={null}
/claude-security:attack-surface-analysis
```

An analysis may take a long time and use a significant number of tokens. Until it ends, leave Claude Code open, and don't commit, switch branches, or edit files.

An analysis doesn't replace a [scan](#scan-and-fix-your-codebase), which looks for vulnerabilities. The analysis looks for:

* Code that the default configuration reaches but no default feature uses
* Sensitive code reachable before login or without any user action
* Combinations of options that silently turn off a security feature

The report is `CLAUDE-SECURITY-<timestamp>/CLAUDE-SECURITY-RESULTS.md`, in the folder where you started Claude Code. If the analysis wrote patches, `attack-surface-patches/PATCHES.md` beside it describes them. Treat findings and patches as untested until you check them yourself.

## Scan from your shell

The `claude-security` command scans the folder that you run it in, and writes the [same report](#read-the-scan-results) there. The scan runs inside the [plugin's sandbox](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-security/README.md#running-in-a-sandbox). It signs in with your Claude Code login or your provider's environment variables.

The sandbox runs only on Linux:

* **Linux**: you need kernel 5.19 or later on x86-64 or arm64, Python 3.10 or later, and a user other than root. On Ubuntu 24.04 or later, add `--sudo`, which sets up the sandbox with `sudo`. If your system doesn't meet these requirements, [scan in a session](#scan-and-fix-your-codebase).
* **Windows**: add `--no-sandbox`, or the command stops
* **macOS and WSL 2**: the command isn't supported, so [scan in a session](#scan-and-fix-your-codebase)

> [!WARNING]
>
> The command doesn't load your repository's `.claude/` settings or hooks, so the deny rules there don't apply. In the sandbox, your organization's [server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md#security-considerations) don't apply either. If you add `--no-sandbox`, the scan runs in [auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode) with your user's access. See the plugin's [trust model](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-security/SECURITY.md#trust-model).

The plugin includes the command. To add it to your `PATH`, enter `/claude-security:install-cli` in Claude Code and follow what it prints.

Then run it in your repository, with `--sudo` or `--no-sandbox` if your system needs it:

* **Scan the codebase**: `claude-security`
* **Scan this branch's changes**: `claude-security --changes`
* **Scan with a full-screen view**: `claude-security --tui`, which needs Node.js 18 or later
* **List the other options**: `claude-security --help`

The command runs in [auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode), and stops if auto mode isn't available. If your Claude Code model doesn't support it, add `--model` with one that does. For any other cause, [scan in a session](#scan-and-fix-your-codebase).

## Scan pull requests in GitHub Actions

On a pull request, the plugin's GitHub Actions job scans the change, posts a review and suggested fixes, and can block the merge. It can also scan the whole repository on a schedule.

> [!WARNING]
>
> Use the job only in a repository where you trust everyone who can push. Anyone who adds text or code to a pull request's branch can steer the scan, have it run that code, and make it send model requests on the job's credential. By default, the job fails for a pull request from a fork.
>
> In a public repository, the review, the job summary, or the job's report artifact can disclose a live vulnerability. To keep findings private, [scan in your session](#scan-only-your-changes) instead.

The job needs a GitHub-hosted Linux runner on GitHub.com, and [Anthropic API access](https://platform.claude.com/docs/en/get-api-key) or a [third-party provider](https://code.claude.com/docs/en/third-party-integrations.md), because it can't sign in with a paid plan. Follow the plugin's [GitHub Actions guide](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-security/CI.md) to add the workflow and create a credential for this job alone. To move to version 0.13.0, put its commit after the `@` in each workflow: `d0d514288960e7a78e1a76e4a3ec694416458726`.

With the guide's sample workflow, a draft pull request from a branch of your repository passes with no scan until you mark it ready for review. A pull request from Dependabot passes with no scan too, so review its changes yourself.

## How the plugin fits with other security tools

The Claude Security plugin is the deep-scan layer in a defense-in-depth stack, alongside the [security guidance plugin](https://code.claude.com/docs/en/security-guidance.md), [Code Review](https://code.claude.com/docs/en/code-review.md), the managed [Claude Security](https://claude.com/product/claude-security) product, and your existing scanners:

| Stage | Tool | What it covers |
| :- | :- | :- |
| In session | [Security guidance plugin](https://code.claude.com/docs/en/security-guidance.md) | Common vulnerabilities in code Claude writes, fixed in the same session |
| On demand, deep scan | Claude Security plugin | Multi-agent scan of a repository or diff, with independently reviewed findings and patches |
| On pull request | [Code Review](https://code.claude.com/docs/en/code-review.md), Team and Enterprise plans | Multi-agent correctness and security review with full codebase context |
| On pull request, deep scan | [Claude Security plugin in GitHub Actions](#scan-pull-requests-in-github-actions) | Multi-agent scan of the pull request's changes |
| Managed | [Claude Security](https://claude.com/product/claude-security), Enterprise plan | Hosted scanning that monitors connected repositories |
| In CI | Your existing static analysis and dependency scanners | Language-specific rules, supply-chain checks, and policy enforcement |

The plugin doesn't replace your existing source-code security tools. Run it alongside static analysis, dependency scanning, and code review: it reasons about your code the way a human security researcher would, which complements the deterministic checks those tools provide.

If your organization uses the managed Claude Security product, `/claude-security:hosted` shows its findings in your session. Before you use it, read the [requirements](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-security/README.md#findings-from-hosted-claude-security) and the [risks](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-security/SECURITY.md#findings-from-hosted-claude-security).

## Troubleshooting

**The `/claude-security` menu opens with a Python warning.** The plugin needs `python3` 3.9 or later on your `PATH`. When it can't find `python3` at all, the menu warns that Claude Security won't work until one is installed; when the first `python3` on your `PATH` is older, the warning names the version it found. Install Python 3, or put a newer `python3` first on your `PATH`, then start a new session.

**You may see a "safeguards flagged this message" notice when scanning on a Fable model.** The message names the model you're running. Fable's cybersecurity safety classifiers flag certain requests, and Claude Code re-runs a flagged request on an Opus model through [automatic model fallback](https://code.claude.com/docs/en/model-config.md#automatic-model-fallback). This is expected. When the request re-runs, the scan should still complete successfully. If the scan stops, see [Continue a stopped scan](#continue-a-stopped-scan).

## Related resources

To go deeper on the pieces this page touches:

* [Security guidance plugin](https://code.claude.com/docs/en/security-guidance.md): catch issues in code as Claude writes it, in the same session
* [Code Review](https://code.claude.com/docs/en/code-review.md): set up the PR-time multi-agent review
* [Claude Security](https://claude.com/product/claude-security): the managed service that monitors connected repositories
* [Claude Code security](https://code.claude.com/docs/en/security.md): how Claude Code approaches trust, permissions, and safeguards
* [Install and manage plugins](https://code.claude.com/docs/en/plugins/install.md): find and install other plugins from the official marketplace
