# Use WIF with Google Cloud

Federate Google Cloud workloads (Cloud Run, Cloud Functions, App Engine, GCE, GKE) to the Claude API using Google-signed identity tokens instead of static API keys.

---

Any Google Cloud compute environment with access to the instance metadata server (Cloud Run, Cloud Functions, App Engine, Compute Engine (GCE), and GKE with Workload Identity) can request a Google-signed identity token for its attached service account. The token's issuer is `https://accounts.google.com`, and Anthropic can validate it directly through standard OIDC discovery, with no extra Google Cloud configuration required.

This guide shows how to register the Google issuer with Anthropic, bind a Google service account to an Anthropic service account, and have your workload exchange its identity token for a short-lived Claude API access token.

## Prerequisites

* Familiarity with [WIF concepts](/docs/en/manage-claude/workload-identity-federation#concepts): service accounts, federation issuers, and federation rules.
* A Google Cloud project with a workload running on Cloud Run, Cloud Functions, App Engine, Compute Engine, or GKE.
* A user-managed Google service account attached to that workload (not the Compute Engine default service account).
* Permission to create service accounts, federation issuers, and federation rules in the Claude Console for your Anthropic organization.

## Configure Google Cloud

Google issues identity tokens automatically to any workload with an attached service account. There is nothing to enable on the Google side beyond attaching the right service account, but the steps differ slightly between standard compute and GKE.

<Tabs>
  <Tab title="Cloud Run, Cloud Functions, App Engine, GCE">
    Attach a dedicated service account to your service or instance:

    ```bash CLI
    gcloud run deploy my-service \
      --service-account inference-worker@my-project.iam.gserviceaccount.com
    ```

    Inside the workload, the metadata server returns a signed identity token on demand. Request it with the `audience` you intend to register on the Anthropic side, and include `format=full` so the response carries the `email` claim:

    ```text wrap
    GET http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full
    Metadata-Flavor: Google
    ```

    Or, with the gcloud CLI:

    ```bash CLI
    gcloud auth print-identity-token \
      --audiences="https://api.anthropic.com" \
      --include-email
    ```

    The SDK equivalents are shown in [Acquire and use the token](#acquire-and-use-the-token).

    The decoded token payload looks like this:

    ```json
    {
      "iss": "https://accounts.google.com",
      "aud": "https://api.anthropic.com",
      "sub": "104892...",
      "azp": "104892...",
      "email": "inference-worker@my-project.iam.gserviceaccount.com",
      "email_verified": true,
      "exp": 1775527120
    }
    ```

    The `sub` claim is the Google service account's opaque numeric unique ID. The `email` claim is the human-readable service account address. Match on both `sub` and `email` in your federation rule.
  </Tab>

  <Tab title="GKE with Workload Identity">
    Enable [Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity) on your cluster and bind your Kubernetes service account to a Google service account with the `iam.gke.io/gcp-service-account` annotation:

    ```yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: inference-worker
      namespace: prod
      annotations:
        iam.gke.io/gcp-service-account: inference-worker@my-project.iam.gserviceaccount.com
    ```

    With this binding in place, the GKE metadata server returns a Google-signed token identical to the Cloud Run and GCE case: same `https://accounts.google.com` issuer, same `email` claim, same fetch URL. Configure Anthropic exactly as in the next section.

    A `format=full` token from GKE additionally includes `google.compute_engine.project_id`, `google.compute_engine.zone`, and `google.compute_engine.instance_name` claims, which you can reference in a federation rule's `condition` matcher (a CEL expression like `claims.google.compute_engine.project_id == "my-project"`) to scope access to a specific cluster or node pool.

    <Note>
      If you do not want to bind Kubernetes service accounts to Google service accounts, GKE pods can instead use the cluster's own OIDC issuer (`https://container.googleapis.com/v1/projects/PROJECT/locations/REGION/clusters/CLUSTER`) with a projected `serviceAccountToken` volume. That path uses a per-cluster issuer rather than `accounts.google.com`. See [Use WIF with Kubernetes](/docs/en/manage-claude/wif-providers/kubernetes) for that pattern.
    </Note>
  </Tab>
</Tabs>

## Configure Anthropic

In the Claude Console, open **Settings → Workload identity**, click **Connect workload**, and select the **Google Cloud** tile. The wizard walks you through registering the issuer, creating a service account, and creating a federation rule.

The wizard creates these resources for you. Use the following values whether you enter them in the wizard or send them to the [Admin API](/docs/en/manage-claude/wif-admin-api):

**Federation issuer:** Google publishes its OIDC discovery document publicly, so use discovery mode. This single issuer covers every Google Cloud surface (Cloud Run, GCE, Cloud Functions, App Engine, and GKE with Workload Identity). Differentiate workloads with rules, not issuers.

```json
{
  "name": "gcp",
  "issuer_url": "https://accounts.google.com",
  "jwks": { "type": "discovery" }
}
```

**Federation rule:** Match on both the `sub` and `email` claims. `email` is the readable service-account address; `sub` is the service account's numeric unique ID, which Google never reuses, so pinning it protects the rule if the service account is deleted and a new one is later created with the same email. Find the unique ID with `gcloud iam service-accounts describe SA_EMAIL --format='value(uniqueId)'`.

```json
{
  "name": "gcp-inference-worker",
  "issuer_id": "fdis_...",
  "match": {
    "audience": "https://api.anthropic.com",
    "claims": {
      "sub": "104892101234567890123",
      "email": "inference-worker@my-project.iam.gserviceaccount.com"
    }
  },
  "target": {
    "type": "service_account",
    "service_account_id": "svac_..."
  },
  "workspace_id": "wrkspc_...",
  "oauth_scope": "workspace:developer",
  "token_lifetime_seconds": 600
}
```

## Acquire and use the token

Inside your Google Cloud workload, fetch the identity token from the metadata server, exchange it at `POST /v1/oauth/token`, and use the returned bearer token to call the Claude API. Each Anthropic SDK handles the exchange and refresh loop for you when you supply a token-provider callable that returns a fresh identity token from the metadata server, as shown in the following examples.

<CodeGroup>
  ```bash cURL
  # Fetch the Google-signed identity token from the metadata server
  JWT=$(curl -sS -H "Metadata-Flavor: Google" \
    "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full")

  # Exchange it for an Anthropic access token
  RESPONSE=$(curl -sS https://api.anthropic.com/v1/oauth/token \
    -H "content-type: application/json" \
    --data @- <<JSON
  {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": "$JWT",
    "federation_rule_id": "$ANTHROPIC_FEDERATION_RULE_ID",
    "organization_id": "$ANTHROPIC_ORGANIZATION_ID",
    "service_account_id": "$ANTHROPIC_SERVICE_ACCOUNT_ID",
    "workspace_id": "$ANTHROPIC_WORKSPACE_ID"
  }
  JSON
  )
  ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r .access_token)

  # Call the Claude API
  curl -sS https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-6",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello from Cloud Run"}]
    }' | jq -r '.content[0].text'
  ```

  ```python Python
  import os
  import anthropic
  import google.auth.transport.requests
  import google.oauth2.id_token
  from anthropic import WorkloadIdentityCredentials

  AUDIENCE = "https://api.anthropic.com"


  def fetch_google_identity_token() -> str:
      request = google.auth.transport.requests.Request()
      return google.oauth2.id_token.fetch_id_token(request, AUDIENCE)


  client = anthropic.Anthropic(
      credentials=WorkloadIdentityCredentials(
          identity_token_provider=fetch_google_identity_token,
          federation_rule_id=os.environ["ANTHROPIC_FEDERATION_RULE_ID"],
          organization_id=os.environ["ANTHROPIC_ORGANIZATION_ID"],
          service_account_id=os.environ["ANTHROPIC_SERVICE_ACCOUNT_ID"],
          workspace_id=os.environ.get("ANTHROPIC_WORKSPACE_ID"),
      ),
  )

  message = client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello from Cloud Run"}],
  )
  print(message.content[0].text)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { oidcFederationProvider } from "@anthropic-ai/sdk/lib/credentials/oidc-federation";

  const METADATA_URL =
    "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full";

  async function fetchGoogleIdentityToken(): Promise<string> {
    const response = await fetch(METADATA_URL, {
      headers: { "Metadata-Flavor": "Google" }
    });
    return response.text();
  }

  const client = new Anthropic({
    credentials: oidcFederationProvider({
      identityTokenProvider: fetchGoogleIdentityToken,
      federationRuleId: process.env.ANTHROPIC_FEDERATION_RULE_ID!,
      organizationId: process.env.ANTHROPIC_ORGANIZATION_ID!,
      serviceAccountId: process.env.ANTHROPIC_SERVICE_ACCOUNT_ID,
      workspaceId: process.env.ANTHROPIC_WORKSPACE_ID,
      baseURL: "https://api.anthropic.com",
      fetch
    })
  });

  const message = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello from Cloud Run" }]
  });
  for (const block of message.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```go Go
  const audience = "https://api.anthropic.com"

  googleIDToken := func(ctx context.Context) (string, error) {
  	creds, err := idtoken.NewCredentials(&idtoken.Options{Audience: audience})
  	if err != nil {
  		return "", err
  	}
  	tok, err := creds.Token(ctx)
  	if err != nil {
  		return "", err
  	}
  	return tok.Value, nil
  }

  client := anthropic.NewClient(
  	option.WithFederationTokenProvider(googleIDToken, option.FederationOptions{
  		FederationRuleID: os.Getenv("ANTHROPIC_FEDERATION_RULE_ID"),
  		OrganizationID:   os.Getenv("ANTHROPIC_ORGANIZATION_ID"),
  		ServiceAccountID: os.Getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"),
  		WorkspaceID:      os.Getenv("ANTHROPIC_WORKSPACE_ID"),
  	}),
  )

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet4_6,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello from Cloud Run")),
  	},
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(message.Content[0].Text)
  ```

  ```java Java
  HttpClient http = HttpClient.newHttpClient();
  HttpRequest metadataRequest = HttpRequest.newBuilder()
          .uri(URI.create("http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full"))
          .header("Metadata-Flavor", "Google")
          .build();

  IdentityTokenProvider fetchGoogleIdentityToken = () -> {
      try {
          return http.send(metadataRequest, HttpResponse.BodyHandlers.ofString()).body();
      } catch (Exception e) {
          throw new RuntimeException(e);
      }
  };

  AnthropicClient client = AnthropicOkHttpClient.builder()
          .federationTokenProvider(
                  fetchGoogleIdentityToken,
                  System.getenv("ANTHROPIC_FEDERATION_RULE_ID"),
                  System.getenv("ANTHROPIC_ORGANIZATION_ID"),
                  System.getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"))
          .build();

  var message = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_4_6)
          .maxTokens(1024)
          .addUserMessage("Hello from Cloud Run")
          .build());

  IO.println(message.content());
  ```

  ```csharp C#
  var credentials = new WorkloadIdentityCredentials(new WorkloadIdentityOptions
  {
      FederationRuleId = Environment.GetEnvironmentVariable("ANTHROPIC_FEDERATION_RULE_ID")!,
      OrganizationId = Environment.GetEnvironmentVariable("ANTHROPIC_ORGANIZATION_ID"),
      ServiceAccountId = Environment.GetEnvironmentVariable("ANTHROPIC_SERVICE_ACCOUNT_ID"),
      WorkspaceId = Environment.GetEnvironmentVariable("ANTHROPIC_WORKSPACE_ID"),
      IdentityTokenProvider = new MetadataTokenProvider(),
  });
  using var client = new AnthropicOidcClient(credentials);

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeSonnet4_6,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello from Cloud Run" }],
  });
  foreach (var block in message.Content)
  {
      if (block.Value is TextBlock textBlock)
      {
          Console.WriteLine(textBlock.Text);
      }
  }

  class MetadataTokenProvider : IIdentityTokenProvider
  {
      private const string METADATA_URL =
          "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full";

      private static readonly HttpClient httpClient = new()
      {
          DefaultRequestHeaders = { { "Metadata-Flavor", "Google" } },
      };

      public async Task<string> GetIdentityTokenAsync(CancellationToken ct = default)
      {
          return await httpClient.GetStringAsync(METADATA_URL, ct);
      }
  }
  ```

  ```bash CLI
  # Write the Google-signed identity token to a file the CLI can read
  ANTHROPIC_IDENTITY_TOKEN_FILE=$(mktemp)
  curl -sS -H "Metadata-Flavor: Google" \
    "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full" \
    > "$ANTHROPIC_IDENTITY_TOKEN_FILE"
  export ANTHROPIC_IDENTITY_TOKEN_FILE

  # ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID, and
  # ANTHROPIC_SERVICE_ACCOUNT_ID, and ANTHROPIC_WORKSPACE_ID are read from the environment.
  ant messages create \
    --model claude-sonnet-4-6 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello from Cloud Run"}'
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Credentials\WorkloadIdentityCredentials;

  const METADATA_URL = 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full';

  $context = stream_context_create([
      'http' => ['header' => "Metadata-Flavor: Google\r\n"],
  ]);

  $credentials = new WorkloadIdentityCredentials(
      identityTokenProvider: fn() => file_get_contents(METADATA_URL, false, $context),
      federationRuleId: getenv('ANTHROPIC_FEDERATION_RULE_ID'),
      organizationId: getenv('ANTHROPIC_ORGANIZATION_ID'),
      serviceAccountId: getenv('ANTHROPIC_SERVICE_ACCOUNT_ID'),
      workspaceId: getenv('ANTHROPIC_WORKSPACE_ID') ?: null,
  );
  $client = new Client(credentials: $credentials);

  $message = $client->messages->create(
      model: 'claude-sonnet-4-6',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello from Cloud Run']],
  );
  echo $message->content[0]->text, PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"
  require "net/http"

  METADATA_URL = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full"

  credentials = Anthropic::WorkloadIdentityCredentials.new(
    identity_token_provider: -> { Net::HTTP.get(URI(METADATA_URL), {"Metadata-Flavor" => "Google"}) },
    federation_rule_id: ENV.fetch("ANTHROPIC_FEDERATION_RULE_ID"),
    organization_id: ENV.fetch("ANTHROPIC_ORGANIZATION_ID"),
    service_account_id: ENV.fetch("ANTHROPIC_SERVICE_ACCOUNT_ID"),
    workspace_id: ENV["ANTHROPIC_WORKSPACE_ID"]
  )
  client = Anthropic::Client.new(credentials: credentials)

  message = client.messages.create(
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello from Cloud Run"}]
  )
  puts message.content.first.text
  ```
</CodeGroup>

Google identity tokens expire after roughly one hour. The SDKs re-invoke the token provider and re-exchange automatically before expiry. For shell scripts that run longer than the access token's `expires_in`, refresh on a timer and repeat the exchange.

## Verify the setup

From inside your workload, decode the identity token and confirm the claims match your rule:

```bash cURL
curl -sS -H "Metadata-Flavor: Google" \
  "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://api.anthropic.com&format=full" \
  | jq -rR 'split(".")[1] | gsub("-";"+") | gsub("_";"/") | @base64d | fromjson'
