> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Agent SDK reference - TypeScript

> Complete API reference for the TypeScript Agent SDK, including all functions, types, and interfaces.

<script src="/components/typescript-sdk-type-links.js" defer />

<Note>
  **Try the new V2 interface (preview):** A simplified interface with `send()` and `stream()` patterns is now available, making multi-turn conversations easier. [Learn more about the TypeScript V2 preview](/en/agent-sdk/typescript-v2-preview)
</Note>

## Installation

```bash theme={null}
npm install @anthropic-ai/claude-agent-sdk
```

## Functions

### `query()`

The primary function for interacting with Claude Code. Creates an async generator that streams messages as they arrive.

```typescript theme={null}
function query({
  prompt,
  options
}: {
  prompt: string | AsyncIterable<SDKUserMessage>;
  options?: Options;
}): Query;
```

#### Parameters

| Parameter | Type                                                              | Description                                                       |
| :-------- | :---------------------------------------------------------------- | :---------------------------------------------------------------- |
| `prompt`  | `string \| AsyncIterable<`[`SDKUserMessage`](#sdkuser-message)`>` | The input prompt as a string or async iterable for streaming mode |
| `options` | [`Options`](#options)                                             | Optional configuration object (see Options type below)            |

#### Returns

Returns a [`Query`](#query-object) object that extends `AsyncGenerator<`[`SDKMessage`](#sdk-message)`, void>` with additional methods.

### `startup()`

Pre-warms the CLI subprocess by spawning it and completing the initialize handshake before a prompt is available. The returned [`WarmQuery`](#warm-query) handle accepts a prompt later and writes it to an already-ready process, so the first `query()` call resolves without paying subprocess spawn and initialization cost inline.

```typescript theme={null}
function startup(params?: {
  options?: Options;
  initializeTimeoutMs?: number;
}): Promise<WarmQuery>;
```

#### Parameters

| Parameter             | Type                  | Description                                                                                                                                                                    |
| :-------------------- | :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `options`             | [`Options`](#options) | Optional configuration object. Same as the `options` parameter to `query()`                                                                                                    |
| `initializeTimeoutMs` | `number`              | Maximum time in milliseconds to wait for subprocess initialization. Defaults to `60000`. If initialization does not complete in time, the promise rejects with a timeout error |

#### Returns

Returns a `Promise<`[`WarmQuery`](#warm-query)`>` that resolves once the subprocess has spawned and completed its initialize handshake.

#### Example

Call `startup()` early, for example on application boot, then call `.query()` on the returned handle once a prompt is ready. This moves subprocess spawn and initialization out of the critical path.

```typescript theme={null}
import { startup } from "@anthropic-ai/claude-agent-sdk";

// Pay startup cost upfront
const warm = await startup({ options: { maxTurns: 3 } });

// Later, when a prompt is ready, this is immediate
for await (const message of warm.query("What files are here?")) {
  console.log(message);
}
```

### `tool()`

Creates a type-safe MCP tool definition for use with SDK MCP servers.

```typescript theme={null}
function tool<Schema extends AnyZodRawShape>(
  name: string,
  description: string,
  inputSchema: Schema,
  handler: (args: InferShape<Schema>, extra: unknown) => Promise<CallToolResult>,
  extras?: { annotations?: ToolAnnotations }
): SdkMcpToolDefinition<Schema>;
```

#### Parameters

| Parameter     | Type                                                                | Description                                                                     |
| :------------ | :------------------------------------------------------------------ | :------------------------------------------------------------------------------ |
| `name`        | `string`                                                            | The name of the tool                                                            |
| `description` | `string`                                                            | A description of what the tool does                                             |
| `inputSchema` | `Schema extends AnyZodRawShape`                                     | Zod schema defining the tool's input parameters (supports both Zod 3 and Zod 4) |
| `handler`     | `(args, extra) => Promise<`[`CallToolResult`](#call-tool-result)`>` | Async function that executes the tool logic                                     |
| `extras`      | `{ annotations?: `[`ToolAnnotations`](#tool-annotations)` }`        | Optional MCP tool annotations providing behavioral hints to clients             |

#### `ToolAnnotations`

Re-exported from `@modelcontextprotocol/sdk/types.js`. All fields are optional hints; clients should not rely on them for security decisions.

| Field             | Type      | Default     | Description                                                                                                                                          |
| :---------------- | :-------- | :---------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| `title`           | `string`  | `undefined` | Human-readable title for the tool                                                                                                                    |
| `readOnlyHint`    | `boolean` | `false`     | If `true`, the tool does not modify its environment                                                                                                  |
| `destructiveHint` | `boolean` | `true`      | If `true`, the tool may perform destructive updates (only meaningful when `readOnlyHint` is `false`)                                                 |
| `idempotentHint`  | `boolean` | `false`     | If `true`, repeated calls with the same arguments have no additional effect (only meaningful when `readOnlyHint` is `false`)                         |
| `openWorldHint`   | `boolean` | `true`      | If `true`, the tool interacts with external entities (for example, web search). If `false`, the tool's domain is closed (for example, a memory tool) |

```typescript theme={null}
import { tool } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const searchTool = tool(
  "search",
  "Search the web",
  { query: z.string() },
  async ({ query }) => {
    return { content: [{ type: "text", text: `Results for: ${query}` }] };
  },
  { annotations: { readOnlyHint: true, openWorldHint: true } }
);
```

### `createSdkMcpServer()`

Creates an MCP server instance that runs in the same process as your application.

```typescript theme={null}
function createSdkMcpServer(options: {
  name: string;
  version?: string;
  tools?: Array<SdkMcpToolDefinition<any>>;
}): McpSdkServerConfigWithInstance;
```

#### Parameters

| Parameter         | Type                          | Description                                              |
| :---------------- | :---------------------------- | :------------------------------------------------------- |
| `options.name`    | `string`                      | The name of the MCP server                               |
| `options.version` | `string`                      | Optional version string                                  |
| `options.tools`   | `Array<SdkMcpToolDefinition>` | Array of tool definitions created with [`tool()`](#tool) |

### `listSessions()`

Discovers and lists past sessions with light metadata. Filter by project directory or list sessions across all projects.

```typescript theme={null}
function listSessions(options?: ListSessionsOptions): Promise<SDKSessionInfo[]>;
```

#### Parameters

| Parameter                  | Type      | Default     | Description                                                                        |
| :------------------------- | :-------- | :---------- | :--------------------------------------------------------------------------------- |
| `options.dir`              | `string`  | `undefined` | Directory to list sessions for. When omitted, returns sessions across all projects |
| `options.limit`            | `number`  | `undefined` | Maximum number of sessions to return                                               |
| `options.includeWorktrees` | `boolean` | `true`      | When `dir` is inside a git repository, include sessions from all worktree paths    |

#### Return type: `SDKSessionInfo`

| Property       | Type                  | Description                                                                 |
| :------------- | :-------------------- | :-------------------------------------------------------------------------- |
| `sessionId`    | `string`              | Unique session identifier (UUID)                                            |
| `summary`      | `string`              | Display title: custom title, auto-generated summary, or first prompt        |
| `lastModified` | `number`              | Last modified time in milliseconds since epoch                              |
| `fileSize`     | `number \| undefined` | Session file size in bytes. Only populated for local JSONL storage          |
| `customTitle`  | `string \| undefined` | User-set session title (via `/rename`)                                      |
| `firstPrompt`  | `string \| undefined` | First meaningful user prompt in the session                                 |
| `gitBranch`    | `string \| undefined` | Git branch at the end of the session                                        |
| `cwd`          | `string \| undefined` | Working directory for the session                                           |
| `tag`          | `string \| undefined` | User-set session tag (see [`tagSession()`](#tag-session))                   |
| `createdAt`    | `number \| undefined` | Creation time in milliseconds since epoch, from the first entry's timestamp |

#### Example

Print the 10 most recent sessions for a project. Results are sorted by `lastModified` descending, so the first item is the newest. Omit `dir` to search across all projects.

```typescript theme={null}
import { listSessions } from "@anthropic-ai/claude-agent-sdk";

const sessions = await listSessions({ dir: "/path/to/project", limit: 10 });

for (const session of sessions) {
  console.log(`${session.summary} (${session.sessionId})`);
}
```

### `getSessionMessages()`

Reads user and assistant messages from a past session transcript.

```typescript theme={null}
function getSessionMessages(
  sessionId: string,
  options?: GetSessionMessagesOptions
): Promise<SessionMessage[]>;
```

#### Parameters

| Parameter        | Type     | Default     | Description                                                                   |
| :--------------- | :------- | :---------- | :---------------------------------------------------------------------------- |
| `sessionId`      | `string` | required    | Session UUID to read (see `listSessions()`)                                   |
| `options.dir`    | `string` | `undefined` | Project directory to find the session in. When omitted, searches all projects |
| `options.limit`  | `number` | `undefined` | Maximum number of messages to return                                          |
| `options.offset` | `number` | `undefined` | Number of messages to skip from the start                                     |

#### Return type: `SessionMessage`

| Property             | Type                    | Description                             |
| :------------------- | :---------------------- | :-------------------------------------- |
| `type`               | `"user" \| "assistant"` | Message role                            |
| `uuid`               | `string`                | Unique message identifier               |
| `session_id`         | `string`                | Session this message belongs to         |
| `message`            | `unknown`               | Raw message payload from the transcript |
| `parent_tool_use_id` | `null`                  | Reserved                                |

#### Example

```typescript theme={null}
import { listSessions, getSessionMessages } from "@anthropic-ai/claude-agent-sdk";

const [latest] = await listSessions({ dir: "/path/to/project", limit: 1 });

if (latest) {
  const messages = await getSessionMessages(latest.sessionId, {
    dir: "/path/to/project",
    limit: 20
  });

  for (const msg of messages) {
    console.log(`[${msg.type}] ${msg.uuid}`);
  }
}
```

### `getSessionInfo()`

Reads metadata for a single session by ID without scanning the full project directory.

```typescript theme={null}
function getSessionInfo(
  sessionId: string,
  options?: GetSessionInfoOptions
): Promise<SDKSessionInfo | undefined>;
```

#### Parameters

| Parameter     | Type     | Default     | Description                                                            |
| :------------ | :------- | :---------- | :--------------------------------------------------------------------- |
| `sessionId`   | `string` | required    | UUID of the session to look up                                         |
| `options.dir` | `string` | `undefined` | Project directory path. When omitted, searches all project directories |

Returns [`SDKSessionInfo`](#return-type-sdk-session-info), or `undefined` if the session is not found.

### `renameSession()`

Renames a session by appending a custom-title entry. Repeated calls are safe; the most recent title wins.

```typescript theme={null}
function renameSession(
  sessionId: string,
  title: string,
  options?: SessionMutationOptions
): Promise<void>;
```

#### Parameters

| Parameter     | Type     | Default     | Description                                                            |
| :------------ | :------- | :---------- | :--------------------------------------------------------------------- |
| `sessionId`   | `string` | required    | UUID of the session to rename                                          |
| `title`       | `string` | required    | New title. Must be non-empty after trimming whitespace                 |
| `options.dir` | `string` | `undefined` | Project directory path. When omitted, searches all project directories |

### `tagSession()`

Tags a session. Pass `null` to clear the tag. Repeated calls are safe; the most recent tag wins.

```typescript theme={null}
function tagSession(
  sessionId: string,
  tag: string | null,
  options?: SessionMutationOptions
): Promise<void>;
```

#### Parameters

| Parameter     | Type             | Default     | Description                                                            |
| :------------ | :--------------- | :---------- | :--------------------------------------------------------------------- |
| `sessionId`   | `string`         | required    | UUID of the session to tag                                             |
| `tag`         | `string \| null` | required    | Tag string, or `null` to clear                                         |
| `options.dir` | `string`         | `undefined` | Project directory path. When omitted, searches all project directories |

## Types

### `Options`

Configuration object for the `query()` function.

| Property                          | Type                                                                                                     | Default                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| :-------------------------------- | :------------------------------------------------------------------------------------------------------- | :------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `abortController`                 | `AbortController`                                                                                        | `new AbortController()`                     | Controller for cancelling operations                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `additionalDirectories`           | `string[]`                                                                                               | `[]`                                        | Additional directories Claude can access                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `agent`                           | `string`                                                                                                 | `undefined`                                 | Agent name for the main thread. The agent must be defined in the `agents` option or in settings                                                                                                                                                                                                                                                                                                                                                                                     |
| `agents`                          | `Record<string, [`AgentDefinition`](#agent-definition)>`                                                 | `undefined`                                 | Programmatically define subagents                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `allowDangerouslySkipPermissions` | `boolean`                                                                                                | `false`                                     | Enable bypassing permissions. Required when using `permissionMode: 'bypassPermissions'`                                                                                                                                                                                                                                                                                                                                                                                             |
| `allowedTools`                    | `string[]`                                                                                               | `[]`                                        | Tools to auto-approve without prompting. This does not restrict Claude to only these tools; unlisted tools fall through to `permissionMode` and `canUseTool`. Use `disallowedTools` to block tools. See [Permissions](/en/agent-sdk/permissions#allow-and-deny-rules)                                                                                                                                                                                                               |
| `betas`                           | [`SdkBeta`](#sdk-beta)`[]`                                                                               | `[]`                                        | Enable beta features                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `canUseTool`                      | [`CanUseTool`](#can-use-tool)                                                                            | `undefined`                                 | Custom permission function for tool usage                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `continue`                        | `boolean`                                                                                                | `false`                                     | Continue the most recent conversation                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `cwd`                             | `string`                                                                                                 | `process.cwd()`                             | Current working directory                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `debug`                           | `boolean`                                                                                                | `false`                                     | Enable debug mode for the Claude Code process                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `debugFile`                       | `string`                                                                                                 | `undefined`                                 | Write debug logs to a specific file path. Implicitly enables debug mode                                                                                                                                                                                                                                                                                                                                                                                                             |
| `disallowedTools`                 | `string[]`                                                                                               | `[]`                                        | Tools to always deny. Deny rules are checked first and override `allowedTools` and `permissionMode` (including `bypassPermissions`)                                                                                                                                                                                                                                                                                                                                                 |
| `effort`                          | `'low' \| 'medium' \| 'high' \| 'xhigh' \| 'max'`                                                        | `'high'`                                    | Controls how much effort Claude puts into its response. Works with adaptive thinking to guide thinking depth                                                                                                                                                                                                                                                                                                                                                                        |
| `enableFileCheckpointing`         | `boolean`                                                                                                | `false`                                     | Enable file change tracking for rewinding. See [File checkpointing](/en/agent-sdk/file-checkpointing)                                                                                                                                                                                                                                                                                                                                                                               |
| `env`                             | `Record<string, string \| undefined>`                                                                    | `process.env`                               | Environment variables. Set `CLAUDE_AGENT_SDK_CLIENT_APP` to identify your app in the User-Agent header                                                                                                                                                                                                                                                                                                                                                                              |
| `executable`                      | `'bun' \| 'deno' \| 'node'`                                                                              | Auto-detected                               | JavaScript runtime to use                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `executableArgs`                  | `string[]`                                                                                               | `[]`                                        | Arguments to pass to the executable                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `extraArgs`                       | `Record<string, string \| null>`                                                                         | `{}`                                        | Additional arguments                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `fallbackModel`                   | `string`                                                                                                 | `undefined`                                 | Model to use if primary fails                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `forkSession`                     | `boolean`                                                                                                | `false`                                     | When resuming with `resume`, fork to a new session ID instead of continuing the original session                                                                                                                                                                                                                                                                                                                                                                                    |
| `hooks`                           | `Partial<Record<`[`HookEvent`](#hook-event)`, `[`HookCallbackMatcher`](#hook-callback-matcher)`[]>>`     | `{}`                                        | Hook callbacks for events                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `includePartialMessages`          | `boolean`                                                                                                | `false`                                     | Include partial message events                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `maxBudgetUsd`                    | `number`                                                                                                 | `undefined`                                 | Stop the query when the client-side cost estimate reaches this USD value. Compared against the same estimate as `total_cost_usd`; see [Track cost and usage](/en/agent-sdk/cost-tracking) for accuracy caveats                                                                                                                                                                                                                                                                      |
| `maxThinkingTokens`               | `number`                                                                                                 | `undefined`                                 | *Deprecated:* Use `thinking` instead. Maximum tokens for thinking process                                                                                                                                                                                                                                                                                                                                                                                                           |
| `maxTurns`                        | `number`                                                                                                 | `undefined`                                 | Maximum agentic turns (tool-use round trips)                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `mcpServers`                      | `Record<string, [`McpServerConfig`](#mcp-server-config)>`                                                | `{}`                                        | MCP server configurations                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `model`                           | `string`                                                                                                 | Default from CLI                            | Claude model to use                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `outputFormat`                    | `{ type: 'json_schema', schema: JSONSchema }`                                                            | `undefined`                                 | Define output format for agent results. See [Structured outputs](/en/agent-sdk/structured-outputs) for details                                                                                                                                                                                                                                                                                                                                                                      |
| `pathToClaudeCodeExecutable`      | `string`                                                                                                 | Uses built-in executable                    | Path to Claude Code executable                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `permissionMode`                  | [`PermissionMode`](#permission-mode)                                                                     | `'default'`                                 | Permission mode for the session                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `permissionPromptToolName`        | `string`                                                                                                 | `undefined`                                 | MCP tool name for permission prompts                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `persistSession`                  | `boolean`                                                                                                | `true`                                      | When `false`, disables session persistence to disk. Sessions cannot be resumed later                                                                                                                                                                                                                                                                                                                                                                                                |
| `plugins`                         | [`SdkPluginConfig`](#sdk-plugin-config)`[]`                                                              | `[]`                                        | Load custom plugins from local paths. See [Plugins](/en/agent-sdk/plugins) for details                                                                                                                                                                                                                                                                                                                                                                                              |
| `promptSuggestions`               | `boolean`                                                                                                | `false`                                     | Enable prompt suggestions. Emits a `prompt_suggestion` message after each turn with a predicted next user prompt                                                                                                                                                                                                                                                                                                                                                                    |
| `resume`                          | `string`                                                                                                 | `undefined`                                 | Session ID to resume                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `resumeSessionAt`                 | `string`                                                                                                 | `undefined`                                 | Resume session at a specific message UUID                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `sandbox`                         | [`SandboxSettings`](#sandbox-settings)                                                                   | `undefined`                                 | Configure sandbox behavior programmatically. See [Sandbox settings](#sandbox-settings) for details                                                                                                                                                                                                                                                                                                                                                                                  |
| `sessionId`                       | `string`                                                                                                 | Auto-generated                              | Use a specific UUID for the session instead of auto-generating one                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `settingSources`                  | [`SettingSource`](#setting-source)`[]`                                                                   | CLI defaults (all sources)                  | Control which filesystem settings to load. Pass `[]` to disable user, project, and local settings. Managed policy settings load regardless. See [Use Claude Code features](/en/agent-sdk/claude-code-features#what-settingsources-does-not-control)                                                                                                                                                                                                                                 |
| `spawnClaudeCodeProcess`          | `(options: SpawnOptions) => SpawnedProcess`                                                              | `undefined`                                 | Custom function to spawn the Claude Code process. Use to run Claude Code in VMs, containers, or remote environments                                                                                                                                                                                                                                                                                                                                                                 |
| `stderr`                          | `(data: string) => void`                                                                                 | `undefined`                                 | Callback for stderr output                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `strictMcpConfig`                 | `boolean`                                                                                                | `false`                                     | Enforce strict MCP validation                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `systemPrompt`                    | `string \| { type: 'preset'; preset: 'claude_code'; append?: string; excludeDynamicSections?: boolean }` | `undefined` (minimal prompt)                | System prompt configuration. Pass a string for custom prompt, or `{ type: 'preset', preset: 'claude_code' }` to use Claude Code's system prompt. When using the preset object form, add `append` to extend it with additional instructions, and set `excludeDynamicSections: true` to move per-session context into the first user message for [better prompt-cache reuse across machines](/en/agent-sdk/modifying-system-prompts#improve-prompt-caching-across-users-and-machines) |
| `thinking`                        | [`ThinkingConfig`](#thinking-config)                                                                     | `{ type: 'adaptive' }` for supported models | Controls Claude's thinking/reasoning behavior. See [`ThinkingConfig`](#thinking-config) for options                                                                                                                                                                                                                                                                                                                                                                                 |
| `toolConfig`                      | [`ToolConfig`](#tool-config)                                                                             | `undefined`                                 | Configuration for built-in tool behavior. See [`ToolConfig`](#tool-config) for details                                                                                                                                                                                                                                                                                                                                                                                              |
| `tools`                           | `string[] \| { type: 'preset'; preset: 'claude_code' }`                                                  | `undefined`                                 | Tool configuration. Pass an array of tool names or use the preset to get Claude Code's default tools                                                                                                                                                                                                                                                                                                                                                                                |

### `Query` object

Interface returned by the `query()` function.

```typescript theme={null}
interface Query extends AsyncGenerator<SDKMessage, void> {
  interrupt(): Promise<void>;
  rewindFiles(
    userMessageId: string,
    options?: { dryRun?: boolean }
  ): Promise<RewindFilesResult>;
  setPermissionMode(mode: PermissionMode): Promise<void>;
  setModel(model?: string): Promise<void>;
  setMaxThinkingTokens(maxThinkingTokens: number | null): Promise<void>;
  initializationResult(): Promise<SDKControlInitializeResponse>;
  supportedCommands(): Promise<SlashCommand[]>;
  supportedModels(): Promise<ModelInfo[]>;
  supportedAgents(): Promise<AgentInfo[]>;
  mcpServerStatus(): Promise<McpServerStatus[]>;
  accountInfo(): Promise<AccountInfo>;
  reconnectMcpServer(serverName: string): Promise<void>;
  toggleMcpServer(serverName: string, enabled: boolean): Promise<void>;
  setMcpServers(servers: Record<string, McpServerConfig>): Promise<McpSetServersResult>;
  streamInput(stream: AsyncIterable<SDKUserMessage>): Promise<void>;
  stopTask(taskId: string): Promise<void>;
  close(): void;
}
```

#### Methods

| Method                                 | Description                                                                                                                                                                                                   |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `interrupt()`                          | Interrupts the query (only available in streaming input mode)                                                                                                                                                 |
| `rewindFiles(userMessageId, options?)` | Restores files to their state at the specified user message. Pass `{ dryRun: true }` to preview changes. Requires `enableFileCheckpointing: true`. See [File checkpointing](/en/agent-sdk/file-checkpointing) |
| `setPermissionMode()`                  | Changes the permission mode (only available in streaming input mode)                                                                                                                                          |
| `setModel()`                           | Changes the model (only available in streaming input mode)                                                                                                                                                    |
| `setMaxThinkingTokens()`               | *Deprecated:* Use the `thinking` option instead. Changes the maximum thinking tokens                                                                                                                          |
| `initializationResult()`               | Returns the full initialization result including supported commands, models, account info, and output style configuration                                                                                     |
| `supportedCommands()`                  | Returns available slash commands                                                                                                                                                                              |
| `supportedModels()`                    | Returns available models with display info                                                                                                                                                                    |
| `supportedAgents()`                    | Returns available subagents as [`AgentInfo`](#agent-info)`[]`                                                                                                                                                 |
| `mcpServerStatus()`                    | Returns status of connected MCP servers                                                                                                                                                                       |
| `accountInfo()`                        | Returns account information                                                                                                                                                                                   |
| `reconnectMcpServer(serverName)`       | Reconnect an MCP server by name                                                                                                                                                                               |
| `toggleMcpServer(serverName, enabled)` | Enable or disable an MCP server by name                                                                                                                                                                       |
| `setMcpServers(servers)`               | Dynamically replace the set of MCP servers for this session. Returns info about which servers were added, removed, and any errors                                                                             |
| `streamInput(stream)`                  | Stream input messages to the query for multi-turn conversations                                                                                                                                               |
| `stopTask(taskId)`                     | Stop a running background task by ID                                                                                                                                                                          |
| `close()`                              | Close the query and terminate the underlying process. Forcefully ends the query and cleans up all resources                                                                                                   |

### `WarmQuery`

Handle returned by [`startup()`](#startup). The subprocess is already spawned and initialized, so calling `query()` on this handle writes the prompt directly to a ready process with no startup latency.

```typescript theme={null}
interface WarmQuery extends AsyncDisposable {
  query(prompt: string | AsyncIterable<SDKUserMessage>): Query;
  close(): void;
}
```

#### Methods

| Method          | Description                                                                                                               |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `query(prompt)` | Send a prompt to the pre-warmed subprocess and return a [`Query`](#query-object). Can only be called once per `WarmQuery` |
| `close()`       | Close the subprocess without sending a prompt. Use this to discard a warm query that is no longer needed                  |

`WarmQuery` implements `AsyncDisposable`, so it can be used with `await using` for automatic cleanup.

### `SDKControlInitializeResponse`

Return type of `initializationResult()`. Contains session initialization data.

```typescript theme={null}
type SDKControlInitializeResponse = {
  commands: SlashCommand[];
  agents: AgentInfo[];
  output_style: string;
  available_output_styles: string[];
  models: ModelInfo[];
  account: AccountInfo;
  fast_mode_state?: "off" | "cooldown" | "on";
};
```

### `AgentDefinition`

Configuration for a subagent defined programmatically.

```typescript theme={null}
type AgentDefinition = {
  description: string;
  tools?: string[];
  disallowedTools?: string[];
  prompt: string;
  model?: "sonnet" | "opus" | "haiku" | "inherit";
  mcpServers?: AgentMcpServerSpec[];
  skills?: string[];
  maxTurns?: number;
  criticalSystemReminder_EXPERIMENTAL?: string;
};
```

| Field                                 | Required | Description                                                                   |
| :------------------------------------ | :------- | :---------------------------------------------------------------------------- |
| `description`                         | Yes      | Natural language description of when to use this agent                        |
| `tools`                               | No       | Array of allowed tool names. If omitted, inherits all tools from parent       |
| `disallowedTools`                     | No       | Array of tool names to explicitly disallow for this agent                     |
| `prompt`                              | Yes      | The agent's system prompt                                                     |
| `model`                               | No       | Model override for this agent. If omitted or `'inherit'`, uses the main model |
| `mcpServers`                          | No       | MCP server specifications for this agent                                      |
| `skills`                              | No       | Array of skill names to preload into the agent context                        |
| `maxTurns`                            | No       | Maximum number of agentic turns (API round-trips) before stopping             |
| `criticalSystemReminder_EXPERIMENTAL` | No       | Experimental: Critical reminder added to the system prompt                    |

### `AgentMcpServerSpec`

Specifies MCP servers available to a subagent. Can be a server name (string referencing a server from the parent's `mcpServers` config) or an inline server configuration record mapping server names to configs.

```typescript theme={null}
type AgentMcpServerSpec = string | Record<string, McpServerConfigForProcessTransport>;
```

Where `McpServerConfigForProcessTransport` is `McpStdioServerConfig | McpSSEServerConfig | McpHttpServerConfig | McpSdkServerConfig`.

### `SettingSource`

Controls which filesystem-based configuration sources the SDK loads settings from.

```typescript theme={null}
type SettingSource = "user" | "project" | "local";
```

| Value       | Description                                  | Location                      |
| :---------- | :------------------------------------------- | :---------------------------- |
| `'user'`    | Global user settings                         | `~/.claude/settings.json`     |
| `'project'` | Shared project settings (version controlled) | `.claude/settings.json`       |
| `'local'`   | Local project settings (gitignored)          | `.claude/settings.local.json` |

#### Default behavior

When `settingSources` is omitted or `undefined`, `query()` loads the same filesystem settings as the Claude Code CLI: user, project, and local. Managed policy settings are loaded in all cases. See [What settingSources does not control](/en/agent-sdk/claude-code-features#what-settingsources-does-not-control) for inputs that are read regardless of this option, and how to disable them.

#### Why use settingSources

**Disable filesystem settings:**

```typescript theme={null}
// Do not load user, project, or local settings from disk
const result = query({
  prompt: "Analyze this code",
  options: { settingSources: [] }
});
```

**Load all filesystem settings explicitly:**

```typescript theme={null}
const result = query({
  prompt: "Analyze this code",
  options: {
    settingSources: ["user", "project", "local"] // Load all settings
  }
});
```

**Load only specific setting sources:**

```typescript theme={null}
// Load only project settings, ignore user and local
const result = query({
  prompt: "Run CI checks",
  options: {
    settingSources: ["project"] // Only .claude/settings.json
  }
});
```

**Testing and CI environments:**

```typescript theme={null}
// Ensure consistent behavior in CI by excluding local settings
const result = query({
  prompt: "Run tests",
  options: {
    settingSources: ["project"], // Only team-shared settings
    permissionMode: "bypassPermissions"
  }
});
```

**SDK-only applications:**

```typescript theme={null}
// Define everything programmatically.
// Pass [] to opt out of filesystem setting sources.
const result = query({
  prompt: "Review this PR",
  options: {
    settingSources: [],
    agents: {
      /* ... */
    },
    mcpServers: {
      /* ... */
    },
    allowedTools: ["Read", "Grep", "Glob"]
  }
});
```

**Loading CLAUDE.md project instructions:**

```typescript theme={null}
// Load project settings to include CLAUDE.md files
const result = query({
  prompt: "Add a new feature following project conventions",
  options: {
    systemPrompt: {
      type: "preset",
      preset: "claude_code" // Use Claude Code's system prompt
    },
    settingSources: ["project"], // Loads CLAUDE.md from project directory
    allowedTools: ["Read", "Write", "Edit"]
  }
});
```

#### Settings precedence

When multiple sources are loaded, settings are merged with this precedence (highest to lowest):

1. Local settings (`.claude/settings.local.json`)
2. Project settings (`.claude/settings.json`)
3. User settings (`~/.claude/settings.json`)

Programmatic options such as `agents` and `allowedTools` override user, project, and local filesystem settings. Managed policy settings take precedence over programmatic options.

### `PermissionMode`

```typescript theme={null}
type PermissionMode =
  | "default" // Standard permission behavior
  | "acceptEdits" // Auto-accept file edits
  | "bypassPermissions" // Bypass all permission checks
  | "plan" // Planning mode - no execution
  | "dontAsk" // Don't prompt for permissions, deny if not pre-approved
  | "auto"; // Use a model classifier to approve or deny each tool call
```

### `CanUseTool`

Custom permission function type for controlling tool usage.

```typescript theme={null}
type CanUseTool = (
  toolName: string,
  input: Record<string, unknown>,
  options: {
    signal: AbortSignal;
    suggestions?: PermissionUpdate[];
    blockedPath?: string;
    decisionReason?: string;
    toolUseID: string;
    agentID?: string;
  }
) => Promise<PermissionResult>;
```

| Option           | Type                                         | Description                                                                  |
| :--------------- | :------------------------------------------- | :--------------------------------------------------------------------------- |
| `signal`         | `AbortSignal`                                | Signaled if the operation should be aborted                                  |
| `suggestions`    | [`PermissionUpdate`](#permission-update)`[]` | Suggested permission updates so the user is not prompted again for this tool |
| `blockedPath`    | `string`                                     | The file path that triggered the permission request, if applicable           |
| `decisionReason` | `string`                                     | Explains why this permission request was triggered                           |
| `toolUseID`      | `string`                                     | Unique identifier for this specific tool call within the assistant message   |
| `agentID`        | `string`                                     | If running within a sub-agent, the sub-agent's ID                            |

### `PermissionResult`

Result of a permission check.

```typescript theme={null}
type PermissionResult =
  | {
      behavior: "allow";
      updatedInput?: Record<string, unknown>;
      updatedPermissions?: PermissionUpdate[];
      toolUseID?: string;
    }
  | {
      behavior: "deny";
      message: string;
      interrupt?: boolean;
      toolUseID?: string;
    };
```

### `ToolConfig`

Configuration for built-in tool behavior.

```typescript theme={null}
type ToolConfig = {
  askUserQuestion?: {
    previewFormat?: "markdown" | "html";
  };
};
```

| Field                           | Type                   | Description                                                                                                                                                                   |
| :------------------------------ | :--------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `askUserQuestion.previewFormat` | `'markdown' \| 'html'` | Opts into the `preview` field on [`AskUserQuestion`](/en/agent-sdk/user-input#question-format) options and sets its content format. When unset, Claude does not emit previews |

### `McpServerConfig`

Configuration for MCP servers.

```typescript theme={null}
type McpServerConfig =
  | McpStdioServerConfig
  | McpSSEServerConfig
  | McpHttpServerConfig
  | McpSdkServerConfigWithInstance;
```

#### `McpStdioServerConfig`

```typescript theme={null}
type McpStdioServerConfig = {
  type?: "stdio";
  command: string;
  args?: string[];
  env?: Record<string, string>;
};
```

#### `McpSSEServerConfig`

```typescript theme={null}
type McpSSEServerConfig = {
  type: "sse";
  url: string;
  headers?: Record<string, string>;
};
```

#### `McpHttpServerConfig`

```typescript theme={null}
type McpHttpServerConfig = {
  type: "http";
  url: string;
  headers?: Record<string, string>;
};
```

#### `McpSdkServerConfigWithInstance`

```typescript theme={null}
type McpSdkServerConfigWithInstance = {
  type: "sdk";
  name: string;
  instance: McpServer;
};
```

#### `McpClaudeAIProxyServerConfig`

```typescript theme={null}
type McpClaudeAIProxyServerConfig = {
  type: "claudeai-proxy";
  url: string;
  id: string;
};
```

### `SdkPluginConfig`

Configuration for loading plugins in the SDK.

```typescript theme={null}
type SdkPluginConfig = {
  type: "local";
  path: string;
};
```

| Field  | Type      | Description                                                |
| :----- | :-------- | :--------------------------------------------------------- |
| `type` | `'local'` | Must be `'local'` (only local plugins currently supported) |
| `path` | `string`  | Absolute or relative path to the plugin directory          |

**Example:**

```typescript theme={null}
plugins: [
  { type: "local", path: "./my-plugin" },
  { type: "local", path: "/absolute/path/to/plugin" }
];
```

For complete information on creating and using plugins, see [Plugins](/en/agent-sdk/plugins).

## Message Types

### `SDKMessage`

Union type of all possible messages returned by the query.

```typescript theme={null}
type SDKMessage =
  | SDKAssistantMessage
  | SDKUserMessage
  | SDKUserMessageReplay
  | SDKResultMessage
  | SDKSystemMessage
  | SDKPartialAssistantMessage
  | SDKCompactBoundaryMessage
  | SDKStatusMessage
  | SDKLocalCommandOutputMessage
  | SDKHookStartedMessage
  | SDKHookProgressMessage
  | SDKHookResponseMessage
  | SDKPluginInstallMessage
  | SDKToolProgressMessage
  | SDKAuthStatusMessage
  | SDKTaskNotificationMessage
  | SDKTaskStartedMessage
  | SDKTaskProgressMessage
  | SDKFilesPersistedEvent
  | SDKToolUseSummaryMessage
  | SDKRateLimitEvent
  | SDKPromptSuggestionMessage;
```

### `SDKAssistantMessage`

Assistant response message.

```typescript theme={null}
type SDKAssistantMessage = {
  type: "assistant";
  uuid: UUID;
  session_id: string;
  message: BetaMessage; // From Anthropic SDK
  parent_tool_use_id: string | null;
  error?: SDKAssistantMessageError;
};
```

The `message` field is a [`BetaMessage`](https://platform.claude.com/docs/en/api/messages/create) from the Anthropic SDK. It includes fields like `id`, `content`, `model`, `stop_reason`, and `usage`.

`SDKAssistantMessageError` is one of: `'authentication_failed'`, `'billing_error'`, `'rate_limit'`, `'invalid_request'`, `'server_error'`, `'max_output_tokens'`, or `'unknown'`.

### `SDKUserMessage`

User input message.

```typescript theme={null}
type SDKUserMessage = {
  type: "user";
  uuid?: UUID;
  session_id: string;
  message: MessageParam; // From Anthropic SDK
  parent_tool_use_id: string | null;
  isSynthetic?: boolean;
  shouldQuery?: boolean;
  tool_use_result?: unknown;
};
```

Set `shouldQuery` to `false` to append the message to the transcript without triggering an assistant turn. The message is held and merged into the next user message that does trigger a turn. Use this to inject context, such as the output of a command you ran out of band, without spending a model call on it.

### `SDKUserMessageReplay`

Replayed user message with required UUID.

```typescript theme={null}
type SDKUserMessageReplay = {
  type: "user";
  uuid: UUID;
  session_id: string;
  message: MessageParam;
  parent_tool_use_id: string | null;
  isSynthetic?: boolean;
  tool_use_result?: unknown;
  isReplay: true;
};
```

### `SDKResultMessage`

Final result message.

```typescript theme={null}
type SDKResultMessage =
  | {
      type: "result";
      subtype: "success";
      uuid: UUID;
      session_id: string;
      duration_ms: number;
      duration_api_ms: number;
      is_error: boolean;
      num_turns: number;
      result: string;
      stop_reason: string | null;
      total_cost_usd: number;
      usage: NonNullableUsage;
      modelUsage: { [modelName: string]: ModelUsage };
      permission_denials: SDKPermissionDenial[];
      structured_output?: unknown;
    }
  | {
      type: "result";
      subtype:
        | "error_max_turns"
        | "error_during_execution"
        | "error_max_budget_usd"
        | "error_max_structured_output_retries";
      uuid: UUID;
      session_id: string;
      duration_ms: number;
      duration_api_ms: number;
      is_error: boolean;
      num_turns: number;
      stop_reason: string | null;
      total_cost_usd: number;
      usage: NonNullableUsage;
      modelUsage: { [modelName: string]: ModelUsage };
      permission_denials: SDKPermissionDenial[];
      errors: string[];
    };
```

### `SDKSystemMessage`

System initialization message.

```typescript theme={null}
type SDKSystemMessage = {
  type: "system";
  subtype: "init";
  uuid: UUID;
  session_id: string;
  agents?: string[];
  apiKeySource: ApiKeySource;
  betas?: string[];
  claude_code_version: string;
  cwd: string;
  tools: string[];
  mcp_servers: {
    name: string;
    status: string;
  }[];
  model: string;
  permissionMode: PermissionMode;
  slash_commands: string[];
  output_style: string;
  skills: string[];
  plugins: { name: string; path: string }[];
};
```

### `SDKPartialAssistantMessage`

Streaming partial message (only when `includePartialMessages` is true).

```typescript theme={null}
type SDKPartialAssistantMessage = {
  type: "stream_event";
  event: BetaRawMessageStreamEvent; // From Anthropic SDK
  parent_tool_use_id: string | null;
  uuid: UUID;
  session_id: string;
};
```

### `SDKCompactBoundaryMessage`

Message indicating a conversation compaction boundary.

```typescript theme={null}
type SDKCompactBoundaryMessage = {
  type: "system";
  subtype: "compact_boundary";
  uuid: UUID;
  session_id: string;
  compact_metadata: {
    trigger: "manual" | "auto";
    pre_tokens: number;
  };
};
```

### `SDKPluginInstallMessage`

Plugin installation progress event. Emitted when [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/en/env-vars) is set, so your Agent SDK application can track marketplace plugin installation before the first turn. The `started` and `completed` statuses bracket the overall install. The `installed` and `failed` statuses report individual marketplaces and include `name`.

```typescript theme={null}
type SDKPluginInstallMessage = {
  type: "system";
  subtype: "plugin_install";
  status: "started" | "installed" | "failed" | "completed";
  name?: string;
  error?: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKPermissionDenial`

Information about a denied tool use.

```typescript theme={null}
type SDKPermissionDenial = {
  tool_name: string;
  tool_use_id: string;
  tool_input: Record<string, unknown>;
};
```

## Hook Types

For a comprehensive guide on using hooks with examples and common patterns, see the [Hooks guide](/en/agent-sdk/hooks).

### `HookEvent`

Available hook events.

```typescript theme={null}
type HookEvent =
  | "PreToolUse"
  | "PostToolUse"
  | "PostToolUseFailure"
  | "Notification"
  | "UserPromptSubmit"
  | "SessionStart"
  | "SessionEnd"
  | "Stop"
  | "SubagentStart"
  | "SubagentStop"
  | "PreCompact"
  | "PermissionRequest"
  | "Setup"
  | "TeammateIdle"
  | "TaskCompleted"
  | "ConfigChange"
  | "WorktreeCreate"
  | "WorktreeRemove";
```

### `HookCallback`

Hook callback function type.

```typescript theme={null}
type HookCallback = (
  input: HookInput, // Union of all hook input types
  toolUseID: string | undefined,
  options: { signal: AbortSignal }
) => Promise<HookJSONOutput>;
```

### `HookCallbackMatcher`

Hook configuration with optional matcher.

```typescript theme={null}
interface HookCallbackMatcher {
  matcher?: string;
  hooks: HookCallback[];
  timeout?: number; // Timeout in seconds for all hooks in this matcher
}
```

### `HookInput`

Union type of all hook input types.

```typescript theme={null}
type HookInput =
  | PreToolUseHookInput
  | PostToolUseHookInput
  | PostToolUseFailureHookInput
  | NotificationHookInput
  | UserPromptSubmitHookInput
  | SessionStartHookInput
  | SessionEndHookInput
  | StopHookInput
  | SubagentStartHookInput
  | SubagentStopHookInput
  | PreCompactHookInput
  | PermissionRequestHookInput
  | SetupHookInput
  | TeammateIdleHookInput
  | TaskCompletedHookInput
  | ConfigChangeHookInput
  | WorktreeCreateHookInput
  | WorktreeRemoveHookInput;
```

### `BaseHookInput`

Base interface that all hook input types extend.

```typescript theme={null}
type BaseHookInput = {
  session_id: string;
  transcript_path: string;
  cwd: string;
  permission_mode?: string;
  agent_id?: string;
  agent_type?: string;
};
```

#### `PreToolUseHookInput`

```typescript theme={null}
type PreToolUseHookInput = BaseHookInput & {
  hook_event_name: "PreToolUse";
  tool_name: string;
  tool_input: unknown;
  tool_use_id: string;
};
```

#### `PostToolUseHookInput`

```typescript theme={null}
type PostToolUseHookInput = BaseHookInput & {
  hook_event_name: "PostToolUse";
  tool_name: string;
  tool_input: unknown;
  tool_response: unknown;
  tool_use_id: string;
};
```

#### `PostToolUseFailureHookInput`

```typescript theme={null}
type PostToolUseFailureHookInput = BaseHookInput & {
  hook_event_name: "PostToolUseFailure";
  tool_name: string;
  tool_input: unknown;
  tool_use_id: string;
  error: string;
  is_interrupt?: boolean;
};
```

#### `NotificationHookInput`

```typescript theme={null}
type NotificationHookInput = BaseHookInput & {
  hook_event_name: "Notification";
  message: string;
  title?: string;
  notification_type: string;
};
```

#### `UserPromptSubmitHookInput`

```typescript theme={null}
type UserPromptSubmitHookInput = BaseHookInput & {
  hook_event_name: "UserPromptSubmit";
  prompt: string;
};
```

#### `SessionStartHookInput`

```typescript theme={null}
type SessionStartHookInput = BaseHookInput & {
  hook_event_name: "SessionStart";
  source: "startup" | "resume" | "clear" | "compact";
  agent_type?: string;
  model?: string;
};
```

#### `SessionEndHookInput`

```typescript theme={null}
type SessionEndHookInput = BaseHookInput & {
  hook_event_name: "SessionEnd";
  reason: ExitReason; // String from EXIT_REASONS array
};
```

#### `StopHookInput`

```typescript theme={null}
type StopHookInput = BaseHookInput & {
  hook_event_name: "Stop";
  stop_hook_active: boolean;
  last_assistant_message?: string;
};
```

#### `SubagentStartHookInput`

```typescript theme={null}
type SubagentStartHookInput = BaseHookInput & {
  hook_event_name: "SubagentStart";
  agent_id: string;
  agent_type: string;
};
```

#### `SubagentStopHookInput`

```typescript theme={null}
type SubagentStopHookInput = BaseHookInput & {
  hook_event_name: "SubagentStop";
  stop_hook_active: boolean;
  agent_id: string;
  agent_transcript_path: string;
  agent_type: string;
  last_assistant_message?: string;
};
```

#### `PreCompactHookInput`

```typescript theme={null}
type PreCompactHookInput = BaseHookInput & {
  hook_event_name: "PreCompact";
  trigger: "manual" | "auto";
  custom_instructions: string | null;
};
```

#### `PermissionRequestHookInput`

```typescript theme={null}
type PermissionRequestHookInput = BaseHookInput & {
  hook_event_name: "PermissionRequest";
  tool_name: string;
  tool_input: unknown;
  permission_suggestions?: PermissionUpdate[];
};
```

#### `SetupHookInput`

```typescript theme={null}
type SetupHookInput = BaseHookInput & {
  hook_event_name: "Setup";
  trigger: "init" | "maintenance";
};
```

#### `TeammateIdleHookInput`

```typescript theme={null}
type TeammateIdleHookInput = BaseHookInput & {
  hook_event_name: "TeammateIdle";
  teammate_name: string;
  team_name: string;
};
```

#### `TaskCompletedHookInput`

```typescript theme={null}
type TaskCompletedHookInput = BaseHookInput & {
  hook_event_name: "TaskCompleted";
  task_id: string;
  task_subject: string;
  task_description?: string;
  teammate_name?: string;
  team_name?: string;
};
```

#### `ConfigChangeHookInput`

```typescript theme={null}
type ConfigChangeHookInput = BaseHookInput & {
  hook_event_name: "ConfigChange";
  source:
    | "user_settings"
    | "project_settings"
    | "local_settings"
    | "policy_settings"
    | "skills";
  file_path?: string;
};
```

#### `WorktreeCreateHookInput`

```typescript theme={null}
type WorktreeCreateHookInput = BaseHookInput & {
  hook_event_name: "WorktreeCreate";
  name: string;
};
```

#### `WorktreeRemoveHookInput`

```typescript theme={null}
type WorktreeRemoveHookInput = BaseHookInput & {
  hook_event_name: "WorktreeRemove";
  worktree_path: string;
};
```

### `HookJSONOutput`

Hook return value.

```typescript theme={null}
type HookJSONOutput = AsyncHookJSONOutput | SyncHookJSONOutput;
```

#### `AsyncHookJSONOutput`

```typescript theme={null}
type AsyncHookJSONOutput = {
  async: true;
  asyncTimeout?: number;
};
```

#### `SyncHookJSONOutput`

```typescript theme={null}
type SyncHookJSONOutput = {
  continue?: boolean;
  suppressOutput?: boolean;
  stopReason?: string;
  decision?: "approve" | "block";
  systemMessage?: string;
  reason?: string;
  hookSpecificOutput?:
    | {
        hookEventName: "PreToolUse";
        permissionDecision?: "allow" | "deny" | "ask";
        permissionDecisionReason?: string;
        updatedInput?: Record<string, unknown>;
        additionalContext?: string;
      }
    | {
        hookEventName: "UserPromptSubmit";
        additionalContext?: string;
      }
    | {
        hookEventName: "SessionStart";
        additionalContext?: string;
      }
    | {
        hookEventName: "Setup";
        additionalContext?: string;
      }
    | {
        hookEventName: "SubagentStart";
        additionalContext?: string;
      }
    | {
        hookEventName: "PostToolUse";
        additionalContext?: string;
        updatedMCPToolOutput?: unknown;
      }
    | {
        hookEventName: "PostToolUseFailure";
        additionalContext?: string;
      }
    | {
        hookEventName: "Notification";
        additionalContext?: string;
      }
    | {
        hookEventName: "PermissionRequest";
        decision:
          | {
              behavior: "allow";
              updatedInput?: Record<string, unknown>;
              updatedPermissions?: PermissionUpdate[];
            }
          | {
              behavior: "deny";
              message?: string;
              interrupt?: boolean;
            };
      };
};
```

## Tool Input Types

Documentation of input schemas for all built-in Claude Code tools. These types are exported from `@anthropic-ai/claude-agent-sdk` and can be used for type-safe tool interactions.

### `ToolInputSchemas`

Union of all tool input types, exported from `@anthropic-ai/claude-agent-sdk`.

```typescript theme={null}
type ToolInputSchemas =
  | AgentInput
  | AskUserQuestionInput
  | BashInput
  | TaskOutputInput
  | ConfigInput
  | EnterWorktreeInput
  | ExitPlanModeInput
  | FileEditInput
  | FileReadInput
  | FileWriteInput
  | GlobInput
  | GrepInput
  | ListMcpResourcesInput
  | McpInput
  | MonitorInput
  | NotebookEditInput
  | ReadMcpResourceInput
  | SubscribeMcpResourceInput
  | SubscribePollingInput
  | TaskStopInput
  | TodoWriteInput
  | UnsubscribeMcpResourceInput
  | UnsubscribePollingInput
  | WebFetchInput
  | WebSearchInput;
```

### Agent

**Tool name:** `Agent` (previously `Task`, which is still accepted as an alias)

```typescript theme={null}
type AgentInput = {
  description: string;
  prompt: string;
  subagent_type: string;
  model?: "sonnet" | "opus" | "haiku";
  resume?: string;
  run_in_background?: boolean;
  max_turns?: number;
  name?: string;
  team_name?: string;
  mode?: "acceptEdits" | "bypassPermissions" | "default" | "dontAsk" | "plan";
  isolation?: "worktree";
};
```

Launches a new agent to handle complex, multi-step tasks autonomously.

### AskUserQuestion

**Tool name:** `AskUserQuestion`

```typescript theme={null}
type AskUserQuestionInput = {
  questions: Array<{
    question: string;
    header: string;
    options: Array<{ label: string; description: string; preview?: string }>;
    multiSelect: boolean;
  }>;
};
```

Asks the user clarifying questions during execution. See [Handle approvals and user input](/en/agent-sdk/user-input#handle-clarifying-questions) for usage details.

### Bash

**Tool name:** `Bash`

```typescript theme={null}
type BashInput = {
  command: string;
  timeout?: number;
  description?: string;
  run_in_background?: boolean;
  dangerouslyDisableSandbox?: boolean;
};
```

Executes bash commands in a persistent shell session with optional timeout and background execution.

### Monitor

**Tool name:** `Monitor`

```typescript theme={null}
type MonitorInput = {
  command: string;
  description: string;
  timeout_ms?: number;
  persistent?: boolean;
};
```

Runs a background script and delivers each stdout line to Claude as an event so it can react without polling. Set `persistent: true` for session-length watches such as log tails. Monitor follows the same permission rules as Bash. See the [Monitor tool reference](/en/tools-reference#monitor-tool) for behavior and provider availability.

### TaskOutput

**Tool name:** `TaskOutput`

```typescript theme={null}
type TaskOutputInput = {
  task_id: string;
  block: boolean;
  timeout: number;
};
```

Retrieves output from a running or completed background task.

### Edit

**Tool name:** `Edit`

```typescript theme={null}
type FileEditInput = {
  file_path: string;
  old_string: string;
  new_string: string;
  replace_all?: boolean;
};
```

Performs exact string replacements in files.

### Read

**Tool name:** `Read`

```typescript theme={null}
type FileReadInput = {
  file_path: string;
  offset?: number;
  limit?: number;
  pages?: string;
};
```

Reads files from the local filesystem, including text, images, PDFs, and Jupyter notebooks. Use `pages` for PDF page ranges (for example, `"1-5"`).

### Write

**Tool name:** `Write`

```typescript theme={null}
type FileWriteInput = {
  file_path: string;
  content: string;
};
```

Writes a file to the local filesystem, overwriting if it exists.

### Glob

**Tool name:** `Glob`

```typescript theme={null}
type GlobInput = {
  pattern: string;
  path?: string;
};
```

Fast file pattern matching that works with any codebase size.

### Grep

**Tool name:** `Grep`

```typescript theme={null}
type GrepInput = {
  pattern: string;
  path?: string;
  glob?: string;
  type?: string;
  output_mode?: "content" | "files_with_matches" | "count";
  "-i"?: boolean;
  "-n"?: boolean;
  "-B"?: number;
  "-A"?: number;
  "-C"?: number;
  context?: number;
  head_limit?: number;
  offset?: number;
  multiline?: boolean;
};
```

Powerful search tool built on ripgrep with regex support.

### TaskStop

**Tool name:** `TaskStop`

```typescript theme={null}
type TaskStopInput = {
  task_id?: string;
  shell_id?: string; // Deprecated: use task_id
};
```

Stops a running background task or shell by ID.

### NotebookEdit

**Tool name:** `NotebookEdit`

```typescript theme={null}
type NotebookEditInput = {
  notebook_path: string;
  cell_id?: string;
  new_source: string;
  cell_type?: "code" | "markdown";
  edit_mode?: "replace" | "insert" | "delete";
};
```

Edits cells in Jupyter notebook files.

### WebFetch

**Tool name:** `WebFetch`

```typescript theme={null}
type WebFetchInput = {
  url: string;
  prompt: string;
};
```

Fetches content from a URL and processes it with an AI model.

### WebSearch

**Tool name:** `WebSearch`

```typescript theme={null}
type WebSearchInput = {
  query: string;
  allowed_domains?: string[];
  blocked_domains?: string[];
};
```

Searches the web and returns formatted results.

### TodoWrite

**Tool name:** `TodoWrite`

```typescript theme={null}
type TodoWriteInput = {
  todos: Array<{
    content: string;
    status: "pending" | "in_progress" | "completed";
    activeForm: string;
  }>;
};
```

Creates and manages a structured task list for tracking progress.

### ExitPlanMode

**Tool name:** `ExitPlanMode`

```typescript theme={null}
type ExitPlanModeInput = {
  allowedPrompts?: Array<{
    tool: "Bash";
    prompt: string;
  }>;
};
```

Exits planning mode. Optionally specifies prompt-based permissions needed to implement the plan.

### ListMcpResources

**Tool name:** `ListMcpResources`

```typescript theme={null}
type ListMcpResourcesInput = {
  server?: string;
};
```

Lists available MCP resources from connected servers.

### ReadMcpResource

**Tool name:** `ReadMcpResource`

```typescript theme={null}
type ReadMcpResourceInput = {
  server: string;
  uri: string;
};
```

Reads a specific MCP resource from a server.

### Config

**Tool name:** `Config`

```typescript theme={null}
type ConfigInput = {
  setting: string;
  value?: string | boolean | number;
};
```

Gets or sets a configuration value.

### EnterWorktree

**Tool name:** `EnterWorktree`

```typescript theme={null}
type EnterWorktreeInput = {
  name?: string;
  path?: string;
};
```

Creates and enters a temporary git worktree for isolated work. Pass `path` to switch into an existing worktree of the current repository instead of creating a new one. `name` and `path` are mutually exclusive.

## Tool Output Types

Documentation of output schemas for all built-in Claude Code tools. These types are exported from `@anthropic-ai/claude-agent-sdk` and represent the actual response data returned by each tool.

### `ToolOutputSchemas`

Union of all tool output types.

```typescript theme={null}
type ToolOutputSchemas =
  | AgentOutput
  | AskUserQuestionOutput
  | BashOutput
  | ConfigOutput
  | EnterWorktreeOutput
  | ExitPlanModeOutput
  | FileEditOutput
  | FileReadOutput
  | FileWriteOutput
  | GlobOutput
  | GrepOutput
  | ListMcpResourcesOutput
  | MonitorOutput
  | NotebookEditOutput
  | ReadMcpResourceOutput
  | TaskStopOutput
  | TodoWriteOutput
  | WebFetchOutput
  | WebSearchOutput;
```

### Agent

**Tool name:** `Agent` (previously `Task`, which is still accepted as an alias)

```typescript theme={null}
type AgentOutput =
  | {
      status: "completed";
      agentId: string;
      content: Array<{ type: "text"; text: string }>;
      totalToolUseCount: number;
      totalDurationMs: number;
      totalTokens: number;
      usage: {
        input_tokens: number;
        output_tokens: number;
        cache_creation_input_tokens: number | null;
        cache_read_input_tokens: number | null;
        server_tool_use: {
          web_search_requests: number;
          web_fetch_requests: number;
        } | null;
        service_tier: ("standard" | "priority" | "batch") | null;
        cache_creation: {
          ephemeral_1h_input_tokens: number;
          ephemeral_5m_input_tokens: number;
        } | null;
      };
      prompt: string;
    }
  | {
      status: "async_launched";
      agentId: string;
      description: string;
      prompt: string;
      outputFile: string;
      canReadOutputFile?: boolean;
    }
  | {
      status: "sub_agent_entered";
      description: string;
      message: string;
    };
```

Returns the result from the subagent. Discriminated on the `status` field: `"completed"` for finished tasks, `"async_launched"` for background tasks, and `"sub_agent_entered"` for interactive subagents.

### AskUserQuestion

**Tool name:** `AskUserQuestion`

```typescript theme={null}
type AskUserQuestionOutput = {
  questions: Array<{
    question: string;
    header: string;
    options: Array<{ label: string; description: string; preview?: string }>;
    multiSelect: boolean;
  }>;
  answers: Record<string, string>;
};
```

Returns the questions asked and the user's answers.

### Bash

**Tool name:** `Bash`

```typescript theme={null}
type BashOutput = {
  stdout: string;
  stderr: string;
  rawOutputPath?: string;
  interrupted: boolean;
  isImage?: boolean;
  backgroundTaskId?: string;
  backgroundedByUser?: boolean;
  dangerouslyDisableSandbox?: boolean;
  returnCodeInterpretation?: string;
  structuredContent?: unknown[];
  persistedOutputPath?: string;
  persistedOutputSize?: number;
};
```

Returns command output with stdout/stderr split. Background commands include a `backgroundTaskId`.

### Monitor

**Tool name:** `Monitor`

```typescript theme={null}
type MonitorOutput = {
  taskId: string;
  timeoutMs: number;
  persistent?: boolean;
};
```

Returns the background task ID for the running monitor. Use this ID with `TaskStop` to cancel the watch early.

### Edit

**Tool name:** `Edit`

```typescript theme={null}
type FileEditOutput = {
  filePath: string;
  oldString: string;
  newString: string;
  originalFile: string;
  structuredPatch: Array<{
    oldStart: number;
    oldLines: number;
    newStart: number;
    newLines: number;
    lines: string[];
  }>;
  userModified: boolean;
  replaceAll: boolean;
  gitDiff?: {
    filename: string;
    status: "modified" | "added";
    additions: number;
    deletions: number;
    changes: number;
    patch: string;
  };
};
```

Returns the structured diff of the edit operation.

### Read

**Tool name:** `Read`

```typescript theme={null}
type FileReadOutput =
  | {
      type: "text";
      file: {
        filePath: string;
        content: string;
        numLines: number;
        startLine: number;
        totalLines: number;
      };
    }
  | {
      type: "image";
      file: {
        base64: string;
        type: "image/jpeg" | "image/png" | "image/gif" | "image/webp";
        originalSize: number;
        dimensions?: {
          originalWidth?: number;
          originalHeight?: number;
          displayWidth?: number;
          displayHeight?: number;
        };
      };
    }
  | {
      type: "notebook";
      file: {
        filePath: string;
        cells: unknown[];
      };
    }
  | {
      type: "pdf";
      file: {
        filePath: string;
        base64: string;
        originalSize: number;
      };
    }
  | {
      type: "parts";
      file: {
        filePath: string;
        originalSize: number;
        count: number;
        outputDir: string;
      };
    };
```

Returns file contents in a format appropriate to the file type. Discriminated on the `type` field.

### Write

**Tool name:** `Write`

```typescript theme={null}
type FileWriteOutput = {
  type: "create" | "update";
  filePath: string;
  content: string;
  structuredPatch: Array<{
    oldStart: number;
    oldLines: number;
    newStart: number;
    newLines: number;
    lines: string[];
  }>;
  originalFile: string | null;
  gitDiff?: {
    filename: string;
    status: "modified" | "added";
    additions: number;
    deletions: number;
    changes: number;
    patch: string;
  };
};
```

Returns the write result with structured diff information.

### Glob

**Tool name:** `Glob`

```typescript theme={null}
type GlobOutput = {
  durationMs: number;
  numFiles: number;
  filenames: string[];
  truncated: boolean;
};
```

Returns file paths matching the glob pattern, sorted by modification time.

### Grep

**Tool name:** `Grep`

```typescript theme={null}
type GrepOutput = {
  mode?: "content" | "files_with_matches" | "count";
  numFiles: number;
  filenames: string[];
  content?: string;
  numLines?: number;
  numMatches?: number;
  appliedLimit?: number;
  appliedOffset?: number;
};
```

Returns search results. The shape varies by `mode`: file list, content with matches, or match counts.

### TaskStop

**Tool name:** `TaskStop`

```typescript theme={null}
type TaskStopOutput = {
  message: string;
  task_id: string;
  task_type: string;
  command?: string;
};
```

Returns confirmation after stopping the background task.

### NotebookEdit

**Tool name:** `NotebookEdit`

```typescript theme={null}
type NotebookEditOutput = {
  new_source: string;
  cell_id?: string;
  cell_type: "code" | "markdown";
  language: string;
  edit_mode: string;
  error?: string;
  notebook_path: string;
  original_file: string;
  updated_file: string;
};
```

Returns the result of the notebook edit with original and updated file contents.

### WebFetch

**Tool name:** `WebFetch`

```typescript theme={null}
type WebFetchOutput = {
  bytes: number;
  code: number;
  codeText: string;
  result: string;
  durationMs: number;
  url: string;
};
```

Returns the fetched content with HTTP status and metadata.

### WebSearch

**Tool name:** `WebSearch`

```typescript theme={null}
type WebSearchOutput = {
  query: string;
  results: Array<
    | {
        tool_use_id: string;
        content: Array<{ title: string; url: string }>;
      }
    | string
  >;
  durationSeconds: number;
};
```

Returns search results from the web.

### TodoWrite

**Tool name:** `TodoWrite`

```typescript theme={null}
type TodoWriteOutput = {
  oldTodos: Array<{
    content: string;
    status: "pending" | "in_progress" | "completed";
    activeForm: string;
  }>;
  newTodos: Array<{
    content: string;
    status: "pending" | "in_progress" | "completed";
    activeForm: string;
  }>;
};
```

Returns the previous and updated task lists.

### ExitPlanMode

**Tool name:** `ExitPlanMode`

```typescript theme={null}
type ExitPlanModeOutput = {
  plan: string | null;
  isAgent: boolean;
  filePath?: string;
  hasTaskTool?: boolean;
  awaitingLeaderApproval?: boolean;
  requestId?: string;
};
```

Returns the plan state after exiting plan mode.

### ListMcpResources

**Tool name:** `ListMcpResources`

```typescript theme={null}
type ListMcpResourcesOutput = Array<{
  uri: string;
  name: string;
  mimeType?: string;
  description?: string;
  server: string;
}>;
```

Returns an array of available MCP resources.

### ReadMcpResource

**Tool name:** `ReadMcpResource`

```typescript theme={null}
type ReadMcpResourceOutput = {
  contents: Array<{
    uri: string;
    mimeType?: string;
    text?: string;
  }>;
};
```

Returns the contents of the requested MCP resource.

### Config

**Tool name:** `Config`

```typescript theme={null}
type ConfigOutput = {
  success: boolean;
  operation?: "get" | "set";
  setting?: string;
  value?: unknown;
  previousValue?: unknown;
  newValue?: unknown;
  error?: string;
};
```

Returns the result of a configuration get or set operation.

### EnterWorktree

**Tool name:** `EnterWorktree`

```typescript theme={null}
type EnterWorktreeOutput = {
  worktreePath: string;
  worktreeBranch?: string;
  message: string;
};
```

Returns information about the git worktree.

## Permission Types

### `PermissionUpdate`

Operations for updating permissions.

```typescript theme={null}
type PermissionUpdate =
  | {
      type: "addRules";
      rules: PermissionRuleValue[];
      behavior: PermissionBehavior;
      destination: PermissionUpdateDestination;
    }
  | {
      type: "replaceRules";
      rules: PermissionRuleValue[];
      behavior: PermissionBehavior;
      destination: PermissionUpdateDestination;
    }
  | {
      type: "removeRules";
      rules: PermissionRuleValue[];
      behavior: PermissionBehavior;
      destination: PermissionUpdateDestination;
    }
  | {
      type: "setMode";
      mode: PermissionMode;
      destination: PermissionUpdateDestination;
    }
  | {
      type: "addDirectories";
      directories: string[];
      destination: PermissionUpdateDestination;
    }
  | {
      type: "removeDirectories";
      directories: string[];
      destination: PermissionUpdateDestination;
    };
```

### `PermissionBehavior`

```typescript theme={null}
type PermissionBehavior = "allow" | "deny" | "ask";
```

### `PermissionUpdateDestination`

```typescript theme={null}
type PermissionUpdateDestination =
  | "userSettings" // Global user settings
  | "projectSettings" // Per-directory project settings
  | "localSettings" // Gitignored local settings
  | "session" // Current session only
  | "cliArg"; // CLI argument
```

### `PermissionRuleValue`

```typescript theme={null}
type PermissionRuleValue = {
  toolName: string;
  ruleContent?: string;
};
```

## Other Types

### `ApiKeySource`

```typescript theme={null}
type ApiKeySource = "user" | "project" | "org" | "temporary" | "oauth";
```

### `SdkBeta`

Available beta features that can be enabled via the `betas` option. See [Beta headers](https://platform.claude.com/docs/en/api/beta-headers) for more information.

```typescript theme={null}
type SdkBeta = "context-1m-2025-08-07";
```

<Warning>
  The `context-1m-2025-08-07` beta is retired as of April 30, 2026. Passing this value with Claude Sonnet 4.5 or Sonnet 4 has no effect, and requests that exceed the standard 200k-token context window return an error. To use a 1M-token context window, migrate to [Claude Sonnet 4.6, Claude Opus 4.6, or Claude Opus 4.7](https://platform.claude.com/docs/en/about-claude/models/overview), which include 1M context at standard pricing with no beta header required.
</Warning>

### `SlashCommand`

Information about an available slash command.

```typescript theme={null}
type SlashCommand = {
  name: string;
  description: string;
  argumentHint: string;
};
```

### `ModelInfo`

Information about an available model.

```typescript theme={null}
type ModelInfo = {
  value: string;
  displayName: string;
  description: string;
  supportsEffort?: boolean;
  supportedEffortLevels?: ("low" | "medium" | "high" | "xhigh" | "max")[];
  supportsAdaptiveThinking?: boolean;
  supportsFastMode?: boolean;
};
```

### `AgentInfo`

Information about an available subagent that can be invoked via the Agent tool.

```typescript theme={null}
type AgentInfo = {
  name: string;
  description: string;
  model?: string;
};
```

| Field         | Type                  | Description                                                          |
| :------------ | :-------------------- | :------------------------------------------------------------------- |
| `name`        | `string`              | Agent type identifier (e.g., `"Explore"`, `"general-purpose"`)       |
| `description` | `string`              | Description of when to use this agent                                |
| `model`       | `string \| undefined` | Model alias this agent uses. If omitted, inherits the parent's model |

### `McpServerStatus`

Status of a connected MCP server.

```typescript theme={null}
type McpServerStatus = {
  name: string;
  status: "connected" | "failed" | "needs-auth" | "pending" | "disabled";
  serverInfo?: {
    name: string;
    version: string;
  };
  error?: string;
  config?: McpServerStatusConfig;
  scope?: string;
  tools?: {
    name: string;
    description?: string;
    annotations?: {
      readOnly?: boolean;
      destructive?: boolean;
      openWorld?: boolean;
    };
  }[];
};
```

### `McpServerStatusConfig`

The configuration of an MCP server as reported by `mcpServerStatus()`. This is the union of all MCP server transport types.

```typescript theme={null}
type McpServerStatusConfig =
  | McpStdioServerConfig
  | McpSSEServerConfig
  | McpHttpServerConfig
  | McpSdkServerConfig
  | McpClaudeAIProxyServerConfig;
```

See [`McpServerConfig`](#mcp-server-config) for details on each transport type.

### `AccountInfo`

Account information for the authenticated user.

```typescript theme={null}
type AccountInfo = {
  email?: string;
  organization?: string;
  subscriptionType?: string;
  tokenSource?: string;
  apiKeySource?: string;
};
```

### `ModelUsage`

Per-model usage statistics returned in result messages. The `costUSD` value is a client-side estimate. See [Track cost and usage](/en/agent-sdk/cost-tracking) for billing caveats.

```typescript theme={null}
type ModelUsage = {
  inputTokens: number;
  outputTokens: number;
  cacheReadInputTokens: number;
  cacheCreationInputTokens: number;
  webSearchRequests: number;
  costUSD: number;
  contextWindow: number;
  maxOutputTokens: number;
};
```

### `ConfigScope`

```typescript theme={null}
type ConfigScope = "local" | "user" | "project";
```

### `NonNullableUsage`

A version of [`Usage`](#usage) with all nullable fields made non-nullable.

```typescript theme={null}
type NonNullableUsage = {
  [K in keyof Usage]: NonNullable<Usage[K]>;
};
```

### `Usage`

Token usage statistics (from `@anthropic-ai/sdk`).

```typescript theme={null}
type Usage = {
  input_tokens: number | null;
  output_tokens: number | null;
  cache_creation_input_tokens?: number | null;
  cache_read_input_tokens?: number | null;
};
```

### `CallToolResult`

MCP tool result type (from `@modelcontextprotocol/sdk/types.js`).

```typescript theme={null}
type CallToolResult = {
  content: Array<{
    type: "text" | "image" | "resource";
    // Additional fields vary by type
  }>;
  isError?: boolean;
};
```

### `ThinkingConfig`

Controls Claude's thinking/reasoning behavior. Takes precedence over the deprecated `maxThinkingTokens`.

```typescript theme={null}
type ThinkingConfig =
  | { type: "adaptive" } // The model determines when and how much to reason (Opus 4.6+)
  | { type: "enabled"; budgetTokens?: number } // Fixed thinking token budget
  | { type: "disabled" }; // No extended thinking
```

### `SpawnedProcess`

Interface for custom process spawning (used with `spawnClaudeCodeProcess` option). `ChildProcess` already satisfies this interface.

```typescript theme={null}
interface SpawnedProcess {
  stdin: Writable;
  stdout: Readable;
  readonly killed: boolean;
  readonly exitCode: number | null;
  kill(signal: NodeJS.Signals): boolean;
  on(
    event: "exit",
    listener: (code: number | null, signal: NodeJS.Signals | null) => void
  ): void;
  on(event: "error", listener: (error: Error) => void): void;
  once(
    event: "exit",
    listener: (code: number | null, signal: NodeJS.Signals | null) => void
  ): void;
  once(event: "error", listener: (error: Error) => void): void;
  off(
    event: "exit",
    listener: (code: number | null, signal: NodeJS.Signals | null) => void
  ): void;
  off(event: "error", listener: (error: Error) => void): void;
}
```

### `SpawnOptions`

Options passed to the custom spawn function.

```typescript theme={null}
interface SpawnOptions {
  command: string;
  args: string[];
  cwd?: string;
  env: Record<string, string | undefined>;
  signal: AbortSignal;
}
```

### `McpSetServersResult`

Result of a `setMcpServers()` operation.

```typescript theme={null}
type McpSetServersResult = {
  added: string[];
  removed: string[];
  errors: Record<string, string>;
};
```

### `RewindFilesResult`

Result of a `rewindFiles()` operation.

```typescript theme={null}
type RewindFilesResult = {
  canRewind: boolean;
  error?: string;
  filesChanged?: string[];
  insertions?: number;
  deletions?: number;
};
```

### `SDKStatusMessage`

Status update message (e.g., compacting).

```typescript theme={null}
type SDKStatusMessage = {
  type: "system";
  subtype: "status";
  status: "compacting" | null;
  permissionMode?: PermissionMode;
  uuid: UUID;
  session_id: string;
};
```

### `SDKTaskNotificationMessage`

Notification when a background task completes, fails, or is stopped. Background tasks include `run_in_background` Bash commands, [Monitor](#monitor) watches, and background subagents.

```typescript theme={null}
type SDKTaskNotificationMessage = {
  type: "system";
  subtype: "task_notification";
  task_id: string;
  tool_use_id?: string;
  status: "completed" | "failed" | "stopped";
  output_file: string;
  summary: string;
  usage?: {
    total_tokens: number;
    tool_uses: number;
    duration_ms: number;
  };
  uuid: UUID;
  session_id: string;
};
```

### `SDKToolUseSummaryMessage`

Summary of tool usage in a conversation.

```typescript theme={null}
type SDKToolUseSummaryMessage = {
  type: "tool_use_summary";
  summary: string;
  preceding_tool_use_ids: string[];
  uuid: UUID;
  session_id: string;
};
```

### `SDKHookStartedMessage`

Emitted when a hook begins executing.

```typescript theme={null}
type SDKHookStartedMessage = {
  type: "system";
  subtype: "hook_started";
  hook_id: string;
  hook_name: string;
  hook_event: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKHookProgressMessage`

Emitted while a hook is running, with stdout/stderr output.

```typescript theme={null}
type SDKHookProgressMessage = {
  type: "system";
  subtype: "hook_progress";
  hook_id: string;
  hook_name: string;
  hook_event: string;
  stdout: string;
  stderr: string;
  output: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKHookResponseMessage`

Emitted when a hook finishes executing.

```typescript theme={null}
type SDKHookResponseMessage = {
  type: "system";
  subtype: "hook_response";
  hook_id: string;
  hook_name: string;
  hook_event: string;
  output: string;
  stdout: string;
  stderr: string;
  exit_code?: number;
  outcome: "success" | "error" | "cancelled";
  uuid: UUID;
  session_id: string;
};
```

### `SDKToolProgressMessage`

Emitted periodically while a tool is executing to indicate progress.

```typescript theme={null}
type SDKToolProgressMessage = {
  type: "tool_progress";
  tool_use_id: string;
  tool_name: string;
  parent_tool_use_id: string | null;
  elapsed_time_seconds: number;
  task_id?: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKAuthStatusMessage`

Emitted during authentication flows.

```typescript theme={null}
type SDKAuthStatusMessage = {
  type: "auth_status";
  isAuthenticating: boolean;
  output: string[];
  error?: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKTaskStartedMessage`

Emitted when a background task begins. The `task_type` field is `"local_bash"` for background Bash commands and [Monitor](#monitor) watches, `"local_agent"` for subagents, or `"remote_agent"`.

```typescript theme={null}
type SDKTaskStartedMessage = {
  type: "system";
  subtype: "task_started";
  task_id: string;
  tool_use_id?: string;
  description: string;
  task_type?: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKTaskProgressMessage`

Emitted periodically while a background task is running.

```typescript theme={null}
type SDKTaskProgressMessage = {
  type: "system";
  subtype: "task_progress";
  task_id: string;
  tool_use_id?: string;
  description: string;
  usage: {
    total_tokens: number;
    tool_uses: number;
    duration_ms: number;
  };
  last_tool_name?: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKFilesPersistedEvent`

Emitted when file checkpoints are persisted to disk.

```typescript theme={null}
type SDKFilesPersistedEvent = {
  type: "system";
  subtype: "files_persisted";
  files: { filename: string; file_id: string }[];
  failed: { filename: string; error: string }[];
  processed_at: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKRateLimitEvent`

Emitted when the session encounters a rate limit.

```typescript theme={null}
type SDKRateLimitEvent = {
  type: "rate_limit_event";
  rate_limit_info: {
    status: "allowed" | "allowed_warning" | "rejected";
    resetsAt?: number;
    utilization?: number;
  };
  uuid: UUID;
  session_id: string;
};
```

### `SDKLocalCommandOutputMessage`

Output from a local slash command (for example, `/voice` or `/cost`). Displayed as assistant-style text in the transcript.

```typescript theme={null}
type SDKLocalCommandOutputMessage = {
  type: "system";
  subtype: "local_command_output";
  content: string;
  uuid: UUID;
  session_id: string;
};
```

### `SDKPromptSuggestionMessage`

Emitted after each turn when `promptSuggestions` is enabled. Contains a predicted next user prompt.

```typescript theme={null}
type SDKPromptSuggestionMessage = {
  type: "prompt_suggestion";
  suggestion: string;
  uuid: UUID;
  session_id: string;
};
```

### `AbortError`

Custom error class for abort operations.

```typescript theme={null}
class AbortError extends Error {}
```

## Sandbox Configuration

### `SandboxSettings`

Configuration for sandbox behavior. Use this to enable command sandboxing and configure network restrictions programmatically.

```typescript theme={null}
type SandboxSettings = {
  enabled?: boolean;
  autoAllowBashIfSandboxed?: boolean;
  excludedCommands?: string[];
  allowUnsandboxedCommands?: boolean;
  network?: SandboxNetworkConfig;
  filesystem?: SandboxFilesystemConfig;
  ignoreViolations?: Record<string, string[]>;
  enableWeakerNestedSandbox?: boolean;
  ripgrep?: { command: string; args?: string[] };
};
```

| Property                    | Type                                                    | Default     | Description                                                                                                                                                                                                                             |
| :-------------------------- | :------------------------------------------------------ | :---------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `enabled`                   | `boolean`                                               | `false`     | Enable sandbox mode for command execution                                                                                                                                                                                               |
| `autoAllowBashIfSandboxed`  | `boolean`                                               | `true`      | Auto-approve bash commands when sandbox is enabled                                                                                                                                                                                      |
| `excludedCommands`          | `string[]`                                              | `[]`        | Commands that always bypass sandbox restrictions (e.g., `['docker']`). These run unsandboxed automatically without model involvement                                                                                                    |
| `allowUnsandboxedCommands`  | `boolean`                                               | `true`      | Allow the model to request running commands outside the sandbox. When `true`, the model can set `dangerouslyDisableSandbox` in tool input, which falls back to the [permissions system](#permissions-fallback-for-unsandboxed-commands) |
| `network`                   | [`SandboxNetworkConfig`](#sandbox-network-config)       | `undefined` | Network-specific sandbox configuration                                                                                                                                                                                                  |
| `filesystem`                | [`SandboxFilesystemConfig`](#sandbox-filesystem-config) | `undefined` | Filesystem-specific sandbox configuration for read/write restrictions                                                                                                                                                                   |
| `ignoreViolations`          | `Record<string, string[]>`                              | `undefined` | Map of violation categories to patterns to ignore (e.g., `{ file: ['/tmp/*'], network: ['localhost'] }`)                                                                                                                                |
| `enableWeakerNestedSandbox` | `boolean`                                               | `false`     | Enable a weaker nested sandbox for compatibility                                                                                                                                                                                        |
| `ripgrep`                   | `{ command: string; args?: string[] }`                  | `undefined` | Custom ripgrep binary configuration for sandbox environments                                                                                                                                                                            |

#### Example usage

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Build and test my project",
  options: {
    sandbox: {
      enabled: true,
      autoAllowBashIfSandboxed: true,
      network: {
        allowLocalBinding: true
      }
    }
  }
})) {
  if ("result" in message) console.log(message.result);
}
```

<Warning>
  **Unix socket security:** The `allowUnixSockets` option can grant access to powerful system services. For example, allowing `/var/run/docker.sock` effectively grants full host system access through the Docker API, bypassing sandbox isolation. Only allow Unix sockets that are strictly necessary and understand the security implications of each.
</Warning>

### `SandboxNetworkConfig`

Network-specific configuration for sandbox mode.

```typescript theme={null}
type SandboxNetworkConfig = {
  allowedDomains?: string[];
  allowManagedDomainsOnly?: boolean;
  allowLocalBinding?: boolean;
  allowUnixSockets?: string[];
  allowAllUnixSockets?: boolean;
  httpProxyPort?: number;
  socksProxyPort?: number;
};
```

| Property                  | Type       | Default     | Description                                                       |
| :------------------------ | :--------- | :---------- | :---------------------------------------------------------------- |
| `allowedDomains`          | `string[]` | `[]`        | Domain names that sandboxed processes can access                  |
| `allowManagedDomainsOnly` | `boolean`  | `false`     | Restrict network access to only the domains in `allowedDomains`   |
| `allowLocalBinding`       | `boolean`  | `false`     | Allow processes to bind to local ports (e.g., for dev servers)    |
| `allowUnixSockets`        | `string[]` | `[]`        | Unix socket paths that processes can access (e.g., Docker socket) |
| `allowAllUnixSockets`     | `boolean`  | `false`     | Allow access to all Unix sockets                                  |
| `httpProxyPort`           | `number`   | `undefined` | HTTP proxy port for network requests                              |
| `socksProxyPort`          | `number`   | `undefined` | SOCKS proxy port for network requests                             |

### `SandboxFilesystemConfig`

Filesystem-specific configuration for sandbox mode.

```typescript theme={null}
type SandboxFilesystemConfig = {
  allowWrite?: string[];
  denyWrite?: string[];
  denyRead?: string[];
};
```

| Property     | Type       | Default | Description                                 |
| :----------- | :--------- | :------ | :------------------------------------------ |
| `allowWrite` | `string[]` | `[]`    | File path patterns to allow write access to |
| `denyWrite`  | `string[]` | `[]`    | File path patterns to deny write access to  |
| `denyRead`   | `string[]` | `[]`    | File path patterns to deny read access to   |

### Permissions Fallback for Unsandboxed Commands

When `allowUnsandboxedCommands` is enabled, the model can request to run commands outside the sandbox by setting `dangerouslyDisableSandbox: true` in the tool input. These requests fall back to the existing permissions system, meaning your `canUseTool` handler is invoked, allowing you to implement custom authorization logic.

<Note>
  **`excludedCommands` vs `allowUnsandboxedCommands`:**

  * `excludedCommands`: A static list of commands that always bypass the sandbox automatically (e.g., `['docker']`). The model has no control over this.
  * `allowUnsandboxedCommands`: Lets the model decide at runtime whether to request unsandboxed execution by setting `dangerouslyDisableSandbox: true` in the tool input.
</Note>

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Deploy my application",
  options: {
    sandbox: {
      enabled: true,
      allowUnsandboxedCommands: true // Model can request unsandboxed execution
    },
    permissionMode: "default",
    canUseTool: async (tool, input) => {
      // Check if the model is requesting to bypass the sandbox
      if (tool === "Bash" && input.dangerouslyDisableSandbox) {
        // The model is requesting to run this command outside the sandbox
        console.log(`Unsandboxed command requested: ${input.command}`);

        if (isCommandAuthorized(input.command)) {
          return { behavior: "allow" as const, updatedInput: input };
        }
        return {
          behavior: "deny" as const,
          message: "Command not authorized for unsandboxed execution"
        };
      }
      return { behavior: "allow" as const, updatedInput: input };
    }
  }
})) {
  if ("result" in message) console.log(message.result);
}
```

This pattern enables you to:

* **Audit model requests:** Log when the model requests unsandboxed execution
* **Implement allowlists:** Only permit specific commands to run unsandboxed
* **Add approval workflows:** Require explicit authorization for privileged operations

<Warning>
  Commands running with `dangerouslyDisableSandbox: true` have full system access. Ensure your `canUseTool` handler validates these requests carefully.

  If `permissionMode` is set to `bypassPermissions` and `allowUnsandboxedCommands` is enabled, the model can autonomously execute commands outside the sandbox without any approval prompts. This combination effectively allows the model to escape sandbox isolation silently.
</Warning>

## See also

* [SDK overview](/en/agent-sdk/overview) - General SDK concepts
* [Python SDK reference](/en/agent-sdk/python) - Python SDK documentation
* [CLI reference](/en/cli-reference) - Command-line interface
* [Common workflows](/en/common-workflows) - Step-by-step guides
