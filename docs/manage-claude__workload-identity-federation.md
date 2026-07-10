# Workload Identity Federation

Authenticate workloads to the Claude API with short-lived identity tokens from your own identity provider instead of long-lived static API keys.

---

Workload Identity Federation (WIF) lets your workloads authenticate to the Claude API with short-lived OpenID Connect (OIDC) tokens instead of long-lived `sk-ant-...` API keys. The tokens come from an identity provider (IdP) you already operate: AWS IAM, Google Cloud, or any standards-compliant OIDC issuer such as GitHub Actions, Kubernetes, SPIFFE, Microsoft Entra ID, or Okta.

Your workload presents a signed JWT from your identity provider. Anthropic validates it against trust rules you configure in the Claude Console and returns a short-lived Anthropic access token bound to a service account in your organization. There are no static secrets to mint, store in CI, rotate, or leak.

Workload Identity Federation strengthens your security posture by replacing static API keys with tokens that expire in minutes rather than never. It is not a complete security story on its own: federated authentication is only as strong as the upstream identity provider that signs the JWT. Pair Workload Identity Federation with the controls your IdP already supports (workload identity binding, conditional access, audit logging) for defense in depth.

## Concepts

You configure three resources in the Claude Console before any workload can federate. Together they express "tokens signed by issuer X, with claims that look like Y, may act as service account Z."

### Service accounts

A **service account** (`svac_...`) is a named, non-human identity inside your Anthropic organization. It is the principal that a federated token acts as. Service accounts live at the organization level and become active in a workspace when you add them as members of that workspace. At exchange time, Anthropic checks that the federation rule's workspace matches one of the service account's workspace memberships; the minted token then follows that workspace's rate limits and usage attribution, the same as an API key. Unlike a human user, a service account has no email, no password, and no Console login. Every service account is implicitly a member of your organization's default workspace; add explicit memberships for any other workspace it should act in.

The key distinction from an API key: an API key *is* a credential, while a service account *has* credentials minted for it on demand. You can audit which workloads acted as which service account.

### Federation issuers

A **federation issuer** (`fdis_...`) registers an OIDC identity provider with your organization. Registering an issuer tells Anthropic "JWTs signed by this provider may assert workload identity for my org."

An issuer has two pieces of configuration:

* **Issuer URL:** The exact `iss` claim value that appears in the provider's JWTs, for example `https://token.actions.githubusercontent.com` or `https://oidc.eks.us-west-2.amazonaws.com/id/EXAMPLE`.
* **JWKS source:** How Anthropic fetches the public keys to verify JWT signatures. Use `discovery` (the default) for any provider that serves `/.well-known/openid-configuration` at its issuer URL. Use `explicit_url` to point at a JWKS endpoint directly, or `inline` to upload the key set for issuers that are not reachable from the public internet (for example, a private Kubernetes cluster).

Issuer and JWKS URLs must be `https`, on port 443, and use a public DNS host name that resolves to public IP addresses; IP literals are not accepted. These constraints apply only to URLs Anthropic fetches; in `explicit_url` and `inline` modes the `issuer_url` is compared as a string and may reference an internal hostname.

You typically register one issuer per environment: your production EKS cluster, your staging cluster, and GitHub Actions are three separate issuers.

### Federation rules

A **federation rule** (`fdrl_...`) is the bridge between an issuer and a service account: "when a JWT from issuer X has claims that look like Y, mint a token for service account Z with scope S."

A rule defines match conditions, a target, and the authorization scope and token lifetime that apply when the rule matches:

