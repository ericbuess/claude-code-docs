# Authenticate with vaults

Register per-user credentials when creating sessions.

---

Vaults and credentials are authentication primitives that let you register credentials for third-party services once and reference them by ID at session creation. This means you don't need to run your own secret store, transmit tokens on every call, or lose track of which end user an agent acted on behalf of.

The vault reference is a per-session parameter, so you can manage your product at the `agent` resource granularity and your users at the `session` resource granularity.

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## Create a vault

<Warning>
  Vaults and credentials are workspace-scoped, meaning anyone with an API key for the same workspace can reference them when creating a session. To revoke access, delete the vault or credential.
</Warning>

A vault is the collection of `credentials` associated with an end user. Give it a `display_name` and optionally tag it with `metadata` so you can map it back to your own user records.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  vault_id=$(curl --fail-with-body -sS https://api.anthropic.com/v1/vaults \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<'EOF' | jq -r '.id'
  {
    "display_name": "Alice",
    "metadata": {"external_user_id": "usr_abc123"}
  }
  EOF
  )
  echo "$vault_id"  # "vlt_01ABC..."
  ```

  ```bash CLI
  VAULT_ID=$(ant beta:vaults create \
    --display-name "Alice" \
    --metadata '{external_user_id: usr_abc123}' \
    --transform id --raw-output)
  echo "$VAULT_ID"  # "vlt_01ABC..."
  ```

  ```python Python
  vault = client.beta.vaults.create(
      display_name="Alice",
      metadata={"external_user_id": "usr_abc123"},
  )
  print(vault.id)  # "vlt_01ABC..."
  ```

  ```typescript TypeScript
  const vault = await client.beta.vaults.create({
    display_name: "Alice",
    metadata: { external_user_id: "usr_abc123" },
  });
  console.log(vault.id); // "vlt_01ABC..."
  ```

  ```csharp C#
  var vault = await client.Beta.Vaults.Create(new()
  {
      DisplayName = "Alice",
      Metadata = new Dictionary<string, string> { ["external_user_id"] = "usr_abc123" },
  });
  Console.WriteLine(vault.ID); // "vlt_01ABC..."
  ```

  ```go Go
  vault, err := client.Beta.Vaults.New(ctx, anthropic.BetaVaultNewParams{
  	DisplayName: "Alice",
  	Metadata:    map[string]string{"external_user_id": "usr_abc123"},
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(vault.ID) // "vlt_01ABC..."
  ```

  ```java Java
  var vault = client.beta().vaults().create(VaultCreateParams.builder()
      .displayName("Alice")
      .metadata(VaultCreateParams.Metadata.builder()
          .putAdditionalProperty("external_user_id", JsonValue.from("usr_abc123"))
          .build())
      .build());
  IO.println(vault.id()); // "vlt_01ABC..."
  ```

  ```php PHP
  $vault = $client->beta->vaults->create(
      displayName: 'Alice',
      metadata: ['external_user_id' => 'usr_abc123'],
  );
  echo $vault->id . "\n"; // "vlt_01ABC..."
  ```

  ```ruby Ruby
  vault = client.beta.vaults.create(
    display_name: "Alice",
    metadata: {external_user_id: "usr_abc123"}
  )
  puts vault.id # "vlt_01ABC..."
  ```
</CodeGroup>

The response is the full vault record:

```json
{
  "type": "vault",
  "id": "vlt_01ABC...",
  "display_name": "Alice",
  "metadata": { "external_user_id": "usr_abc123" },
  "created_at": "2026-03-18T10:00:00Z",
  "updated_at": "2026-03-18T10:00:00Z",
  "archived_at": null
}
```

## Add a credential

Two credential categories are supported:

* **MCP credentials** (`mcp_oauth`, `static_bearer`): each credential is keyed by an `mcp_server_url`. When the agent connects to a server at that URL at session runtime, the token is injected automatically.
* **Environment variables** (`environment_variable`): each credential is keyed by a `secret_name` (the environment variable name) and stored in the sandbox as an opaque placeholder. When the agent initiates an outbound request, the opaque placeholder is substituted with the real secret at egress. The agent never sees the secret value. Use this for any service that authenticates through an environment variable, such as CLIs, SDKs, or direct API calls.

The actual credential values you supply (`token`, `access_token`, `refresh_token`, `client_secret`, `secret_value`) are treated as sensitive, write-only fields and never returned in API responses.

<Note>
  Environment variable credentials (`environment_variable`) are not yet supported with [self-hosted sandboxes](/docs/en/managed-agents/self-hosted-sandboxes).
</Note>

<Tabs>
  <Tab title="MCP OAuth">
    Use `mcp_oauth` when the MCP server uses OAuth 2.0. If you supply a `refresh` block, Anthropic refreshes the access token on your behalf when it expires.

    The `refresh.token_endpoint_auth.type` field indicates how to authenticate the refresh call:

    * `none`: public client
    * `client_secret_basic`: HTTP Basic authentication with the client secret
    * `client_secret_post`: client secret in the POST body

    <CodeGroup defaultLanguage="CLI">
      ```bash curl
      credential_id=$(curl --fail-with-body -sS "https://api.anthropic.com/v1/vaults/$vault_id/credentials" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        --data @- <<'EOF' | jq -r '.id'
      {
        "display_name": "Alice's Slack",
        "auth": {
          "type": "mcp_oauth",
          "mcp_server_url": "https://mcp.slack.com/mcp",
          "access_token": "xoxp-...",
          "expires_at": "2099-12-31T23:59:59Z",
          "refresh": {
            "token_endpoint": "https://slack.com/api/oauth.v2.access",
            "client_id": "1234567890.0987654321",
            "scope": "channels:read chat:write",
            "refresh_token": "xoxe-1-...",
            "token_endpoint_auth": {"type": "client_secret_post", "client_secret": "abc123..."}
          }
        }
      }
      EOF
      )
      ```

      ```bash CLI
      CREDENTIAL_ID=$(ant beta:vaults:credentials create \
        --vault-id "$VAULT_ID" \
        --display-name "Alice's Slack" \
        --transform id --raw-output <<'YAML'
      auth:
        type: mcp_oauth
        mcp_server_url: https://mcp.slack.com/mcp
        access_token: xoxp-...
        expires_at: "2099-12-31T23:59:59Z"
        refresh:
          token_endpoint: https://slack.com/api/oauth.v2.access
          client_id: "1234567890.0987654321"
          scope: channels:read chat:write
          refresh_token: xoxe-1-...
          token_endpoint_auth:
            type: client_secret_post
            client_secret: abc123...
      YAML
      )
      ```

      ```python Python
      credential = client.beta.vaults.credentials.create(
          vault_id=vault.id,
          display_name="Alice's Slack",
          auth={
              "type": "mcp_oauth",
              "mcp_server_url": "https://mcp.slack.com/mcp",
              "access_token": "xoxp-...",
              "expires_at": "2099-12-31T23:59:59Z",
              "refresh": {
                  "token_endpoint": "https://slack.com/api/oauth.v2.access",
                  "client_id": "1234567890.0987654321",
                  "scope": "channels:read chat:write",
                  "refresh_token": "xoxe-1-...",
                  "token_endpoint_auth": {"type": "client_secret_post", "client_secret": "abc123..."},
              },
          },
      )
      ```

      ```typescript TypeScript
      const credential = await client.beta.vaults.credentials.create(vault.id, {
        display_name: "Alice's Slack",
        auth: {
          type: "mcp_oauth",
          mcp_server_url: "https://mcp.slack.com/mcp",
          access_token: "xoxp-...",
          expires_at: "2099-12-31T23:59:59Z",
          refresh: {
            token_endpoint: "https://slack.com/api/oauth.v2.access",
            client_id: "1234567890.0987654321",
            scope: "channels:read chat:write",
            refresh_token: "xoxe-1-...",
            token_endpoint_auth: {
              type: "client_secret_post",
              client_secret: "abc123...",
            },
          },
        },
      });
      ```

      ```csharp C#
      var credential = await client.Beta.Vaults.Credentials.Create(vault.ID, new()
      {
          DisplayName = "Alice's Slack",
          Auth = new BetaManagedAgentsMcpOAuthCreateParams
          {
              Type = BetaManagedAgentsMcpOAuthCreateParamsType.McpOAuth,
              McpServerUrl = "https://mcp.slack.com/mcp",
              AccessToken = "xoxp-...",
              ExpiresAt = DateTimeOffset.Parse("2099-12-31T23:59:59Z"),
              Refresh = new()
              {
                  TokenEndpoint = "https://slack.com/api/oauth.v2.access",
                  ClientID = "1234567890.0987654321",
                  Scope = "channels:read chat:write",
                  RefreshToken = "xoxe-1-...",
                  TokenEndpointAuth = new BetaManagedAgentsTokenEndpointAuthPostParam
                  {
                      Type = BetaManagedAgentsTokenEndpointAuthPostParamType.ClientSecretPost,
                      ClientSecret = "abc123...",
                  },
              },
          },
      });
      ```

      ```go Go
      credential, err := client.Beta.Vaults.Credentials.New(ctx, vault.ID, anthropic.BetaVaultCredentialNewParams{
      	DisplayName: anthropic.String("Alice's Slack"),
      	Auth: anthropic.BetaVaultCredentialNewParamsAuthUnion{
      		OfMCPOAuth: &anthropic.BetaManagedAgentsMCPOAuthCreateParams{
      			Type:         anthropic.BetaManagedAgentsMCPOAuthCreateParamsTypeMCPOAuth,
      			MCPServerURL: "https://mcp.slack.com/mcp",
      			AccessToken:  "xoxp-...",
      			ExpiresAt:    anthropic.Time(time.Date(2099, time.December, 31, 23, 59, 59, 0, time.UTC)),
      			Refresh: anthropic.BetaManagedAgentsMCPOAuthRefreshParams{
      				TokenEndpoint: "https://slack.com/api/oauth.v2.access",
      				ClientID:      "1234567890.0987654321",
      				Scope:         anthropic.String("channels:read chat:write"),
      				RefreshToken:  "xoxe-1-...",
      				TokenEndpointAuth: anthropic.BetaManagedAgentsMCPOAuthRefreshParamsTokenEndpointAuthUnion{
      					OfClientSecretPost: &anthropic.BetaManagedAgentsTokenEndpointAuthPostParam{
      						Type:         anthropic.BetaManagedAgentsTokenEndpointAuthPostParamTypeClientSecretPost,
      						ClientSecret: "abc123...",
      					},
      				},
      			},
      		},
      	},
      })
      if err != nil {
      	panic(err)
      }
      ```

      ```java Java
      var credential = client.beta().vaults().credentials().create(vault.id(),
          CredentialCreateParams.builder()
              .displayName("Alice's Slack")
              .auth(BetaManagedAgentsMcpOAuthCreateParams.builder()
                  .type(BetaManagedAgentsMcpOAuthCreateParams.Type.MCP_OAUTH)
                  .mcpServerUrl("https://mcp.slack.com/mcp")
                  .accessToken("xoxp-...")
                  .expiresAt(OffsetDateTime.parse("2099-12-31T23:59:59Z"))
                  .refresh(BetaManagedAgentsMcpOAuthRefreshParams.builder()
                      .tokenEndpoint("https://slack.com/api/oauth.v2.access")
                      .clientId("1234567890.0987654321")
                      .scope("channels:read chat:write")
                      .refreshToken("xoxe-1-...")
                      .clientSecretPostTokenEndpointAuth("abc123...")
                      .build())
                  .build())
              .build());
      ```

      ```php PHP
      $credential = $client->beta->vaults->credentials->create(
          vaultID: $vault->id,
          displayName: "Alice's Slack",
          auth: ManagedAgentsMCPOAuthCreateParams::with(
              type: 'mcp_oauth',
              mcpServerURL: 'https://mcp.slack.com/mcp',
              accessToken: 'xoxp-...',
              expiresAt: new DateTimeImmutable('2099-12-31T23:59:59Z'),
              refresh: ManagedAgentsMCPOAuthRefreshParams::with(
                  tokenEndpoint: 'https://slack.com/api/oauth.v2.access',
                  clientID: '1234567890.0987654321',
                  scope: 'channels:read chat:write',
                  refreshToken: 'xoxe-1-...',
                  tokenEndpointAuth: ManagedAgentsTokenEndpointAuthPostParam::with(
                      type: 'client_secret_post',
                      clientSecret: 'abc123...',
                  ),
              ),
          ),
      );
      ```

      ```ruby Ruby
      credential = client.beta.vaults.credentials.create(
        vault.id,
        display_name: "Alice's Slack",
        auth: {
          type: "mcp_oauth",
          mcp_server_url: "https://mcp.slack.com/mcp",
          access_token: "xoxp-...",
          expires_at: "2099-12-31T23:59:59Z",
          refresh: {
            token_endpoint: "https://slack.com/api/oauth.v2.access",
            client_id: "1234567890.0987654321",
            scope: "channels:read chat:write",
            refresh_token: "xoxe-1-...",
            token_endpoint_auth: {
              type: "client_secret_post",
              client_secret: "abc123..."
            }
          }
        }
      )
      ```
    </CodeGroup>
  </Tab>

  <Tab title="MCP static bearer">
    Use `static_bearer` when the MCP server accepts a fixed bearer token (API key, personal access token, or similar). No refresh flow is needed.

    <CodeGroup defaultLanguage="CLI">
      ```bash curl
      curl --fail-with-body -sS "https://api.anthropic.com/v1/vaults/$vault_id/credentials" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        --data @- <<'EOF'
      {
        "display_name": "Linear API key",
        "auth": {
          "type": "static_bearer",
          "mcp_server_url": "https://mcp.linear.app/mcp",
          "token": "lin_api_your_linear_key"
        }
      }
      EOF
      ```

      ```bash CLI
      ant beta:vaults:credentials create --vault-id "$VAULT_ID" <<'YAML'
      display_name: Linear API key
      auth:
        type: static_bearer
        mcp_server_url: https://mcp.linear.app/mcp
        token: lin_api_your_linear_key
      YAML
      ```

      ```python Python
      bearer_credential = client.beta.vaults.credentials.create(
          vault_id=vault.id,
          display_name="Linear API key",
          auth={
              "type": "static_bearer",
              "mcp_server_url": "https://mcp.linear.app/mcp",
              "token": "lin_api_your_linear_key",
          },
      )
      ```

      ```typescript TypeScript
      const bearerCredential = await client.beta.vaults.credentials.create(vault.id, {
        display_name: "Linear API key",
        auth: {
          type: "static_bearer",
          mcp_server_url: "https://mcp.linear.app/mcp",
          token: "lin_api_your_linear_key",
        },
      });
      ```

      ```csharp C#
      var bearerCredential = await client.Beta.Vaults.Credentials.Create(vault.ID, new()
      {
          DisplayName = "Linear API key",
          Auth = new BetaManagedAgentsStaticBearerCreateParams
          {
              Type = BetaManagedAgentsStaticBearerCreateParamsType.StaticBearer,
              McpServerUrl = "https://mcp.linear.app/mcp",
              Token = "lin_api_your_linear_key",
          },
      });
      ```

      ```go Go
      bearerCredential, err := client.Beta.Vaults.Credentials.New(ctx, vault.ID, anthropic.BetaVaultCredentialNewParams{
      	DisplayName: anthropic.String("Linear API key"),
      	Auth: anthropic.BetaVaultCredentialNewParamsAuthUnion{
      		OfStaticBearer: &anthropic.BetaManagedAgentsStaticBearerCreateParams{
      			Type:         anthropic.BetaManagedAgentsStaticBearerCreateParamsTypeStaticBearer,
      			MCPServerURL: "https://mcp.linear.app/mcp",
      			Token:        "lin_api_your_linear_key",
      		},
      	},
      })
      if err != nil {
      	panic(err)
      }
      _ = bearerCredential
      ```

      ```java Java
      var bearerCredential = client.beta().vaults().credentials().create(vault.id(),
          CredentialCreateParams.builder()
              .displayName("Linear API key")
              .auth(BetaManagedAgentsStaticBearerCreateParams.builder()
                  .type(BetaManagedAgentsStaticBearerCreateParams.Type.STATIC_BEARER)
                  .mcpServerUrl("https://mcp.linear.app/mcp")
                  .token("lin_api_your_linear_key")
                  .build())
              .build());
      ```

      ```php PHP
      $bearerCredential = $client->beta->vaults->credentials->create(
          vaultID: $vault->id,
          displayName: 'Linear API key',
          auth: ManagedAgentsStaticBearerCreateParams::with(
              type: 'static_bearer',
              mcpServerURL: 'https://mcp.linear.app/mcp',
              token: 'lin_api_your_linear_key',
          ),
      );
      ```

      ```ruby Ruby
      bearer_credential = client.beta.vaults.credentials.create(
        vault.id,
        display_name: "Linear API key",
        auth: {
          type: "static_bearer",
          mcp_server_url: "https://mcp.linear.app/mcp",
          token: "lin_api_your_linear_key"
        }
      )
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Environment variable">
    Use `environment_variable` to authenticate to external services through an environment variable, such as CLIs, SDKs, or direct API calls. Environment variable credentials work for clients that send the secret value verbatim in an outbound request, so check the client eligibility criteria in this tab before configuring one.

    The `networking.allowed_hosts` array controls which outbound hosts the secret can be substituted for. Use `"type": "limited"` with a specific list, or `"type": "unrestricted"` if the caller reaches domains you can't enumerate in advance.

    Limiting domains is strongly recommended for security purposes, and prevents your key from ever being shared with unauthorized hosts.

    <Note>
      `networking.allowed_hosts` on a vault credential controls which requests use the secret, not which requests are allowed. For the agent to actually reach a domain, it must also be allowed at the [environment level](/docs/en/managed-agents/environments). Both levels must include the domain (either through `unrestricted` networking or by explicitly listing the domain in `allowed_hosts`) for a secret-substituted request to succeed.
    </Note>

    The optional `injection_location` field scopes where the secret is substituted; the full semantics follow the example.

    <CodeGroup defaultLanguage="CLI">
      ```bash curl
      curl --fail-with-body -sS "https://api.anthropic.com/v1/vaults/$vault_id/credentials" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        --data @- <<'EOF' | jq '.auth.injection_location'
      {
        "auth": {
          "type": "environment_variable",
          "secret_name": "NOTION_API_KEY",
          "secret_value": "ntn_your-secret-here",
          "networking": {
            "type": "limited",
            "allowed_hosts": ["api.notion.com"]
          },
          "injection_location": {"header": true}
        },
        "display_name": "Notion API key for sandbox"
      }
      EOF
      ```

      ```bash CLI
      ant beta:vaults:credentials create \
        --vault-id "$VAULT_ID" \
        --transform 'auth.injection_location' --format json <<'YAML'
      display_name: Notion API key for sandbox
      auth:
        type: environment_variable
        secret_name: NOTION_API_KEY
        secret_value: ntn_your-secret-here
        injection_location:
          header: true
        networking:
          type: limited
          allowed_hosts: [api.notion.com]
      YAML
      ```

      ```python Python
      env_credential = client.beta.vaults.credentials.create(
          vault_id=vault.id,
          display_name="Notion API key for sandbox",
          auth={
              "type": "environment_variable",
              "secret_name": "NOTION_API_KEY",
              "secret_value": "ntn_your-secret-here",
              "networking": {
                  "type": "limited",
                  "allowed_hosts": ["api.notion.com"],
              },
              "injection_location": {"header": True},
          },
      )
      if env_credential.auth.type == "environment_variable":
          location = env_credential.auth.injection_location
          print(f"header: {location.header}, body: {location.body}")  # header: True, body: False
      ```

      ```typescript TypeScript
      const envVarCredential = await client.beta.vaults.credentials.create(vault.id, {
        display_name: "Notion API key for sandbox",
        auth: {
          type: "environment_variable",
          secret_name: "NOTION_API_KEY",
          secret_value: "ntn_your-secret-here",
          networking: {
            type: "limited",
            allowed_hosts: ["api.notion.com"],
          },
          injection_location: { header: true },
        },
      });
      if (envVarCredential.auth.type === "environment_variable") {
        console.log(envVarCredential.auth.injection_location); // { header: true, body: false }
      }
      ```

      ```csharp C#
      var envVarCredential = await client.Beta.Vaults.Credentials.Create(vault.ID, new()
      {
          DisplayName = "Notion API key for sandbox",
          Auth = new BetaManagedAgentsEnvironmentVariableCreateParams
          {
              Type = BetaManagedAgentsEnvironmentVariableCreateParamsType.EnvironmentVariable,
              SecretName = "NOTION_API_KEY",
              SecretValue = "ntn_your-secret-here",
              Networking = new BetaManagedAgentsLimitedCredentialNetworkingParams
              {
                  Type = BetaManagedAgentsLimitedCredentialNetworkingParamsType.Limited,
                  AllowedHosts = ["api.notion.com"],
              },
              InjectionLocation = new() { Header = true },
          },
      });
      if (envVarCredential.Auth.TryPickBetaManagedAgentsEnvironmentVariableAuthResponse(out var envVarAuth))
      {
          var injectionLocation = envVarAuth.InjectionLocation;
          Console.WriteLine($"Header: {injectionLocation.Header}, Body: {injectionLocation.Body}"); // "Header: True, Body: False"
      }
      ```

      ```go Go
      envVarCredential, err := client.Beta.Vaults.Credentials.New(ctx, vault.ID, anthropic.BetaVaultCredentialNewParams{
      	DisplayName: anthropic.String("Notion API key for sandbox"),
      	Auth: anthropic.BetaVaultCredentialNewParamsAuthUnion{
      		OfEnvironmentVariable: &anthropic.BetaManagedAgentsEnvironmentVariableCreateParams{
      			Type:        anthropic.BetaManagedAgentsEnvironmentVariableCreateParamsTypeEnvironmentVariable,
      			SecretName:  "NOTION_API_KEY",
      			SecretValue: "ntn_your-secret-here",
      			Networking: anthropic.BetaManagedAgentsCredentialNetworkingParamsUnion{
      				OfLimited: &anthropic.BetaManagedAgentsLimitedCredentialNetworkingParams{
      					Type:         anthropic.BetaManagedAgentsLimitedCredentialNetworkingParamsTypeLimited,
      					AllowedHosts: []string{"api.notion.com"},
      				},
      			},
      			InjectionLocation: anthropic.BetaManagedAgentsInjectionLocationParams{
      				Header: anthropic.Bool(true),
      			},
      		},
      	},
      })
      if err != nil {
      	panic(err)
      }
      if envVarAuth, ok := envVarCredential.Auth.AsAny().(anthropic.BetaManagedAgentsEnvironmentVariableAuthResponse); ok {
      	injectionLocation := envVarAuth.InjectionLocation
      	fmt.Printf("Header:%t Body:%t\n", injectionLocation.Header, injectionLocation.Body) // "Header:true Body:false"
      }
      ```

      ```java Java
      var envVarCredential = client.beta().vaults().credentials().create(vault.id(),
          CredentialCreateParams.builder()
              .displayName("Notion API key for sandbox")
              .auth(BetaManagedAgentsEnvironmentVariableCreateParams.builder()
                  .type(BetaManagedAgentsEnvironmentVariableCreateParams.Type.ENVIRONMENT_VARIABLE)
                  .secretName("NOTION_API_KEY")
                  .secretValue("ntn_your-secret-here")
                  .limitedNetworking(List.of("api.notion.com"))
                  .injectionLocation(BetaManagedAgentsInjectionLocationParams.builder()
                      .header(true)
                      .build())
                  .build())
              .build());
      envVarCredential.auth().environmentVariable().ifPresent(envVarAuth -> {
          var injectionLocation = envVarAuth.injectionLocation();
          IO.println("header=" + injectionLocation.header() + " body=" + injectionLocation.body()); // header=true body=false
      });
      ```

      ```php PHP
      $envVarCredential = $client->beta->vaults->credentials->create(
          vaultID: $vault->id,
          displayName: 'Notion API key for sandbox',
          auth: ManagedAgentsEnvironmentVariableCreateParams::with(
              type: ManagedAgentsEnvironmentVariableCreateParams\Type::ENVIRONMENT_VARIABLE,
              secretName: 'NOTION_API_KEY',
              secretValue: 'ntn_your-secret-here',
              networking: ManagedAgentsLimitedCredentialNetworkingParams::with(
                  type: ManagedAgentsLimitedCredentialNetworkingParams\Type::LIMITED,
                  allowedHosts: ['api.notion.com'],
              ),
              injectionLocation: ManagedAgentsInjectionLocationParams::with(header: true),
          ),
      );
      if ($envVarCredential->auth instanceof ManagedAgentsEnvironmentVariableAuthResponse) {
          $injectionLocation = $envVarCredential->auth->injectionLocation;
          echo 'header: ' . json_encode($injectionLocation->header) . "\n"; // header: true
          echo 'body: ' . json_encode($injectionLocation->body) . "\n"; // body: false
      }
      ```

      ```ruby Ruby
      env_credential = client.beta.vaults.credentials.create(
        vault.id,
        display_name: "Notion API key for sandbox",
        auth: {
          type: "environment_variable",
          secret_name: "NOTION_API_KEY",
          secret_value: "ntn_your-secret-here",
          networking: {
            type: "limited",
            allowed_hosts: ["api.notion.com"]
          },
          injection_location: {header: true}
        }
      )
      if env_credential.auth.type == :environment_variable
        env_credential.auth.injection_location => {header:, body:}
        puts "header: #{header}, body: #{body}" # header: true, body: false
      end
      ```
    </CodeGroup>

    Request payloads are often assembled from content the agent is working with, so the request body is the broader exposure surface. Most services read an API key from a request header, so enabling only `header` is the narrower configuration. It scopes substitution to request header values for that credential.

    The credential's `injection_location` controls which parts of an outbound request the secret is substituted into. It is an optional object, a sibling of `networking`, with two Boolean fields: `header` (request headers) and `body` (request body). `injection_location` is independent of `networking.allowed_hosts`: `allowed_hosts` scopes which hosts the secret is substituted for, and `injection_location` scopes which parts of the request it is substituted into.

    `injection_location` behaves differently on create and on update:

    | Operation         | `injection_location` behavior                                                                                                                                                              |
    | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | Create credential | If you provide the object, any field you omit inside it defaults to `false`: `{"header": true}` creates a header-only credential. Omit the object entirely and both locations are enabled. |
    | Update credential | Fields merge individually: `{"body": false}` disables body substitution and leaves `header` unchanged.                                                                                     |

    A credential must have at least one location enabled, so a create or update that would disable both locations returns a 400 error. Passing an explicit `null` for the `injection_location` object or for either field also returns a 400 error ("omit the field instead"). The response always returns both fields with their resolved values.

    A placeholder in a disabled location is neither substituted nor stripped. The request is sent to the third party with the literal opaque placeholder string in that location. If a request arrives at the third party containing the literal placeholder string, either that location is disabled for the credential or the destination host is not covered by the credential's `networking.allowed_hosts`.

    The substitution happens at egress, not inside the sandbox. Anything that processes the credential locally sees the opaque placeholder, not the real value: clients that validate the credential format at startup may reject it, and clients that compute a request signature from the secret (for example, AWS SigV4) produce an invalid signature. Environment variable credentials work for clients that send the secret value verbatim in an outbound request, in a location the credential's `injection_location` enables.

    Substitution is outbound only. If a client uses the stored secret to fetch a session token (for example, an OAuth client-credentials grant), the returned token arrives in the sandbox unredacted. For exchange-based flows, perform the exchange yourself and store the resulting token in the vault instead.

    <Tip>
      Scope the API key to only the permissions the agent needs. The agent can do anything the key allows, so a key with broader permissions than necessary increases the blast radius if the agent behaves unexpectedly.
    </Tip>
  </Tab>
</Tabs>

Credentials are stored as provided and are not validated until session runtime. An invalid credential surfaces as an authentication or downstream error during the session, which is emitted but does not block the session from continuing.

Constraints:

* **Unique key per vault.** `mcp_server_url` (MCP credentials) and `secret_name` (environment variable credentials) must be unique among active credentials in a vault. Creating a duplicate returns a 409.
* **Keys are immutable.** To change `mcp_server_url` or `secret_name`, archive the credential and create a new one.
* **Maximum 20 credentials per vault.**

## Reference the vault at session creation

Pass `vault_ids` when creating a session:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  session_id=$(curl --fail-with-body -sS https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<EOF | jq -r '.id'
  {
    "agent": "$agent_id",
    "environment_id": "$environment_id",
    "vault_ids": ["$vault_id"],
    "title": "Alice's Slack digest"
  }
  EOF
  )
  ```

  ```bash CLI
  SESSION_ID=$(ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID" \
    --vault-id "$VAULT_ID" \
    --title "Alice's Slack digest" \
    --transform id --raw-output)
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      vault_ids=[vault.id],
      title="Alice's Slack digest",
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    vault_ids: [vault.id],
    title: "Alice's Slack digest",
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      VaultIds = [vault.ID],
      Title = "Alice's Slack digest",
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(agent.ID),
  	},
  	EnvironmentID: environment.ID,
  	VaultIDs:      []string{vault.ID},
  	Title:         anthropic.String("Alice's Slack digest"),
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(agent.id())
      .environmentId(environment.id())
      .vaultIds(List.of(vault.id()))
      .title("Alice's Slack digest")
      .build());
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      vaultIDs: [$vault->id],
      title: "Alice's Slack digest",
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    vault_ids: [vault.id],
    title: "Alice's Slack digest"
  )
  ```
</CodeGroup>

Runtime behavior:

* When no MCP credential matches by `mcp_server_url`, the connection is attempted unauthenticated and will error if the server requires authentication.
* When multiple vaults contain a matching credential, the first vault with a match wins.
* In [multi-agent sessions](/docs/en/managed-agents/multi-agent), vault credentials apply to every thread. An agent whose own definition declares the matching MCP server authenticates with these credentials. See [Connect agents to MCP servers](/docs/en/managed-agents/multi-agent#connect-agents-to-mcp-servers).

## Rotate a credential

Secret values, `display_name`, and (on environment variable credentials) `injection_location` can be updated. `injection_location` updates merge per field, as described in the Environment variable tab of [Add a credential](#add-a-credential). For a running session, an `injection_location` update propagates the same way as a secret rotation: the session's credentials are re-resolved without a restart, as described in [Credential lifecycle](#credential-lifecycle), and the updated locations apply to the session's subsequent outbound requests. Structural fields (`mcp_server_url`, `secret_name`, `token_endpoint`, `client_id`) are locked after creation. To change them, archive the credential and create a new one.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/vaults/$vault_id/credentials/$credential_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<'EOF' > /dev/null
  {
    "auth": {
      "type": "mcp_oauth",
      "access_token": "xoxp-new-...",
      "expires_at": "2099-12-31T23:59:59Z",
      "refresh": {"refresh_token": "xoxe-1-new-..."}
    }
  }
  EOF
  ```

  ```bash CLI
  ant beta:vaults:credentials update \
    --vault-id "$VAULT_ID" \
    --credential-id "$CREDENTIAL_ID" <<'YAML'
  auth:
    type: mcp_oauth
    access_token: xoxp-new-...
    expires_at: "2099-12-31T23:59:59Z"
    refresh:
      refresh_token: xoxe-1-new-...
  YAML
  ```

  ```python Python
  client.beta.vaults.credentials.update(
      credential.id,
      vault_id=vault.id,
      auth={
          "type": "mcp_oauth",
          "access_token": "xoxp-new-...",
          "expires_at": "2099-12-31T23:59:59Z",
          "refresh": {"refresh_token": "xoxe-1-new-..."},
      },
  )
  ```

  ```typescript TypeScript
  await client.beta.vaults.credentials.update(credential.id, {
    vault_id: vault.id,
    auth: {
      type: "mcp_oauth",
      access_token: "xoxp-new-...",
      expires_at: "2099-12-31T23:59:59Z",
      refresh: {
        refresh_token: "xoxe-1-new-...",
      },
    },
  });
  ```

  ```csharp C#
  await client.Beta.Vaults.Credentials.Update(credential.ID, new()
  {
      VaultID = vault.ID,
      Auth = new BetaManagedAgentsMcpOAuthUpdateParams
      {
          Type = BetaManagedAgentsMcpOAuthUpdateParamsType.McpOAuth,
          AccessToken = "xoxp-new-...",
          ExpiresAt = DateTimeOffset.Parse("2099-12-31T23:59:59Z"),
          Refresh = new() { RefreshToken = "xoxe-1-new-..." },
      },
  });
  ```

  ```go Go
  _, err = client.Beta.Vaults.Credentials.Update(ctx, credential.ID, anthropic.BetaVaultCredentialUpdateParams{
  	VaultID: vault.ID,
  	Auth: anthropic.BetaVaultCredentialUpdateParamsAuthUnion{
  		OfMCPOAuth: &anthropic.BetaManagedAgentsMCPOAuthUpdateParams{
  			Type:        anthropic.BetaManagedAgentsMCPOAuthUpdateParamsTypeMCPOAuth,
  			AccessToken: anthropic.String("xoxp-new-..."),
  			ExpiresAt:   anthropic.Time(time.Date(2099, time.December, 31, 23, 59, 59, 0, time.UTC)),
  			Refresh: anthropic.BetaManagedAgentsMCPOAuthRefreshUpdateParams{
  				RefreshToken: anthropic.String("xoxe-1-new-..."),
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().vaults().credentials().update(credential.id(),
      CredentialUpdateParams.builder()
          .vaultId(vault.id())
          .auth(BetaManagedAgentsMcpOAuthUpdateParams.builder()
              .type(BetaManagedAgentsMcpOAuthUpdateParams.Type.MCP_OAUTH)
              .accessToken("xoxp-new-...")
              .expiresAt(OffsetDateTime.parse("2099-12-31T23:59:59Z"))
              .refresh(BetaManagedAgentsMcpOAuthRefreshUpdateParams.builder()
                  .refreshToken("xoxe-1-new-...")
                  .build())
              .build())
          .build());
  ```

  ```php PHP
  $client->beta->vaults->credentials->update(
      $credential->id,
      vaultID: $vault->id,
      auth: ManagedAgentsMCPOAuthUpdateParams::with(
          type: 'mcp_oauth',
          accessToken: 'xoxp-new-...',
          expiresAt: new DateTimeImmutable('2099-12-31T23:59:59Z'),
          refresh: ManagedAgentsMCPOAuthRefreshUpdateParams::with(refreshToken: 'xoxe-1-new-...'),
      ),
  );
  ```

  ```ruby Ruby
  client.beta.vaults.credentials.update(
    credential.id,
    vault_id: vault.id,
    auth: {
      type: "mcp_oauth",
      access_token: "xoxp-new-...",
      expires_at: "2099-12-31T23:59:59Z",
      refresh: {refresh_token: "xoxe-1-new-..."}
    }
  )
  ```
