---
title: Reference
url: https://platform.claude.com/docs/en/managed-agents/reference
description: Event types, self-hosted worker CLI flags, supported MCP server types, rate limits, and branding guidelines for Claude Managed Agents.
---

This page collects reference material for Claude Managed Agents. For task-oriented guides, follow the links in each section. For the operations on the session resource, see [Session operations](https://platform.claude.com/docs/en/managed-agents/session-operations).

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](https://platform.claude.com/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## Event types

Persisted event type strings follow a `{domain}.{action}` naming convention; the stream-only event deltas (see the Event deltas tab) are the exception. See [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming) for sending, streaming, and listing events.

<Tabs>
  <Tab title="User events">
    | Type                      | Description                                                                                                                                                                                                                                          |
    | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `user.message`            | A user message with text, image, or document content.                                                                                                                                                                                                |
    | `user.interrupt`          | Stop the agent mid-execution.                                                                                                                                                                                                                        |
    | `user.custom_tool_result` | Response to a custom tool call from the agent.                                                                                                                                                                                                       |
    | `user.tool_confirmation`  | Approve or deny an agent or MCP tool call when a permission policy requires confirmation.                                                                                                                                                            |
    | `user.define_outcome`     | Define an [outcome](https://platform.claude.com/docs/en/managed-agents/define-outcomes) for the agent to work toward.                                                                                                                                |
    | `user.tool_result`        | For sessions with `self_hosted` [environments](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes) only, your integration is responsible for providing `agent_toolset` results. The SDK helpers and CLI do this automatically. |
  </Tab>

  <Tab title="Agent events">
    | Type                             | Description                                                                                                                                                                                                                                                                    |
    | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | `agent.message`                  | Agent response content blocks.                                                                                                                                                                                                                                                 |
    | `agent.thinking`                 | Signals the agent is making forward progress through extended thinking. This is a progress signal only and does not carry the thinking content.                                                                                                                                |
    | `agent.tool_use`                 | Agent invokes a pre-built agent tool (bash, file operations, and so on).                                                                                                                                                                                                       |
    | `agent.tool_result`              | Result of a pre-built agent tool execution.                                                                                                                                                                                                                                    |
    | `agent.mcp_tool_use`             | Agent invokes an MCP server tool.                                                                                                                                                                                                                                              |
    | `agent.mcp_tool_result`          | Result of an MCP tool execution.                                                                                                                                                                                                                                               |
    | `agent.custom_tool_use`          | Agent invokes one of your custom tools. Respond with a `user.custom_tool_result` event.                                                                                                                                                                                        |
    | `agent.thread_context_compacted` | Conversation history was compacted to fit the context window.                                                                                                                                                                                                                  |
    | `agent.thread_message_received`  | In a [multiagent](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration) session, a message from another thread arrived on the thread whose stream carries this event; on the primary thread, an agent sent a report or question to the coordinator.     |
    | `agent.thread_message_sent`      | In a [multiagent](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration) session, the thread whose stream carries this event sent a message to another thread; on the primary thread, the coordinator sent a task or follow-up message to another agent. |

    Message content in these events can include a `redacted` content block, `{"type": "redacted"}`: a placeholder for content withheld by Anthropic model policy. The block carries no other fields. Redacted blocks appear only in content the platform emits; a user event that includes one is rejected with a 400 error.
  </Tab>

  <Tab title="Session events">
    | Type                                | Description                                                                                                                                                                                                                                                     |
    | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `session.status_running`            | Agent is actively processing.                                                                                                                                                                                                                                   |
    | `session.status_idle`               | Agent finished its current task and is waiting for input. Includes a `stop_reason` indicating why the agent stopped.                                                                                                                                            |
    | `session.status_rescheduled`        | A transient error occurred and the session is retrying automatically.                                                                                                                                                                                           |
    | `session.status_terminated`         | Session ended, either because of an unrecoverable error or because it was archived.                                                                                                                                                                             |
    | `session.deleted`                   | Session was deleted. Terminates any active event stream; no further events are emitted for this session.                                                                                                                                                        |
    | `session.updated`                   | Session update request changed at least one field. Includes only the fields that changed. Updates apply on the next turn.                                                                                                                                       |
    | `session.error`                     | An error occurred during processing. Includes a typed `error` object with a `retry_status`.                                                                                                                                                                     |
    | `session.usage`                     | Snapshot of the session's cumulative usage and tracked list cost. Carries the session's usage totals and an echo of the session's [budget](https://platform.claude.com/docs/en/managed-agents/budgets), or `null` when the session has none.                    |
    | `session.thread_created`            | A [multiagent](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration) thread was created.                                                                                                                                                 |
    | `session.thread_status_running`     | A session thread began executing. Every session emits this for its primary thread; in [multiagent](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration) sessions, child-thread transitions are also cross-posted to the primary stream. |
    | `session.thread_status_idle`        | A session thread finished its turn and is awaiting input. Includes `stop_reason`.                                                                                                                                                                               |
    | `session.thread_status_rescheduled` | A session thread hit a transient error and is retrying automatically.                                                                                                                                                                                           |
    | `session.thread_status_terminated`  | A session thread was archived or reached a terminal error.                                                                                                                                                                                                      |
  </Tab>

  <Tab title="Span events">
    Span events are observability markers that wrap activity for timing and usage tracking.

    | Type                              | Description                                                                                                                                                                                                                                              |
    | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `span.model_request_start`        | A model inference call has started.                                                                                                                                                                                                                      |
    | `span.model_request_end`          | A model inference call has completed. Includes `model_usage` with token counts.                                                                                                                                                                          |
    | `span.outcome_evaluation_start`   | [Outcome](https://platform.claude.com/docs/en/managed-agents/define-outcomes) evaluation has started.                                                                                                                                                    |
    | `span.outcome_evaluation_ongoing` | Heartbeat during an ongoing [outcome](https://platform.claude.com/docs/en/managed-agents/define-outcomes) evaluation.                                                                                                                                    |
    | `span.outcome_evaluation_end`     | An [outcome](https://platform.claude.com/docs/en/managed-agents/define-outcomes) evaluation cycle has completed. A `needs_revision` result means another cycle follows; `satisfied`, `max_iterations_reached`, `failed`, and `interrupted` are terminal. |
  </Tab>

  <Tab title="System events">
    | Type             | Description                                                                                                                                                                                                                                                                                           |
    | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `system.message` | Append privileged system-level context that applies to the accompanying turn and all subsequent turns. Supported on Claude Opus 4.8, Claude Fable 5, Claude Mythos 5, and Claude Opus 5; on an unsupported primary model the event is rejected with `model_does_not_support_mid_conversation_system`. |
  </Tab>

  <Tab title="Event deltas">
    Event deltas are stream-only preview events. They are emitted on stream connections (session-level or per-thread) that opt in with the `event_deltas[]` parameter, and they are never persisted to the session's event history. See [Event deltas](https://platform.claude.com/docs/en/managed-agents/events-and-streaming#event-deltas) for opting in, accumulating, and reconciling them.

    | Type          | Description                                                                                                              |
    | ------------- | ------------------------------------------------------------------------------------------------------------------------ |
    | `event_start` | A previewed event has started generating. Carries the upcoming event's `type` and `id`. Stream-only and never persisted. |
    | `event_delta` | Incremental content for a previewed event, identified by `event_id`. Stream-only and never persisted.                    |
  </Tab>
</Tabs>

## Self-hosted worker

These are the `ant beta:worker` CLI flags for the pre-built worker that drives a `self_hosted` environment. See [Self-hosted sandboxes](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes) for setting up the environment, running a worker, and the SDK helper options.

| Flag                   | Description                                                                                                                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--environment-id`     | The environment to poll for work. Also reads from `ANTHROPIC_ENVIRONMENT_ID`.                                                                                                         |
| `--environment-key`    | Authenticates the worker with this environment. Also reads from `ANTHROPIC_ENVIRONMENT_KEY`.                                                                                          |
| `--workdir`            | Directory where skills are downloaded and tools read and write files. Defaults to `.` (the current directory); the system default working directory is `/workspace`.                  |
| `--on-work`            | Script to call for each claimed work item instead of running tools in-process. Receives session details as environment variables.                                                     |
| `--unrestricted-paths` | Allow the file tools to read and write paths outside `--workdir`. The workdir check is a guardrail for the file tools only, not a sandbox; it does not constrain bash.                |
| `--max-idle`           | How long to wait after the session goes idle with an `end_turn` [stop reason](https://platform.claude.com/docs/en/api/handling-stop-reasons) before shutting down. Defaults to `60s`. |
| `--log-format`         | Log output format. Use `json` for structured log ingestion. Defaults to `text`.                                                                                                       |

The CLI worker does not mount [memory stores](https://platform.claude.com/docs/en/managed-agents/memory): a session that attaches one still runs, but the agent finds nothing at the store's `mount_path` and no changes sync back to the store. To use memory stores in sessions on a self-hosted environment, run the SDK worker instead; see [Use memory stores](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#use-memory-stores).

## Supported MCP server types

Claude Managed Agents connects to [remote MCP servers](https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers) that expose an HTTP endpoint, or to private MCP servers through [MCP tunnels](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview). The server should support the MCP protocol's streamable HTTP transport; servers that only support the deprecated SSE transport still work through an automatic fallback. See [MCP connector](https://platform.claude.com/docs/en/managed-agents/mcp-connector) for declaring servers on an agent.

For more information on MCP and building MCP servers, see the [MCP documentation](https://modelcontextprotocol.io).

## Rate limits

Managed Agents endpoints are rate-limited per organization:

| Operation                                                     | Limit                     |
| ------------------------------------------------------------- | ------------------------- |
| Create endpoints (such as agents, sessions, and environments) | 300 requests per minute   |
| Read endpoints (such as retrieve, list, and stream)           | 1,200 requests per minute |

Organization-level [spend limits and usage-tier rate limits](https://platform.claude.com/docs/en/api/rate-limits) also apply.

## Branding guidelines

For partners integrating Claude Managed Agents, use of Claude branding is optional. When referencing Claude in your product:

**Allowed:**

* "Claude Agent" (preferred for dropdown menus)
* "Claude" (when within a menu already labeled "Agents")
* "\{YourAgentName} Powered by Claude" (if you have an existing agent name)

**Not permitted:**

* "Claude Code" or "Claude Code Agent"
* "Claude Cowork" or "Claude Cowork Agent"
* Claude Code-branded ASCII art or visual elements that mimic Claude Code

Your product should maintain its own branding and not appear to be Claude Code, Claude Cowork, or any other Anthropic product. For questions about branding compliance, contact the Anthropic [sales team](https://www.anthropic.com/contact-sales).
