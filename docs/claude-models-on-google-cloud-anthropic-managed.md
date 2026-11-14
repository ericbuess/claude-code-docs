> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code with Claude Models on Google Cloud (Anthropic managed)

> Configure Claude Code to use the Claude API that Anthropic runs through your Google Cloud project, with Google Cloud credentials, IAM, and Marketplace billing.

Claude Models on Google Cloud (Anthropic managed) is the Claude API, run by Anthropic and reached through your Google Cloud project. To use it from Claude Code, sign in to Google Cloud and set three environment variables.

> [!NOTE]
>
> Google Cloud also offers Claude through Google Cloud's Agent Platform, formerly Vertex AI, which Google manages. If you use Agent Platform, follow [Claude Code on Google Cloud's Agent Platform](https://code.claude.com/docs/en/google-vertex-ai.md) instead. To find out which one you use, see [Which offering are you using?](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/overview#which-offering-are-you-using)

Before you start, [install Claude Code](https://code.claude.com/docs/en/setup.md#install-claude-code) v2.1.307 or later. To check your version, run `claude --version` in your shell. To update, run `claude update`.

## Prerequisites

* A Google Cloud project where the [account setup](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#set-up-your-account) is complete
* The `roles/claude.user` [IAM role](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#iam-roles) on that project, for each Google account or service account that runs Claude Code
* Your project ID and your [workspace ID](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id), which starts with `wrkspc_`
* The [gcloud CLI](https://cloud.google.com/sdk/docs/install), if you sign in with a Google account rather than with a service account key file

## Set up Claude Code

**1. Create Application Default Credentials**

> [tab] Google account
>
> Run this command in your shell, and sign in with the Google account that has the `roles/claude.user` role:
>
> ```bash theme={null}
> gcloud auth application-default login
> ```
>
> Run it even if you've already run `gcloud auth login`.
>
> If `GOOGLE_APPLICATION_CREDENTIALS` is set, unset it. While that variable is set, Claude Code uses the file it names and ignores the credentials that the command saves.

> [tab] Service account key file
>
> In the shell or CI job that runs Claude Code, set `GOOGLE_APPLICATION_CREDENTIALS` to the path of a [service account key file](https://docs.cloud.google.com/iam/docs/keys-create-delete). For other credential sources, see [how to authenticate](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#authentication).

**2. Add the variables to your settings**

Add three variables to the `env` block of your [user settings file](https://code.claude.com/docs/en/settings.md), `~/.claude/settings.json`. If the file doesn't exist, create it with this content:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_USE_ANTHROPIC_GOOGLE_CLOUD": "1",
    "ANTHROPIC_GOOGLE_CLOUD_PROJECT": "my-project-id",
    "ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID": "wrkspc_01ABCDEFGHIJKLMN"
  }
}
```

Use your own project ID and [workspace ID](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id) in place of `my-project-id` and the `wrkspc_` value. To configure a single shell or a CI job instead, set the same three variables in that environment.

You don't need to log in to an Anthropic account, or to log out of one.

**3. Start Claude Code and check the provider**

Run `claude` in your shell, then run `/status` at the Claude Code prompt. The `API provider` line contains `on Google Cloud`, and the lines after it show your `Workspace ID`, `GCP project`, and `GCP location`. To print the same lines from your shell or a CI job, run [`claude auth status --text`](https://code.claude.com/docs/en/cli-reference).

If you see `on Google Cloud`, send a prompt, or run `claude -p "hello"` in a CI job. A reply confirms that your credentials and IAM role work. If you don't see it, or Claude Code shows an error, [troubleshoot the provider setup](#troubleshooting).

### Set up Claude Code for a team

Put the `env` block from step 2 of [Set up Claude Code](#set-up-claude-code) in a [managed settings](https://code.claude.com/docs/en/managed-settings.md) file on each developer's machine. Grant each developer the `roles/claude.user` role on the project, and have each one run `gcloud auth application-default login` on their own machine.

## Pin model versions

If you deploy to a team, [pin the model IDs](https://code.claude.com/docs/en/model-config.md#pin-models-for-third-party-deployments), so a Claude Code update doesn't move everyone to a newer model at once. Add these variables to the `env` block that holds the three variables from [Set up Claude Code](#set-up-claude-code):

```json theme={null}
{
  "env": {
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-5-5",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-5-5",
    "ANTHROPIC_DEFAULT_FABLE_MODEL": "claude-fable-5-1",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-4-5-20251001"
  }
}
```

Use the Claude API model IDs that you want from [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) in place of the example values.

## Environment variables

| Variable | Required | Description |
| - | - | - |
| `CLAUDE_CODE_USE_ANTHROPIC_GOOGLE_CLOUD` | Yes | Set to `1` to send model requests to Claude Models on Google Cloud (Anthropic managed) |
| `ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID` | Yes, unless you set `ANTHROPIC_GOOGLE_CLOUD_BASE_URL` | Your workspace ID |
| `ANTHROPIC_GOOGLE_CLOUD_PROJECT` | Recommended | Your Google Cloud project ID. Without it, Claude Code uses `GOOGLE_CLOUD_PROJECT` |
| `ANTHROPIC_GOOGLE_CLOUD_LOCATION` | No | The [location](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#project-location-and-workspace-resolution) in the request URL. Defaults to `global` |
| `ANTHROPIC_GOOGLE_CLOUD_BASE_URL` | No | Replaces the base URL that Claude Code builds from the project, location, and workspace ID, for example with the address of an [LLM gateway](https://code.claude.com/docs/en/llm-gateway). Claude Code appends the API path, such as `/v1/messages` |
| `CLAUDE_CODE_SKIP_ANTHROPIC_GOOGLE_CLOUD_AUTH` | No | Set to `1` when a gateway attaches the Google credentials itself, so that Claude Code sends no Google access token |

## Claude Code features that aren't available

With Claude Models on Google Cloud (Anthropic managed), the features you can't use include:

* [Fast mode](https://code.claude.com/docs/en/fast-mode.md): you can't turn it on with `/fast` or the `fastMode` setting
* [Remote Control](https://code.claude.com/docs/en/remote-control.md) and [cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web.md)
* [MCP connectors from claude.ai](https://code.claude.com/docs/en/mcp.md#use-mcp-servers-from-claude-ai)
* [Channels](https://code.claude.com/docs/en/channels.md)
* The [`/design-sync` and `/import` commands](https://code.claude.com/docs/en/commands#all-commands)
* [Server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md). To enforce settings for your team, use [managed settings](https://code.claude.com/docs/en/managed-settings.md) on each machine instead

To see other features that are unavailable or partially supported, select the **Google Cloud (Anthropic managed)** tab in the [feature availability summary](https://code.claude.com/docs/en/feature-availability.md#summary-by-provider).

## Troubleshooting

If Claude Code asks you to log in, or the `API provider` line in `/status` doesn't contain `on Google Cloud`:

* Make sure `CLAUDE_CODE_USE_ANTHROPIC_GOOGLE_CLOUD` is `1`
* Make sure `claude --version` prints 2.1.307 or later
* Remove `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_FOUNDRY`, and `CLAUDE_CODE_USE_ANTHROPIC_AWS` from your shell and your [settings files](https://code.claude.com/docs/en/settings.md#find-or-create-your-settings-files)

`CLAUDE_CODE_USE_VERTEX` can stay set. After you change a variable, restart Claude Code. If `/status` doesn't show the change, see [A value you set is ignored](https://code.claude.com/docs/en/settings.md#a-value-you-set-is-ignored).

### `No workspace ID found`

Set `ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID` to your [workspace ID](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#find-your-workspace-id), then restart Claude Code. Ignore the `workspaceId` constructor option that the message mentions: it's for people who call Anthropic's SDK from their own code.

### `No project was given`

Set `ANTHROPIC_GOOGLE_CLOUD_PROJECT` to your Google Cloud project ID, then restart Claude Code.

### `Could not load Google Cloud credentials`

Repeat step 1 of [Set up Claude Code](#set-up-claude-code), with a new key if you use a service account key file.

### `Google Cloud credentials expired or invalid`

If the message tells you to refresh your Google Cloud credentials, repeat step 1 of [Set up Claude Code](#set-up-claude-code). With a service account key file, use a new key.

### `Google Cloud authentication failed`

Follow the steps for [`Google Cloud credentials expired or invalid`](#google-cloud-credentials-expired-or-invalid). If that doesn't clear the error:

* **Project**: in `/status`, make sure the `GCP project` line names your project. If it names another project, or there's no such line, follow [`No project was given`](#no-project-was-given)
* **Workspace**: in `/status`, make sure the `Workspace ID` line shows your workspace ID. If it shows another, follow [`No workspace ID found`](#no-workspace-id-found)
* **IAM role**: make sure the Google account or service account that runs Claude Code has `roles/claude.user` or `roles/claude.admin` on the project in the `GCP project` line. To grant the role, use [the service's grant command](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#before-making-api-calls), or ask a project admin to grant it
* **Service**: make sure the `claude.googleapis.com` service is enabled on the project in the `GCP project` line. To enable it, follow [the service's account setup steps](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed#set-up-your-account), or ask a project admin to enable it

## Related resources

* [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed): account setup, IAM roles, billing, data retention, and feature support
* [Enterprise deployment overview](https://code.claude.com/docs/en/third-party-integrations.md): the other ways to deploy Claude Code, and proxy and gateway setup
* [Model configuration](https://code.claude.com/docs/en/model-config.md): model aliases, pinning a model version, and restricting which models users can select