```

Check that `iss` is `https://accounts.google.com`, `aud` is `https://api.anthropic.com`, and `email` matches the value in your federation rule. Then run the exchange from the previous section. A successful exchange returns an `access_token` beginning with `sk-ant-oat01-` and an `expires_in` value in seconds. On `400 invalid_grant`, see [Troubleshoot a failed exchange](/docs/en/manage-claude/wif-reference#troubleshoot-a-failed-exchange); the most common Google Cloud-side cause is the `email` claim missing (request the token with `format=full` so it is included).

## Scope your rule

<Warning>
  The Google `sub` claim is the service account's opaque numeric unique ID and has no stable prefix. A `subject_prefix` with a trailing `*` matches arbitrary service accounts across every Google Cloud project, and any of them could obtain a federated Anthropic token.
</Warning>

Lock the rule's `match` block to the narrowest scope that fits your use case:

* **Match `sub` exactly:** Set the full numeric unique ID in `claims.sub` and never use `subject_prefix` for Google tokens.
* **Pin the `email` claim:** Add `claims.email` alongside `sub` so both the stable ID and the readable address must match.
* **Pin the audience:** Set `audience` to the exact value you request from the metadata server so tokens minted for other consumers are rejected.
* **Pin the project on GKE:** For `format=full` tokens, add a `condition` such as `claims.google.compute_engine.project_id == "my-project"` to restrict the rule to one project's nodes.

## Next steps

* Read the [Workload Identity Federation](/docs/en/manage-claude/workload-identity-federation) page for the full resource model and SDK credential precedence.
* Add a separate federation rule per environment (production, staging) so you can revoke one without affecting the others.
