> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Zero data retention

> Learn about Zero Data Retention (ZDR) for Claude Code, available to qualified accounts on Claude for Enterprise, including scope, disabled features, and how to request enablement.

Zero Data Retention (ZDR) for Claude Code is available to qualified accounts on Claude for Enterprise. When ZDR is enabled, prompts and model responses generated during Claude Code sessions are processed in real time and not stored by Anthropic after the response is returned, except where needed to comply with law or combat misuse.

<Note>
  ZDR is not included in the standard Claude for Enterprise plan and cannot be enabled from your admin settings. It is available to qualified accounts and requires separate enablement by Anthropic. If your organization requires ZDR, [contact sales](https://www.anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=zero_data_retention_request) or your Anthropic account team to confirm eligibility.
</Note>

ZDR on Claude for Enterprise gives enterprise customers the ability to use Claude Code with zero data retention and access administrative capabilities:

* Cost controls per user
* [Analytics](/en/analytics) dashboard
* [Server-managed settings](/en/server-managed-settings)
* Audit logs

ZDR for Claude Code on Claude for Enterprise applies only to Anthropic's direct platform. For Claude deployments on Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry, refer to those platforms' data retention policies.

## ZDR scope

ZDR covers Claude Code inference on Claude for Enterprise.

<Warning>
  ZDR is enabled on a per-organization basis. Each new organization requires ZDR to be enabled separately by your Anthropic account team. ZDR does not automatically apply to new organizations created under the same account. Contact your account team to enable ZDR for any new organizations.
</Warning>

### What ZDR covers

ZDR covers model inference calls made through Claude Code on Claude for Enterprise. When you use Claude Code in your terminal, the prompts you send and the responses Claude generates are not retained by Anthropic. This applies to every model available to ZDR organizations. Some models require data retention and are not available under ZDR; see [Model availability under ZDR](#model-availability-under-zdr).

### What ZDR does not cover

ZDR does not extend to the following, even for organizations with ZDR enabled. These features follow [standard data retention policies](/en/data-usage#data-retention):

| Feature                  | Details                                                                                                                                                                                                                                                     |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Chat on claude.ai        | Chat conversations through the Claude for Enterprise web interface are not covered by ZDR.                                                                                                                                                                  |
| Cowork                   | Cowork sessions are not covered by ZDR.                                                                                                                                                                                                                     |
| Claude Code Analytics    | Does not store prompts or model responses, but collects productivity metadata such as account emails and usage statistics. Contribution metrics are not available for ZDR organizations; the [analytics dashboard](/en/analytics) shows usage metrics only. |
| User and seat management | Administrative data such as account emails and seat assignments is retained under standard policies.                                                                                                                                                        |
| Third-party integrations | Data processed by third-party tools, MCP servers, or other external integrations is not covered by ZDR. Review those services' data handling practices independently.                                                                                       |

## Features disabled under ZDR

When ZDR is enabled for a Claude Code organization on Claude for Enterprise, certain features that require storing prompts or completions are automatically disabled at the backend level:

| Feature                                                           | Reason                                                                                      |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [Claude Code on the Web](/en/claude-code-on-the-web)              | Requires server-side storage of conversation history.                                       |
| [Cloud sessions](/en/desktop#cloud-sessions) from the Desktop app | Requires persistent session data that includes prompts and completions.                     |
| [Artifacts](/en/artifacts)                                        | Requires storing published page content on Anthropic-operated infrastructure.               |
| Feedback submission (`/feedback`)                                 | Submitting feedback sends conversation data to Anthropic.                                   |
| [Remote Control](/en/remote-control)                              | Stores the session transcript on Anthropic servers to sync the conversation across devices. |

These features are blocked in the backend regardless of client-side display. If you see a disabled feature in the Claude Code terminal during startup, attempting to use it returns an error indicating the organization's policies do not allow that action.

Future features may also be disabled if they require storing prompts or completions.

### Model availability under ZDR

Claude Fable 5 is not available for organizations with zero data retention enabled. This model class [requires data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements), so requests from ZDR organizations cannot be served by it. The model is either absent from the `/model` picker for ZDR organizations or shown as disabled with a notice that disabling ZDR is required, and the server rejects requests for it regardless of client configuration.

Other models remain available under ZDR. Fable 5 is not the default model, and the `best` alias, which resolves to Fable 5 where it is available, resolves to Opus for organizations where it is not, including ZDR organizations.

## Data retention for policy violations

Even with ZDR enabled, Anthropic may retain data where required by law or to address Usage Policy violations. If a session is flagged for a policy violation, Anthropic may retain the associated inputs and outputs for up to 2 years, consistent with Anthropic's standard ZDR policy.

## Request ZDR

To request ZDR for Claude Code on Claude for Enterprise, [contact sales](https://www.anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=zero_data_retention_request) or your Anthropic account team. Your account team will submit the request internally, and Anthropic will review and enable ZDR on your organization after confirming eligibility. All enablement actions are audit-logged.

If you are currently using ZDR for Claude Code via pay-as-you-go API keys, you can transition to Claude for Enterprise to gain access to administrative features while maintaining ZDR for Claude Code. Contact your account team to coordinate the migration.
