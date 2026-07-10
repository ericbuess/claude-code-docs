# API and data retention

Learn about how Anthropic's APIs and associated features retain data, including information about zero data retention (ZDR) and HIPAA-ready API access.

---

This page covers the Claude API (`api.anthropic.com`) and Claude Platform on AWS, where Anthropic is the data processor. On Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry, the cloud provider is the data processor; refer to those platforms' data retention and compliance documentation for their equivalent controls.

Anthropic offers two data handling arrangements for the Claude API: [zero data retention (ZDR)](#zero-data-retention-zdr-scope) and [HIPAA readiness](#hipaa-readiness). The [feature eligibility table](#feature-eligibility) lists which API features each arrangement covers. For Anthropic's standard retention policies outside these arrangements, see the [commercial data retention policy](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data) and the [consumer data retention policy](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data).

## How Anthropic approaches data retention

Different APIs and features have different storage needs. Where a feature does not require storage of customer prompts or responses, it may be eligible for ZDR. Where a feature necessarily requires storage, Anthropic designs for the smallest possible retention footprint under the following commitments:

* Retained data is never used for model training without your express permission.
* Only what is technically necessary for the feature to work is retained. Conversation content (your prompts and Claude's outputs) is not retained by default; the exception is [Covered Models](#model-specific-data-retention-requirements), which require 30-day retention.
* Retained data is purged on the shortest practical time to live (TTL), and Anthropic aims to give customers control over how long data is retained. What is held, and the retention duration where a specific TTL applies, is documented on each feature's page.

Several retention models sit outside the ZDR and HIPAA arrangements described on this page. Data accessible through the [Compliance API](/docs/en/manage-claude/compliance-api) follows its own retention model, the [Activity Feed](/docs/en/manage-claude/compliance-activity-feed) retains data for 6 years, and chat, file, and project content from claude.ai follows your organization's retention policy set in [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls).

## Zero data retention (ZDR)

Under a ZDR arrangement, Anthropic does not store customer prompts or responses at rest after the API response is returned. To request ZDR for your organization, contact the [Anthropic sales team](https://claude.com/contact-sales). ZDR is enabled per organization; each new organization requires ZDR to be enabled separately by your account team, and enablement does not automatically extend to other organizations under the same account.

### What ZDR covers

* **Claude Messages and Token Counting APIs:** ZDR applies to these endpoints for eligible features listed in the [feature eligibility table](#feature-eligibility). Features that ride on `/v1/messages` but are marked "No" in the table (such as code execution) are not covered.
* **Claude Code:** ZDR applies when Claude Code is used with API keys from a Commercial organization (an organization under Anthropic's Commercial Terms of Service, as distinct from a consumer Claude account) or through Claude Enterprise with ZDR enabled. If metrics logging is enabled in Claude Code, productivity data such as usage statistics is exempted from ZDR and may be retained. See the [Claude Code ZDR documentation](https://code.claude.com/docs/en/zero-data-retention) for full details.
* **Claude Platform on AWS:** [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws) follows the same data retention policy as the first-party Claude API. ZDR is available on request; contact your Anthropic account representative to enable it.

### What ZDR does not cover

* **Console and Workbench:** Any usage on Claude Console or the Workbench prompt-testing interface.
* **Claude Managed Agents:** Claude Managed Agents is a stateful resource; session transcripts persist until you delete them.
* **Claude consumer products:** Claude Free, Pro, and Max plans, including when customers on those plans use Claude's web, desktop, or mobile apps or Claude Code.
* **Claude Teams and Claude Enterprise product interfaces:** These interfaces are not ZDR-eligible. The exception is Claude Code used through Claude Enterprise with ZDR enabled; see [What ZDR covers](#what-zdr-covers).
* **Claude for Excel:** Not currently ZDR-eligible.
* **Claude Fable 5 and Claude Mythos 5:** These models require 30-day data retention and are not available under ZDR. See [Model-specific data retention requirements](#model-specific-data-retention-requirements).
* **Third-party integrations:** Data processed by third-party websites, tools, or other integrations is not covered, though some may have similar offerings. Review each service's data handling practices.
* **Cross-Origin Resource Sharing (CORS):** CORS is not supported for organizations with ZDR arrangements. To make API calls from browser-based applications, route requests through a backend proxy server. See the [API security guidance](/docs/en/api/overview) for proxy patterns and API-key handling.
* **Flagged content and legal holds:** See [Retention regardless of arrangement](#retention-regardless-of-arrangement).

<Note>
  For the most up-to-date information on which products and features are ZDR-eligible, refer to your contract terms or contact your Anthropic account representative.
</Note>

## HIPAA readiness

The Claude API supports HIPAA-ready integrations for organizations that handle protected health information (PHI). With a signed BAA and a HIPAA-enabled organization, you can use supported API features to process PHI while supporting your organization's HIPAA compliance. HIPAA readiness applies a broader set of privacy and security safeguards than ZDR (encryption, access controls, and audit logging that protect PHI throughout its lifecycle) rather than requiring immediate deletion. If your organization handles PHI, HIPAA readiness is the arrangement to use; you do not also need ZDR. See the [feature eligibility table](#feature-eligibility) for which features each arrangement covers.

<Note>
  This page covers HIPAA readiness for the Claude API. For the full HIPAA Implementation Guide covering Claude Enterprise and configuration requirements, see the [Anthropic Trust Center](https://trust.anthropic.com/resources).
</Note>

### What HIPAA readiness covers

* **Claude API:** HIPAA readiness applies to the Claude API (`api.anthropic.com`) for eligible features listed in the [feature eligibility table](#feature-eligibility).

### What HIPAA readiness does not cover

* **Claude consumer products:** Claude Free, Pro, and Max plans.
* **Console and Workbench:** Usage through the Claude Console interface.
* **Partner-operated platforms:** Amazon Bedrock and Google Cloud's Agent Platform. Refer to those platforms' compliance documentation.
* **Claude Platform on AWS and Microsoft Foundry:** HIPAA readiness is not available on these platforms.
* **Third-party integrations:** Data processed by external tools or services connected to your application.
* **Claude Code:** Claude Code is not covered under HIPAA readiness.
* **Beta features:** Features in beta are generally not covered under the BAA unless explicitly listed as eligible in the [feature eligibility table](#feature-eligibility).
* **Flagged content and legal holds:** See [Retention regardless of arrangement](#retention-regardless-of-arrangement).

### PHI handling guidelines

Protected health information (PHI) includes any individually identifiable health information. In the context of the Claude API, PHI typically appears in message content (prompts and Claude's responses), attached files (images, PDFs), and file names or metadata associated with message content. The following fields are not expected to contain PHI under the BAA: workspace names, user information (name, email, phone number), billing data, and support tickets.

When using [structured outputs](/docs/en/build-with-claude/structured-outputs) or tools with `strict: true`, the API compiles JSON schemas into grammars that are cached separately from message content. These cached schemas do not receive the same PHI protections as prompts and responses. **Do not include PHI in JSON schema definitions.** This restriction applies to schema property names, `enum` values, `const` values, and `pattern` regular expressions. Patient-specific information should appear only in message content, where it is protected under HIPAA safeguards.

### HIPAA error handling

Your signed BAA is the official source of truth for which features are covered. The API also enforces these restrictions automatically. When a HIPAA-enabled organization sends a request that includes a non-eligible feature, the API returns a `400` error to prevent accidental use of features not covered by your BAA:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "The requested features are not available for HIPAA-regulated organizations without Zero Data Retention: code_execution."
  }
}
```

The error message lists the non-eligible features detected in the request; remove them and retry. The phrase "without Zero Data Retention" is the API's own wording and does not change the resolution.

### Getting started with HIPAA readiness

<Steps>
  <Step title="Sign a Business Associate Agreement">
    Contact the [Anthropic sales team](https://claude.com/contact-sales) to sign a BAA that covers API usage.
  </Step>

  <Step title="Provision a HIPAA-enabled organization">
    Anthropic provisions a dedicated organization with HIPAA readiness controls enabled. This organization automatically enforces feature restrictions, blocking API requests that use non-eligible features.
  </Step>

  <Step title="Build with eligible features">
    Use the [feature eligibility table](#feature-eligibility) to confirm which features are supported. Review the [PHI handling guidelines](#phi-handling-guidelines) for features that require specific restrictions on where PHI can appear. For detailed configuration and compliance requirements, refer to the [HIPAA Implementation Guide](https://trust.anthropic.com/resources).
  </Step>
</Steps>

<Warning>
  HIPAA readiness is enforced at the organization level. If you need both HIPAA-ready and general-purpose API access, use separate organizations for each.
</Warning>

## Model-specific data retention requirements

Claude Fable 5 and Claude Mythos 5 are designated [Covered Models](https://support.claude.com/en/articles/15425695) and require 30-day data retention; ZDR is therefore not available for either model. On the Claude API, requests to Claude Fable 5 from an organization whose data retention configuration does not meet this requirement return a `400 invalid_request_error`:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "In order to access this model, your organization or workspace must have data retention enabled."
  }
}
```

The 30-day data retention requirement applies wherever Covered Models are offered. On the Claude API (including Claude Platform on AWS), Anthropic handles retained data. On Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry, retained data stays within your cloud provider's environment; review each platform's documentation for enablement steps.

### Enable 30-day retention for a workspace

Organizations with a ZDR arrangement can make Claude Fable 5 and Claude Mythos 5 available in a specific workspace by enabling 30-day retention for that workspace only. Other workspaces in the organization keep zero data retention.

<Steps>
  <Step title="Open the workspace's privacy controls">
    In [Claude Console > Settings > Workspaces](https://platform.claude.com/settings/workspaces), select the workspace and open its **Privacy controls** tab.
  </Step>

  <Step title="Turn on 30-day data retention">
    Enable the 30-day data retention setting for the workspace.
  </Step>

  <Step title="Verify">
    Requests to Claude Fable 5 and Claude Mythos 5 from this workspace now succeed. Workspaces without an override continue to follow the organization default.
  </Step>
</Steps>

## Feature eligibility

The following table lists which Claude API features are eligible for ZDR and HIPAA readiness arrangements.

Each eligibility column uses three values:

* **Yes:** The feature is fully eligible under the arrangement. For ZDR, "Yes" also assumes you are using a model that does not require 30-day data retention; [Covered Models](#model-specific-data-retention-requirements) are not available under ZDR regardless of feature eligibility.
* **Yes (qualified):** Your prompts and Claude's outputs are not stored, but a bounded technical artifact (named in the Details column) is retained briefly for the feature to function. See [How Anthropic approaches data retention](#how-anthropic-approaches-data-retention) for the commitments that govern these features.
* **No:** The feature is not eligible. Under HIPAA readiness, the API blocks requests that include a "No" feature and returns a `400` error. Under ZDR, the API does **not** block these features; using one is a choice to step outside your ZDR arrangement for that specific data, and the feature's own documented retention policy applies. Features marked "No" for ZDR are typically stateful (they store jobs, files, or container state), which is why they cannot be zero-retention.

| Feature                                                                                       | Endpoint                                         | ZDR eligible                                            | HIPAA eligible                      | Details                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [1M token context window](/docs/en/build-with-claude/context-windows)                         | `/v1/messages`                                   | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [Adaptive thinking](/docs/en/build-with-claude/adaptive-thinking)                             | `/v1/messages`                                   | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [Advisor tool](/docs/en/agents-and-tools/tool-use/advisor-tool)                               | `/v1/messages` (with `advisor` tool)             | <Eligible>Yes</Eligible>                                | <Eligible status="no">No</Eligible> | Advisor model output is returned in the API response; nothing is stored server-side after the response.                                                                                                                                                                                                                                                                                                                                                                            |
| [Agent skills](/docs/en/agents-and-tools/agent-skills/overview)                               | `/v1/messages` (with `skills`) / `/v1/skills`    | <Eligible status="no">No</Eligible>                     | <Eligible status="no">No</Eligible> | Skill data retained per standard policy. See [Agent skills](/docs/en/agents-and-tools/agent-skills/overview#data-retention).                                                                                                                                                                                                                                                                                                                                                       |
| [Bash tool](/docs/en/agents-and-tools/tool-use/bash-tool)                                     | `/v1/messages` (with `bash` tool)                | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            | Client-side tool executed in your environment.                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| [Batch processing](/docs/en/build-with-claude/batch-processing)                               | `/v1/messages/batches`                           | <Eligible status="no">No</Eligible>                     | <Eligible status="no">No</Eligible> | 29-day retention; async storage required. See [Batch processing](/docs/en/build-with-claude/batch-processing#data-retention).                                                                                                                                                                                                                                                                                                                                                      |
| [Cache diagnostics](/docs/en/build-with-claude/cache-diagnostics)                             | `/v1/messages` (with `diagnostics`)              | <Eligible status="qualified">Yes (qualified)</Eligible> | <Eligible status="no">No</Eligible> | Your prompts and Claude's outputs are not stored. A fingerprint of cryptographic hashes and token-count estimates is retained briefly to enable comparison against the next request. See [Cache diagnostics](/docs/en/build-with-claude/cache-diagnostics#data-retention).                                                                                                                                                                                                         |
| [Citations](/docs/en/build-with-claude/citations)                                             | `/v1/messages`                                   | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [Claude Managed Agents](/docs/en/managed-agents/overview)                                     | `/v1/agents`, `/v1/sessions`, `/v1/environments` | <Eligible status="no">No</Eligible>                     | <Eligible status="no">No</Eligible> | Sessions are stateful resources; transcripts persist until you delete them. Applies to all Managed Agents sub-features, including [Self-hosted sandboxes](/docs/en/managed-agents/self-hosted-sandboxes).                                                                                                                                                                                                                                                                          |
| [Code execution](/docs/en/agents-and-tools/tool-use/code-execution-tool)                      | `/v1/messages` (with `code_execution` tool)      | <Eligible status="no">No</Eligible>                     | <Eligible status="no">No</Eligible> | Container data retained up to 30 days. See [Code execution](/docs/en/agents-and-tools/tool-use/code-execution-tool#data-retention).                                                                                                                                                                                                                                                                                                                                                |
| [Computer use](/docs/en/agents-and-tools/tool-use/computer-use-tool)                          | `/v1/messages` (with `computer` tool)            | <Eligible>Yes</Eligible>                                | <Eligible status="no">No</Eligible> | Client-side tool where screenshots and files are captured and stored in your environment, not by Anthropic. See [Computer use](/docs/en/agents-and-tools/tool-use/computer-use-tool#data-retention).                                                                                                                                                                                                                                                                               |
| [Context editing](/docs/en/build-with-claude/context-editing)                                 | `/v1/messages` (with `context_management`)       | <Eligible>Yes</Eligible>                                | <Eligible status="no">No</Eligible> | Context edits (tool use clearing and thinking clearing) are applied in real time.                                                                                                                                                                                                                                                                                                                                                                                                  |
| [Context management (compaction)](/docs/en/build-with-claude/compaction)                      | `/v1/messages` (with `context_management`)       | <Eligible>Yes</Eligible>                                | <Eligible status="no">No</Eligible> | Server-side compaction results are returned and round-tripped statelessly through the API response.                                                                                                                                                                                                                                                                                                                                                                                |
| [Data residency](/docs/en/manage-claude/data-residency)                                       | `/v1/messages` (with `inference_geo`)            | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [Effort](/docs/en/build-with-claude/effort)                                                   | `/v1/messages` (with `effort`)                   | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [Extended thinking](/docs/en/build-with-claude/extended-thinking)                             | `/v1/messages` (with `thinking`)                 | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [Fast mode](/docs/en/build-with-claude/fast-mode)                                             | `/v1/messages` (with `speed: "fast"`)            | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            | Same Messages API endpoint with faster inference. ZDR applies regardless of speed setting.                                                                                                                                                                                                                                                                                                                                                                                         |
| [Files API](/docs/en/build-with-claude/files)                                                 | `/v1/files`                                      | <Eligible status="no">No</Eligible>                     | <Eligible status="no">No</Eligible> | Files retained until explicitly deleted. See [Files API](/docs/en/build-with-claude/files#data-retention).                                                                                                                                                                                                                                                                                                                                                                         |
| [Fine-grained tool streaming](/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming) | `/v1/messages`                                   | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [MCP connector](/docs/en/agents-and-tools/mcp-connector)                                      | `/v1/messages` (with `mcp_servers`)              | <Eligible status="no">No</Eligible>                     | <Eligible status="no">No</Eligible> | Data retained per standard policy. See [MCP connector](/docs/en/agents-and-tools/mcp-connector#data-retention).                                                                                                                                                                                                                                                                                                                                                                    |
| [MCP tunnels](/docs/en/agents-and-tools/mcp-tunnels/overview)                                 | `/v1/tunnels`                                    | <Eligible status="no">No</Eligible>                     | <Eligible status="no">No</Eligible> | Research preview. See [MCP tunnels security](/docs/en/agents-and-tools/mcp-tunnels/security) for the data-flow boundary and subprocessor details.                                                                                                                                                                                                                                                                                                                                  |
| [Memory tool](/docs/en/agents-and-tools/tool-use/memory-tool)                                 | `/v1/messages` (with `memory` tool)              | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            | Client-side memory storage where you control data retention.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| [Messages API](/docs/en/build-with-claude/working-with-messages)                              | `/v1/messages`                                   | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            | Standard API calls for generating Claude responses.                                                                                                                                                                                                                                                                                                                                                                                                                                |
| [PDF support](/docs/en/build-with-claude/pdf-support)                                         | `/v1/messages`                                   | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            | HIPAA eligibility applies to PDFs sent inline through the Messages API, not through the Files API.                                                                                                                                                                                                                                                                                                                                                                                 |
| [Programmatic tool calling](/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)     | `/v1/messages` (with `code_execution` tool)      | <Eligible status="no">No</Eligible>                     | <Eligible status="no">No</Eligible> | Built on code execution containers; data retained up to 30 days. See [Programmatic tool calling](/docs/en/agents-and-tools/tool-use/programmatic-tool-calling#data-retention).                                                                                                                                                                                                                                                                                                     |
| [Prompt caching](/docs/en/build-with-claude/prompt-caching)                                   | `/v1/messages`                                   | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            | Your prompts and Claude's outputs are not stored. KV cache representations and cryptographic hashes are held in memory for the cache TTL and promptly deleted after expiry. See [Prompt caching](/docs/en/build-with-claude/prompt-caching#data-retention).                                                                                                                                                                                                                        |
| [Search results](/docs/en/build-with-claude/search-results)                                   | `/v1/messages` (with `search_results` source)    | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [Structured outputs](/docs/en/build-with-claude/structured-outputs)                           | `/v1/messages`                                   | <Eligible status="qualified">Yes (qualified)</Eligible> | <Eligible>Yes</Eligible>            | Your prompts and Claude's outputs are not stored. Only the JSON schema is cached, for up to 24 hours since last use. This also covers [strict tool use](/docs/en/agents-and-tools/tool-use/strict-tool-use) (`strict: true` on tools), which uses the same grammar pipeline. PHI must not be included in JSON schema definitions; see [PHI handling guidelines](#phi-handling-guidelines). See [Structured outputs](/docs/en/build-with-claude/structured-outputs#data-retention). |
| [Text editor tool](/docs/en/agents-and-tools/tool-use/text-editor-tool)                       | `/v1/messages` (with `text_editor` tool)         | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            | Client-side tool executed in your environment.                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| [Token counting](/docs/en/build-with-claude/token-counting)                                   | `/v1/messages/count_tokens`                      | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            | Count tokens before sending requests.                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| [Tool search](/docs/en/agents-and-tools/tool-use/tool-search-tool)                            | `/v1/messages` (with `tool_search` tool)         | <Eligible>Yes</Eligible>                                | <Eligible status="no">No</Eligible> | Server-side tool executed by Anthropic; the tool definitions in the request are searched in memory per call and nothing is stored after the response.                                                                                                                                                                                                                                                                                                                              |
| [Web fetch](/docs/en/agents-and-tools/tool-use/web-fetch-tool)                                | `/v1/messages` (with `web_fetch` tool)           | <Eligible>Yes</Eligible>                                | <Eligible status="no">No</Eligible> | Fetched web content returned in the API response. [Dynamic filtering](/docs/en/agents-and-tools/tool-use/web-search-tool#dynamic-filtering) is not eligible for ZDR or HIPAA. Website publishers may retain request data (such as fetched URLs and request metadata) according to their own policies.                                                                                                                                                                              |
| [Web search](/docs/en/agents-and-tools/tool-use/web-search-tool)                              | `/v1/messages` (with `web_search` tool)          | <Eligible>Yes</Eligible>                                | <Eligible>Yes</Eligible>            | Real-time web search results returned in the API response. [Dynamic filtering](/docs/en/agents-and-tools/tool-use/web-search-tool#dynamic-filtering) is not eligible for ZDR or HIPAA.                                                                                                                                                                                                                                                                                             |

## Retention regardless of arrangement

Even with ZDR or HIPAA arrangements in place, Anthropic may retain data where required by law or where it has been flagged by Anthropic's automated trust and safety systems. As a result, if a chat or session is flagged, Anthropic may retain inputs and outputs for up to 2 years.

## Frequently asked questions

<AccordionGroup>
  <Accordion title="How do I know if my organization has ZDR arrangements?">
    Check your contract terms or contact your Anthropic account representative to confirm whether your organization has ZDR arrangements in place.
  </Accordion>

  <Accordion title="Can I use ZDR-eligible (qualified) features under my ZDR arrangement?">
    Yes. These features retain a minimal, documented set of technical data, not your prompts or Claude's outputs. See the [feature eligibility table](#feature-eligibility) legend for what "Yes (qualified)" means and [How Anthropic approaches data retention](#how-anthropic-approaches-data-retention) for the commitments that govern these features.
  </Accordion>

  <Accordion title="What happens if I use a feature marked &#x22;No&#x22; under ZDR?">
    Nothing blocks the request. Features marked "No" for ZDR are fundamentally stateful: the Batch API stores your jobs, the Files API stores your files, and code execution runs in persistent containers. Data for these features is retained per the feature's documented policy. Using them is a choice to step outside your ZDR arrangement for that specific data.
  </Accordion>

  <Accordion title="Can I request deletion of data from features that are not ZDR-eligible?">
    Contact your Anthropic account representative to discuss deletion options for non-ZDR features.
  </Accordion>

  <Accordion title="How does HIPAA readiness differ from ZDR?">
    ZDR prevents customer data from being stored at rest after the API response is returned. HIPAA readiness involves a broader set of privacy and security safeguards that protect PHI throughout its lifecycle, including encryption, access controls, and audit logging. Under HIPAA readiness, data can be retained with these safeguards in place rather than requiring immediate deletion. The two arrangements cover different feature sets; see the [feature eligibility table](#feature-eligibility).
  </Accordion>

  <Accordion title="Do I still need ZDR if I have HIPAA readiness?">
    No. HIPAA-ready API access is designed as an alternative to ZDR for organizations handling PHI. With HIPAA readiness enabled, you get access to supported API features while maintaining the privacy and security protections that HIPAA requires.
  </Accordion>

  <Accordion title="What happens if I use a non-eligible feature under HIPAA?">
    The API returns a `400` error with an `invalid_request_error` type. The error message identifies which features are not available. Remove the non-eligible features from your request and retry. See [HIPAA error handling](#hipaa-error-handling).
  </Accordion>

  <Accordion title="Can I use the same organization for HIPAA and non-HIPAA workloads?">
    No. HIPAA readiness is enforced at the organization level and automatically blocks all non-eligible features. Use a separate organization for workloads that do not require HIPAA readiness.
  </Accordion>

  <Accordion title="How do I request HIPAA-ready API access?">
    Contact the [Anthropic sales team](https://claude.com/contact-sales) to discuss HIPAA-ready API access and sign a Business Associate Agreement.
  </Accordion>

  <Accordion title="Does this apply to Amazon Bedrock or Google Cloud?">
    No. The ZDR and HIPAA arrangements described on this page apply to the Claude API, where Anthropic is the data processor. On Bedrock and Google Cloud, the cloud provider is the data processor; refer to those platforms' data retention and compliance policies for their equivalent controls.
  </Accordion>

  <Accordion title="Is Claude Platform on AWS eligible for ZDR or HIPAA readiness?">
    Claude Platform on AWS follows the same data retention policy as the first-party Claude API. ZDR is available on request; contact your Anthropic account representative to enable it. HIPAA readiness is not available on Claude Platform on AWS. See [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws) for details.
  </Accordion>

  <Accordion title="Is Claude Code eligible for ZDR?">
    Claude Code is eligible for ZDR through two paths:

    * **API keys:** Claude Code used with pay-as-you-go API keys from a Commercial organization
    * **Claude Enterprise:** Claude Code used through Claude Enterprise with ZDR enabled for the organization

    ZDR is enabled on a per-organization basis. Each new organization requires ZDR to be enabled separately by your account team. ZDR does not automatically apply to new organizations created under the same account.

    Additionally, if you have metrics logging enabled in Claude Code, productivity data (such as usage statistics) is exempted from ZDR and may be retained.

    For full details on ZDR for Claude Code on Claude Enterprise, including disabled features and how to request enablement, see the [Claude Code ZDR documentation](https://code.claude.com/docs/en/zero-data-retention).
  </Accordion>

  <Accordion title="Does Claude for Excel support ZDR?">
    No, Claude for Excel is not currently ZDR-eligible.
  </Accordion>

  <Accordion title="How do I request ZDR?">
    To request a ZDR arrangement, contact the [Anthropic sales team](https://claude.com/contact-sales).
  </Accordion>
</AccordionGroup>

## Related resources

* [Privacy Policy](https://www.anthropic.com/legal/privacy)
* [Structured outputs](/docs/en/build-with-claude/structured-outputs)
* [Prompt caching](/docs/en/build-with-claude/prompt-caching)
* [Batch processing](/docs/en/build-with-claude/batch-processing)
* [Files API](/docs/en/api/files-create)
* [Trust Center](https://trust.anthropic.com/resources)
