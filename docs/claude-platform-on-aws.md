> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code on Claude Platform on AWS

> Configure Claude Code to use the Anthropic-operated Claude API with AWS authentication, IAM access control, and AWS Marketplace billing.

Claude Platform on AWS is the Anthropic-operated Claude API with AWS authentication, IAM access control, and AWS Marketplace billing. Requests reach Anthropic's API directly, so you get the same models and features as the [Claude API](https://platform.claude.com/docs) on the same release schedule. You authenticate with AWS credentials or a workspace API key, and you pay through AWS Marketplace.

Use this guide to point Claude Code at a workspace you've already provisioned through Claude Platform on AWS. For the AWS subscription and workspace setup that comes before this, see the [Claude Platform on AWS documentation](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws).

<Note>
  Subscribing through AWS Marketplace provisions a new Anthropic organization tied to your AWS account. This organization is separate from any organization you already have with Anthropic, and credentials don't transfer between them. Use the workspace ID and API keys from the AWS-linked organization, not from a pre-existing Claude Console account.
</Note>

## Prerequisites

Before configuring Claude Code, you need:

* An active Claude Platform on AWS subscription through AWS Marketplace
* A workspace in your AWS-linked Anthropic organization, with its workspace ID
* An IAM principal with permission to invoke the Anthropic service, or an API key scoped to the workspace
* AWS credentials in your environment, in `~/.aws/credentials`, or from an attached IAM role if you want SigV4 authentication. The AWS CLI is required only for the SSO login flow.

## Setup

### 1. Configure AWS credentials

Claude Code supports two authentication methods for Claude Platform on AWS. Choose the method that fits how your team manages access.

**Option A: AWS credentials with SigV4**

Claude Code signs requests with SigV4 using the standard AWS credential chain: environment variables, shared credentials in `~/.aws/credentials`, IAM roles, AWS SSO sessions, and any other sources the AWS SDK supports.

For local use, log in with the AWS CLI before starting Claude Code. The example below uses an SSO profile, but any method that produces credentials in the standard locations works.

```bash theme={null}
aws sso login --profile my-profile
export AWS_PROFILE=my-profile
```

For CI and automation, give the runner an IAM role with permission to invoke the Anthropic service and set `AWS_REGION`. The credential chain picks the role up automatically.

