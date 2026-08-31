> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Error reference

> Look up Claude Code runtime error messages with what each one means and how to fix it.

This page lists runtime errors Claude Code displays and how to recover from each one, plus what to check when responses seem off without an error. For installation errors such as `command not found` or TLS failures during setup, see [Troubleshoot installation and login](/docs/en/troubleshoot-install).

Except for [Wrapper and IDE errors](#wrapper-and-ide-errors), which the launching program prints rather than Claude Code itself, these errors and recovery commands apply across the CLI, the [Desktop app](/docs/en/desktop), and [Claude Code on the web](/docs/en/claude-code-on-the-web), since all three wrap the same Claude Code CLI. For other surface-specific issues, see the troubleshooting section on that surface's page.

<Note>
  Claude Code calls the Claude API for model responses, so most runtime errors map to an underlying API error code. This page covers what each error means inside Claude Code and how to recover. For the raw HTTP status code definitions, see the [Claude Platform error reference](https://platform.claude.com/docs/en/api/errors).
</Note>

## Find your error

Match the message you see to a section below.

| Message                                                                                                                                                                                               | Section                                                                                                                       |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| `API Error: 500 Internal server error`                                                                                                                                                                | [Server errors](#api-error-500-internal-server-error)                                                                         |
| `API Error: Repeated 529 Overloaded errors`                                                                                                                                                           | [Server errors](#api-error-repeated-529-overloaded-errors)                                                                    |
| `Request timed out`                                                                                                                                                                                   | [Server errors](#request-timed-out), or [Network](#unable-to-connect-to-api) if the message mentions your internet connection |
| `API Error: No response from API`                                                                                                                                                                     | [Server errors](#no-response-from-api)                                                                                        |
| `Server error mid-response. The response above may be incomplete.`                                                                                                                                    | [Server errors](#the-response-above-may-be-incomplete)                                                                        |
| `Connection lost mid-response` / `Your computer went to sleep mid-response` / `The response stopped arriving`                                                                                         | [Server errors](#the-response-above-may-be-incomplete)                                                                        |
| `Connection closed mid-response` / `Response stalled mid-stream`                                                                                                                                      | [Server errors](#the-response-above-may-be-incomplete)                                                                        |
| `Connection lost before a response was produced` / `Your computer went to sleep before a response was produced` / `The response stalled before a response was produced`                               | [Automatic retries](#automatic-retries)                                                                                       |
| `Connection closed while thinking` / `Response stalled while thinking`                                                                                                                                | [Automatic retries](#automatic-retries)                                                                                       |
| `Connection lost while your computer was asleep`                                                                                                                                                      | [Automatic retries](#automatic-retries)                                                                                       |
| `<model> is temporarily unavailable, so auto mode cannot determine the safety of...`                                                                                                                  | [Server errors](#auto-mode-cannot-determine-the-safety-of-an-action)                                                          |
| `Auto mode could not evaluate this action and is blocking it for safety`                                                                                                                              | [Server errors](#auto-mode-cannot-determine-the-safety-of-an-action)                                                          |
| `Auto mode classifier transcript exceeded context window`                                                                                                                                             | [Server errors](#auto-mode-cannot-determine-the-safety-of-an-action)                                                          |
| `Agent aborted: auto mode classifier request refused by the safety safeguard`                                                                                                                         | [Server errors](#auto-mode-cannot-determine-the-safety-of-an-action)                                                          |
| `Agent terminated early due to an API error`                                                                                                                                                          | [Server errors](#agent-terminated-early-due-to-an-api-error)                                                                  |
| `You've hit your session limit` / `You've hit your weekly limit` / `You've hit your Opus limit` / `You've hit your Sonnet limit`                                                                      | [Usage limits](#youve-hit-your-session-limit)                                                                                 |
| `Usage credits required for 1M context`                                                                                                                                                               | [Usage limits](#usage-credits-required-for-1m-context)                                                                        |
| `the prompt to confirm went unanswered — nothing was sent`                                                                                                                                            | [Usage limits](#the-prompt-to-confirm-went-unanswered)                                                                        |
| `Server is temporarily limiting requests`                                                                                                                                                             | [Usage limits](#server-is-temporarily-limiting-requests)                                                                      |
| `Request rejected (429)`                                                                                                                                                                              | [Usage limits](#request-rejected-429)                                                                                         |
| `Credit balance is too low`                                                                                                                                                                           | [Usage limits](#credit-balance-is-too-low)                                                                                    |
| `Could not update your spend limit`                                                                                                                                                                   | [Usage limits](#could-not-update-your-spend-limit)                                                                            |
| `spend limit reached` / `spend limit unavailable`                                                                                                                                                     | [Usage limits](#spend-limit-reached)                                                                                          |
| `Not logged in · Please run /login`                                                                                                                                                                   | [Authentication](#not-logged-in)                                                                                              |
| `Could not resolve authentication method`                                                                                                                                                             | [Authentication](#could-not-resolve-authentication-method)                                                                    |
| `Invalid API key`                                                                                                                                                                                     | [Authentication](#invalid-api-key)                                                                                            |
| `Your apiKeyHelper script is failing`                                                                                                                                                                 | [Authentication](#your-apikeyhelper-script-is-failing)                                                                        |
| `Invalid auth token · Fix external auth token`                                                                                                                                                        | [Authentication](#invalid-request-header-value)                                                                               |
| `Invalid ANTHROPIC_CUSTOM_HEADERS · Fix the environment variable`                                                                                                                                     | [Authentication](#invalid-request-header-value)                                                                               |
| `Invalid request header from the environment · Fix the environment variable`                                                                                                                          | [Authentication](#invalid-request-header-value)                                                                               |
| `This organization has been disabled`                                                                                                                                                                 | [Authentication](#this-organization-has-been-disabled)                                                                        |
| `Your organization has disabled API key authentication`                                                                                                                                               | [Authentication](#your-organization-has-disabled-api-key-authentication)                                                      |
| `Your organization has disabled Claude subscription access`                                                                                                                                           | [Authentication](#your-organization-has-disabled-claude-subscription-access)                                                  |
| `Routines are disabled by your organization's policy`                                                                                                                                                 | [Authentication](#routines-are-disabled-by-your-organizations-policy)                                                         |
| `Remote Control is only available when using Claude via api.anthropic.com`                                                                                                                            | [Authentication](#remote-control-requires-the-anthropic-api)                                                                  |
| `OAuth token refresh failed — run /login to re-authenticate`                                                                                                                                          | [Authentication](#remote-control-couldnt-refresh-your-login)                                                                  |
| `JWT refresh failed: no OAuth token — run /login`                                                                                                                                                     | [Authentication](#remote-control-couldnt-refresh-your-login)                                                                  |
| `Claude.ai login expired`                                                                                                                                                                             | [Authentication](#remote-control-couldnt-refresh-your-login)                                                                  |
| `Claude.ai login was rejected — run /login, then /remote-control`                                                                                                                                     | [Authentication](#remote-control-couldnt-refresh-your-login)                                                                  |
| `OAuth token unavailable — run /login to restore Remote Control`                                                                                                                                      | [Authentication](#remote-control-couldnt-refresh-your-login)                                                                  |
| `Signed out of Claude — run /login, then /remote-control`                                                                                                                                             | [Authentication](#remote-control-couldnt-refresh-your-login)                                                                  |
| `signed-in claude.ai account or organization changed on this machine`                                                                                                                                 | [Authentication](#remote-control-stopped-because-the-signed-in-account-changed)                                               |
| `Remote Control stopped — the app running this session is now signed in to a different Claude account`                                                                                                | [Authentication](#remote-control-stopped-because-the-app-running-the-session-signed-out-or-switched-accounts)                 |
| `Remote Control stopped — the app running this session is signed out of Claude`                                                                                                                       | [Authentication](#remote-control-stopped-because-the-app-running-the-session-signed-out-or-switched-accounts)                 |
| `OAuth token revoked` / `OAuth token has expired`                                                                                                                                                     | [Authentication](#oauth-token-revoked-or-expired)                                                                             |
| `API Error: 401 Invalid authentication credentials`                                                                                                                                                   | [Authentication](#api-error-401-invalid-authentication-credentials)                                                           |
| `Login expired · Please run /login`                                                                                                                                                                   | [Authentication](#login-expired)                                                                                              |
| `Failed to authenticate: OAuth session expired and could not be refreshed`                                                                                                                            | [Authentication](#login-expired)                                                                                              |
| `Anthropic profile login expired · Re-authenticate your Anthropic profile`                                                                                                                            | [Authentication](#anthropic-profile-login-expired)                                                                            |
| `Anthropic profile login expired · Run /login to use your claude.ai account instead, or re-authenticate the profile`                                                                                  | [Authentication](#anthropic-profile-login-expired)                                                                            |
| `does not meet scope requirement user:profile`                                                                                                                                                        | [Authentication](#oauth-scope-requirement)                                                                                    |
| `claude.ai rejected the session token` / `session token rejected`                                                                                                                                     | [Authentication](#claude-ai-rejected-the-session-token)                                                                       |
| `Issuer mismatch in authorization response (RFC 9207)`                                                                                                                                                | [Authentication](#issuer-mismatch-in-authorization-response)                                                                  |
| `AWS credentials expired or invalid`                                                                                                                                                                  | [Authentication](#aws-credentials-expired-or-invalid)                                                                         |
| `AWS authentication failed`                                                                                                                                                                           | [Authentication](#aws-authentication-failed)                                                                                  |
| `AWS default-chain credential resolve timed out`                                                                                                                                                      | [Authentication](#aws-default-chain-credential-resolve-timed-out)                                                             |
| `Could not load the default credentials` on Google Cloud's Agent Platform                                                                                                                             | [Automatic retries](#automatic-retries)                                                                                       |
| `Unable to connect to API`                                                                                                                                                                            | [Network](#unable-to-connect-to-api)                                                                                          |
| `Connection refused —` / `Can't reach the API server —` / `No internet route —` / `Couldn't connect through your proxy` / `Connection dropped`, each ending with an error code in parentheses         | [Network](#unable-to-connect-to-api)                                                                                          |
| `Unable to connect to Anthropic services` during setup                                                                                                                                                | [Network](#unable-to-connect-to-anthropic-services)                                                                           |
| `Socket is closed`                                                                                                                                                                                    | [Network](#socket-is-closed)                                                                                                  |
| `Waiting for API response · will retry in`                                                                                                                                                            | [Automatic retries](#automatic-retries), or [Network](#unable-to-connect-to-api) if it persists                               |
| `API returned an empty or malformed response`                                                                                                                                                         | [Network](#api-returned-an-empty-or-malformed-response)                                                                       |
| `Streaming response ended before any complete data was received`                                                                                                                                      | [Network](#streaming-response-ended-before-any-complete-data-was-received)                                                    |
| `Bedrock streaming response has content-type "..."; expected "application/vnd.amazon.eventstream"`                                                                                                    | [Network](#bedrock-streaming-response-has-an-unexpected-content-type)                                                         |
| `SSL certificate verification failed`                                                                                                                                                                 | [Network](#ssl-certificate-errors)                                                                                            |
| `SSL certificate error (...)` during login or startup                                                                                                                                                 | [Network](#ssl-certificate-errors)                                                                                            |
| `403` with `x-deny-reason: host_not_allowed` in a cloud or routine session                                                                                                                            | [Network](#host-not-allowed-in-a-cloud-session)                                                                               |
| `proxy refused the connection`                                                                                                                                                                        | [Network](#the-proxy-refused-the-connection)                                                                                  |
| `403` with `This GraphQL query is not enabled for this session` in a cloud session                                                                                                                    | [GitHub proxy](/docs/en/cloud-environments#github-proxy)                                                                           |
| `The cloud environments service returned an empty response` / `The cloud environments service returned a response in an unexpected format`                                                            | [Network](#the-cloud-environments-service-returned-an-empty-or-unexpected-response)                                           |
| `Couldn't reconnect to your Remote Control session`                                                                                                                                                   | [Network](#couldnt-reconnect-to-your-remote-control-session)                                                                  |
| `N sessions ended while this machine was offline — the environment was cleaned up on the server and can't be resumed.`                                                                                | [Network](#sessions-ended-while-this-machine-was-offline)                                                                     |
| `Couldn't share the transcript.`                                                                                                                                                                      | [Network](#couldnt-share-the-transcript)                                                                                      |
| `Prompt is too long` / `Input is too long for requested model`                                                                                                                                        | [Request errors](#prompt-is-too-long)                                                                                         |
| `Prompt is too long · automatic compaction failed:`                                                                                                                                                   | [Request errors](#prompt-is-too-long)                                                                                         |
| `Prompt is too long · this conversation is a single exchange` / `A single-exchange conversation cannot be compacted`                                                                                  | [Request errors](#prompt-is-too-long)                                                                                         |
| `Context limit reached · /compact or /clear to continue`                                                                                                                                              | [Request errors](#prompt-is-too-long)                                                                                         |
| `Context limit reached · /clear to continue`                                                                                                                                                          | [Request errors](#prompt-is-too-long)                                                                                         |
| `capability_rejected: prompt_too_long` on a Claude apps gateway session                                                                                                                               | [Request errors](#prompt-is-too-long)                                                                                         |
| `upstream rejected the request` / `request too large for this upstream` on a Claude apps gateway session                                                                                              | [Upstream error messages](/docs/en/claude-apps-gateway-config#upstream-error-messages)                                             |
| `upstream rate limit exceeded` on a Claude apps gateway session                                                                                                                                       | [Upstream error messages](/docs/en/claude-apps-gateway-config#upstream-error-messages)                                             |
| `all upstreams failed (N attempted)` on a Claude apps gateway session                                                                                                                                 | [Upstream error messages](/docs/en/claude-apps-gateway-config#upstream-error-messages)                                             |
| `Context exceeds the ...-token limit by ... tokens` in `/context` output                                                                                                                              | [Request errors](#context-exceeds-the-token-limit)                                                                            |
| `Error during compaction: Conversation too long`                                                                                                                                                      | [Request errors](#error-during-compaction-conversation-too-long)                                                              |
| `Request too large`                                                                                                                                                                                   | [Request errors](#request-too-large)                                                                                          |
| `Request too large for the API's 32MB request limit`                                                                                                                                                  | [Request errors](#request-too-large)                                                                                          |
| `Image was too large`                                                                                                                                                                                 | [Request errors](#image-was-too-large)                                                                                        |
| `Unable to resize image`                                                                                                                                                                              | [Request errors](#unable-to-resize-image)                                                                                     |
| `PDF too large` / `PDF is password protected`                                                                                                                                                         | [Request errors](#pdf-errors)                                                                                                 |
| `Extra inputs are not permitted`                                                                                                                                                                      | [Request errors](#extra-inputs-are-not-permitted)                                                                             |
| `API Error: 400 ... tools.N.custom.input_schema: JSON schema is invalid`                                                                                                                              | [Request errors](#tool-input-schema-is-invalid)                                                                               |
| `There's an issue with the selected model`                                                                                                                                                            | [Request errors](#theres-an-issue-with-the-selected-model)                                                                    |
| `Model ... is not a recognized model id`                                                                                                                                                              | [Request errors](#model-is-not-a-recognized-model-id)                                                                         |
| `Claude Opus is not available with the Claude Pro plan`                                                                                                                                               | [Request errors](#claude-opus-is-not-available-with-the-claude-pro-plan)                                                      |
| `Model ... is restricted by your organization's settings`                                                                                                                                             | [Request errors](#model-is-restricted-by-your-organizations-settings)                                                         |
| `thinking.type.enabled is not supported for this model`                                                                                                                                               | [Request errors](#thinking-type-enabled-is-not-supported-for-this-model)                                                      |
| `Effort '<level>' isn't available with thinking turned off on this model`                                                                                                                             | [Request errors](#effort-isnt-available-with-thinking-turned-off)                                                             |
| `effort '<level>' is not supported when thinking is disabled`                                                                                                                                         | [Request errors](#effort-isnt-available-with-thinking-turned-off)                                                             |
| `max_tokens must be greater than thinking.budget_tokens`                                                                                                                                              | [Request errors](#thinking-budget-exceeds-output-limit)                                                                       |
| `API Error: 400 due to tool use concurrency issues`                                                                                                                                                   | [Request errors](#tool-use-or-thinking-block-mismatch)                                                                        |
| `[Unsupported tool content removed]`                                                                                                                                                                  | [Request errors](#unsupported-tool-content-removed)                                                                           |
| `server_tool_use.name: Input should be` on every turn of a resumed session                                                                                                                            | [Request errors](#unsupported-tool-content-removed)                                                                           |
| `<model> can't help with this. Start a new session to continue`                                                                                                                                       | [Request errors](#usage-policy-refusal)                                                                                       |
| `Claude Code is unable to respond to this request, which appears to violate our Usage Policy`                                                                                                         | [Request errors](#usage-policy-refusal)                                                                                       |
| `<model>'s safeguards flagged this message`                                                                                                                                                           | [Request errors](#safety-measures-flagged-a-cybersecurity-topic)                                                              |
| `<model> has safety measures that flagged this message for a cybersecurity topic`                                                                                                                     | [Request errors](#safety-measures-flagged-a-cybersecurity-topic)                                                              |
| `Installation was killed before it could finish (exit code 137)`                                                                                                                                      | [Installation errors](#installation-was-killed-before-it-could-finish)                                                        |
| `The connection dropped while downloading the update`                                                                                                                                                 | [Installation errors](#the-connection-dropped-while-downloading-the-update)                                                   |
| `Download timed out: exceeded the total deadline`                                                                                                                                                     | [Installation errors](#the-connection-dropped-while-downloading-the-update)                                                   |
| `--bg and --print conflict`                                                                                                                                                                           | [Command-line errors](#command-line-errors)                                                                                   |
| `Cloud sessions cannot be created from a --restricted session`                                                                                                                                        | [Command-line errors](#cloud-sessions-cannot-be-created-from-a-restricted-session)                                            |
| `Error: --json-schema is not a valid JSON Schema`                                                                                                                                                     | [Command-line errors](#command-line-errors)                                                                                   |
| `Error: Invalid --agents configuration:`                                                                                                                                                              | [Command-line errors](#invalid-agents-configuration)                                                                          |
| `Error: Settings file exceeds the 2MiB limit`                                                                                                                                                         | [Command-line errors](#settings-file-exceeds-the-2mib-limit)                                                                  |
| `The current directory no longer exists (it was deleted or moved)` / `Can't read the current directory`                                                                                               | [Command-line errors](#the-current-directory-no-longer-exists)                                                                |
| `Error: Workspace not trusted` when starting Remote Control                                                                                                                                           | [Command-line errors](#workspace-not-trusted-when-starting-remote-control)                                                    |
| `` `<flag>` before `remote-control` is not carried over to the sessions Remote Control starts ``                                                                                                      | [Command-line errors](#not-carried-over-to-the-sessions-remote-control-starts)                                                |
| `` `claude import` is not yet available in this build ``                                                                                                                                              | [Command-line errors](#claude-import-is-not-yet-available-in-this-build)                                                      |
| `Could not read Claude Code config`                                                                                                                                                                   | [Command-line errors](#could-not-read-claude-code-config)                                                                     |
| `Could not import <server>: <reason>`                                                                                                                                                                 | [Command-line errors](#could-not-import-a-server-from-claude-desktop)                                                         |
| `is Anthropic-hosted and doesn't support local OAuth`                                                                                                                                                 | [Command-line errors](#anthropic-hosted-and-doesnt-support-local-oauth)                                                       |
| `Server rejected the Authorization header minted by the configured headersHelper`                                                                                                                     | [Command-line errors](#server-rejected-the-authorization-header-minted-by-the-configured-headershelper)                       |
| `Error: MCP tool <name> (passed via --permission-prompt-tool) not found`                                                                                                                              | [Command-line errors](#mcp-permission-prompt-tool-not-found)                                                                  |
| `Shell command failed for pattern "..."`, from `/security-review` or any skill that injects dynamic context                                                                                           | [Command-line errors](#security-review-fails-without-origin-head)                                                             |
| `Shell command permission check failed for pattern "..."`, from a skill that injects dynamic context                                                                                                  | [Command-line errors](#security-review-fails-without-origin-head)                                                             |
| ``Skill <name> requires bash (`shell: bash` in frontmatter) but Git Bash was not found``                                                                                                              | [Command-line errors](#security-review-fails-without-origin-head)                                                             |
| `Input must be provided either through stdin or as a prompt argument when using --print`                                                                                                              | [Command-line errors](#input-must-be-provided-when-using-print)                                                               |
| `Error: Input contained only whitespace`                                                                                                                                                              | [Command-line errors](#input-contained-only-whitespace)                                                                       |
| `Blank prompt — the message was only whitespace, so nothing was sent to the model.`                                                                                                                   | [Command-line errors](#input-contained-only-whitespace)                                                                       |
| `Unknown command: /<name>`, with or without a `Did you mean` suggestion                                                                                                                               | [Command-line errors](#unknown-command)                                                                                       |
| `Diff is too large for ultrareview` / `PR #<N> is too large for ultrareview`                                                                                                                          | [Command-line errors](#diff-is-too-large-for-ultrareview)                                                                     |
| `Could not find merge-base with <branch>`                                                                                                                                                             | [Command-line errors](#could-not-find-merge-base-with-the-base-branch)                                                        |
| `Your checkout has no branches (detached HEAD only)`                                                                                                                                                  | [Command-line errors](#your-checkout-has-no-branches)                                                                         |
| `Ultrareview clones <owner>/<repo> in the cloud with the GitHub account connected to your Claude account, and none is connected`                                                                      | [Command-line errors](#no-github-account-is-connected-to-your-claude-account)                                                 |
| `Your connected GitHub account can't see <owner>/<repo>`                                                                                                                                              | [Command-line errors](#your-connected-github-account-cant-see-the-repository)                                                 |
| `The GitHub App preflight failed transiently (network or service hiccup) — retry in a moment to start from GitHub instead`                                                                            | [Command-line errors](#the-github-app-preflight-failed-transiently)                                                           |
| `Failed to resume the conversation`                                                                                                                                                                   | [Command-line errors](#failed-to-resume-the-conversation)                                                                     |
| `No conversation found with session ID: <session-id>`                                                                                                                                                 | [Command-line errors](#no-conversation-found-with-the-session-id)                                                             |
| `Cannot switch renderers in this session`                                                                                                                                                             | [Command-line errors](#cannot-switch-renderers-in-this-session)                                                               |
| `Cannot switch renderers while work is running in the background`                                                                                                                                     | [Command-line errors](#cannot-switch-renderers-in-this-session)                                                               |
| `Couldn't read your Zed keymap` / `Couldn't back up your Zed keymap` / `Couldn't update your Zed keymap`                                                                                              | [Command-line errors](#terminal-setup-left-your-zed-keymap-unchanged)                                                         |
| `Your Zed keymap isn't a readable list of keybindings`                                                                                                                                                | [Command-line errors](#terminal-setup-left-your-zed-keymap-unchanged)                                                         |
| `Marketplace "<name>" is registered from an untrusted source`                                                                                                                                         | [Plugin errors](#marketplace-is-registered-from-an-untrusted-source)                                                          |
| `references ${user_config.*} in a shell-form command`                                                                                                                                                 | [Plugin errors](#plugin-command-references-user-config)                                                                       |
| `Monitor "<name>" from plugin <plugin> references ${user_config.*} in its command`                                                                                                                    | [Plugin errors](#plugin-command-references-user-config)                                                                       |
| `headersHelper for MCP server '<name>' references ${user_config.*}`                                                                                                                                   | [Plugin errors](#plugin-command-references-user-config)                                                                       |
| `Plugin archive integrity check failed`                                                                                                                                                               | [Plugin errors](#plugin-archive-integrity-check-failed)                                                                       |
| `path escapes plugin directory`                                                                                                                                                                       | [Plugin errors](#path-escapes-plugin-directory)                                                                               |
| `Failed to load marketplace configuration`                                                                                                                                                            | [Plugin errors](#failed-to-load-marketplace-configuration)                                                                    |
| `Marketplace configuration file is corrupted`                                                                                                                                                         | [Plugin errors](#failed-to-load-marketplace-configuration)                                                                    |
| `would be spawned with zero tools — refusing`                                                                                                                                                         | [Tool errors](#agent-would-be-spawned-with-zero-tools)                                                                        |
| `File is covered by a Read deny rule in your permission settings`                                                                                                                                     | [Tool errors](#file-is-covered-by-a-read-deny-rule)                                                                           |
| `subagent_type is required: the general-purpose agent is not available in this session`                                                                                                               | [Tool errors](#subagent-type-is-required)                                                                                     |
| `Error: this write left the memory index at MEMORY.md at ..., over its ... read limit`                                                                                                                | [Tool errors](#memory-index-is-over-its-read-limit)                                                                           |
| `pkill: refusing to run`                                                                                                                                                                              | [Tool errors](#pkill-pattern-matches-the-claude-code-process)                                                                 |
| `Failed to write to <name>'s inbox — nothing was sent`                                                                                                                                                | [Tool errors](#failed-to-write-to-a-teammate-inbox)                                                                           |
| `Failed to write the plan approval request to the lead's inbox — plan not submitted`                                                                                                                  | [Tool errors](#failed-to-write-to-a-teammate-inbox)                                                                           |
| `Message too large for cross-session delivery`                                                                                                                                                        | [Tool errors](#message-too-large-for-cross-session-delivery)                                                                  |
| `Too many messages to this session just now`                                                                                                                                                          | [Tool errors](#too-many-messages-to-this-session-just-now)                                                                    |
| `Refusing to send: reply target is a symlink` / `Refusing to send: cannot vet reply target`                                                                                                           | [Tool errors](#refusing-to-send-a-cross-session-message)                                                                      |
| `Refusing to send: connected endpoint is not the expected process` / `Refusing to send: connected endpoint identity could not be read`                                                                | [Tool errors](#refusing-to-send-a-cross-session-message)                                                                      |
| `Refusing to send: connected endpoint is not owned by this user` / `Refusing to send: connected endpoint owner could not be read`                                                                     | [Tool errors](#refusing-to-send-a-cross-session-message)                                                                      |
| `Refusing to send: connected endpoint is a different process with the expected pid`                                                                                                                   | [Tool errors](#refusing-to-send-a-cross-session-message)                                                                      |
| `Refusing to read <path>: its symlink resolution changed after permission was checked` / `Refusing to search <path>: its symlink resolution changed after permission was checked`                     | [Tool errors](#refusing-after-a-symlink-changed)                                                                              |
| `Refusing to write <path>: its parent-directory symlink resolution changed after permission was checked` / `Refusing to write <path>: it is a symbolic link. Write to the link's target path instead` | [Tool errors](#refusing-after-a-symlink-changed)                                                                              |
| `Refusing to search <path>: a path one of its Read deny rules is written through changed while the search was being prepared` / `Refusing to search <path>: it could not be opened`                   | [Tool errors](#refusing-after-a-symlink-changed)                                                                              |
| `its permission check expired before it ran (too many concurrent file operations)` / `ripgrep was found only by name on PATH`                                                                         | [Tool errors](#refusing-after-a-symlink-changed)                                                                              |
| `Can't open MCP settings while no terminal is attached to this background session`                                                                                                                    | [Background session errors](#commands-refused-in-a-background-session)                                                        |
| `Can't open MCP settings in a background session`                                                                                                                                                     | [Background session errors](#commands-refused-in-a-background-session)                                                        |
| `blocked because the path is spelled in a form that cannot be safely resolved`                                                                                                                        | [Background session errors](#write-or-command-blocked-because-the-path-cannot-be-safely-resolved)                             |
| `blocked because the path is network-shaped`                                                                                                                                                          | [Background session errors](#write-or-command-blocked-because-the-path-names-a-network-location)                              |
| `This session has no saved transcript`                                                                                                                                                                | [Background session errors](#this-session-has-no-saved-transcript)                                                            |
| `Can't open — this session is running in another terminal`                                                                                                                                            | [Background session errors](#this-session-is-running-in-another-terminal)                                                     |
| `This conversation is already open in another running Claude session`                                                                                                                                 | [Background session errors](#this-session-is-running-in-another-terminal)                                                     |
| `This session's saved conversation is no longer on disk`                                                                                                                                              | [Background session errors](#this-sessions-saved-conversation-is-no-longer-on-disk)                                           |
| `kept <id> — worktree has commits that are not pushed anywhere`                                                                                                                                       | [Background session errors](#worktree-has-commits-that-are-not-pushed-anywhere)                                               |
| `terminal host process died — press Enter to restart` / `This session's terminal host process died`                                                                                                   | [Background session errors](#terminal-host-process-died)                                                                      |
| `Session isn't responding` / `Press enter again to restart this session — it isn't responding`                                                                                                        | [Background session errors](#session-isnt-responding)                                                                         |
| `Session <id> was stopped while the respawn was in flight`                                                                                                                                            | [Background session errors](#session-was-stopped-while-the-respawn-was-in-flight)                                             |
| `This session was running agent '<name>', which is no longer available`                                                                                                                               | [Background session errors](#session-agent-no-longer-available)                                                               |
| `CLAUDE_CODE_PROCESS_WRAPPER: launcher ...`                                                                                                                                                           | [Background session errors](#claude_code_process_wrapper-launcher-errors)                                                     |
| `EUNKNOWN: unknown error, uv_spawn`                                                                                                                                                                   | [Background session errors](#eunknown-when-starting-a-background-session)                                                     |
| `EACCES: permission denied, posix_spawn`                                                                                                                                                              | [Background session errors](#eacces-when-starting-a-background-session)                                                       |
| `exited before it became reachable`                                                                                                                                                                   | [Background session errors](#background-service-exited-before-it-became-reachable)                                            |
| `Claude Code process exited with code N`                                                                                                                                                              | [Wrapper and IDE errors](#claude-code-process-exited-with-code-n)                                                             |
| `Could not locate the Claude CLI on PATH`                                                                                                                                                             | [Wrapper and IDE errors](#could-not-locate-the-claude-cli-on-path)                                                            |
| `Restored the code, but skipped N files`                                                                                                                                                              | [Rewind warnings](#restored-the-code-but-skipped-files)                                                                       |
| `Transcript writes are failing (...)`                                                                                                                                                                 | [Session saving warnings](#transcript-writes-are-failing)                                                                     |
| `Transcript saving is off — CLAUDE_CODE_SKIP_PROMPT_HISTORY is set`                                                                                                                                   | [Session saving warnings](#transcript-saving-is-off-skip-prompt-history)                                                      |
| `Transcript saving is off — inherited CLAUDE_CODE_CHILD_SESSION marker`                                                                                                                               | [Session saving warnings](#transcript-saving-is-off-child-session-marker)                                                     |
| `Claude Code's fullscreen renderer didn't finish starting last time on this machine` / `Claude Code's fullscreen renderer has repeatedly failed to start on this machine`                             | [Configuration warnings](#fullscreen-failed-start-notice)                                                                     |
| `Claude Code exited after an unrecoverable interface error (...)`                                                                                                                                     | [Configuration warnings](#exited-after-an-unrecoverable-interface-error)                                                      |
| `Agent descriptions are over the 15.0k-token limit`                                                                                                                                                   | [Configuration warnings](#agent-descriptions-are-over-the-15000-token-limit)                                                  |
| `Ignoring N permissions.allow entries from ... this workspace has not been trusted`                                                                                                                   | [Configuration warnings](#workspace-has-not-been-trusted)                                                                     |
| `Remote managed settings failed to load (<cause>)`                                                                                                                                                    | [Configuration warnings](#remote-managed-settings-failed-to-load)                                                             |
| `"crossSessionInbound" must be one of "accept", "hold", "refuse"`                                                                                                                                     | [Configuration warnings](#crosssessioninbound-must-be-one-of-accept-hold-refuse)                                              |
| `headersHelper not run — this workspace has no persisted trust`                                                                                                                                       | [Configuration warnings](#headershelper-not-run)                                                                              |
| `... is not matched by file permission checks`                                                                                                                                                        | [Configuration warnings](#is-not-matched-by-file-permission-checks)                                                           |
| `... has a wildcard before the rest of the command`                                                                                                                                                   | [Configuration warnings](#has-a-wildcard-before-the-rest-of-the-command)                                                      |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT is set, but the 200K limit isn't enforced`                                                                                                                            | [Configuration warnings](#the-200k-limit-isnt-enforced)                                                                       |
| `[claude-code:unrecognized_model]`                                                                                                                                                                    | [Configuration warnings](#unrecognized-model-id-on-a-request)                                                                 |
| Responses seem lower quality than usual                                                                                                                                                               | [Response quality](#responses-seem-lower-quality-than-usual)                                                                  |

## Automatic retries

Claude Code retries transient failures up to 10 times with exponential backoff before showing you an error. It doesn't always retry a failure that arrives partway through Claude's response. When you see one of the errors on this page, Claude Code has already made whatever retries apply to that failure; the lists below say which failures get the full budget, which get a smaller one, and which get none.

Claude Code retries these failures:

* Server errors, overloaded responses, and request timeouts that arrive before any of Claude's response has streamed.
* Dropped connections. When a connection drops partway through a request before Claude has completed any part of its response, including its thinking, Claude Code re-issues the request with the same backoff and the turn continues, even if some text had already started streaming. When it drops after Claude has finished thinking but before it has started any text or tool call, Claude Code instead re-issues the request up to two times in quick succession, and ends the turn with `Connection lost before a response was produced` if the connection keeps dropping at that point.
* A connection that Claude Code detects was broken by your computer going to sleep partway through a request. Claude Code counts it as a dropped connection under the rules above; once the retry label names the specific reason, it reads `Connection lost while your computer was asleep`, and if the turn ends after Claude has finished thinking but before any text or tool call, the message reads `Your computer went to sleep before a response was produced`.
* A stalled response stream, when the response headers have arrived but none of Claude's response has arrived, or when Claude has finished thinking but hasn't started any text or tool call: Claude Code aborts the stalled connection and re-issues the request at most once, outside the 10-attempt budget above. If the response stalls a second time after Claude has finished thinking but before any text or tool call, Claude Code ends the turn with `The response stalled before a response was produced`.
* A streaming request the API never answers with response headers, on a connection where the [first-byte deadline runs](/docs/en/network-config#streaming-idle-watchdogs): Claude Code aborts it at the deadline and re-sends it at most once per model request, within the retry budget, then ends the turn with [No response from API](#no-response-from-api) if that attempt goes unanswered too. On other connections, the request waits out `API_TIMEOUT_MS`. When you set `CLAUDE_CODE_RETRY_WATCHDOG`, the one-retry cap doesn't apply.
* Temporary 429 throttles, but not a gateway's spend-limit `429`, which isn't a throttle; see [Spend limit reached](#spend-limit-reached).
  * When you're signed in with a claude.ai subscription, this includes 429 throttles that don't carry your plan's quota headers. Before v2.1.199, Claude Code retried those throttles only for API key and Enterprise sign-ins.
* A request rejected because the input plus `max_tokens` exceeds the context limit. Re-sending it unchanged would fail the same way, so Claude Code retries with a reduced `max_tokens`, and stops retrying and compacts instead in two cases:
  * When no reduction can fit, for example when the conversation itself nearly fills the context window.
  * When a retry can't shrink `max_tokens` any further. Before v2.1.218, Claude Code could re-send a reduced request that still didn't fit, such as when the extended thinking budget exceeded the remaining context, until the retry budget ran out.
* An expired or missing Google Cloud credential on [Google Cloud's Agent Platform](/docs/en/google-vertex-ai), which surfaces as an error such as `Could not load the default credentials`. Claude Code discards its cached credentials and retries up to two times, running your [`gcpAuthRefresh`](/docs/en/google-vertex-ai#advanced-credential-configuration) command if you configured one, then reports the error so you can re-authenticate right away. [Google Cloud's Agent Platform troubleshooting](/docs/en/google-vertex-ai#troubleshooting) covers re-authenticating. Before v2.1.228, Claude Code retried a failing credential through the full retry budget before showing the error.
* A `401` or `403` from the Anthropic API, directly or through an [LLM gateway](/docs/en/llm-gateway), while an [`apiKeyHelper`](/docs/en/settings-reference#apikeyhelper) script supplies the credential. Claude Code re-runs the script and retries with its fresh output, within the full retry budget. When the script itself fails on the re-run, Claude Code shows [Your apiKeyHelper script is failing](#your-apikeyhelper-script-is-failing) instead.

Before v2.1.227, `Connection lost before a response was produced` read `Connection closed while thinking, before producing a response` and `The response stalled before a response was produced` read `Response stalled while thinking, before producing a response`.

Claude Code doesn't retry these failures:

* A TLS certificate validation failure, such as a TLS-inspecting proxy, a missing `NODE_EXTRA_CA_CERTS` bundle, or an expired certificate. Claude Code reports the error on the first attempt, so you can fix the certificate setup right away; see [SSL certificate errors](#ssl-certificate-errors). Claude Code still retries transient TLS conditions such as a handshake timeout. Before v2.1.199, Claude Code retried certificate failures through the full retry budget before showing the error.
* A server error, dropped connection, or stalled stream that arrives after Claude has completed a block of text or a tool call, or has started one after finishing its thinking, but before it finishes the response. Claude Code doesn't re-run the request, because that could execute the same tool calls twice. It keeps what Claude completed, runs any tool calls Claude finished, and continues the turn from their results. For what you see in an interactive session and in a non-interactive one, read [The response above may be incomplete](#the-response-above-may-be-incomplete). Before v2.1.199, Claude Code discarded the partial output and reported the whole turn as an error when a server error arrived mid-stream.
* A failure that arrives after Claude has finished the response: nothing needs retrying, so Claude Code keeps the complete response and ends the turn normally.
* An [Amazon Bedrock streaming response with an unexpected content-type](#bedrock-streaming-response-has-an-unexpected-content-type), because the gateway or proxy rewriting the response would rewrite the retry the same way. Requires Claude Code v2.1.208 or later.
* A non-streaming retry of a failed streaming request that gets a success status but [no Claude API message in the body](#api-returned-an-empty-or-malformed-response). Claude Code ends the turn with that error.
* A request that your organization's policy check denied, which surfaces as an `API Error:` line carrying the denial message. Your organization's administrators set up the check with [Inference hooks](https://platform.claude.com/docs/en/manage-claude/inference-hooks), a Claude Enterprise feature, and the message ends with the instructions they configured, or by default tells you to contact them. Claude Code doesn't re-send the denied request to the same model or to a [fallback model](/docs/en/model-config#fallback-model-chains), because the denial is about the request's content rather than the model. Before v2.1.239, Claude Code could re-send a denied request, without streaming or on a configured fallback model, before showing you the denial.

### What you see while Claude Code retries or waits

While retrying, the spinner shows a `Retrying in Ns · attempt x/y` countdown after an error label. The label names the specific reason from the first attempt for failures you can act on right away: the network is down, a TLS handshake failed, or you hit a rate limit. For other errors it reads `API error` at first. As of v2.1.198 it switches to the specific reason from the third attempt, or on the final attempt when `CLAUDE_CODE_MAX_RETRIES` allows fewer than three; earlier versions switch only on the final attempt.

As of v2.1.198, the usual spinner tip is suppressed during retries. Once the error reason is revealed, if the failure is a 529 overload the line below the countdown also names where to check service status: `status.claude.com` on the Anthropic API, or the provider or gateway host named in the message on other configurations.

If no data arrives on the response stream for 20 seconds while a request is still pending, the spinner shows `Waiting for API response · will retry in … · check your network` before any retry has started. The request hasn't failed yet: the countdown runs to the point where Claude Code aborts the stalled connection. After the abort, what you see depends on how far the response had got:

* Before Claude has completed a block of text or a tool call, or started one after finishing its thinking, Claude Code retries the request or ends the turn with an error. [Automatic retries](#automatic-retries) says which stalls it retries and how many times.
* After Claude has completed a block of text or a tool call, or started one after finishing its thinking, but before Claude has finished the response, Claude Code keeps what Claude completed, continues the turn from any tool calls Claude finished, and shows [The response above may be incomplete](#the-response-above-may-be-incomplete). In a non-interactive session, Claude Code may first prompt Claude to continue the response; that entry says when it does and when you still see the notice there.
* After Claude finished the response, Claude Code ends the turn normally.

The banner clears on its own once data resumes or a retry succeeds. If it reappears on every attempt, treat it as a [network issue](#unable-to-connect-to-api). Before v2.1.185, the banner appeared after 10 seconds with different wording.

While Claude is consulting the [advisor](/docs/en/advisor), the banner appears after 90 seconds without data instead of 20, because a long advisor review can send nothing for well over 20 seconds. Before v2.1.214, the 20-second threshold applied during advisor calls too, so the banner appeared during advisor reviews even when nothing was wrong.

### Tune retry behavior

You can tune retry behavior with these environment variables:

| Variable                                              | Default | Effect                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :---------------------------------------------------- | :------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`CLAUDE_CODE_MAX_RETRIES`](/docs/en/env-vars)             | 10      | Number of retry attempts. Capped at 15 as of v2.1.186; as of v2.1.199 `CLAUDE_CODE_RETRY_WATCHDOG` raises the default and removes the cap. Lower it to surface failures faster in scripts.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [`CLAUDE_CODE_RETRY_WATCHDOG`](/docs/en/env-vars)          | unset   | Set to `1` in unattended sessions such as CI jobs to retry `429` and `529` capacity errors indefinitely instead of failing after `CLAUDE_CODE_MAX_RETRIES` attempts. Claude Code fails at once on a `429` that reports a spend limit or exhausted usage credits, even one from a [gateway spend cap](#spend-limit-reached) that resets on a schedule. Before v2.1.239, the watchdog retried these indefinitely. On v2.1.199 or later it also raises the default retry count for other transient errors, such as server errors, timeouts, and dropped connections, to 300, roughly three hours of backoff, and removes the cap of 15 on `CLAUDE_CODE_MAX_RETRIES` if you set that variable explicitly. |
| [`API_TIMEOUT_MS`](/docs/en/env-vars)                      | 600000  | Per-request timeout in milliseconds. Raise it for slow networks or proxies. It also bounds the [first-byte deadline](#no-response-from-api).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| [`CLAUDE_STREAM_FIRST_BYTE_TIMEOUT_MS`](/docs/en/env-vars) | unset   | Deadline in milliseconds for the first response byte of a streaming request. Requires Claude Code v2.1.242 or later. For how Claude Code picks the deadline when this is unset, see [No response from API](#no-response-from-api).                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

## Server errors

Most of these errors come from the inference provider: Anthropic's service on the Anthropic API, and the service behind that provider's endpoint on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or a custom gateway. [Auto mode cannot determine the safety of an action](#auto-mode-cannot-determine-the-safety-of-an-action) and [Agent terminated early due to an API error](#agent-terminated-early-due-to-an-api-error) also cover causes on your side, such as an Amazon Bedrock account that can't invoke the classifier model or a subagent that hit a usage limit.

### API Error: 500 Internal server error

Claude Code shows the status code and the API's error message for any 5xx response. The example below shows a 500 response on the Anthropic API:

```text theme={null}
API Error: 500 Internal server error. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.
```

The trailing sentence names where to check service health and varies by provider. Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry configurations name that provider's service status. A custom `ANTHROPIC_BASE_URL` names the gateway host.

This indicates an unexpected failure inside the API. It is not caused by your prompt, settings, or account.

**What to do:**

* Check [status.claude.com](https://status.claude.com), or the provider status page named in the message, for active incidents
* Wait a minute, then send your message again. Your original message is still in the conversation, so for a long prompt you can type `try again` instead of pasting the whole thing.
* If the error persists with no posted incident, run `/feedback` so Anthropic can investigate with your request details. See [Report an error](#report-an-error) if `/feedback` is unavailable in your environment.

### API Error: Repeated 529 Overloaded errors

The API is temporarily at capacity across all users. Claude Code has already retried several times before showing this message:

```text theme={null}
API Error: Repeated 529 Overloaded errors. The API is at capacity — this is usually temporary. Try again in a moment. If it persists, check https://status.claude.com.
```

The trailing sentence varies by provider in the same way as the 500 error above.

A 529 is not your usage limit and doesn't count against your quota.

**What to do:**

* Check [status.claude.com](https://status.claude.com), or the provider status page named in the message, for capacity notices
* Try again in a few minutes
* Run `/model` and switch to a different model to keep working, since capacity is tracked per model. Claude Code prompts you to do this when one model is under particularly high load, for example `Opus is experiencing high load, please use /model to switch to Sonnet`.

### Request timed out

The API didn't respond before the connection deadline.

```text theme={null}
Request timed out
```

This can happen during periods of high load or when the model is generating a very large response. The default request timeout is 10 minutes.

**What to do:**

* Retry the request
* For long-running tasks, break the work into smaller prompts
* If a slow network or proxy is the cause, raise `API_TIMEOUT_MS` as described in [Automatic retries](#automatic-retries)
* If timeouts are frequent and your network is otherwise healthy, see [Network and connection errors](#network-and-connection-errors) below

### No response from API

Claude Code sent a streaming request and the API returned no response headers within the deadline for the first byte, so Claude Code aborted the request instead of waiting for the full `API_TIMEOUT_MS` request timeout, 10 minutes by default. Claude Code sends the request again at most once per model request, within the retry budget, and ends the turn with this message when that attempt goes unanswered too. When you set [`CLAUDE_CODE_RETRY_WATCHDOG`](/docs/en/env-vars), the one-retry cap doesn't apply and Claude Code retries under the budget described in [Tune retry behavior](#tune-retry-behavior).

```text theme={null}
API Error: No response from API
```

Claude Code picks the deadline from the first of these that applies:

* [`CLAUDE_STREAM_FIRST_BYTE_TIMEOUT_MS`](/docs/en/env-vars), when you set it to 1 or more: Claude Code uses that value, clamped to between 10 seconds and 30 minutes, and adds one second for every 32KB of request body. Claude Code ignores 0 and lower.
* [`API_TIMEOUT_MS`](/docs/en/env-vars), when you set it above the byte-level watchdog timeout, 180 seconds on the Anthropic API and 300 seconds elsewhere: Claude Code uses one second less than the value you set.
* Otherwise, Claude Code uses the byte-level watchdog timeout, and adds one second for every 32KB of request body.

Whichever case applies, the deadline never exceeds one second less than a positive `API_TIMEOUT_MS`, and a positive `API_TIMEOUT_MS` under 11 seconds turns the deadline off. See [Streaming idle watchdogs](/docs/en/network-config#streaming-idle-watchdogs) for the variables that change the watchdog timeout and the connections the deadline runs on. The byte-level watchdog starts only once the response headers arrive, so a response that stops sending bytes after that follows the [stalled-stream rules](#automatic-retries) instead of this deadline.

**What to do:**

* Send your message again. Your original message is still in the conversation, so for a long prompt you can type `try again` instead of pasting the whole thing.
* If it repeats, treat it as a [network or proxy problem](#unable-to-connect-to-api). A proxy that accepts the connection and never forwards the request produces this error on every attempt.
* On a slow network, set `CLAUDE_STREAM_FIRST_BYTE_TIMEOUT_MS` to the deadline you want, or set `API_TIMEOUT_MS` above the watchdog timeout.

Before v2.1.242, Claude Code waited for the full `API_TIMEOUT_MS` request timeout, 10 minutes by default, before failing an unanswered streaming request.

### The response above may be incomplete

A streaming request failed while the response was still in progress, after Claude had completed a block of text or a tool call, or had started one after finishing its thinking. Re-sending the request could run the same tool calls twice, so Claude Code keeps the output Claude completed and appends this notice instead of discarding the turn. Which variant you see names the cause:

```text theme={null}
API Error: Server error mid-response. The response above may be incomplete.
API Error: Connection lost mid-response. The response above may be incomplete.
API Error: Your computer went to sleep mid-response. The response above may be incomplete.
API Error: The response stopped arriving. The response above may be incomplete.
```

* `Server error mid-response`: a mid-stream overloaded or 5xx server error. This variant requires Claude Code v2.1.199 or later; before then that case discarded the partial output and reported the whole turn as an error.
* `Connection lost mid-response`: the connection dropped.
* `Your computer went to sleep mid-response`: Claude Code detected that your computer went to sleep while the response was streaming. Once your computer wakes, Claude Code treats the connection as broken and stops reading from it.
* `The response stopped arriving`: the connection stayed open but stopped delivering data, so the streaming idle watchdog aborted it. Before v2.1.222, Claude Code could also report this failure on [gateway](/docs/en/gateways) connections reached through `ANTHROPIC_BASE_URL` or `ANTHROPIC_AWS_BASE_URL` while the server's keep-alive pings were still arriving, because it counted only parsed response events there; upgrading stops those spurious timeouts on those routes. Gateways reached through a provider base URL such as `ANTHROPIC_BEDROCK_BASE_URL` aren't wrapped by the byte watchdog; see [Streaming idle watchdogs](/docs/en/network-config#streaming-idle-watchdogs).

Before v2.1.227, `Connection lost mid-response` read `Connection closed mid-response` and `The response stopped arriving` read `Response stalled mid-stream`.

In three cases, Claude Code handles the failure without showing this notice right away:

* Earlier in the response, Claude Code either retries the failure or ends the turn with a different error. See [Automatic retries](#automatic-retries).
* When one of these failures arrives after Claude has finished the response, Claude Code keeps the complete response and ends the turn normally, without this notice. Before v2.1.222, Claude Code showed this notice when the connection dropped or stalled after the response finished, and reported the turn as an error even though the response was complete.
* In a [non-interactive session](/docs/en/headless), such as a `-p` run, an [Agent SDK](/docs/en/agent-sdk/overview) run, or a [cloud session](/docs/en/claude-code-on-the-web), you don't have to send `continue` yourself when the cut-off response is in the main conversation and contains text but no tool calls: Claude Code keeps the partial output and prompts Claude to continue from where it stopped, up to three times in a row. You see this notice for such a response only once Claude Code has used up those continuations. Before v2.1.246, Claude Code ended a non-interactive turn with this notice on the first cut-off.

**What to do:**

* In an interactive session, read the response that remains on screen: Claude Code keeps every block Claude completed before the error, but discards an interrupted final block when the turn ends, so the final sentences or tool calls may be missing. Reply with `continue` to have Claude pick up from its last completed block.
* In [non-interactive mode](/docs/en/headless) (`-p`):
  * With the default text output, Claude Code prints the last completed block of text it still holds from earlier in the turn, followed by this message. When it holds none, Claude Code prints this message alone, for example because Claude Code compacted the conversation mid-turn and cleared that text. Before v2.1.219, Claude Code printed only this message in `-p` text output and dropped the response it had already produced.
  * With `--output-format json` or `stream-json`, Claude Code reports this message in the `result` field.
  * To continue the turn once the connection is stable, resume the session and send `continue` as described in [Continue conversations](/docs/en/headless#continue-conversations).

### Auto mode cannot determine the safety of an action

The model that [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode) uses to classify actions couldn't produce a decision, so auto mode didn't approve the action automatically. The message you see depends on how the classifier failed.

Reads, searches, and edits inside your working directory skip the classifier, so they keep working in all of these cases.

When the classifier model is unavailable:

```text theme={null}
<model> is temporarily unavailable, so auto mode cannot determine the safety of <tool> right now. Wait a moment and then try this action again.
```

When Claude Code can determine the failure category, it names the category in parentheses after `temporarily unavailable`, for example `<model> is temporarily unavailable (rate-limited), so auto mode cannot determine the safety of <tool> right now`. The categories are `(rate-limited)`, `(overloaded)`, `(server error)`, `(timed out)`, and `(connection failed)`. Rate-limited, overloaded, and server errors are transient, and retrying works. If `(timed out)` or `(connection failed)` repeats, check your connection; see [Unable to connect to API](#unable-to-connect-to-api). Before v2.1.229, the message never named a category and read `Wait briefly and then try this action again`.

When no category fits, the message appears with no category in parentheses; more than one failure produces that form. On [Amazon Bedrock](/docs/en/amazon-bedrock), including the [Mantle endpoint](/docs/en/amazon-bedrock#use-the-mantle-endpoint), it also appears when your AWS account can't invoke the model named in the message, and that failure repeats on every retry until your account is granted access to the model.

**What to do:**

* Retry after a few seconds; Claude sees the same message and usually retries on its own. A transient failure is unrelated to [auto mode eligibility](/docs/en/permission-modes#eliminate-prompts-with-auto-mode); you don't need to change settings
* If retries keep failing, continue with read-only tasks and come back to the blocked action later
* On Amazon Bedrock, if the message returns on every retry, check that your account can invoke the model it names: for standard Amazon Bedrock models, confirm your [IAM policy](/docs/en/amazon-bedrock#iam-configuration) allows invoking it; for Mantle model IDs, [contact your AWS account team](/docs/en/amazon-bedrock#mantle-endpoint-errors)

When a classifier request fails because your OAuth token expired or was rotated by another session, Claude Code refreshes the token and retries the request once, so a routine token expiry doesn't surface as this message. Before v2.1.216, an expired or rotated token failed each classifier request, and auto mode denied every checked action with this message until the token was refreshed.

When the classifier returned an unparseable response:

```text theme={null}
Auto mode could not evaluate this action and is blocking it for safety — run with --debug for details
```

**What to do:**

* Retry the action; this usually succeeds on the next attempt
* Run `claude --debug` and repeat the action to see the underlying classifier response in the debug log

When a separate API safety check blocked the classifier request because of earlier conversation content:

```text theme={null}
Auto mode could not evaluate this action and is blocking it for safety — a safety check separate from auto mode blocked this request because of earlier conversation content — it isn't about the action itself — run with --debug for details
```

Claude Code denies the action but tells Claude this isn't a judgment that the action is unsafe, and to continue with other tasks rather than retry. These denials don't count toward [auto mode's pause thresholds](/docs/en/permission-modes#when-auto-mode-falls-back). In a [non-interactive](/docs/en/headless) `-p` run, Claude Code doesn't stop the run. What Claude receives depends on where it requested the action:

* To a [background subagent](/docs/en/sub-agents#run-subagents-in-foreground-or-background) in a `-p` run without `--input-format stream-json`, Claude Code returns an error result containing `Agent aborted: auto mode classifier request refused by the safety safeguard in headless mode`
* Everywhere else, including interactive sessions and the main conversation of a `-p` run, Claude Code returns that denial to Claude

Before v2.1.225, Claude Code counted these refusals toward the pause thresholds and returned the same rejection message as a genuine classifier block.

**What to do:**

* This is not a decision about your action. Content already in your conversation triggered a safety filter on the API when auto mode sent the conversation to the classifier
* Retrying will not help; the same conversation content will trigger the filter again
* In an interactive session, switch to a different [permission mode](/docs/en/permission-modes) so you can approve the action when prompted
* Start a fresh conversation without the triggering content

When the conversation has grown larger than the classifier's context window:

```text theme={null}
Auto mode classifier transcript exceeded context window — falling back to manual approval (try /compact to reduce conversation size)
```

What happens to the action depends on where Claude requested it:

* In an interactive session, auto mode falls back to a normal permission prompt for that action so you can approve or deny it manually
* To a [background subagent](/docs/en/sub-agents#run-subagents-in-foreground-or-background) in a [non-interactive](/docs/en/headless) `-p` run without `--input-format stream-json`, Claude Code returns an error result containing `Agent aborted: auto mode classifier transcript exceeded context window in headless mode`, and the run continues
* Elsewhere in a `-p` run without a [`--permission-prompt-tool`](/docs/en/cli-reference#cli-flags), there is no prompt to fall back to, so the action doesn't run and the run continues

**What to do:**

* In an interactive session, approve or deny the action in the prompt that appears
* In an interactive session, run `/compact` to reduce the conversation size so subsequent actions fit within the classifier window again

### Agent terminated early due to an API error

A [subagent](/docs/en/sub-agents)'s API request failed terminally, for example because a usage limit was reached or retries for a server error ran out, so the subagent stopped before finishing its task. This message requires Claude Code v2.1.199 or later; before then the API error text was returned to Claude as if it were the subagent's result.

```text theme={null}
Agent terminated early due to an API error: <error detail>
```

**What to do:**

* Match the error detail after the colon to its own section on this page, such as [Usage limits](#usage-limits) or [Server errors](#server-errors), and follow that section's steps
* Once the underlying error clears, ask Claude to retry the task or [resume the subagent](/docs/en/sub-agents#resume-subagents)

When a rate limit, overload, or server error interrupts a foreground subagent that already produced text output, Claude receives that partial output marked as incomplete instead of this error. A subagent whose only output was tool calls gets this error too; in v2.1.199 that shape returned an empty partial result instead. See [API errors in subagents](/docs/en/sub-agents#api-errors-in-subagents).

## Usage limits

Most errors in this section mean a quota tied to your account or plan has been reached. Three work differently: [`Server is temporarily limiting requests`](#server-is-temporarily-limiting-requests) is a server-side throttle unrelated to your plan quota, [`Usage credits required for 1M context`](#usage-credits-required-for-1m-context) is an entitlement check rather than an exhausted quota, and [`The prompt to confirm went unanswered`](#the-prompt-to-confirm-went-unanswered) means a usage-credits consent prompt closed unanswered, whether or not a quota was reached.

<h3 id="youve-hit-your-session-limit">
  You've hit your session limit
</h3>

Subscription plans include a rolling usage allowance. When it runs out you see one of these messages:

```text theme={null}
You've hit your session limit · resets 3:45pm
You've hit your weekly limit · resets Mon 12:00am
You've hit your Opus limit · resets 3:45pm
You've hit your Sonnet limit · resets 3:45pm
```

Claude Code blocks further requests until the reset time shown in the message. The session and weekly limits are shared across all models, so switching models doesn't restore access. The Opus and Sonnet limits each apply only to requests to that model family, so switching to a model outside the family with `/model` keeps you working.

In an interactive session signed in with a claude.ai subscription, Claude Code can also wait in the open session and continue the interrupted task shortly after the reset. While it waits, a line at the bottom of the session reads `Usage limit reached · continuing automatically at 3:45pm · esc to cancel`. Press `Esc` at an empty prompt to cancel the wait. See [Wait for a usage limit to reset](/docs/en/interactive-mode#wait-for-a-usage-limit-to-reset) for what you see, how to start or cancel a wait, and how to turn automatic continue off. Before v2.1.234, Claude Code didn't offer this wait.

Usage counts against the session and weekly allowances at the same time. A single burst of heavy activity, such as a large workflow fanout, can exhaust the weekly allowance before the session window resets.

**What to do:**

* Wait for the reset time shown in the error
* In the Code tab of the [Desktop app](/docs/en/desktop), the session-limit card offers an **Auto-continue when limits reset** checkbox. The weekly-limit card doesn't. When it's checked, the Desktop app retries the interrupted turn after the reset and shows the retry time on the card. The Desktop checkbox and the CLI's **Continue automatically at usage limit** setting in `/config` are separate, so turn each off on its own.
* For the Opus or Sonnet limit, run `/model` and switch to a model outside that family to keep working. Each model has its own prompt cache, so the next request re-reads the whole conversation with no cache hits; see [Switching models](/docs/en/prompt-caching#switching-models)
* Run `/usage` to see your plan limits and when they reset
* Run `/usage-credits` to buy additional usage on Pro and Max, or to request it from your admin on Team and Enterprise. See [usage credits for paid plans](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) for how this is billed.
* To upgrade your plan for higher base limits, see [claude.com/pricing](https://claude.com/pricing)

To watch your remaining allowance before you hit the limit, add the `rate_limits` fields to a [custom status line](/docs/en/statusline#rate-limit-usage), or in the Desktop app click the [usage ring](/docs/en/desktop#check-usage) next to the model picker.

### Usage credits required for 1M context

The selected model uses the 1M-token extended context window, and your plan only includes it through usage credits.

```text theme={null}
API Error: Usage credits required for 1M context · run /usage-credits to turn them on, or /model to switch to standard context
```

This is an entitlement check, not a quota exhaustion. It fires even when your session and weekly allowances have capacity remaining. See [Extended context](/docs/en/model-config#extended-context) for which plans include 1M context directly and which require usage credits. Claude Code runs this check when you pick the model with `/model`, and only on a direct connection to the Anthropic API; if you point `ANTHROPIC_BASE_URL` at an [LLM gateway](/docs/en/llm-gateway), `/model` allows the `[1m]` selection and the gateway decides whether the request succeeds.

When this error appears mid-conversation because the context grew past 200K tokens, Claude Code automatically compacts the conversation back under the standard context limit and keeps the session at that limit afterward, so no action is needed. On versions before v2.1.172, the error repeated on every subsequent request including `/compact`; run `/clear` on those versions to recover. The steps below apply when you explicitly selected a `[1m]` model.

**What to do:**

* Run `/model` and select the variant without the `[1m]` suffix to fall back to the standard context window
* Run `/usage-credits` to turn on metered billing for the 1M variant on Pro and Max, or to request it from your admin on Team and Enterprise
* If the error persists after `/model`, a 1M model ID may be set elsewhere. See [Setting your model](/docs/en/model-config#setting-your-model) for the configuration locations to check in priority order.
* To remove 1M variants from the model picker entirely, set [`CLAUDE_CODE_DISABLE_1M_CONTEXT=1`](/docs/en/env-vars)

### The prompt to confirm went unanswered

On plans where Fable 5 usage [bills to usage credits](/docs/en/model-config#fable-5-and-usage-credits), Claude Code asks you to confirm before a request bills them. When nobody answers that consent prompt in a session that may have no one at its terminal, Claude Code closes the prompt and ends the turn with one of these messages:

```text theme={null}
Fable 5 limit reached · continuing on Fable 5 uses usage credits, and the prompt to confirm went unanswered — nothing was sent · answer it where this session is running, or /model to change
Fable 5 now uses usage credits · the prompt to confirm went unanswered — nothing was sent · answer it where this session is running, or /model to change
```

This happens in [Remote Control](/docs/en/remote-control) sessions, [background sessions](/docs/en/agent-view), and [agent team](/docs/en/agent-teams) teammate sessions. Claude Code shows the consent prompt only in the session's own interactive view: the terminal where it runs, or, for a background session, the [agents view](/docs/en/agent-view) once you attach. A Remote Control client can't display it. Claude Code closes the prompt at the [`dialogExpiry`](/docs/en/settings-reference#dialogexpiry) deadline, five minutes by default, or as soon as a new prompt arrives while nobody has typed at that terminal, such as a prompt sent from a Remote Control client. Typing at the terminal where the session runs cancels the deadline, and Claude Code waits for your answer. In a background session's attached view, typing doesn't cancel the deadline, and a new prompt still closes the consent prompt, so answer before either happens. Claude Code sends nothing and keeps your model, so when you send your next prompt, Claude Code shows the consent prompt again.

**What to do:**

* At the terminal where the session runs, send another prompt and answer the consent prompt when it reappears. For a background session, attach to it from the [agents view](/docs/en/agent-view) first. Resending from a Remote Control client shows this message again, because the client can't display the prompt.
* Run `/model` to switch to a model that doesn't bill usage credits
* To give yourself more time to reach that terminal, set [`dialogExpiry`](/docs/en/settings-reference#dialogexpiry) to a longer value or `"never"`

Before v2.1.236, this message didn't appear: while a Remote Control client was connected, Claude Code waited 60 seconds for an answer and then continued the turn on your default model.

### Server is temporarily limiting requests

The API applied a short-lived throttle that is unrelated to your plan quota.

```text theme={null}
API Error: Server is temporarily limiting requests (not your usage limit)
```

Claude Code tells these apart from your plan limit by the absence of the unified quota headers a real limit response carries. As of v2.1.199 this is [retried automatically](#automatic-retries) with backoff before being shown, whichever way you authenticate. On earlier versions, a session signed in with a claude.ai subscription failed the turn on the first occurrence; only API key and Enterprise sign-ins retried it.

**What to do:**

* Wait briefly and try again
* Check [status.claude.com](https://status.claude.com) if it persists

### Request rejected (429)

You have hit the rate limit configured for your API key, Amazon Bedrock project, or Google Cloud project.

```text theme={null}
API Error: Request rejected (429) · this may be a temporary capacity issue. If it persists, check https://status.claude.com.
```

The trailing sentence names where to check service health and varies by provider. Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry configurations name that provider's service status instead of the Anthropic status page. A custom `ANTHROPIC_BASE_URL` names the gateway host.

**What to do:**

* Run `/status` and confirm the active credential is the one you expect. A stray `ANTHROPIC_API_KEY` in your environment can route requests through a low-tier key instead of your subscription.
* Check your provider console for the active limits and request a higher tier if needed
* For Anthropic API keys, see the [rate limits reference](https://platform.claude.com/docs/en/api/rate-limits) for how tiers work and how to set per-workspace caps
* Reduce concurrency: lower [`CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY`](/docs/en/env-vars), avoid running many parallel subagents, or switch to a smaller model with `/model` for high-volume scripted runs

<h3 id="spend-limit-reached">
  Spend limit reached
</h3>

You connect through a [Claude apps gateway](/docs/en/claude-apps-gateway) and have passed a [spend cap](/docs/en/claude-apps-gateway-spend-limits) your gateway operator set. The gateway blocks your requests until the named period resets or the operator raises the cap. It marks each blocked `429` response `x-should-retry: false`, so Claude Code shows this message without retrying.

```text theme={null}
spend limit reached (daily; resets 2026-08-09 00:00 UTC)
```

The message names the cap's period and reset time, and when the operator configured a `blocked_message`, their instructions follow it. Before v2.1.225, the message read only `spend limit reached`; a gateway on an older version still sends that shorter form.

**What to do:**

* Wait for the reset time the message names, or follow the operator's instructions if the message carries them
* Ask your gateway operator to raise the cap if you hit it routinely

A related message, `spend limit unavailable`, means the gateway could not read its spend records and blocked the request as a precaution rather than over your cap. It usually clears on its own; if it persists, tell your gateway operator.

### Credit balance is too low

Your Console organization has run out of prepaid credits, or Claude Code is sending your requests with a Console API key when you meant to use your subscription.

```text theme={null}
Credit balance is too low
```

**What to do:**

* If you have a Pro, Max, Team, or Enterprise plan and see this, run `/status` and check the `API key` row. An approved `ANTHROPIC_API_KEY` in your environment routes requests through that key instead of your subscription. Unset it in the current shell and remove it from your shell profile, then relaunch `claude`. Run `/login` if you haven't signed in with your subscription yet.
* Add credits at [platform.claude.com/settings/billing](https://platform.claude.com/settings/billing), and consider enabling auto-reload there so the balance refills before it hits zero
* Set per-workspace spend caps in the Console to prevent a single project from draining the org balance. See [Manage costs effectively](/docs/en/costs).

### Could not update your spend limit

The server rejected a spend limit change you made from the prompt that appears when you reach your spend limit.

```text theme={null}
Could not update your spend limit: <reason from the server>
```

When the server explains the rejection, the message ends with that reason, and retrying the same value fails again. When the failure has no server-provided reason, such as a dropped connection, the message reads `Could not update your spend limit. Press Enter to retry.` and retrying can succeed. Before v2.1.216, Claude Code showed the generic form for every failure.

**What to do:**

* If the message includes a reason, choose a limit that satisfies it, such as a lower amount
* If the message shows only the generic form, retry; the failure may be transient
* If the change keeps failing, make it from your [claude.ai billing settings](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) in the browser instead

## Authentication errors

These errors mean Claude Code cannot prove who you are to the API. Run `/status` at any time to see which credential is currently active.

### Not logged in

No valid credential is available for this session.

```text theme={null}
Not logged in · Please run /login
```

**What to do:**

* Run `/login` to authenticate with your Claude subscription or Console account
* If you expected an environment variable to authenticate you, confirm `ANTHROPIC_API_KEY` is set and exported in the shell where you launched `claude`
* For CI or automation where interactive login is not possible, configure an [`apiKeyHelper`](/docs/en/settings-reference#apikeyhelper) script that fetches a key at startup
* See [Authentication precedence](/docs/en/authentication#authentication-precedence) to understand which credential Claude Code uses when several are present

If you are prompted to log in repeatedly, see [Not logged in or token expired](/docs/en/troubleshoot-install#not-logged-in-or-token-expired) for system clock checks and macOS credential-storage recovery steps.

### Could not resolve authentication method

The session reached the API client without any credential. [Background sessions](/docs/en/agent-view) and cloud sessions show this message when the worker starts without a credential. Interactive, `-p`, and Agent SDK runs report the same condition as [Not logged in](#not-logged-in) and write this string only to their debug log, so if you found it there, follow that entry instead.

```text theme={null}
Could not resolve authentication method. Expected one of apiKey, authToken, credentials, config, or profile to be set. Or for one of the "X-Api-Key" or "Authorization" headers to be explicitly omitted
```

On current versions the error means no credential was available to the worker process. Before v2.1.174, a background session assigned to an idle pre-initialized worker could fail this way even when valid credentials were configured. Before v2.1.176, a cloud session that sat idle before being claimed could too. Upgrade to recover.

**What to do:**

* Upgrade to v2.1.176 or later if this appears in a background or cloud session and your credentials are already configured
* Confirm `ANTHROPIC_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN`, or your cloud provider credentials are set in the environment that launches the worker, not only in your interactive shell
* For the Agent SDK, see [authentication setup in the quickstart](/docs/en/agent-sdk/quickstart#setup)
* Run `/status` in an interactive session in the same environment to confirm which credential source resolves

### Invalid API key

The `ANTHROPIC_API_KEY` environment variable or `apiKeyHelper` script returned a key the API rejected, or Claude Code blocked a key from `ANTHROPIC_API_KEY` before sending it.

```text theme={null}
Invalid API key · Fix external API key
```

When the message continues past `Fix external API key` with a description such as `Invalid X-Api-Key header value from ANTHROPIC_API_KEY: it contains a line break at character 41 (120 characters on 2 lines).`, the API never saw the key. Claude Code found a character that HTTP headers can't carry and stopped the request before sending it. See [Invalid request header value](#invalid-request-header-value) for how to read the description and fix the value.

**What to do:**

* Check for typos and confirm the key has not been revoked in the [Console](https://platform.claude.com/settings/keys)
* In the same shell, run `env | grep ANTHROPIC`, or in PowerShell `Get-ChildItem Env:ANTHROPIC*`. Tools like direnv, dotenv shell plugins, and IDE terminals can load a stale key from a `.env` file in your project without you setting it explicitly.
* Unset `ANTHROPIC_API_KEY` and run `/login` to use subscription auth instead
* If the key comes from an [`apiKeyHelper`](/docs/en/settings-reference#apikeyhelper) script, run the script directly to confirm it prints a valid key on stdout
* Run `/status` to confirm which credential source Claude Code is actually using

### Your apiKeyHelper script is failing

Claude Code ran the command in your [`apiKeyHelper`](/docs/en/settings-reference#apikeyhelper) setting and didn't get a key back. Without one, the request reaches the API with a placeholder credential, and the API rejects it with `401`. The `Authentication` panel in the terminal shows which of these happened:

* The command exited with an error or timed out
* The command printed nothing to stdout
* The command printed something besides the key, such as a login banner or a log line. The panel shows `returned output that cannot be used as an API key` and says what's wrong, without repeating the output. Before v2.1.227, Claude Code sent whatever the command printed, after trimming surrounding whitespace.

```text theme={null}
Your apiKeyHelper script is failing · This usually means you need to re-authenticate with your provider · Run /status to see the script's error output
```

Claude Code re-runs the script and retries the request up to two more times before showing this message, so the failure surfaces within three attempts. Before v2.1.208, Claude Code spent the full [retry budget](#automatic-retries) resending the request with the placeholder credential and then reported a generic `401` authentication error instead of the script failure.

Running `/login` doesn't help here: the helper's output [takes precedence](/docs/en/authentication#authentication-precedence) over a saved login for as long as the setting is present.

**What to do:**

* Run the command configured in `apiKeyHelper` directly in your shell to reproduce the failure
* If the command reports an expired session, re-authenticate with your credential provider, for example by signing in to your SSO or secrets vault again
* Fix the command so it prints only the key to stdout, as a single token of printable ASCII up to 16,384 characters, and exits with code 0. See [rotate credentials with apiKeyHelper](/docs/en/llm-gateway-connect#rotate-credentials-with-apikeyhelper) for a working setup.
* Run `/status` to confirm `apiKeyHelper` is the active credential source. Each time the command fails, its exit code and error output appear in an `Authentication` panel in the terminal. Before v2.1.212, the panel was titled `Cloud authentication`.

### Invalid request header value

A value Claude Code was about to send as a request header contains a character that HTTP headers can't carry: a line break, a NUL byte, or a character above `U+00FF`, such as a curly quote or a zero-width space. Claude Code stops the request before anything is sent and names the variable or setting to fix. The usual cause is a credential pasted from a document or chat that carried an invisible character or a stray line break.

Claude Code runs this check when it sends requests to the Claude API directly or through an [LLM gateway](/docs/en/llm-gateway). On a third-party cloud provider such as [Amazon Bedrock](/docs/en/amazon-bedrock), Claude Code doesn't run it before sending.

```text theme={null}
Invalid auth token · Fix external auth token
Invalid ANTHROPIC_CUSTOM_HEADERS · Fix the environment variable
Invalid request header from the environment · Fix the environment variable
```

The first part of the message depends on where the bad value came from:

* `Invalid auth token`: a bearer token from [`ANTHROPIC_AUTH_TOKEN`](/docs/en/env-vars) or [`CLAUDE_CODE_OAUTH_TOKEN`](/docs/en/env-vars)
* `Invalid ANTHROPIC_CUSTOM_HEADERS`: a header name or value you set in [`ANTHROPIC_CUSTOM_HEADERS`](/docs/en/env-vars). The description counts which `Name: Value` pair is at fault, such as `distinct header 2 of 3 parsed from ANTHROPIC_CUSTOM_HEADERS`, without repeating the name or value, since you chose both.
* `Invalid request header from the environment`: a value Claude Code copies into a request header from another environment variable, such as `CLAUDE_AGENT_SDK_CLIENT_APP`. The description names the variable to fix.

Claude Code reports a bad `ANTHROPIC_API_KEY` caught by this check as [Invalid API key](#invalid-api-key), with the same trailing description. It reports a bad saved `/login` credential as [Not logged in](#not-logged-in) instead; run `/login` to save a fresh one. An [`apiKeyHelper`](/docs/en/settings-reference#apikeyhelper) script's output never reaches this check: Claude Code validates it when the script runs, and output an HTTP header can't carry fails with [Your apiKeyHelper script is failing](#your-apikeyhelper-script-is-failing).

After the second `·`, the message describes the problem, as in this full example:

```text theme={null}
Invalid auth token · Fix external auth token · Invalid Authorization header value from ANTHROPIC_AUTH_TOKEN: it contains a line break at character 41 (120 characters on 2 lines).
```

Positions count characters starting at one. The description is built from fixed phrases and character counts, so it never includes the value itself. It names the offending character only when it is a well-known invisible or typographic character, such as a byte-order mark, a zero-width space, or a curly quote, and reports anything else as `a non-ASCII character`.

**What to do:**

* Re-set the variable or setting the message names, retyping the characters around the reported position rather than pasting from the same source again
* For `ANTHROPIC_CUSTOM_HEADERS`, keep one `Name: Value` pair per line and rewrite the pair the message counts
* Run `/status` to confirm which credential source is active

### This organization has been disabled

Claude Code is using a stale `ANTHROPIC_API_KEY` from a disabled Console organization. When you have a saved subscription login, the key overrides it.

```text theme={null}
Your ANTHROPIC_API_KEY belongs to a disabled organization · Unset the environment variable to use your subscription instead
Your ANTHROPIC_API_KEY belongs to a disabled organization · Update or unset the environment variable
API Error: 400 ... This organization has been disabled.
```

The hint after the `·` depends on your saved credentials: the first form appears when a stored `/login` can take over after you unset the key, and the second when the key is your only credential.

Environment variables take precedence over `/login`, so a key exported in your shell profile or loaded from a `.env` file is used even when you have a working Pro or Max subscription. In non-interactive mode (`-p`), the key is always used when present.

**What to do:**

* Unset `ANTHROPIC_API_KEY` in the current shell and remove it from your shell profile, then relaunch `claude`
* If the message says `Update or unset`, you have no saved login to fall back to. Unset the key and run `/login`, or replace the key with one from an active Console organization.
* Run `/status` afterward to confirm the active credential is your subscription
* If no environment variable is set and the error persists, the disabled organization is the one tied to your `/login`. Contact support or sign in with a different account.

### Your organization has disabled API key authentication

This message requires Claude Code v2.1.169 or later. Your Console organization's admin has turned off API key authentication, so the API rejects the key Claude Code is sending. The recovery hint after the `·` varies by where the key came from:

```text theme={null}
Your organization has disabled API key authentication · Run /login to sign in with your claude.ai account
Your organization has disabled API key authentication · Unset ANTHROPIC_API_KEY to use your claude.ai account instead
Your organization has disabled API key authentication · Unset ANTHROPIC_API_KEY and run /login to sign in with your claude.ai account
Your organization has disabled API key authentication · Unset the apiKeyHelper setting and run /login to sign in with your claude.ai account
```

Environment variables and `apiKeyHelper` take precedence over `/login`, so running `/login` alone doesn't help while either is still supplying a key. See [Authentication precedence](/docs/en/authentication#authentication-precedence).

**What to do:**

* If the message names `ANTHROPIC_API_KEY`, unset it in the current shell and remove it from your shell profile or `.env` file, then relaunch `claude`
* If the message names `apiKeyHelper`, remove the [`apiKeyHelper`](/docs/en/settings-reference#apikeyhelper) setting from your `settings.json`
* Run `/login` to sign in with your claude.ai account
* Run `/status` afterward to confirm the active credential is your subscription rather than an API key
* If you need API key authentication for automation, ask your organization admin to re-enable it in the Console

### Your organization has disabled Claude subscription access

Your Claude organization doesn't allow signing in to Claude Code with a subscription login. Running `/login` again with the same account returns the same error.

```text theme={null}
Your organization has disabled Claude subscription access for Claude Code · Use an Anthropic API key instead, or ask your admin to enable access
```

This is a server-side organization setting, so it can't be overridden from local settings, environment variables, or CLI flags.

The Agent SDK and `-p` non-interactive mode surface this as the `oauth_org_not_allowed` error code.

**What to do:**

* Ask your admin to enable Claude Code access for your organization
* Authenticate with a Console API key instead of your subscription. See [Claude Console authentication](/docs/en/authentication#claude-console-authentication) for setup.
* If you are the admin and do not see an option to enable access, contact [Anthropic support](https://support.claude.com)

<h3 id="routines-are-disabled-by-your-organizations-policy">
  Routines are disabled by your organization's policy
</h3>

An Owner in your Team or Enterprise organization has turned off routines at the organization level. The error appears when you try to create or run a routine, for example from the [Routines](/docs/en/routines) UI on claude.ai/code. On Claude Code v2.1.227 or later, the same setting also [hides `/schedule`](/docs/en/routines#troubleshooting) in the CLI.

```text theme={null}
Routines are disabled by your organization's policy.
```

This is a server-side setting, so it can't be overridden from local settings, environment variables, or CLI flags.

**What to do:**

* Ask an Owner in your organization to enable the **Routines** toggle at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code)
* For one-off scheduled work that does not require organization-level routines, see [scheduled tasks](/docs/en/scheduled-tasks)

### Remote Control requires the Anthropic API

The session isn't talking to the Anthropic API directly, so there is no claude.ai backend for [Remote Control](/docs/en/remote-control) to pair with.

```text theme={null}
Remote Control is only available when using Claude via api.anthropic.com. CLAUDE_CODE_USE_BEDROCK is set, so this session is using Amazon Bedrock — unset it (or run in a shell without it) to use Remote Control.
```

A second sentence explains what routed the session away from the Anthropic API; before v2.1.219, the message was the first sentence alone. Depending on the cause, the message names:

* A `CLAUDE_CODE_USE_*` provider variable, such as `CLAUDE_CODE_USE_BEDROCK` for [Amazon Bedrock](/docs/en/amazon-bedrock) or `CLAUDE_CODE_USE_VERTEX` for [Google Cloud's Agent Platform](/docs/en/google-vertex-ai)
* [`ANTHROPIC_BASE_URL`](/docs/en/env-vars) pointing at a host other than `api.anthropic.com`, such as an [LLM gateway](/docs/en/llm-gateway) or proxy, even when you sign in with claude.ai; before v2.1.196, a custom base URL didn't block Remote Control
* An enterprise [cloud gateway](/docs/en/claude-apps-gateway) sign-in made through `/login`, which doesn't support Remote Control and has no variable to unset

**What to do:**

* Unset the variable the message names, such as `CLAUDE_CODE_USE_BEDROCK` or `ANTHROPIC_BASE_URL`, and restart the session, or start Remote Control from a session that talks to the Anthropic API directly
* If the variable isn't set in your shell, check the `env` key in your [settings files](/docs/en/settings#where-settings-live), which applies environment variables to every session
* For this and the other Remote Control startup messages, see [Troubleshoot Remote Control](/docs/en/remote-control#troubleshooting)

<h3 id="remote-control-couldnt-refresh-your-login">
  Remote Control couldn't refresh your login
</h3>

Claude Code runs a live [Remote Control](/docs/en/remote-control) connection on short-lived credentials that it obtains and renews using your saved claude.ai login. When claude.ai stops accepting that login, or Claude Code has no saved login left, Claude Code stops Remote Control and needs you to sign in again. Either failure can happen while Claude Code is still connecting or later, when it renews the credentials.

When Claude Code asks the login service to refresh your saved login and gets no answer, it keeps Remote Control running and tries the refresh again while the connection's current credential is still valid. A refresh gets no answer when Claude Code can't reach the login service, the request times out, or the service fails without rejecting your login. If the login service still isn't answering when that credential expires, Claude Code stops Remote Control and reports `OAuth token refresh failed`.

When Claude Code stops Remote Control, it shows the reason in a warning and in a transcript line that starts with `Remote Control disconnected`. Your local session keeps running without Remote Control. This section covers these lines:

```text theme={null}
Remote Control disconnected — Claude.ai login expired — run /login to restore Remote Control
Remote Control disconnected — Claude.ai login expired — run /login, then /remote-control
Remote Control disconnected — Claude.ai login was rejected — run /login, then /remote-control
Remote Control disconnected — OAuth token unavailable — run /login to restore Remote Control
Remote Control disconnected — OAuth token refresh failed — run /login to re-authenticate
Remote Control disconnected — JWT refresh failed: no OAuth token — run /login
Remote Control disconnected — Signed out of Claude — run /login, then /remote-control
```

Claude Code names the cause in the middle of the message:

* `Claude.ai login expired` and `Claude.ai login was rejected`: claude.ai no longer accepts your saved login token, because it expired or was revoked
* `OAuth token unavailable`: Claude Code had no saved login token when the connection's credential came due for renewal
* `OAuth token refresh failed`: claude.ai rejected your saved login token while Claude Code was reconnecting, and refreshing the token produced no new one
* `JWT refresh failed: no OAuth token`: Claude Code found no saved login token to renew with
* `Signed out of Claude`: you signed out on this machine, for example by running `/logout` in another terminal, so Claude Code has no saved login left to renew the connection with

**What to do:**

* Run `/login` to sign in again
* Run `/remote-control` to reconnect the session. Messages ending `run /login to restore Remote Control` don't need this step: Claude Code reconnects on its own once you sign in.

Before v2.1.224, `OAuth token refresh failed — run /login to re-authenticate` read `OAuth token refresh failed — re-authenticate, then re-enable Remote Control`, and `JWT refresh failed: no OAuth token — run /login` read `no OAuth token available for recovery (code <N>)`. The `Claude.ai login expired`, `Claude.ai login was rejected`, and `OAuth token unavailable` messages were added in v2.1.225.

Before v2.1.238, Claude Code reported the cases that now say `Signed out of Claude` as `JWT refresh failed: no OAuth token — run /login`, and stopped Remote Control with `Claude.ai login expired — run /login to restore Remote Control` as soon as one login refresh got no answer.

<h3 id="remote-control-stopped-because-the-signed-in-account-changed">
  Remote Control stopped because the signed-in account changed
</h3>

Claude Code shows this line during a [Remote Control](/docs/en/remote-control) session when you sign in to a different claude.ai account or organization on this machine. You made the switch outside the Claude Code session, for example by running `/login` in another terminal.

A Remote Control session that you started while signed in through `/login` belongs to the claude.ai account and organization that were signed in at the time.

```text theme={null}
Remote Control disconnected — signed-in claude.ai account or organization changed on this machine — run /remote-control to start a session for the current account, or /login to switch back, then /remote-control
```

Claude Code stops the Remote Control session as soon as claude.ai confirms that the account or organization changed. Your local session keeps running without Remote Control.

**What to do:**

* Run `/remote-control` to start a new Remote Control session under the current account or organization
* To switch back, run `/login` and sign in to the previous account or organization again. Then run `/remote-control`.

Before v2.1.234, Claude Code didn't notice when you switched to a different account or organization outside the Claude Code session. Claude Code kept the Remote Control session connected until a later request to the Remote Control server failed with `Remote Control server rejected the request (HTTP 404)`. That failure could come hours after the switch.

<h3 id="remote-control-stopped-because-the-app-running-the-session-signed-out-or-switched-accounts">
  Remote Control stopped because the app running the session signed out or switched accounts
</h3>

When the Claude desktop app or an IDE hosts your session, Claude Code gets its login token from that app rather than from `/login`. When claude.ai rejects that token, Claude Code asks the app for a new one. If the app answers that it's signed out, or that it's now signed in to a different Claude account, Claude Code ends the [Remote Control](/docs/en/remote-control) session and sends the app one of these lines:

```text theme={null}
Remote Control stopped — the app running this session is now signed in to a different Claude account
Remote Control stopped — the app running this session is signed out of Claude. Sign in there, then turn Remote Control back on
```

Your local session keeps running without Remote Control.

**What to do:**

* If the app is signed out, sign in to it again, then turn Remote Control back on in the app
* If the app switched accounts, Claude Code can't continue the ended session under the new account. Start a new Remote Control session under that account.

Before v2.1.238, Claude Code sent the app the `run /login` messages listed under [Remote Control couldn't refresh your login](#remote-control-couldnt-refresh-your-login) in both cases.

### OAuth token revoked or expired

Your saved login is no longer valid. A revoked token means you signed out everywhere or an admin removed access; an expired token means the automatic refresh failed mid-session.

Both messages report a rejection the API returned for a request Claude Code sent. When the saved login has already been cleared after a failed refresh, you see [Login expired](#login-expired) instead. If you authenticate with a long-lived token in [`CLAUDE_CODE_OAUTH_TOKEN`](/docs/en/env-vars), you see the same messages when that token expires or is revoked.

```text theme={null}
OAuth token revoked · Please run /login
OAuth token has expired · Please run /login
API Error: 401 ... authentication_error
```

**What to do:**

* Run `/login` to sign in again
* If the error returns within the same session after re-authenticating, run `/logout` first to fully clear the stored token, then `/login`
* If you authenticate with the `CLAUDE_CODE_OAUTH_TOKEN` environment variable, Claude Code keeps sending the value you set after a request fails with a 401, rather than switching to a stored login's token. [`/status`](/docs/en/commands) shows this credential as an `Auth token` row reading `CLAUDE_CODE_OAUTH_TOKEN`. Generate a fresh token with [`claude setup-token`](/docs/en/authentication#generate-a-long-lived-token) and restart with it, or unset the variable and run `/login`. Before v2.1.225, Claude Code could replace the variable's value mid-session with the short-lived access token from a stored login, and the session failed with 401 errors again once that token expired.
* For repeated prompts to log in across launches, see the system clock checks and macOS credential-storage recovery steps in [Troubleshooting](/docs/en/troubleshoot-install#not-logged-in-or-token-expired)
* For other failures including `403 Forbidden` and OAuth browser issues, see [Login and authentication](/docs/en/troubleshoot-install#login-and-authentication)

### API Error: 401 Invalid authentication credentials

The API recognized the format of your credential but rejected the account or organization behind it. Anthropic returns this message when a credential was recently revoked, when an organization was disabled or removed your access, or when the account itself was deactivated, so an expired token isn't the cause. The credential can be your saved login or an approved `ANTHROPIC_API_KEY`, and the fix differs, so start by running `/status` to see which one is active.

```text theme={null}
Please run /login · API Error: 401 Invalid authentication credentials
```

**What to do:**

* If `/status` shows an `API key` row, an approved [`ANTHROPIC_API_KEY`](/docs/en/authentication#authentication-precedence) is the active credential and takes precedence over your login, so `/login` doesn't replace it. Rotate the key in the Claude Console, or fall back to your subscription by running `unset ANTHROPIC_API_KEY`, or in PowerShell `Remove-Item Env:ANTHROPIC_API_KEY`.
* If `/status` shows only your login, run `/login` once. If the credential was revoked, a fresh login replaces it.
* If the same message returns for the same login account, the account or organization is no longer active. Check the account and organization that `/status` reports, and ask your organization admin to restore access.
* If [`ANTHROPIC_BASE_URL`](/docs/en/env-vars) points at an [LLM gateway](/docs/en/llm-gateway), the text after `401` is your gateway's message rather than Anthropic's, and `/login` doesn't change it. Fix the credential your gateway expects instead.

### Login expired

Claude Code tried to renew your saved claude.ai or Claude Console login and the OAuth service rejected the stored refresh token, so Claude Code cleared the saved credentials. After that, each request stops locally before it reaches the API, because only `/login` can create new credentials. Before v2.1.206, Claude Code sent the request anyway with whatever credential remained in the environment, and every model then failed with [There's an issue with the selected model](#theres-an-issue-with-the-selected-model) or a 401 instead of a prompt to sign in.

```text theme={null}
Login expired · Please run /login
```

In [non-interactive mode](/docs/en/headless) (`-p`) and the [Agent SDK](/docs/en/agent-sdk/overview), the message reads as follows, and the structured error code is `authentication_failed`:

```text theme={null}
Failed to authenticate: OAuth session expired and could not be refreshed
```

This is not the same state as [OAuth token revoked or expired](#oauth-token-revoked-or-expired). Those messages report a 401 the API returned. Claude Code itself produces `Login expired` for a login it already failed to renew, so it sends no request.

Sessions authenticated with an API key, [`CLAUDE_CODE_OAUTH_TOKEN`](/docs/en/env-vars), or a third-party provider don't use the saved login and never see this message.

You can check for this state before a request fails: [`/status`](/docs/en/commands) shows a `Login` row reading `Expired — log in again`, plus the organization and email it has saved for the expired login. The row appears only when the saved login is your active credential and can no longer be refreshed. Sessions authenticated another way don't show the row, even if an expired login remains saved. Before v2.1.210, `/status` gave no indication in this state that a login had ever existed, because the cleared credential left it nothing to report.

**What to do:**

* Run `/login` to sign in again. Retrying without signing in shows the same message on every request.
* In non-interactive mode, run `claude` in the same environment, complete `/login`, then rerun your command. For automation that can't sign in interactively, authenticate with `ANTHROPIC_API_KEY` or [generate a long-lived token with `claude setup-token`](/docs/en/authentication#generate-a-long-lived-token).
* If signing in keeps failing, see [Login and authentication](/docs/en/troubleshoot-install#login-and-authentication)

### Anthropic profile login expired

Claude Code is authenticating through an Anthropic credential profile whose saved login credential has expired, and the profile holds no refresh credential Claude Code can use to renew it. Claude Code stops each request locally without retrying, because a retry would read the same expired credential.

```text theme={null}
Anthropic profile login expired · Re-authenticate your Anthropic profile
Anthropic profile login expired · Run /login to use your claude.ai account instead, or re-authenticate the profile
```

This appears only when the active credential comes from an Anthropic credential profile, one you select with the `ANTHROPIC_PROFILE` environment variable, that Claude Code discovers as the active profile in your Anthropic configuration directory, or that Claude Code wrote when you [signed in without an API key](/docs/en/authentication#sign-in-without-an-api-key). Sessions that authenticate with `/login`'s claude.ai option, an API key, a bearer token such as `ANTHROPIC_AUTH_TOKEN`, or a third-party provider never see this message.

On a machine that [offers the keyless sign-in](/docs/en/authentication#sign-in-without-an-api-key), run `/login`, choose the Anthropic Console account, and sign in again to renew a profile that the keyless Console sign-in or the Claude Platform CLI's `ant auth login` wrote. Claude Code replaces the expired credential in that profile. For a federation profile or one another tool created, `/login` doesn't renew the credential. Which form you see depends on whether you selected the profile or Claude Code discovered it:

* When you set `ANTHROPIC_PROFILE` explicitly, the message ends with `Re-authenticate your Anthropic profile`.
* When Claude Code discovered the profile from your configuration directory, the message offers `/login`, because Claude Code gives a working `/login` precedence over the discovered profile and then authenticates with your claude.ai or Console account instead. Before v2.1.234, Claude Code showed the `Re-authenticate your Anthropic profile` form in this case too.

**What to do:**

* Sign in to the profile again, then retry: on a machine that [offers the keyless sign-in](/docs/en/authentication#sign-in-without-an-api-key), run `/login` and choose the Anthropic Console account for a profile the keyless Console sign-in or the Claude Platform CLI's `ant auth login` wrote; for other profiles, use the tool that created them
* If an administrator provisioned the profile's credential, ask them to issue a new one
* Run `/status` to confirm the active credential source and profile name
* To stop using the profile, unset `ANTHROPIC_PROFILE` if you set it, then authenticate another way, such as `/login` or `ANTHROPIC_API_KEY`

### OAuth scope requirement

The stored token predates a permission scope that a newer feature needs. You see this most often from `/usage` and the status line usage indicator:

```text theme={null}
OAuth token does not meet scope requirement: user:profile
```

**What to do:**

* Run `/login` to get a new token with the current scopes. You don't need to log out first.

### claude.ai rejected the session token

A [claude.ai connector](/docs/en/mcp#use-mcp-servers-from-claude-ai) request failed because claude.ai rejected the token from your Claude Code login, usually a login that expired and couldn't be refreshed. The rejected token is your login, not the connector's own authorization in claude.ai, so authorizing the connector again doesn't resolve it. In `/mcp`, the connector shows as `connected · session token rejected` and its detail view reads:

```text theme={null}
claude.ai rejected the session token. Run /login, then reconnect.
```

**What to do:**

* Run `/login` to sign in again
* Reconnect the connector from `/mcp`, or run `/mcp reconnect <server>`. Reconnecting before you sign in again leaves the connector in the same state. The `/mcp` panel's **Reconnect** option reports `your claude.ai session token was rejected`; the typed `/mcp reconnect <server>` form reports a successful reconnect even though the token is still rejected.

Before v2.1.222, Claude Code marked the connector as needing authentication instead, which pointed you at the connector's authorization flow even though completing it didn't resolve the state.

### Issuer mismatch in authorization response

During an [MCP OAuth sign-in](/docs/en/mcp#authenticate-with-remote-mcp-servers), the authorization server redirected back to Claude Code with an `iss` parameter that doesn't name the issuer that Claude Code expected from the server's OAuth metadata. A wrong issuer at this step is how an authorization server mix-up attack looks, so Claude Code fails the sign-in instead of exchanging the authorization code. Claude Code shows the error in the `/mcp` server menu after the browser sign-in:

```text theme={null}
Issuer mismatch in authorization response (RFC 9207): expected "https://auth.example.com", received "https://other.example.com"
```

`expected` is the issuer from the server's OAuth metadata, and `received` is the `iss` value the redirect carried. A sign-in whose redirect carries no `iss` parameter passes the check, unless the server's metadata sets `authorization_response_iss_parameter_supported`, in which case Claude Code fails the sign-in.

**What to do:**

* Try the sign-in again from `/mcp`
* If the error repeats, report it to the server operator. The fix is server-side: the authorization server must return the same issuer in the `iss` parameter that it advertises in its metadata
* To connect while the server is being fixed, start Claude Code with [`MCP_SDK_GENERATION=v1`](/docs/en/env-vars), whose [runtime](/docs/en/mcp#mcp-client-runtimes) doesn't run this check. This removes a protection against mix-up attacks, so prefer the server-side fix

Before v2.1.232, Claude Code used the v2 runtime only in a gradual rollout or when you set `MCP_SDK_GENERATION=v2`.

### AWS credentials expired or invalid

This message requires Claude Code v2.1.198 or later and only appears when [`awsAuthRefresh`](/docs/en/amazon-bedrock#advanced-credential-configuration) is set in your settings file. Your AWS session token expired or was rejected, and the automatic refresh Claude Code already ran didn't produce a credential the API accepts. It appears on a 401 from [Claude Platform on AWS](/docs/en/claude-platform-on-aws) or the [Mantle endpoint](/docs/en/amazon-bedrock#use-the-mantle-endpoint), which is how those providers report an expired security token.

The action hint in the middle names the `awsAuthRefresh` command from your settings, so it varies. The stable part is the leading `AWS credentials expired or invalid`:

```text theme={null}
AWS credentials expired or invalid · run /login and select "Claude Platform on AWS · refresh credentials", or run `aws sso login --profile myprofile` in another terminal · API Error: 401 ...
```

Without `awsAuthRefresh` configured, the same 401 shows the generic `Please run /login` message instead, which can't refresh AWS credentials.

**What to do:**

* Run the `awsAuthRefresh` command named in the message, such as `aws sso login --profile myprofile`, in another terminal and complete the browser sign-in, then retry
* In an interactive session, run `/login`, choose **3rd-party platform**, then select **Claude Platform on AWS · refresh credentials** under **Using 3rd-party platforms** to run the same command without restarting Claude Code. See [Configure AWS credentials](/docs/en/claude-platform-on-aws#1-configure-aws-credentials)
* If the error repeats after the refresh command succeeds, confirm the identity is valid outside Claude Code with `aws sts get-caller-identity` in the same shell and profile

### AWS authentication failed

This message requires Claude Code v2.1.198 or later and only appears when [`awsAuthRefresh`](/docs/en/amazon-bedrock#advanced-credential-configuration) is set in your settings file. Your AWS provider returned a 403, or [Amazon Bedrock](/docs/en/amazon-bedrock) returned a 401.

Claude Code can't tell which cause you hit. Amazon Bedrock reports an expired security token as a 403, but a 403 is also how it reports an authorization denial, such as an `AccessDeniedException` from a missing IAM permission or a model that isn't enabled for your account.

A 401 from Amazon Bedrock also lands here rather than under [AWS credentials expired or invalid](#aws-credentials-expired-or-invalid), because Amazon Bedrock doesn't report an expired token as a 401. A 401 from that endpoint typically comes from something else in the request path, such as a corporate proxy.

A credential refresh fixes an expired token and can't fix the other causes, so the message offers both:

```text theme={null}
AWS authentication failed · run /login and select "Claude Platform on AWS · refresh credentials", or run `aws sso login --profile myprofile` in another terminal · if credentials are current, check AWS permissions and model access · API Error: 403 ...
```

The action hint in the middle names the `awsAuthRefresh` command from your settings, so it varies. The stable part is the leading `AWS authentication failed`.

**What to do:**

* Run the `awsAuthRefresh` command named in the message, or `aws sso login`, in case an expired credential is the cause
* If your credentials are current, confirm the IAM permissions in [IAM configuration](/docs/en/amazon-bedrock#iam-configuration) are attached to the identity you're using and that the selected model is enabled for your account and region
* Run `aws sts get-caller-identity` to confirm which identity your requests use; a stale `AWS_PROFILE` or default profile is a common cause of a permission mismatch

### AWS default-chain credential resolve timed out

The AWS default credential provider chain didn't produce credentials within 60 seconds, so Claude Code stopped the resolve and failed the request. The failure is local credential resolution: the request never reached [Amazon Bedrock](/docs/en/amazon-bedrock), [Claude Platform on AWS](/docs/en/claude-platform-on-aws), or the [Mantle endpoint](/docs/en/amazon-bedrock#use-the-mantle-endpoint). Claude Code clears its [credential cache](/docs/en/amazon-bedrock#credential-caching-and-resolution-timeout) and retries before this error surfaces, so by the time you see it the chain has stalled on repeated attempts.

```text theme={null}
API Error: AWS default-chain credential resolve timed out
```

Common causes are a `credential_process` command in your AWS profile that waits for input it can't receive, and a container or VM whose instance metadata service (IMDS) never answers the chain's probe. Before v2.1.207, a stalled chain left the request waiting indefinitely instead of failing with this message.

**What to do:**

* Run `aws sts get-caller-identity` in the same shell with the same `AWS_PROFILE`. If it also hangs, fix the profile; a `credential_process` command that prompts interactively is a common cause.
* Complete the sign-in step before starting Claude Code, for example `aws sso login --profile myprofile`, so the chain resolves from the local SSO cache instead of waiting on a browser flow
* If your chain runs an interactive sign-in that legitimately needs more than 60 seconds, such as SSO with MFA through a wrapper like `aws-vault`, raise the limit in milliseconds with [`CLAUDE_CODE_AWS_CHAIN_RESOLVE_TIMEOUT_MS`](/docs/en/env-vars)

## Network and connection errors

Most of these errors mean a network request from Claude Code failed to reach its destination, or something between Claude Code and the API altered the response on its way back; where an entry also has a local cause, such as a failed archive write, its body says so. They usually originate in your local network, proxy, or firewall, or in the cloud environment's network policy.

### Unable to connect to API

The TCP connection to the API failed or never completed. For the common connection error codes, the message names the kind of failure and keeps the code in parentheses:

```text theme={null}
Unable to connect to API. Check your internet connection
Connection refused — a firewall or proxy may be blocking it (ConnectionRefused)
Can't reach the API server — check your internet or DNS (ENOTFOUND)
No internet route — check your connection or VPN (EHOSTUNREACH)
Couldn't connect through your proxy (ERR_PROXY_TUNNEL)
Connection dropped (ECONNRESET)
fetch failed
Request timed out. Check your internet connection and proxy settings
```

A code Claude Code doesn't recognize appears as `Unable to connect to API` followed by the code in parentheses. Some of these messages can show more than one code: `Connection refused` can show `ConnectionRefused` or `ECONNREFUSED`, for example, and `Can't reach the API server` can show `ENOTFOUND` or `FailedToOpenSocket`.

Before v2.1.227, each of these coded messages read `Unable to connect to API` followed by the code, for example `Unable to connect to API (ECONNREFUSED)`.

Common causes include no internet access, a VPN that blocks `api.anthropic.com`, or a required corporate proxy that is not configured.

**What to do:**

* Confirm you can reach the API host from the same shell by running `curl -I https://api.anthropic.com`. On Windows PowerShell use `curl.exe -I https://api.anthropic.com` so the built-in `Invoke-WebRequest` alias is not used.
* If you are behind a corporate proxy, set `HTTPS_PROXY` before launching Claude Code and see [Network configuration](/docs/en/network-config)
* If you route through an LLM gateway or relay, set [`ANTHROPIC_BASE_URL`](/docs/en/env-vars) to its address. See [Connect Claude Code to an LLM gateway](/docs/en/llm-gateway-connect) for setup.
* Ensure your firewall allows the hosts listed in [Network access requirements](/docs/en/network-config#network-access-requirements)
* Intermittent failures are [retried automatically](#automatic-retries); persistent failures point to a local network issue

If `curl` succeeds but Claude Code still fails, the cause is usually something between the runtime and the network rather than the network itself:

* On Linux and WSL, check `/etc/resolv.conf` for an unreachable nameserver. WSL in particular can inherit a broken resolver from the host.
* On macOS, a VPN client that was disconnected or uninstalled can leave a tunnel interface or routing rule behind. Check `ifconfig` for stale `utun` interfaces and remove the VPN's network extension in System Settings.
* Docker Desktop and similar container runtimes can intercept outbound traffic. Quit them and retry to rule this out.

### Unable to connect to Anthropic services

During first-run setup, Claude Code checks that it can reach `api.anthropic.com` and `platform.claude.com` before showing the sign-in step. When either check fails, Claude Code prints the reason and exits.

```text theme={null}
Unable to connect to Anthropic services
Failed to connect to api.anthropic.com: ECONNREFUSED
Connection to api.anthropic.com timed out after 10 seconds
A proxy is configured via HTTPS_PROXY. Check that it allows connections to the host above.
```

Claude Code sends the check through the same [proxy configuration](/docs/en/network-config) as API requests and gives each probe 10 seconds. When the failed probe went through a proxy, the message names the environment variable that configured it, such as `HTTPS_PROXY`. Before v2.1.222, the check used a different proxy transport with no timeout: behind a proxy URL with the `https://` scheme, it could stall on `Checking connectivity...` indefinitely and then fail even though API requests through the same proxy succeed.

Claude Code skips this check when a [managed settings file, MDM policy, or policy helper](/docs/en/managed-settings) sets [`forceLoginMethod`](/docs/en/settings-reference#forceloginmethod) to `"gateway"`, or sets [`forceLoginGatewayUrl`](/docs/en/settings-reference#forcelogingatewayurl) without `forceLoginMethod`. With either configuration, Claude Code opens the sign-in step on the **Cloud gateway** screen rather than an Anthropic sign-in method. Claude Code also skips the check when a managed settings source on the machine exists but can't be read, since that source may hold the gateway configuration. Before v2.1.247, Claude Code ran the check under this configuration too, and exited with this error when Anthropic's endpoints were unreachable.

**What to do:**

* If the message names a proxy variable, check that its value points at the right proxy and ask your network team to allow HTTPS connections through it to the host in the message. See [Network configuration](/docs/en/network-config).
* Work through the checks in [Unable to connect to API](#unable-to-connect-to-api). The `curl` test and firewall guidance there apply to this check too.
* If your organization signs in through a [cloud gateway](/docs/en/claude-apps-gateway) and this error appears on first run, update to Claude Code v2.1.247 or later.
* If your network is open and the failure persists, Claude Code may not be [available in your country](https://www.anthropic.com/supported-countries)

### Socket is closed

`Socket is closed` means the connection carrying a streaming response was closed while the response was still arriving. The most common cause is a corporate proxy on Windows dropping an established tunnel mid-response.

Depending on how far the response had progressed, Claude Code retries the request, keeps what Claude produced, or ends the turn. See [Automatic retries](#automatic-retries).

Before v2.1.214, Claude Code didn't retry this failure, and the turn stopped with an error containing `Socket is closed`.

**What to do:**

* If you see this error, update to v2.1.214 or later with `claude update`, then send your message again
* If turns keep failing behind the same proxy after updating, work through [Unable to connect to API](#unable-to-connect-to-api) and check the proxy setup in [Network configuration](/docs/en/network-config)

### API returned an empty or malformed response

Claude Code shows this error when its non-streaming retry of a failed streaming request gets an HTTP success status but the body isn't a Claude API message: commonly an HTML error or sign-in page, an empty body, or JSON in another format. A proxy, gateway, or network sign-in page answering in the API's place is the usual source. Claude Code doesn't retry the request, and the turn ends with this error.

```text theme={null}
API returned an empty or malformed response (HTTP 200) — check for a proxy or gateway intercepting the request.
```

After that opening, the message reports what came back and which request failed:

* A `Response:` clause with the content type, the kind of body, such as `body is an HTML page` or `empty body`, its size in bytes, and whether the response carried an Anthropic request id. When the response names a recognizable server, such as `nginx` or `cloudflare`, or carries intermediary headers, such as `cf-ray` or `via`, the clause lists those too.
* A sentence naming the failed streaming request's id and the failure that triggered the retry. When a stream had opened before the failure, it also reports how many stream events arrived and, if any did, how long the stream had been silent when the attempt failed.

Before v2.1.234, the message ended after `intercepting the request`.

**What to do:**

* Read the `Response:` clause to see which system answered. An HTML body, no Anthropic request id, or a named server such as `nginx` or `cloudflare` means that something between Claude Code and the API replied in its place
* If you route through an [LLM gateway](/docs/en/llm-gateway-connect#troubleshoot-gateway-errors), test the route with a direct request and fix the hop that returns the non-API response
* On a network with a sign-in page, such as guest Wi-Fi, complete the sign-in in a browser, then retry
* If only the non-streaming route through your gateway is broken, set [`CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK=1`](/docs/en/env-vars#variables) so a request that fails mid-stream goes to the normal retry path instead of this fallback, except when the streaming endpoint itself returns `404`, where Claude Code still falls back

### Streaming response ended before any complete data was received

A streaming response from your model provider completed without delivering any usable data, so Claude Code re-sent the request without streaming to finish the turn. Claude Code shows the warning once per session, in interactive sessions only. Before v2.1.239, Claude Code silently retried without streaming.

```text theme={null}
Streaming response ended before any complete data was received. Retrying without streaming. If this keeps happening, check any proxy or gateway between Claude Code and your model provider.
```

Claude Code sends each affected request twice: the empty streaming attempt and the retry. The usual cause is a proxy or gateway that consumes or transforms the streaming response body on its way back.

**What to do:**

* Configure any proxy or gateway between Claude Code and your model provider to pass streaming response bodies and their headers through unmodified
* On [Amazon Bedrock](/docs/en/amazon-bedrock), see [Streaming errors behind a gateway or proxy](/docs/en/amazon-bedrock#streaming-errors-behind-a-gateway-or-proxy) for the header and body requirements

### Bedrock streaming response has an unexpected content-type

A gateway or proxy between Claude Code and [Amazon Bedrock](/docs/en/amazon-bedrock) is transforming the streaming response body or its `Content-Type` header. Amazon Bedrock streams responses as `application/vnd.amazon.eventstream`. Rather than decode a body it can't read, Claude Code rejects a successful streaming response that reports a different content-type. Claude Code doesn't retry the request.

```text theme={null}
Bedrock streaming response has content-type "text/event-stream"; expected "application/vnd.amazon.eventstream". A gateway or proxy between Claude Code and Bedrock is likely transforming the response body — Bedrock's binary event-stream format must be passed through unmodified. Set CLAUDE_CODE_DISABLE_BEDROCK_CONTENT_TYPE_GUARD=1 to suppress this check while the gateway is being fixed.
```

Before v2.1.208, the same misconfiguration surfaced as `API Error: Truncated event message received` after the whole response had been buffered.

**What to do:**

* Configure the gateway to pass the `InvokeModelWithResponseStream` response body and its `Content-Type` header through unmodified. An intermediary that re-emits the stream as server-sent events is a common cause.
* Setting [`CLAUDE_CODE_DISABLE_BEDROCK_CONTENT_TYPE_GUARD=1`](/docs/en/env-vars) hides this error, but Claude Code doesn't decode a binary body under a rewritten header, so those requests fall back to a slower non-streaming path. See [Streaming errors behind a gateway or proxy](/docs/en/amazon-bedrock#streaming-errors-behind-a-gateway-or-proxy).

### SSL certificate errors

A proxy or security appliance on your network is intercepting TLS traffic with its own certificate, and Claude Code does not trust it.

```text theme={null}
Unable to connect to API: SSL certificate verification failed. Check your proxy or corporate SSL certificates
Unable to connect to API: Self-signed certificate detected. Check your proxy or corporate SSL certificates
```

As of v2.1.199, a certificate validation failure isn't retried, so this error appears on the first attempt instead of after the full [retry budget](#automatic-retries). Earlier versions spent a few minutes retrying before showing it. Transient TLS conditions, such as a handshake timeout, still retry.

During `/login` and the startup connectivity check, the same failure is reported with the OpenSSL code and the fix inline:

```text theme={null}
SSL certificate error (UNABLE_TO_GET_ISSUER_CERT_LOCALLY). If you are behind a corporate proxy or TLS-intercepting firewall, set NODE_EXTRA_CA_CERTS to your CA bundle path, or ask IT to allowlist *.anthropic.com. Run `claude doctor` for details.
```

**What to do:**

* Export your organization's CA bundle and point Claude Code at it with `NODE_EXTRA_CA_CERTS=/path/to/ca-bundle.pem`
* See [Network configuration](/docs/en/network-config#custom-ca-certificates) for full setup instructions
* Don't set `NODE_TLS_REJECT_UNAUTHORIZED=0`, which disables certificate validation entirely

### Host not allowed in a cloud session

An outbound HTTP request from a cloud session or routine was blocked by the environment's network policy.

```text theme={null}
HTTP 403
x-deny-reason: host_not_allowed
```

You may also see a TLS certificate that doesn't match the destination's real certificate. Cloud sessions route outbound traffic through a proxy that enforces the network policy, so a mismatched certificate means the proxy terminated the connection, not the destination.

This is not a client-side network problem. Cloud sessions and [routines](/docs/en/routines) run inside a sandboxed VM whose outbound traffic through the session's network is filtered to the [cloud environment's](/docs/en/cloud-environments) allowlist; [GitHub operations](/docs/en/cloud-environments#github-proxy) and MCP connector traffic use separate channels, which is why they can keep working while other hosts are blocked. The **Default** environment uses **Trusted** access, which permits the [default allowlist](/docs/en/cloud-environments#default-allowed-domains) of package registries, cloud provider APIs, container registries, and common development domains and blocks other domains on that path.

**What to do:**

* Open the routine for editing, or start a cloud session. Select the cloud icon showing your environment's name, such as **Default**, to open the selector. Hover over your environment and click the settings icon.
* In the **Update cloud environment** dialog, change **Network access** from **Trusted** to **Custom**, then add the blocked domain to **Allowed domains**. Enter one domain per line. Check **Also include default list of common package managers** to keep the [default allowlist](/docs/en/cloud-environments#default-allowed-domains) alongside your custom domains. Select **Full** instead if you want unrestricted access.
* Click **Save changes**. The next run uses the updated allowlist.

See [Network access](/docs/en/cloud-environments#network-access) for access levels and the default allowlist. Local CLI sessions are not affected by this policy.

<h3 id="the-proxy-refused-the-connection">
  The proxy refused the connection
</h3>

You see this message when Claude reads an [artifact](/docs/en/artifacts) through the proxy you set in `HTTPS_PROXY` or a related [proxy variable](/docs/en/network-config#environment-variables). Artifact content comes from `*.frame.claudeusercontent.com`, so Claude Code first sends the proxy a `CONNECT` request asking it to open a tunnel to that host. When the proxy refuses, nothing reaches the host, and the message carries the proxy's HTTP status:

```text theme={null}
artifact content fetch failed (proxy refused the connection: HTTP 407)
artifact content fetch failed (proxy refused the connection: HTTP 403)
the proxy refused the connection to the artifact's content host (HTTP 502)
```

The status is the proxy's answer to the `CONNECT`. The host never answered, so each status points at a different fix:

* `HTTP 407`: the proxy requires credentials it didn't get. Put them in the proxy URL, as [Basic authentication](/docs/en/network-config#basic-authentication) shows.
* `HTTP 403`: the proxy refuses to tunnel to `*.frame.claudeusercontent.com`. Ask whoever runs the proxy to allow that host, which [Network access requirements](/docs/en/network-config#network-access-requirements) lists.
* Any other status, such as `HTTP 502`: the proxy didn't open the tunnel for its own reason, such as failing to reach the host. Look the status up in the proxy's logs.
* `unreadable reply` in place of a status: whatever is at the proxy address didn't answer with an HTTP status line. Check that the address is an HTTP proxy.

**What to do:**

* Check the address and credentials in the proxy variable, as [Proxy configuration](/docs/en/network-config#proxy-configuration) describes, then run `curl -x http://proxy.example.com:8080 -I https://api.anthropic.com` from the shell you start Claude Code in, using your own proxy URL. On Windows PowerShell, run `curl.exe`. If this probe fails the same way, fix the proxy setup first. If it succeeds, the refusal is specific to the artifact host.
* If your network lets Claude Code reach the artifact host directly, add `.frame.claudeusercontent.com` to [`NO_PROXY`](/docs/en/network-config#environment-variables). Keep the entry that narrow: a broader `.claudeusercontent.com` entry also bypasses the proxy for `bridge.claudeusercontent.com`, which organizations with [IP allowlisting](/docs/en/network-config#organization-ip-allowlists-and-proxy-egress) need to keep on the proxy.

Before v2.1.238, Claude Code reported a refused tunnel as a generic network error.

<h3 id="the-cloud-environments-service-returned-an-empty-or-unexpected-response">
  The cloud environments service returned an empty or unexpected response
</h3>

Claude Code requests your [cloud environments](/docs/en/cloud-environments) list at several points, such as when you create a cloud session from the CLI or run [`/remote-env`](/docs/en/cloud-environments#select-an-environment-from-the-cli). When it can't read the server's answer, it shows one of these messages:

```text theme={null}
The cloud environments service returned an empty response (HTTP 200 with no body). This is usually temporary — try again in a moment.
The cloud environments service returned a response in an unexpected format (HTTP 200 with a non-JSON body). This is usually temporary — try again in a moment.
The cloud environments service returned a response in an unexpected format (HTTP 200 without a usable environments list). This is usually temporary — try again in a moment.
```

The server accepted the request but answered with a body that isn't the environments list: empty, not JSON, or JSON without the list. This usually accompanies a service-side disruption and clears on its own. Depending on the surface that requested the list, Claude Code may add a prefix, such as `couldn't list environments:` in the `/remote-env` dialog.

**What to do:**

* Retry the action. Claude Code requests the list again each time
* If the message keeps appearing, check [status.claude.com](https://status.claude.com) for active incidents

Before v2.1.236, Claude Code showed a raw JavaScript TypeError instead of these messages.

<h3 id="couldnt-reconnect-to-your-remote-control-session">
  Couldn't reconnect to your Remote Control session
</h3>

```text theme={null}
Couldn't reconnect to your Remote Control session. Retry, or start a fresh session without --resume.
```

Resuming with `claude --resume` or `claude --continue` reconnects to the [Remote Control](/docs/en/remote-control) session recorded in that conversation. This message means the reconnection failed for a reason that may be temporary, such as a network interruption or a server error, so Claude Code can't confirm whether the remote session still exists. Your local session keeps running without Remote Control.

**What to do:**

* Run `/remote-control` to retry the connection
* Start a new session with `claude --remote-control` to create a new Remote Control session
* For other Remote Control startup messages, see [Troubleshoot Remote Control](/docs/en/remote-control#troubleshooting)

If the server reports instead that the previous session is gone, you don't see this message. Claude Code starts a new session in its place or shows [`Previous session is unavailable — run /remote-control to start a new one`](/docs/en/remote-control#previous-session-is-unavailable), depending on [the conversation's reconnection record](/docs/en/remote-control#resume-outcomes). From v2.1.227 through v2.1.231, Claude Code showed a message that starts with `Remote Control could not resume the previous session under the current login` instead, and [earlier versions behaved differently again](/docs/en/remote-control#reconnect-history).

<h3 id="sessions-ended-while-this-machine-was-offline">
  Sessions ended while this machine was offline
</h3>

Claude Code shows this message in the terminal running [`claude remote-control`](/docs/en/remote-control#start-a-remote-control-session) after your machine was offline long enough that the server cleaned up the Remote Control environment your machine was serving. The sessions in that environment ended, and you can't resume them. The count is the number of sessions that ended.

```text theme={null}
2 sessions ended while this machine was offline — the environment was cleaned up on the server and can't be resumed.
```

**What to do:**

* When Claude Code lists kept worktrees under this message, pick up any uncommitted work from them
* Run `claude remote-control` to start a fresh environment

<h3 id="couldnt-share-the-transcript">
  Couldn't share the transcript
</h3>

After you agree to share your session transcript from a survey prompt, such as the [session quality survey](/docs/en/data-usage#session-quality-surveys), Claude Code uploads it to Anthropic, or saves a local archive instead on third-party providers, on [Claude apps gateway](/docs/en/claude-apps-gateway) sessions, and when no Anthropic credentials are available. This message means the share didn't complete.

```text theme={null}
Couldn't share the transcript.
```

The upload must fit an 8 MiB limit. On a long session, Claude Code progressively drops parts of the share, the last request's model settings first, then the structured conversation and subagent transcripts, and shows this message only when no reduced version can be sent or a network or server error stops the upload. When Claude Code saves a local archive instead, the message means it couldn't write the archive.

**What to do:**

* Run `/feedback` to send the transcript with a description of what happened. See [Report an error](#report-an-error) if `/feedback` is unavailable in your environment
* If other requests are failing too, check your network connection and see [Unable to connect to API](#unable-to-connect-to-api)

## Request errors

These errors relate to the content of your request. Most come back from the API after it rejected the request; a few are produced locally by Claude Code before any request is sent.

### Prompt is too long

The conversation plus attached files exceeds the model's context window.

```text theme={null}
Prompt is too long
```

In an interactive session, Claude Code shows this error as:

```text theme={null}
Context limit reached · /compact or /clear to continue
```

The line names only `/clear` when [`DISABLE_COMPACT`](/docs/en/env-vars) is set. Longer forms of the error, such as the compaction-failed form below, keep the `Prompt is too long ·` wording. In `-p` output and the transcript, the text stays `Prompt is too long`.

When you turned auto-compact off in your [user settings](/docs/en/settings-reference#autocompactenabled), the line also says so:

```text theme={null}
Context limit reached · /compact or /clear to continue · auto-compact is off · /config to turn it on
```

The **Auto-compact** toggle in `/config` writes `autoCompactEnabled` to user settings. The hint appears only when a `/config` change would take effect. For example, it doesn't appear when [`DISABLE_AUTO_COMPACT`](/docs/en/env-vars) or [`DISABLE_COMPACT`](/docs/en/env-vars) turned auto-compact off. It also doesn't appear when a higher-precedence scope, such as project or managed settings, set `autoCompactEnabled` to `false`. Before v2.1.235, the line carried no auto-compact hint.

Amazon Bedrock reports this condition as `Input is too long for requested model.`, which Claude Code handles the same way. Before v2.1.217, Claude Code didn't recognize the Bedrock wording, so auto-compact never triggered on it and `/compact` failed with the same error.

A [Claude apps gateway](/docs/en/claude-apps-gateway-config#upstream-error-messages) reports this condition as `capability_rejected: prompt_too_long` when a cloud upstream rejects the request in the provider's own error shape. Claude Code treats the token the same as `Prompt is too long`. Before v2.1.228, Claude Code didn't recognize the token, so auto-compact didn't trigger on it.

When automatic compaction ran on this turn and failed on an underlying error, such as an unavailable model or an authentication failure, the message names that error after a separator:

```text theme={null}
Prompt is too long · automatic compaction failed: <the underlying error>
```

Resolve the named error first; `/compact` fails on the same error until you do. Before v2.1.229, a failed automatic compaction surfaced `Prompt is too long` without the cause.

A single-exchange conversation has no earlier turns to summarize. When automatic compaction would have run on one, Claude Code skips the attempt and explains what fills the request instead. When the API doesn't report token counts in its error, the message reads:

```text theme={null}
Prompt is too long · this conversation is a single exchange and cannot be compacted — the request size comes mostly from system prompt, tool definitions, or attachments.
```

When the API reports token counts in its error, Claude Code compares them with its own estimate of the conversation's size to tell which is most of the request: the conversation's own content, or the system prompt, tool definitions, and attachment content that Claude Code sends with it. When the conversation's own content is most of the request, the message reads:

```text theme={null}
Prompt is too long · the request is ~<request tokens> tokens (limit <limit>) and this conversation's own content is most of it. A single-exchange conversation cannot be compacted; start with less content (smaller files or pasted text).
```

When most of the request is outside the conversation, the message reads:

```text theme={null}
Prompt is too long · the request is ~<request tokens> tokens (limit <limit>) but this conversation is only ~<conversation tokens> tokens — the rest is system prompt, tool definitions, and attachment content. A single-exchange conversation cannot be compacted; reduce attached files/tools or start with less context.
```

Before v2.1.162, Claude Code attempted the compaction anyway and surfaced the bare `Prompt is too long` when it failed.

**What to do:**

* In a multi-turn conversation, run `/compact` to summarize earlier turns and free space, or `/clear` to start fresh. A single-exchange conversation can't be compacted, so shrink the request instead
* Run `/context` to see a breakdown of what is consuming the window: system prompt, tools, memory files, and messages
* Disable MCP servers you are not using with `/mcp disable <name>` to remove their tool definitions from context
* Trim large `CLAUDE.md` memory files, or move instructions into [path-scoped rules](/docs/en/memory#path-specific-rules) that load only when relevant
* Subagents inherit every MCP tool definition from the parent session, which can fill their context window before the first turn. Disable MCP servers you are not using before spawning subagents.
* Auto-compact is on by default and normally prevents this error. If you turned it off in `/config` or with [`DISABLE_AUTO_COMPACT`](/docs/en/env-vars), turn it back on. If you keep it off, run `/compact` yourself before the window fills.

See [Explore the context window](/docs/en/context-window) for an interactive view of how context fills up.

### Context exceeds the token limit

`/context` shows this warning at the top of its output when the conversation has grown past the model's context window. Requests fail with [`Prompt is too long`](#prompt-is-too-long) until you free space. An interactive session shows that error as the `Context limit reached` line.

```text theme={null}
Context exceeds the 200k-token limit by 94k tokens — run /compact or /clear to continue.
```

When the limit you exceeded is a compaction window smaller than the model's context window, such as the 200K boundary on 1M-context models, the warning reads differently. Requests still succeed past a compaction window; run the named command to bring usage back under it.

```text theme={null}
Context is 94k tokens past the 200k-token compaction window — run /compact to reduce usage.
```

Both forms name `/clear` instead of `/compact` when you have set [`DISABLE_COMPACT`](/docs/en/env-vars).

**What to do:**

* In a multi-turn conversation, run `/compact` to summarize earlier turns and free space. To start fresh instead, run `/clear`
* For more ways to reduce usage, see [Prompt is too long](#prompt-is-too-long)

Before v2.1.216, `/context` showed usage above 100% with no warning line explaining what that meant or how to recover.

### Error during compaction: Conversation too long

`/compact` itself failed because there is not enough free context to hold the summary it produces.

```text theme={null}
Error during compaction: Conversation too long. Press esc twice to go up a few messages and try again.
```

This can happen when the window is already full at the moment auto-compact triggers, or when you run `/compact` after seeing [`Prompt is too long`](#prompt-is-too-long). In an interactive session, that error is the `Context limit reached` line.

**What to do:**

* Press Esc twice to open the message list and step back several turns. This drops the most recent messages from context. Then run `/compact` again.
* If stepping back doesn't free enough space, run `/clear` to start a fresh session. Your previous conversation is preserved and can be reopened with `/resume`.

This message and other `/compact` failures display in error styling. Before v2.1.216, they rendered in the same dim style as successful command output, so you could read a failed compaction as a success.

### Request too large

The raw request body exceeded the API's 32MB limit before tokenization, usually because of large pasted content, tool results, or attachments. This limit is separate from the [context window](#prompt-is-too-long).

```text theme={null}
Request too large (max 32MB). Accumulated images and attachments in the conversation pushed the request over the limit. Run /compact, or double press esc to go back and remove attachments.
```

When the request went straight to the Claude API and the API itself rejected it, Claude Code measures the conversation and words the message by whether recovery can work. Through a proxy, gateway, or cloud provider you get the general message. The measured forms:

* `Request too large (max 32MB; 20.1MB of about 33.4MB is images or documents).`: images or documents pushed the request over the limit. Claude Code retries with them stripped.
* `Request too large for the API's 32MB request limit`: the messages alone are over the limit, so the message says `compacting cannot make it fit` and Claude Code doesn't retry. In [non-interactive mode](/docs/en/headless), the message tells you to reduce the input or start a new session instead.

Before v2.1.212, conversations with enough accumulated images failed on every turn with `Request too large (max 32MB). Double press esc to go back and try with a smaller file.` Before v2.1.229, Claude Code showed the attachment advice for every rejection, even when compacting couldn't help.

**What to do:**

* If the message says `compacting cannot make it fit`, press Esc twice to step back past the turn that added the large content, or run `/clear` to start fresh
* Otherwise, run `/compact`, which drops accumulated images and attachments
* Reference large files by path instead of pasting their contents, so Claude can read them in chunks
* For images, see [Image was too large](#image-was-too-large) below

### Image was too large

A pasted or attached image exceeds the API's size or dimension limits.

```text theme={null}
Image was too large. Double press esc to go back and try again with a smaller image.
API Error: 400 ... image dimensions exceed max allowed size
```

Claude Code replaces the unprocessable image with a text placeholder and retries, so subsequent messages succeed. On versions before 2.1.142, a pasted image could remain in the conversation and repeat the same error on every subsequent message. To recover on those versions, press Esc twice and step back past the turn where the image was added.

**What to do:**

* Resize the image before pasting. The API accepts images up to 8000 pixels on the longest edge for a single image, or 2000 pixels when many images are in context.
* Take a tighter screenshot of the relevant region instead of the full screen

### Unable to resize image

Claude Code couldn't downscale an attached image before sending it to the API.

```text theme={null}
Unable to resize image — image processing is unavailable and dimensions could not be read from the file header. Please convert the image to PNG, JPEG, GIF, or WebP.
Unable to resize image — dimensions exceed the 2000x2000px limit and image processing failed. Please resize the image to reduce its pixel dimensions.
Unable to resize image (… raw, … base64). The image exceeds the … API limit and compression failed. Please resize the image manually or use a smaller image.
Unable to resize image — could not verify image dimensions are within the 2000x2000px API limit.
```

Claude Code normally resizes large images automatically. These errors mean the native image processor failed to load or returned an error, so the image couldn't be resized to fit within API limits.

**What to do:**

* If the message asks you to convert the image, convert it to PNG, JPEG, GIF, or WebP and attach it again. Claude Code can verify dimensions for these formats without the image processor.
* If the message reports a dimension or size limit, resize or recompress the image below that limit before attaching.

### PDF errors

The PDF you attached couldn't be processed. The messages are shown here in their non-interactive form; in an interactive session they instead prompt you to double press esc and try again.

```text theme={null}
PDF too large (max 100 pages, 20MB). Try reading the file a different way (e.g., extract text with pdftotext).
PDF is password protected. Try using a CLI tool to extract or convert the PDF.
The PDF file was not valid. Try converting it to text first (e.g., pdftotext).
```

**What to do:**

* For oversized PDFs, ask Claude to read a page range with the Read tool instead of attaching the whole file, or extract text with a tool like `pdftotext` and reference the output file by path
* For protected or invalid PDFs, remove the password or re-export the file from its source application, then try again

### Extra inputs are not permitted

A proxy or LLM gateway between Claude Code and the API stripped the `anthropic-beta` request header, so the API rejected fields that depend on it.

```text theme={null}
API Error: 400 ... Extra inputs are not permitted ... context_management
API Error: 400 ... Unexpected value(s) for the `anthropic-beta` header
```

Claude Code sends beta-only fields such as `context_management` and `effort` alongside an `anthropic-beta` header that enables them. When a gateway forwards the body but drops the header, the API sees fields it doesn't recognize.

**What to do:**

* Configure your gateway to forward the `anthropic-beta` header. See [feature pass-through](/docs/en/llm-gateway-protocol#feature-pass-through) for what gateways must forward.
* As a fallback, set [`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`](/docs/en/env-vars) before launching. [Disable pre-release capabilities](/docs/en/llm-gateway-protocol#disable-pre-release-capabilities) covers the exact scope.

### Tool input schema is invalid

A tool in the request declared an `input_schema` that fails the API's JSON Schema validation, so the API rejected the whole request. The number after `tools.` is the failing tool's position in the request's tool list, not a name you can look up.

```text theme={null}
API Error: 400 ... tools.N.custom.input_schema: JSON schema is invalid
```

Claude Code [excludes MCP tools whose input schema would fail this validation](/docs/en/mcp#tools-with-invalid-input-schemas) when it loads a server's tools, so requests normally never include one.

On a [deployment where flag fetching is off](/docs/en/env-vars#features-that-need-feature-flag-fetching), or on a machine whose flags have never arrived, Claude Code records in the server's log which tool would be rejected but sends it anyway, so this error can still occur.

The error can also occur for a tool whose schema declares a JSON Schema dialect other than draft 2020-12 in `$schema`. Claude Code doesn't check those schemas against the JSON Schema meta-schema, though the top-level property-name check still applies.

Before v2.1.216, no deployment ran the exclusion checks.

**What to do:**

* If your Claude Code version is earlier than v2.1.216, run `claude update`.
* Remove or [disable](/docs/en/mcp#disable-a-server-without-removing-it) the MCP server that declares the invalid schema. The error names the tool only by position. On v2.1.216 or later, check each server's log for a line naming a tool whose input schema would be rejected. If no log names one, disable servers one at a time.
* If you maintain the server, fix the tool's `input_schema`. The schema must be valid JSON Schema, and top-level property names must be 1 to 64 characters long and use only ASCII letters and digits, `_`, `.`, and `-`. See [Tools with invalid input schemas](/docs/en/mcp#tools-with-invalid-input-schemas).

<h3 id="theres-an-issue-with-the-selected-model">
  There's an issue with the selected model
</h3>

The configured model name was not recognized or your account lacks access to it. As of v2.1.160 the trailing hint, shown here in its interactive form, varies by surface.

```text theme={null}
There's an issue with the selected model (claude-...). It may not exist or you may not have access to it. Run /model to pick a different model.
```

**What to do:**

* **Interactive CLI**: run `/model` to pick from models available to your account.
* **Non-interactive mode (`-p`)**: pass `--model` with a valid alias or ID, or set [`ANTHROPIC_MODEL`](/docs/en/env-vars). The error text shows `Run --model` on this surface.
* **Agent SDK**: the error text omits the hint because the model is set programmatically. Set [`model` on `Options`](/docs/en/agent-sdk/typescript#options) in TypeScript or [`ClaudeAgentOptions(model=...)`](/docs/en/agent-sdk/python#claudeagentoptions) in Python, and handle the structured `model_not_found` error to surface your own retry or model picker.
* Use an alias such as `sonnet` or `opus` instead of a full versioned ID. Aliases resolve to a maintained default so they don't go stale. See [Model configuration](/docs/en/model-config).
* If the wrong model keeps coming back in the CLI, a stale ID is set somewhere. Check the places you can set a model in [priority order](/docs/en/model-config#setting-your-model) and remove the stale value.
* A newly launched model can be available on the Anthropic API before Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry offers it. If you pinned a new model ID on one of those providers and see this error, check your provider's model catalog for availability in your region, and keep the previous version pinned until the new one appears there.
* Claude Code reports an expired claude.ai login as [Login expired](#login-expired), not as this error. Before v2.1.206, an expired login that could no longer be refreshed failed every model with this error; run `/login` if you see that on an older version.
* For Google Cloud's Agent Platform deployments, see [Google Cloud's Agent Platform troubleshooting](/docs/en/google-vertex-ai#troubleshooting).

### Model is not a recognized model id

The model string you passed to a model switch isn't a model alias, a model ID this Claude Code version knows, or an ID that starts with `claude-`. The usual causes are a typo in the ID, a display name such as `Sonnet 5` where the ID `claude-sonnet-5` is expected, or an alias that only newer Claude Code versions recognize. Claude Code rejects the switch immediately. Before v2.1.200, Claude Code saved the string and failed on the next request with [There's an issue with the selected model](#theres-an-issue-with-the-selected-model).

```text theme={null}
Model "claud-sonnet-5" is not a recognized model id. Did you mean 'claude-sonnet-5'?
```

The trailing hint names the closest matching alias or model ID. When nothing is close enough, it reads `Run /model to see available models.` instead.

Claude Code produces this error locally at the moment the switch is requested, before any API request is made. It applies when a model is set through the [Agent SDK](/docs/en/agent-sdk/typescript) `setModel()` method or by an app such as the [Desktop app](/docs/en/desktop) that runs the Claude Code CLI for you.

**What to do:**

* Run `/model` with no argument to open the picker and choose from the models available to your account, then pass the alias or ID shown there
* If you used an alias that a newer Claude Code version supports, run `claude update`. A full ID that starts with `claude-` passes this check even when the model is newer than your Claude Code version, so upgrading isn't needed for those.
* A model saved before v2.1.200 isn't repaired by this check. If a stale value keeps coming back, remove it from the locations listed under [Setting your model](/docs/en/model-config#setting-your-model).
* The check runs only on the Anthropic API. On any other provider or gateway, including a custom `ANTHROPIC_BASE_URL`, the provider defines the model names, so Claude Code accepts any string and passes it through. Claude Code can still write the [unrecognized-model diagnostic line](#unrecognized-model-id-on-a-request) at request time, on every provider.

### Claude Opus is not available with the Claude Pro plan

Your active subscription plan does not include the model you selected.

```text theme={null}
Claude Opus is not available with the Claude Pro plan. If you have updated your subscription plan recently, run /logout and /login for the plan to take effect.
```

**What to do:**

* Run `/model` and select a model your plan includes
* If you upgraded your plan recently and still see this, run `/logout` then `/login`. The stored token reflects your plan at the time you signed in, so upgrading on the web does not take effect in an existing session until you re-authenticate.
* See [claude.com/pricing](https://claude.com/pricing) for which models each plan includes

<h3 id="model-is-restricted-by-your-organizations-settings">
  Model is restricted by your organization's settings
</h3>

Your organization admin has disabled this model in the claude.ai admin console, or it is excluded by an [`availableModels`](/docs/en/model-config#restrict-model-selection) allowlist in managed settings. When the restricted model was set with `--model`, `ANTHROPIC_MODEL`, or the `model` setting, Claude Code substitutes an allowed model and continues. Typing `/model <name>` for a restricted model is rejected with `Run /model to choose a different model.` and the session keeps its current model.

```text theme={null}
Model "claude-opus-4-8" is restricted by your organization's settings. Using claude-sonnet-4-6 instead.
```

A notice prefixed with an agent, skill, or command name means the restriction applied to that [subagent's requested model](/docs/en/sub-agents#choose-a-model): the subagent runs on the substituted model and your session's model is unchanged. Before v2.1.223, Claude Code showed the notice only for subagents launched with the Agent tool.

Claude Code treats a model family alias, one of `opus`, `sonnet`, `haiku`, or `fable`, as a request for that family rather than for its newest version. On the Anthropic API and on [Claude Platform on AWS](/docs/en/claude-platform-on-aws), a restricted family alias resolves to the newest version of the family that your organization and the `availableModels` allowlist permit, and the substitution notice names that version. Claude Code rejects `/model <alias>` only when every version of the family is restricted. Before v2.1.205, a family alias was substituted or rejected based on its newest version alone, even when an older version of the same family was allowed.

**What to do:**

* Run `/model` to pick from the models your organization allows. Restricted models are hidden from the picker.
* If the restricted model was set in `--model`, `ANTHROPIC_MODEL`, the `model` field of a settings file, or the `model` frontmatter of a [subagent](/docs/en/sub-agents#choose-a-model), skill, or command, remove or update that value so the notice doesn't recur
* If you need access to the restricted model, ask your organization admin to enable it. See [Organization model restrictions](/docs/en/model-config#organization-model-restrictions).

### thinking.type.enabled is not supported for this model

Your Claude Code version is older than the minimum for the selected model. The CLI sent a thinking configuration the model no longer accepts.

```text theme={null}
API Error: 400 ... "thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

**What to do:**

* Run `claude update` and restart Claude Code. Opus 4.7 needs v2.1.111 or later. Opus 4.8 needs v2.1.154 or later. Sonnet 5 needs v2.1.197 or later. Opus 5 needs v2.1.219 or later
* If you can't upgrade, run `/model` and select Opus 4.6 or Sonnet 4.6 instead
* If you hit this in the [Agent SDK](/docs/en/agent-sdk/overview), upgrade the SDK package instead. Opus 4.8 needs TypeScript SDK v0.3.154 or later and Python SDK v0.2.88 or later. Sonnet 5 needs TypeScript SDK v0.3.197 or later. Opus 5 needs TypeScript SDK v0.3.219 or later

<h3 id="effort-isnt-available-with-thinking-turned-off">
  Effort isn't available with thinking turned off
</h3>

You turned [extended thinking](/docs/en/model-config#extended-thinking) off and ran at an [effort level](/docs/en/model-config#adjust-effort-level) above `high`. The model doesn't accept that combination, so the API rejected the request.

```text theme={null}
API Error: Effort 'xhigh' isn't available with thinking turned off on this model · run /effort high to continue, or turn thinking back on (unset MAX_THINKING_TOKENS=0)
```

**What to do:**

* [Lower the effort level](/docs/en/model-config#set-the-effort-level) to `high` or below.
* Turn thinking back on, for example by unsetting [`MAX_THINKING_TOKENS`](/docs/en/env-vars) or removing [`"alwaysThinkingEnabled": false`](/docs/en/settings-reference#alwaysthinkingenabled) from your settings.

Before v2.1.242, Claude Code showed the API's own message: `API Error: 400 output_config.effort 'xhigh' is not supported when thinking is disabled on this model. Use effort 'high' or below, or enable thinking.` Before v2.1.251, Claude Code sent the request at the effort level you set, so Opus 5 rejected every request above `high` with thinking turned off. Claude Code now sends effort `high` instead to models it knows reject the combination, such as Opus 5, so on v2.1.251 or later this error reaches you only from a model Claude Code doesn't know rejects it.

### Thinking budget exceeds output limit

The configured extended thinking budget exceeds the maximum response length, so there is no room left for the actual answer.

```text theme={null}
API Error: 400 ... max_tokens must be greater than thinking.budget_tokens
```

Claude Code adjusts these values automatically on the Anthropic API. You typically see this error on Amazon Bedrock or Google Cloud's Agent Platform when [`MAX_THINKING_TOKENS`](/docs/en/env-vars) is set higher than the provider's output limit, or when plan mode raises the thinking budget.

**What to do:**

* Lower `MAX_THINKING_TOKENS`, or raise [`CLAUDE_CODE_MAX_OUTPUT_TOKENS`](/docs/en/env-vars) above the thinking budget
* See [Extended thinking](/docs/en/model-config#extended-thinking) for how the budget interacts with output length

### Tool use or thinking block mismatch

The conversation history reached the API in an inconsistent state, usually after a tool call was interrupted or a turn was edited mid-stream.

```text theme={null}
API Error: 400 due to tool use concurrency issues. Run /rewind to recover the conversation.
API Error: 400 ... unexpected `tool_use_id` found in `tool_result` blocks
API Error: 400 ... thinking blocks ... cannot be modified
```

All three variants mean the same thing: the sequence of `tool_use`, `tool_result`, and `thinking` blocks in history no longer matches what the API expects.

**What to do:**

* If you are using Opus 4.7 or Opus 4.8, run `claude update` first. Versions before v2.1.156 can trigger this error during normal tool use, and `/rewind` doesn't clear it.
* Run `/rewind`, or press Esc twice, to step back to a checkpoint before the corrupted turn and continue from there. See [Checkpointing](/docs/en/checkpointing) for how checkpoints are created and restored.

### Unsupported tool content removed

When Claude Code connects directly to the Anthropic API and loads or previews a saved session, it removes tool content the Anthropic API doesn't accept and leaves this line where removed content sat between two thinking blocks:

```text theme={null}
[Unsupported tool content removed]
```

Such content reaches a session file when something other than the Anthropic API answered in the API's format, typically a third-party proxy set through [`ANTHROPIC_BASE_URL`](/docs/en/env-vars) that translates another provider's tool calls. Claude Code removes it only when the session connects directly to the Anthropic API, and loads the saved history as it is when the session runs through a proxy or on another provider. Before v2.1.246, Claude Code sent the tool use and its result back to the API, and every turn of the resumed session failed with a 400 error such as `messages.1.content.0.server_tool_use.name: Input should be 'web_search', 'web_fetch', ...`.

**What to do:**

* None needed when you see the placeholder line. The session continues without the removed content.
* If every turn of a resumed session fails with the 400 error instead, run `claude update` and resume the session again. Versions before v2.1.246 don't remove the content.

### Usage Policy refusal

The API declined to respond because content in the conversation triggered a [Usage Policy](https://www.anthropic.com/legal/aup) check. The message includes a Request ID you can quote to support if you believe the refusal is incorrect.

```text theme={null}
API Error: Opus 4.6 can't help with this. Start a new session to continue.

Send feedback with /feedback or learn more: https://www.anthropic.com/legal/aup
```

The message names the model that declined, or `Claude` when no model is recorded.

The check evaluates the full conversation, not only your latest prompt, so sending a new message in the same session usually re-triggers the same refusal. The same applies after exiting and reopening the session with `--continue` or `--resume`, since the transcript on disk still contains the triggering content. On [Amazon Bedrock](/docs/en/amazon-bedrock), [Google Cloud's Agent Platform](/docs/en/google-vertex-ai), and [Microsoft Foundry](/docs/en/microsoft-foundry), this message also covers requests the model's safety measures flagged as a cybersecurity topic. See [Safety measures flagged a cybersecurity topic](#safety-measures-flagged-a-cybersecurity-topic).

Before v2.1.219, the message read `Claude Code is unable to respond to this request, which appears to violate our Usage Policy (https://www.anthropic.com/legal/aup). Please double press esc to edit your last message or start a new session for Claude Code to assist with a different task.`

**What to do:**

* Press Esc twice or run `/rewind` to step back to a checkpoint before the turn that triggered the refusal, then rephrase or take a different approach. See [Checkpointing](/docs/en/checkpointing).
* If you can't identify which turn caused it, run `/clear` to start a fresh conversation in the same project. Your previous conversation is preserved on disk and remains available in `/resume`.
* In [non-interactive mode](/docs/en/headless) (`-p`), where rewind is unavailable, retry with a rephrased prompt in a new session without `--continue`. Policy checks vary by model, so switching to a different model with `--model` may also resolve the refusal in some cases.

### Safety measures flagged a cybersecurity topic

The model's safety measures flagged content in the conversation as a cybersecurity topic. The message names the model that flagged the request:

```text theme={null}
API Error: Opus 4.8's safeguards flagged this message. Our intentionally broad safeguards allow us to deliver more capabilities faster, but can sometimes flag legitimate cybersecurity work. Apply to the Cyber Verification Program to reduce these interruptions. Send feedback with /feedback or learn more: https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude
```

The message links to the [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude), which grants access for legitimate cybersecurity work.

On [Amazon Bedrock](/docs/en/amazon-bedrock), [Google Cloud's Agent Platform](/docs/en/google-vertex-ai), and [Microsoft Foundry](/docs/en/microsoft-foundry), a cybersecurity flag produces the [Usage Policy refusal](#usage-policy-refusal) message instead.

The safeguard itself is server-side and predates v2.1.203; client releases since then have changed only the message's wording.
From v2.1.203 through v2.1.218, the message read `<model> has safety measures that flagged this message for a cybersecurity topic. To learn about the Cyber Verification Program and apply for access, visit our help center:` followed by the same help-center link, and interactive sessions appended `If you were not engaging in a cybersecurity topic, please send feedback via /feedback.`
Before v2.1.203, it read `<model>'s safeguards flagged this message for a cybersecurity topic. If your work requires this access, you can apply for an exemption:` followed by an exemption form link.

**What to do:**

* If your work requires this content, apply for access through the [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude)
* If your request wasn't about a cybersecurity topic, run `/feedback` to report the false positive
* To keep working in the same session, press Esc twice or run `/rewind` to step back to a checkpoint before the turn that triggered the flag, then take a different approach. See [Checkpointing](/docs/en/checkpointing).

## Installation errors

These errors appear while installing or updating Claude Code, from the [install script](/docs/en/setup#install-claude-code), `claude install`, or `claude update`. For `command not found`, PATH, permission, and TLS problems during setup, see [Troubleshoot installation and login](/docs/en/troubleshoot-install).

### Installation was killed before it could finish

The install script reports when the `claude install` step is terminated by a signal. On Linux, exit code 137 means the process received SIGKILL, and on a low-memory host that's usually the kernel out-of-memory (OOM) killer. The script prints this explanation and exits with code 137:

```text theme={null}
Installation was killed before it could finish (exit code 137). This usually means the system ran out of memory.
Claude Code needs roughly 512MB of free memory to install. Free up memory, then run this script again.
```

For any other fatal signal, and for exit code 137 on macOS, the script prints `Installation was killed before it could finish (exit code <N>)` with the actual exit code and omits the out-of-memory explanation. The message comes from the install script macOS and Linux use, which also covers installs inside WSL; the native Windows install scripts never print it. Before v2.1.200, the script exited with only the shell's bare `Killed` line.

**What to do:**

* Stop other processes to free memory, then rerun the installer
* Add swap space or move to a larger instance. See [Install killed on low-memory Linux servers](/docs/en/troubleshoot-install#install-killed-on-low-memory-linux-servers) for the swap-file commands.

### The connection dropped while downloading the update

The connection to the download server closed while `claude install`, `claude update`, or the [automatic updater](/docs/en/setup#auto-updates) was fetching the Claude Code binary, and the retries didn't recover. Claude Code retries the download when the connection drops, the transfer stalls, or the downloaded file fails its checksum, up to three attempts in total. A completed HTTP error, such as a 404, isn't retried because the server already answered. Before v2.1.202, a single dropped connection failed the download immediately with the bare error `aborted` instead of retrying.

```text theme={null}
The connection dropped while downloading the update (attempt 3/3: aborted). Check your network — proxies sometimes cut off large downloads.
```

The text in parentheses names which attempt failed and the underlying network error. `claude update` precedes the message with `Error: Failed to install native update` on stderr.

A download that stays connected but doesn't finish within 10 minutes fails with `Download timed out: exceeded the total deadline` instead. Claude Code doesn't retry a timed-out download, because a connection too slow to finish inside the deadline won't finish on an immediate retry either. The steps below apply to both messages.

The usual cause is a proxy or gateway that closes a long transfer before it finishes. The Claude Code binary is a large download, so a proxy connection limit that never affects normal API traffic can still interrupt it.

**What to do:**

* Run `claude update` again. On an otherwise healthy network, the download usually succeeds on the next run. For the timed-out message, run it again from a faster or less throttled network.
* If your network requires a proxy, set `HTTPS_PROXY` before running the installer or `claude update`. See [Check network connectivity](/docs/en/troubleshoot-install#check-network-connectivity).
* If a corporate proxy keeps closing the transfer, ask your network team to allow the full download from `downloads.claude.ai`. See [Network access requirements](/docs/en/network-config#network-access-requirements).
* Run `claude doctor` from your shell for installation diagnostics

## Command-line errors

These errors come from the `claude` command line and its subcommands, from a command name you submit at the prompt, and from commands such as `/security-review` that gather context by running shell commands before their prompt runs. So do errors from `/tui`, which relaunches the CLI.

### Conflict between --bg and --print

This message requires Claude Code v2.1.198 or later. You combined `--bg` with `-p` or `--print` in the same `claude` invocation. `--bg` starts a [background session](/docs/en/agent-view#from-your-shell) that you later attach to with `claude agents`, while `--print` runs [non-interactively](/docs/en/headless) and never starts the interactive session that `claude agents` attaches to. Before v2.1.198 this combination silently created a background job that could never be attached to.

```text theme={null}
--bg and --print conflict: --print never starts the interactive session that `claude agents` attaches to, so the job would be unattachable. The prompt is the positional — drop --print: `claude --bg '<task>'`.
```

**What to do:**

* Drop `-p` or `--print`. `--bg` takes the prompt as its positional argument, so `claude --bg "<task>"` is the complete command. See [Dispatch new agents from your shell](/docs/en/agent-view#from-your-shell).
* To run the prompt non-interactively and print the result instead of creating a background session, drop `--bg` and run `claude -p "<task>"`

<h3 id="invalid-agents-configuration">
  Invalid --agents configuration
</h3>

The value you passed to `--agents` is invalid, so `claude` exits with code 1 instead of starting the session. When you pass `--safe-mode`, `--resume`, or `--continue`, or set [`CLAUDE_CODE_SAFE_MODE`](/docs/en/env-vars#variables), Claude Code doesn't check the value and starts the session. Before v2.1.242, Claude Code started the session anyway and left out the definitions it couldn't load.

```text theme={null}
Error: Invalid --agents configuration:
<what failed>
```

What follows the first line depends on how the value failed. Claude Code runs these checks in order and stops at the first one that fails. If your value has two kinds of problem, you see the second only after you fix the first:

1. When the value doesn't parse as JSON, Claude Code prints one `invalid JSON:` line carrying the JSON parser's own message
2. When it parses but an agent definition doesn't match the schema for [CLI-defined subagents](/docs/en/sub-agents#choose-the-subagent-scope), Claude Code prints one line per problem
3. When an agent name starts with `-`, Claude Code prints `<name>: agent names must not start with '-'`

When there are more than 20 problem lines, Claude Code prints the first 20 and replaces the rest with `…and N more`.

**What to do:**

* Fix each problem the message lists, then run the command again. See [the fields a CLI-defined subagent takes](/docs/en/sub-agents#choose-the-subagent-scope).

<h3 id="cloud-sessions-cannot-be-created-from-a-restricted-session">
  Cloud sessions cannot be created from a --restricted session
</h3>

When you start a session with [`--restricted`](/docs/en/cli-reference#cli-flags), Claude Code refuses to create [cloud sessions](/docs/en/claude-code-on-the-web#from-terminal-to-web) from it, because the new session would run outside the restricted process and wouldn't enforce restricted mode. Claude Code refuses on the client, before contacting the server, so no cloud session is created:

```text theme={null}
Cloud sessions cannot be created from a --restricted session: they would not enforce it.
```

**What to do:**

* Run the task locally in the restricted session
* If you control how the session was launched, start a new `claude` session without `--restricted` and create the cloud session from there

Before v2.1.248, Claude Code had no `--restricted` flag; earlier versions reject the flag itself with an unknown-option error.

### The --json-schema value is not a valid JSON Schema

The schema you passed to [`--json-schema`](/docs/en/cli-reference#cli-flags) in [non-interactive mode](/docs/en/headless#get-structured-output) failed JSON Schema compilation, so `claude` exits with code 1 instead of running the prompt. Before v2.1.205, an invalid schema produced unstructured output with no error, and any schema that used the `format` keyword was treated as invalid.

```text theme={null}
Error: --json-schema is not a valid JSON Schema: data/type must be equal to one of the allowed values
```

The text after the second colon is the validator's diagnostic and names the keyword or location that failed. Schemas that use the `format` keyword, such as `"format": "email"`, are valid: Claude Code accepts `format` as an annotation and doesn't enforce it.

Claude Code runs two checks before schema compilation: it rejects a value that isn't parseable JSON with `Error: --json-schema is not valid JSON`, and valid JSON that isn't an object with `Error: --json-schema must be a JSON object`.

**What to do:**

* Fix the part of the schema the diagnostic names, then rerun the command
* If the diagnostic is `schema too large`, reduce the schema's nesting and `$ref` reuse
* See [Get structured output](/docs/en/headless#get-structured-output) for a working schema and command

### Settings file exceeds the 2MiB limit

The file you passed to [`--settings`](/docs/en/cli-reference#cli-flags) is larger than 2 MiB, so `claude` exits with code 1 at startup instead of loading it. A settings file is a small JSON document, so a file this large usually means the path points at the wrong file. Before v2.1.214, Claude Code read the file with no size check, and a multi-gigabyte file or a device file such as `/dev/zero` grew memory without bound.

```text theme={null}
Error: Settings file exceeds the 2MiB limit: /path/to/settings.json
```

Claude Code rejects a `--settings` path that isn't a regular file the same way: a device, FIFO, or socket reports `Error: Cannot use settings file (Not a regular file (device, FIFO, or socket))` followed by the path, and a directory reports an `EISDIR` reason.

**What to do:**

* Point `--settings` at a regular JSON settings file under 2 MiB. See [Settings](/docs/en/settings) for the format.

### The current directory no longer exists

You started `claude` from a directory that was deleted or moved after your shell entered it, for example a worktree or temp directory another shell removed. Claude Code can't read its working directory, so it exits with code 1 before starting the session, in interactive and [non-interactive](/docs/en/headless) mode alike. Before v2.1.239, Claude Code crashed with minified bundle source and a raw `ENOENT ... uv_cwd` stack on stderr instead of this message.

```text theme={null}
The current directory no longer exists (it was deleted or moved). Start Claude Code from an existing directory.
```

When Claude Code can't read the working directory for a different reason, such as a permissions change, the message names the error code instead: `Can't read the current directory (EACCES). Start Claude Code from a different directory.`

**What to do:**

* Change to a directory that exists, such as your home or project directory, then run `claude` again
* If the directory was recreated at the same path, your shell still holds the deleted one. Run `cd "$PWD"` or leave and re-enter the directory, then run `claude` again

### Workspace not trusted when starting Remote Control

You started [Remote Control](/docs/en/remote-control) server mode with `claude remote-control` or its `claude rc` alias in a directory you haven't trusted. The command doesn't show the workspace trust dialog itself, so it exits with code 1 and names the fix:

```text theme={null}
Error: Workspace not trusted. Please run `claude` in /Users/you/project first to review and accept the workspace trust dialog.
```

In your home directory the message is different, because the workspace trust dialog never saves trust for the home directory, so accepting it there can't satisfy this check. Before v2.1.214, the home directory showed the message above, whose advice can't succeed there.

```text theme={null}
Error: Workspace not trusted. /Users/you is your home directory, and for security home-directory trust is never saved, so running `claude` here first won't help. Run `claude rc` from a project directory instead (run `claude` there once to accept the trust dialog).
```

**What to do:**

* Run `claude` in the directory, accept the [workspace trust dialog](/docs/en/permissions#project-allow-rules-and-workspace-trust), then run `claude remote-control` again
* In your home directory, change to a project directory and start Remote Control there

<h3 id="not-carried-over-to-the-sessions-remote-control-starts">
  Not carried over to the sessions Remote Control starts
</h3>

You started [Remote Control](/docs/en/remote-control) with a global `claude` flag before the `remote-control` verb, one that would restrict or configure the sessions Remote Control starts, such as `--settings`, `--setting-sources`, `--permission-mode`, `--disallowed-tools`, or `--mcp-config`. A flag placed before the verb never reaches those sessions. Claude Code refuses to start instead, naming the flag:

```text theme={null}
Error: `--settings` before `remote-control` is not carried over to the sessions Remote Control starts, so Remote Control refuses to start rather than drop it — remove it, and give Remote Control's own options after the verb (see `claude remote-control --help`).
```

Claude Code doesn't refuse global flags that are harmless to drop, such as `--verbose`, `--model`, or a wrapper-injected `--session-id` or `--plugin-dir`: it ignores them and Remote Control starts.

Claude Code also refuses to start for a global flag it doesn't yet recognize as harmless, so a flag added in a newer release can appear in this message until a later release marks it harmless.

**What to do:**

* Remove the flag from before the verb and pass [Remote Control's own options](/docs/en/remote-control#start-a-remote-control-session) after it; `claude remote-control --help` lists them
* When the refused flag is `--permission-mode`, run `claude remote-control --permission-mode <mode>` to set the permission mode for the sessions Remote Control starts

Before v2.1.248, `claude remote-control` didn't accept its own flags when a global flag came first, and the command failed with an `unknown option` error.

### claude import is not yet available in this build

You ran [`claude import`](/docs/en/cli-reference#cli-commands), and Claude Code found the import flow turned off, so the command exits with code 1 instead of starting the import. Before v2.1.222, a build with the import flow off treated `import` as a prompt and started an interactive session instead of printing this message.

```text theme={null}
`claude import` is not yet available in this build. Run `claude` and use /mcp or edit ~/.claude/settings.json directly.
```

Claude Code turns `claude import` on through a feature flag it fetches from Anthropic and caches on disk. This message means the cached value is off. The cause is usually one of the following:

* You haven't started a session since installing, so Claude Code hasn't fetched the flag yet. The first `claude import` can print this even when the feature is available to you.
* You use Claude Code through Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or Claude Platform on AWS. Claude Code doesn't fetch feature flags on these providers, so `claude import` stays unavailable.
* You set `DISABLE_TELEMETRY`, `DO_NOT_TRACK`, `DISABLE_GROWTHBOOK`, or [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`](/docs/en/env-vars), which turn off feature-flag fetching, so `claude import` stays unavailable.

**What to do:**

* On a fresh installation, start `claude`, wait for the session to load, exit, and run `claude import` again
* Where feature-flag fetching stays off, set the configuration up yourself: add MCP servers with [`claude mcp add`](/docs/en/mcp#installing-mcp-servers), and create the [`CLAUDE.md` files](/docs/en/memory#how-claude-md-files-load), [skills and commands](/docs/en/skills#where-skills-live), and [subagents](/docs/en/sub-agents#choose-the-subagent-scope) you want to carry over. The message also names `~/.claude/settings.json`. Of the configuration `claude import` carries, that file holds only the [permission mode](/docs/en/settings-reference#permission-settings); Claude Code doesn't read MCP servers from it.

### Could not read Claude Code config

You ran [`claude import`](/docs/en/cli-reference#cli-commands) while Claude Code couldn't parse `~/.claude.json`, the file where it stores your login and per-project state. The subcommand reads that file to check availability but doesn't show the recovery dialog the interactive session shows, so it exits with code 1. Before v2.1.222, `claude import` with an unreadable config file started an interactive session, whose recovery dialog handled the file.

```text theme={null}
Could not read Claude Code config — run `claude` with no arguments to recover it.
```

**What to do:**

* Run `claude` with no arguments. Claude Code detects the invalid file and offers to reset it. Then run `claude import` again.
* To keep manual edits you've made, fix the JSON syntax in `~/.claude.json` in an editor instead, then rerun `claude import`

### Could not import a server from Claude Desktop

Claude Code couldn't add one of the servers you selected in `claude mcp add-from-claude-desktop`. The command still imports the other selected servers and prints one line per server it couldn't add. Before v2.1.205, the first server that failed stopped the import and none of the selected servers were added.

```text theme={null}
Could not import my server: Invalid name my server. Names can only contain letters, numbers, hyphens, and underscores.
```

The text after the server name is the reason. The most common one is the name check: Claude Desktop allows characters in server names, such as spaces and periods, that `claude mcp` restricts to letters, numbers, hyphens, and underscores. Other reasons include a server configuration that fails validation and a server blocked by your organization's [MCP policy](/docs/en/managed-mcp).

**What to do:**

* Rename the server in `claude_desktop_config.json` to use only letters, numbers, hyphens, and underscores, then run `claude mcp add-from-claude-desktop` again
* Add that server directly with `claude mcp add` or `claude mcp add-json` under a valid name. See [Import MCP servers from Claude Desktop](/docs/en/mcp#import-mcp-servers-from-claude-desktop).

<h3 id="anthropic-hosted-and-doesnt-support-local-oauth">
  Server is Anthropic-hosted and doesn't support local OAuth
</h3>

You started a sign-in for an MCP server whose URL points at an Anthropic-hosted connector host that authenticates through a third-party identity provider. These hosts include `microsoft365.mcp.claude.com`, `gmail.mcp.claude.com`, and `gcal.mcp.claude.com`. Claude Code refuses to start its local OAuth flow for these hosts from both the `/mcp` panel and `claude mcp login`, because [their sign-in works only through claude.ai](/docs/en/mcp#use-mcp-servers-from-claude-ai).

```text theme={null}
"gmail" is Anthropic-hosted and doesn't support local OAuth. Connect it via Settings → Connectors on claude.ai (requires `claude login`), then it'll be available here automatically.
```

Claude Code matches these hosts by URL, so the message appears when a server you added with `claude mcp add` or in `.mcp.json` points at one of them.

**What to do:**

* Remove your entry with `claude mcp remove <name>`, so it can't hide the claude.ai connector at the same URL
* After removing it, connect the service at [claude.ai/customize/connectors](https://claude.ai/customize/connectors), while signed in to the account you use in Claude Code. Once connected, [the connector appears in Claude Code automatically](/docs/en/mcp#use-mcp-servers-from-claude-ai) if your active authentication method is a claude.ai subscription login

<h3 id="server-rejected-the-authorization-header-minted-by-the-configured-headershelper">
  Server rejected the Authorization header minted by the configured headersHelper
</h3>

An MCP server whose [`headersHelper`](/docs/en/mcp#use-dynamic-headers-for-custom-authentication) supplies the `Authorization` header answered the connection with HTTP 401 or 403, so Claude Code reports the connection as failed. Because the helper supplies the `Authorization` header, Claude Code [doesn't fall back to OAuth](/docs/en/mcp#authenticate-with-remote-mcp-servers) for the server:

```text theme={null}
Server rejected the Authorization header minted by the configured headersHelper (HTTP 401). Check that the helper command returns a valid credential for this MCP endpoint — OAuth fallback is disabled when the helper supplies Authorization.
```

Claude Code re-runs the helper on each connection attempt, so a retry after a transient rejection, such as a token-rotation race, can succeed with a fresh credential.

**What to do:**

* Run the `headersHelper` command yourself the way Claude Code runs it: from the [directory Claude Code runs it in](/docs/en/mcp#where-the-helper-runs), with the [environment variables Claude Code sets for it](/docs/en/mcp#use-dynamic-headers-for-custom-authentication), and without the [credential variables Claude Code removes](/docs/en/mcp#which-variables-a-helper-can-read) for a server from a project `.mcp.json`, a plugin, or a project agent file. Check that it prints an `Authorization` value the server's endpoint accepts
* After fixing the helper or its credential source, select the server in `/mcp` and choose **Reconnect**

Before v2.1.248, Claude Code ran OAuth discovery for a server whose helper supplied the `Authorization` header. That discovery could fail with `Incompatible auth server: does not support dynamic client registration` instead of reporting the rejected credential.

### MCP permission prompt tool not found

The tool you passed to [`--permission-prompt-tool`](/docs/en/cli-reference#cli-flags) wasn't among the connected MCP tools when the run first needed a permission decision, either because its server never connected or because no connected server exposes a tool by that name. Claude Code still sends your prompt: the [non-interactive](/docs/en/headless) run exits with this error, and exit code 1, on the first tool call that needs approval, so it produces no answer even though the request was made. Before the first prompt, Claude Code waits up to the per-server connection timeout of 30 seconds set by [`MCP_TIMEOUT`](/docs/en/env-vars) for that server to connect. Before v2.1.206, startup didn't wait for the server to finish connecting, so a slow-starting but healthy server produced this error too.

```text theme={null}
Error: MCP tool mcp__permissions__approve (passed via --permission-prompt-tool) not found. Available MCP tools: none
```

The list after `Available MCP tools:` names the MCP tools that were connected when the wait ended.

**What to do:**

* Check that the server starts and stays connected: run `claude mcp list` in the same directory and confirm the server is listed as connected
* Confirm the tool name matches the `mcp__<server>__<tool>` name the server exposes
* If the server needs longer than 30 seconds to start, raise [`MCP_TIMEOUT`](/docs/en/env-vars)

<h3 id="security-review-fails-without-origin-head">
  /security-review fails without origin/HEAD
</h3>

[`/security-review`](/docs/en/commands#all-commands) builds its review context by diffing your branch against `origin/HEAD`, the local ref that records which branch is the default on your `origin` remote. When that ref doesn't exist, the git commands that gather the diff fail and the review stops before it starts.

```text theme={null}
Error: Shell command failed for pattern "!`git diff --name-only origin/HEAD...`": [stderr]
fatal: ambiguous argument 'origin/HEAD...': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
```

The quoted command varies between runs: the review starts several `git` commands against `origin/HEAD` at once and reports whichever fails first, so you may see `git log` or a different `git diff` in its place. Git creates the ref only when the remote's default branch is both advertised by the remote and covered by your fetch refspec. A full `git clone` of a remote with commits meets both conditions. Single-branch and CI checkouts fetch too narrow a refspec, a server-side HEAD left pointing at a branch nobody pushed advertises no default, and a repository with no `origin` remote, or one you never fetched, provides neither.

Claude Code shows the same error for any skill that [injects dynamic context](/docs/en/skills#when-an-injected-command-fails). A failed injected command aborts that skill's invocation. Two sibling strings fire before the command runs at all:

* `Shell command permission check failed for pattern "..."`: the command's permission check returned something other than allow. Injected commands never prompt, so the invocation aborts without asking you. Pre-approve commands that no rule matches with [`allowed-tools`](/docs/en/skills#pre-approve-tools-for-a-skill). A matching ask or deny rule still aborts the invocation regardless of `allowed-tools`
* ``Skill <name> requires bash (`shell: bash` in frontmatter) but Git Bash was not found``: the skill's frontmatter demands bash on a machine without it. Install Git for Windows or change the frontmatter to `shell: powershell`. See [How injected commands run](/docs/en/skills#how-injected-commands-run)

**What to do:**

* Create the ref by naming your remote's default branch: `git remote set-head origin <default-branch>`. This works whenever the local tracking ref `origin/<default-branch>` exists. If it doesn't, as in single-branch clones, fetch the branch first: run `git remote set-branches --add origin <branch>`, then `git fetch origin`, then rerun the set-head command. Rerun `/security-review`.
* If you'd rather not name the branch, run `git fetch origin` and then `git remote set-head origin --auto`, which asks the remote which branch is its default. It fails with `error: Cannot determine remote HEAD` when the remote advertises no default branch, because it is empty or its HEAD points at a branch nobody pushed; name the branch explicitly instead. It fails with `error: Not a valid ref` when your clone doesn't fetch that branch; widen the refspec as above first.
* If the repository has no remote, add one with `git remote add origin <url>` and fetch before creating the ref. If the remote is empty, push your branch first with `git push -u origin HEAD` and name that branch in the set-head command; `origin/HEAD` then points at the branch you just pushed, so `/security-review` sees an empty diff until the branch diverges from it.

<h3 id="input-must-be-provided-when-using-print">
  Input must be provided when using --print
</h3>

Bare `claude` needs stdout to be a terminal to start the interactive UI. When stdout is redirected, or the console isn't a real terminal, such as PowerShell ISE and some IDE output panes, `claude` runs [non-interactively](/docs/en/headless) instead. That is the same mode as `claude -p`, which requires a prompt, so the message names `--print` even when you didn't pass the flag. Passing `-p`/`--print` with no prompt and nothing piped on stdin produces the same error anywhere.

```text theme={null}
Error: Input must be provided either through stdin or as a prompt argument when using --print
```

**What to do:**

* For interactive use, run `claude` in a real terminal: Windows Terminal or the PowerShell console rather than ISE, and your IDE's integrated terminal rather than an output pane
* For one-shot use, pass the prompt: `claude -p "your question"`, or pipe it with `echo "your question" | claude -p`

### Input contained only whitespace

In [non-interactive mode](/docs/en/headless), Claude Code refuses a prompt made up entirely of spaces, tabs, or newlines instead of sending it, because the API rejects messages with no visible text. Which message you see depends on where the blank prompt came from:

* **Prompt argument or piped stdin for `claude -p`**: `claude` exits with `Error: Input contained only whitespace. Provide a prompt with text through stdin or as a prompt argument when using --print`
* **Message submitted to a running `--input-format stream-json` or [Agent SDK](/docs/en/agent-sdk/overview) session**: Claude Code ends the turn without calling the model and the session stays usable. The refusal arrives as an informational message and as the turn's result text: `Blank prompt — the message was only whitespace, so nothing was sent to the model.`

Before v2.1.229, Claude Code sent the whitespace-only message to the API, which rejected the request with a 400 error.

**What to do:**

* Include visible text in the prompt. If a script builds the prompt from a variable or file, check that the source isn't empty before calling Claude Code.

### Unknown command

You submitted a `/` name that doesn't match any command in this session, so Claude Code reports the name instead of running anything:

```text theme={null}
Unknown command: /hepl. Did you mean /help?
```

Claude Code suggests the closest command name or alias that the menu lists in this session. When nothing is close, the message ends after the name. The cause is usually one of the following:

* A typo, such as `/hepl` for `/help`. [How the command menu matches what you type](/docs/en/commands#how-the-command-menu-matches-what-you-type) covers picking a close match before you submit
* A command that exists but isn't available in this session because a requirement isn't met, such as your platform, plan, or authentication method. The troubleshooting entries for [`/web-setup`](/docs/en/web-quickstart#web-setup-shows-no-commands-match-or-unknown-command) and [`/schedule`](/docs/en/routines#schedule-returns-unknown-command) walk through two common cases. Some commands answer with their own message when your organization's policy disables them
* A command from a [plugin](/docs/en/plugins) or [MCP server](/docs/en/mcp#use-mcp-prompts-as-commands) that isn't installed or connected in this session

Claude Code doesn't treat every prompt that starts with `/` as a command. It sends the prompt to Claude as a normal message when the first word after the `/` starts with punctuation, such as the `/--` that opens a Lean doc comment, or is a path such as `/var/log/syslog`.

Before v2.1.236, if you pressed `Enter` while the command menu listed a near match for the name you typed, Claude Code ran that match, so a typo such as `/hepl` ran `/help` instead of producing this message.

**What to do:**

* Run the suggested name, or type `/` followed by part of the name to see what's available in this session
* If Claude Code reports a documented command as unknown, check its row in the [commands reference](/docs/en/commands) for the requirement it names

### Diff is too large for ultrareview

The diff between your branch and the base branch, including uncommitted and staged changes, exceeds the size limits for an [ultrareview](/docs/en/ultrareview), so `/code-review ultra` and the `claude ultrareview` subcommand refuse the review before the cloud session starts. A refused review doesn't use a free run and doesn't bill usage credits. The message names the limits in effect, the size of your diff, and the files that contribute the most changed lines. Before v2.1.216, the message showed only the raw diff statistics.

```text theme={null}
Diff is too large for ultrareview: 812 files, 96,410 lines changed (limits: 500 files, 8,000 lines). Largest files: package-lock.json (41,904 lines), dist/bundle.js (18,210 lines), src/generated/api.ts (9,876 lines). Pass a closer base branch (`/code-review ultra <branch>`) to narrow the scope, or split the change.
```

Reviewing a pull request applies the same limits; that form of the message begins `PR #<N> is too large for ultrareview` and names the PR's file and line counts.

**What to do:**

* Pass a base branch closer to your work, such as `/code-review ultra develop`, so the review covers only the diff against that branch
* Split the change into smaller branches and review each one. The files the message names contribute the most changed lines, so start by moving those to their own branch.

### Could not find merge-base with the base branch

`/code-review ultra` and the `claude ultrareview` subcommand review the diff between your branch and a base branch, which needs a commit the two share. When `git merge-base` finds none, Claude Code refuses the review before the cloud session starts. On a clone Claude Code can verify is complete, with at least one branch, it falls back to [reviewing every tracked file](/docs/en/ultrareview#diff-limits-and-fallbacks) instead of refusing. You see this refusal when the base branch can't be found at all, when Claude Code can't verify that your clone is complete, or in the rare repository where the whole-tree diff isn't possible, such as the SHA-256 object format.

```text theme={null}
Could not find merge-base with main. Pass the base branch explicitly (e.g. `/code-review ultra develop`) or make sure you're in a git repo with a main branch.
```

The hint after the first sentence depends on what Claude Code observed:

* **You didn't pass a base branch**: Claude Code compared against the repository's default branch and suggests passing your base explicitly, as in the example above
* **You passed a base branch that was already in your clone**: the hint reads ``Make sure <branch> exists locally or on origin (try `git fetch origin <branch>`)``
* **You passed a base branch that wasn't in your clone**: Claude Code fetched it from origin before comparing. The hint reads ``<branch> was fetched from origin but shares no history with HEAD. If another branch is your real base, pass it explicitly (`/code-review ultra <branch>`)``; when Claude Code can't tell whether your clone is shallow, it suggests `git fetch --unshallow origin` instead. Before v2.1.221, the hint suggested `git fetch --unshallow origin` for every fetched base branch, and on a complete clone that command fails with `fatal: --unshallow on a complete repository does not make sense`.

**What to do:**

* If another branch is your real base, pass it explicitly: `/code-review ultra <branch>`
* If your clone might not have full history, run `git fetch --unshallow origin` and rerun the review

### Your checkout has no branches

A checkout can have commits but no branches: if you run `git init` followed by `git fetch <url>` and `git checkout FETCH_HEAD`, you get a detached HEAD with no refs. Claude Code packages your repository as a git bundle to upload it for an [ultrareview](/docs/en/ultrareview), and it can't bundle a repository that has no branches or other refs, so `/code-review ultra` and the `claude ultrareview` subcommand refuse the review before the cloud session starts.

```text theme={null}
Your checkout has no branches (detached HEAD only), which cloud review can't bundle. Create one first — `git checkout -b <name>` — then rerun /code-review ultra.
```

Before v2.1.221, Claude Code attempted to review every tracked file in this checkout, and the upload failed.

**What to do:**

* Create a branch at your current commit with `git checkout -b <name>`, then rerun the review

<h3 id="no-github-account-is-connected-to-your-claude-account">
  No GitHub account is connected to your Claude account
</h3>

You ran `/code-review ultra <PR#>` or `claude ultrareview <PR#>`, and before creating the cloud session Claude Code asks the server whether [the GitHub account connected to your Claude account](/docs/en/ultrareview#review-a-pull-request) can reach the PR's repository. No account is connected, or the connection expired, so the cloud clone would fail and Claude Code refuses the launch. Claude Code doesn't spend a free run or bill usage credits for a refused launch.

```text theme={null}
Ultrareview clones <owner>/<repo> in the cloud with the GitHub account connected to your Claude account, and none is connected (or the connection expired). To fix: run /web-setup to reuse your GitHub CLI login, or connect an account at https://claude.ai/code/onboarding?step=alt-auth — then re-run /code-review ultra 1234 (allow a minute after connecting).
```

When [`/web-setup`](/docs/en/web-quickstart#connect-from-your-terminal) isn't available in your session, the message names only the claude.ai link.

**What to do:**

* Run `/web-setup` to connect your GitHub CLI login to your Claude account, or connect an account at [claude.ai/code/onboarding](https://claude.ai/code/onboarding?step=alt-auth)
* Rerun the review a minute after connecting

Before v2.1.248, Claude Code didn't check this before launch.

<h3 id="your-connected-github-account-cant-see-the-repository">
  Your connected GitHub account can't see the repository
</h3>

You ran `/code-review ultra <PR#>` or `claude ultrareview <PR#>`, and [the GitHub account connected to your Claude account](/docs/en/ultrareview#review-a-pull-request) can't read the PR's repository, so the cloud clone would fail and Claude Code refuses the launch. Claude Code doesn't spend a free run or bill usage credits for a refused launch.

```text theme={null}
Your connected GitHub account can't see <owner>/<repo> — usually the Claude GitHub app isn't installed on <owner> or wasn't granted this repo (web-connected accounts need it for private repos), or a different GitHub account is connected. To fix: run /web-setup to reuse your GitHub CLI login, or install the app at https://github.com/apps/claude/installations/new — then re-run /code-review ultra 1234.
```

When [`/web-setup`](/docs/en/web-quickstart#connect-from-your-terminal) isn't available in your session, the message names only the app install.

**What to do:**

* If your local `gh` CLI can read the repository, run `/web-setup` to connect that login to your Claude account
* Rerun the review after the change

Before v2.1.248, Claude Code didn't check this before launch.

<h3 id="the-github-app-preflight-failed-transiently">
  The GitHub App preflight failed transiently
</h3>

You started a [cloud session](/docs/en/claude-code-on-the-web) from a local repository, and two steps failed together. Claude Code couldn't build or upload the bundle of your repository. Before the upload, it checked whether the cloud service can clone the repository from GitHub, and rather than a definite answer, that check ended in an error that a retry could clear, such as a network error, a timeout, or a temporary server error. The full message starts with what stopped the bundle, for example `Could not upload repo bundle (<error>)`, and ends with the preflight sentence:

```text theme={null}
Could not upload repo bundle (<error>). The GitHub App preflight failed transiently (network or service hiccup) — retry in a moment to start from GitHub instead
```

**What to do:**

* Rerun the command after a moment. When the GitHub check passes, Claude Code can start the session from a GitHub clone, so the failed upload no longer blocks the launch
* If retries keep failing, the start of the message names what stopped the upload. When that cause is something you can fix, fix it so the session can start from your local repository instead

Before v2.1.251, Claude Code ended the message with `Please set up GitHub on https://claude.ai/code` even when the GitHub check failed only transiently, and setup advice can't clear a transient failure.

### Failed to resume the conversation

Claude Code couldn't read or process the saved transcript for the session you selected from the [`claude --resume` picker](/docs/en/sessions#use-the-session-picker), so it ends the process rather than continue in a partially loaded state. The message includes the command to retry:

```text theme={null}
Failed to resume the conversation.
Run claude --resume <session-id> to retry, or claude to start a new session.
```

Claude Code exits with code 1 after showing the message. The `/resume` picker inside a running session reports `Failed to resume conversation` in the conversation instead, and your current session keeps running. Before v2.1.216, a failed resume from the `claude --resume` picker stayed on the `Resuming conversation…` spinner indefinitely instead of showing this message.

**What to do:**

* Run `claude --resume <session-id>` with the session ID from the message to retry
* If the retry fails again, run `claude` to start a new session

### No conversation found with the session ID

You passed a session ID to `claude --resume <session-id>` and no saved transcript matched it:

```text theme={null}
No conversation found with session ID: <session-id>
```

Claude Code exits with code 1 after showing the message. Claude Code [searches the current project first, then every other project on this machine](/docs/en/sessions#resume-a-session) for the ID. Before v2.1.223, the lookup stopped at the current project directory and its git worktrees, so resume from the directory the session last worked in.

Common causes:

* **Mistyped ID**: for a non-interactive run, the ID is the `session_id` field of the [`--output-format json` output](/docs/en/headless#get-structured-output)
* **Deleted transcript**: Claude Code removes transcripts after the [retention period](/docs/en/sessions#where-transcripts-are-stored), 30 days by default, following the [retention sweep rules](/docs/en/claude-directory#cleaned-up-automatically)
* **Different machine**: Claude Code stores transcripts locally, so resume the session on the machine where it ran
* **Duplicate copies**: if you copied a project directory under `~/.claude/projects` so two transcripts carry the same ID, Claude Code reports this message rather than resume one copy arbitrarily

**What to do:**

* For an interactive session, open the [session picker](/docs/en/sessions#use-the-session-picker) with `claude --resume` and press `Ctrl+A` to widen it to every project on this machine, then select the session
* Sessions created with `claude -p` or the [Agent SDK](/docs/en/agent-sdk/overview) don't appear in the picker, so re-check the ID against the `session_id` your original run printed

### Cannot switch renderers in this session

When you switch renderers, Claude Code restarts its process. You ran [`/tui`](/docs/en/fullscreen#enable-fullscreen-rendering) in a session Claude Code declines to restart, so it doesn't switch and saves nothing. Which message you see tells you the cause:

* `Cannot switch renderers while work is running in the background`: you have background work running that a restart would abandon, such as a background shell or a subagent. Wait for the work to finish or stop it with [`/tasks`](/docs/en/commands), then run `/tui fullscreen` or `/tui default` again
* `Cannot switch renderers in this session`: the session has restrictions Claude Code can't pass to the restarted process. Before v2.1.234, Claude Code restarted anyway and the relaunched session ran without them

In the restrictions message, the part in parentheses names the restrictions Claude Code found:

```text theme={null}
Cannot switch renderers in this session — it has restrictions a restart can't carry over (permission rules set for this session only). Nothing was changed. Running /tui fullscreen in a session started without them switches every later session too.
```

Each reason the message can show in parentheses:

* `launch flags: a custom system prompt, a tool allowlist, or restricted settings`: you started the session with a flag Claude Code doesn't pass back to the restarted process. These flags include [`--system-prompt`](/docs/en/cli-reference#cli-flags), `--system-prompt-file`, `--append-system-prompt-file`, a [`--tools`](/docs/en/cli-reference#cli-flags) allowlist, [`--setting-sources`](/docs/en/cli-reference#cli-flags), and [`--permission-prompt-tool`](/docs/en/cli-reference#cli-flags)
* `permission rules set for this session only`: a [permission update](/docs/en/hooks#permission-update-entries) from a hook or SDK caller added deny or ask rules with the `session` destination. Session-scoped allow rules don't trigger the refusal. A restart drops them, and Claude Code prompts again instead
* `ask-before-running rules with no command-line form`: a permission update from a hook or SDK caller added ask rules alongside the rules Claude Code passes back as `--allowed-tools` and `--disallowed-tools`. No flag exists for ask rules
* `permission rules a command line cannot carry intact` and `added directories a command line cannot carry intact`: a permission update added a rule or directory path mid-session. The restarted process's command line can't carry its text as the same value

**What to do:**

* In a session started without those restrictions, run `/tui fullscreen`, or `/tui default` to switch back. Claude Code saves the [`tui` setting](/docs/en/settings-reference#tui) there

<h3 id="terminal-setup-left-your-zed-keymap-unchanged">
  /terminal-setup left your Zed keymap unchanged
</h3>

You ran [`/terminal-setup`](/docs/en/terminal-config#enter-multiline-prompts) in Zed, and Claude Code couldn't complete the update to your Zed `keymap.json`, so it left the file as it was.

Each message names the path to your keymap and ends with the keybinding block to add yourself:

```text theme={null}
Couldn't update your Zed keymap, so it was left unchanged.
To add the binding yourself, add this block to the keymap array in <path to keymap.json>:
{ "context": "Terminal", "bindings": { "shift-enter": ["terminal::SendText", "\u001b\r"] } }
```

The first line of the message names the cause:

* `Couldn't read your Zed keymap, so it was left unchanged.`: Claude Code couldn't read the file, for example because of file permissions
* `Your Zed keymap isn't a readable list of keybindings, so it was left unchanged.`: the file read fine but doesn't parse as an array of keybinding blocks, even with `//` comments and trailing commas allowed
* `Couldn't back up your Zed keymap; not modifying it.`: Claude Code couldn't copy the file to a `.bak` backup beside it, so it changed nothing
* `Couldn't update your Zed keymap, so it was left unchanged.`: the merged result didn't verify as a valid keymap carrying the binding, so Claude Code discarded it instead of writing. A keybinding block with a duplicated key can cause this

**What to do:**

* Copy the block from the message into the top-level array in your `keymap.json` at the path the message names
* For `isn't a readable list of keybindings`, fix the syntax error, or make the file's top-level value an array, then run `/terminal-setup` again

Before v2.1.247, `/terminal-setup` couldn't parse a Zed keymap that used `//` comments or trailing commas, and it replaced the entire file with only its own binding while reporting the binding as installed. To restore a keymap an earlier version replaced, use the `.bak` backup file described under [Enter multiline prompts](/docs/en/terminal-config#enter-multiline-prompts).

## Plugin errors

These errors come from [plugin](/docs/en/plugins) and [marketplace](/docs/en/plugin-marketplaces) configuration. For plugin problems that don't produce one of the messages on this page, such as a marketplace URL that doesn't load or a plugin that installs but doesn't appear, see [Plugin troubleshooting](/docs/en/discover-plugins#troubleshooting).

### Marketplace is registered from an untrusted source

The marketplace is registered under a name that is [reserved for official Anthropic marketplaces](/docs/en/plugin-marketplaces#marketplace-schema), but its registered source isn't an `anthropics` GitHub repository. Claude Code re-checks reserved names every time it loads or refreshes a marketplace, so the marketplace and the plugins installed from it stop loading. Before v2.1.205, the name was checked only when the marketplace was added, so an entry registered before its name became reserved kept loading.

```text theme={null}
Marketplace "claude-community" is registered from an untrusted source: The name 'claude-community' is reserved for official Anthropic marketplaces. Only repositories from 'github.com/anthropics/' can use this name. To fix it, remove the marketplace and re-add it from the official source.
```

**What to do:**

* Run `claude plugin marketplace remove <name>`, then add the marketplace again from the official `github.com/anthropics` repository
* If you publish a third-party marketplace that used the name before it became reserved, rename it and ask users to re-add it from your source
* See the reserved name list under [Marketplace schema](/docs/en/plugin-marketplaces#marketplace-schema)

<h3 id="plugin-command-references-user-config">
  Plugin command references user\_config in a shell command
</h3>

A plugin hook, [monitor](/docs/en/plugins-reference#monitors), or MCP [`headersHelper`](/docs/en/mcp#use-dynamic-headers-for-custom-authentication) command references a `${user_config.KEY}` [plugin option](/docs/en/plugins-reference#user-configuration), and the substituted string would be passed to a shell. A configured value containing `$(...)`, backticks, or `;` would run as code there, so Claude Code refuses to start the component instead of substituting the value. The check runs on the command template, so the error appears even when no value is configured yet. Before v2.1.207, the value was substituted into the shell command.

The wording depends on which surface referenced the option. A shell-form hook reports:

```text theme={null}
Hook from plugin formatter@acme-tools references ${user_config.*} in a shell-form command. The substituted value would be re-parsed by the shell. Use exec form instead — {"command": "<executable>", "args": ["${user_config.KEY}", ...]} — or read $CLAUDE_PLUGIN_OPTION_<KEY> from the hook's environment. Command: ./scripts/notify.sh ${user_config.webhook_url}
```

A monitor reports:

```text theme={null}
Monitor "deploy-status" from plugin deploy-tools references ${user_config.*} in its command. The substituted value would be passed to a shell. Monitor commands cannot safely reference ${user_config.*}; have the monitor script read the value from a config file or prompt instead.
```

An MCP `headersHelper` reports:

```text theme={null}
headersHelper for MCP server 'internal-api' references ${user_config.*}. The substituted value would be passed to a shell; read the value inside the helper script instead (e.g. from an env var set in the server's "env" block).
```

**What to do:**

* For a hook, add an `args` array so it runs in [exec form](/docs/en/hooks#exec-form-and-shell-form), where each `${user_config.KEY}` becomes one argument with no shell in between. Or drop the reference and read the `$CLAUDE_PLUGIN_OPTION_<KEY>` environment variable inside the script
* For a monitor, drop the reference and have the monitor script read the value from a config file
* For a `headersHelper`, move `${user_config.KEY}` into the server's `headers` field, which isn't shell-parsed, or read the value inside the helper script

### Plugin archive integrity check failed

The plugin's marketplace entry uses an [`archive` source](/docs/en/plugin-marketplaces#zip-archives) with a `sha256` pin, and the digest of the downloaded file doesn't match the pin. Claude Code refuses the install, so nothing changes in the plugin cache. The mismatch has three possible causes:

* The file at the URL changed after the author computed the pin
* The author entered the wrong digest in the marketplace entry
* The URL serves a different file than the author pinned

```text theme={null}
Plugin archive integrity check failed for https://artifacts.example.com/claude-plugins/my-plugin.zip: expected sha256 6bfa50e3d2e00c052b46abe51fff89346ac803e45771f76dcf6df1ab74cca5e1, got ac52220c0914ef8ca6a602e4a7362f88d30fb021110f72a6d15b68c3fe7df2b7. The archive was not installed. Verify the sha256 in the marketplace entry, or that the URL serves the intended file.
```

**What to do:**

* If you publish the plugin, recompute the digest of the exact file the URL serves, for example with `shasum -a 256 my-plugin.zip`, or `Get-FileHash -Algorithm SHA256 my-plugin.zip` in PowerShell, and update the `sha256` in the marketplace entry
* If you install the plugin, run `/plugin marketplace update <name>` to refresh the catalog in case the entry was corrected, then retry the install
* If the digests still disagree after a refresh, ask the marketplace owner which file they pinned before installing

### Path escapes plugin directory

A plugin component path, declared in the plugin's `plugin.json` or in its [marketplace entry](/docs/en/plugin-marketplaces#plugin-entries), resolves outside the plugin's own directory. Claude Code drops that path and loads the rest of the plugin. The component name in the message, such as `commands` or `hooks`, names the field that declared the path.

```text theme={null}
commands path escapes plugin directory: ./../shared.md
```

In `claude plugin` command output, the same error reads `Path escapes plugin directory: ./../shared.md (commands)`.

Before v2.1.251, Claude Code loaded a `commands` path declared in a marketplace entry even when it pointed outside the plugin directory. Claude Code already rejected paths declared in `plugin.json` and the other component paths in a marketplace entry.

**What to do:**

* Move the referenced file inside the plugin directory and point the path at it with a `./` relative path
* To share files with other plugins in the same marketplace, link them with a symlink inside the plugin directory, following the [symlink rules](/docs/en/plugins-reference#share-files-within-a-marketplace-with-symlinks)

### Failed to load marketplace configuration

Claude Code keeps the plugin marketplaces you've added in a registry file at `~/.claude/plugins/known_marketplaces.json`. A plugin command that needs the registry, such as `claude plugin install`, fails with one of two messages when Claude Code can't use the file:

* `Failed to load marketplace configuration`: the file isn't valid JSON, or can't be read. An empty file fails this way too.
* `Marketplace configuration file is corrupted`: the file is valid JSON but its contents don't match the registry schema.

A missing file isn't a failure: Claude Code treats it as a registry with no marketplaces.

With an empty file, `claude plugin install` reports:

```text theme={null}
✘ Failed to install plugin "my-plugin": Failed to load marketplace configuration: JSON Parse error: Unexpected EOF
```

Before v2.1.246, `claude plugin install` didn't report this failure.

**What to do:**

* Open `~/.claude/plugins/known_marketplaces.json` and repair the JSON, or fix the entries the message names as not matching the registry schema
* If you can't repair it, delete the file or replace its contents with `{}`, then re-add each marketplace with `claude plugin marketplace add <source>`. Claude Code re-registers the marketplaces your user or managed settings declare in [`extraKnownMarketplaces`](/docs/en/settings-reference#extraknownmarketplaces) the next time you start it in a folder you've trusted.

## Tool errors

These errors come from Claude's built-in tools. Claude corrects most tool errors on its own; the first two below need a change from you, because they come from a subagent definition or a permission rule you control.

### Agent would be spawned with zero tools

Every entry in the subagent's [`tools` list](/docs/en/sub-agents#supported-frontmatter-fields) failed to match a usable tool, so Claude Code refused to launch the subagent: with no tools, it couldn't act. The message groups your entries by what went wrong:

* **Unrecognized**: the entry matches no tool name, usually a typo such as `Grpe` for `Grep`.
* **Not available to subagents**: the entry names a real tool that [subagents can't use](/docs/en/sub-agents#available-tools). Background subagents keep a smaller built-in tool set, so an entry that only a foreground subagent can use lands here when the subagent would run in the background, which is the default. If you list `Agent`, the message reports it under the next group instead.
* **Matched no tools in this session**: the entry is valid but no tool in the current session matches it right now, such as `mcp__github__*` with no GitHub MCP server connected, or `Agent` for a subagent at the [depth limit](/docs/en/sub-agents#let-subagents-spawn-their-own-subagents).

Omitting the `tools` field never triggers this refusal. If you leave the `tools` list empty, or `disallowedTools` removes every entry in it, Claude Code also skips the refusal and launches the subagent without tools.

Before v2.1.208, the subagent launched with no tools and could return an empty or confusing result.

```text theme={null}
Agent 'code-reviewer' would be spawned with zero tools — refusing. Its tools list resolved to nothing: unrecognized [Grpe]. Fix the agent's tools frontmatter or pass a different subagent_type.
```

**What to do:**

* Correct each entry the error names against the [tools available to subagents](/docs/en/sub-agents#available-tools)
* Remove entries for tools the session doesn't have, such as MCP tools from a server that isn't connected
* For a tool that [background subagents drop](/docs/en/sub-agents#available-tools), such as `LSP`, remove the entry. To keep the tool, [turn fork mode off](/docs/en/sub-agents#turn-fork-mode-on-or-off) and ask Claude to run the subagent in the foreground
* Delete the `tools` field instead of listing tools to give the subagent every [tool available to subagents](/docs/en/sub-agents#available-tools)
* For a `tools` list that contains only `Agent`, raise the [depth limit](/docs/en/sub-agents#let-subagents-spawn-their-own-subagents) or give the agent at least one other tool: Claude Code withholds `Agent` at that limit, so a list with nothing else in it resolves to no tools

### File is covered by a Read deny rule

The Edit or Write tool was called on a path matched by a [`Read` deny rule](/docs/en/permissions#read-and-edit), including creating a new file at that path. Both tools change content Claude has to be able to read back, so Claude Code refuses the call before any file access. NotebookEdit isn't covered by `Read` deny rules. Before v2.1.228, the rule blocked the Edit tool only, and before v2.1.208, only an `Edit` deny rule blocked edits.

```text theme={null}
File is covered by a Read deny rule in your permission settings and cannot be edited.
```

When Claude Code refuses the Write tool, the message ends `and cannot be written` instead.

**What to do:**

* If Claude should be able to change the file, remove or narrow the `Read` deny rule in `/permissions` or in [settings](/docs/en/settings-reference#permission-settings)
* If the file must stay untouched, keep the rule and add an `Edit` deny rule for the same path to block the NotebookEdit tool too

<h3 id="subagent-type-is-required">
  subagent\_type is required
</h3>

```text theme={null}
subagent_type is required: the general-purpose agent is not available in this session. Available agents: ...
```

Claude called the [Agent tool](/docs/en/tools-reference#agent-tool-behavior) without a `subagent_type`, and this session has no [general-purpose subagent](/docs/en/sub-agents#built-in-subagents) to fall back on. That is the case in two setups:

* [`CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1`](/docs/en/env-vars) is set in non-interactive mode, which removes every built-in subagent
* The session's main-thread agent has a [`tools: Agent(...)` allowlist](/docs/en/sub-agents#restrict-which-subagents-can-be-spawned) that leaves out `general-purpose`

**What to do:**

* Usually nothing: the message lists the subagents the session does have, so Claude can retry with one of them
* If Claude keeps failing, add `general-purpose` to the `tools: Agent(...)` allowlist, or unset `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS`

Before v2.1.235, the same call failed with `Agent type 'general-purpose' not found`.

### Memory index is over its read limit

Claude wrote to the [auto memory](/docs/en/memory#auto-memory) index `MEMORY.md` and left it over one of its read limits: 200 lines or 25KB. The write succeeded, but only the first 200 lines or 25KB, whichever comes first, load at the start of a session, so everything past the limit is dropped each time the index is read. Before v2.1.210, an over-limit index was silently truncated on the next load with no write-time signal.

```text theme={null}
Error: this write left the memory index at MEMORY.md at 214 lines, over its 200-line read limit. The write succeeded, but everything past the limit is silently dropped each time the index is loaded — entries at the end are already invisible to readers. Rewrite it to under 140 lines now: keep one line per entry, move detail into topic files, and merge or drop stale entries.
```

Only the content that loads counts toward the limits. YAML frontmatter and block-level HTML comments are stripped before the index is loaded, so they're excluded from the measurement. Before v2.1.211, Claude Code measured the raw file, and frontmatter or comments could trigger this error even when the loaded content fit.

Claude Code delivers the error to Claude after the write rather than printing it as a banner in your terminal, so you may notice it only in the transcript.

When Claude's write brings the file near a limit without crossing it, Claude Code returns a milder reminder to compact the index instead of this error.

**What to do:**

* Let Claude rewrite `MEMORY.md`, or ask it to: keep one line per entry, move detail into topic files, and merge or drop stale entries
* To trim the index yourself, see [Audit and edit your memory](/docs/en/memory#audit-and-edit-your-memory)

### pkill pattern matches the Claude Code process

A `pkill` command in a Bash tool call used a pattern, typically with `-f`, that matches the Claude Code process itself, so Claude Code refuses the command instead of letting it end the session. Claude Code tests the pattern with `pgrep` before running `pkill` and refuses when its own process ID is in the result. The check runs on Linux only; on macOS, `pkill` runs unmodified. Before v2.1.214, the command ran, and a matching pattern killed the Claude Code session mid-turn.

```text theme={null}
pkill: refusing to run — this pattern matches the Claude CLI process (PID 12345). Narrow the pattern, or target your own children with `pkill -P $$ ...`.
```

The refusal appears in the Bash tool result rather than as a banner in your terminal, and Claude usually adjusts the command on its own.

**What to do:**

* Narrow the pattern so it matches only the intended process, for example the full path of the target binary rather than a short substring
* To stop processes started by the current shell, use `pkill -P $$` with the pattern, which limits the match to the shell's own child processes

<h3 id="failed-to-write-to-a-teammate-inbox">
  Failed to write to a teammate's inbox
</h3>

Claude Code couldn't write a message to a teammate's mailbox file under `~/.claude/teams/{team-name}/inboxes/`, so the recipient received nothing. The write fails when Claude Code can't create or update the file, for example because the disk is full, the directory isn't writable, or another agent holds the inbox lock for too long. Before v2.1.224, Claude Code reported the message as sent even when the write failed.

The error appears in the sending agent's tool result rather than as a banner in your terminal, and its text tells Claude to try again:

```text theme={null}
Failed to write to researcher's inbox — nothing was sent. Try again, or message the lead.
```

Structured [agent team](/docs/en/agent-teams) protocol messages fail the same way, and the error names the undelivered message: when Claude Code can't write a plan approval, plan rejection, shutdown request, or shutdown rejection, the error reads `Failed to write the <message> to <name>'s inbox — nothing was sent`. The `plan approval` in that list is the lead's decision approving a teammate's plan; the teammate's plan submission is the separate `plan approval request` message. That message and two other protocol messages carry their own message text and consequence:

* `Failed to write the plan approval request to the lead's inbox — plan not submitted; try again`: the teammate's plan never reached the lead, and the teammate stays in plan mode until a resubmission succeeds
* `The permission request could not be delivered to the team lead (mailbox write failed)`: the teammate's permission request never reached the lead, so nobody approved the tool call
* `The confirmation could not be written to team-lead's inbox.`: the shutdown approval itself took effect and the teammate exits; only the confirmation to the lead is missing

When you message a teammate yourself, typing `@name` followed by the message in the lead session, the same failure appears as a notification, `Couldn't write to @name's inbox — message not sent. Try again.`, and Claude Code keeps your text in the prompt box so you can send it again.

**What to do:**

* Ask the sender to resend the message; contention for the inbox lock is transient and clears on retry
* Check free disk space, and check that `~/.claude/teams` and the files under it are writable by your user

### Message too large for cross-session delivery

Claude's [cross-session message](/docs/en/cross-session-messaging) to another of your sessions on this machine was too long to send. Claude Code refused it, and the receiving session got nothing. The refusal appears in the sending session's tool result, not as a banner in your terminal. It names both sizes and how to make the message fit:

```text wrap theme={null}
Failed to send to api-worker: Message too large for cross-session delivery: the serialized message is 1,203,844 characters and the limit is 1,048,576. Shorten the message text — put bulk content in a file the recipient can read rather than in the message — or split it into smaller messages.
```

Resending the same text fails the same way.

**What to do:**

* Ask Claude to summarize the message, or to put the bulk content in a file and send the file's path
* Ask Claude to split the content across several shorter messages

Before v2.1.235, Claude Code reported an oversized message as sent. The receiving session dropped it unread.

### Too many messages to this session just now

Claude sent a rapid burst of [cross-session messages](/docs/en/cross-session-messaging) to one of your sessions on this machine, and the burst reached what that session's inbox accepts. Claude Code refused the next send, and the receiving session got nothing from it. The refusal appears in the sending session's tool result, not as a banner in your terminal:

```text wrap theme={null}
Failed to send to api-worker: Too many messages to this session just now: 30 were sent recently and more would be dropped by its rate limit, so this one was not sent. Batch what remains into one message, or wait a little before sending more.
```

**What to do:**

* Usually nothing: Claude batches the remaining content into one message, or waits before sending more
* If you prompted the burst yourself, ask Claude to combine what's left into a single message

Before v2.1.236, Claude Code reported these sends as sent. The receiving session dropped them unread.

### Refusing to send a cross-session message

Before Claude Code writes a [cross-session message](/docs/en/cross-session-messaging) to another of your sessions on this machine, it checks that the target session's inbox socket is the endpoint the message was addressed to. When a check fails, Claude Code refuses the send in the sending session, and the target session receives nothing. For a message Claude sends, the refusal appears in the sending session's tool result:

```text theme={null}
Failed to send to api-worker: Refusing to send: reply target is a symlink
```

The text after `Refusing to send:` names the check that failed:

* `reply target is a symlink`: a symbolic link sits at the target session's socket path. Claude Code doesn't deliver through it, because a link there could redirect the message to an endpoint the target session didn't create.
* `cannot vet reply target`: Claude Code couldn't inspect the target path at all, for example because reading it failed with a permission error.
* `connected endpoint is not the expected process`: the process holding the socket isn't the session the message was addressed to, so the address is stale or another process replaced the socket.
* `connected endpoint identity could not be read`: Claude Code connected but couldn't read which process holds the other end, so it couldn't confirm the target. This can be transient.
* `connected endpoint is not owned by this user`: the process holding the socket runs as a different user account, so it isn't one of your sessions.
* `connected endpoint owner could not be read`: Claude Code connected but couldn't read which user account owns the other end, so it couldn't confirm the endpoint is yours.
* `connected endpoint is a different process with the expected pid`: the process id matches the one the message was addressed to, but Claude Code couldn't confirm it's the same process. Usually that session exited and the operating system reused its process id, so the address is stale.

**What to do:**

* Usually nothing: the checks keep a message from reaching an endpoint other than the session it was addressed to, and nothing was sent
* Ask Claude to list your sessions again and resend; a refusal caused by a stale address clears once Claude sends to the current one
* If `reply target is a symlink` repeats for one session, check what created a link at that session's socket path, shown in its `/status` under `Peer address`
* For `connected endpoint identity could not be read`, resend; the condition can be transient
* If `connected endpoint is not owned by this user` appears on a shared machine, the session at that address runs under another user's account, so Claude can't message it from yours

Before v2.1.248, Claude Code didn't check the endpoint's owning user or process start time, so the refusals that name those checks don't appear on earlier versions.

<h3 id="refusing-after-a-symlink-changed">
  Refusing to read, write, or search a path
</h3>

Claude Code checks a file path's [permission rules](/docs/en/permissions#read-and-edit), then confirms that resolution again when the tool opens the file or starts the search. When it can't confirm that the path still leads to the location the check approved, Claude Code refuses the operation instead of following it. The refusal appears in the tool result:

```text theme={null}
Refusing to read /path/to/file: its symlink resolution changed after permission was checked. If a link in the working directory is being rewritten concurrently, stop that and retry.
```

The text after the path names the reason:

* `its symlink resolution changed after permission was checked`: a symlink along the path, or at a Grep or Glob search root, was replaced between the permission check and the operation
* `its parent-directory symlink resolution changed after permission was checked`: a directory the write path passes through no longer resolves to the approved location
* `it is a symbolic link. Write to the link's target path instead`: a symbolic link sits at the approved write location itself
* `a path one of its Read deny rules is written through changed while the search was being prepared. Retry.`: a `Read` deny rule for the search names a path that passes through a symlink, and that link changed while Claude Code was preparing the search
* `it could not be opened (EACCES) — it is unreadable, or is being replaced concurrently.`: the search root exists but couldn't be opened; the parenthesized code is the operating system error
* `its permission check expired before it ran (too many concurrent file operations). Retry.`: Claude Code evicted the approval record under many simultaneous file operations before the tool used it; retrying runs a fresh permission check
* `ripgrep was found only by name on PATH, and a search outside the working directory cannot apply your Read deny rules in that configuration`: Claude Code couldn't resolve the `rg` binary to an absolute path, so it refuses searches outside the working directory rather than run one your deny rules don't cover

**What to do:**

* Usually nothing: the refusal reaches Claude as the tool result, and the refused operation doesn't run
* If a symlink refusal repeats on one path, find what keeps rewriting a link there, such as a build tool or file watcher, or ask Claude to use the file's resolved path instead of the linked one
* For the ripgrep refusal, install ripgrep with your package manager so `rg` resolves to an absolute path on `PATH`, or keep searches under the working directory

Before v2.1.251, Claude Code re-checked a path's resolution only for file writes, so a link replaced after the permission check could redirect a read or search to a different location without a message. Of these refusals, only the parent-directory write refusal appears on earlier versions.

## Background session errors

[Background sessions](/docs/en/agent-view) run without an interactive terminal of their own, so commands that need one behave differently there. These messages appear in the transcript of a background session, in the terminal that attaches to one, in the session or shell you dispatch from, or, for the [worktree-guard entries](#write-or-command-blocked-because-the-path-cannot-be-safely-resolved) below, in any session isolated in a worktree or running a worktree-isolated subagent; where a message is specific to one surface, its entry says so.

### Commands refused in a background session

Commands that open an interactive dialog can't do so while no terminal is attached to a background session. `/install-github-app`, the `/mcp` settings list, and the authentication actions in the MCP server menu respond with a message, and the session appears under **Needs input** in [agent view](/docs/en/agent-view) so you can find it, attach, and run the command again. While a terminal is attached, these commands work normally.

Before v2.1.216, the session didn't appear under **Needs input** after one of these refusals. In v2.1.213 through v2.1.215, the commands still worked while a terminal was attached, and the refusal message told you to attach and run the command again. From v2.1.208 through v2.1.212, Claude Code refused them even while a terminal was attached, with a message such as `Can't open MCP settings in a background session`; on those versions, run the command from a regular `claude` session instead, or upgrade. Before v2.1.208, they opened their dialog inside the background session. In v2.1.208 only, Claude Code also refused the `/model` picker in a background session, and `/upgrade` printed the upgrade URL instead of opening a browser.

The wording names the command. The `/mcp` settings list reports:

```text theme={null}
Can't open MCP settings while no terminal is attached to this background session. This session now shows "needs input" in agent view — open it and run /mcp to manage servers, or use `/mcp enable|disable|reconnect <server>` to steer without the panel.
```

**What to do:**

* Attach to the session from agent view, where it's listed under **Needs input**, and run the command again
* Or use the form the message names, such as `/mcp reconnect <server>`, `/mcp enable`, or `/mcp disable`, which work without attaching

### Write or command blocked because the path cannot be safely resolved

Claude addressed a file or working directory through a spelling that the [worktree-isolation guard](/docs/en/agent-view#how-file-edits-are-isolated) can't resolve to one verifiable location. The guard checks writes and command working directories in [any session isolated in a worktree](/docs/en/worktrees#how-claude-code-enforces-isolation), interactive or background, and in [worktree-isolated subagents](/docs/en/worktrees#isolate-subagents-with-worktrees). It resolves symlinks before checking that the operation doesn't reach the shared checkout, and when resolution fails, it blocks the operation rather than letting it land there. The message names the path forms it refuses and how to retry:

```text theme={null}
This write was blocked because the path is spelled in a form that cannot be safely resolved (for example through a symlink storing a raw dot segment, a network-share or device-namespace shape, or an unreadable ancestor directory). If the file is inside the worktree /path/to/worktree, address it by its direct symlink-free path instead.
```

A blocked command reports the same cause for its working directory and ends with `re-run the command from its direct symlink-free path`. Before v2.1.217, the guard compared path spellings without resolving symlinks, so these spellings weren't blocked and a write routed through a symlink could land in the shared checkout.

**What to do:**

* Usually nothing: the full message goes to Claude as a tool error, and Claude retries with the direct path it names. For a blocked file edit, the conversation view shows only a short `Error editing file` line; the full message appears in the transcript view, which you open with `Ctrl+O`. A blocked command prints it in its command output.
* If the block repeats on the same file, the path likely runs through a committed symlink whose target contains `..`, such as `docs/current -> ../README.md`; ask Claude to edit the target file by its real path instead of through the link

### Write or command blocked because the path names a network location

Claude addressed a file or working directory through a path that names a drive that isn't on your machine, a UNC share such as `\\server\share\file` or a `/net` automount path, while the session's checkout is on a local disk. The same [worktree-isolation guard](#write-or-command-blocked-because-the-path-cannot-be-safely-resolved) can't verify that such a path stays out of the shared checkout, so it blocks the operation. Isolating the session in a worktree doesn't lift the block. The message names the form of path to use instead:

```text theme={null}
This write was blocked because the path is network-shaped (a UNC share or /net automount spelling) while this session's checkout is local. Isolating cannot unblock it. If the file is genuinely inside the worktree /path/to/worktree, address it by its local, plainly-spelled path instead.
```

A blocked command reports the same cause for its working directory and ends with `re-run the command from its local, plainly-spelled path`. Before v2.1.217, the guard compared path text only, so addressing a file inside the checkout through a UNC or `/net` path wasn't blocked.

**What to do:**

* Usually nothing: Claude retries with the local spelling the message asks for
* If the file is on a network share rather than a local file spelled with a network path, it's outside the session's local workspace; edit it from a regular interactive session instead

### This session has no saved transcript

You attached to a stopped [background session](/docs/en/agent-view) that was backgrounded from another conversation with `←` or `/background` and stopped before its first response finished. Until that first response finishes, the conversation still lives only in the session it was backgrounded from, so `claude attach` refuses to start the stopped session rather than begin a blank conversation under the same session ID. The message ends with the `claude respawn` command for this session:

```text theme={null}
This session has no saved transcript — it was stopped before its first response finished. If it was backgrounded from another conversation, that one is still intact; `claude respawn <id>` starts this one fresh.
```

Opening the same session's row in [agent view](/docs/en/agent-view) shows `Press enter again to restart this session fresh` below the list instead, and a second `Enter` on the row restarts the session with an empty conversation. Before v2.1.212, opening the row showed the refusal message with no way to restart from agent view. Before v2.1.211, opening the stopped session silently started that blank conversation and could re-run the session's original prompt.

**What to do:**

* The conversation you backgrounded from is intact: resume it with [`claude --resume`](/docs/en/sessions) or keep working in it
* To start the stopped session fresh anyway, run `claude respawn <id>` with the ID from the message, or press `Enter` twice on its row in agent view
* If the session did finish a response and you still see this refusal on a version before v2.1.214, an unreadable folder in `~/.claude/projects` could make the transcript scan miss the saved conversation; update to v2.1.214 or later, which tolerates unreadable folders during the scan

<h3 id="this-session-is-running-in-another-terminal">
  This session is running in another terminal
</h3>

You opened a stopped session's row in [agent view](/docs/en/agent-view), and its saved conversation is already open in another live Claude Code process on this machine, so Claude Code refuses to start a second process that would write to the same transcript. Which message you see depends on [what holds the conversation](/docs/en/agent-view#opening-a-session-says-the-conversation-is-already-open):

```text theme={null}
Can't open — this session is running in another terminal
This conversation is already open in another running Claude session — use that one, or close it and try again
```

* **`running in another terminal`**: a terminal holds the conversation, for example one where you resumed it with `claude --resume` or `/resume`. The row also shows `Open in a terminal`.
* **`already open in another running Claude session`**: another non-interactive Claude Code process holds it, for example a [background session](/docs/en/agent-view#the-supervisor-process) process for the same conversation that hasn't exited yet.

Claude Code saves a reply you typed when opening the row and sends it as the session's next prompt when the session next starts.

**What to do:**

* Continue the conversation in the process that has it open, or exit that process and open the row again

Before v2.1.248, only the `already open in another running Claude session` refusal existed: a conversation resumed in a terminal didn't count as open, and opening the row started a second Claude Code process writing to the same conversation.

<h3 id="this-sessions-saved-conversation-is-no-longer-on-disk">
  This session's saved conversation is no longer on disk
</h3>

You opened a [background session](/docs/en/agent-view) that ended while the background service was off, and [transcript cleanup](/docs/en/settings-reference#cleanupperioddays) has since removed its saved conversation, for example after the machine was off for weeks. Opening such a row normally [resumes its saved conversation](/docs/en/agent-view#sessions-show-as-failed-after-shutdown). With nothing left to resume, Claude Code refuses rather than re-run the session's original prompt without asking:

```text theme={null}
This session's saved conversation is no longer on disk (it ended while the background service was off, and old transcripts are cleaned up), so there is nothing to resume. `claude rm 7c5dcf5d` deletes the row; `claude respawn 7c5dcf5d` runs its original prompt again instead.
```

`claude attach <id>` prints this text. In agent view, the footer is shorter and ends with `ctrl+x deletes the row`.

**What to do:**

* Run `claude rm <id>` to delete the row. When one of the [kept cases](/docs/en/agent-view#what-deleting-a-session-removes) applies, `claude rm` keeps the row and the worktree instead and names the reason
* To run the session's original prompt again as a fresh conversation, run `claude respawn <id>`

Before v2.1.248, opening such a row re-ran the session's original prompt instead of refusing, pulling a weeks-old task back into the foreground.

<h3 id="worktree-has-commits-that-are-not-pushed-anywhere">
  Worktree has commits that are not pushed anywhere
</h3>

You tried to delete a [background session](/docs/en/agent-view#what-deleting-a-session-removes) whose worktree holds commits Claude Code can't confirm are saved elsewhere. Claude Code keeps the worktree and the session row rather than destroy the commits. `claude rm` prints the kept path and the reason:

```text theme={null}
kept 7c5dcf5d — worktree has commits that are not pushed anywhere
  worktree kept at /home/you/project/.claude/worktrees/fix-login
  resolve that (commit/push, or remove the worktree), then run 'claude rm 7c5dcf5d' again
```

When you delete from [agent view](/docs/en/agent-view) with a `Ctrl+X` double-press, you consent to discarding uncommitted changes, but not to discarding commits, so Claude Code refuses there too. After a refused delete, the session's row shows `not deleted` with the same reason.

Commits on a remote don't block the delete. Neither do commits on the local copy of your `origin` remote's default branch, as long as that branch is checked out in your main checkout, the repository directory itself rather than a worktree.

**What to do:**

* Push the worktree's branch, or merge it into the default branch checked out in your main checkout, then delete the session again
* To delete the session without pushing or merging the commits, first note the branch that `git worktree list` shows for the path the message names. Remove the worktree yourself with `git worktree remove --force <path>`, as described in [Clean up subagent and background-session worktrees](/docs/en/worktrees#clean-up-subagent-and-background-session-worktrees), then run `claude rm <id>` again. Neither step deletes that branch, so the commits stay on it until you run `git branch -D <branch>`.

Before v2.1.248, the default branch checked out in your main checkout didn't count: a branch you had already merged there still triggered this refusal until its commits reached a remote.

### Terminal host process died

Each [background session's](/docs/en/agent-view) terminal runs in a host process under the background service, and that process died while the service still held its connection, so the session couldn't be reached.

On Linux and WSL, the background service checks each host process every few seconds, marks the session failed when the process has exited but its connection to the service never closed, and shows the reason on its row in [agent view](/docs/en/agent-view#read-session-state):

```text theme={null}
terminal host process died — press Enter to restart
```

If you open the row before the check runs, the footer shows `This session's terminal host process died (the conversation is saved) — press Enter to restart it` and the row turns failed.

From the shell, `claude attach <id>` restarts a session already marked failed for a dead host, and otherwise prints the cause and exits:

```text theme={null}
Couldn't attach to <id> — This session's terminal host process died (the conversation is saved) — run `claude attach <id>` again to restart it on a fresh host.
```

The conversation is saved either way.

A row running a [shell command](/docs/en/agent-view#run-a-shell-command) instead shows `terminal host process died — its output is gone; the command was not run again`, and `claude attach` prints `This command's terminal host process died — its output is gone and the command was not run again`. Claude Code never reruns the command for you.

**What to do:**

* In agent view, press `Enter` on the failed row; the session restarts on a fresh host process and the conversation resumes
* From the shell, run `claude attach <id>` again. Claude Code prints `Session <id>'s terminal host died — restarting it on a fresh one…` and reopens the session
* You can't restart a shell-command row this way; dispatch the command again to rerun it

Before v2.1.247, a dead host process could pass every liveness check the background service ran, so opening the session showed `opening… · esc to cancel` indefinitely and `claude attach <id>` waited without reporting an error.

<h3 id="session-isnt-responding">
  Session isn't responding
</h3>

You opened a [background session](/docs/en/agent-view) and the background service accepted the open, but no output arrived for about ten seconds, so Claude Code concludes that the process relaying the session's terminal can't deliver output, and ends the attempt instead of waiting.

In agent view, Claude Code offers a restart in the footer:

```text theme={null}
Press enter again to restart this session — it isn't responding (its conversation is saved and resumes).
```

From the shell, `claude attach <id>` prints the cause and exits:

```text theme={null}
Couldn't attach to <id> — Session isn't responding — `claude stop <id>`, then `claude attach <id>` restarts it (the conversation is saved).
```

Claude Code never restarts a row running a [shell command](/docs/en/agent-view#run-a-shell-command) for you, because a restart would run the command again.

**What to do:**

* In agent view, press `Enter` on the same row again. Claude Code stops the unresponsive process and restarts the session, and the conversation resumes. Nothing is stopped without that second press
* From the shell, run `claude stop <id>`, then `claude attach <id>`
* For a shell-command row, press `Ctrl+X` in agent view or run `claude stop <id>` to stop it; dispatch the command again to rerun it

### Session was stopped while the respawn was in flight

You opened a [background session](/docs/en/agent-view) whose process wasn't running, and while Claude Code was restarting it, another Claude Code process stopped it, for example `claude stop` in another terminal. Claude Code keeps the session stopped:

```text theme={null}
Session <id> was stopped while the respawn was in flight
```

Opening a session you just dispatched, while its process is still starting, waits for the process instead. Before v2.1.246, opening it at that moment could stop it and show this message.

**What to do:**

* If you didn't stop the session, open its row again in agent view or run `claude respawn <id>` to restart it
* If you stopped it yourself, nothing remains to do: the session stays stopped

<h3 id="session-agent-no-longer-available">
  Session agent no longer available
</h3>

You resumed a session that was running a [custom agent](/docs/en/sub-agents#invoke-subagents-explicitly), started with `--agent` or the `agent` setting, and Claude Code didn't find an agent by that name. It searches the session's original directory first, when you have [trusted that workspace](/docs/en/permissions#project-allow-rules-and-workspace-trust), then the directory you resume from. The session still resumes, but with the default tools and system prompt, so the agent's tool restrictions no longer apply:

```text theme={null}
This session was running agent 'code-reviewer', which is no longer available (no agent by that name in /home/you/project). Continuing with the default tools and system prompt — the agent's tool restrictions no longer apply. To restore it, re-create the agent, or resume with an explicit --agent <name>.
```

The warning names only the directories Claude Code searched, and it appears in the resumed conversation whether you wake a [background session](/docs/en/agent-view), run `/resume` or `claude --resume`, or resume in [non-interactive mode](/docs/en/headless), where it also goes to stderr. Sessions using `--input-format stream-json` don't show it, because the Agent SDK supplies agents after startup.

Claude Code doesn't save the fallback to the session, so the warning repeats on each resume until you act. The built-in `claude` agent doesn't trigger the warning, since falling back to the default toolset changes nothing for it. Before v2.1.216, Claude Code silently continued as the default agent, and the lookup covered only the directory you resumed from, so a project-scoped agent was lost on any resume from another directory.

**What to do:**

* Re-create the agent file at `.claude/agents/<name>.md` in the session's project, or at `~/.claude/agents/<name>.md` for a personal agent, then resume again
* Or resume with `--agent <name>` naming an agent that does exist, to run the session as that agent instead
* If the agent is project-scoped and you haven't trusted the session's original directory, run Claude Code there once, accept the trust dialog, then resume again

### CLAUDE\_CODE\_PROCESS\_WRAPPER launcher errors

[`CLAUDE_CODE_PROCESS_WRAPPER`](/docs/en/corporate-launcher) is set, and its value can't be used, so Claude Code refuses to start the affected process rather than run it without the launcher. Configuration problems are reported with a message that starts with the variable name and states the reason, for example:

```text theme={null}
CLAUDE_CODE_PROCESS_WRAPPER: launcher `/opt/corp/launcher` is not an executable regular file
```

A launcher that starts but exits without replacing itself with Claude Code fails the session it was starting, and the session's row in agent view reports that the launcher `must exec, not daemonize`, followed by anything the launcher printed. A session that can't start or reach the background service because of the launcher reports the launcher problem as the reason inside `Couldn't reach the background service (...)`.

**What to do:**

* Set the variable to the absolute path of an executable that ends by calling `exec "$@"`. See [the launcher contract](/docs/en/corporate-launcher#the-launcher-contract) for the full contract
* Check `/status`, which shows the resolved launch command in its Self-exec entry and warns when the running background service doesn't match it, or run `claude daemon status` from a shell
* After fixing the value in the `env` block of [settings](/docs/en/corporate-launcher#set-up-the-launcher), restart the background service with `claude daemon stop --any` so the next dispatch starts a wrapped one

### EUNKNOWN when starting a background session

Windows refused to start a program with an error code that has no standard name, so the failure surfaces as `EUNKNOWN`. The usual trigger is a software restriction policy, such as Group Policy or AppLocker, blocking the program being started. The error appears when you start a [background session](/docs/en/agent-view) with `/background` or `claude --bg`:

```text theme={null}
Couldn't reach the background service (spawn background service: EUNKNOWN: unknown error, uv_spawn) — run 'claude daemon status'
```

On some accounts the message says `daemon` in place of `background service`.

On an npm installation, an `EUNKNOWN` that appears while `npm install -g @anthropic-ai/claude-code` is replacing the binary has the same cause as [`EACCES` during a reinstall](#eacces-when-starting-a-background-session) and clears when you retry after the install finishes.

Claude Code starts the background service through PowerShell so the service survives closing the terminal, using PowerShell 7 when it's installed and Windows PowerShell 5.1 otherwise. When neither PowerShell can run, Claude Code starts the service directly instead, so a policy that blocks only PowerShell doesn't cause this error. If you see it while no npm install is running, the policy is blocking the Claude Code executable itself.

Before v2.1.212, Claude Code used only Windows PowerShell 5.1 to start the service, so any machine where Group Policy blocked PowerShell 5.1 failed with `Couldn't start the session — EUNKNOWN: unknown error, uv_spawn`, even with PowerShell 7 installed.

**What to do:**

* If the message reads `Couldn't start the session`, upgrade to v2.1.212 or later. On earlier versions you can also run `claude daemon run` in a separate terminal first, then start the background session again. That command runs the background service in the terminal's foreground, so the service lasts only as long as that terminal stays open.
* If an npm install was replacing the binary, wait for it to finish, then start the background session again
* If the error appears on v2.1.212 or later while no npm install is running, ask your Windows administrator to allow the Claude Code executable in the restriction policy
* If the background service stops when you close the terminal, Claude Code started it without PowerShell. Install PowerShell 7, or ask your administrator to unblock PowerShell, so the service can outlive the terminal.

### EACCES when starting a background session

Claude Code couldn't run its own binary to start the [background service](/docs/en/agent-view#the-supervisor-process) that hosts background sessions. On an npm installation, this usually means `npm install -g @anthropic-ai/claude-code` was replacing the binary at that moment, whether you ran it or the [auto-updater](/docs/en/setup#auto-updates) did. The error appears when you open a session from [agent view](/docs/en/agent-view):

```text theme={null}
Couldn't start the background service — spawn background service: EACCES: permission denied, posix_spawn '/usr/local/lib/node_modules/@anthropic-ai/claude-code/bin/claude'
```

When you start a session with `/background` or `claude --bg`, the same reason appears inside `Couldn't reach the background service (...)`. During the same reinstall window the error can name another code instead, such as `ENOENT` or `ENOEXEC`, or `EUNKNOWN` or `EPERM` on Windows; an `EUNKNOWN` that persists across retries has a [different cause](#eunknown-when-starting-a-background-session).

On an npm installation, Claude Code waits up to ten seconds for the reinstall to finish and retries on its own, so you see the error only when the binary stays unrunnable for longer, such as while npm is still downloading the package. Before v2.1.246, Claude Code failed at once.

**What to do:**

* Wait a few seconds, then open the session or dispatch again.
* If the error persists while no npm install is running, your user can't run the installed binary. Check its permissions and its directory's, or reinstall Claude Code.

### Background service exited before it became reachable

The process Claude Code started as the [background service](/docs/en/agent-view#the-supervisor-process) exited before it accepted connections, so Claude Code couldn't open your session. When the service printed an error before exiting, the reason in parentheses gives the exit code or signal and the first line the service printed, which names what stopped it:

```text theme={null}
Couldn't reach the background service (background service exited before it became reachable (exit code N): <the service's first error line>) — run 'claude daemon status'
```

When you open a session from [agent view](/docs/en/agent-view), the same reason follows `Couldn't start the background service —`. When the service printed nothing before exiting, the message says `nothing on stderr` instead.

Claude Code reports the failure with the service's error line. Before v2.1.246, the failure surfaced only after a 45-second wait, as `background service did not become reachable within 45s`, without the service's error line.

**What to do:**

* If the message quotes a line, fix what it names, then open the session or dispatch again. The next attempt starts the service again
* Run `claude daemon status` to check whether a service is running now

## Wrapper and IDE errors

These errors come from the program that launched Claude Code for you, such as an IDE extension or an [Agent SDK](/docs/en/agent-sdk/overview) application, rather than from Claude Code itself.

### Claude Code process exited with code N

The underlying `claude` process exited with a non-zero code. The exit code alone doesn't say what failed: the real error is in the process's own output, which the wrapper appends when it captured any and otherwise keeps in its logs.

```text theme={null}
Error: Claude Code process exited with code 1
```

**What to do:**

* In VS Code, follow the **View output logs** link shown with the error to see the underlying failure
* In an Agent SDK application, catch the error around your message loop. The entries under [CLI process exit](/docs/en/agent-sdk/troubleshooting#cli-process-exit) cover what your code receives in each SDK language.
* Run `claude` in a terminal in the same project. The failure usually reproduces there with its real error message, which you can then look up on this page.
* Run `claude doctor` in a terminal to check the installation and configuration

<h3 id="could-not-locate-the-claude-cli-on-path">
  Could not locate the Claude CLI on PATH
</h3>

The [VS Code extension](/docs/en/vs-code) shows this error on Windows when you open Claude Code in the integrated terminal, the terminal's shell is PowerShell, and the extension can't find the installed `claude` executable on PATH. The extension refuses to launch Claude Code until it finds the installed `claude` on PATH.

```text theme={null}
Failed to run Claude Code: Error: Could not locate the Claude CLI on PATH. Launching by name in a PowerShell terminal would run a 'claude' from the open folder instead of the installed CLI, so the launch was blocked. Make sure the Claude CLI's install directory is on your system PATH (not only your PowerShell profile), then restart VS Code and try again. VS Code reads PATH when it starts, so PATH changes take effect only after a restart.
```

**What to do:**

* Open a new PowerShell window outside VS Code and run `where.exe claude`. If it doesn't print a path, the CLI isn't on your PATH: add its install directory by following [Verify your PATH](/docs/en/troubleshoot-install#verify-your-path). If it prints a path, the entry comes from your PowerShell profile or from a PATH change VS Code hasn't picked up yet; the next two steps cover those cases.
* Set the PATH entry as a user or system environment variable, not in your PowerShell profile. The extension doesn't run your profile, so a PATH edit that lives only there never reaches it.
* Restart VS Code after changing PATH. The extension checks the PATH that VS Code captured at startup, so a PATH change takes effect only after a restart.

## Rewind warnings

This warning comes from a [`/rewind`](/docs/en/checkpointing) code restore. It reports paths the restore refused to touch; the restore completed for every other tracked file.

<h3 id="restored-the-code-but-skipped-files">
  Restored the code, but skipped files
</h3>

A `/rewind` code restore skipped one or more tracked paths instead of writing or deleting through them. Claude Code skips a path when:

* it is, or became, a symlink, hard link, or other non-regular file
* its directory changed since the checkpoint
* its backup can't be safely read

Skipped paths keep their current contents. Before v2.1.216, `/rewind` wrote and deleted through links at tracked paths, and didn't report a partial restore.

```text theme={null}
Restored the code, but skipped 2 files: the tracked path is (or became) a link or other non-regular file, its directory changed since the checkpoint, or its backup could not be safely read. Skipped files were left untouched — run with --debug for the paths.
```

**What to do:**

* Identify which files were skipped so you can handle each one with the steps below. The message gives only a count; the debug log at `~/.claude/debug/<session-id>.txt` names each skipped path as the restore runs, so turn on debug logging with `/debug` before your next restore. On macOS or Linux, you can instead find the links directly: `find . -type l` for symlinks and `find . -type f -links +1` for hard-linked files.
* If a skipped file is a link you created on purpose, such as a config file managed by a dotfile manager or a file hard-linked by tools like pnpm, the rewind left its contents alone. To undo the session's changes to it, ask Claude to reverse the edit or edit the file yourself
* If you didn't create the link, inspect the path before trusting its contents: something replaced the file after the checkpoint

## Session saving warnings

Claude Code shows these warnings on a persistent line below the input box when it isn't saving your session transcript. The session keeps working either way; the warnings tell you the session may be missing from [`--resume`](/docs/en/sessions) later.

### Transcript writes are failing

Claude Code saves the transcript to disk as you work, and its writes to [the transcript file](/docs/en/sessions#where-transcripts-are-stored) are failing. The message names the cause with the underlying error code, for example a full disk:

```text theme={null}
Transcript writes are failing (disk full — ENOSPC) · recent messages may not be saved for resume
```

The warning appears at different points depending on the error:

* On the first failure for conditions that don't clear on their own: a full disk, an exceeded disk quota, a read-only filesystem, a path over the filesystem's length limit, or, on macOS and Linux, a permission error
* After repeated failures spanning at least a minute for everything else, including permission errors on Windows, where an antivirus scan can fail a single write that then succeeds on retry

Before v2.1.217, Claude Code dropped the failing writes without a warning, and a later `--resume` missing recent messages was the first sign.

**What to do:**

* Fix the condition the error code names: free disk space for `ENOSPC`; raise or clear the quota for `EDQUOT`; restore write access to the transcript location for `EACCES`, `EPERM`, or `EROFS`
* The warning clears on its own at the next successful write; no restart is needed
* Messages sent while the warning was showing may still be missing when you resume the session later

<h3 id="transcript-saving-is-off-skip-prompt-history">
  Transcript saving is off because CLAUDE\_CODE\_SKIP\_PROMPT\_HISTORY is set
</h3>

This session started with [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/docs/en/env-vars) set, so Claude Code writes no transcript or prompt history for it:

```text theme={null}
Transcript saving is off — CLAUDE_CODE_SKIP_PROMPT_HISTORY is set · --resume will not find this session; if unintended, unset it and restart
```

The variable is an intentional opt-out for ephemeral scripted sessions, but it can also reach a session through a shell profile, a wrapper script, or a parent process that exported it.

**What to do:**

* If you set the variable on purpose, no action is needed; the notice confirms the session won't appear in `--resume`, `--continue`, or up-arrow history
* If you didn't, remove the variable from the shell or script that launches `claude`, then start a new session. Messages from the current session aren't saved retroactively.

<h3 id="transcript-saving-is-off-child-session-marker">
  Transcript saving is off because of an inherited CLAUDE\_CODE\_CHILD\_SESSION marker
</h3>

Claude Code sets [`CLAUDE_CODE_CHILD_SESSION`](/docs/en/env-vars) in the subprocesses it spawns, and treats an interactive session that inherits it as nested: Claude Code saves no transcript for it, so sessions that Claude itself starts don't fill your `--resume` list. This notice means your current session inherited the marker:

```text theme={null}
Transcript saving is off — inherited CLAUDE_CODE_CHILD_SESSION marker · restart with CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1 to keep future transcripts
```

The notice is expected when you ran `claude` from inside another Claude Code session; it signals a misclassification when the marker leaked through a long-lived intermediary, for example a terminal, `screen` session, or launcher that a Claude Code session originally started.

Inside tmux, Claude Code detects a marker that arrived through the tmux server's global environment and keeps saving, so this notice doesn't appear for that case.

**What to do:**

* If you started this session from inside another Claude Code session on purpose, no action is needed
* If this is a top-level session, exit and restart with [`CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1`](/docs/en/env-vars) set. Saving applies from the restart, so messages sent before it aren't saved.
* To fix future launches from the same terminal or launcher, remove `CLAUDE_CODE_CHILD_SESSION` from its environment

## Configuration warnings

Claude Code writes most of these messages to stderr, not into the conversation, and writes most of them at startup. An entry says so when its message appears somewhere else, such as in the debug log or as a startup notice in the conversation view, or at another time, such as the [unrecognized-model diagnostic line](#unrecognized-model-id-on-a-request) at request time.

<h3 id="fullscreen-failed-start-notice">
  Fullscreen renderer didn't finish starting
</h3>

A previous [fullscreen](/docs/en/fullscreen) session on this machine exited before it finished starting, so Claude Code starts this session on the classic renderer and prints one of these notices:

```text theme={null}
Claude Code's fullscreen renderer didn't finish starting last time on this machine, so this launch is using the classic renderer. It will try fullscreen again next launch; /tui default keeps the classic renderer.

Claude Code's fullscreen renderer has repeatedly failed to start on this machine, so it has been turned off here. Run /tui fullscreen to try it again (this also resets after an update).
```

**What to do:**

* Follow [Fullscreen rendering](/docs/en/fullscreen#fullscreen-renderer-didnt-finish-starting). It says which notice you get, what Claude Code does in later sessions, and how to try fullscreen again or keep the classic renderer.
* If the session that died printed an exit message, see [Claude Code exited after an unrecoverable interface error](#exited-after-an-unrecoverable-interface-error) for what it names.

Before v2.1.236, Claude Code printed no notice and kept starting sessions in fullscreen rendering after a failed start.

<h3 id="exited-after-an-unrecoverable-interface-error">
  Claude Code exited after an unrecoverable interface error
</h3>

Claude Code prints this message when it exits because its terminal interface hit an error it can't recover from, in either renderer. The second sentence appears only when the error happened while the [fullscreen](/docs/en/fullscreen) renderer was starting:

```text theme={null}
Claude Code exited after an unrecoverable interface error (<error>). It happened while the fullscreen renderer was starting, so the next launch will use the classic renderer (CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1 forces that any time).
```

**What to do:**

* Start Claude Code again. To pick the conversation back up, run `claude --resume` in the same directory.
* If the message names the fullscreen renderer, [Fullscreen rendering](/docs/en/fullscreen#fullscreen-renderer-didnt-finish-starting) says what the next launch does, which depends on how you turned fullscreen on, and how to try fullscreen again or keep the classic renderer.

Before v2.1.236, Claude Code exited without printing a message after this kind of error.

<h3 id="agent-descriptions-are-over-the-15000-token-limit">
  Agent descriptions are over the 15.0k-token limit
</h3>

Claude Code shows this warning as a startup notice in the conversation view rather than on stderr. The combined descriptions of your [subagents](/docs/en/sub-agents), except the built-in ones, exceed 15,000 tokens as Claude Code estimates them. Each agent counts its name plus its `description` frontmatter. Claude Code loads every agent whether or not the total is over the limit, so the warning doesn't change what loads.

```text theme={null}
Agent descriptions are over the 15.0k-token limit (~16.2k tokens) · ask Claude to trim agent descriptions in .claude/agents/
```

**What to do:**

* Shorten the `description` frontmatter of your agent files, or ask Claude to trim them for you.
* Remove agent files you no longer use.

### Workspace has not been trusted

Claude Code found `permissions.allow` rules or `permissions.additionalDirectories` entries in the project's `.claude/settings.json` or `.claude/settings.local.json` and didn't apply them, because [allow rules from project settings require workspace trust](/docs/en/permissions#project-allow-rules-and-workspace-trust). The count, the setting name, and the file named in the message vary with your configuration. `deny` and `ask` rules aren't affected.

```text theme={null}
Ignoring 2 permissions.allow entries from .claude/settings.local.json: this workspace has not been trusted. Run Claude Code interactively here once and accept the trust dialog, or set projects["/Users/you/project"].hasTrustDialogAccepted: true in /Users/you/.claude.json.
```

**What to do:**

* Run `claude` in the directory and accept the trust dialog. [Project allow rules and workspace trust](/docs/en/permissions#project-allow-rules-and-workspace-trust) says which folder that acceptance covers.
* In [non-interactive mode](/docs/en/headless) with `-p` no dialog is shown. Set the `hasTrustDialogAccepted` entry in `~/.claude.json` using the exact `projects` key the message prints.
* If the message names `.claude/settings.local.json` and you started Claude Code outside a git repository or in your home directory, update to v2.1.200 or later. Versions 2.1.196 through 2.1.199 treated your own `.claude/settings.local.json` as repository-supplied in those workspaces. On v2.1.207 and later, updating isn't enough outside a git repository if you haven't trusted the folder: determining that a folder isn't inside a repository runs git, and Claude Code runs that check only after you accept the trust dialog, so use the first step. Your home directory and any other [configuration home](/docs/en/permissions#project-allow-rules-and-workspace-trust) are exempt and don't wait for the dialog. See [Project allow rules and workspace trust](/docs/en/permissions#project-allow-rules-and-workspace-trust).

<h3 id="remote-managed-settings-failed-to-load">
  Remote managed settings failed to load
</h3>

Your session is eligible for [server-managed settings](/docs/en/server-managed-settings), but Claude Code couldn't fetch them, so it shows this warning in interactive sessions. The parenthesized cause names what failed, such as `network error`, `request timed out`, or `authentication rejected (401)`, and the rest of the line says which policy the session runs on:

* **Settings cached from an earlier successful fetch**: Claude Code runs the session on that cached policy, except the [withheld environment variables](/docs/en/server-managed-settings#fetch-and-caching-behavior), and the line reads `using cached policy`.
* **No cache**: Claude Code runs the session without server-managed settings, and the line reads `no remote policy applied`.

**What to do:**

* Act on the cause the message names: for a network cause, check that this machine can reach `api.anthropic.com`; for an authentication cause, check your sign-in with `/status`
* Run `/status` or `claude doctor` for the full diagnostic

Before v2.1.248, Claude Code reported a failed settings fetch only in the debug log.

### headersHelper not run

Claude Code connected an MCP server with its static `headers` alone and skipped the server's [`headersHelper`](/docs/en/mcp#use-dynamic-headers-for-custom-authentication), because the helper is a shell command and the folder has no saved trust. A folder gets saved trust when you set its entry in `~/.claude.json` by hand or, outside your home directory, when you accept the trust dialog for it in an interactive session. See [Trust a folder before its headersHelper runs](/docs/en/mcp#trust-a-folder-before-its-headershelper-runs) for which servers this check applies to.

Claude Code writes this line in [non-interactive mode](/docs/en/headless) only, once per server. In an interactive session it writes the same refusal to the debug log instead.

```text theme={null}
MCP server 'internal-api': headersHelper not run — this workspace has no persisted trust; accept the trust dialog here once interactively, or set projects["/Users/you/project"].hasTrustDialogAccepted in /Users/you/.claude.json.
```

The `projects` key the message prints is the folder [Project allow rules and workspace trust](/docs/en/permissions#project-allow-rules-and-workspace-trust) says Claude Code keys the trust on. Accepting the trust dialog for a parent folder doesn't satisfy the check, and a `-p` or SDK session doesn't satisfy it either.

**What to do:**

* Run `claude` in the folder the message names, accept the trust dialog, then run your `-p` or SDK command again
* Set the `hasTrustDialogAccepted` entry in `~/.claude.json` yourself, using the exact `projects` key the message prints
* If you started the session in your home directory, work from a project directory you have trusted. When you accept the trust dialog in your home directory, Claude Code holds that trust for the current session only.

### Is not matched by file permission checks

Claude Code found a `Write`, `NotebookEdit`, `MultiEdit`, or `Glob` [permission rule](/docs/en/permissions#read-and-edit) with a path in one of your [settings files](/docs/en/settings#where-settings-live), in [managed settings](/docs/en/managed-settings), or in a `--allowedTools`, `--disallowedTools`, or `--settings` flag value. It checks file permissions against `Edit` and `Read` rules only, so it never consults a path rule that names one of the other file tools. It keeps the rule and changes nothing else; the warning names the rule, its source in parentheses, and the replacement to write:

```text theme={null}
Permission deny rule (.claude/settings.json): Write(docs/**) is not matched by file permission checks — only Edit(path) rules are. Use Edit(docs/**) instead (Edit rules cover all file-editing tools).
```

**What to do:**

* Replace `Write(path)`, `NotebookEdit(path)`, and legacy `MultiEdit(path)` rules with `Edit(path)`. `Edit` rules cover all file-editing tools.
* Except in `--allowedTools`, where Claude Code accepts a `Glob` rule without warning, replace `Glob(path)` rules with `Read(path)`.
* Fix the rule at the source the warning names in parentheses: a settings file path, or the flag itself for `--allowed-tools` and `--disallowed-tools`. A `claude-settings-<hash>.json` path that doesn't exist on disk stands for an inline `--settings` value; fix the JSON you pass to that flag.
* Leave bare tool-name rules such as `Write` or `Glob` alone. Claude Code matches them at the [tool level](/docs/en/permissions#match-all-uses-of-a-tool) and doesn't warn about them.
* If the source reads `managed policy settings`, forward the warning to whoever maintains your managed settings; you can't clear it yourself.

In a [background session](/docs/en/agent-view) or with `--output-format json` or `stream-json`, Claude Code writes the warning to the debug log instead of stderr, so machine-read output stays clean; run with `--debug` to capture it at `~/.claude/debug/<session-id>.txt`. Before v2.1.210, Claude Code accepted these rules without a warning.

### Has a wildcard before the rest of the command

Claude Code found a `Bash` allow rule whose `*` comes before a later word that determines which command it is, such as `Bash(git * main)` or `Bash(git -C * status *)`, in one of your [settings files](/docs/en/settings#where-settings-live), in [managed settings](/docs/en/managed-settings), or in an `--allowedTools` or `--settings` flag value. The `*` matches any text, including options inserted at that position: `Bash(git * main)` also approves `git -c core.fsmonitor=<script> diff main`, where `-c` makes git run a program the command names. [Wildcard patterns](/docs/en/permissions#wildcard-patterns) shows the matching rules.

The warning exists so you can narrow a rule whose wildcard is broader than you intended. Claude Code keeps the rule and changes nothing about how it matches; the warning names the rule and its source in parentheses:

```text theme={null}
Permission allow rule (.claude/settings.json): Bash(git -C * status *) has a wildcard before the rest of the command, so it also matches any options inserted at that position and approves them without a prompt. For git, options such as -c and --exec-path can run arbitrary commands. Replace that * with the exact value you mean, or only use * after the subcommand (for example Bash(git status *)).
```

**What to do:**

* Replace the `*` before the subcommand with the exact value you mean: `Bash(git checkout main)` in place of `Bash(git * main)`.
* Move every `*` after the subcommand: `Bash(git status *)` in place of `Bash(git -C * status *)`. Write one rule per subcommand you want to allow.
* Fix the rule at the source the warning names in parentheses: a settings file path, or the `--allowed-tools` flag itself. A `claude-settings-<hash>.json` path that doesn't exist on disk stands for an inline `--settings` value. Fix the JSON you pass to that flag.
* If the source reads `managed policy settings`, forward the warning to whoever maintains your managed settings, since you can't clear it yourself.

Claude Code doesn't warn about deny and ask rules with the same shape: it refuses or prompts for the extra commands they match rather than approving them. It also doesn't warn about rules whose subcommand comes before the first `*`, such as `Bash(git commit *)`, or rules in which no word other than an option follows the `*`, such as `Bash(git *)`, or about `:*` prefix rules such as `Bash(git:*)`.

In a [background session](/docs/en/agent-view) or with `--output-format json` or `stream-json`, Claude Code writes the warning to the debug log instead of stderr, so machine-read output stays clean. Run with `--debug` to capture it at `~/.claude/debug/<session-id>.txt`. Before v2.1.246, Claude Code accepted these rules without a warning.

<h3 id="crosssessioninbound-must-be-one-of-accept-hold-refuse">
  crossSessionInbound must be one of accept, hold, refuse
</h3>

A settings file sets [`crossSessionInbound`](/docs/en/settings-reference#crosssessioninbound) to a value Claude Code doesn't recognize, such as the typo `"reject"`. The warning's second sentence depends on which file holds the value; in a user, project, local, or `--settings` file it reads:

```text theme={null}
"crossSessionInbound" must be one of "accept", "hold", "refuse"; received "reject". This value was ignored; while it is present, cross-session messages are held for your approval instead of being delivered. Set it to one of the values above.
```

In [managed settings](/docs/en/managed-settings), Claude Code treats the unrecognized value as `refuse`, the most restrictive value, and the warning says cross-session messages are turned away until an administrator fixes it. For how the hold combines with values in your other settings files, see [`crossSessionInbound`](/docs/en/settings-reference#crosssessioninbound).

**What to do:**

* Set the key to `"accept"`, `"hold"`, or `"refuse"`, or remove it
* When the warning names managed settings, ask the administrator to fix the value

Before v2.1.248, Claude Code ignored an unrecognized value without warning.

<h3 id="the-200k-limit-isnt-enforced">
  The 200K limit isn't enforced
</h3>

You set [`CLAUDE_CODE_DISABLE_1M_CONTEXT=1`](/docs/en/env-vars), which normally makes [auto-compaction](/docs/en/model-config#default-auto-compact-thresholds) hold sessions on 1M-context models to a 200K window, but no compaction threshold caps this session at or below 200K, so the conversation can grow past it.

```text theme={null}
CLAUDE_CODE_DISABLE_1M_CONTEXT is set, but the 200K limit isn't enforced for <model>, so this session can grow past it. To enforce it, set CLAUDE_CODE_AUTO_COMPACT_WINDOW=200000 (or the autoCompactWindow setting).
```

Claude Code enforces the 200K limit on its own for every model it recognizes as having a native 1M window, and for model IDs it doesn't recognize it compacts at the window it assumes. The warning appears when other configuration defeats that enforcement:

* The model ID isn't one Claude Code recognizes, such as an [LLM gateway](/docs/en/llm-gateway) alias, and you set [`CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1`](/docs/en/env-vars) or raised the assumed window past 200K with [`CLAUDE_CODE_MAX_CONTEXT_TOKENS`](/docs/en/env-vars). In this case the message also offers `or update to a Claude Code version that recognizes <model>` as a remedy.
* A `context-1m` beta requested through [`ANTHROPIC_BETAS`](/docs/en/env-vars) or the [`--betas`](/docs/en/cli-reference#cli-flags) flag still asks the API for the 1M window on a model that accepts that beta, while nothing compacts the session at 200K

**What to do:**

* Set [`CLAUDE_CODE_AUTO_COMPACT_WINDOW=200000`](/docs/en/env-vars), or the [`autoCompactWindow`](/docs/en/settings-reference#autocompactwindow) setting to `200000`, so auto-compaction compacts at the 200K boundary
* If the message names a model ID this version doesn't recognize, run `claude update`. A version that recognizes the ID as a 1M-context model enforces the limit without further configuration.
* If you want the session to use the model's full window instead, unset `CLAUDE_CODE_DISABLE_1M_CONTEXT`; the warning reports only that the 200K limit isn't enforced

In a [background session](/docs/en/agent-view) or with `--output-format json` or `stream-json`, Claude Code writes the warning to the debug log instead of stderr.

<h3 id="unrecognized-model-id-on-a-request">
  Unrecognized model ID on a request
</h3>

Claude Code sent a request for a model ID that your Claude Code version doesn't recognize, and found no [`modelOverrides`](/docs/en/model-config#override-model-ids-per-version) entry that maps that ID to a model it does recognize. Claude Code still sends the request with the ID as you configured it, and doesn't exit or switch models.

```text theme={null}
[claude-code:unrecognized_model] {"model":"my-proxy-model","query_source":"sdk"}
```

In a script or harness that reads stderr, match on the `[claude-code:unrecognized_model]` prefix. After the prefix and one space, Claude Code writes a one-line JSON object. Claude Code can add fields to it in a later version, so ignore any field you don't expect. It writes at least these two:

* `model`: the model string as you configured it
* `query_source`: the request path that used the model. Claude Code reports `sdk` for a `-p` run and a value that starts with `agent:` for a subagent.

Claude Code writes the line to one of two places, depending on how you run it:

* In [non-interactive mode](/docs/en/headless) with `-p`, Claude Code writes it to stderr under every `--output-format`, so you can parse stdout without filtering the line out
* In an interactive session or a [background session](/docs/en/agent-view), Claude Code writes it to the debug log instead; run with `--debug` to capture it at `~/.claude/debug/<session-id>.txt`

Claude Code writes the line once per model string per process. It writes a separate line for each further unrecognized ID, such as one that a [subagent](/docs/en/sub-agents#choose-a-model) or [background functionality](/docs/en/costs#background-token-usage) uses.

Claude Code doesn't write the line for provider IDs it resolves to a model it recognizes, such as Amazon Bedrock `us.anthropic.claude-...` IDs, Google Cloud's Agent Platform IDs with an `@` version suffix, and Microsoft Foundry deployment names that contain a Claude model ID. Claude Code checks the model behind an Amazon Bedrock [application inference profile ARN](/docs/en/amazon-bedrock#map-each-model-version-to-an-inference-profile) rather than the ARN itself. It writes no line for an ARN it can't resolve, such as a mistyped one.

**What to do:**

* If you set the ID on purpose, such as an [LLM gateway](/docs/en/llm-gateway) alias, add a [`modelOverrides`](/docs/en/model-config#override-model-ids-per-version) entry to your [settings file](/docs/en/settings#where-settings-live) with the ID as its value. Use an Anthropic model ID as the key, not a family alias such as `opus`. For `my-proxy-model` from the example line, add this entry:

  ```json theme={null}
  {
    "modelOverrides": {
      "claude-opus-4-6": "my-proxy-model"
    }
  }
  ```

  Claude Code then treats `my-proxy-model` as `claude-opus-4-6` and stops writing the line.

* If the ID names a model newer than your Claude Code version, run `claude update`

* If the ID is a typo, fix it in whichever of the [places you can set a model](/docs/en/model-config#setting-your-model) or [alias variables](/docs/en/model-config#environment-variables) holds it. If `query_source` starts with `agent:`, fix it where you set the [subagent's model](/docs/en/sub-agents#choose-a-model) instead.

Before v2.1.233, Claude Code wrote no line when it sent a request for a model ID it didn't recognize.

## Responses seem lower quality than usual

If Claude's answers seem less capable than you expect but no error is shown, the cause is usually conversation state rather than the model itself. Claude Code doesn't silently change model versions. It can switch to a fallback model in three specific cases:

* A configured [`--fallback-model`](/docs/en/cli-reference#cli-flags) takes over after an availability error, for that turn only, with a notice in the transcript
* An Amazon Bedrock or Google Cloud's Agent Platform startup check finds your default model unavailable
* [Automatic model fallback](/docs/en/model-config#automatic-model-fallback) on Fable 5 and Opus 5 moves the session to the flagged category's fallback model, when that category has one, and shows a notice in the transcript

The Model selection check below catches the second and third cases; the first appears as a transcript notice rather than a `/model` change. [Model configuration](/docs/en/model-config) explains when each fallback applies.

Check these first:

* **Model selection**: run `/model` to confirm you are on the model you expect. A previous `/model` choice or an `ANTHROPIC_MODEL` environment variable may have you on a smaller model than you intended.
* **Effort level**: run `/effort` to check the current reasoning level and raise it for hard debugging or design work. Defaults vary by model, so check before assuming you are below the maximum. See [Adjust effort level](/docs/en/model-config#adjust-effort-level) for per-model defaults and the `ultrathink` shortcut.
* **Context pressure**: run `/context` to see how full the window is. If it is near capacity, run `/compact` at a natural breakpoint or `/clear` to start fresh. See [Explore the context window](/docs/en/context-window) for how auto-compact affects earlier turns.
* **Stale instructions**: large or outdated `CLAUDE.md` files and MCP tool definitions consume context and can steer responses. The `/doctor` checkup flags oversized memory files and unused extensions, and `/context` shows MCP tool token usage. Before v2.1.205, `/doctor` opened a diagnostics screen that flagged oversized memory files and subagent definitions.

When a response goes wrong, rewinding usually works better than replying with corrections. Press Esc twice or run `/rewind` to step back to before the bad turn, then rephrase the prompt with more specifics. Correcting in-thread keeps the wrong attempt in context, which can anchor later answers to it. See [Checkpointing](/docs/en/checkpointing).

If quality still seems off after checking the above, run `/feedback` and describe what you expected versus what you got. Feedback submitted this way includes the conversation transcript, which is the fastest way for Anthropic to diagnose a real regression. See [Report an error](#report-an-error) if `/feedback` is unavailable in your environment.

If Claude warns about a suspected prompt injection, or refuses a request because of a suspected injection, and the text the warning names is context Claude Code adds to the conversation automatically rather than file or web content, run `claude update` and retry. If the warning repeats after updating, [report it](#report-an-error) rather than pasting the flagged content back into the prompt. Before v2.1.201, Sonnet 5 refused some requests the same way.

## Report an error

For errors from components this page doesn't cover, see the relevant guide:

* MCP server failed to connect or authenticate: [MCP](/docs/en/mcp)
* Hook script failed or blocked a tool: [Debug hooks](/docs/en/hooks#debug-hooks)
* Permission denied or filesystem errors during install: [Troubleshoot installation and login](/docs/en/troubleshoot-install)

If an error is not listed here or the suggested fix does not help:

* Run `/feedback` inside Claude Code to send the transcript and a description to Anthropic. The command also offers to open a prefilled GitHub issue. Sending to Anthropic requires [authentication](/docs/en/authentication). On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and other third-party providers, or when no Anthropic credentials are configured, `/feedback` saves a local archive you can send to your Anthropic account representative instead.
* Run `claude doctor` from your shell for a read-only diagnostic of your installation, or run the `/doctor` checkup inside Claude Code to find and fix setup problems
* Check [status.claude.com](https://status.claude.com) for active incidents
* Search [existing issues](https://github.com/anthropics/claude-code/issues) on GitHub
