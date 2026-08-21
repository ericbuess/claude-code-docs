---
title: Use WIF with GitHub Actions
url: https://platform.claude.com/docs/en/manage-claude/wif-providers/github-actions
description: Authenticate GitHub Actions workflows to the Claude API with short-lived identity tokens instead of long-lived API keys.
---

Every GitHub Actions workflow run can request a signed identity token from GitHub's hosted issuer at `https://token.actions.githubusercontent.com`. With Workload Identity Federation, your workflow exchanges that token for a short-lived Anthropic access token, so your CI jobs can call the Claude API without an `ANTHROPIC_API_KEY` secret stored in your repository.

The token's `sub` claim encodes the repository and trigger context. For a push to a branch it has the form `repo:<owner>/<repo>:ref:refs/heads/<branch>`. Pull-request runs use `repo:<owner>/<repo>:pull_request`, and environment-gated deployments use `repo:<owner>/<repo>:environment:<name>`. Your federation rule matches against this claim (and others, such as `repository_owner` and `ref`) to decide which workflow runs are allowed to authenticate.

## Prerequisites

* Familiarity with [WIF concepts](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation#concepts): service accounts, federation issuers, and federation rules.
* A GitHub repository where you can edit workflow files and grant the `id-token: write` permission.
* Permission to create service accounts, federation issuers, and federation rules in the Claude Console for your Anthropic organization.
* Your Anthropic organization ID. You can find it in the Claude Console under **Settings → Organization**.

## Configure your workflow

GitHub only issues an identity token to jobs that explicitly request it. Add the `id-token: write` permission at the workflow or job level:

```yaml
permissions:
  id-token: write
  contents: read
```

Inside the job, the runner exposes two environment variables: `ACTIONS_ID_TOKEN_REQUEST_URL` and `ACTIONS_ID_TOKEN_REQUEST_TOKEN`. Call the request URL with the request token as a bearer credential and your chosen audience as a query parameter, then write the returned JSON Web Token (JWT) to a file:

```yaml
- name: Fetch GitHub OIDC token
  run: |
    curl -sS -H "Authorization: Bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" \
      "$ACTIONS_ID_TOKEN_REQUEST_URL&audience=https://api.anthropic.com" \
      | jq -r .value > /tmp/gha-jwt
```

If you prefer JavaScript, `actions/github-script` exposes the same capability through `core.getIDToken(audience)`:

```yaml
- name: Fetch GitHub OIDC token
  uses: actions/github-script@v8
  with:
    script: |
      const fs = require('fs');
      const token = await core.getIDToken('https://api.anthropic.com');
      fs.writeFileSync('/tmp/gha-jwt', token);
```

The decoded token carries claims that describe the workflow run. Your federation rule matches against these:

```json
{
  "iss": "https://token.actions.githubusercontent.com",
  "sub": "repo:your-org/your-repo:ref:refs/heads/main",
  "aud": "https://api.anthropic.com",
  "repository": "your-org/your-repo",
  "repository_owner": "your-org",
  "ref": "refs/heads/main",
  "sha": "abc123...",
  "workflow": "CI",
  "actor": "octocat",
  "event_name": "push"
}
```

See [GitHub's OIDC subject claim reference](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#example-subject-claims) for the full list of `sub` formats.

## Configure Anthropic

In the Claude Console, open **Settings → Workload identity**, click **Connect workload**, and select the **GitHub Actions** tile. The wizard walks you through registering the issuer, creating a service account, and creating a federation rule.

The wizard creates these resources for you. Use the following values whether you enter them in the wizard or send them to the [Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api):

**Federation issuer:** GitHub publishes its OIDC discovery document and JWKS publicly, so use discovery mode. Anthropic refreshes the keys automatically when GitHub rotates them.

```json
{
  "name": "github-actions",
  "issuer_url": "https://token.actions.githubusercontent.com",
  "jwks": { "type": "discovery" }
}
```

**Federation rule:** Match only the workflow runs you intend to trust. See [Restrict which workflows can authenticate](https://platform.claude.com/docs/en/manage-claude/wif-providers/github-actions#restrict-which-workflows-can-authenticate) for how to scope these claims safely.

```json
{
  "name": "gha-main",
  "issuer_id": "fdis_...",
  "match": {
    "subject_prefix": "repo:your-org/your-repo:ref:refs/heads/main",
    "audience": "https://api.anthropic.com",
    "claims": {
      "repository_owner": "your-org"
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

Be as specific as the workload allows. Loosen `subject_prefix` to `repo:your-org/your-repo:*` (paired with a `claims.ref` constraint) only if the rule must match multiple event types from the same repository, because the trailing segment of `sub` varies between `ref:...`, `environment:...`, and `pull_request` events.

## Acquire and use a token

Set the federation environment variables on the job and call the SDK normally. `Anthropic()` reads `ANTHROPIC_IDENTITY_TOKEN_FILE`, exchanges the JWT on the first request, and refreshes the access token automatically before it expires.

<CodeGroup>
  ```yaml Workflow
  name: Call Claude
  on: push

  permissions:
    id-token: write
    contents: read

  jobs:
    call-claude:
      runs-on: ubuntu-latest
      env:
        ANTHROPIC_FEDERATION_RULE_ID: fdrl_...
        ANTHROPIC_ORGANIZATION_ID: 00000000-0000-0000-0000-000000000000
        ANTHROPIC_SERVICE_ACCOUNT_ID: svac_...
        ANTHROPIC_WORKSPACE_ID: wrkspc_...  # required when the rule covers multiple workspaces
        ANTHROPIC_IDENTITY_TOKEN_FILE: /tmp/gha-jwt
      steps:
        - uses: actions/checkout@v5
        - name: Fetch GitHub OIDC token
          run: |
            curl -sS -H "Authorization: Bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" \
              "$ACTIONS_ID_TOKEN_REQUEST_URL&audience=https://api.anthropic.com" \
              | jq -r .value > "$ANTHROPIC_IDENTITY_TOKEN_FILE"
        - name: Run your script
          run: |
            pip install anthropic
            python your_script.py
  ```

  ```bash cURL
  JWT=$(cat /tmp/gha-jwt)

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

  curl https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }' | jq -r '.content[] | select(.type == "text") | .text'
  ```

  ```python Python
  import anthropic

  # Reads ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  # ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, and ANTHROPIC_IDENTITY_TOKEN_FILE
  # from the job environment.
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(next(block.text for block in message.content if block.type == "text"))
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  // Reads ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  // ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, and ANTHROPIC_IDENTITY_TOKEN_FILE
  // from the job environment.
  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-opus-5",
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
  // Reads ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  // ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, and ANTHROPIC_IDENTITY_TOKEN_FILE
  // from the job environment.
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  	},
  })
  if err != nil {
  	panic(err)
  }
  for _, block := range message.Content {
  	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  		fmt.Println(textBlock.Text)
  		break
  	}
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var message = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .build());

  IO.println(message.content());
  ```

  ```csharp C#
  var result = AnthropicCredentials.Resolve()
      ?? throw new InvalidOperationException("No federation credentials found in environment");
  using var client = new AnthropicOidcClient(result);

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus5,
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

  ```bash CLI
  # Reads ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  # ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, and ANTHROPIC_IDENTITY_TOKEN_FILE
  # from the job environment.
  ant messages create \
    --model claude-opus-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```php PHP
  use Anthropic\Client;

  // Reads ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  // ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, and ANTHROPIC_IDENTITY_TOKEN_FILE
  // from the job environment.
  $client = new Client();

  $message = $client->messages->create(
      model: 'claude-opus-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  );
  $textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
  echo $textBlock->text, PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"

  # Reads ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  # ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, and ANTHROPIC_IDENTITY_TOKEN_FILE
  # from the job environment.
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}]
  )
  puts message.content.find { it.type == :text }.text
  ```
</CodeGroup>

Each GitHub-issued identity token expires roughly five minutes after issuance. The token-request endpoint (`ACTIONS_ID_TOKEN_REQUEST_URL`) stays valid for the entire job, so you can fetch a fresh token at any point. The SDK exchanges the token on first use and caches the resulting Anthropic access token. For jobs that run longer than the Anthropic token's lifetime, the SDK re-reads `ANTHROPIC_IDENTITY_TOKEN_FILE` on each refresh, so re-run the fetch step periodically (or wrap it in a background loop) to keep the file current. Alternatively, pass a token-provider callback to the SDK that calls `ACTIONS_ID_TOKEN_REQUEST_URL` directly instead of using the file path.

## Verify the setup

A successful exchange returns an `access_token` beginning with `sk-ant-oat01-` and an `expires_in` value in seconds. A denied exchange returns an opaque `401` `authentication_error` with the fixed message `Authentication failed`, whichever check failed; in most cases the deny reason is recorded on the attempt's entry in the [authentication history page](https://platform.claude.com/settings/workload-identity-federation?tab=history), and [Troubleshoot a failed exchange](https://platform.claude.com/docs/en/manage-claude/wif-reference#troubleshoot-a-failed-exchange) walks the checks in order. The most common GitHub Actions-side cause is the `sub` claim format not matching (its trailing segment varies between `ref:...`, `environment:...`, and `pull_request` events); the history entry shows reason `match_subject_prefix`.

## Restrict which workflows can authenticate

<Warning>
  A `subject_prefix` of `repo:your-org/*` alone matches every repository in your organization, and without a `ref` constraint it also matches `pull_request` runs triggered from forks. Anyone who can open a pull request against a matching repository could obtain a federated Anthropic token.
</Warning>

Lock the rule's `match` block to the narrowest scope that fits your use case:

* **Pin to a single repository:** Use `subject_prefix: "repo:your-org/your-repo:*"` so other repositories in the organization do not match.
* **Pin to a protected branch:** Add `"ref": "refs/heads/main"` (or your release branch) under `claims` so pull-request runs and feature branches do not match.
* **Pin the owner explicitly:** Add `"repository_owner": "your-org"` under `claims` as a defense-in-depth check against `sub` parsing edge cases.
* **Pin to a deployment environment:** For deploy jobs, match `subject_prefix: "repo:your-org/your-repo:environment:production"` and gate that environment with required reviewers in GitHub.

## Next steps

* [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation): full setup walkthrough, environment variables, and credential precedence.
* [Authentication](https://platform.claude.com/docs/en/manage-claude/authentication): how federation compares to API keys.