* **Match:** The conditions an incoming JWT must satisfy. You can match on a `subject_prefix` (for example, `system:serviceaccount:prod:worker`, or with a trailing `*` for a prefix match), an exact `audience`, a map of exact claim values, a [CEL](https://cel.dev/) `condition` expression for complex logic, or any combination. At least one of `subject_prefix`, `claims`, or `condition` must be set, and all configured matchers must pass for the JWT to be accepted.
* **Target:** The service account the matched JWT maps to.
* **Authorization:** The OAuth `scope` granted on the minted token. The default is `workspace:developer`, which grants the same access as an API key issued for that workspace. Some products lock the scope when you create a rule from their flow; for example, the [MCP tunnels](/docs/en/agents-and-tools/mcp-tunnels/overview) create-tunnel modal creates rules scoped to `workspace:manage_tunnels`. See [OAuth scopes](/docs/en/manage-claude/wif-reference#oauth-scopes). The rule also sets `token_lifetime_seconds` (60 to 86400, default 3600).

A single issuer can have many rules: one per team, namespace, or permission level. Rules are evaluated by ID: the client specifies which rule to use in the exchange request, and Anthropic verifies the JWT satisfies that rule's match criteria. There is no implicit rule search.

## How it works

1. **Your IdP issues a JWT to the workload.** On most platforms this is ambient: a Kubernetes projected service-account token, the Google Cloud metadata server, Azure IMDS, or the GitHub Actions OIDC endpoint. The JWT's `iss` claim identifies the provider, and its `sub` and other claims identify the specific workload.
2. **The SDK exchanges the JWT for an Anthropic access token.** The SDK posts the JWT to `POST /v1/oauth/token` using the [RFC 7523](https://www.rfc-editor.org/rfc/rfc7523) `jwt-bearer` grant. Anthropic verifies the JWT against the issuer's JWKS and the federation rule's match conditions, then returns a short-lived `sk-ant-oat01-...` token that acts on behalf of the rule's target service account.
3. **The SDK sends the token on every request and refreshes it before it expires.** Your application code constructs the client with no `api_key` and calls the API as usual. The SDK re-runs the exchange before the token expires.

## Set up federation

You need the admin, owner, or primary owner role in your Anthropic organization, an OIDC-capable identity provider with a reachable JWKS endpoint (or a JWKS document you can paste, for air-gapped clusters), and a workload that can obtain an identity token from that provider.

The **Connect workload** wizard creates all three resources (the issuer, the service account, and the federation rule) in one guided flow, then verifies the connection end to end.

<Steps>
  <Step title="Open Connect workload">
    In the Claude Console, go to **Settings → Workload identity** and select **Connect workload**.
  </Step>

  <Step title="Choose your provider">
    Select the tile for your identity provider: GitHub Actions, AWS, Google Cloud, Microsoft Entra ID, or Kubernetes. Each tile prefills the issuer URL pattern and the match fields that provider's JWTs support. For any other standards-compliant provider (such as SPIFFE or Okta), select **Custom OIDC**.
  </Step>

  <Step title="Fill in the guided fields">
    The wizard walks you through the provider-specific fields: the issuer configuration, the match conditions for incoming JWTs, and names for the service account and federation rule it creates. The wizard prefills `oauth_scope=workspace:developer` and `token_lifetime_seconds=600` (the API default when `token_lifetime_seconds` is omitted is 3600); adjust these if your workload needs a different scope or lifetime.
  </Step>

  <Step title="Verify the issuer">
    Optionally select **Verify issuer** to dry-run the issuer configuration before anything is created. Verification confirms Anthropic can fetch and parse the JWKS from the URLs you entered, which catches reachability and configuration mistakes early.
  </Step>

  <Step title="Test the connection">
    The wizard creates the issuer, service account, and federation rule, then listens for a successful token exchange for 15 minutes. Trigger an exchange from your workload within that window (see [Authenticate from your workload](#authenticate-from-your-workload)) to confirm the setup works. If the window elapses, the resources persist; you can re-run the test from the federation rule's detail page. Note the rule's ID (`fdrl_...`) and the service account ID (`svac_...`) the wizard creates: your workload passes both, along with your organization ID (and your workspace ID when the rule covers more than one workspace), in every token-exchange request.
  </Step>
</Steps>

To manage these resources programmatically, see [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api) for the curl walkthrough, or see the [Service accounts API reference](/docs/en/api/admin/service_accounts), [Federation issuers API reference](/docs/en/api/admin/federation_issuers), and [Federation rules API reference](/docs/en/api/admin/federation_rules) for complete parameter details and response schemas.

## Authenticate from your workload

With federation configured, your workload exchanges its IdP-issued JWT for an Anthropic token at runtime. The SDKs handle the exchange and refresh loop for you. The cURL tab shows the underlying HTTP exchange for shell scripts, debugging, or languages without SDK support.

### Construct the SDK client

You can construct the client with explicit credentials or with no arguments. With no arguments, the SDK resolves credentials from environment variables or the active profile, as described under [Credential precedence](#credential-precedence). The zero-argument form is the recommended pattern for production workloads: ship the same container image everywhere and inject `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, `ANTHROPIC_WORKSPACE_ID`, and `ANTHROPIC_IDENTITY_TOKEN_FILE` per environment.

<CodeGroup>
  ```bash cURL
  # 1. Acquire your IdP's JWT (platform-specific; see the per-provider guides).
  JWT=$(cat /var/run/secrets/anthropic.com/token)

  # 2. Exchange it for a short-lived Anthropic access token.
  RESPONSE=$(curl -sS https://api.anthropic.com/v1/oauth/token \
    -H "content-type: application/json" \
    --data @- <<JSON
  {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": "$JWT",
    "federation_rule_id": "fdrl_...",
    "organization_id": "00000000-0000-0000-0000-000000000000",
    "service_account_id": "svac_...",
    "workspace_id": "wrkspc_..."
  }
  JSON
  )

  ACCESS_TOKEN=$(jq -r .access_token <<<"$RESPONSE")
  EXPIRES_IN=$(jq -r .expires_in <<<"$RESPONSE")  # seconds; re-exchange before this elapses

  # 3. Call the API with the access token in the Authorization: Bearer header.
  curl -sS https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    --data @- <<'JSON' | jq -r '.content[0].text'
  {
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello, Claude"}]
  }
  JSON
  ```

  ```python Python
  from anthropic import Anthropic, WorkloadIdentityCredentials, IdentityTokenFile

  client = Anthropic(
      credentials=WorkloadIdentityCredentials(
          identity_token_provider=IdentityTokenFile(
              "/var/run/secrets/anthropic.com/token"
          ),
          federation_rule_id="fdrl_...",
          organization_id="00000000-0000-0000-0000-000000000000",
          service_account_id="svac_...",
          workspace_id="wrkspc_...",
      ),
  )

  message = client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(message.content[0].text)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { oidcFederationProvider } from "@anthropic-ai/sdk/lib/credentials/oidc-federation";
  import { identityTokenFromFile } from "@anthropic-ai/sdk/lib/credentials/identity-token";

  const client = new Anthropic({
    credentials: oidcFederationProvider({
      identityTokenProvider: identityTokenFromFile("/var/run/secrets/anthropic.com/token"),
      federationRuleId: "fdrl_...",
      organizationId: "00000000-0000-0000-0000-000000000000",
      serviceAccountId: "svac_...",
      workspaceId: "wrkspc_...",
      baseURL: "https://api.anthropic.com",
      fetch
    })
  });

  const message = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  });
  for (const block of message.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```go Go
  client := anthropic.NewClient(
  	option.WithFederationTokenProvider(
  		option.IdentityTokenFile("/var/run/secrets/anthropic.com/token"),
  		option.FederationOptions{
  			FederationRuleID: "fdrl_...",
  			OrganizationID:   "00000000-0000-0000-0000-000000000000",
  			ServiceAccountID: "svac_...",
  			WorkspaceID:      "wrkspc_...",
  		},
  	),
  )

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet4_6,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(message.Content[0].Text)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.builder()
          .fromEnv()
          .configurationProvider(InMemoryProfileConfigProvider.of(ProfileConfig.builder()
                  .organizationId("00000000-0000-0000-0000-000000000000")
                  .workspaceId("wrkspc_...")
                  .authentication(AuthenticationConfig.builder()
                          .type(AuthenticationType.OIDC_FEDERATION)
                          .federationRuleId("fdrl_...")
                          .serviceAccountId("svac_...")
                          .identityToken(IdentityTokenConfig.builder()
                                  .source("file")
                                  .path("/var/run/secrets/anthropic.com/token")
                                  .build())
                          .build())
                  .build()))
          .build();

  var message = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_4_6)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .build());

  IO.println(message.content());
  ```

  ```csharp C#
  var credentials = new WorkloadIdentityCredentials(new WorkloadIdentityOptions
  {
      FederationRuleId = "fdrl_...",
      OrganizationId = "00000000-0000-0000-0000-000000000000",
      ServiceAccountId = "svac_...",
      WorkspaceId = "wrkspc_...",
      IdentityTokenProvider = new FileIdentityTokenProvider("/var/run/secrets/anthropic.com/token"),
  });
  using var client = new AnthropicOidcClient(credentials);

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeSonnet4_6,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello, Claude" }],
  });
  foreach (var block in message.Content)
  {
      if (block.Value is TextBlock textBlock)
      {
          Console.WriteLine(textBlock.Text);
      }
  }
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Lib\Credentials\CredentialResult;
  use Anthropic\Lib\Credentials\IdentityTokenFile;
  use Anthropic\Lib\Credentials\TokenCache;
  use Anthropic\Lib\Credentials\WorkloadIdentityCredentials;

  $client = new Client(credentials: new CredentialResult(
      provider: new TokenCache(
          new WorkloadIdentityCredentials(
              identityProvider: new IdentityTokenFile('/var/run/secrets/anthropic.com/token'),
              federationRuleId: 'fdrl_...',
              organizationId: '00000000-0000-0000-0000-000000000000',
              serviceAccountId: 'svac_...',
              workspaceId: 'wrkspc_...',
          ),
      ),
  ));

  $message = $client->messages->create(
      model: 'claude-sonnet-4-6',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  );

  echo $message->content[0]->text . PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new(
    credentials: Anthropic::Credentials::WorkloadIdentity.new(
      identity_token_provider: Anthropic::Credentials::IdentityTokenFile.new(
        "/var/run/secrets/anthropic.com/token"
      ),
      federation_rule_id: "fdrl_...",
      organization_id: "00000000-0000-0000-0000-000000000000",
      service_account_id: "svac_...",
      workspace_id: "wrkspc_..."
    )
  )

  message = client.messages.create(
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

The token-exchange response follows [RFC 6749 §5.1](https://www.rfc-editor.org/rfc/rfc6749#section-5.1). See [Token exchange response](/docs/en/manage-claude/wif-reference#token-exchange-response) for the field reference.

## Credential precedence

Every SDK resolves credentials in the same five-tier order: constructor arguments, then `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN`, then an explicit `ANTHROPIC_PROFILE`, then the federation environment variables, then the implicit active profile. The first source that yields a credential wins.

<Warning>
  `ANTHROPIC_API_KEY` sits above the federation tiers, so a leftover key in the environment silently shadows federation. When migrating a workload from API keys to Workload Identity Federation, confirm `ANTHROPIC_API_KEY` is unset everywhere that workload runs (container env, CI secrets, shell profiles). The CLI's [`ant auth status`](/docs/en/cli-sdks-libraries/cli/authentication#check-authentication-status) command reports which source won.
</Warning>

For the full precedence table, the per-tier semantics, and the profile file schema, see [Credential precedence](/docs/en/manage-claude/wif-reference#credential-precedence) in the WIF reference.

## Migrate from API keys

To switch an existing workload from a static API key to federation without downtime:

1. **Configure federation in parallel.** Complete the [setup walkthrough](#set-up-federation) and confirm the federation rule matches your workload's token. Leave the existing `ANTHROPIC_API_KEY` in place for now.
2. **Smoke-test which credential wins.** Run `ant auth status` from inside the workload (or inspect SDK debug logs). Because `ANTHROPIC_API_KEY` sits above the federation tiers in the precedence chain, the API key still wins at this stage.
3. **Unset `ANTHROPIC_API_KEY` everywhere it is injected.** Remove it from CI secrets, container environment, and shell profiles (see the preceding warning). Re-run `ant auth status` and confirm the federation source is now selected.
4. **Revoke the API key.** Once the workload is running on the federated token, delete the key in the Claude Console under **Settings → API keys**.

## Token lifetime and refresh

The minted Anthropic token's lifetime is the lesser of (a) the rule's `token_lifetime_seconds` (default 3600 seconds) and (b) twice the remaining lifetime of the IdP JWT you presented. The result is never less than 60 seconds. The second bound prevents an Anthropic token from outliving the upstream identity it was derived from by more than a small margin.

The SDKs cache the token and refresh it on a two-tier schedule modeled on `botocore`:

* **Advisory refresh** at expiry minus 120 seconds. The SDK attempts a new exchange. If the token endpoint is unreachable, the SDK continues serving the cached token, which is still valid for roughly 90 more seconds.
* **Mandatory refresh** at expiry minus 30 seconds. A failed exchange at this point raises an error. The cached token is too close to expiry to be safe.

Because the SDK re-reads `ANTHROPIC_IDENTITY_TOKEN_FILE` on every exchange, it transparently picks up rotated projected tokens (Kubernetes service-account tokens, for example, rotate well before their `exp`).

## Identity providers

Each guide covers where the JWT comes from on that platform, what its claims look like, and the issuer and rule configuration to register.

<CardGroup cols={3}>
  <Card title="AWS" icon="cloud" href="/docs/en/manage-claude/wif-providers/aws">
    STS web identity tokens, or EKS IRSA projected tokens.
  </Card>

  <Card title="Google Cloud" icon="cloud" href="/docs/en/manage-claude/wif-providers/gcp">
    Google-signed identity tokens from the metadata server.
  </Card>

  <Card title="Microsoft Entra ID" icon="cloud" href="/docs/en/manage-claude/wif-providers/azure">
    Managed Identity (IMDS) and Entra Workload ID on AKS.
  </Card>

  <Card title="GitHub Actions" icon="github-logo" href="/docs/en/manage-claude/wif-providers/github-actions">
    Keyless CI authentication with the Actions OIDC token.
  </Card>

  <Card title="Kubernetes" icon="cube" href="/docs/en/manage-claude/wif-providers/kubernetes">
    Self-managed and on-premises clusters using projected service-account tokens.
  </Card>

  <Card title="SPIFFE" icon="fingerprint" href="/docs/en/manage-claude/wif-providers/spiffe">
    Workloads with SPIFFE JWT-SVIDs from SPIRE or another conformant issuer.
  </Card>

  <Card title="Okta" icon="lock" href="/docs/en/manage-claude/wif-providers/okta">
    Okta service applications using client-credentials flow.
  </Card>
</CardGroup>

## See also

* [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api): create issuers, service accounts, and rules from infrastructure as code
* [WIF reference](/docs/en/manage-claude/wif-reference): environment variables, profile file schema, validation rules, and error codes
* [Authentication](/docs/en/manage-claude/authentication): all authentication options across the Anthropic SDKs
* [Admin API reference](/docs/en/api/admin): generated request and response schemas for every Admin API endpoint
