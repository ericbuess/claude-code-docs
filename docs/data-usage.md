> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Data usage

> Learn about Anthropic's data usage policies for Claude

## Data policies

### Data training policy

**Consumer users (Free, Pro, and Max plans)**:
We give you the choice to allow your data to be used to improve future Claude models. We will train new models using data from Free, Pro, and Max accounts when this setting is on (including when you use Claude Code from these accounts).

**Commercial users**: (Team and Enterprise plans, API, 3rd-party platforms, and Claude Gov) maintain existing policies: Anthropic does not train generative models using code or prompts sent to Claude Code under commercial terms, unless the customer has chosen to provide their data to us for model improvement (for example, the [Developer Partner Program](https://support.claude.com/en/articles/11174108-about-the-development-partner-program)).

### Development Partner Program

If you explicitly opt in to methods to provide us with materials to train on, such as via the [Development Partner Program](https://support.claude.com/en/articles/11174108-about-the-development-partner-program), we may use those materials provided to train our models. An organization admin can expressly opt-in to the Development Partner Program for their organization. Note that this program is available only for Anthropic first-party API, and not for Amazon Bedrock or Google Cloud's Agent Platform users.

### Feedback using the `/feedback` command

If you choose to send us feedback about Claude Code using the `/feedback` command, we may use your feedback to improve our products and services. Transcripts shared via `/feedback`, or via `/bug` and `/share`, which report through the same path, are retained for 5 years.

### Session quality surveys

When you see the "How is Claude doing this session?" prompt in Claude Code, responding to this survey, including selecting "Dismiss", records only your rating. We do not collect or store any conversation transcripts, inputs, outputs, or other session data as part of the rating prompt itself. Unlike thumbs up/down feedback or `/feedback` reports, this session quality survey is a simple product satisfaction metric.

After the rating prompt, you may see a separate follow-up asking "Can Anthropic look at your session transcript to help us improve Claude Code?". This is an optional second step distinct from the rating:

* **Yes**: uploads your conversation transcript, any subagent transcripts, and the raw session log file from disk to Anthropic. Known API key and token patterns are redacted before upload. Source code, file contents, and other conversation content are uploaded as-is. Shared transcripts are retained for up to 6 months. On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and signed-in [Claude apps gateway](/en/claude-apps-gateway) sessions, Yes writes the same payload to a local archive under `~/.claude/feedback-bundles/` instead of uploading; nothing leaves your machine until you forward that file.
* **No**: declines without sending anything
* **Don't ask again**: declines and stops this follow-up from appearing in future sessions

Nothing is uploaded unless you explicitly select **Yes**. Organizations with [zero data retention](/en/zero-data-retention), or where product feedback is disabled by organization policy, or where `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` is set, never see this follow-up. Your responses to this survey, including session transcripts submitted after the rating prompt, do not impact your data training preferences and cannot be used to train our AI models.

To disable these surveys, set `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`. The survey is also disabled when `DISABLE_TELEMETRY`, `DO_NOT_TRACK`, or `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` is set. Organizations that block nonessential traffic but capture survey responses through their own [OpenTelemetry collector](/en/monitoring-usage) can opt the survey back in by setting `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL=1`. The survey then logs ratings to the configured collector only. The transcript-share follow-up and all other Anthropic-bound feedback traffic stay disabled. To control frequency instead of disabling, set [`feedbackSurveyRate`](/en/settings#available-settings) in your settings file to a probability between `0` and `1`.

### Data retention

Anthropic retains Claude Code data based on your account type and preferences.

**Consumer users (Free, Pro, and Max plans)**:

* Users who allow data use for model improvement: 5-year retention period to support model development and safety improvements
* Users who don't allow data use for model improvement: 30-day retention period
* Privacy settings can be changed at any time at [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls).

**Commercial users (Team, Enterprise, and API)**:

* Standard: 30-day retention period
* [Zero data retention](/en/zero-data-retention): available to qualified accounts for Claude Code on Claude for Enterprise. ZDR is not included in the standard Enterprise plan; it is enabled on a per-organization basis by your account team after confirming eligibility
* Local caching: Claude Code clients store session transcripts locally in plaintext under `~/.claude/projects/` for 30 days by default to enable session resumption. Adjust the period with `cleanupPeriodDays`. See [application data](/en/claude-directory#application-data) for what's stored and how to clear it.

You can delete individual Claude Code on the web sessions at any time. Deleting a session permanently removes the session's event data. For instructions on how to delete sessions, see [Delete sessions](/en/claude-code-on-the-web#delete-sessions).

Learn more about data retention practices in our [Privacy Center](https://privacy.anthropic.com/).

For full details, please review our [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) (for Team, Enterprise, and API users) or [Consumer Terms](https://www.anthropic.com/legal/consumer-terms) (for Free, Pro, and Max users) and [Privacy Policy](https://www.anthropic.com/legal/privacy).

## Data access

For all first party users, you can learn more about what data is logged for [local Claude Code](#local-claude-code-data-flow-and-dependencies) and [remote Claude Code](#cloud-execution-data-flow-and-dependencies). [Remote Control](/en/remote-control) sessions follow the local data flow since all execution happens on your machine; while connected, the session transcript is also stored on Anthropic servers to sync the conversation across devices, as described in [Connection and security](/en/remote-control#connection-and-security). Note for remote Claude Code, Claude accesses the repository where you initiate your Claude Code session. Claude does not access repositories that you have connected but have not started a session in.

## Local Claude Code: Data flow and dependencies

The diagram below shows how Claude Code connects to external services during installation and normal operation. Solid lines indicate required connections, while dashed lines represent optional or user-initiated data flows.

<img src="https://mintcdn.com/claude-code/YR4DRZyI3CdsXkiT/images/claude-code-data-flow.svg?fit=max&auto=format&n=YR4DRZyI3CdsXkiT&q=85&s=2846ea92cfc2297b8620c31c82b482ad" alt="Diagram showing Claude Code's external connections: install/update connects to the distribution server, and user requests connect to Anthropic's Console auth and public-api, with optional telemetry flows carrying metrics and error reports to Anthropic and third-party services. Feedback sent with /feedback goes to Google Cloud Storage and optionally creates a GitHub issue" width="720" height="520" data-path="images/claude-code-data-flow.svg" />

Claude Code runs locally. To interact with the LLM, Claude Code sends data over the network. This data includes all user prompts and model outputs, encrypted in transit via TLS 1.2+. Claude Code is compatible with most popular VPNs and LLM proxies.

Encryption at rest depends on your model provider:

| Provider                      | Encryption at rest                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Anthropic API                 | Infrastructure-level disk encryption (AES-256). Enable [Zero Data Retention](/en/zero-data-retention) for no server-side persistence.                                                                                                                                                                                                                                                                                                   |
| Amazon Bedrock                | AES-256 with AWS-managed keys. Customer-managed keys available via AWS KMS.                                                                                                                                                                                                                                                                                                                                                             |
| Google Cloud's Agent Platform | Google-managed encryption keys. CMEK available.                                                                                                                                                                                                                                                                                                                                                                                         |
| Microsoft Foundry             | Depends on the deployment's [hosting option](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#hosting-options). For Hosted on Azure deployments, prompts and completions remain within Azure; only usage metadata and content flagged by Anthropic's safety systems egress to Anthropic. For Hosted on Anthropic deployments, requests route to Anthropic infrastructure with AES-256 disk encryption. |

Claude Code is built on Anthropic's APIs. For details on API security controls, including API logging procedures, see the compliance artifacts in the [Anthropic Trust Center](https://trust.anthropic.com).

### Cloud execution: Data flow and dependencies

When using [Claude Code on the web](/en/claude-code-on-the-web), sessions run in Anthropic-managed virtual machines instead of locally. In cloud environments:

* **Code and data storage:** Your repository is cloned to an isolated VM. Code and session data are subject to the retention and usage policies for your account type (see Data retention section above)
* **Credentials:** GitHub authentication is handled through a secure proxy; your GitHub credentials never enter the sandbox
* **Network traffic:** All outbound traffic goes through a security proxy for audit logging and abuse prevention
* **Session data:** Prompts, code changes, and outputs follow the same data policies as local Claude Code usage

For security details about cloud execution, see [Security](/en/security#cloud-execution-security).

## Telemetry services

Claude Code sends two kinds of operational telemetry: usage metrics and error reports. You can turn each off individually with the environment variables below, or disable all non-essential traffic at once by setting `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`.

**Metrics**: latency, reliability, and usage patterns, sent to Anthropic and to third-party logging infrastructure over TLS. Metrics never include your code, prompts, or file paths. Set `DISABLE_TELEMETRY=1` to opt out.

**Error reports**: error messages and stack traces from Claude Code's own internals, sent to a third-party error tracking service over TLS. Claude Code redacts known patterns of secrets, file paths, email addresses, and other personal information before anything leaves your machine. Set `DISABLE_ERROR_REPORTING=1` to opt out.

Error reporting is on only when all of these apply:

* you sign in with a Claude Pro or Max subscription
* you're running Claude Code v2.1.198 or later
* you're connecting directly to the Claude API
* your organization doesn't have a zero data retention or HIPAA agreement

When you run the `/feedback` command, a copy of your conversation history including code is sent to Anthropic. The `/bug` and `/share` commands submit through the same path. Before submitting, you choose how much history to include: the current session only, which is the default, or also other sessions from the same project over the last 24 hours or 7 days. The data is encrypted in transit via TLS and stored in Google Cloud Storage, which encrypts stored data at rest by default. Optionally, a GitHub issue is created in the public repository. To opt out, set the `DISABLE_FEEDBACK_COMMAND` environment variable to `1`.

When you use a third-party provider such as Amazon Bedrock or Google Cloud's Agent Platform, or have no Anthropic credentials configured, `/feedback` writes the report to a local archive under `~/.claude/feedback-bundles/` instead of sending it to Anthropic. Known API key and token patterns are redacted before the archive is written. Nothing leaves your machine until you send that file to your Anthropic account representative or attach it to a support request.

## Default behaviors by API provider

By default, error reporting, telemetry, and bug reporting are disabled when using Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or Claude Platform on AWS. Session quality surveys and the WebFetch domain safety check are exceptions and run regardless of provider. On a signed-in [Claude apps gateway](/en/claude-apps-gateway) session, usage analytics, error reporting, and survey ratings to Anthropic are disabled by the gateway credential itself, with no setting to re-enable them. You can opt out of all non-essential traffic, including surveys, at once by setting `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. This variable doesn't affect the WebFetch check or official plugin marketplace auto-install; each has its own opt-out: `skipWebFetchPreflight` in [settings](/en/settings) for WebFetch, and `CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL` for the marketplace. Here are the full default behaviors:

| Service                              | Claude API                                                                                            | Google Cloud's Agent Platform API                                                      | Amazon Bedrock API                                                                     | Microsoft Foundry API                                                                  | Claude Platform on AWS                                                                 |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **Metrics**                          | Default on.<br />`DISABLE_TELEMETRY=1` to disable.                                                    | Default off.<br />`CLAUDE_CODE_USE_VERTEX` must be 1.                                  | Default off.<br />`CLAUDE_CODE_USE_BEDROCK` must be 1.                                 | Default off.<br />`CLAUDE_CODE_USE_FOUNDRY` must be 1.                                 | Default off.<br />`CLAUDE_CODE_USE_ANTHROPIC_AWS` must be 1.                           |
| **Error reports**                    | On for Pro and Max sign-ins on v2.1.198+, otherwise off.<br />`DISABLE_ERROR_REPORTING=1` to disable. | Default off.<br />`CLAUDE_CODE_USE_VERTEX` must be 1.                                  | Default off.<br />`CLAUDE_CODE_USE_BEDROCK` must be 1.                                 | Default off.<br />`CLAUDE_CODE_USE_FOUNDRY` must be 1.                                 | Default off.<br />`CLAUDE_CODE_USE_ANTHROPIC_AWS` must be 1.                           |
| **Claude API (`/feedback` reports)** | Default on.<br />`DISABLE_FEEDBACK_COMMAND=1` to disable.                                             | Default off.<br />`CLAUDE_CODE_USE_VERTEX` must be 1.                                  | Default off.<br />`CLAUDE_CODE_USE_BEDROCK` must be 1.                                 | Default off.<br />`CLAUDE_CODE_USE_FOUNDRY` must be 1.                                 | Default off.<br />`CLAUDE_CODE_USE_ANTHROPIC_AWS` must be 1.                           |
| **Session quality surveys**          | Default on.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` to disable.                                  | Default on.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` to disable.                   | Default on.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` to disable.                   | Default on.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` to disable.                   | Default on.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` to disable.                   |
| **WebFetch domain safety check**     | Default on.<br />`skipWebFetchPreflight: true` in [settings](/en/settings) to disable.                | Default on.<br />`skipWebFetchPreflight: true` in [settings](/en/settings) to disable. | Default on.<br />`skipWebFetchPreflight: true` in [settings](/en/settings) to disable. | Default on.<br />`skipWebFetchPreflight: true` in [settings](/en/settings) to disable. | Default on.<br />`skipWebFetchPreflight: true` in [settings](/en/settings) to disable. |

All environment variables can be checked into `settings.json` (see [settings reference](/en/settings)).

As of v2.1.126, when a host platform sets `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`, metrics default to on for Google Cloud's Agent Platform, Amazon Bedrock, and Microsoft Foundry, and follow the standard `DISABLE_TELEMETRY` opt-out. Error reporting and `/feedback` reports remain off by default on those providers.

### WebFetch domain safety check

Before fetching a URL, the WebFetch tool sends the requested hostname to `api.anthropic.com` to check it against a safety blocklist maintained by Anthropic. Only the hostname is sent, not the full URL, path, or page contents. Results are cached per hostname for five minutes.

This check runs regardless of which model provider you use and is not affected by `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. If your network blocks `api.anthropic.com`, WebFetch requests fail until you either allowlist the domain or set `skipWebFetchPreflight: true` in [settings](/en/settings). Disabling the check means WebFetch attempts to retrieve any URL without consulting the blocklist, so combine it with [`WebFetch` permission rules](/en/permissions#webfetch) if you need to restrict which domains Claude can reach.