</CodeGroup>

## Credential lifecycle

Credentials are re-resolved periodically, both during a session and during the vault lifecycle. This ensures that credential rotation, archival, or deletion propagates to running sessions without a restart.

To be notified if a credential is archived, deleted, or fails to refresh, you can subscribe to the vault and credential [webhooks](/docs/en/managed-agents/webhooks) associated with those lifecycle changes.

| Event                             | Trigger                                                                                                              |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `vault.archived`                  | Vault archived. A `vault_credential.archived` event is also emitted for each underlying credential.                  |
| `vault.deleted`                   | Vault deleted. A `vault_credential.deleted` event is also emitted for each underlying credential.                    |
| `vault_credential.archived`       | Credential archived, either directly or as a result of vault archival.                                               |
| `vault_credential.deleted`        | Credential deleted, either directly or as a result of vault deletion.                                                |
| `vault_credential.refresh_failed` | An `mcp_oauth` credential cannot be refreshed (invalid refresh token, or irrecoverable error from the OAuth server). |

<Note>
  This is a non-exhaustive list of webhooks; see [Subscribe to webhooks](/docs/en/managed-agents/webhooks) for the complete list.
</Note>

For `mcp_oauth` credentials, re-resolution also refreshes the access token if it has expired. If the refresh fails, a `vault_credential.refresh_failed` event is emitted.

