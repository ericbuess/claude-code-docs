# Use WIF with Okta

Federate Okta service application identities to the Claude API with Workload Identity Federation.

---

Okta can act as a workload identity provider by issuing OIDC access tokens to a **service application** through the OAuth 2.0 `client_credentials` grant. Your workload authenticates to Okta (typically with `private_key_jwt`, so no shared secret is stored), receives a signed JSON Web Token (JWT), and exchanges that JWT with Anthropic for a short-lived access token.

The Okta authorization server's issuer URL takes the form `https://<your-domain>.okta.com/oauth2/<auth-server-id>`. If you use the built-in default server, the path is `/oauth2/default`.

<Note>
  You must use an Okta **custom authorization server** (including the `default` one). Tokens issued directly by the Okta org authorization server (the `/oauth2/v1/token` endpoint with no authorization server ID in the path) cannot be validated by external parties because Okta does not publish signing keys for them.
</Note>

There are many ways to configure and authenticate to Okta that are outside the scope of this documentation. Ensure that your configuration and authentication mechanisms follow your company's guidance and security practices.

## Prerequisites

* Familiarity with [WIF concepts](/docs/en/manage-claude/workload-identity-federation#concepts): service accounts, federation issuers, and federation rules.
* An Okta organization with API Access Management enabled (required for custom authorization servers).
* Permission to create service accounts, federation issuers, and federation rules in the Claude Console for your Anthropic organization.
* A workload that can request a token from Okta's `/v1/token` endpoint and reach `api.anthropic.com`.

## Configure Okta

At a high level you need to:

1. Create an Okta service application.
2. Configure your default authorization server (or create a new custom authorization server) with an audience, a scope, an access policy, and any custom claims you want to match on.

The exact navigation depends on your Okta org configuration and admin console version. The following numbered steps walk through one common path:

1. **Create a service app integration.** In the Okta Admin Console, create a new app integration of type **API Services** (OIDC, machine-to-machine). Note the generated **Client ID**.
2. **Configure client authentication.** For a keyless setup, choose **Public key / Private key** (`private_key_jwt`) and register your workload's public JWK. Alternatively, use a client secret if your environment can store one securely. For the following example you may need to disable the DPoP requirement on the application; ensure that your production setup adheres to your organization's security requirements.
3. **Set the audience.** On your custom authorization server, set the audience to `https://api.anthropic.com` so issued access tokens carry that `aud` claim. Anthropic validates `aud` against this fixed value.
4. **Grant a scope.** On your custom authorization server, ensure at least one scope exists that the service app is allowed to request (for example, `anthropic.access`). Okta rejects `client_credentials` requests that do not include a granted scope.
5. **Create an access policy.** On your custom authorization server, create an access policy with at least one rule that allows your service app to request the scope you granted in step 4.
6. **(Optional) Add custom claims.** If you want to match on something other than the client ID, add a claim to the access token in your authorization server's **Claims** tab.

For a service app using `client_credentials`, Okta sets the `sub` claim of the issued access token to the application's **Client ID**, and `iss` to the authorization server's issuer URL.

## Configure Anthropic

In the Claude Console, open **Settings → Workload identity**, click **Connect workload**, and select **Custom OIDC**. The wizard walks you through registering the issuer, creating a service account, and creating a federation rule.

The wizard creates these resources for you. Use the following values whether you enter them in the wizard or send them to the [Admin API](/docs/en/manage-claude/wif-admin-api):

**Federation issuer:** Use your Okta custom authorization server URL and discovery mode. Anthropic reads Okta's `.well-known/openid-configuration` discovery document and fetches the JWKS from the `jwks_uri` it advertises.

```json
{
  "name": "okta-prod",
  "issuer_url": "https://acme.okta.com/oauth2/aus1a2b3c4d5e6f7g8h9",
  "jwks": { "type": "discovery" }
}
```

**Federation rule:** Match on the Okta `sub` claim, which is the service app's Client ID. If you defined custom claims in Okta, you can match on those instead with the `claims` map or a CEL `condition`.

```json
{
  "name": "okta-pipeline",
  "issuer_id": "fdis_...",
  "match": {
    "subject_prefix": "0oa1b2c3d4e5f6g7h8i9",
    "audience": "https://api.anthropic.com"
  },
  "target": { "type": "service_account", "service_account_id": "svac_..." },
  "workspace_id": "wrkspc_...",
  "oauth_scope": "workspace:developer",
  "token_lifetime_seconds": 600
}
```

## Acquire a token and call the Claude API

Unlike platform-native providers (AWS, Google Cloud, Kubernetes), which make a token available inside the workload's runtime (through a projected file or local metadata endpoint), Okta does not. Your workload must call Okta's token endpoint to obtain a JWT, then pass that JWT to the Anthropic SDK as the identity token.

<CodeGroup>
  ```bash cURL
  # 1. Request an access token from Okta (client_credentials with private_key_jwt).
  OKTA_JWT=$(curl -sS "https://acme.okta.com/oauth2/aus1a2b3c4d5e6f7g8h9/v1/token" \
    -d grant_type=client_credentials \
    -d scope=anthropic.access \
    -d client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer \
    --data-urlencode client_assertion="$SIGNED_CLIENT_ASSERTION" \
    | jq -r .access_token)

  # 2. Exchange the Okta JWT for an Anthropic access token.
  ACCESS_TOKEN=$(curl -sS https://api.anthropic.com/v1/oauth/token \
    -H "content-type: application/json" \
    -d @- <<JSON | jq -r .access_token
  {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": "$OKTA_JWT",
    "federation_rule_id": "$ANTHROPIC_FEDERATION_RULE_ID",
    "organization_id": "$ANTHROPIC_ORGANIZATION_ID",
    "service_account_id": "$ANTHROPIC_SERVICE_ACCOUNT_ID",
    "workspace_id": "$ANTHROPIC_WORKSPACE_ID"
  }
  JSON
  )

  # 3. Call the Claude API.
  curl https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{"model": "claude-sonnet-4-6", "max_tokens": 1024, "messages": [{"role": "user", "content": "Hello, Claude"}]}' \
    | jq -r '.content[0].text'
  ```

  ```python Python
  import os
  import httpx
  import anthropic
  from anthropic import WorkloadIdentityCredentials


  def fetch_okta_token() -> str:
      response = httpx.post(
          f"{os.environ['OKTA_ISSUER']}/v1/token",
          data={
              "grant_type": "client_credentials",
              "scope": "anthropic.access",
              "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
              # Build the RFC 7523 client_assertion JWT signed with your Okta app's private key
              "client_assertion": build_signed_client_assertion(),
          },
      )
      response.raise_for_status()
      return response.json()["access_token"]


  client = anthropic.Anthropic(
      credentials=WorkloadIdentityCredentials(
          identity_token_provider=fetch_okta_token,
          federation_rule_id=os.environ["ANTHROPIC_FEDERATION_RULE_ID"],
          organization_id=os.environ["ANTHROPIC_ORGANIZATION_ID"],
          service_account_id=os.environ["ANTHROPIC_SERVICE_ACCOUNT_ID"],
          workspace_id=os.environ.get("ANTHROPIC_WORKSPACE_ID"),
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

  async function fetchOktaToken(): Promise<string> {
    const response = await fetch(`${process.env.OKTA_ISSUER}/v1/token`, {
      method: "POST",
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        grant_type: "client_credentials",
        scope: "anthropic.access",
        client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        // Build the RFC 7523 client_assertion JWT signed with your Okta app's private key
        client_assertion: buildSignedClientAssertion()
      })
    });
    const body = (await response.json()) as { access_token: string };
    return body.access_token;
  }

  const client = new Anthropic({
    credentials: oidcFederationProvider({
      identityTokenProvider: fetchOktaToken,
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
    messages: [{ role: "user", content: "Hello, Claude" }]
  });
  for (const block of message.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```go Go
  package main

  import (
  	"context"
  	"encoding/json"
  	"fmt"
  	"net/http"
  	"net/url"
  	"os"
  	"strings"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/option"
  )

  func fetchOktaToken(ctx context.Context) (string, error) {
  	form := url.Values{
  		"grant_type":            {"client_credentials"},
  		"scope":                 {"anthropic.access"},
  		"client_assertion_type": {"urn:ietf:params:oauth:client-assertion-type:jwt-bearer"},
  		// Build the RFC 7523 client_assertion JWT signed with your Okta app's private key
  		"client_assertion": {buildSignedClientAssertion()},
  	}
  	req, err := http.NewRequestWithContext(ctx, http.MethodPost,
  		os.Getenv("OKTA_ISSUER")+"/v1/token", strings.NewReader(form.Encode()))
  	if err != nil {
  		return "", err
  	}
  	req.Header.Set("content-type", "application/x-www-form-urlencoded")
  	resp, err := http.DefaultClient.Do(req)
  	if err != nil {
  		return "", err
  	}
  	defer resp.Body.Close()
  	var body struct {
  		AccessToken string `json:"access_token"`
  	}
  	if err := json.NewDecoder(resp.Body).Decode(&body); err != nil {
  		return "", err
  	}
  	return body.AccessToken, nil
  }

  func main() {
  	client := anthropic.NewClient(
  		option.WithFederationTokenProvider(option.IdentityTokenFunc(fetchOktaToken), option.FederationOptions{
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
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(message.Content[0].Text)
  }
  ```

  ```java Java
  IdentityTokenProvider fetchOktaToken = () -> {
      try {
          var form = Map.of(
                          "grant_type", "client_credentials",
                          "scope", "anthropic.access",
                          "client_assertion_type", "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                          // Build the RFC 7523 client_assertion JWT signed with your Okta app's private key
                          "client_assertion", buildSignedClientAssertion())
                  .entrySet().stream()
                  .map(entry -> entry.getKey() + "=" + URLEncoder.encode(entry.getValue(), UTF_8))
                  .collect(Collectors.joining("&"));
          var request = HttpRequest.newBuilder(URI.create(System.getenv("OKTA_ISSUER") + "/v1/token"))
                  .header("content-type", "application/x-www-form-urlencoded")
                  .POST(HttpRequest.BodyPublishers.ofString(form))
                  .build();
          var response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
          return new ObjectMapper().readTree(response.body()).get("access_token").asText();
      } catch (Exception e) {
          throw new RuntimeException(e);
      }
  };

  AnthropicClient client = AnthropicOkHttpClient.builder()
          .federationTokenProvider(
                  fetchOktaToken,
                  System.getenv("ANTHROPIC_FEDERATION_RULE_ID"),
                  System.getenv("ANTHROPIC_ORGANIZATION_ID"),
                  System.getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"))
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
      FederationRuleId = Environment.GetEnvironmentVariable("ANTHROPIC_FEDERATION_RULE_ID")!,
      OrganizationId = Environment.GetEnvironmentVariable("ANTHROPIC_ORGANIZATION_ID"),
      ServiceAccountId = Environment.GetEnvironmentVariable("ANTHROPIC_SERVICE_ACCOUNT_ID"),
      WorkspaceId = Environment.GetEnvironmentVariable("ANTHROPIC_WORKSPACE_ID"),
      IdentityTokenProvider = new OktaTokenProvider(),
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

  class OktaTokenProvider : IIdentityTokenProvider
  {
      private static readonly HttpClient Http = new();

      public async Task<string> GetIdentityTokenAsync(CancellationToken ct = default)
      {
          var form = new FormUrlEncodedContent(new Dictionary<string, string>
          {
              ["grant_type"] = "client_credentials",
              ["scope"] = "anthropic.access",
              ["client_assertion_type"] = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
              // Build the RFC 7523 client_assertion JWT signed with your Okta app's private key
              ["client_assertion"] = BuildSignedClientAssertion(),
          });
          var response = await Http.PostAsync(
              $"{Environment.GetEnvironmentVariable("OKTA_ISSUER")}/v1/token", form, ct);
          response.EnsureSuccessStatusCode();
          using var json = await JsonDocument.ParseAsync(
              await response.Content.ReadAsStreamAsync(ct), default, ct);
          return json.RootElement.GetProperty("access_token").GetString()!;
      }
  }
  ```

  ```bash CLI
  # 1. Request an access token from Okta and write it to a temp file.
  ANTHROPIC_IDENTITY_TOKEN_FILE=$(mktemp)
  curl -sS "$OKTA_ISSUER/v1/token" \
    -d grant_type=client_credentials \
    -d scope=anthropic.access \
    -d client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer \
    --data-urlencode client_assertion="$SIGNED_CLIENT_ASSERTION" \
    | jq -r .access_token > "$ANTHROPIC_IDENTITY_TOKEN_FILE"
  export ANTHROPIC_IDENTITY_TOKEN_FILE

  # 2. Call the Claude API. The CLI reads ANTHROPIC_FEDERATION_RULE_ID,
  # ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, and
  # ANTHROPIC_IDENTITY_TOKEN_FILE and performs the exchange.
  ant messages create \
    --model claude-sonnet-4-6 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Credentials\WorkloadIdentityCredentials;

  function fetchOktaToken(): string
  {
      $ch = curl_init(getenv('OKTA_ISSUER') . '/v1/token');
      curl_setopt_array($ch, [
          CURLOPT_RETURNTRANSFER => true,
          CURLOPT_POSTFIELDS => http_build_query([
              'grant_type' => 'client_credentials',
              'scope' => 'anthropic.access',
              'client_assertion_type' => 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
              // Build the RFC 7523 client_assertion JWT signed with your Okta app's private key
              'client_assertion' => buildSignedClientAssertion(),
          ]),
      ]);
      $body = json_decode(curl_exec($ch), true);
      curl_close($ch);
      return $body['access_token'];
  }

  $client = new Client(
      credentials: new WorkloadIdentityCredentials(
          identityTokenProvider: fetchOktaToken(...),
          federationRuleId: getenv('ANTHROPIC_FEDERATION_RULE_ID'),
          organizationId: getenv('ANTHROPIC_ORGANIZATION_ID'),
          serviceAccountId: getenv('ANTHROPIC_SERVICE_ACCOUNT_ID'),
          workspaceId: getenv('ANTHROPIC_WORKSPACE_ID') ?: null,
      ),
  );

  $message = $client->messages->create(
      model: 'claude-sonnet-4-6',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  );
  echo $message->content[0]->text, PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"
  require "json"
  require "net/http"

  def fetch_okta_token
    uri = URI("#{ENV.fetch('OKTA_ISSUER')}/v1/token")
    response = Net::HTTP.post_form(
      uri,
      "grant_type" => "client_credentials",
      "scope" => "anthropic.access",
      "client_assertion_type" => "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
      # Build the RFC 7523 client_assertion JWT signed with your Okta app's private key
      "client_assertion" => build_signed_client_assertion
    )
    JSON.parse(response.body).fetch("access_token")
  end

  client = Anthropic::Client.new(
    credentials: Anthropic::WorkloadIdentityCredentials.new(
      identity_token_provider: -> { fetch_okta_token },
      federation_rule_id: ENV.fetch("ANTHROPIC_FEDERATION_RULE_ID"),
      organization_id: ENV.fetch("ANTHROPIC_ORGANIZATION_ID"),
      service_account_id: ENV.fetch("ANTHROPIC_SERVICE_ACCOUNT_ID"),
      workspace_id: ENV["ANTHROPIC_WORKSPACE_ID"]
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

Each SDK tab shows the callable pattern: the Anthropic SDK calls your identity-token provider again whenever the Anthropic access token approaches expiry, so your Okta fetcher should return a fresh token on each call rather than caching one indefinitely. The `ant` CLI re-reads `ANTHROPIC_IDENTITY_TOKEN_FILE` on each exchange, so refresh that file on a timer for long-running shells.

## Verify the setup

A successful exchange returns an `access_token` beginning with `sk-ant-oat01-` and an `expires_in` value in seconds. On `400 invalid_grant`, see [Troubleshoot a failed exchange](/docs/en/manage-claude/wif-reference#troubleshoot-a-failed-exchange); the most common Okta-side cause is an `issuer_url` mismatch (it must include the `/oauth2/<auth-server-id>` path; the Okta org authorization server is not usable).

## Scope your rule

<Warning>
  Multiple service apps under the same Okta authorization server share the same issuer. A rule that omits `subject_prefix` matches every service app on that server, so any team that can register one could obtain a federated Anthropic token.
</Warning>

Lock the rule's `match` block to the narrowest scope that fits your use case:

* **Pin the exact Client ID:** Set `subject_prefix` to the service app's full Client ID with no trailing `*`.
* **Pin the audience:** Match the `audience` value you configured on the authorization server so tokens minted for a different audience are rejected.
* **Match on custom claims:** For finer-grained scoping, add claims in the authorization server's **Claims** tab and match them with the rule's `claims` map or a CEL `condition`.
* **Use one rule per service app:** Create a separate federation rule for each service app rather than sharing one rule across apps.

## Next steps

* Review the [WIF reference](/docs/en/manage-claude/wif-reference) for the full credential resolution order and profile configuration.
* See the [WIF reference](/docs/en/manage-claude/wif-reference#rule-matching-semantics) to match on custom Okta claims with CEL expressions.
