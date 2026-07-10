# Manage tunnels in the Console

Create tunnels, register CA certificates, retrieve the tunnel token, and attach tunneled MCP servers to agents from the Claude Console.

---

<Note>
  MCP tunnels are in research preview. [Request access](https://claude.com/form/claude-managed-agents) to try them.
</Note>

This page covers the Console side of an MCP tunnels deployment: creating a tunnel, registering your CA certificate, retrieving the tunnel token, and attaching the [upstream MCP servers](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) to an agent. [Deploy MCP tunnels with Helm](/docs/en/agents-and-tools/mcp-tunnels/deploy-helm) and [Deploy MCP tunnels with Docker Compose](/docs/en/agents-and-tools/mcp-tunnels/deploy-compose) cover running the [tunnel stack](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) inside your network.

## Prerequisites

* **One or more MCP servers** running in your private network. The tunnel routes traffic to them; it does not host them. See [Remote MCP servers](/docs/en/agents-and-tools/remote-mcp-servers) for examples you can deploy.

* **A Console role with the Manage tunnels permission**, so you can create and archive tunnels, rotate the token, and manage certificates. Organization admins and owners have it by default; custom roles and per-account grants can also include it. Roles without it have read-only access to the **MCP tunnels** page and tunnel details.

* **A way for your stack to authenticate to the Tunnels API.** Choose one:

  * **[Programmatic access](/docs/en/agents-and-tools/mcp-tunnels/concepts#credential-provisioning) (recommended).** Set up [Workload Identity Federation](/docs/en/manage-claude/workload-identity-federation) during tunnel creation so your stack mints short-lived API tokens from your identity provider, fetches the tunnel token, and generates and registers a CA certificate automatically. Requires permission to manage federation rules, a registered OIDC issuer, and a federation rule with the `workspace:manage_tunnels` scope.
  * **[Manual](/docs/en/agents-and-tools/mcp-tunnels/concepts#credential-provisioning).** Skip programmatic access. After creating the tunnel, [get the tunnel token](#get-the-connection-details), generate and [register a CA certificate](#add-a-ca-certificate) yourself, and supply the token and your server certificate to your tunnel stack as secrets.

## Create a tunnel

<Steps>
  <Step title="Open the MCP tunnels page">
    In the Console sidebar, go to **Manage > MCP tunnels**. Tunnels are workspace-scoped; the new tunnel belongs to the workspace currently selected in the Console, so switch workspaces first if you want it elsewhere.
  </Step>

  <Step title="Name the tunnel">
    Click **New tunnel** and enter a name in the **Create tunnel** dialog. The name is required and identifies the tunnel in the list, on the detail page, and in the agent MCP server picker. A domain of the form `abcd1234.tunnel.anthropic.com` is assigned automatically.
  </Step>

  <Step title="Optionally set up programmatic access">
    If your role can manage federation rules, a **Set up programmatic access** toggle appears (off by default). If not, the Console shows a notice in its place and your tunnel stack uses the manual flow instead. The rest of the create flow is the same either way.

    Programmatic access relies on [Workload Identity Federation](/docs/en/manage-claude/workload-identity-federation); read that page first if federation issuers, rules, and service accounts are unfamiliar. To turn the toggle on you need:

    1. **A registered OIDC issuer** for the identity provider your stack presents tokens from (such as a Kubernetes cluster, AWS IAM, Google Cloud, or GitHub Actions). Register one under **Settings > Workload identity > Issuers** if your organization doesn't have one.
    2. **A federation rule with the `workspace:manage_tunnels` scope.** Turning on the toggle reveals a **Federation rule** picker. Choose an existing rule with that scope, or click **Create federation rule** to create one inline.
    3. **The rule's service account added to this workspace.** The Tunnels API authorizes against the service account's workspace memberships. If you're creating the tunnel in a workspace other than the organization's default, add the service account under **Settings > Workspaces** and pass the workspace ID at deploy time (`api.wif.workspaceId` for Helm, `ANTHROPIC_WORKSPACE_ID` for Compose).

    Skipping this step is fully supported; both deploy guides have a **Without programmatic access** tab.
  </Step>

  <Step title="Create the tunnel">
    Click **Create tunnel**. The Console provisions the tunnel and opens the detail page.
  </Step>

  <Step title="Record the deployment identifiers">
    Both deploy paths need:

    * The **tunnel ID** (`tnl_...`), shown on the tunnel detail page.
    * The **tunnel domain** (`abcd1234.tunnel.anthropic.com`), shown on the tunnel detail page. Used as the proxy's `tunnel_domain` and in the server certificate's SAN.

    What else you need depends on the [credential-provisioning mode](/docs/en/agents-and-tools/mcp-tunnels/concepts#credential-provisioning):

    | With programmatic access                                                                                                                                                   | Without programmatic access                                                                                                                                                 |
    | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | The **federation rule ID** (`fdrl_...`) of the rule you selected. The rule is org-level, not stored on the tunnel; find it under **Settings > Workload identity > Rules**. | The **tunnel token**, revealed with the eye icon next to **Token** on the detail page. Treat it as a secret. See [Get the connection details](#get-the-connection-details). |
    | The **organization ID** (a UUID), shown under **Settings > Organization**.                                                                                                 | A **CA certificate** that you generate and [register on the tunnel](#add-a-ca-certificate).                                                                                 |

    With programmatic access, your stack fetches the tunnel token through the Tunnels API, generates the CA and server certificate locally (the private key never leaves your environment), and registers only the CA's public certificate with Anthropic. You're still responsible for securing the private keys and renewing the server certificate before it expires.
  </Step>
</Steps>

Your organization can have up to 10 active tunnels. Creating a tunnel does not establish any connectivity; that happens once your stack dials in with the tunnel token and a CA certificate is registered.

## Get the connection details

Open the tunnel. The detail page shows a **Connection** section with the domain and token and a **Certificates** section.

| Field      | Description                                                                                                                                                                                                         |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Domain** | Copy the assigned `abcd1234.tunnel.anthropic.com` value. Your proxy's routes are subdomains of this domain.                                                                                                         |
| **Token**  | Click the eye icon (**Show token**) to fetch the tunnel token, then use the copy icon to copy it into your tunnel stack's secret store. Click **Rotate token** to invalidate the current token and issue a new one. |

<Note>
  Every reveal and rotation is recorded in your organization's [Compliance API](/docs/en/manage-claude/compliance-api) activity log. Rotation does not sever cloudflared connections that are already established, so you can rotate, redeploy with the new value, and let the old connections drain.
</Note>

## Add a CA certificate

Anthropic verifies [inner TLS](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) to your [proxy](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) against the CA certificates you register on the tunnel. A tunnel with no active certificates cannot accept connections, and does not appear in the agent MCP server picker until one is registered.

<Steps>
  <Step title="Find the Certificates section">
    On the tunnel's detail page, scroll to the **Certificates** section and click **Add certificate**.
  </Step>

  <Step title="Provide the certificate">
    Click **Choose file** to select a `.pem`, `.crt`, or `.cer` file, drag the file onto the text area, or paste the PEM block directly. The modal rejects private-key material and content that isn't a `-----BEGIN CERTIFICATE-----` block. The file must be 8 kB or smaller.
  </Step>

  <Step title="Add the certificate">
    Click **Add certificate**. The fingerprint and expiry appear in the certificate list, and the slot count on the section header increments.
  </Step>
</Steps>

A tunnel holds up to two active certificates so you can rotate without downtime: register the new certificate alongside the old one, redeploy your proxy with the new key pair, confirm traffic is flowing, then click **Revoke** on the old certificate's row. Revoked certificates remain visible in the list with a **Revoked** badge.

## Deploy the tunnel stack

The tunnel exists in the Console, but no traffic flows until the tunnel stack is running inside your network and dialed in with the tunnel token. Follow one of the deploy guides:

<CardGroup cols={2}>
  <Card title="Deploy with Docker Compose" icon="cube" href="/docs/en/agents-and-tools/mcp-tunnels/deploy-compose">
    Run the tunnel stack on a single host. Both programmatic-access and manual flows.
  </Card>

  <Card title="Deploy with Helm" icon="stack" href="/docs/en/agents-and-tools/mcp-tunnels/deploy-helm">
    Run the tunnel stack on a Kubernetes cluster. Both programmatic-access and manual flows.
  </Card>
</CardGroup>

## Use the tunnel in an agent

Once your stack is running and has one or more MCP servers configured, attach an upstream MCP server to a Managed Agent session. To call the same servers from the Messages API instead, see [Use the tunneled MCP servers](/docs/en/agents-and-tools/mcp-tunnels/overview#use-the-tunneled-mcp-servers).

<Note>
  The picker only shows tunnels with at least one active certificate. A tunnel that still shows **Needs certificate** in the **MCP tunnels** list does not appear in the dropdown; register a CA certificate first. The picker is also workspace-scoped: it lists tunnels in the same workspace as the session, not other workspaces.
</Note>

<Steps>
  <Step title="Open the New session modal">
    Go to **Managed Agents > Sessions** and click **New session**.
  </Step>

  <Step title="Define an inline agent">
    In the agent picker, choose **Create new agent** so you can edit the MCP server list directly.
  </Step>

  <Step title="Add the MCP server">
    Click **+ MCP Server** and open the dropdown. Tunnels created in the current workspace appear at the top of the list, above the public connector catalog. Select the tunnel that fronts the server you want to reach.
  </Step>

  <Step title="Supply the routing">
    The card shows two optional fields: **Subdomain** (prefixed to the tunnel domain) and **Path** (appended after it). Fill in one or both, depending on how your proxy's routes are configured. The **Resolves to** line shows the full MCP server URL that the agent connects to.
  </Step>
</Steps>

<Note>
  The tunnel carries traffic; it does not authenticate to the upstream MCP server. Configure OAuth or bearer auth on the MCP server the same way as for any other MCP server.
</Note>

## Archive a tunnel

Archiving immediately stops the tunnel from accepting connections and is permanent.

In the **MCP tunnels** list, open the row menu for the tunnel and choose **Archive**. Archived tunnels remain visible when you filter the list by **Archived** or **All**.

## Next steps

<CardGroup cols={2}>
  <Card title="Deploy with Helm" icon="stack" href="/docs/en/agents-and-tools/mcp-tunnels/deploy-helm">
    Install on a Kubernetes cluster using the Anthropic Helm chart.
  </Card>

  <Card title="Security" icon="lock" href="/docs/en/agents-and-tools/mcp-tunnels/security">
    Hardening guidance, credential rotation, and breach response.
  </Card>
</CardGroup>
