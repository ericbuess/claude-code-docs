# Use WIF with Kubernetes

Authenticate to the Claude API from self-managed Kubernetes clusters using projected service account tokens.

---

Self-managed Kubernetes clusters (kubeadm, k3s, OpenShift, and on-premises distributions) sign OIDC JSON Web Tokens (JWTs) for every pod through [projected service account tokens](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#serviceaccount-token-volume-projection). The cluster's API server acts as the OIDC issuer, and each token's `sub` claim follows the form `system:serviceaccount:<namespace>:<service-account>`. You can find your cluster's issuer URL by reading its discovery document:

```bash cURL
kubectl get --raw /.well-known/openid-configuration | jq -r .issuer
```

<Note>
  The mechanism on this page (projected service-account token, cluster API server as the OIDC issuer) is native to Kubernetes itself, so it underlies every Kubernetes distribution. If you run on a managed Kubernetes service, the cloud provider guides walk through where to find the provider-managed issuer URL: [AWS (EKS)](/docs/en/manage-claude/wif-providers/aws#use-eks-projected-service-account-tokens), [Google Cloud (GKE)](/docs/en/manage-claude/wif-providers/gcp), or [Azure (AKS)](/docs/en/manage-claude/wif-providers/azure). If your cluster runs SPIRE, the SPIRE OIDC Discovery Provider is the issuer rather than the cluster API server; see [SPIFFE](/docs/en/manage-claude/wif-providers/spiffe). For any other distribution or a managed provider not listed there, follow this guide and use the issuer URL your cluster reports.
</Note>

## Prerequisites

* Familiarity with [WIF concepts](/docs/en/manage-claude/workload-identity-federation#concepts): service accounts, federation issuers, and federation rules.

* A Kubernetes cluster with the [`--service-account-issuer`](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/) flag configured on the API server. Most distributions set this by default; kubeadm clusters typically use `https://kubernetes.default.svc.cluster.local`. Your platform team can confirm the value if you don't have direct access to the API server configuration.

* One of the following so Anthropic can validate token signatures:

  * The issuer's JWKS endpoint is reachable from the public internet over HTTPS on port 443, or
  * You can fetch the JWKS from inside the cluster and register it in `inline` mode (covered in [Configure Anthropic](#configure-anthropic)).

* Permission to create service accounts, federation issuers, and federation rules in the Claude Console for your Anthropic organization.

## Configure Kubernetes

Project a service account token into your pod with the audience and lifetime that your federation rule expects. The `serviceAccountToken` projection writes a fresh JWT to the mount path and rotates it before `expirationSeconds` elapses.

```yaml Pod
apiVersion: v1
kind: Pod
metadata:
  name: inference-worker
  namespace: inference
spec:
  serviceAccountName: inference-worker
  volumes:
    - name: anthropic-token
      projected:
        sources:
          - serviceAccountToken:
              audience: https://api.anthropic.com
              expirationSeconds: 3600
              path: token
  containers:
    - name: app
      image: your-registry/inference-worker:latest
      env:
        - name: ANTHROPIC_IDENTITY_TOKEN_FILE
          value: /var/run/secrets/anthropic.com/token
        - name: ANTHROPIC_FEDERATION_RULE_ID
          value: fdrl_...
        - name: ANTHROPIC_ORGANIZATION_ID
          value: 00000000-0000-0000-0000-000000000000
        - name: ANTHROPIC_SERVICE_ACCOUNT_ID
          value: svac_...
        - name: ANTHROPIC_WORKSPACE_ID  # required when the rule covers multiple workspaces
          value: wrkspc_...
      volumeMounts:
        - name: anthropic-token
          mountPath: /var/run/secrets/anthropic.com
          readOnly: true
```

The token issued for this pod carries `sub: "system:serviceaccount:inference:inference-worker"` and `aud: ["https://api.anthropic.com"]`.

## Configure Anthropic

In the Claude Console, open **Settings → Workload identity**, click **Connect workload**, and select the **Kubernetes** tile. The wizard walks you through registering the issuer, creating a service account, and creating a federation rule.

The wizard creates these resources for you. Use the following values whether you enter them in the wizard or send them to the [Admin API](/docs/en/manage-claude/wif-admin-api):

**Federation issuer:** Many self-managed clusters use an issuer URL such as `https://kubernetes.default.svc.cluster.local` that is not reachable from the public internet. If that applies to your cluster, choose the **inline** JWKS source and paste the cluster's keys. Fetch them from inside the cluster:

```bash cURL
kubectl get --raw /openid/v1/jwks
```

Then configure the issuer with the contents of the returned `keys` array (not the surrounding `{"keys": [...]}` wrapper):

```json
{
  "name": "onprem-k8s",
  "issuer_url": "https://kubernetes.default.svc.cluster.local",
  "jwks": {
    "type": "inline",
    "keys": [{ "kty": "RSA", "kid": "...", "n": "...", "e": "AQAB" }]
  }
}
```

In `inline` mode the `issuer_url` is only compared against the JWT's `iss` claim; Anthropic never attempts to reach it. If your issuer is publicly reachable, use `"jwks": {"type": "discovery"}` instead.

<Warning>
  With `inline` keys you are responsible for updating the issuer when the cluster rotates its service account signing key. Rotation is rare (typically only during cluster upgrades), but token exchanges fail with a signature error until you push the new JWKS.
</Warning>

**Federation rule:** Match the service account's `sub` claim and the audience you set on the projected token.

```json
{
  "name": "onprem-inference",
  "issuer_id": "fdis_...",
  "match": {
    "subject_prefix": "system:serviceaccount:inference:inference-worker",
    "audience": "https://api.anthropic.com"
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

Be as specific as the workload allows. Loosen `subject_prefix` to `system:serviceaccount:inference:*` (the trailing `*` makes it a prefix match) only if every service account in the namespace should map to the same Anthropic service account. Add the rule's `fdrl_...` ID to your pod's `ANTHROPIC_FEDERATION_RULE_ID` environment variable.

## Acquire and use the token

The pod spec in [Configure Kubernetes](#configure-kubernetes) sets `ANTHROPIC_IDENTITY_TOKEN_FILE` to the projected mount path, along with `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, and `ANTHROPIC_WORKSPACE_ID`. With those in place, the SDK reads the token from disk on every exchange and refreshes the Anthropic access token automatically.

<CodeGroup>
  ```bash cURL
  JWT=$(cat "$ANTHROPIC_IDENTITY_TOKEN_FILE")

  ACCESS_TOKEN=$(curl -sS https://api.anthropic.com/v1/oauth/token \
    -H "content-type: application/json" \
    --data @- <<JSON | jq -r .access_token
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

  curl https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-6",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }' | jq -r '.content[0].text'
  ```

  ```python Python
  import anthropic

  # Reads ANTHROPIC_IDENTITY_TOKEN_FILE, ANTHROPIC_FEDERATION_RULE_ID,
  # ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, and ANTHROPIC_WORKSPACE_ID
  # from the pod's environment.
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  print(message.content[0].text)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  // Reads ANTHROPIC_IDENTITY_TOKEN_FILE, ANTHROPIC_FEDERATION_RULE_ID,
  // ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, and ANTHROPIC_WORKSPACE_ID
  // from the pod's environment.
  const client = new Anthropic();

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
  // Reads ANTHROPIC_IDENTITY_TOKEN_FILE, ANTHROPIC_FEDERATION_RULE_ID,
  // ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, and ANTHROPIC_WORKSPACE_ID
  // from the pod's environment.
  client := anthropic.NewClient()

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
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var message = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_4_6)
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

  ```bash CLI
  # Reads ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  # ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, and ANTHROPIC_IDENTITY_TOKEN_FILE
  ant messages create \
    --model claude-sonnet-4-6 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```php PHP
  use Anthropic\Client;

  // Reads ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  // ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, and ANTHROPIC_IDENTITY_TOKEN_FILE
  $client = new Client();

  $message = $client->messages->create(
      model: 'claude-sonnet-4-6',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  );
  echo $message->content[0]->text, PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"

  # Reads ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  # ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, and ANTHROPIC_IDENTITY_TOKEN_FILE
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}]
  )
  puts message.content.first.text
  ```
</CodeGroup>

## Verify the setup

A successful exchange returns an `access_token` beginning with `sk-ant-oat01-` and an `expires_in` value in seconds. On `400 invalid_grant`, see [Troubleshoot a failed exchange](/docs/en/manage-claude/wif-reference#troubleshoot-a-failed-exchange); the most common Kubernetes-side cause is a JWKS key mismatch (for `inline` mode, re-fetch with `kubectl get --raw /openid/v1/jwks` and update the issuer).

## Scope your rule

<Warning>
  A `subject_prefix` of `system:serviceaccount:*` matches every service account in the cluster, so any pod can obtain a federated Anthropic token. Without an `audience` matcher, the rule also matches the cluster's default-audience tokens, which every pod already has projected.
</Warning>

Lock the rule's `match` block to the narrowest scope that fits your use case:

* **Pin namespace and service-account name:** Use the full `system:serviceaccount:<namespace>:<name>` value with no trailing `*`.
* **Always set an audience:** Require `audience` on the rule and set the same value on the pod's `serviceAccountToken` projection so default-audience tokens are rejected.
* **Use a separate rule per namespace:** Create a distinct rule and Anthropic service account for each namespace rather than widening one rule.
* **Scope inline-JWKS issuers to one cluster:** When several clusters share an issuer URL, register each cluster's JWKS as its own federation issuer and bind rules to that issuer only.

## Next steps

* [Workload Identity Federation](/docs/en/manage-claude/workload-identity-federation): concepts, the token-exchange flow, and SDK configuration options.
* [WIF reference](/docs/en/manage-claude/wif-reference): environment variables, JWKS source modes, and rule match modes.
