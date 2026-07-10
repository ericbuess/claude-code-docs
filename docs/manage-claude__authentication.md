# Authentication

Authenticate to the Claude API with API keys or Workload Identity Federation.

---

The Claude API supports two ways to authenticate requests:

| Method                                                        | Credential                                                                      | Best for                                                                                                                                        |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| [API key](#api-keys)                                          | Static `sk-ant-api...` secret in the `x-api-key` header                         | Local development, prototyping, scripts, and single-tenant servers where you control secret storage                                             |
| [Workload Identity Federation](#workload-identity-federation) | Short-lived bearer token exchanged from your identity provider's identity token | Production workloads on cloud platforms (AWS, Google Cloud, Azure), CI/CD pipelines, and Kubernetes, where you want to eliminate static secrets |

Both methods grant the same access to Claude API endpoints. Choose API keys to get started quickly, and move to Workload Identity Federation when your workload already has a platform-issued identity you can federate.

## API keys

API keys are static secrets that you generate in the Claude Console and pass on every request.

* **Create a key:** Go to [Settings → API keys](https://platform.claude.com/settings/keys) in the Claude Console. You choose an [expiration](#key-expiration) as part of creation. Use [workspaces](https://platform.claude.com/settings/workspaces) to scope keys by project or environment.
* **Send the key:** Set the `x-api-key` header on direct HTTP requests, or set the `ANTHROPIC_API_KEY` environment variable and the [client SDKs](/docs/en/cli-sdks-libraries/overview) pick it up automatically.

```http
POST /v1/messages
x-api-key: YOUR_API_KEY
anthropic-version: 2023-06-01
content-type: application/json
```

Store API keys in a secrets manager, rotate them periodically, and revoke any key you suspect has leaked. You can also set an [expiration](#key-expiration) when you create a key to limit how long a leaked credential stays usable.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }'
  ```

  ```python Python
  client = Anthropic(api_key="my-anthropic-api-key")
  # or, with ANTHROPIC_API_KEY set in the environment:
  client = Anthropic()
  ```

  ```typescript TypeScript
  const client = new Anthropic({ apiKey: "my-anthropic-api-key" });
  // or, with ANTHROPIC_API_KEY set in the environment:
  // const client = new Anthropic();
  ```

  ```go Go
  client := anthropic.NewClient(
  	option.WithAPIKey("sk-ant-api03-..."), // defaults to os.LookupEnv("ANTHROPIC_API_KEY")
  )
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;

  // Explicit
  AnthropicClient client = AnthropicOkHttpClient.builder()
    .apiKey("my-anthropic-api-key")
    .build();

  // From ANTHROPIC_API_KEY (or anthropic.apiKey system property)
  AnthropicClient clientFromEnv = AnthropicOkHttpClient.fromEnv();
  ```

  ```csharp C#
  using Anthropic;

  AnthropicClient client = new() { ApiKey = "my-anthropic-api-key" };
  // Or, with ANTHROPIC_API_KEY set in the environment:
  // AnthropicClient client = new();
  ```

  ```php PHP
  // Reads ANTHROPIC_API_KEY from the environment
  $client = new Client();
  // Or pass the key explicitly:
  $client = new Client(apiKey: 'my-anthropic-api-key');
  ```

  ```ruby Ruby
  anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")
  # or, with ANTHROPIC_API_KEY set in the environment:
  anthropic = Anthropic::Client.new
  ```

  ```bash CLI
  # See /docs/en/cli-sdks-libraries/cli/authentication#api-key for zsh, bash, and Windows variants
  export ANTHROPIC_API_KEY=sk-ant-api03-...
  ```
</CodeGroup>

### Key expiration

When you create an API key from the [API keys page](https://platform.claude.com/settings/keys) in the Claude Console, you choose an expiration: a preset (3 hours, 1 day, 7 days, or 30 days), a custom duration, or **Never** for keys you store in a secrets manager and rotate yourself. If your organization has a maximum expiration policy, the Console limits presets and custom durations to the policy maximum, and **Never** is unavailable. Existing keys keep their current behavior; expiration is set at creation time and cannot be changed afterward. The same expiration choice applies when you [create an Admin API key](/docs/en/manage-claude/admin-api-keys) in the Claude Console.

Anthropic emails the key's creator as the expiration approaches: 7 days before expiration for keys created with a lifetime of at least 14 days, and 1 day before for keys with a lifetime of at least 7 days. Keys with shorter lifetimes expire without a warning email.

After a key expires, requests made with it return a `401 authentication_error`. Create a new key to restore access; expired keys cannot be reactivated.

The Console API keys table shows each key's expiration, and the Admin API reports each key's `expires_at` timestamp on the [List API Keys](/docs/en/api/admin/api_keys/list) and [Get API Key](/docs/en/api/admin/api_keys/retrieve) endpoints, so you can audit and rotate keys before they expire. The field is `null` for keys without an expiration.

Expiration limits the lifetime of a leaked credential, but it is not a substitute for secret hygiene. Regardless of expiration, store keys in a secrets manager and revoke any key you suspect has leaked.

## Workload Identity Federation

Workload Identity Federation (WIF) lets a workload authenticate with a short-lived identity token issued by an identity provider (IdP) you already trust, such as AWS IAM, Google Cloud, or any standards-compliant OIDC issuer (such as GitHub Actions, Kubernetes service accounts, SPIFFE, Microsoft Entra ID, or Okta). The workload exchanges its IdP-issued JWT at `POST /v1/oauth/token` for a short-lived Claude API access token, and the SDK refreshes that token automatically before it expires. There is no `sk-ant-api...` string to mint, distribute, or rotate.

Federation removes long-lived Claude API keys from your environment, which shrinks the blast radius of a leaked credential and lets you manage access with the same IdP controls you already use for cloud resources. It does not, on its own, guarantee end-to-end security: the trust chain is only as strong as your identity provider's configuration, and a long-lived secret one hop upstream (for example, a static cloud credential that can mint IdP tokens) can still undermine it. Pair federation with your provider's controls, such as IP allowlists, MFA, and audit logging.

To configure federation, you create three resources in the Claude Console (a service account, a federation issuer, and a federation rule) and then point your SDK at the rule. See [Workload Identity Federation](/docs/en/manage-claude/workload-identity-federation) for the full setup walkthrough.

## Next steps

<CardGroup cols={2}>
  <Card title="Set up Workload Identity Federation" icon="lock" href="/docs/en/manage-claude/workload-identity-federation">
    Configure issuers, rules, and service accounts, then exchange tokens
  </Card>

  <Card title="Identity provider guides" icon="cloud" href="/docs/en/manage-claude/workload-identity-federation#identity-providers">
    Step-by-step guides for AWS, Google Cloud, Azure, GitHub Actions, Kubernetes, SPIFFE, and Okta
  </Card>

  <Card title="WIF reference" icon="book" href="/docs/en/manage-claude/wif-reference">
    Environment variables, validation rules, profile configuration, and error reference
  </Card>

  <Card title="Client SDKs" icon="code" href="/docs/en/cli-sdks-libraries/overview">
    Python, TypeScript, C#, Go, Java, PHP, Ruby, and the CLI
  </Card>
</CardGroup>
