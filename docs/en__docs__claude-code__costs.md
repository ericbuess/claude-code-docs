# Manage costs effectively

> Learn how to track and optimize token usage and costs when using Claude Code.

Claude Code consumes tokens for each interaction. The average cost is \$6 per developer per day, with daily costs remaining below \$12 for 90% of users.

For team usage, Claude Code charges by API token consumption. On average, Claude Code costs \~\$100-200/developer per month with Sonnet 4.5 though there is large variance depending on how many instances users are running and whether they're using it in automation.

## Track your costs

### Using the `/cost` command

<Note>
  The `/cost` command is not intended for Claude Max and Pro subscribers.
</Note>

The `/cost` command provides detailed token usage statistics for your current session:

```
Total cost:            $0.55
Total duration (API):  6m 19.7s
Total duration (wall): 6h 33m 10.2s
Total code changes:    0 lines added, 0 lines removed
```

### Additional tracking options

Check [historical usage](https://support.claude.com/en/articles/9534590-cost-and-usage-reporting-in-console) in the Claude Console (requires Admin or Billing role) and set [workspace spend limits](https://support.claude.com/en/articles/9796807-creating-and-managing-workspaces) for the Claude Code workspace (requires Admin role).

<Note>
  When you first authenticate Claude Code with your Claude Console account, a workspace called "Claude Code" is automatically created for you. This workspace provides centralized cost tracking and management for all Claude Code usage in your organization. You cannot create API keys for this workspace - it is exclusively for Claude Code authentication and usage.
</Note>

## Managing costs for teams

When using Claude API, you can limit the total Claude Code workspace spend. To configure, [follow these instructions](https://support.claude.com/en/articles/9796807-creating-and-managing-workspaces). Admins can view cost and usage reporting by [following these instructions](https://support.claude.com/en/articles/9534590-cost-and-usage-reporting-in-console).

On Bedrock and Vertex, Claude Code does not send metrics from your cloud. In order to get cost metrics, several large enterprises reported using [LiteLLM](/en/docs/claude-code/bedrock-vertex-proxies#litellm), which is an open-source tool that helps companies [track spend by key](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend). This project is unaffiliated with Anthropic and we have not audited its security.

### Rate limit recommendations

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

The TPM per user decreases as team size grows because we expect fewer users to use Claude Code concurrently in larger organizations. These rate limits apply at the organization level, not per individual user, which means individual users can temporarily consume more than their calculated share when others aren't actively using the service.

<Note>
  If you anticipate scenarios with unusually high concurrent usage (such as live training sessions with large groups), you may need higher TPM allocations per user.
</Note>

## Reduce token usage

* **Compact conversations:**

  * Claude uses auto-compact by default when context exceeds 95% capacity
  * Toggle auto-compact: Run `/config` and navigate to "Auto-compact enabled"
  * Use `/compact` manually when context gets large
  * Add custom instructions: `/compact Focus on code samples and API usage`
  * Customize compaction by adding to CLAUDE.md:

    ```markdown  theme={null}
    # Summary instructions

    When you are using compact, please focus on test output and code changes
    ```

* **Write specific queries:** Avoid vague requests that trigger unnecessary scanning

* **Break down complex tasks:** Split large tasks into focused interactions

* **Clear history between tasks:** Use `/clear` to reset context

Costs can vary significantly based on:

* Size of codebase being analyzed
* Complexity of queries
* Number of files being searched or modified
* Length of conversation history
* Frequency of compacting conversations

## Background token usage

Claude Code uses tokens for some background functionality even when idle:

* **Conversation summarization**: Background jobs that summarize previous conversations for the `claude --resume` feature
* **Command processing**: Some commands like `/cost` may generate requests to check status

These background processes consume a small amount of tokens (typically under \$0.04 per session) even without active interaction.

## Tracking version changes and updates

### Current version information

To check your current Claude Code version and installation details:

```bash  theme={null}
claude doctor
```

This command shows your version, installation type, and system information.

### Understanding changes in Claude Code behavior

Claude Code regularly receives updates that may change how features work, including cost reporting:

* **Version tracking**: Use `claude doctor` to see your current version
* **Behavior changes**: Features like `/cost` may display information differently across versions
* **Documentation access**: Claude always has access to the latest documentation, which can help explain current feature behavior

### When cost reporting changes

If you notice changes in how costs are displayed (such as the `/cost` command showing different information):

1. **Verify your version**: Run `claude doctor` to confirm your current version
2. **Consult documentation**: Ask Claude directly about current feature behavior, as it has access to up-to-date documentation
3. **Contact support**: For specific billing questions, contact Anthropic support through your Console account

<Note>
  For team deployments, we recommend starting with a small pilot group to
  establish usage patterns before wider rollout.
</Note>
