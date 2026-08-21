---
title: CLI authentication options
url: https://platform.claude.com/docs/en/cli-sdks-libraries/cli/authentication
description: Authenticate the ant CLI with interactive login, API keys, named profiles, and Workload Identity Federation.
---

The `ant` CLI supports several credential sources. The [Quickstart](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/quickstart#authentication) covers the one-command happy path (`ant auth login`). This page covers every option in full.

## Interactive login

`ant auth login` lets you call the API without creating or managing an API key. It opens a browser-based OAuth flow against the Claude Console and stores the resulting credentials under `$ANTHROPIC_CONFIG_DIR` (see [Configuration directory](https://platform.claude.com/docs/en/manage-claude/wif-reference#configuration-directory) for the OS-specific default). On a remote host or in any environment without a local browser, pass `--no-browser` to print the authorize URL and paste the returned code back into the terminal.

```bash CLI
ant auth login

# On a remote host without a browser:
ant auth login --no-browser

# Bind to a specific workspace and skip the browser picker:
ant auth login --workspace-id wrkspc_01...

# If the named profile you pass with --profile doesn't exist,
# a new named profile will be created with that name.
ant auth login --profile <profile-name>
```

During the browser flow, you select an organization and then a [workspace](https://platform.claude.com/docs/en/manage-claude/workspaces). The issued token is [scoped to that workspace](https://platform.claude.com/docs/en/manage-claude/workspaces#api-keys-and-resource-scoping), so the CLI can only see resources that belong to it. Pass `--workspace-id` to bind directly and skip the picker. To work in more than one workspace, see [Switch between workspaces](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/authentication#switch-between-workspaces).

Interactive login is intended for local development and scripting on your own machine. For non-interactive workloads such as CI, servers, and containers, use [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation) instead.

Login writes credentials to `credentials/<profile>.json`. The first login for a profile also creates `configs/<profile>.json` and sets it as the active profile. To remove stored credentials, run `ant auth logout`, or `ant auth logout --all` to clear every profile.

## Admin access

By default, `ant auth login` requests a workspace-scoped token. To manage the resources documented on the [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api) page, request the `org:admin` scope under a dedicated profile:

```bash CLI
ant auth login --profile admin --scope "org:admin"

# Print a bearer token for Authorization headers:
ant auth print-credentials --profile admin --access-token
```

The `org:admin` scope is granted only to organization members with the admin, owner, or primary owner role. The issued token has organization-wide access, and any workspace binding on the profile does not constrain it. Keep the admin profile separate from your day-to-day profile so routine commands never run with elevated access.

## API key

The CLI also reads your API key from the `ANTHROPIC_API_KEY` environment variable. Get a key from the [Claude Console](https://platform.claude.com/settings/keys).

<Tabs>
  <Tab title="zsh">
    ```bash
    echo 'export ANTHROPIC_API_KEY=sk-ant-api03-...' >> ~/.zshrc
    source ~/.zshrc
    ```
  </Tab>

  <Tab title="bash">
    ```bash
    echo 'export ANTHROPIC_API_KEY=sk-ant-api03-...' >> ~/.bashrc
    source ~/.bashrc
    ```
  </Tab>

  <Tab title="Windows">
    ```powershell
    setx ANTHROPIC_API_KEY "sk-ant-api03-..."
    ```

    Open a new terminal for the change to take effect.
  </Tab>
</Tabs>

To override the key for a single invocation, pass `--api-key`. To point at a different API host, set `ANTHROPIC_BASE_URL` or pass `--base-url`.

## Check authentication status

`ant auth status` prints the credential source the CLI selected (API key environment variable, OAuth login, federation, or profile), the active profile, the workspace the active token is bound to, and the configuration directory paths. Use it to diagnose why a workload picked the wrong credential or workspace.

```bash CLI
ant auth status
```

```text
Active profile:  default
Config dir:      ~/.config/anthropic
Profile config:  ~/.config/anthropic/configs/default.json
Credentials:     ~/.config/anthropic/credentials/default.json

Credentials
  (active) * Profile (user_oauth) [via active_config]       sk-ant-oat01-EXA...
...

Workspace
  (active) * Workspace                                      wrkspc_01... (Engineering)
```

Read the `(active)` rows to see which credential source and workspace won. The command reports status rather than performing a health check, so don't script against the exit status. For the full ordering of credential sources, see [Credential precedence](https://platform.claude.com/docs/en/manage-claude/wif-reference#credential-precedence).

## Switch between workspaces

An interactive-login token is bound to a single workspace. To use the CLI against more than one workspace, log in to each under its own named profile, then switch between them:

```bash CLI
# 1. Create the profile (interactive; pick the other workspace in the
#    browser, or pass --workspace-id to skip the picker):
# ant auth login --profile other-ws

# 2. Make it the default for subsequent commands:
ant profile activate other-ws

# 3. Or select it for a single command without changing the default:
ant --profile other-ws models list
ANTHROPIC_PROFILE=other-ws ant models list
```

Run [`ant auth status`](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/authentication#check-authentication-status) to confirm which profile and workspace are active.

<Note>
  Profiles are only consulted when no API key is set. If `ANTHROPIC_API_KEY` is present in your environment, it overrides every profile and these commands all use whatever workspace that key is scoped to. Unset it before switching profiles.
</Note>

## Manage profiles

The `ant profile` subcommands inspect and edit profile state directly:

```bash CLI
ant profile list
ant profile get --profile other-ws
ant profile set workspace_id wrkspc_01... --profile other-ws
```

The writable keys for `ant profile set` are `workspace_id`, `base_url`, `organization_id`, `scope`, `client_id`, and `console_url`. Setting `workspace_id` records the target workspace in the profile config but does not rebind credentials that were already issued; run `ant auth login` again under that profile to mint a token for the new workspace.

For the profile file schema and the federation block, see [Profile configuration file](https://platform.claude.com/docs/en/manage-claude/wif-reference#profile-configuration-file). For Workload Identity Federation, see the [Authentication overview](https://platform.claude.com/docs/en/manage-claude/authentication) and the [WIF reference](https://platform.claude.com/docs/en/manage-claude/wif-reference).

## Next steps

<CardGroup cols={3}>
  <Card title="Using the CLI" icon="terminal" href="https://platform.claude.com/docs/en/cli-sdks-libraries/cli/using">
    Command structure, output formats, GJSON transforms, and request bodies
  </Card>

  <Card title="CLI scripting and automation" icon="code" href="https://platform.claude.com/docs/en/cli-sdks-libraries/cli/scripting">
    Version-control API resources, scripting patterns, and use from Claude Code
  </Card>

  <Card title="Workload Identity Federation" icon="cloud" href="https://platform.claude.com/docs/en/manage-claude/workload-identity-federation">
    Non-interactive authentication for CI, servers, and containers
  </Card>
</CardGroup>