### Diagnose an OAuth refresh failure

To diagnose why a refresh failed, call `POST /v1/vaults/{vault_id}/credentials/{credential_id}/mcp_oauth_validate` (or `client.beta.vaults.credentials.mcp_oauth_validate(...)` in the SDK). This lets you decide how to handle the failure; the right action depends on the error type.

The top-level `status` tells you what to do next:

* `valid`: the token works; no action needed.
* `invalid`: the grant is gone or the OAuth server rejected the refresh with a 4xx. Prompt the end user to re-authorize.
* `unknown`: a transient error (5xx, 429, or network failure). Wait and retry.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl --fail-with-body -sS -X POST \
    "https://api.anthropic.com/v1/vaults/$vault_id/credentials/$credential_id/mcp_oauth_validate?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"
  ```

  ```bash CLI
  ant beta:vaults:credentials mcp-oauth-validate \
    --vault-id "$VAULT_ID" \
    --credential-id "$CREDENTIAL_ID" \
    --transform status --raw-output  # "valid", "invalid", or "unknown"
  ```

  ```python Python
  validation = client.beta.vaults.credentials.mcp_oauth_validate(
      credential.id,
      vault_id=vault.id,
  )
  print(validation.status)  # "valid", "invalid", or "unknown"
  ```

  ```typescript TypeScript
  const validation = await client.beta.vaults.credentials.mcpOAuthValidate(
    credential.id,
    { vault_id: vault.id },
  );
  console.log(validation.status); // "valid", "invalid", or "unknown"
  ```

  ```csharp C#
  var validation = await client.Beta.Vaults.Credentials.McpOAuthValidate(credential.ID, new()
  {
      VaultID = vault.ID,
  });
  Console.WriteLine(validation.Status.Raw()); // "valid", "invalid", or "unknown"
  ```

  ```go Go
  validation, err := client.Beta.Vaults.Credentials.MCPOAuthValidate(ctx, credential.ID, anthropic.BetaVaultCredentialMCPOAuthValidateParams{
  	VaultID: vault.ID,
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(validation.Status) // "valid", "invalid", or "unknown"
  ```

  ```java Java
  var validation = client.beta().vaults().credentials().mcpOAuthValidate(credential.id(),
      CredentialMcpOAuthValidateParams.builder()
          .vaultId(vault.id())
          .build());
  IO.println(validation.status()); // valid, invalid, or unknown
  ```

  ```php PHP
  $validation = $client->beta->vaults->credentials->mcpOAuthValidate(
      $credential->id,
      vaultID: $vault->id,
  );
  echo $validation->status . "\n"; // "valid", "invalid", or "unknown"
  ```

  ```ruby Ruby
  validation = client.beta.vaults.credentials.mcp_oauth_validate(
    credential.id,
    vault_id: vault.id
  )
  puts validation.status # :valid, :invalid, or :unknown
  ```
</CodeGroup>

The response is a `vault_credential_validation` object. `mcp_probe` includes the failed MCP handshake step; `refresh` includes the outcome of the attempted refresh.

```json
{
  "type": "vault_credential_validation",
  "credential_id": "vcrd_01ABC...",
  "vault_id": "vlt_01XYZ...",
  "validated_at": "2026-04-29T17:12:00Z",
  "has_refresh_token": false,
  "status": "invalid",
  "mcp_probe": {
    "method": "initialize",
    "http_response": {
      "status_code": 401,
      "content_type": "application/json",
      "body": "{\"error\":\"invalid_token\"}",
      "body_truncated": false
    }
  },
  "refresh": {
    "status": "no_refresh_token",
    "http_response": null
  }
}
```

## Other operations

* **List vaults or credentials:** Paginated, newest first. Archived records are excluded by default (pass `include_archived=true` to include them).
* **Archive a vault:** `POST /v1/vaults/{id}/archive`. Cascades to all credentials. Secrets are purged; records are retained for auditing. Future sessions referencing this vault fail; running sessions continue.
* **Archive a credential:** `POST /v1/vaults/{id}/credentials/{cred_id}/archive`. Purges the secret payload; the credential key (`mcp_server_url` or `secret_name`) remains visible and is freed for a replacement credential.
* **Delete a vault or credential:** Hard delete. The record is not retained. Use archive if you need an audit trail.
