> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Scan your codebase for vulnerabilities

> Install the Claude Security plugin to scan your codebase for vulnerabilities in a Claude Code session and turn findings into patches you review and apply.

The Claude Security plugin runs a multi-agent vulnerability scan of your codebase inside a Claude Code session. A team of Claude agents maps your architecture, builds a threat model, hunts for vulnerabilities, and independently reviews every finding before writing the report. Use the plugin to scan a whole repository or [only a set of changes](#scan-only-your-changes), such as a branch's diff, a pull request's diff, or a single commit, then turn the findings you choose into patches that you review and apply yourself.

The plugin runs locally in your session, and each scan counts against your plan's usage limits. If you want a managed service that monitors your repositories, see the [Claude Security](https://claude.com/product/claude-security) product, available on the Enterprise plan. The plugin reaches code the managed product can't reach, such as repositories hosted on GitLab or Bitbucket, or on networks that don't allow inbound connections.

The plugin is also distinct from the review tools already in Claude Code: the [security guidance plugin](/docs/en/security-guidance) reviews code as Claude writes it, [`/security-review`](/docs/en/commands#all-commands) runs a single pass over your branch, and [Code Review](/docs/en/code-review) reviews pull requests. For how the layers stack, see [How the plugin fits with other security tools](#how-the-plugin-fits-with-other-security-tools).

## Prerequisites

To run the plugin, you need:

* {/* min-version: 2.1.154 */}Claude Code v2.1.154 or later on a paid plan, for the [dynamic workflows](/docs/en/workflows) the scan uses to orchestrate its agents. On Pro, turn them on from the Dynamic workflows row in `/config`.
* Python 3.9.6 or later available on your `PATH` as `python3`. Check with `python3 --version`. The plugin's tooling uses only the Python standard library, so nothing is installed.
* Linux, macOS, or Windows.
* Git, for change scans and for turning findings into patches; those jobs don't support other version control systems. A full scan works in any directory, with or without version control.

## Install the plugin

In a Claude Code session, install from the [official Anthropic marketplace](/docs/en/discover-plugins#official-anthropic-marketplace):

```text theme={null}
/plugin install claude-security@claude-plugins-official
```

<Note>
  If Claude Code reports that the marketplace is not found, run `/plugin marketplace add anthropics/claude-plugins-official` first, then retry the install.
</Note>

Then activate the plugin in the current session with `/reload-plugins`, which applies pending plugin changes without a restart:

```text theme={null}
/reload-plugins
```

The plugin is now active, and you're ready to [scan and fix your codebase](#scan-and-fix-your-codebase).

### Uninstall the plugin

To remove the plugin, uninstall it from the `/plugin` menu, or run `claude plugin uninstall claude-security` in your terminal.

## Scan and fix your codebase

The plugin adds one command, `/claude-security`, which opens a menu of its three jobs: scanning the codebase, scanning a set of changes, and suggesting patches. The happy path runs a full scan, then turns its findings into patches:

<Steps>
  <Step title="Open the Claude Security menu">
    Run `/claude-security` and pick **Scan codebase**.
  </Step>

  <Step title="Choose what to scan">
    The plugin reads your repository first, then offers the whole repository or a focused area, with each option's file count and relative cost stated. Pick the whole repository, or answer "I don't know" and the plugin picks a sensible default for your repository's size.
  </Step>

  <Step title="Confirm the run">
    A scan may take a while, may use a significant number of tokens, and needs Claude Code left open while it completes. Nothing runs until you confirm.
  </Step>

  <Step title="Read the report">
    While the scan runs, it reports each stage as it starts, with the detail available under [`/workflows`](/docs/en/workflows). Results land in a timestamped directory in your repository, described in [Read the scan results](#read-the-scan-results).
  </Step>

  <Step title="Turn findings into patches">
    Run `/claude-security` again and pick **Suggest patches**, then choose which findings to address. Reviewed patches land in the report's `patches/` folder; [Fix findings](#fix-findings) covers how each patch is built and reviewed.
  </Step>

  <Step title="Apply the patches you accept">
    Apply each patch from your shell with `git apply`, in its own pull request. Patches are never applied automatically.
  </Step>
</Steps>

You don't have to start from the menu: ask for a job directly, as arguments to the command, such as `/claude-security scan my branch`, or in plain language, such as "scan commit abc1234". The plugin works best in [auto mode](/docs/en/permission-modes), which lets the scan's agents proceed without a permission prompt at each step; the plugin reminds you how to enable it when a job starts.

### Scan only your changes

When your branch has commits its base doesn't, the `/claude-security` menu offers to scan only that diff, so you can check a branch before merging. You can also scan one of your open pull requests, or a single commit by asking for it, such as "scan commit abc1234". Only committed changes are scanned: commit or stash in-progress edits first, or run a full scan, which reads the working tree.

Change scans need a git repository; full scans of an unversioned directory still work. Finding your open pull requests is the one step that reaches the network, and it's offered only when your session already has permission to run the GitHub CLI and `gh` is signed in.

### Scope large repositories

On a large repository, scan one area at a time instead of the whole tree. Pick one of the focused scopes the plugin offers, such as your API layer or your authentication code, and the run sizes itself to what you pick. The report's coverage section states what was and wasn't examined. Run another scan on a different area anytime.

### Read the scan results

Every scan writes its results into a timestamped `CLAUDE-SECURITY-<timestamp>/` directory in your repository:

* **`CLAUDE-SECURITY-RESULTS.md`**: the report, with each finding's ID, such as `F1`, plus its impact, exploit scenario, severity, confidence, and recommendation
* **`CLAUDE-SECURITY-RESULTS.jsonl`**: the same findings in machine-readable form, one JSON object per line
* **`CLAUDE-SECURITY-REVISION-<commit>.json`**: the revision stamp, recording which commit was scanned, at what effort, whether uncommitted changes were part of the scanned tree, and how thoroughly the run was verified, so a report is always tied to the code it describes. A scan outside version control stamps `UNVERSIONED` in place of the commit

That directory is the only change a scan makes to your checkout, and it carries its own `.gitignore`, so a stray `git add` never sweeps a report into a commit. To keep a report in history for an audit trail, delete that one `.gitignore` file and commit the directory like any other.

Findings only appear in the report after independent verifier agents analyze them, which keeps reports short and worth reading. Scans are nondeterministic: two scans of the same code can surface different findings. Run scans regularly, and use the revision stamps to attribute each report to the exact code and settings it covered.

## Fix findings

Start the fix flow by picking **Suggest patches** from the `/claude-security` menu, or ask in plain language, such as "fix finding F3", then pick which findings from the report to address. Patches are built against committed code, and the report has to still describe the code you have: findings whose code has since changed are skipped with a note, and the plugin offers a fresh scan instead of patching from a stale report. Each patch is drafted in a scratch copy of your repository, so your source files stay untouched until you apply a patch yourself.

Before delivery, each patch is reviewed by an agent independent of the one that wrote it, which runs your project's tests against the change when the code has them and reads the diff on its own terms for anything new it might introduce. A patch is written only when that review can vouch that the change addresses the one finding, introduces no new vulnerability, and leaves behavior otherwise unchanged. When it can't vouch for all three, you get a short note explaining why instead of a patch.

### Patches are never applied automatically

Applying a patch is always your decision. Patches land in the report's `patches/` folder, one `F<n>.patch` per finding with a note beside it explaining the change. Apply one from your shell, or ask Claude to apply it and open a pull request:

```bash theme={null}
git apply CLAUDE-SECURITY-<timestamp>/patches/F1.patch
```

When the patched code has no tests, the patch's note says so, so you know its review ran without a test pass. Apply each patch in its own pull request so it can be reviewed and tested on its own.

## How the plugin fits with other security tools

The Claude Security plugin is the on-demand deep-scan layer in a defense-in-depth stack, alongside the [security guidance plugin](/docs/en/security-guidance), [`/security-review`](/docs/en/commands#all-commands), [Code Review](/docs/en/code-review), the managed [Claude Security](https://claude.com/product/claude-security) product, and your existing scanners:

| Stage                  | Tool                                                                           | What it covers                                                                             |
| :--------------------- | :----------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- |
| In session             | [Security guidance plugin](/docs/en/security-guidance)                              | Common vulnerabilities in code Claude writes, fixed in the same session                    |
| On demand, single pass | [`/security-review`](/docs/en/commands#all-commands)                                | One-time security pass on the current branch                                               |
| On demand, deep scan   | Claude Security plugin                                                         | Multi-agent scan of a repository or diff, with independently reviewed findings and patches |
| On pull request        | [Code Review](/docs/en/code-review), Team and Enterprise plans                      | Multi-agent correctness and security review with full codebase context                     |
| Managed                | [Claude Security](https://claude.com/product/claude-security), Enterprise plan | Hosted scanning that monitors connected repositories                                       |
| In CI                  | Your existing static analysis and dependency scanners                          | Language-specific rules, supply-chain checks, and policy enforcement                       |

The plugin doesn't replace your existing source-code security tools. Run it alongside static analysis, dependency scanning, and code review: it reasons about your code the way a human security researcher would, which complements the deterministic checks those tools provide.

## Troubleshooting

**The `/claude-security` menu opens with a Python warning.** The plugin needs `python3` 3.9.6 or later on your `PATH`. When it can't find `python3` at all, the menu warns that Claude Security won't work until one is installed; when the first `python3` on your `PATH` is older, the warning names the version it found. Install Python 3, or put a newer `python3` first on your `PATH`, then start a new session.

## Related resources

To go deeper on the pieces this page touches:

* [Security guidance plugin](/docs/en/security-guidance): catch issues in code as Claude writes it, in the same session
* [Code Review](/docs/en/code-review): set up the PR-time multi-agent review
* [Claude Security](https://claude.com/product/claude-security): the managed service that monitors connected repositories
* [Claude Code security](/docs/en/security): how Claude Code approaches trust, permissions, and safeguards
* [Discover and install plugins](/docs/en/discover-plugins#official-anthropic-marketplace): browse other official plugins
