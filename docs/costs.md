> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Manage costs effectively

> Track token usage, set team spend limits, and reduce Claude Code costs with context management, model selection, extended thinking settings, and preprocessing hooks.

Claude Code charges by API token consumption. For subscription plan pricing (Pro, Max, Team, Enterprise), see [claude.com/pricing](https://claude.com/pricing). Per-developer costs vary widely based on model selection, codebase size, and usage patterns such as running multiple instances or automation.

Across enterprise deployments, the average cost is around \$13 per developer per active day and \$150-250 per developer per month, with costs remaining below \$30 per active day for 90% of users. To estimate spend for your own team, start with a small pilot group and use the tracking tools below to establish a baseline before wider rollout.

This page covers how to [track your costs](#track-your-costs), [manage costs for your organization](#manage-costs-for-your-organization), and [reduce token usage](#reduce-token-usage).

## Track your costs

### Using the `/usage` command

<Note>
  The Session block in `/usage` shows API token usage and is intended for API users. Claude Max and Pro subscribers have usage included in their subscription, so the session cost figure isn't relevant for billing purposes. Subscribers see plan usage bars, activity stats, and a usage breakdown on the same screen.
</Note>

The Session block at the top of `/usage` shows detailed token usage statistics for your current session. The dollar figure is an estimate computed locally from token counts and may differ from your actual bill. For authoritative billing, see the Usage page in the [Claude Console](https://platform.claude.com/usage).

```text theme={null}
Total cost:            $0.55
Total duration (API):  6m 19.7s
Total duration (wall): 6h 33m 10.2s
Total code changes:    0 lines added, 0 lines removed
```

On a Pro, Max, Team, or Enterprise plan, `/usage` also shows a breakdown of what counts against your plan limits. It attributes recent usage to skills, subagents, plugins, and individual MCP servers, with each shown as a percentage of the total. Press `d` or `w` to switch between the last 24 hours and the last 7 days. The figures are approximate and computed from local session history on this machine, so usage from other devices or claude.ai is not included.

In the [VS Code extension](/en/vs-code#check-account-and-usage), the same breakdown appears in the Account & usage dialog with a Day and Week toggle. Requires Claude Code v2.1.174 or later.

### Set a spend limit on Pro and Max

On Pro and Max plans, the `/usage-credits` command opens a dialog in the CLI where you manage [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans). From the dialog you can:

* Turn on usage credits for your account
* Buy more usage credits, either a listed bundle or a custom amount
* Set, change, or remove your monthly spend limit
* Configure auto-reload, which buys more usage credits automatically when your balance falls below a threshold you set

On Claude Code versions before v2.1.207 and on accounts where the in-CLI dialog isn't available, `/usage-credits` opens the usage-credits billing page in your browser instead. On Team and Enterprise plans, members with billing access get the same browser page, and members without billing access send a request from the CLI asking their admin to turn on usage credits or raise the limit.

Changing the monthly spend limit requires billing access on the account. If you reach the limit while you still have usage credits available, Claude Code prompts you to raise or remove it so you can continue without leaving the CLI.

Amounts you type into the dialog, such as a custom purchase amount, the monthly spend limit, or the auto-reload threshold and target, must be digits, optionally followed by a period and one or two decimal digits, for example `20` or `20.50`. Any other input, including commas, shows an inline error and isn't saved. Versions before v2.1.207 don't show the dialog and open the billing page instead.

Claude Code asks you to type `yes` before applying an amount above \$1,000, or above 1,000 units of a non-US-dollar billing currency. A purchase whose post-tax total crosses that threshold requires the same confirmation, even when the amount you typed is below it.

## Manage costs for your organization

Which controls you have depends on how your organization accesses Claude Code: a Claude for Teams or Enterprise plan, the Claude Console, or a cloud provider. On Teams and Enterprise plans, usage draws from each member's seat allowance. On the Console and on cloud providers, usage is billed per token to your organization. If your organization mixes sign-in methods, each developer is metered according to the one they authenticated with.

The table maps each setup to where you see spend, where you cap it, and how you pull per-user numbers.

| Your setup                                                                              | See spend                                                                                                                           | Cap spend                      | Per-user reporting                                                                                                                                                                                                        |
| :-------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- | :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Claude for Teams or Enterprise](#claude-for-teams-and-enterprise)                      | [Spend report in org analytics](https://support.claude.com/en/articles/12883420-view-usage-analytics-for-team-and-enterprise-plans) | Spend limits in admin settings | [Spend report CSV](https://support.claude.com/en/articles/12883420-view-usage-analytics-for-team-and-enterprise-plans); [Enterprise Analytics API](https://platform.claude.com/docs/en/api/admin/analytics) on Enterprise |
| [Claude Console (API)](#claude-console)                                                 | [Console usage page](https://platform.claude.com/usage)                                                                             | Workspace spend limits         | [Console dashboard](https://platform.claude.com/claude-code), [Claude Code Analytics API](https://platform.claude.com/docs/en/build-with-claude/claude-code-analytics-api)                                                |
| [Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry](#cloud-providers) | Your cloud billing console                                                                                                          | Your cloud's budget controls   | [OpenTelemetry](/en/monitoring-usage) or an [LLM gateway](/en/llm-gateway)                                                                                                                                                |

[OpenTelemetry export](/en/monitoring-usage) works on every setup and is the only option that streams per-user token and cost metrics into your own observability stack in near real time.

### Claude for Teams and Enterprise

On Claude for Teams and Enterprise plans, each member's Claude Code usage draws from a per-seat allowance that resets on a rolling five-hour window and a weekly window. The allowance is shared with Claude chat and Cowork, and its size depends on the member's [seat tier](https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan) (Standard or Premium). Your controls live in the claude.ai admin console, not the Claude Console.

* **See spend**: the [spend report in org analytics](https://support.claude.com/en/articles/12883420-view-usage-analytics-for-team-and-enterprise-plans) shows estimated spend per user and per model, with CSV export, updated daily. The report covers usage-credit spend and appears once usage credits are turned on. Usage inside the seat allowance isn't metered in dollars.
* **See adoption**: the [analytics dashboard](https://claude.ai/analytics/claude-code) shows daily active users, sessions, and contribution metrics, with CSV export of contribution data. See [track team usage with analytics](/en/analytics).
* **Cap spend**: the seat allowance is the default ceiling. To let members continue past it, turn on [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) and set spend limits at the organization, group, or individual member level.
* **Pull per-user numbers**: on the Enterprise plan, the [Enterprise Analytics API](https://platform.claude.com/docs/en/api/admin/analytics) returns per-user usage and cost reports across Claude surfaces, including Claude Code. A Primary Owner creates a key with the `read:analytics` scope at [claude.ai/analytics/api-keys](https://claude.ai/analytics/api-keys). On the Teams plan, export the [spend report CSV](https://support.claude.com/en/articles/12883420-view-usage-analytics-for-team-and-enterprise-plans), which lists token usage and estimated spend per user and per model.

The [Claude Enterprise consumption guide](https://support.claude.com/en/articles/14782391-claude-enterprise-consumption-guide) is the planning reference for admins. It explains how consumption differs across Claude chat, Claude Code, and Cowork, and gives per-user dollar starting points for budgeting. Budget more for a coding seat than a chat seat: each Claude Code turn carries file contents, tool calls, and multi-step reasoning, so one debugging session can consume more than a day of chat.

### Claude Console

API organizations manage Claude Code spend through [workspaces](https://platform.claude.com/docs/en/build-with-claude/workspaces). You can [set workspace spend limits](https://platform.claude.com/docs/en/build-with-claude/workspaces#workspace-limits) on total Claude Code spend and [view cost and usage reporting](https://platform.claude.com/docs/en/build-with-claude/workspaces#usage-and-cost-tracking) in the Console.

<Note>
  When you first authenticate Claude Code with your Claude Console account, a workspace called "Claude Code" is automatically created for you. This workspace provides centralized cost tracking and management for all Claude Code usage in your organization. You cannot create API keys for this workspace; it is exclusively for Claude Code authentication and usage.

  For organizations with custom rate limits, Claude Code traffic in this workspace counts toward your organization's overall API rate limits. You can set a [workspace rate limit](https://platform.claude.com/docs/en/api/rate-limits#setting-lower-limits-for-workspaces) on this workspace's Limits page in the Claude Console to cap Claude Code's share and protect other production workloads.
</Note>

For per-user reporting, the [Console dashboard](https://platform.claude.com/claude-code) shows spend and accepted lines per member, and the [Claude Code Analytics API](https://platform.claude.com/docs/en/build-with-claude/claude-code-analytics-api) returns the same daily per-user metrics programmatically with an [Admin API key](https://platform.claude.com/settings/admin-keys). See [analytics for API customers](/en/analytics#access-analytics-for-api-customers).

#### Rate limit recommendations

When setting up Claude Code for teams, consider these Token Per Minute (TPM) and Request Per Minute (RPM) per-user recommendations based on your organization size:

| Team size     | TPM per user | RPM per user |
| ------------- | ------------ | ------------ |
| 1-5 users     | 200k-300k    | 5-7          |
| 5-20 users    | 100k-150k    | 2.5-3.5      |
| 20-50 users   | 50k-75k      | 1.25-1.75    |
| 50-100 users  | 25k-35k      | 0.62-0.87    |
| 100-500 users | 15k-20k      | 0.37-0.47    |
| 500+ users    | 10k-15k      | 0.25-0.35    |

For example, if you have 200 users, you might request 20k TPM for each user, or 4 million total TPM (200\*20,000 = 4 million).

The TPM per user decreases as team size grows because fewer users tend to use Claude Code concurrently in larger organizations. These rate limits apply at the organization level, not per individual user, which means individual users can temporarily consume more than their calculated share when others aren't actively using the service.

<Note>
  If you anticipate scenarios with unusually high concurrent usage (such as live training sessions with large groups), you may need higher TPM allocations per user.
</Note>

### Cloud providers

On Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry, Claude Code is billed per token to your cloud account, and spend controls live in your cloud provider's billing console. Claude Code does not send metrics from your cloud back to Anthropic, so the [analytics dashboards](/en/analytics) and the Claude Code Analytics API do not cover this usage.

For per-user cost attribution, you have three options:

* **OpenTelemetry**: [export metrics](/en/monitoring-usage) from each developer's machine to your own observability stack. This gives you per-user token counts, costs, and tool activity regardless of provider.
* **A Claude apps gateway**: a self-hosted [Claude apps gateway](/en/claude-apps-gateway) provides per-user usage attribution, OTLP metrics with token counts, and [per-user spend limits](/en/claude-apps-gateway-spend-limits) on these providers.
* **An LLM gateway**: route all Claude Code traffic through a proxy that tracks spend per key. Several large enterprises reported using [LiteLLM](/en/llm-gateway), an open-source tool that [tracks spend by key](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend). This project is unaffiliated with Anthropic and has not been audited for security.

### When a developer asks about a limit

Developers usually bring limit questions to their admin, so it helps to know which ceiling they hit. The three situations mean different things:

* **"You've hit your session limit" or "You've hit your weekly limit"**: a seat-based usage window on a subscription plan. These windows are shared across all models, so switching models with `/model` doesn't restore access, though it does keep the developer working after the model-specific "You've hit your Opus limit" message. The message shows when the window resets, and the developer can run `/usage-credits` to request usage beyond the allowance if you have [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) turned on. See [usage limit errors](/en/errors#youve-hit-your-session-limit).
* **A context or auto-compact warning**: not a usage limit. The conversation has grown close to the model's maximum input size, and Claude Code summarizes older history to free space. Point the developer at [reduce token usage](#reduce-token-usage).
* **Unexpectedly high spend on an API or cloud-provider plan**: usually traces back to long sessions that were never cleared or to Opus left as the default model. The highest-impact habits to share are clearing between unrelated tasks and matching the model to the job, both covered in [reduce token usage](#reduce-token-usage).

### Agent team token costs

[Agent teams](/en/agent-teams) spawn multiple Claude Code instances, each with its own context window. Token usage scales with the number of active teammates and how long each one runs.

To keep agent team costs manageable:

* Use Sonnet for teammates. It balances capability and cost for coordination tasks.
* Keep teams small. Each teammate runs its own context window, so token usage is roughly proportional to team size.
* Keep spawn prompts focused. Teammates load CLAUDE.md, MCP servers, and skills automatically, but everything in the spawn prompt adds to their context from the start.
* Shut down teammates when their work is done. Each active teammate continues consuming tokens until it exits or the session ends.
* Agent teams are disabled by default. Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in your [settings.json](/en/settings) or environment to enable them. See [enable agent teams](/en/agent-teams#enable-agent-teams).

## Reduce token usage

Token costs scale with context size: the more context Claude processes, the more tokens you use. Claude Code automatically optimizes costs through [prompt caching](/en/prompt-caching), which reduces costs for repeated content like system prompts, and auto-compaction, which summarizes conversation history when approaching context limits.

The following strategies help you keep context small and reduce per-message costs.

### Manage context proactively

Use `/usage` to check your current token usage, or [configure your status line](/en/statusline#context-window-usage) to display it continuously.

* **Clear between tasks**: Use `/clear` to start fresh when switching to unrelated work. Stale context wastes tokens on every subsequent message. Use `/rename` before clearing so you can easily find the session later, then `/resume` to return to it.
* **Add custom compaction instructions**: `/compact Focus on code samples and API usage` tells Claude what to preserve during summarization.

You can also customize compaction behavior in your CLAUDE.md file at the root of your project:

```markdown theme={null}
# Compact instructions

When you are using compact, please focus on test output and code changes
```

### Choose the right model

Sonnet handles most coding tasks well and costs less than Opus. Reserve Opus for complex architectural decisions or multi-step reasoning. Use `/model` to switch models mid-session, or set a default in `/config`. For simple subagent tasks, specify `model: haiku` in your [subagent configuration](/en/sub-agents#choose-a-model).

### Reduce MCP server overhead

MCP tool definitions are [deferred by default](/en/mcp#scale-with-mcp-tool-search), so only tool names enter context until Claude uses a specific tool. Run `/context` to see what's consuming space.

* **Prefer CLI tools when available**: Tools like `gh`, `aws`, `gcloud`, and `sentry-cli` are still more context-efficient than MCP servers because they don't add any per-tool listing. Claude can run CLI commands directly.
* **Disable unused servers**: Run `/mcp` to see configured servers and disable any you're not actively using.

### Install code intelligence plugins for typed languages

[Code intelligence plugins](/en/discover-plugins#code-intelligence) give Claude precise symbol navigation instead of text-based search, reducing unnecessary file reads when exploring unfamiliar code. A single "go to definition" call replaces what might otherwise be a grep followed by reading multiple candidate files. Installed language servers also report type errors automatically after edits, so Claude catches mistakes without running a compiler.

### Offload processing to hooks and skills

Custom [hooks](/en/hooks) can preprocess data before Claude sees it. Instead of Claude reading a 10,000-line log file to find errors, a hook can grep for `ERROR` and return only matching lines, reducing context from tens of thousands of tokens to hundreds.

A [skill](/en/skills) can give Claude domain knowledge so it doesn't have to explore. For example, a "codebase-overview" skill could describe your project's architecture, key directories, and naming conventions. When Claude invokes the skill, it gets this context immediately instead of spending tokens reading multiple files to understand the structure.

For example, this PreToolUse hook filters test output to show only failures:

<Tabs>
  <Tab title="settings.json">
    Add this to your [settings.json](/en/settings#settings-files) to run the hook before every Bash command:

    ```json theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "~/.claude/hooks/filter-test-output.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="filter-test-output.sh">
    The hook calls this script. Create the folder with `mkdir -p ~/.claude/hooks`, save the script below as `~/.claude/hooks/filter-test-output.sh`, and make it executable with `chmod +x ~/.claude/hooks/filter-test-output.sh`. It checks if the command is a test runner and modifies it to show only failures:

    ```bash theme={null}
    #!/bin/bash
    input=$(cat)
    cmd=$(echo "$input" | jq -r '.tool_input.command')

    # If running tests, filter to show only failures
    if [[ "$cmd" =~ ^(npm test|pytest|go test) ]]; then
      filtered_cmd="$cmd 2>&1 | grep -A 5 -E '(FAIL|ERROR|error:)' | head -100"
      echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"updatedInput\":{\"command\":\"$filtered_cmd\"}}}"
    else
      echo "{}"
    fi
    ```
  </Tab>
</Tabs>

### Move instructions from CLAUDE.md to skills

Your [CLAUDE.md](/en/memory) file is loaded into context at session start. If it contains detailed instructions for specific workflows (like PR reviews or database migrations), those tokens are present even when you're doing unrelated work. [Skills](/en/skills) load on-demand only when invoked, so moving specialized instructions into skills keeps your base context smaller. Aim to keep CLAUDE.md under 200 lines by including only essentials.

### Adjust extended thinking

Extended thinking is enabled by default because it significantly improves performance on complex planning and reasoning tasks. Thinking tokens are billed as output tokens, and the default budget can be tens of thousands of tokens per request depending on the model. For simpler tasks where deep reasoning isn't needed, you can reduce costs by lowering the [effort level](/en/model-config#adjust-effort-level) with `/effort` or in `/model`, disabling thinking in `/config`, or, on models with a [fixed thinking budget](/en/model-config#adaptive-reasoning-and-fixed-thinking-budgets), lowering the budget by setting the `MAX_THINKING_TOKENS` [environment variable](/en/env-vars), for example `MAX_THINKING_TOKENS=8000`. Adaptive-reasoning models ignore nonzero budgets, so use effort levels there instead. Disabling thinking is not available on Fable 5, which always uses extended thinking.

### Delegate verbose operations to subagents

Running tests, fetching documentation, or processing log files can consume significant context. Delegate these to [subagents](/en/sub-agents#isolate-high-volume-operations) so the verbose output stays in the subagent's context while only a summary returns to your main conversation.

### Manage agent team costs

Agent teams use approximately 7x more tokens than standard sessions when teammates run in plan mode, because each teammate maintains its own context window and runs as a separate Claude instance. Keep team tasks small and self-contained to limit per-teammate token usage. See [agent teams](/en/agent-teams) for details.

### Write specific prompts

Vague requests like "improve this codebase" trigger broad scanning. Specific requests like "add input validation to the login function in auth.ts" let Claude work efficiently with minimal file reads.

### Work efficiently on complex tasks

For longer or more complex work, these habits help avoid wasted tokens from going down the wrong path:

* **Use plan mode for complex tasks**: Press Shift+Tab to enter [plan mode](/en/permission-modes#analyze-before-you-edit-with-plan-mode) before implementation. Claude explores the codebase and proposes an approach for your approval, preventing expensive re-work when the initial direction is wrong.
* **Course-correct early**: If Claude starts heading the wrong direction, press Escape to stop immediately. Use `/rewind` or double-tap Escape to restore conversation and code to a previous checkpoint.
* **Give verification targets**: Include test cases, paste screenshots, or define expected output in your prompt. When Claude can verify its own work, it catches issues before you need to request fixes.
* **Test incrementally**: Write one file, test it, then continue. This catches issues early when they're cheap to fix.

## Background token usage

Claude Code uses tokens for some background functionality even when idle:

* **Conversation summarization**: Background jobs that summarize previous conversations for the `claude --resume` feature
* **Command processing**: Some commands like `/usage` may generate requests to check status

These background processes consume a small amount of tokens (typically under \$0.04 per session) even without active interaction.

## Understanding changes in Claude Code behavior

Claude Code regularly receives updates that may change how features work, including cost reporting. Run `claude --version` to check your current version. For specific billing questions, contact Anthropic support through your [Console account](https://platform.claude.com/login).
