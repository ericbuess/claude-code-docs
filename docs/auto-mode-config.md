> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configure auto mode

> Tell the auto mode classifier which repos, buckets, and domains your organization trusts. Set environment context, override the default block and allow rules, and inspect your effective config with the auto-mode CLI subcommands.

[Auto mode](/en/permission-modes#eliminate-prompts-with-auto-mode) lets Claude Code run without routine permission prompts by routing tool calls through a classifier that blocks anything irreversible, destructive, or aimed outside your environment. Deny and explicit ask rules are evaluated before the classifier and still block or prompt. Use the `autoMode` settings block to tell that classifier which repos, buckets, and domains your organization trusts, so it stops blocking routine internal operations.

<Note>
  Auto mode is available to all users on the Anthropic API. On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and signed-in [Claude apps gateway](/en/claude-apps-gateway) sessions, you must first [set `CLAUDE_CODE_ENABLE_AUTO_MODE`](/en/permission-modes#enable-auto-mode-on-bedrock-agent-platform-or-foundry). If Claude Code reports auto mode as unavailable for your account, check the [full requirements](/en/permission-modes#eliminate-prompts-with-auto-mode), which also cover the supported models and Owner enablement on Team and Enterprise plans.
</Note>

By default, the classifier trusts only the working directory and the current repo's configured remotes. Actions like pushing to your company's source-control org or writing to a team cloud bucket are blocked until you add them to `autoMode.environment`.

For how to enable auto mode and what it blocks by default, see [Permission modes](/en/permission-modes#eliminate-prompts-with-auto-mode). This page is the configuration reference.

This page covers how to:

* [Choose where to set rules](#where-the-classifier-reads-configuration) across CLAUDE.md, user settings, and managed settings
* [Define trusted infrastructure](#define-trusted-infrastructure) with `autoMode.environment`
* [Override the block and allow rules](#override-the-block-and-allow-rules) when the defaults don't fit your pipeline
* [Route all shell commands through the classifier](#route-all-shell-commands-through-the-classifier) with `autoMode.classifyAllShell`
* [Inspect your effective config](#inspect-the-defaults-and-your-effective-config) with the `claude auto-mode` subcommands
* [Review denials](#review-denials) so you know what to add next

## Where the classifier reads configuration

The classifier reads the same [CLAUDE.md](/en/memory) content Claude itself loads, so an instruction like "never force push" in your project's CLAUDE.md steers both Claude and the classifier at the same time. Start there for project conventions and behavioral rules.

For rules that apply across projects, such as trusted infrastructure or organization-wide deny rules, use the `autoMode` settings block. The classifier reads `autoMode` from the following scopes:

| Scope                          | File                                            | Use for                                              |
| :----------------------------- | :---------------------------------------------- | :--------------------------------------------------- |
| One developer                  | `~/.claude/settings.json`                       | Personal trusted infrastructure                      |
| One project, one developer     | `.claude/settings.local.json`                   | Per-project trusted buckets or services              |
| Organization-wide              | [Managed settings](/en/server-managed-settings) | Trusted infrastructure distributed to all developers |
| `--settings` flag or Agent SDK | Inline JSON                                     | Per-invocation overrides for automation              |

The classifier doesn't read `autoMode` from shared project settings in `.claude/settings.json`, so a checked-in repo can't inject its own allow rules.

Entries from each scope are combined. A developer can extend `environment`, `allow`, `soft_deny`, and `hard_deny` with personal entries but can't remove entries that managed settings provide. Because allow rules act as exceptions to soft block rules inside the classifier, a developer-added `allow` entry can override an organization `soft_deny` entry: the combination is additive, not a hard policy boundary.

<Note>
  The classifier is a second gate that runs after the [permissions system](/en/permissions). For actions that must never run regardless of user intent or classifier configuration, use `permissions.deny` in managed settings, which blocks the action before the classifier is consulted and can't be overridden.
</Note>

## Define trusted infrastructure

For most organizations, `autoMode.environment` is the only field you need to set. It tells the classifier which repos, buckets, and domains are trusted: the classifier uses it to decide what "external" means, so any destination not listed is a potential exfiltration target.

As of Claude Code v2.1.198, `claude auto-mode defaults` prints three kinds of environment entry. Versions before v2.1.195 print only the first five trust slots.

* **Context slots**: describe your organization, stack, and security posture so the classifier reads the other rules in your context. Unlike the other two kinds, context slots have no rules of their own that target them. Each defaults to `None configured` or to the conservative assumption named next to it:
  * **Organization**
  * **Primary use of Claude Code**: defaults to software development
  * **Cloud provider(s)**
  * **Repository visibility**: a repository is assumed private unless its remote host and name indicate otherwise, {/* min-version: 2.1.200 */}or something earlier in the session already showed it is public, such as a `gh repo view` result in the transcript. The transcript-evidence check requires Claude Code v2.1.200 or later
  * **Internal sharing / snippet hosting**: public paste and gist services are treated as outside the trust boundary until you name one
  * **Org-specific CLIs**
  * **Secrets management**
  * **Default / protected branches**: `main` and `master` are treated as protected until you name others
  * **CI/CD deploy targets**
  * **Network posture**
  * **Protected deployment namespaces / environments**: falls back to the Sensitive remote targets heuristic until you name them
  * **Data retention / declassification**
* **Trust slots**: name what the classifier treats as inside your boundary. The slots are Trusted repo, Source control, Trusted internal domains, Trusted cloud buckets, Key internal services, and Internal package registry. The repo and source-control entries default to the working repository and its configured remotes. Every other trust slot defaults to `None configured`, so nothing else is trusted until you add it.
* **Sensitivity slots**: name what the protective rules treat as high-risk. The slots are Sensitive data locations & audiences, Sensitive remote targets, and Protected IaC scopes. Each defaults to a broad heuristic, such as treating any host or namespace whose name carries `prod` or `production` as a sensitive remote target, so the protective rules are active before you configure anything. Naming concrete targets in a sensitivity slot makes those rules apply to the named targets instead of the heuristic.

To add your own entries alongside the defaults, include the literal string `"$defaults"` in the array. The default entries are spliced in at that position, so your custom entries can go before or after them.

The following example keeps the default entries and adds an organization's repos, buckets, domains, and services.

```json theme={null}
{
  "autoMode": {
    "environment": [
      "$defaults",
      "Source control: github.example.com/acme-corp and all repos under it",
      "Trusted cloud buckets: s3://acme-build-artifacts, gs://acme-ml-datasets",
      "Trusted internal domains: *.corp.example.com, api.internal.example.com",
      "Key internal services: Jenkins at ci.example.com, Artifactory at artifacts.example.com"
    ]
  }
}
```

Entries are prose, not regex or tool patterns. The classifier reads them as natural-language rules. Write them the way you would describe your infrastructure to a new engineer. A thorough environment section covers:

* **Organization**: your company name and what Claude Code is primarily used for, like software development, infrastructure automation, or data engineering
* **Source control**: every GitHub, GitLab, or Bitbucket org your developers push to
* **Cloud providers and trusted buckets**: bucket names or prefixes that Claude should be able to read from and write to
* **Trusted internal domains**: hostnames for APIs, dashboards, and services inside your network, like `*.internal.example.com`
* **Key internal services**: CI, artifact registries, internal package indexes, incident tooling
* **Internal package registry**: the private npm, PyPI, or other registry that installs should route through, so installs that bypass it for a public registry get blocked
* **Sensitive data locations & audiences**: the buckets, databases, or paths that hold personal data, confidential business data, credentials, regulated data, or similarly sensitive material, and the audiences that data in each location may be shared with, so the classifier protects those locations instead of guessing from content. {/* min-version: 2.1.195 */}{/* max-version: 2.1.197 */}Claude Code v2.1.195 through v2.1.197 name this entry PII / regulated-data locations and cover only locations that hold personal or regulated data, without the audience dimension
* **Sensitive remote targets**: the namespaces, hosts, or containers that count as production, so remote shells and port-forwards into them need your explicit approval
* **Protected IaC scopes**: the infrastructure resources whose apply or destroy should always require you to name the change
* **Additional context**: regulated-industry constraints, multi-tenant infrastructure, or compliance requirements that affect what the classifier should treat as risky

The Internal package registry, Sensitive data locations & audiences, Sensitive remote targets, and Protected IaC scopes entries require Claude Code v2.1.195 or later. Earlier versions still read them as plain context but don't have the built-in rules that target them.

A useful starting template: fill in the bracketed fields and remove any lines that don't apply.

```json theme={null}
{
  "autoMode": {
    "environment": [
      "$defaults",
      "Organization: {COMPANY_NAME}. Primary use: {PRIMARY_USE_CASE, e.g. software development, infrastructure automation}",
      "Source control: {SOURCE_CONTROL, e.g. GitHub org github.example.com/acme-corp}",
      "Cloud provider(s): {CLOUD_PROVIDERS, e.g. AWS, GCP, Azure}",
      "Trusted cloud buckets: {TRUSTED_BUCKETS, e.g. s3://acme-builds, gs://acme-datasets}",
      "Trusted internal domains: {TRUSTED_DOMAINS, e.g. *.internal.example.com, api.example.com}",
      "Key internal services: {SERVICES, e.g. Jenkins at ci.example.com, Artifactory at artifacts.example.com}",
      "Additional context: {EXTRA, e.g. regulated industry, multi-tenant infrastructure, compliance requirements}"
    ]
  }
}
```

The more specific context you give, the better the classifier can distinguish routine internal operations from exfiltration attempts.

You don't need to fill everything in at once. A reasonable rollout: start with the defaults and add your source control org and key internal services, which resolves the most common false positives like pushing to your own repos. Add trusted domains and cloud buckets next. Fill the rest as blocks come up.

## Override the block and allow rules

Three additional fields let you replace the classifier's built-in rule lists:

* `autoMode.hard_deny`: unconditional security boundaries
* `autoMode.soft_deny`: destructive actions that user intent can clear
* `autoMode.allow`: exceptions to soft block rules

Each is an array of prose descriptions, read as natural-language rules. For tool-pattern-based hard blocks that run before the classifier, use [`permissions.deny`](/en/permissions).

Inside the classifier, precedence works in four tiers:

* `hard_deny` rules block unconditionally. User intent and `allow` exceptions don't apply.
* `soft_deny` rules block next. User intent and `allow` exceptions can override these.
* `allow` rules then override matching `soft_deny` rules as exceptions.
* Explicit user intent overrides the remaining soft blocks: if the user's message directly and specifically describes the exact action Claude is about to take, the classifier allows it even when a `soft_deny` rule matches.

General requests don't count as explicit intent. Asking Claude to "clean up the repo" doesn't authorize force-pushing, but asking Claude to "force-push this branch" does.

To loosen, add to `allow` when the classifier repeatedly flags a routine pattern the default exceptions don't cover. To tighten, add to `soft_deny` for destructive risks specific to your environment that the defaults miss, or to `hard_deny` for security boundaries that must never be crossed.

To keep the built-in rules while adding your own, include the literal string `"$defaults"` in the array. The default rules are spliced in at that position, so your custom rules can go before or after them, and you continue to inherit updates as the built-in list changes across releases.

The following example keeps the defaults in all four lists and adds organization-specific rules to each.

```json theme={null}
{
  "autoMode": {
    "environment": [
      "$defaults",
      "Source control: github.example.com/acme-corp and all repos under it"
    ],
    "allow": [
      "$defaults",
      "Deploying to the staging namespace is allowed: staging is isolated from production and resets nightly",
      "Writing to s3://acme-scratch/ is allowed: ephemeral bucket with a 7-day lifecycle policy"
    ],
    "soft_deny": [
      "$defaults",
      "Never run database migrations outside the migrations CLI, even against dev databases",
      "Never modify files under infra/terraform/prod/: production infrastructure changes go through the review workflow"
    ],
    "hard_deny": [
      "$defaults",
      "Never send repository contents to third-party code-review APIs"
    ]
  }
}
```

<Danger>
  Setting any of `environment`, `allow`, `soft_deny`, or `hard_deny` without `"$defaults"` replaces the entire default list for that section. A `soft_deny` array without `"$defaults"` discards every built-in soft block rule, including force push, `curl | bash`, and production deploys. A `hard_deny` array without `"$defaults"` discards the built-in data exfiltration and auto-mode bypass rules.
</Danger>

Each section is evaluated independently, so setting `environment` alone leaves the default `allow`, `soft_deny`, and `hard_deny` lists intact.

Only omit `"$defaults"` when you intend to take full ownership of the list. To do that safely, run `claude auto-mode defaults` to print the built-in rules, copy them into your settings file, then review each rule against your own pipeline and risk tolerance.

## Route all shell commands through the classifier

By default, narrow Bash and PowerShell allow rules such as `Bash(npm test)` carry over into auto mode and resolve before the classifier runs. Auto mode suspends only the broad rules that grant arbitrary code execution, such as `Bash(*)` or wildcarded interpreters. This means a narrow rule can still let a destructive argument through without the classifier seeing it, for example a script path or flag the rule's prefix didn't anticipate.

Set `autoMode.classifyAllShell` to `true` to suspend every Bash and PowerShell allow rule while auto mode is active, so the classifier evaluates every shell command regardless of your allow list.

```json theme={null}
{
  "autoMode": {
    "classifyAllShell": true
  }
}
```

This trades latency for coverage: a command that an allow rule would have approved instantly now waits for a classifier decision, and each shell command counts as a classifier call.

The setting applies only while auto mode is active, and your allow rules behave normally in other permission modes.

<Note>
  `autoMode.classifyAllShell` requires Claude Code v2.1.193 or later. Earlier versions ignore the key and continue to carry narrow shell allow rules into auto mode.
</Note>

## Inspect the defaults and your effective config

Three CLI subcommands help you inspect and validate your configuration.

Print the built-in `environment`, `allow`, `soft_deny`, and `hard_deny` rules as JSON:

```bash theme={null}
claude auto-mode defaults
```

Print what the classifier actually uses as JSON, with your settings applied where set and defaults otherwise:

```bash theme={null}
claude auto-mode config
```

Get AI feedback on your custom `allow`, `soft_deny`, and `hard_deny` rules:

```bash theme={null}
claude auto-mode critique
```

Run `claude auto-mode config` after saving your settings to confirm the effective rules are what you expect, with `"$defaults"` expanded in place. If you've written custom rules, `claude auto-mode critique` reviews them and flags entries that are ambiguous, redundant, or likely to cause false positives.

If you need to remove or rewrite a built-in rule rather than add alongside it, save the output of `claude auto-mode defaults` to a file, edit the lists, and paste the result into your settings file in place of `"$defaults"`.

## Review denials

When auto mode denies a tool call, the denial is recorded in `/permissions` under the Recently denied tab. Press `r` on a denied action to mark it for retry: when you exit the dialog, Claude Code sends a message telling the model it may retry that tool call and resumes the conversation.

In Claude Code v2.1.193 and later, the classifier's reason for each denial appears alongside the blocked tool call in the transcript, in the denial notification, and under each entry on the Recently denied tab. Use the reason to decide whether the fix is an `environment` entry, an `allow` exception, or retrying with explicit intent in your next message.

Repeated denials for the same destination usually mean the classifier is missing context. Add that destination to `autoMode.environment`, then run `claude auto-mode config` to confirm it took effect.

To react to denials programmatically, use the [`PermissionDenied` hook](/en/hooks#permissiondenied).

## See also

* [Permission modes](/en/permission-modes#eliminate-prompts-with-auto-mode): what auto mode is, what it blocks by default, and how to enable it
* [Managed settings](/en/server-managed-settings): deploy `autoMode` configuration across your organization
* [Permissions](/en/permissions): allow, ask, and deny rules that apply before the classifier runs
* [Settings](/en/settings): the full settings reference, including the `autoMode` key
