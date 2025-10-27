# Analytics

> View detailed usage insights and productivity metrics for your organization's Claude Code deployment.

Claude Code provides an analytics dashboard that helps organizations understand developer usage patterns, track productivity metrics, and optimize their Claude Code adoption.

<Note>
  Analytics are currently available only for organizations using Claude Code with the Claude API through the Claude Console.
</Note>

## Access analytics

Navigate to the analytics dashboard at [console.anthropic.com/claude-code](https://console.anthropic.com/claude-code).

### Required roles

* **Primary Owner**
* **Owner**
* **Billing**
* **Admin**
* **Developer**

<Note>
  Users with **User**, **Claude Code User** or **Membership Admin** roles cannot access analytics.
</Note>

## Available metrics

### Lines of code accepted

Total lines of code written by Claude Code that users have accepted in their sessions.

* Excludes rejected code suggestions
* Doesn't track subsequent deletions

### Suggestion accept rate

Percentage of times users accept code editing tool usage, including:

* Edit
* Write
* NotebookEdit

### Activity

**users**: Number of active users in a given day (number on left Y-axis)

**sessions**: Number of active sessions in a given day (number on right Y-axis)

### Spend

**users**: Number of active users in a given day (number on left Y-axis)

**spend**: Total dollars spent in a given day (number on right Y-axis)

### Team insights

**Members**: All users who have authenticated to Claude Code

* API key users are displayed by **API key identifier**
* OAuth users are displayed by **email address**

**Spend this month:** Per-user total spend for the current month.

**Lines this month:** Per-user total of accepted code lines for the current month.

## Using analytics effectively

### Monitor adoption

Track team member status to identify:

* Active users who can share best practices
* Overall adoption trends across your organization

### Measure productivity

Tool acceptance rates and code metrics help you:

* Understand developer satisfaction with Claude Code suggestions
* Track code generation effectiveness
* Identify opportunities for training or process improvements

## Related resources

* [Monitoring usage with OpenTelemetry](/en/docs/claude-code/monitoring-usage) for custom metrics and alerting
* [Identity and access management](/en/docs/claude-code/iam) for role configuration
