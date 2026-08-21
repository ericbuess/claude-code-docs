---
title: Claude Platform release notes
url: https://platform.claude.com/docs/en/release-notes/overview
description: Updates to the Claude Platform, including the Claude API, client SDKs, and the Claude Console.
---

The Claude Platform release notes list changes to the Claude API, the client SDKs, and the Claude Console, newest first.

<Tip>
  For release notes on Claude Apps, see the [Release notes for Claude Apps in the Claude Help Center](https://support.claude.com/en/articles/12138966-release-notes).

  For updates to Claude Code, see the [complete CHANGELOG.md](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) in the `claude-code` repository.
</Tip>

### August 19, 2026

* The [computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) is now generally available on the Claude API as the `computer_toolset_20260801` toolset: no beta header, batch actions (several actions in one turn), `zoom` enabled by default, and per-member configuration through `configs`. Earlier beta versions remain available. Upgrading an existing integration changes the request shape and tool handling; see [Migrate from `computer_20251124`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124).
* We've launched the [browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) (`browser_toolset_20260801`), a client toolset for driving a browser that your application hosts. It works inside a browser viewport rather than a whole desktop, reading the page itself (its accessibility tree, elements, forms, and tabs) and adding element references, form input, tab management, download reporting, and opt-in file upload on top of screenshot-and-click control.
* Both toolsets are available for Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Sonnet 5, and Claude Opus 4.8 on the Claude API.
* The [Files API](https://platform.claude.com/docs/en/build-with-claude/files) is now generally available on the Claude API. Requests to the `/v1/files` endpoints, and Messages API requests that reference an uploaded file, no longer require the `files-api-2025-04-14` beta header. Requests sent without the header use the GA response format: [file expiration](https://platform.claude.com/docs/en/build-with-claude/files#file-expiration) (set `expires_in_seconds` when you upload a file; file objects report `expires_at`), and `page` and `next_page` [pagination](https://platform.claude.com/docs/en/api/overview#pagination) plus an `ids[]` filter when you [list files](https://platform.claude.com/docs/en/build-with-claude/files#list-files). `/v1/files` requests that still send the beta header keep working and return the previous response format.
* [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) and the Skills API (`/v1/skills`) are now generally available on the Claude API. Requests no longer require the `skills-2025-10-02` beta header, including Messages API requests that load Skills through the `container` parameter. Requests that still send the header continue to work unchanged. See [Using Agent Skills with the API](https://platform.claude.com/docs/en/build-with-claude/skills-guide).
* The [Admin API](https://platform.claude.com/docs/en/api/admin) user-management endpoints for **Claude Enterprise** (claude.ai) organizations (members, invites, groups, and custom roles) are now generally available. The `anthropic-beta: ce-user-management-2026-07-13` header is no longer required on group and custom-role requests; requests that still send it are accepted unchanged. See [User management](https://platform.claude.com/docs/en/manage-claude/user-management).
* You can now restrict which sites a Claude Managed Agents agent's `web_search` and `web_fetch` tools can reach. Set `allowed_domains` or `blocked_domains` on the tool's entry in the `agent_toolset_20260401` `configs` array; `web_fetch` also accepts `max_content_tokens` and `web_search` accepts `user_location`. Each `configs` entry is identified by its `name` and typed by an optional `type`, and requests that pass only `name`, `enabled`, and `permission_policy` continue to work; in the typed SDKs, `configs` entries become per-tool types. See [Restrict web search and web fetch domains](https://platform.claude.com/docs/en/managed-agents/tools#restrict-web-search-and-web-fetch-domains).
* Claude Managed Agents sessions that run in a [self-hosted sandbox](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes) can now attach [memory stores](https://platform.claude.com/docs/en/managed-agents/memory). The Python, TypeScript, and Go SDK workers download each attached store into the sandbox at its `mount_path` and sync the agent's changes back to the store. See [Use memory stores](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#use-memory-stores).
* The session viewer in the Claude Console has been redesigned with a timeline minimap, a transcript grouped by model request, and an Inspector panel for session details and cost, raw events, per-tool statistics, mounted resources, and per-thread activity. See [Console observability](https://platform.claude.com/docs/en/managed-agents/events-and-streaming#console-observability).

### August 18, 2026

* Workbench is now [**Playground**](https://platform.claude.com/playground) in the Claude Console. Playground supports every Messages API parameter and includes templates that demonstrate API features such as code execution and web search. It shows the full SDK request and the API response for each run, to help you understand the API and build with it. For more, see the [Claude Help Center](https://support.claude.com/en/articles/8606378-how-do-i-use-playground) or try it at [platform.claude.com/playground](https://platform.claude.com/playground).

### August 11, 2026

* The [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api) now returns transcripts of Cowork and Claude Code sessions that run on your users' machines, in beta for Claude Enterprise organizations. `GET /v1/compliance/apps/sessions/local` lists sessions across your organization, `GET /v1/compliance/apps/sessions/local/{session_id}` retrieves one session's metadata, and `GET /v1/compliance/apps/sessions/local/{session_id}/messages` returns its transcript, all with your existing Compliance Access Key and the `read:compliance_user_data` scope. See [Sessions on users' machines](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-local-sessions).
* We've added the `anthropic-workspace-id` response header to the Claude API. It carries the `wrkspc_`-prefixed ID of the workspace that the request's API key or access token resolved to, including your organization's Default Workspace. See [Identify the workspace behind an API response](https://platform.claude.com/docs/en/manage-claude/workspaces#identify-the-workspace-behind-an-api-response).

### August 10, 2026

* The introductory pricing for **Claude Sonnet 5** ($2 / $10 per MTok) is now the standard price: the previously scheduled increase to $3 / $15 per MTok on September 1, 2026 will not occur. See [Pricing](https://platform.claude.com/docs/en/about-claude/pricing).

### August 7, 2026

* You can now set a budget on a Claude Managed Agents session: a hard cap on the session's spend, priced at public list rates. A session that reaches its budget pauses with the `budget_reached` stop reason instead of starting new model requests; changing or removing the budget resumes it. Deployments accept the same budget and apply it to each session they start. See [Session budgets](https://platform.claude.com/docs/en/managed-agents/budgets).
* You can now give a Claude Managed Agents session an advisor: a model at least as capable as the agent's own that the session's primary thread can consult mid-turn for strategic guidance. Configure it as a `{"type": "advisor"}` entry in the agent's multiagent roster, naming the `model` to consult. See [Give the session an advisor](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration#give-the-session-an-advisor).
* You can now control where model inference runs for a Claude Managed Agents agent. Set `inference_geo` inside the `model` object when you [create the agent](https://platform.claude.com/docs/en/managed-agents/agent-setup#pin-the-inference-geo), or [override it for a single session](https://platform.claude.com/docs/en/managed-agents/sessions#pin-the-inference-geo-for-a-session). See [Data residency](https://platform.claude.com/docs/en/manage-claude/data-residency) for the available geos and pricing.
* Claude Managed Agents sessions can now [load skills from a GitHub repository](https://platform.claude.com/docs/en/managed-agents/skills#load-skills-from-a-github-repository). When a session [mounts a repository](https://platform.claude.com/docs/en/managed-agents/github), any skills in its root `.claude/skills` directory are discovered automatically at session start and available to the agent for that session.

### August 5, 2026

* **Inference hooks** are now in beta for Claude Enterprise organizations. Point Claude at your organization's AI security server, and each governed prompt across claude.ai, Cowork, and Claude Code is held for the server's allow or deny verdict before inference proceeds. Requests are signed, failure handling is configurable, and every denial is recorded in the compliance [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed). See [Inference hooks](https://platform.claude.com/docs/en/manage-claude/inference-hooks).
* We've retired the Claude Opus 4.1 model (`claude-opus-4-1-20250805`). All requests to this model on the Claude API will now return an error. We recommend upgrading to [Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison). Researchers can request ongoing access through the [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).

### August 3, 2026

* The [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api) now returns transcripts of Cowork sessions started on claude.ai web or mobile, in beta for Claude Enterprise organizations. `GET /v1/compliance/apps/sessions/remote` lists sessions and `GET /v1/compliance/apps/sessions/remote/{session_id}/messages` returns one session's transcript, using your existing Compliance Access Key with the `read:compliance_user_data` scope. See [Sessions in the cloud](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-remote-sessions).

### August 1, 2026

* [Dreams](https://platform.claude.com/docs/en/managed-agents/dreams) (research preview) now supports Claude Opus 5. See [Supported models](https://platform.claude.com/docs/en/managed-agents/dreams#limits).

### July 24, 2026

* We've launched **Claude Opus 5** (`claude-opus-5`), a step-change improvement over Claude Opus 4.8. Claude Opus 5 supports a [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) (both the default and the maximum), 128k max output tokens, and [thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) on by default, at $5 / $25 USD per MTok, the same pricing as Claude Opus 4.8. It's available on the Claude API, [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock), [Claude on Google Cloud](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai), and [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry). See [What's new in Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5) for new features, behavior changes, and migration guidance, and the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview) for complete specs.
* On Claude Opus 5, disabling thinking is allowed only at effort `high` or below: `thinking: {"type": "disabled"}` with effort `xhigh` or `max` returns a 400 error, a breaking change from Claude Opus 4.8. See [What's new in Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5#behavior-changes).
* [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) is the primary control for steering Claude Opus 5: the model supports the full ladder (`low`, `medium`, `high`, `xhigh`, `max`), with `max` for capability-critical work.
* Mid-conversation tool changes are now in beta on Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, and Claude Opus 5: add or remove tools between turns of a conversation while preserving the prompt cache. Include the `mid-conversation-tool-changes-2026-07-01` beta header in your requests.
* The `fallbacks` parameter now supports a `"default"` mode, which applies Anthropic's recommended fallback models by refusal category. Server-side fallback is in beta, and the `"default"` mode requires the `server-side-fallback-2026-07-01` beta header. See [Refusals and fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback).
* We've removed [fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode) for Claude Opus 4.7. Requests to `claude-opus-4-7` with `speed: "fast"` now return an error; unlike Claude Opus 4.6, they do not fall back to standard speed. Claude Opus 4.7 itself remains available at standard speed. To continue using fast mode, migrate to [Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-from-claude-opus-47) or Claude Opus 4.8. Read more in [Fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode#supported-models).

### July 22, 2026

* You can now set an `effort` level on a Claude Managed Agents agent's model configuration. Pass `effort` inside the `model` object when you [create the agent](https://platform.claude.com/docs/en/managed-agents/agent-setup#create-an-agent). See [Effort levels](https://platform.claude.com/docs/en/build-with-claude/effort#effort-levels) for what each level does.
* Webhooks for Claude Managed Agents now cover the environment and memory store lifecycle: four `environment.*` event types and three `memory_store.*` event types. You can react to environment and memory store lifecycle changes without polling. See the Environment events and Memory store events tabs in [Subscribe to webhooks](https://platform.claude.com/docs/en/managed-agents/webhooks#supported-event-types).
* When creating a Claude Managed Agents session, you can now [seed it with initial events](https://platform.claude.com/docs/en/managed-agents/sessions#seed-the-session-with-initial-events). Pass `initial_events` on `POST /v1/sessions` with up to 50 `user.message` and `user.define_outcome` events. A non-empty list starts the agent loop in the same call, so you don't need a separate send-events request to start work.
* The `version` field is now optional when [updating a Claude Managed Agents agent](https://platform.claude.com/docs/en/managed-agents/agent-setup#update-an-agent). Supply it for optimistic concurrency (a mismatch returns a 409 error), or omit it to apply the update unconditionally. See [Update semantics](https://platform.claude.com/docs/en/managed-agents/agent-setup#update-semantics).
* Claude Managed Agents session thread event streams now support [event deltas](https://platform.claude.com/docs/en/managed-agents/events-and-streaming#event-deltas). `GET /v1/sessions/{session_id}/threads/{thread_id}/stream` accepts the same `event_deltas[]` query parameter as the session-level stream, so you can preview a subagent's text as the model generates it. A connection previews only the thread it's reading. See [Preview session thread events](https://platform.claude.com/docs/en/managed-agents/events-and-streaming#preview-session-thread-events).

### July 17, 2026

* The legacy **Workbench** ([platform.claude.com/workbench](https://platform.claude.com/workbench)) in the Claude Console is being sunset with access ending on August 17, 2026. Saved prompts, variables, and evals are not supported in the updated [Workbench](https://platform.claude.com/playground). You can export any data you want to keep from the banner and under your **Organizational Settings**. For more, see [How do I use the Workbench?](https://support.claude.com/en/articles/8606378-how-do-i-use-the-workbench) in the Claude Help Center.
* The experimental prompt tools APIs for generating, improving, and templatizing prompts (`/v1/experimental/generate_prompt`, `/v1/experimental/improve_prompt`, and `/v1/experimental/templatize_prompt`) are being retired along with the Workbench on August 17, 2026. After removal, requests to these endpoints will return an error.

### July 15, 2026

* [Mid-conversation system messages](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages) are available on Claude Fable 5, Claude Mythos 5, and Claude Opus 4.8, on the Claude API, [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock), and [Google Cloud](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai). No beta header is required. This corrects earlier availability notes.

### July 14, 2026

* You can now manage the people in your **Claude Enterprise** (claude.ai) organization with the [Admin API](https://platform.claude.com/docs/en/api/admin), in beta for all Claude Enterprise organizations: list members and look them up by email address, change a member's role, remove members, send and withdraw invites, manage groups and their membership, and read custom roles. Group and custom-role requests require the `anthropic-beta: ce-user-management-2026-07-13` beta header; member and invite requests take no beta header. An Admin API key with the `read:org_audit` scope can also call every user-management `GET` endpoint. See [User management](https://platform.claude.com/docs/en/manage-claude/user-management).

### July 10, 2026

* [Dreams](https://platform.claude.com/docs/en/managed-agents/dreams) (research preview) now supports Claude Fable 5 and Claude Sonnet 5. See [Supported models](https://platform.claude.com/docs/en/managed-agents/dreams#limits).
* We've expanded the [Access Transparency](https://platform.claude.com/docs/en/manage-claude/access-transparency) documentation of `cmek_preserve` events with a filter example, an example event payload, and two preservation reason codes (`policy_violation_investigation`, `csae_report`). The documentation now also clarifies that a preservation event is written whether the preservation was initiated by a human reviewer or an automated safety pipeline. See [CMEK content preservation](https://platform.claude.com/docs/en/manage-claude/access-transparency#cmek-content-preservation).

### July 8, 2026

* You can now set an expiration when you create an API key or an Admin API key in the [Claude Console](https://platform.claude.com/settings/keys). Choose a preset, a custom duration, or **Never**. For keys with a lifetime of at least 7 days, Anthropic emails the creator before expiration. Existing keys are unaffected. The Admin API reports each key's expiration in the [`expires_at`](https://platform.claude.com/docs/en/api/admin/api_keys/list) field. See [Authentication](https://platform.claude.com/docs/en/manage-claude/authentication#key-expiration).

### July 2, 2026

* We've added the `agent-memory-2026-07-22` beta header, which changes how [listing memories](https://platform.claude.com/docs/en/managed-agents/memory#list-memories) (`GET /v1/memory_stores/{memory_store_id}/memories`) behaves: results are returned in a stable, server-defined order and the `order_by` and `order` parameters are ignored; `depth` accepts only `0`, `1`, or being omitted (other values return a `400` error); and `path_prefix` must end with `/` and matches whole path segments instead of a substring. Page cursors issued without the header aren't valid with it, so restart from the first page when you adopt it. On memory store endpoints, `agent-memory-2026-07-22` replaces `managed-agents-2026-04-01`; sending both returns a `400` error. On July 22, 2026, the `managed-agents-2026-04-01` header adopts the same list behavior. See [Beta headers](https://platform.claude.com/docs/en/api/beta-headers#endpoint-specific-headers).
* The Python (0.116.0), TypeScript (0.110.0), Go (1.56.0), Java (2.48.0), Ruby (1.55.0), PHP (0.36.0), C# (12.35.0), and CLI (1.16.0) SDKs now send `agent-memory-2026-07-22` on all memory store calls instead of `managed-agents-2026-04-01`. If your code passes `betas` explicitly on memory store calls, replace `managed-agents-2026-04-01` with `agent-memory-2026-07-22` there rather than adding a second value.

### July 1, 2026

* We've restored access to Claude Fable 5 and Claude Mythos 5. See [our statement](https://www.anthropic.com/news/redeploying-fable-5) for more information.

### June 30, 2026

* We've launched **Claude Sonnet 5** (`claude-sonnet-5`), the next generation of our Sonnet model family, at introductory pricing of $2 / $10 per MTok (made the standard price on August 10, 2026). Claude Sonnet 5 supports a [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows), 128k max output tokens, and the same set of tools and platform features as Claude Sonnet 4.6, except [Priority Tier](https://platform.claude.com/docs/en/api/service-tiers#supported-models), which is not available on Claude Sonnet 5. Three behavior changes apply when migrating: [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) is now on by default; manual extended thinking (`thinking: {type: "enabled", budget_tokens: N}`) is removed and returns a 400 error (it was deprecated on Sonnet 4.6); and setting sampling parameters (`temperature`, `top_p`, `top_k`) to non-default values returns a 400 error. Claude Sonnet 5 also uses a new tokenizer that produces approximately 30% more tokens for the same text. The exact increase depends on the content and workload shape. See [What's new in Claude Sonnet 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5) for details and migration guidance. For behavioral differences and model-specific prompting patterns, see [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5).
* Claude Managed Agents session event streams now support [event deltas](https://platform.claude.com/docs/en/managed-agents/events-and-streaming#event-deltas). Opt in with the `event_deltas[]` query parameter on `GET /v1/sessions/{session_id}/events/stream`. The `event_start` and `event_delta` events preview an agent message's text as it's generated, before the complete `agent.message` event arrives.
* [Listing sessions](https://platform.claude.com/docs/en/managed-agents/session-operations#listing-sessions) for Claude Managed Agents now supports backward pagination. `GET /v1/sessions` returns a `prev_page` cursor alongside `next_page`; pass it as the `page` parameter to return to the previous page. See [Pagination](https://platform.claude.com/docs/en/api/overview#pagination).
* When creating a Claude Managed Agents session, you can now [override the agent's configuration for that session](https://platform.claude.com/docs/en/managed-agents/sessions#override-agent-configuration-for-a-session). Pass `agent` with `type: "agent_with_overrides"` to replace the model, system prompt, tools, MCP servers, or skills for a single session. The agent itself is unchanged.
* Claude Managed Agents vaults now support an `injection_location` setting on [environment variable credentials](https://platform.claude.com/docs/en/managed-agents/vaults#add-a-credential) (the Environment variable tab). It controls whether the credential's value is substituted, at egress, into the agent's outbound request headers, the request body, or both.
* Webhooks for Claude Managed Agents now cover the agent, deployment, and deployment run lifecycle. You can react to a newly published agent version, a paused deployment, or a failed scheduled run without polling. See the Agent events, Deployment events, and Deployment run events tabs in [Subscribe to webhooks](https://platform.claude.com/docs/en/managed-agents/webhooks#supported-event-types).

### June 29, 2026

* We've removed [fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode) for Claude Opus 4.6. Requests to `claude-opus-4-6` with `speed: "fast"` no longer run at fast speed or premium pricing: they run at standard speed, are billed at standard rates, and do not return an error. The response's `usage.speed` field reports the speed used. To continue using fast mode, migrate to [Claude Opus 4.8](https://platform.claude.com/docs/en/about-claude/models/migration-guide). Read more in [Fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode#supported-models).

### June 26, 2026

* We've raised [rate limits](https://platform.claude.com/docs/en/api/rate-limits) across the Claude API. Claude Sonnet and Claude Haiku rate limits now match Claude Opus at every usage tier, and usage tiers have been consolidated into three: Start, Build, and Scale. Most organizations move to a higher tier, no organization receives lower limits than before, and no action is required. You can view your tier and current limits in the [Claude Console](https://platform.claude.com/settings/limits).

### June 25, 2026

* We've deprecated [fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode) for Claude Opus 4.7, with removal on July 24, 2026. After removal, requests to `claude-opus-4-7` with `speed: "fast"` will return an error. Migrate to fast mode for Claude Opus 4.8. Read more in [Fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode#supported-models).

### June 22, 2026

* **MCP tunnels** (research preview): the management API moved from `/v1/organizations/tunnels` on the Admin API to `/v1/tunnels` on the Claude API. The new surface uses the `anthropic-beta: mcp-tunnels-2026-06-22` header and the `workspace:manage_tunnels` WIF scope. The previous surface remains available during a migration window. See the [Tunnels API reference](https://platform.claude.com/docs/en/api/beta/tunnels).

### June 18, 2026

* The Python, TypeScript, Go, Java, Ruby, PHP, and C# SDKs now include support for `code_execution_20260120`, the [code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) version that adds REPL state persistence and is the minimum version for [programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling). To adopt it, set the tool's `type` to `code_execution_20260120`; no beta header is required. It's available on Claude Fable 5, Claude Mythos 5, Claude Opus 4.5 and newer, and Claude Sonnet 4.5 and newer; see the [model compatibility table](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#model-compatibility).

### June 15, 2026

* We've retired the Claude Sonnet 4 model (`claude-sonnet-4-20250514`) and the Claude Opus 4 model (`claude-opus-4-20250514`). All requests to these models on the Claude API will now return an error. We recommend upgrading to [Claude Sonnet 4.6](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison) and [Claude Opus 4.8](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison) respectively. Researchers can request ongoing access through the [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).

### June 11, 2026

* The [code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) now supports `code_execution_20260521`, which discloses the 90-second per-cell execution time limit in the tool description so Claude can budget long-running cells. No beta header is required.
* The [web search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool) and [web fetch tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool) now support `web_search_20260318` and `web_fetch_20260318`, adding a `response_inclusion` parameter to drop consumed result blocks from the API response for agentic workflows. No beta header is required.

### June 10, 2026

* The `GET /v1/environments/{id}/work` endpoint, which lists pending work for a [self-hosted sandbox](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes), is now available on [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws). See [IAM actions for Claude Platform on AWS](https://platform.claude.com/docs/en/api/claude-platform-on-aws-iam-actions) for the `GetEnvironment` action that authorizes it.

### June 9, 2026

* We've launched **Claude Fable 5** (`claude-fable-5`), our most capable widely released model, alongside **Claude Mythos 5** (`claude-mythos-5`) for Project Glasswing participants. Both models support a [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) by default, 128k max output tokens, and always-on [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking). See [Introducing Claude Fable 5 and Claude Mythos 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) for capabilities, API changes, and availability.
* Claude Fable 5 and Claude Mythos 5 use the tokenizer introduced with Claude Opus 4.7. Compared to models before Claude Opus 4.7, the same text produces roughly 30% more tokens. The exact increase depends on the content and workload shape. Use the [token counting API](https://platform.claude.com/docs/en/build-with-claude/token-counting#token-counts-on-claude-fable-5) with `model: "claude-fable-5"` to measure your prompts under the new tokenizer.
* Claude Fable 5 runs safety classifiers on requests and during response generation. When a classifier declines a request, the Messages API returns `stop_reason: "refusal"`. You are not billed for a request refused before any output is generated. An opt-in `fallbacks` parameter (in beta on the Claude API and Claude Platform on AWS; not supported on the Message Batches API) re-runs refused requests on another model, billed at the fallback model's rates. See [Handling stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons).
* The [`stop_details.category`](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#refusal-response) field on refusal responses now includes `"reasoning_extraction"` on Claude Fable 5, returned when a request is blocked under Anthropic's Terms of Service restrictions on reverse engineering or duplicating model outputs. The existing `"cyber"` and `"bio"` categories are unchanged. No beta header is required.
* On Claude Fable 5 and Claude Mythos 5, [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) is the only thinking mode: `thinking: {"type": "disabled"}` is not supported, and manual extended thinking budgets and assistant prefill are not supported (both return a 400 error). See [Migrating from Claude Mythos Preview to Claude Mythos 5](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-from-claude-mythos-preview).
* On Claude Fable 5 and Claude Mythos 5, `thinking.display` defaults to `"omitted"`, the same as Claude Opus 4.8, Claude Opus 4.7, and Claude Mythos Preview; set `display: "summarized"` to receive readable thinking summaries. The raw chain of thought is never returned; pass thinking blocks back unchanged in multi-turn conversations on the same model. See [Thinking output on Claude Fable 5 and Claude Mythos 5](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).
* Claude Fable 5 requires 30-day data retention and is not available under zero data retention. See [Model-specific data retention requirements](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* Claude Managed Agents now supports [scheduled deployments](https://platform.claude.com/docs/en/managed-agents/scheduled-deployments), letting you run sessions on a cron schedule without managing your own scheduler.
* Claude Managed Agents vaults now support [environment variable credentials](https://platform.claude.com/docs/en/managed-agents/vaults#add-a-credential), so you can securely inject secrets into the agent's sandbox for CLIs, SDKs, and other services that authenticate through environment variables.
* The [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api) [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed) (`GET /v1/compliance/activities`) is now available on [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws). See [IAM actions for Claude Platform on AWS](https://platform.claude.com/docs/en/api/claude-platform-on-aws-iam-actions#compliance) for the `ListComplianceActivities` action that authorizes it.
* The `session.thread_*` webhook events now include a `session_thread_id` field identifying the multiagent thread that triggered the event.
* We've released a [Swift package](https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/apple-foundation-models) in beta that adds Claude as a server-side `LanguageModel` in Apple's Foundation Models framework. Call Claude through the same `LanguageModelSession` API as Apple's on-device model on iOS 27, macOS 27, visionOS 27, and watchOS 27 (beta).

### June 5, 2026

* We announced the deprecation of the Claude Opus 4.1 model (`claude-opus-4-1-20250805`), with retirement on the Claude API scheduled for August 5, 2026. We recommend migrating to [Claude Opus 4.8](https://platform.claude.com/docs/en/about-claude/models/migration-guide). Read more in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).

### June 2, 2026

* The [advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool) now supports a `max_tokens` parameter to cap the advisor model's output per call, reducing latency and output token cost for workloads that don't need full-length advisor responses. Set `tools[].max_tokens` on the advisor tool definition; see [Capping advisor output](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool#capping-advisor-output).
* On the Claude API, you are no longer billed for a request when it returns `stop_reason: "refusal"` without Claude having generated any output. See [Streaming refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals) for detecting and handling refusals.

### May 29, 2026

* Claude Managed Agents [webhooks](https://platform.claude.com/docs/en/managed-agents/webhooks), [multiagent orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration), and [self-hosted sandboxes](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes) are now available on [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws). See [IAM actions for Claude Platform on AWS](https://platform.claude.com/docs/en/api/claude-platform-on-aws-iam-actions) for the new IAM actions and the `AnthropicSelfHostedEnvironmentAccess` managed policy.

### May 28, 2026

* We've launched **Claude Opus 4.8** (claude-opus-4-8), our most capable generally available model. Claude Opus 4.8 supports a [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) by default on the Claude API, Amazon Bedrock, Google Cloud, and Microsoft Foundry, 128k max output tokens, and the same set of tools and platform features as Claude Opus 4.7. See the [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide) for baseline settings, features, and migration guidance.
* We've launched [mid-conversation system messages](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages). On Claude Opus 4.8, you can send `role: "system"` messages after a user turn (subject to [placement rules](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages#limitations)) in the `messages` array, preserving prompt cache hits when instructions change during a long-running session. No beta header is required.
* The [`stop_details`](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#refusal-response) field on refusal responses is now publicly documented; it returns a `category` (`cyber`, `bio`, or `null`) and a human-readable `explanation`, so your application can route different classes of refusal to the right next step. No beta header is required.
* On Claude Opus 4.8, the [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) defaults to `high` across all surfaces, including Claude Code and the Messages API.
* On Claude Opus 4.8, the minimum cacheable prompt length for [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) is 1,024 tokens, lower than on Claude Opus 4.7.
* With [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) enabled, Claude Opus 4.8 triggers reasoning only when a turn needs it, reducing wasted thinking tokens compared to Claude Opus 4.7 at the same effort level.
* Claude Opus 4.8 supports [high-resolution image input](https://platform.claude.com/docs/en/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) (up to 2576 pixels on the long edge), same as Claude Opus 4.7.
* [Task budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets) now support Claude Opus 4.8.
* The [advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool) now supports Claude Opus 4.8.
* [Computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) now supports Claude Opus 4.8.
* [Fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode) for Claude Opus 4.8 is available as a research preview on the Claude API only.
* Setting the sampling parameters `temperature`, `top_p`, or `top_k` to a non-default value returns a 400 error on Claude Opus 4.8, same as on Claude Opus 4.7. See the [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide) for details.
* In Claude Code, we've expanded Auto mode to more users for long-running tasks. See the [Claude Code documentation](https://code.claude.com/docs).
* In Claude Code, Max plan users now default to [fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode) on Claude Opus 4.8. See the [Claude Code documentation](https://code.claude.com/docs).
* In Claude Code, Workflows are available as a research preview, letting you define and run multistep agentic plans. See the [Claude Code documentation](https://code.claude.com/docs).
* We've deprecated [fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode) for Claude Opus 4.6, with removal approximately 30 days after launch. Migrate to fast mode for Claude Opus 4.8 or Claude Opus 4.7. Read more in [Fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode#supported-models).
* For updates to claude.ai, Cowork, Claude for Microsoft 365, and other Claude apps in this release, see the [release notes for Claude Apps](https://support.claude.com/en/articles/12138966-release-notes).

### May 27, 2026

* The Messages API response now includes [`usage.output_tokens_details.thinking_tokens`](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#budget-rules-and-tuning), reporting how many of the billed output tokens were extended thinking. When streaming, the breakdown appears only on the final `message_delta` event. No beta header is required.

### May 19, 2026

* [MCP tunnels](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview) is now available as a research preview, so you can connect to MCP servers in your private network.
* Self-hosted sandboxes are now available for Claude Managed Agents, as an alternative to running tool execution in Anthropic's infrastructure. See [Self-hosted sandboxes](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes).
* With Claude Managed Agents, you can now update the agent's MCP server and tool configurations associated with an active session.
* With Claude Managed Agents, large outputs from `agent_toolset` and MCP tools exceeding 100K characters (about 25K tokens) are now automatically spilled to a file in the sandbox. The model receives a truncated preview with the file path and can read the full content from there.

### May 18, 2026

* The [web search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool) now returns richer SEC filing data, making it easier to ground financial research agents, earnings analysis, and due-diligence workflows in primary sources with citations.

### May 13, 2026

* We've launched [cache diagnostics](https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics) in public beta. Pass `diagnostics.previous_message_id` on a Messages request and the API reports a `cache_miss_reason` explaining where the prompt cache prefix diverged from the previous turn. Include the `cache-diagnosis-2026-04-07` beta header in your requests.

### May 12, 2026

* [Fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode) (research preview) now supports Claude Opus 4.7. Set `speed: "fast"` with `model: "claude-opus-4-7"` and the `fast-mode-2026-02-01` beta header for significantly faster output token generation at premium pricing. Pricing, rate limits, and access are the same as for Opus 4.6 fast mode; interested customers should join the [waitlist](https://claude.com/fast-mode).

### May 11, 2026

* We've launched **Claude Platform on AWS**, bringing the Claude API to Anthropic-managed infrastructure accessible through AWS, with AWS billing and IAM authentication. Access the full Messages API, Files API, Message Batches API, Claude Managed Agents, Agent Skills, code execution, and tool use through native AWS endpoints. Learn more in [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws).

### May 6, 2026

* [Multiagent orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration) and [Outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes) are now in public beta under the standard `managed-agents-2026-04-01` beta header.
* Claude Managed Agents vault credential background refresh is now supported for `mcp_oauth` credentials. See [Authenticate with vaults](https://platform.claude.com/docs/en/managed-agents/vaults).
* Webhooks for Claude Managed Agents are now supported. Webhook event types include session and vault lifecycle events. See [Subscribe to webhooks](https://platform.claude.com/docs/en/managed-agents/webhooks).
* Additional filtering and sorting options are now supported for Claude Managed Agents. Sessions can be filtered by status, and events can be filtered by type. Events can now be filtered by creation time.
* [Dreams](https://platform.claude.com/docs/en/managed-agents/dreams) for Claude Managed Agents are now available as a research preview. A dream reads an existing memory store alongside past session transcripts and produces a reorganized output memory store with duplicates merged, stale entries replaced, and new insights surfaced. Dream endpoints are gated by the `dreaming-2026-04-21` beta header. [Request access](https://claude.com/form/claude-managed-agents) to try it.

### May 4, 2026

* [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation) is now generally available. Authenticate workloads to the Claude API with short-lived OIDC tokens from your own identity provider (AWS IAM, Google Cloud, GitHub Actions, Kubernetes, Microsoft Entra ID, Okta, SPIFFE, and more) instead of long-lived static API keys. Configure issuers and federation rules in the Claude Console, and the SDK handles token exchange and refresh automatically. See [Authentication](https://platform.claude.com/docs/en/manage-claude/authentication).

### April 30, 2026

* We've retired the 1M token context window beta (`context-1m-2025-08-07`) for Claude Sonnet 4.5 and Claude Sonnet 4. The beta header now has no effect on these models, and requests exceeding the standard 200k-token context window return an error. To use the 1M context window, migrate to [Claude Sonnet 4.6](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison) or [Claude Opus 4.6](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison), where it's generally available at standard pricing with no beta header required.

### April 29, 2026

* We've released the [Claude API skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill), an open-source [Agent Skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) that gives Claude up-to-date reference material for building on the Messages API and Claude Managed Agents across 8 languages. The skill is bundled with Claude Code and available in the [Anthropic skills repository](https://github.com/anthropics/skills/tree/main/skills/claude-api).

### April 24, 2026

* We've released the [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api), allowing administrators to programmatically query the rate limits configured for their organization and workspaces.

### April 23, 2026

* Memory for Claude Managed Agents is now in public beta under the standard `managed-agents-2026-04-01` header. See [Using agent memory](https://platform.claude.com/docs/en/managed-agents/memory) for the full integration guide.

### April 20, 2026

* We've retired the Claude Haiku 3 model (`claude-3-haiku-20240307`). All requests to this model will now return an error. We recommend upgrading to [Claude Haiku 4.5](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison).

### April 16, 2026

* We've launched [Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7), our most capable generally available model for complex reasoning and agentic coding, at the same $5 / $25 per MTok pricing as Opus 4.6. See [What's new in Claude Opus 4.7](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7) for capability improvements, new features, and the updated tokenizer. Opus 4.7 includes API breaking changes versus Opus 4.6; see the [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide) before upgrading.
* [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock) is now open to all Amazon Bedrock customers. Claude Opus 4.7 and Claude Haiku 4.5 are available self-serve from the Bedrock console through the Messages API endpoint at `/anthropic/v1/messages`, in 27 AWS regions with global and regional endpoints.
* We've launched [task budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets) in beta on Claude Opus 4.7. Give Claude an advisory token budget for a full agentic loop (thinking, tool calls, tool results, and output) and the model sees a running countdown, using it to prioritize work and finish gracefully as the budget is consumed. Include the `task-budgets-2026-03-13` beta header in your requests.
* Claude Opus 4.7 supports [high-resolution image input](https://platform.claude.com/docs/en/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7), raising the maximum image resolution from 1568 to 2576 pixels on the long edge for improved performance on computer use, screenshot understanding, and document analysis. High-resolution support is automatic and requires no beta header; images may use up to approximately 3x more image tokens than on prior models.
* We've added the `xhigh` [effort](https://platform.claude.com/docs/en/build-with-claude/effort) level on Claude Opus 4.7. `xhigh` sits between `high` and `max` and is tuned for long-running agentic and coding tasks (over 30 minutes) with token budgets in the millions. No beta header is required.

### April 14, 2026

* We announced the deprecation of the Claude Sonnet 4 model (`claude-sonnet-4-20250514`) and the Claude Opus 4 model (`claude-opus-4-20250514`), with retirement on the Claude API scheduled for June 15, 2026. We recommend migrating to [Claude Sonnet 4.6](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison) and [Claude Opus 4.8](https://platform.claude.com/docs/en/about-claude/models/migration-guide) respectively. Read more in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).

### April 9, 2026

* We've launched the [advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool) in public beta. Pair a faster executor model with a higher-intelligence advisor model that provides strategic guidance mid-generation, so long-horizon agentic workloads get close to advisor-solo quality while the bulk of token generation happens at executor-model rates. Include the beta header `advisor-tool-2026-03-01` in your requests.

### April 8, 2026

* We've launched **Claude Managed Agents** in public beta, a fully managed agent harness for running Claude as an autonomous agent with secure sandboxing, built-in tools, and server-sent event streaming. Create agents, configure containers, and run sessions through the API. All endpoints require the `managed-agents-2026-04-01` beta header. Learn more in [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview).
* We've launched the **`ant` CLI**, a command-line client for the Claude API that enables faster interaction with the Claude API, native integration with Claude Code, and versioning of API resources in YAML files. Learn more in the [CLI quickstart](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/quickstart).

### April 7, 2026

* We announced [Claude Mythos Preview](https://anthropic.com/glasswing) is available as a gated research preview for defensive cybersecurity work as part of [Project Glasswing](https://anthropic.com/glasswing). Access is invitation-only.
* The [Messages API](https://platform.claude.com/docs/en/api/messages) is now available on Amazon Bedrock as a research preview. The new Claude in Amazon Bedrock endpoint at `/anthropic/v1/messages` uses the same request shape as the first-party Claude API and runs on AWS-managed infrastructure with zero operator access. Available in `us-east-1`; contact your Anthropic account executive to request access. Learn more in [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock).

### March 30, 2026

* We've raised the `max_tokens` cap to 300k on the [Message Batches API](https://platform.claude.com/docs/en/build-with-claude/batch-processing#extended-output-beta) for Claude Opus 4.6 and Sonnet 4.6. Include the `output-300k-2026-03-24` beta header to generate longer single-turn outputs for long-form content, structured data, and large code generation tasks.
* We're retiring the 1M token context window beta for Claude Sonnet 4.5 and Claude Sonnet 4 on **April 30, 2026**. After that date, the `context-1m-2025-08-07` beta header will have no effect on these models, and requests that exceed the standard 200k-token context window will return an error. To continue using 1M context windows, migrate to [Claude Sonnet 4.6](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison) or [Claude Opus 4.6](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison), which support the full 1M token context window at standard pricing with no beta header required.

### March 18, 2026

* We've added model capability fields to the [Models API](https://platform.claude.com/docs/en/api/models/list). `GET /v1/models` and `GET /v1/models/{model_id}` now return `max_input_tokens`, `max_tokens`, and a `capabilities` object. Query the API to discover what each model supports.

### March 16, 2026

* We've launched the `display` field for extended thinking, letting you omit thinking content from responses for faster streaming. Set `thinking.display: "omitted"` to receive thinking blocks with an empty `thinking` field and the `signature` preserved for multi-turn continuity. Billing is unchanged. Learn more in [Controlling thinking display](https://platform.claude.com/docs/en/build-with-claude/thinking#controlling-thinking-display).

### March 13, 2026

* The [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) is now generally available for Claude Opus 4.6 and Sonnet 4.6 at standard pricing. Requests over 200k tokens work automatically for these models with no beta header required. The 1M token context window remains in beta for Claude Sonnet 4.5 and Sonnet 4.
* We've removed the dedicated 1M rate limits for all supported models. Your standard account limits now apply across every context length.
* We've raised the media limit from 100 to 600 images or PDF pages per request when using the 1M token context window.

### February 19, 2026

* We've launched **automatic caching** for the Messages API. Add a single `cache_control` field to your request body and the system automatically caches the last cacheable block, moving the cache point forward as conversations grow. No manual breakpoint management required. Works alongside existing block-level cache control for fine-grained optimization. Available on the Claude API and Microsoft Foundry (preview). Learn more in [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#automatic-caching).
* We've retired the Claude Sonnet 3.7 model (`claude-3-7-sonnet-20250219`) and the Claude Haiku 3.5 model (`claude-3-5-haiku-20241022`). All requests to Claude Sonnet 3.7 will now return an error. Requests to Claude Haiku 3.5 on the Claude API will now return an error; it remains available on Amazon Bedrock and Google Cloud. We recommend upgrading to [Claude Sonnet 4.6](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison) and [Claude Haiku 4.5](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison) respectively. Researchers can request ongoing access through the [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).
* We announced the deprecation of the Claude Haiku 3 model (`claude-3-haiku-20240307`), with retirement scheduled for April 20, 2026. We recommend migrating to [Claude Haiku 4.5](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison). Read more in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).

### February 17, 2026

* We've launched [Claude Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6), our latest balanced model combining speed and intelligence for everyday tasks. Sonnet 4.6 delivers improved agentic search performance while consuming fewer tokens. Sonnet 4.6 supports [extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) and a [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) (beta). See [Models & Pricing](https://platform.claude.com/docs/en/about-claude/models) for details.
* API [code execution](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) is now **free when used with web search or web fetch**. Sandboxed code execution improves model capability and token efficiency. See the [pricing details](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#usage-and-pricing) for standalone usage.
* The [web search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool) and [programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) are now generally available (no beta header required). Web search and web fetch now support [dynamic filtering](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool#dynamic-filtering), which uses code execution to filter results before they reach the context window for better performance and reduced token cost.
* The [code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool), [web fetch tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool), [tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool), [tool use examples](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#providing-tool-use-examples), and [memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) are now generally available (no beta header required).

### February 7, 2026

* We've launched [fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode) in research preview for Opus 4.6, providing significantly faster output token generation through the `speed` parameter. Fast mode is up to 2.5x as fast at premium pricing. Interested customers should join the [waitlist](https://claude.com/fast-mode).

### February 5, 2026

* We've launched [Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6), our most intelligent model for complex agentic tasks and long-horizon work. Opus 4.6 recommends [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) (`thinking: {type: "adaptive"}`); manual thinking (`type: "enabled"` with `budget_tokens`) is deprecated. Opus 4.6 does not support prefilling assistant messages. Learn more in [What's new in Claude 4.6](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6).
* The [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) is now generally available (no beta header required) and supports Claude Opus 4.6. Effort replaces `budget_tokens` for controlling thinking depth on new models.
* We've launched the [compaction API](https://platform.claude.com/docs/en/build-with-claude/compaction) in beta, providing server-side context summarization for effectively infinite conversations. Available on Opus 4.6.
* We've introduced [data residency controls](https://platform.claude.com/docs/en/manage-claude/data-residency), allowing you to specify where model inference runs with the `inference_geo` parameter. US-only inference is available at 1.1x pricing for models released after February 1, 2026.
* The [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) is now available in beta for Claude Opus 4.6, in addition to Sonnet 4.5 and Sonnet 4. [Long context pricing](https://platform.claude.com/docs/en/about-claude/pricing#long-context-pricing) applies to requests exceeding 200k input tokens.
* [Fine-grained tool streaming](https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming) is now generally available on all models and platforms (no beta header required).

### January 29, 2026

* [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) are now generally available on the Claude API for Claude Sonnet 4.5, Claude Opus 4.5, and Claude Haiku 4.5. GA includes expanded schema support, improved grammar compilation latency, and a simplified integration path with no beta header required. The `output_format` parameter has moved to `output_config.format`. Existing beta users can continue using the beta header during the transition period. Structured outputs remain in public beta on Amazon Bedrock and Microsoft Foundry.

### January 12, 2026

* `console.anthropic.com` now redirects to `platform.claude.com`. The Claude Console has moved to its new home as part of our Claude brand consolidation. Existing bookmarks and links will continue working through an automatic redirect. For more details, see the [September 16, 2025 announcement](https://platform.claude.com/docs/en/release-notes/overview#september-16-2025).

### January 5, 2026

* We've retired the Claude Opus 3 model (`claude-3-opus-20240229`). All requests to this model will now return an error. We recommend upgrading to [Claude Opus 4.5](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison), which offers significantly improved intelligence at a third of the cost. Researchers can request ongoing access to Claude Opus 3 on the API through the [External Researcher Access Program](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program).

### December 19, 2025

* We announced the deprecation of the Claude Haiku 3.5 model. Read more in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).

### December 4, 2025

* [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) now supports Claude Haiku 4.5.

### November 24, 2025

* We've launched [Claude Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5), our most intelligent model combining maximum capability with practical performance. Ideal for complex specialized tasks, professional software engineering, and advanced agents. Features step-change improvements in vision, coding, and computer use at a more accessible price point than previous Opus models. Learn more in [Models overview](https://platform.claude.com/docs/en/about-claude/models).
* We've launched [programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) in public beta, allowing Claude to call tools from within code execution to reduce latency and token usage in multi-tool workflows.
* We've launched the [tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) in public beta, enabling Claude to dynamically discover and load tools on-demand from large tool catalogs.
* We've launched the [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) in public beta for Claude Opus 4.5, allowing you to control token usage by trading off between response thoroughness and efficiency.
* We've added [client-side compaction](https://platform.claude.com/docs/en/build-with-claude/context-editing#client-side-compaction-sdk) to our Python and TypeScript SDKs, automatically managing conversation context through summarization when using `tool_runner`.

### November 21, 2025

* Search result content blocks are now generally available on Amazon Bedrock. Learn more in [Search results](https://platform.claude.com/docs/en/build-with-claude/search-results).

### November 19, 2025

* We've launched a **new documentation platform** at [platform.claude.com/docs](https://platform.claude.com/docs). Our documentation now lives side by side with the Claude Console, providing a unified developer experience. The previous docs site at docs.claude.com will redirect to the new location.

### November 18, 2025

* We've launched **Claude in Microsoft Foundry**, bringing Claude models to Azure customers with Azure billing and OAuth authentication. Access the full Messages API including extended thinking, prompt caching (5-minute and 1-hour), PDF support, Files API, Agent Skills, and tool use. Learn more in [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry).

### November 14, 2025

* We've launched [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) in public beta, providing guaranteed schema conformance for Claude's responses. Use JSON outputs for structured data responses or strict tool use for validated tool inputs. Available for Claude Sonnet 4.5 and Claude Opus 4.1. To enable, use the beta header `structured-outputs-2025-11-13`.

### October 28, 2025

* We announced the deprecation of the Claude Sonnet 3.7 model. Read more in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).
* We've retired the Claude Sonnet 3.5 models. All requests to these models will now return an error.
* We've expanded context editing with thinking block clearing (`clear_thinking_20251015`), enabling automatic management of thinking blocks. Learn more in [Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing).

### October 16, 2025

* We've launched [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (`skills-2025-10-02` beta), a new way to extend Claude's capabilities. Skills are organized folders of instructions, scripts, and resources that Claude loads dynamically to perform specialized tasks. The initial release includes:

  * **Anthropic-managed Skills**: Pre-built Skills for working with PowerPoint (.pptx), Excel (.xlsx), Word (.docx), and PDF files
  * **Custom Skills**: Upload your own Skills through the Skills API (`/v1/skills` endpoints) to package domain expertise and organizational workflows
  * Skills require the [code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) to be enabled
  * Learn more in [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) and [API reference](https://platform.claude.com/docs/en/api/skills/create)

### October 15, 2025

* We've launched [Claude Haiku 4.5](https://www.anthropic.com/news/claude-haiku-4-5), our fastest and most intelligent Haiku model with near-frontier performance. Ideal for real-time applications, high-volume processing, and cost-sensitive deployments requiring strong reasoning. Learn more in [Models overview](https://platform.claude.com/docs/en/about-claude/models).

### September 29, 2025

* We've launched [Claude Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5), our best model for complex agents and coding, with the highest intelligence across most tasks. Learn more in the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview).
* We've introduced [global endpoint pricing](https://platform.claude.com/docs/en/about-claude/pricing#cloud-platform-pricing) for Amazon Bedrock and Vertex AI. The Claude API (1P) pricing is unaffected.
* We've introduced a new stop reason `model_context_window_exceeded` that allows you to request the maximum possible tokens without calculating input size. Learn more in [Handling stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons).
* We've launched the memory tool in beta, enabling Claude to store and consult information across conversations. Learn more in [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool).
* We've launched context editing in beta, providing strategies to automatically manage conversation context. The initial release supports clearing older tool results and calls when approaching token limits. Learn more in [Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing).

### September 17, 2025

* We've launched tool helpers in beta for the Python and TypeScript SDKs, simplifying tool creation and execution with type-safe input validation and a tool runner for automated tool handling in conversations. For details, see the documentation for [the Python SDK](https://github.com/anthropics/anthropic-sdk-python/blob/main/tools.md) and [the TypeScript SDK](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/helpers.md#tool-helpers).

### September 16, 2025

* We've unified our developer offerings under the Claude brand. You should see updated naming and URLs across our platform and documentation, but **our developer interfaces will remain the same**. Here are some notable changes:

  * Claude Console ([console.anthropic.com](https://console.anthropic.com)) → Claude Console ([platform.claude.com](https://platform.claude.com)). The console will be available at both URLs until January 12, 2026. After that date, [console.anthropic.com](https://console.anthropic.com) will automatically redirect to [platform.claude.com](https://platform.claude.com).
  * Anthropic Docs ([docs.anthropic.com](https://docs.anthropic.com)) → Claude Docs ([docs.claude.com](https://docs.claude.com))
  * Anthropic Help Center ([support.anthropic.com](https://support.anthropic.com)) → Claude Help Center ([support.claude.com](https://support.claude.com))
  * API endpoints, headers, environment variables, and SDKs remain the same. Your existing integrations will continue working without any changes.

### September 10, 2025

* We've launched the web fetch tool in beta, allowing Claude to retrieve full content from specified web pages and PDF documents. Learn more in [Web fetch tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool).
* We've launched the [Claude Code Analytics API](https://platform.claude.com/docs/en/manage-claude/claude-code-analytics-api), enabling organizations to programmatically access daily aggregated usage metrics for Claude Code, including productivity metrics, tool usage statistics, and cost data.

### September 8, 2025

* We launched a beta version of the [C# SDK](https://github.com/anthropics/anthropic-sdk-csharp).

### September 5, 2025

* We've launched [rate limit charts](https://platform.claude.com/docs/en/api/rate-limits#monitoring-your-rate-limits-in-the-console) in the Console [Usage](https://console.anthropic.com/settings/usage) page, allowing you to monitor your API rate limit usage and caching rates over time.

### September 3, 2025

* We've launched support for citable documents in client-side tool results. Learn more in [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).

### September 2, 2025

* We've launched v2 of the [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) in public beta, replacing the original Python-only tool with Bash command execution and direct file manipulation capabilities, including writing code in other languages.

### August 27, 2025

* We launched a beta version of the [PHP SDK](https://github.com/anthropics/anthropic-sdk-php).

### August 26, 2025

* We've increased rate limits on the [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) for Claude Sonnet 4 on the Claude API.
* The 1M token context window is now available on Vertex AI. For more information, see [Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai).

### August 19, 2025

* Request IDs are now included directly in error response bodies alongside the existing `request-id` header. Learn more in [Errors](https://platform.claude.com/docs/en/api/errors#error-shapes).

### August 18, 2025

* We've released the [Usage & Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api), allowing administrators to programmatically monitor their organization's usage and cost data.
* We've added a new endpoint to the Admin API for retrieving organization information. For details, see the [Organization Info Admin API reference](https://platform.claude.com/docs/en/api/admin-api/organization/get-me).

### August 13, 2025

* We announced the deprecation of the Claude Sonnet 3.5 models (`claude-3-5-sonnet-20240620` and `claude-3-5-sonnet-20241022`). These models will be retired on October 28, 2025. We recommend migrating to Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`) for improved performance and capabilities. Read more in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).
* The 1-hour cache duration for prompt caching is now generally available. You can now use the extended cache TTL without a beta header. Learn more in [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#1-hour-cache-duration).

### August 12, 2025

* We've launched beta support for a [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) in Claude Sonnet 4 on the Claude API and Amazon Bedrock.

### August 11, 2025

* Some customers might encounter 429 (`rate_limit_error`) [errors](https://platform.claude.com/docs/en/api/errors) following a sharp increase in API usage due to acceleration limits on the API. Previously, 529 (`overloaded_error`) errors would occur in similar scenarios.

### August 8, 2025

* Search result content blocks are now generally available on the Claude API and Vertex AI. This feature enables natural citations for RAG applications with proper source attribution. The beta header `search-results-2025-06-09` is no longer required. Learn more in [Search results](https://platform.claude.com/docs/en/build-with-claude/search-results).

### August 5, 2025

* We've launched [Claude Opus 4.1](https://www.anthropic.com/news/claude-opus-4-1), an incremental update to Claude Opus 4 with enhanced capabilities and performance improvements.\* Learn more in [Models overview](https://platform.claude.com/docs/en/about-claude/models).

*\*Opus 4.1 does not allow both `temperature` and `top_p` parameters to be specified. Please use only one.*

### July 28, 2025

* We've released `text_editor_20250728`, an updated text editor tool that fixes some issues from the previous versions and adds an optional `max_characters` parameter that allows you to control the truncation length when viewing large files.

### July 24, 2025

* We've increased [rate limits](https://platform.claude.com/docs/en/api/rate-limits) for Claude Opus 4 on the Claude API to give you more capacity to build and scale with Claude. For customers with [usage tier 1-4 rate limits](https://platform.claude.com/docs/en/api/rate-limits#rate-limits), these changes apply immediately to your account - no action needed.

### July 21, 2025

* We've retired the Claude 2.0, Claude 2.1, and Claude Sonnet 3 models. All requests to these models will now return an error. Read more in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).

### July 17, 2025

* We've increased [rate limits](https://platform.claude.com/docs/en/api/rate-limits) for Claude Sonnet 4 on the Claude API to give you more capacity to build and scale with Claude. For customers with [usage tier 1-4 rate limits](https://platform.claude.com/docs/en/api/rate-limits#rate-limits), these changes apply immediately to your account - no action needed.

### July 3, 2025

* We've launched search result content blocks in beta, enabling natural citations for RAG applications. Tools can now return search results with proper source attribution, and Claude will automatically cite these sources in its responses - matching the citation quality of web search. This eliminates the need for document workarounds in custom knowledge base applications. Learn more in [Search results](https://platform.claude.com/docs/en/build-with-claude/search-results). To enable this feature, use the beta header `search-results-2025-06-09`.

### June 30, 2025

* We announced the deprecation of the Claude Opus 3 model. Read more in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).

### June 23, 2025

* Console users with the Developer role can now access the [Cost](https://console.anthropic.com/settings/cost) page. Previously, the Developer role allowed access to the [Usage](https://console.anthropic.com/settings/usage) page, but not the Cost page.

### June 11, 2025

* We've launched [fine-grained tool streaming](https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming) in public beta, a feature that enables Claude to stream tool use parameters without buffering / JSON validation. To enable fine-grained tool streaming, use the [beta header](https://platform.claude.com/docs/en/api/beta-headers) `fine-grained-tool-streaming-2025-05-14`.

### May 22, 2025

* We've launched [Claude Opus 4 and Claude Sonnet 4](https://www.anthropic.com/news/claude-4), our latest models with extended thinking capabilities. Learn more in [Models overview](https://platform.claude.com/docs/en/about-claude/models).
* The default behavior of [extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) in Claude 4 models returns a summary of Claude's full thinking process, with the full thinking encrypted and returned in the `signature` field of `thinking` block output.
* We've launched [interleaved thinking](https://platform.claude.com/docs/en/build-with-claude/thinking#interleaved-thinking) in public beta, a feature that enables Claude to think in between tool calls. To enable interleaved thinking, use the [beta header](https://platform.claude.com/docs/en/api/beta-headers) `interleaved-thinking-2025-05-14`.
* We've launched the [Files API](https://platform.claude.com/docs/en/build-with-claude/files) in public beta, enabling you to upload files and reference them in the Messages API and code execution tool.
* We've launched the [Code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) in public beta, a tool that enables Claude to execute Python code in a secure, sandboxed environment.
* We've launched the [MCP connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector) in public beta, a feature that allows you to connect to remote MCP servers directly from the Messages API.
* To increase answer quality and decrease tool errors, we've changed the default value for the `top_p` [nucleus sampling](https://en.wikipedia.org/wiki/Top-p_sampling) parameter in the Messages API from 0.999 to 0.99 for all models. To revert this change, set `top_p` to 0.999. Additionally, when extended thinking is enabled, you can now set `top_p` to values between 0.95 and 1.
* We've moved our [Go SDK](https://github.com/anthropics/anthropic-sdk-go) from beta to GA.
* We've included minute and hour level granularity to the [Usage](https://console.anthropic.com/settings/usage) page of Console alongside 429 error rates on the Usage page.

### May 21, 2025

* We've moved our [Ruby SDK](https://github.com/anthropics/anthropic-sdk-ruby) from beta to GA.

### May 7, 2025

* We've launched a web search tool in the API, allowing Claude to access up-to-date information from the web. Learn more in [Web search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool).

### May 1, 2025

* Cache control must now be specified directly in the parent `content` block of `tool_result` and `document.source`. For backwards compatibility, if cache control is detected on the last block in `tool_result.content` or `document.source.content`, it will be automatically applied to the parent block instead. Cache control on any other blocks within `tool_result.content` and `document.source.content` will result in a validation error.

### April 9th, 2025

* We launched a beta version of the [Ruby SDK](https://github.com/anthropics/anthropic-sdk-ruby).

### March 31st, 2025

* We've moved our [Java SDK](https://github.com/anthropics/anthropic-sdk-java) from beta to GA.
* We've moved our [Go SDK](https://github.com/anthropics/anthropic-sdk-go) from alpha to beta.

### February 27th, 2025

* We've added URL source blocks for images and PDFs in the Messages API. You can now reference images and PDFs directly through a URL instead of having to base64-encode them. Learn more in [Vision](https://platform.claude.com/docs/en/build-with-claude/vision) and [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support).
* We've added support for a `none` option to the `tool_choice` parameter in the Messages API that prevents Claude from calling any tools. Additionally, you're no longer required to provide any `tools` when including `tool_use` and `tool_result` blocks.
* We've launched an OpenAI-compatible API endpoint, allowing you to test Claude models by changing just your API key, base URL, and model name in existing OpenAI integrations. This compatibility layer supports core chat completions functionality. Learn more in [OpenAI SDK compatibility](https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk).

### February 24th, 2025

* We've launched [Claude Sonnet 3.7](https://www.anthropic.com/news/claude-3-7-sonnet), our most intelligent model yet. Claude Sonnet 3.7 can produce near-instant responses or show its extended thinking step-by-step. One model, two ways to think. Learn more about all Claude models in [Models overview](https://platform.claude.com/docs/en/about-claude/models).

* We've added vision support to Claude Haiku 3.5, enabling the model to analyze and understand images.

* We've released a token-efficient tool use implementation, improving overall performance when using tools with Claude. Learn more in [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

* We've changed the default temperature in the [Console](https://console.anthropic.com/workbench) for new prompts from 0 to 1 for consistency with the default temperature in the API. Existing saved prompts are unchanged.

* We've released updated versions of our tools that decouple the text edit and bash tools from the computer use system prompt:

  * `bash_20250124`: Same functionality as previous version but is independent from computer use. Does not require a beta header.
  * `text_editor_20250124`: Same functionality as previous version but is independent from computer use. Does not require a beta header.
  * `computer_20250124`: Updated computer use tool with new command options including "hold\_key", "left\_mouse\_down", "left\_mouse\_up", "scroll", "triple\_click", and "wait". This tool requires the "computer-use-2025-01-24" anthropic-beta header. Learn more in [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

### February 10th, 2025

* We've added the `anthropic-organization-id` response header to all API responses. This header provides the organization ID associated with the API key used in the request.

### January 31st, 2025

* We've moved our [Java SDK](https://github.com/anthropics/anthropic-sdk-java) from alpha to beta.

### January 23rd, 2025

* We've launched citations capability in the API, allowing Claude to provide source attribution for information. Learn more in [Citations](https://platform.claude.com/docs/en/build-with-claude/citations).
* We've added support for plain text documents and custom content documents in the Messages API.

### January 21st, 2025

* We announced the deprecation of the Claude 2, Claude 2.1, and Claude Sonnet 3 models. Read more in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).

### January 15th, 2025

* We've updated [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) to be easier to use. Now, when you set a cache breakpoint, we'll automatically read from your longest previously cached prefix.
* You can now put words in Claude's mouth when using tools.

### January 10th, 2025

* We've optimized support for [prompt caching in the Message Batches API](https://platform.claude.com/docs/en/build-with-claude/batch-processing#using-prompt-caching-with-message-batches) to improve cache hit rate.

### December 19th, 2024

* We've added support for a [delete endpoint](https://platform.claude.com/docs/en/api/deleting-message-batches) in the Message Batches API.

### December 17th, 2024

The following features are now generally available in the Claude API:

* [Models API](https://platform.claude.com/docs/en/api/models/list): Query available models, validate model IDs, and resolve [model aliases](https://platform.claude.com/docs/en/about-claude/models/overview) to their canonical model IDs.
* [Message Batches API](https://platform.claude.com/docs/en/build-with-claude/batch-processing): Process large batches of messages asynchronously at 50% of the standard API cost.
* [Token counting API](https://platform.claude.com/docs/en/build-with-claude/token-counting): Calculate token counts for Messages before sending them to Claude.
* [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching): Reduce costs by up to 90% and latency by up to 80% by caching and reusing prompt content.
* [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support): Process PDFs to analyze both text and visual content within documents.

We also released new official SDKs:

* [Java SDK](https://github.com/anthropics/anthropic-sdk-java) (alpha)
* [Go SDK](https://github.com/anthropics/anthropic-sdk-go) (alpha)

### December 4th, 2024

* We've added the ability to group by API key on the [Usage](https://console.anthropic.com/settings/usage) and [Cost](https://console.anthropic.com/settings/cost) pages of the [Developer Console](https://console.anthropic.com).
* We've added two new **Last used at** and **Cost** columns and the ability to sort by any column on the [API keys](https://console.anthropic.com/settings/keys) page of the [Developer Console](https://console.anthropic.com).

### November 21st, 2024

* We've released the [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api), allowing users to programmatically manage their organization's resources.

### November 20th, 2024

* We've updated our rate limits for the Messages API. We've replaced the tokens per minute rate limit with new input and output tokens per minute rate limits. Read more in [Rate limits](https://platform.claude.com/docs/en/api/rate-limits).
* We've added support for [tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) in the [Workbench](https://console.anthropic.com/workbench).

### November 13th, 2024

* We've added PDF support for all Claude Sonnet 3.5 models. Read more in [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support).

### November 6th, 2024

* We've retired the Claude 1 and Instant models. Read more in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).

### November 4th, 2024

* [Claude Haiku 3.5](https://www.anthropic.com/claude/haiku) is now available on the Claude API as a text-only model.

### November 1st, 2024

* We've added PDF support for use with the new Claude Sonnet 3.5. Read more in [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support).
* We've also added token counting, which allows you to determine the total number of tokens in a Message prior to sending it to Claude. Read more in [Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting).

### October 22nd, 2024

* We've added Anthropic-defined computer use tools to our API for use with the new Claude Sonnet 3.5. Read more in [Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool).
* Claude Sonnet 3.5, our most intelligent model yet, just got an upgrade and is now available on the Claude API. Read more in the [Claude Sonnet documentation](https://www.anthropic.com/claude/sonnet).

### October 8th, 2024

* The Message Batches API is now available in beta. Process large batches of queries asynchronously in the Claude API for 50% less cost. Read more in [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing).
* We've loosened restrictions on the ordering of `user`/`assistant` turns in our Messages API. Consecutive `user`/`assistant` messages will be combined into a single message instead of erroring, and we no longer require the first input message to be a `user` message.
* We've deprecated the Build and Scale plans in favor of a standard feature suite (formerly referred to as Build), along with additional features that are available through sales. Read more in our [API pricing information](https://claude.com/platform/api).

### October 3rd, 2024

* We've added the ability to disable parallel tool use in the API. Set `disable_parallel_tool_use: true` in the `tool_choice` field to ensure that Claude uses at most one tool. Read more in [Parallel tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use).

### September 10th, 2024

* We've added Workspaces to the [Developer Console](https://console.anthropic.com). Workspaces allow you to set custom spend or rate limits, group API keys, track usage by project, and control access with user roles. Read more in our [blog post](https://www.anthropic.com/news/workspaces).

### September 4th, 2024

* We announced the deprecation of the Claude 1 models. Read more in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).

### August 22nd, 2024

* We've added support for usage of the SDK in browsers by returning CORS headers in the API responses. Set `dangerouslyAllowBrowser: true` in the SDK instantiation to enable this feature.

### August 19th, 2024

* We've moved 8,192 token outputs from beta to general availability for Claude Sonnet 3.5.

### August 14th, 2024

* [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) is now available as a beta feature in the Claude API. Cache and re-use prompts to reduce latency by up to 80% and costs by up to 90%.

### July 15th, 2024

* Generate outputs up to 8,192 tokens in length from Claude Sonnet 3.5 with the new `anthropic-beta: max-tokens-3-5-sonnet-2024-07-15` header.

### July 9th, 2024

* Automatically generate test cases for your prompts using Claude in the [Developer Console](https://console.anthropic.com).
* Compare the outputs from different prompts side by side in the new output comparison mode in the [Developer Console](https://console.anthropic.com).

### June 27th, 2024

* View API usage and billing broken down by dollar amount, token count, and API keys in the new [Usage](https://console.anthropic.com/settings/usage) and [Cost](https://console.anthropic.com/settings/cost) tabs in the [Developer Console](https://console.anthropic.com).
* View your current API rate limits in the new [Rate Limits](https://console.anthropic.com/settings/limits) tab in the [Developer Console](https://console.anthropic.com).

### June 20th, 2024

* [Claude Sonnet 3.5](https://www.anthropic.com/news/claude-3-5-sonnet), our most intelligent model yet, is now generally available across the Claude API, Amazon Bedrock, and Vertex AI.

### May 30th, 2024

* [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) is now generally available across the Claude API, Amazon Bedrock, and Vertex AI.

### May 10th, 2024

* Our prompt generator tool is now available in the [Developer Console](https://console.anthropic.com). Prompt Generator makes it easy to guide Claude to generate a high-quality prompts tailored to your specific tasks. Read more in our [blog post](https://www.anthropic.com/news/prompt-generator).