If your SSO credentials expire mid-session, configure [`awsAuthRefresh`](/en/amazon-bedrock#advanced-credential-configuration) so Claude Code re-runs your login command and retries instead of failing. Add the command to your `settings.json`:

```json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile my-profile"
}
```

**Option B: Workspace API key**

A workspace API key is a long-lived secret, useful when you don't want to manage federated AWS credentials. Generate one in the AWS Console under **Claude Platform on AWS → API keys** and set it as `ANTHROPIC_AWS_API_KEY`:

```bash theme={null}
export ANTHROPIC_AWS_API_KEY=sk-ant-xxxxx
```

The key is sent as `x-api-key` and takes precedence over SigV4, so any AWS credentials in your environment are ignored. API keys from a separate Claude Console organization won't work here.

Treat workspace API keys like any other production credential. The [user settings file](/en/settings) `env` block is a convenient way to scope the key to your machine without exporting it globally.

<Note>
  The `/login` and `/logout` commands don't change Claude Platform on AWS authentication. Authentication runs through your AWS credentials or workspace API key, not through a Claude.ai subscription.
</Note>

### 2. Configure Claude Code

Set the environment variables that route Claude Code through Claude Platform on AWS instead of the default Anthropic API.

```bash theme={null}
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export AWS_REGION=us-east-1
```

`ANTHROPIC_AWS_WORKSPACE_ID` is required and is sent on every request as the `anthropic-workspace-id` header. The base URL is computed from `AWS_REGION` as `https://aws-external-anthropic.{region}.api.aws`. To override the URL directly, set `ANTHROPIC_AWS_BASE_URL`.

Claude Platform on AWS is opt-in even when AWS credentials are present in your environment. Bedrock and Foundry take precedence in provider routing, so unset `CLAUDE_CODE_USE_BEDROCK` and `CLAUDE_CODE_USE_FOUNDRY` if they're set.

### 3. Pin model versions

Claude Platform on AWS uses the same model IDs as the direct Claude API. The default aliases `fable`, `opus`, `sonnet`, and `haiku` resolve to Claude Code's built-in defaults for Claude Platform on AWS, which can lag the newest release. Without `ANTHROPIC_DEFAULT_OPUS_MODEL`, the `opus` alias resolves to Opus 4.7.

If you deploy Claude Code to a team, pin the model IDs explicitly so a new release doesn't move everyone at once:

```bash theme={null}
export ANTHROPIC_DEFAULT_FABLE_MODEL=claude-fable-5
export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-7
export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-6
export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5
```

For the full list of model IDs and aliases, see [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). For other model-related variables, see [Model configuration](/en/model-config).

[Prompt caching](/en/prompt-caching) is enabled automatically. To request a 1-hour cache TTL instead of the 5-minute default, set `ENABLE_PROMPT_CACHING_1H=1`. The API bills 1-hour cache writes at a higher rate. See [prompt caching pricing](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing) for the rates.

## Use the Agent SDK

The [Agent SDK](/en/agent-sdk/overview) reads the same environment variables as the CLI, so any program that spawns the Claude Code subprocess can target Claude Platform on AWS by exporting `CLAUDE_CODE_USE_ANTHROPIC_AWS`, `ANTHROPIC_AWS_WORKSPACE_ID`, and either `ANTHROPIC_AWS_API_KEY` or AWS credentials before the call.

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

process.env.CLAUDE_CODE_USE_ANTHROPIC_AWS = "1";
process.env.ANTHROPIC_AWS_WORKSPACE_ID = "wrkspc_01ABCDEFGHIJKLMN";
process.env.AWS_REGION = "us-east-1";

for await (const msg of query({ prompt: "What's in this repo?" })) {
  console.log(msg);
}
```

This example relies on the ambient AWS credential chain for SigV4. To authenticate with a workspace API key instead, set `ANTHROPIC_AWS_API_KEY` the same way. For the broader Agent SDK surface, see [Agent SDK overview](/en/agent-sdk/overview).

## Route through a corporate proxy

To route traffic through a proxy or [LLM gateway](/en/llm-gateway), set `ANTHROPIC_AWS_BASE_URL` to the proxy's address. Claude Code sends requests to that URL with the same workspace and authentication headers, so any gateway that forwards them unchanged works.

```bash theme={null}
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export ANTHROPIC_AWS_BASE_URL=https://anthropic-proxy.example.com
```

If your gateway signs requests itself, set `CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH=1` so Claude Code sends unsigned requests and lets the gateway add SigV4 headers before forwarding to AWS. If the gateway requires its own token, set it in `ANTHROPIC_AUTH_TOKEN`.

```bash theme={null}
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
export CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH=1
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export ANTHROPIC_AWS_BASE_URL=https://anthropic-proxy.example.com
```

## Troubleshooting

Run `/status` to see the resolved provider and any explicitly configured workspace ID, region, base URL override, and auth-skip setting. This is the fastest way to confirm Claude Code is targeting Claude Platform on AWS at all.

### `403 Forbidden` or `AccessDenied` on every request

The IAM principal Claude Code resolved likely lacks permission to invoke the Anthropic service in your workspace. Check the role attached to your AWS profile or the runner that started Claude Code, and verify it has the `aws-external-anthropic` actions documented in the [IAM action reference](https://platform.claude.com/docs/en/api/claude-platform-on-aws-iam-actions).

If you set `ANTHROPIC_AWS_API_KEY`, the key takes precedence over SigV4 and a stale key produces the same error. Regenerate the key in the AWS Console under **Claude Platform on AWS → API keys** or unset the variable to fall back to your AWS credentials.

### Requests fail with a missing-workspace error

`ANTHROPIC_AWS_WORKSPACE_ID` is likely unset or empty. Every Claude Platform on AWS request must include the workspace ID. It is not implied by your AWS credentials. Find the ID under **Workspaces** on the AWS Console service page and export it before starting Claude Code.

### Requests still go to `api.anthropic.com`

`CLAUDE_CODE_USE_ANTHROPIC_AWS` is likely unset or set to a value that doesn't parse as truthy. Set it to `1` and run `/status` to confirm the resolved provider. If `CLAUDE_CODE_USE_BEDROCK` or `CLAUDE_CODE_USE_FOUNDRY` is also set, those take precedence over Claude Platform on AWS.

## Additional resources

The Claude Platform on AWS subscription, workspace, and IAM setup that comes before configuring Claude Code is covered in the platform documentation:

* [Claude Platform on AWS overview](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws): subscription, workspace setup, and product reference
* [IAM action reference](https://platform.claude.com/docs/en/api/claude-platform-on-aws-iam-actions): permissions and managed policies
