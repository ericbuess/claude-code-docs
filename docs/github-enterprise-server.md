> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code with GitHub Enterprise Server

> Connect Claude Code to your self-hosted GitHub Enterprise Server instance for web sessions, code review, and plugin marketplaces.

<Note>
  GitHub Enterprise Server support is available for Team and Enterprise plans.
</Note>

GitHub Enterprise Server (GHES) support lets your organization use Claude Code with repositories hosted on your self-managed GitHub instance instead of github.com. Once an Owner connects your GHES instance, developers can run web sessions and get automated code reviews without any per-repository configuration. Plugin marketplaces hosted on your instance are also supported; credential requirements vary by surface, as described in [Plugin marketplaces on GHES](#plugin-marketplaces-on-ghes).

For repositories on github.com, see [Claude Code on the web](/docs/en/claude-code-on-the-web) and [Code Review](/docs/en/code-review). To run Claude in your own CI infrastructure, see [GitHub Actions](/docs/en/github-actions).

## What works with GitHub Enterprise Server

The table below shows which Claude Code features support GHES and any differences from github.com behavior.

| Feature                | GHES support    | Notes                                                                                                                          |
| :--------------------- | :-------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| Claude Code on the web | ✅ Supported     | An Owner connects the GHES instance once; developers use `claude --cloud` or [claude.ai/code](https://claude.ai/code) as usual |
| Code Review            | ✅ Supported     | Same automated PR reviews as github.com                                                                                        |
| Claude Security        | ✅ Supported     | Available in public beta for Enterprise plans at [claude.ai/security](https://claude.ai/security)                              |
| Teleport sessions      | ✅ Supported     | Move sessions between web and terminal with `--teleport`                                                                       |
| Plugin marketplaces    | ✅ Supported     | Credential requirements differ by surface. See [Plugin marketplaces on GHES](#plugin-marketplaces-on-ghes)                     |
| Contribution metrics   | ✅ Supported     | Delivered via webhooks to the [analytics dashboard](/docs/en/analytics)                                                             |
| GitHub Actions         | ✅ Supported     | Requires manual workflow setup; `/install-github-app` is github.com only                                                       |
| GitHub MCP server      | ❌ Not supported | The GitHub MCP server does not work with GHES instances                                                                        |

## Admin setup

An Owner connects your GHES instance to Claude Code once. After that, developers in your organization can use GHES repositories without any additional configuration. You need the Owner or Primary Owner role in your Claude organization and permission to create GitHub Apps on your GHES instance.

The guided setup generates a GitHub App manifest and redirects you to your GHES instance to create the app in one click. If your environment blocks the redirect flow, an [alternative manual setup](#manual-setup) is available.

<Steps>
  <Step title="Open Claude Code admin settings">
    Go to [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) and find the GitHub Enterprise Server section.
  </Step>

  <Step title="Start the guided setup">
    Click **Connect**. Enter a display name for the connection and your GHES hostname, for example `github.example.com`. If your GHES instance uses a self-signed or private certificate authority, paste the CA certificate in the optional field.
  </Step>

  <Step title="Create the GitHub App">
    Click **Continue to GitHub Enterprise**. Your browser redirects to your GHES instance with a pre-filled app manifest. Review the configuration and click **Create GitHub App**. GHES redirects you back to Claude with the app credentials stored automatically.
  </Step>

  <Step title="Install the app on your repositories">
    From the GitHub App page on your GHES instance, install the app on the repositories or organizations you want Claude to access. You can start with a subset and add more later.
  </Step>

  <Step title="Enable features">
    Return to [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) and enable [Code Review](/docs/en/code-review#set-up-code-review), Claude Security, and [contribution metrics](/docs/en/analytics#enable-contribution-metrics) for your GHES repositories using the same configuration as github.com.
  </Step>
</Steps>

### GitHub App permissions

The manifest configures the GitHub App with the permissions and webhook events Claude needs across web sessions, Code Review, Claude Security, and contribution metrics:

| Permission       | Access         | Used for                                    |
| :--------------- | :------------- | :------------------------------------------ |
| Contents         | Read and write | Cloning repositories and pushing branches   |
| Pull requests    | Read and write | Creating PRs and posting review comments    |
| Issues           | Read and write | Responding to issue mentions                |
| Checks           | Read and write | Posting Code Review check runs              |
| Actions          | Read           | Reading CI status for auto-fix              |
| Repository hooks | Read and write | Receiving webhooks for contribution metrics |
| Metadata         | Read           | Required by GitHub for all apps             |

The app subscribes to `pull_request`, `issue_comment`, `pull_request_review_comment`, `pull_request_review`, and `check_run` events.

### Manual setup

If the guided redirect flow is blocked by your network configuration, click **Add manually** instead of Connect. Create a GitHub App on your GHES instance with the [permissions and events above](#github-app-permissions), then enter the app credentials in the form: hostname, OAuth client ID and secret, GitHub App ID, client ID, client secret, webhook secret, and private key.

### Network requirements

Your GHES instance must be reachable from Anthropic infrastructure so Claude can clone repositories and post review comments. If your GHES instance is behind a firewall, allowlist the [Anthropic API IP addresses](https://platform.claude.com/docs/en/api/ip-addresses).

## Developer workflow

Once an Owner has connected the GHES instance, no developer-side configuration is needed. Claude Code detects your GHES hostname automatically from the git remote in your working directory.

Clone a repository from your GHES instance as you normally would, replacing `github.example.com` and the repository path with your GHES hostname and repository:

```bash theme={null}
git clone git@github.example.com:platform/api-service.git
cd api-service
```

Then start a web session. Claude detects the GHES host from your git remote and routes the session through your organization's configured instance:

```bash theme={null}
claude --cloud "Add retry logic to the payment webhook handler"
```

The session runs on Anthropic infrastructure, clones your repository from GHES, and pushes changes back to a branch. Monitor progress with `/tasks` or at [claude.ai/code](https://claude.ai/code). See [Claude Code on the web](/docs/en/claude-code-on-the-web) for the full cloud session workflow including diff review, auto-fix, and routines.

### Teleport sessions to your terminal

Pull a web session into your local terminal with `claude --teleport`. Teleport verifies you're in a checkout of the same GHES repository before fetching the branch and loading the session history. See [teleport requirements](/docs/en/claude-code-on-the-web#teleport-requirements) for details.

## Plugin marketplaces on GHES

Host plugin marketplaces on your GHES instance to distribute internal tooling across your organization. The marketplace structure is identical to github.com-hosted marketplaces, but installation works differently depending on where you add the marketplace, and credentials differ across surfaces:

| Surface                                     | How installation works                                                                                                                                                                                                               | What each user needs                                                                                                                                                                                      |
| :------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude Code CLI and desktop                 | Claude Code clones the marketplace repository using the machine's existing git credentials                                                                                                                                           | Git access to your GHES host from their machine                                                                                                                                                           |
| Managed settings (`extraKnownMarketplaces`) | Claude Code registers the entry and clones the repository using the machine's existing git credentials                                                                                                                               | Git access to your GHES host from their machine                                                                                                                                                           |
| claude.ai organization plugin settings      | An Owner selects the GHES instance as the source; Anthropic's backend fetches and syncs the repository using the GitHub App from [admin setup](#admin-setup)                                                                         | Nothing per user once added. The Owner adding it needs their own GitHub Enterprise account connected as an access check, and the GitHub App must be installed on the marketplace repository               |
| claude.ai user settings                     | Anthropic's backend fetches the repository using the submitting user's GitHub Enterprise connection                                                                                                                                  | Their own GitHub Enterprise account connected to Claude                                                                                                                                                   |
| Claude Code on the web                      | Cloud sessions clone marketplaces inside the session sandbox. The sandbox can reach your GHES instance only when the session's repository is on that same instance, and its git credentials are scoped to the session's repositories | Not reliable for GHES-hosted marketplaces: a different host than the session's repository is not reachable, and even same-instance installs can fail. Use the CLI, managed settings, or claude.ai instead |

<Warning>
  GitHub Enterprise connections on claude.ai are per user when a marketplace is added from user settings. The [admin setup](#admin-setup) connects your GHES instance to your organization, but it does not connect individual user accounts: each user who adds a GHES marketplace from their own settings must first connect their own GitHub Enterprise account, and one user's connection, including the Owner's, does not cover anyone else. Marketplaces added by an Owner in the organization plugin settings do not put this requirement on users, because ongoing fetches use the organization's GitHub App. The Owner adding the marketplace still needs their own GitHub Enterprise account connected at add time.
</Warning>

### Add a GHES marketplace

The `owner/repo` shorthand always resolves to github.com. For GHES-hosted marketplaces, use the full git URL, replacing `github.example.com` and the repository path with your own. HTTPS URLs are recommended:

```bash theme={null}
/plugin marketplace add https://github.example.com/platform/claude-plugins.git
```

SSH URLs work if the machine already trusts your GHES host:

```bash theme={null}
/plugin marketplace add git@github.example.com:platform/claude-plugins.git
```

Claude Code runs git non-interactively and rejects SSH connections to hosts that are not in the machine's `known_hosts` file. An HTTPS URL with a git credential helper avoids the `known_hosts` requirement.

See [Create and distribute a plugin marketplace](/docs/en/plugin-marketplaces) for the full guide to building marketplaces.

### Pre-register GHES marketplaces with managed settings

The `extraKnownMarketplaces` setting pre-registers a marketplace so developers get it without manual setup. It works from [any settings file](/docs/en/settings#extraknownmarketplaces), including a repository's `.claude/settings.json`; managed settings deliver it organization-wide:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "internal-tools": {
      "source": {
        "source": "git",
        "url": "https://github.example.com/platform/claude-plugins.git"
      }
    }
  }
}
```

Claude Code installs these marketplaces locally: it registers each entry and clones the repository with the machine's existing git credentials. This path does not go through claude.ai, so the per-user GitHub Enterprise connection is not required. For a successful rollout:

* **Use a full git URL.** The `owner/repo` shorthand always resolves to github.com and cannot reference a GHES host.
* **Prefer HTTPS URLs.** SSH clones fail on machines that do not already trust your GHES host key. An HTTPS URL with your organization's standard git credential helper works on any machine with credentials configured.
* **Confirm each machine can clone from your GHES host.** If a machine lacks credentials, the marketplace is registered but never installed, and its plugins report as not found instead of prompting for credentials.
* **Confirm the setting reaches each machine.** A managed settings file only takes effect on machines it's deployed to, for example through your device management system. See [managed settings](/docs/en/settings#settings-files) for file locations.

### Allowlist GHES marketplaces in managed settings

If your organization uses [managed settings](/docs/en/settings) to restrict which marketplaces developers can add, use the `hostPattern` source type to allow all marketplaces from your GHES instance without enumerating each repository:

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

See the [strictKnownMarketplaces](/docs/en/settings#strictknownmarketplaces) and [extraKnownMarketplaces](/docs/en/settings#extraknownmarketplaces) settings reference for the complete schema.

## Limitations

A few features behave differently on GHES than on github.com. The [feature table](#what-works-with-github-enterprise-server) summarizes support; this section covers the workarounds.

* **`/install-github-app` command**: follow the [admin setup](#admin-setup) flow on claude.ai instead. If you also want GitHub Actions workflows on GHES, adapt the [example workflow](https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml) manually.
* **GitHub MCP server**: use the `gh` CLI configured for your GHES host instead. Run `gh auth login --hostname github.example.com` to authenticate, then Claude can use `gh` commands in sessions.

## Troubleshooting

### Web session fails to clone repository

If `claude --cloud` fails with a clone error, verify that an Owner has completed setup for your GHES instance and that the GitHub App is installed on the repository you're working in. Ask the Owner who connected the instance to confirm that the hostname registered in Claude settings matches the hostname in your git remote.

### Marketplace add fails with a policy error

If `/plugin marketplace add` is blocked for your GHES URL, your organization has restricted marketplace sources. Ask your admin to add a `hostPattern` entry for your GHES hostname in [managed settings](#allowlist-ghes-marketplaces-in-managed-settings).

### Marketplace add on claude.ai fails with a GitHub access error

If adding a GHES marketplace from your user settings fails with a generic error like "Marketplace couldn't be added", check your GitHub Enterprise connection first. This is what appears when your own GitHub Enterprise account is not connected to Claude, even if your organization's GHES instance is configured and other users are connected. The dialog does not point to the GitHub Enterprise connect flow, and the "Connect to GitHub" option on the Browse tab signs in to github.com, which does not grant access to GHES repositories.

To connect your GitHub Enterprise account: the repository picker on [claude.ai/code](https://claude.ai/code) offers a connect option for each configured GHES instance, and Owners can also connect from the GitHub Enterprise section of the [Claude Code admin settings](https://claude.ai/admin-settings/claude-code). Then add the marketplace again. Alternatively, ask an Owner to add the marketplace in the organization plugin settings, which removes the per-user connection requirement.

On other claude.ai surfaces, a "Repository not found. If it's private, GitHub access is required" error on a GHES marketplace usually indicates the same missing connection. Connect your GitHub Enterprise account through one of the paths above, then try again.

### GHES instance not reachable

If reviews or web sessions time out, your GHES instance may not be reachable from Anthropic infrastructure. Confirm your firewall allows inbound connections from the [Anthropic API IP addresses](https://platform.claude.com/docs/en/api/ip-addresses).

### Session start fails with `Unable to get organization UUID`

Web sessions require a Team or Enterprise organization. Sign in with `/login` using your organization account. If you authenticate with an API key instead, web sessions fail earlier with a message asking you to run `/login`.

## Related resources

These pages cover the features referenced throughout this guide in more depth:

* [Claude Code on the web](/docs/en/claude-code-on-the-web): run Claude Code sessions on cloud infrastructure
* [Code Review](/docs/en/code-review): automated PR reviews
* [Plugin marketplaces](/docs/en/plugin-marketplaces): build and distribute plugin catalogs
* [Analytics](/docs/en/analytics): track usage and contribution metrics
* [Managed settings](/docs/en/settings): organization-wide policy configuration
* [Network configuration](/docs/en/network-config): firewall and IP allowlist requirements
