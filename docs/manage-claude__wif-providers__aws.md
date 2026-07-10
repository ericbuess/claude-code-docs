# Use WIF with AWS

Authenticate AWS workloads on Lambda, EC2, ECS, or EKS to the Claude API with Workload Identity Federation and STS-issued identity tokens.

---

AWS workloads can authenticate to the Claude API without static API keys by exchanging an AWS-signed OIDC identity token. The recommended path calls the AWS STS [`GetWebIdentityToken`](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetWebIdentityToken.html) API, which works anywhere the workload has AWS credentials: Lambda, EC2, ECS, and EKS. EKS workloads can alternatively use the [Kubernetes projected-token path](#use-eks-projected-service-account-tokens), which has fewer configuration steps but only works inside a pod.

This guide shows both paths. For the underlying concepts (service accounts, federation issuers, and federation rules), see [Workload Identity Federation](/docs/en/manage-claude/workload-identity-federation).

## Prerequisites

* Familiarity with [WIF concepts](/docs/en/manage-claude/workload-identity-federation#concepts): service accounts, federation issuers, and federation rules.
* An AWS workload (EKS pod, ECS task, Lambda function, or EC2 instance) with an attached IAM role.
* The `aws` CLI or an AWS SDK available in the workload.
* Permission to create service accounts, federation issuers, and federation rules in the Claude Console for your Anthropic organization.

## Use STS web identity tokens (recommended)

The AWS STS `GetWebIdentityToken` API returns an OIDC token signed by AWS that asserts the caller's IAM identity. Because it uses the workload's ambient AWS credentials, the same integration covers Lambda, EC2, ECS, and EKS.

### Configure AWS

<Steps>
  <Step title="Enable outbound web identity federation for the account">
    This is an account-level flag, off by default. In the AWS console, open **IAM**, choose **Account settings**, and enable **Outbound web identity federation**. To enable it programmatically:

    ```bash
    python3 -c "import boto3; boto3.client('iam').enable_outbound_web_identity_federation()"
    ```

    If this is not enabled, calls to `GetWebIdentityToken` fail with `OutboundWebIdentityFederationDisabledException`.
  </Step>

  <Step title="Grant the workload's IAM role permission to call the API">
    Attach this policy to the IAM role that your Lambda function, EC2 instance, or ECS task runs as:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": ["sts:GetWebIdentityToken"],
          "Resource": "*"
        }
      ]
    }
    ```
  </Step>

  <Step title="Find your account's STS issuer URL">
    After enabling outbound federation, the **IAM > Account settings** page shows a **Get Token Issuer URL** field with a value of the form `https://<uuid>.tokens.sts.global.api.aws`. This URL is unique to your AWS account; copy it for the next step. To retrieve it programmatically:

    ```bash
    python3 -c "import boto3; print(boto3.client('iam').get_outbound_web_identity_federation_info())"
    ```
  </Step>
</Steps>

### Configure Anthropic

In the Claude Console, open **Settings → Workload identity**, click **Connect workload**, and select the **AWS** tile. The wizard walks you through registering the issuer, creating a service account, and creating a federation rule.

The wizard creates these resources for you. Use the following values whether you enter them in the wizard or send them to the [Admin API](/docs/en/manage-claude/wif-admin-api):

**Federation issuer:** Register the per-account STS issuer URL you copied in the prior step. It exposes a public JWKS endpoint, so use discovery mode.

```json
{
  "name": "aws-sts",
  "issuer_url": "https://<uuid>.tokens.sts.global.api.aws",
  "jwks": { "type": "discovery" }
}
```

**Federation rule:** Match the audience you pass to `GetWebIdentityToken` and the calling role's IAM role ARN in the `sub` claim. The `sub` value is the IAM role ARN of the workload that called the API, in the form `arn:aws:iam::<account>:role/<role-name>`. The token also carries an `https://sts.amazonaws.com/` claim with `aws_account`, `org_id`, `principal_id`, and any `request_tags` you passed; you can match on those with the rule's `claims` map or a CEL `condition` for finer control.

```json
{
  "name": "prod-inference",
  "issuer_id": "fdis_...",
  "match": {
    "subject_prefix": "arn:aws:iam::123456789012:role/inference-worker",
    "audience": "https://api.anthropic.com"
  },
  "target": { "type": "service_account", "service_account_id": "svac_..." },
  "workspace_id": "wrkspc_...",
  "oauth_scope": "workspace:developer",
  "token_lifetime_seconds": 600
}
```

Be as specific as the workload allows. Match the exact role ARN, and only broaden `subject_prefix` (for example, to `arn:aws:iam::123456789012:role/*`) if multiple IAM roles should map to the same Anthropic service account.

### Acquire and use the token

Call `GetWebIdentityToken` with `https://api.anthropic.com` as the audience, then pass the result to the SDK's federation credentials. The token provider is a callable, so the SDK re-invokes STS on each refresh.

<Note>
  `GetWebIdentityToken` is available only on regional STS endpoints. If you receive `'STS' object has no attribute 'get_web_identity_token'` or a similar error, pin your STS client to a region (for example, `boto3.client("sts", region_name="us-east-1")`) and ensure your AWS SDK is recent enough to include the API.
</Note>

<CodeGroup>
  ```bash cURL
  JWT=$(aws sts get-web-identity-token \
    --region us-east-1 \
    --audience "https://api.anthropic.com" \
    --signing-algorithm RS256 \
    --duration-seconds 900 \
    --query WebIdentityToken --output text)

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
      "model": "claude-sonnet-4-6",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello from AWS"}]
    }' | jq -r '.content[0].text'
  ```

  ```python Python
  import os

  import anthropic
  import boto3
  from anthropic import WorkloadIdentityCredentials


  def get_sts_web_identity_token() -> str:
      sts = boto3.client("sts", region_name="us-east-1")
      resp = sts.get_web_identity_token(
          Audience=["https://api.anthropic.com"],
          SigningAlgorithm="RS256",
          DurationSeconds=900,
      )
      return resp["WebIdentityToken"]


  client = anthropic.Anthropic(
      credentials=WorkloadIdentityCredentials(
          identity_token_provider=get_sts_web_identity_token,
          federation_rule_id=os.environ["ANTHROPIC_FEDERATION_RULE_ID"],
          organization_id=os.environ["ANTHROPIC_ORGANIZATION_ID"],
          service_account_id=os.environ["ANTHROPIC_SERVICE_ACCOUNT_ID"],
          workspace_id=os.environ.get("ANTHROPIC_WORKSPACE_ID"),
      ),
  )

  message = client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello from AWS"}],
  )
  print(message.content[0].text)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { oidcFederationProvider } from "@anthropic-ai/sdk/lib/credentials/oidc-federation";
  import { STSClient, GetWebIdentityTokenCommand } from "@aws-sdk/client-sts";

  const sts = new STSClient({ region: "us-east-1" });

  async function getStsWebIdentityToken(): Promise<string> {
    const out = await sts.send(
      new GetWebIdentityTokenCommand({
        Audience: ["https://api.anthropic.com"],
        SigningAlgorithm: "RS256",
        DurationSeconds: 900
      })
    );
    return out.WebIdentityToken!;
  }

  const client = new Anthropic({
    credentials: oidcFederationProvider({
      identityTokenProvider: getStsWebIdentityToken,
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
    messages: [{ role: "user", content: "Hello from AWS" }]
  });
  for (const block of message.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```go Go
  ctx := context.TODO()
  cfg, err := config.LoadDefaultConfig(ctx, config.WithRegion("us-east-1"))
  if err != nil {
  	panic(err)
  }
  stsClient := sts.NewFromConfig(cfg)

  getStsToken := option.IdentityTokenFunc(func(ctx context.Context) (string, error) {
  	out, err := stsClient.GetWebIdentityToken(ctx, &sts.GetWebIdentityTokenInput{
  		Audience:         []string{"https://api.anthropic.com"},
  		SigningAlgorithm: "RS256",
  		DurationSeconds:  aws.Int32(900),
  	})
  	if err != nil {
  		return "", err
  	}
  	return *out.WebIdentityToken, nil
  })

  client := anthropic.NewClient(
  	option.WithFederationTokenProvider(getStsToken, option.FederationOptions{
  		FederationRuleID: os.Getenv("ANTHROPIC_FEDERATION_RULE_ID"),
  		OrganizationID:   os.Getenv("ANTHROPIC_ORGANIZATION_ID"),
  		ServiceAccountID: os.Getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"),
  		WorkspaceID:      os.Getenv("ANTHROPIC_WORKSPACE_ID"),
  	}),
  )

  message, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet4_6,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello from AWS")),
  	},
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(message.Content[0].Text)
  ```

  ```java Java
  StsClient sts = StsClient.builder().region(Region.US_EAST_1).build();

  IdentityTokenProvider getStsToken = () -> sts.getWebIdentityToken(
                  GetWebIdentityTokenRequest.builder()
                          .audience("https://api.anthropic.com")
                          .signingAlgorithm("RS256")
                          .durationSeconds(900)
                          .build())
          .webIdentityToken();

  AnthropicClient client = AnthropicOkHttpClient.builder()
          .federationTokenProvider(
                  getStsToken,
                  System.getenv("ANTHROPIC_FEDERATION_RULE_ID"),
                  System.getenv("ANTHROPIC_ORGANIZATION_ID"),
                  System.getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"))
          .build();

  var message = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_4_6)
          .maxTokens(1024)
          .addUserMessage("Hello from AWS")
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
      IdentityTokenProvider = new StsTokenProvider(),
  });
  using var client = new AnthropicOidcClient(credentials);

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeSonnet4_6,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello from AWS" }],
  });
  foreach (var block in message.Content)
  {
      if (block.Value is TextBlock textBlock)
      {
          Console.WriteLine(textBlock.Text);
      }
  }

  class StsTokenProvider : IIdentityTokenProvider
  {
      private readonly AmazonSecurityTokenServiceClient _sts = new(Amazon.RegionEndpoint.USEast1);

      public async Task<string> GetIdentityTokenAsync(CancellationToken ct = default)
      {
          var resp = await _sts.GetWebIdentityTokenAsync(new GetWebIdentityTokenRequest
          {
              Audience = ["https://api.anthropic.com"],
              SigningAlgorithm = "RS256",
              DurationSeconds = 900,
          }, ct);
          return resp.WebIdentityToken;
      }
  }
  ```

  ```bash CLI
  TOKEN_FILE=$(mktemp)
  aws sts get-web-identity-token \
    --region us-east-1 \
    --audience "https://api.anthropic.com" \
    --signing-algorithm RS256 \
    --duration-seconds 900 \
    --query WebIdentityToken --output text > "$TOKEN_FILE"

  export ANTHROPIC_IDENTITY_TOKEN_FILE="$TOKEN_FILE"
  # ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID, and
  # ANTHROPIC_SERVICE_ACCOUNT_ID, and ANTHROPIC_WORKSPACE_ID are read from the environment
  ant messages create \
    --model claude-sonnet-4-6 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello from AWS"}'
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Credentials\WorkloadIdentityCredentials;
  use Aws\Sts\StsClient;

  $sts = new StsClient(['region' => 'us-east-1', 'version' => 'latest']);
  $client = new Client(credentials: new WorkloadIdentityCredentials(
      identityTokenProvider: fn() => $sts->getWebIdentityToken([
          'Audience' => ['https://api.anthropic.com'],
          'SigningAlgorithm' => 'RS256',
          'DurationSeconds' => 900,
      ])['WebIdentityToken'],
      federationRuleId: getenv('ANTHROPIC_FEDERATION_RULE_ID'),
      organizationId: getenv('ANTHROPIC_ORGANIZATION_ID'),
      serviceAccountId: getenv('ANTHROPIC_SERVICE_ACCOUNT_ID'),
      workspaceId: getenv('ANTHROPIC_WORKSPACE_ID') ?: null,
  ));

  $message = $client->messages->create(
      model: 'claude-sonnet-4-6',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello from AWS']],
  );
  echo $message->content[0]->text, PHP_EOL;
  ```

  ```ruby Ruby
  require "anthropic"
  require "aws-sdk-sts"

  sts = Aws::STS::Client.new(region: "us-east-1")
  client = Anthropic::Client.new(
    credentials: Anthropic::WorkloadIdentityCredentials.new(
      identity_token_provider: -> {
        sts.get_web_identity_token(
          audience: ["https://api.anthropic.com"],
          signing_algorithm: "RS256",
          duration_seconds: 900,
        ).web_identity_token
      },
      federation_rule_id: ENV.fetch("ANTHROPIC_FEDERATION_RULE_ID"),
      organization_id: ENV.fetch("ANTHROPIC_ORGANIZATION_ID"),
      service_account_id: ENV.fetch("ANTHROPIC_SERVICE_ACCOUNT_ID"),
      workspace_id: ENV["ANTHROPIC_WORKSPACE_ID"],
    ),
  )

  message = client.messages.create(
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello from AWS"}]
  )
  puts message.content.first.text
  ```
</CodeGroup>

### Verify the setup

From inside the workload, exchange an STS-issued token directly and inspect the response:

```bash cURL
JWT=$(aws sts get-web-identity-token \
  --region us-east-1 \
  --audience "https://api.anthropic.com" \
  --signing-algorithm RS256 \
  --duration-seconds 900 \
  --query WebIdentityToken --output text)

curl -sS https://api.anthropic.com/v1/oauth/token \
  -H "content-type: application/json" \
  -d "{
    \"grant_type\": \"urn:ietf:params:oauth:grant-type:jwt-bearer\",
    \"assertion\": \"$JWT\",
    \"federation_rule_id\": \"fdrl_...\",
    \"organization_id\": \"00000000-0000-0000-0000-000000000000\",
    \"service_account_id\": \"svac_...\",
    \"workspace_id\": \"wrkspc_...\"
  }" | jq
```

A successful exchange returns an `access_token` beginning with `sk-ant-oat01-` and an `expires_in` value in seconds. On `400 invalid_grant`, see [Troubleshoot a failed exchange](/docs/en/manage-claude/wif-reference#troubleshoot-a-failed-exchange); the most common AWS-side cause is an `iss` mismatch (the per-account STS issuer URL must match the registered `issuer_url` exactly).

## Use EKS projected service-account tokens

If your workload runs in an EKS pod, you can skip the STS call and read a Kubernetes-projected service-account token directly from disk. Kubernetes natively projects an OIDC-compatible token into the pod, and the SDK can read it from a file path, so no token-provider callable is required. This path has two fewer AWS configuration steps than the STS path but only works inside a pod; the underlying mechanism is the same as the [generic Kubernetes integration](/docs/en/manage-claude/wif-providers/kubernetes).

This path additionally requires an EKS cluster with an [IAM OIDC provider enabled](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html) and `kubectl` access to the cluster.

### Configure your EKS cluster

<Steps>
  <Step title="Find your cluster's OIDC issuer URL">
    Each EKS cluster has a unique OIDC issuer. Retrieve it with the AWS CLI:

    ```bash CLI
    aws eks describe-cluster \
      --name <cluster-name> \
      --query "cluster.identity.oidc.issuer" \
      --output text
    ```

    The output looks like `https://oidc.eks.us-west-2.amazonaws.com/id/6FA42E7BFDE8549CB...`. You'll register this URL as a federation issuer in the next section.
  </Step>

  <Step title="Create the service account and project an Anthropic-audience token">
    The EKS pod identity webhook detects the `eks.amazonaws.com/role-arn` annotation and automatically projects a token with `aud: sts.amazonaws.com`, exposing its path as `AWS_WEB_IDENTITY_TOKEN_FILE`. That token is for AWS role assumption. For the Anthropic exchange, project a second token with `audience: https://api.anthropic.com` and mount it at a dedicated path.

    ```yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: inference-worker
      namespace: inference
      annotations:
        eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/inference-worker
    ```

    ```yaml
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
  </Step>

  <Step title="Note the token's claim shape">
    The projected token is a JSON Web Token (JWT) signed by your cluster's OIDC issuer. Its `sub` claim follows the Kubernetes convention `system:serviceaccount:<namespace>:<service-account-name>`:

    ```json
    {
      "iss": "https://oidc.eks.us-west-2.amazonaws.com/id/6FA42E7BFDE8549CB...",
      "sub": "system:serviceaccount:inference:inference-worker",
      "aud": ["https://api.anthropic.com"],
      "kubernetes.io": {
        "namespace": "inference",
        "serviceaccount": { "name": "inference-worker", "uid": "..." }
      },
      "exp": 1775527120,
      "iat": 1775523520
    }
    ```

    The `serviceAccountToken` projection sets `aud` to `https://api.anthropic.com`. The separate IRSA-injected token at `AWS_WEB_IDENTITY_TOKEN_FILE` carries `aud: sts.amazonaws.com` and is for AWS API calls, not this exchange.
  </Step>
</Steps>

### Configure Anthropic

In the Claude Console, open **Settings → Workload identity**, click **Connect workload**, and select the **AWS** tile. The wizard walks you through registering the issuer, creating a service account, and creating a federation rule.

The wizard creates these resources for you. Use the following values whether you enter them in the wizard or send them to the [Admin API](/docs/en/manage-claude/wif-admin-api):

**Federation issuer:** EKS issuers expose a public JWKS endpoint, so use discovery mode. The issuer URL must exactly match the token's `iss` claim. Register one issuer per cluster.

```json
{
  "name": "prod-eks-uswest2",
  "issuer_url": "https://oidc.eks.us-west-2.amazonaws.com/id/6FA42E7BFDE8549CB...",
  "jwks": { "type": "discovery" }
}
```

**Federation rule:** Match the Kubernetes `sub` claim and the Anthropic audience `https://api.anthropic.com`. (Project a dedicated service-account token with that audience; don't reuse the IRSA default `sts.amazonaws.com` token.)

```json
{
  "name": "prod-inference",
  "issuer_id": "fdis_...",
  "match": {
    "subject_prefix": "system:serviceaccount:inference:inference-worker",
    "audience": "https://api.anthropic.com"
  },
  "target": { "type": "service_account", "service_account_id": "svac_..." },
  "workspace_id": "wrkspc_...",
  "oauth_scope": "workspace:developer",
  "token_lifetime_seconds": 600
}
```

Be as specific as the workload allows. Loosen `subject_prefix` to `system:serviceaccount:inference:*` (the trailing `*` makes it a prefix match) only if every service account in the namespace should map to the same Anthropic service account.

### Acquire and use the token

Inside the pod, the projected token is at `/var/run/secrets/anthropic.com/token` (exposed as `ANTHROPIC_IDENTITY_TOKEN_FILE` in the Pod spec). Pass that file to the SDK's federation credentials and the SDK handles the exchange and refresh.

<CodeGroup>
  ```bash cURL
  JWT=$(cat "$ANTHROPIC_IDENTITY_TOKEN_FILE")

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
      "model": "claude-sonnet-4-6",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello from EKS"}]
    }' | jq -r '.content[0].text'
  ```

  ```python Python
  import os

  import anthropic
  from anthropic import IdentityTokenFile, WorkloadIdentityCredentials

  client = anthropic.Anthropic(
      credentials=WorkloadIdentityCredentials(
          identity_token_provider=IdentityTokenFile(
              os.environ["ANTHROPIC_IDENTITY_TOKEN_FILE"]
          ),
          federation_rule_id=os.environ["ANTHROPIC_FEDERATION_RULE_ID"],
          organization_id=os.environ["ANTHROPIC_ORGANIZATION_ID"],
          service_account_id=os.environ["ANTHROPIC_SERVICE_ACCOUNT_ID"],
          workspace_id=os.environ.get("ANTHROPIC_WORKSPACE_ID"),
      ),
  )

  message = client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello from EKS"}],
  )
  print(message.content[0].text)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { oidcFederationProvider } from "@anthropic-ai/sdk/lib/credentials/oidc-federation";
  import { identityTokenFromFile } from "@anthropic-ai/sdk/lib/credentials/identity-token";

  const client = new Anthropic({
    credentials: oidcFederationProvider({
      identityTokenProvider: identityTokenFromFile(process.env.ANTHROPIC_IDENTITY_TOKEN_FILE!),
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
    messages: [{ role: "user", content: "Hello from EKS" }]
  });
  for (const block of message.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```go Go
  tokenPath := os.Getenv("ANTHROPIC_IDENTITY_TOKEN_FILE")

  readToken := option.IdentityTokenFunc(func(ctx context.Context) (string, error) {
  	raw, err := os.ReadFile(tokenPath)
  	if err != nil {
  		return "", fmt.Errorf("read identity token: %w", err)
  	}
  	return string(raw), nil
  })

  client := anthropic.NewClient(
  	option.WithFederationTokenProvider(readToken, option.FederationOptions{
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
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello from EKS")),
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
          .addUserMessage("Hello from EKS")
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
      Messages = [new() { Role = Role.User, Content = "Hello from EKS" }],
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
    --message '{role: user, content: "Hello from EKS"}'
  ```

  ```php PHP
  use Anthropic\Client;

  // Reads ANTHROPIC_FEDERATION_RULE_ID, ANTHROPIC_ORGANIZATION_ID,
  // ANTHROPIC_SERVICE_ACCOUNT_ID, ANTHROPIC_WORKSPACE_ID, and ANTHROPIC_IDENTITY_TOKEN_FILE
  $client = new Client();

  $message = $client->messages->create(
      model: 'claude-sonnet-4-6',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello from EKS']],
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
    messages: [{role: "user", content: "Hello from EKS"}]
  )
  puts message.content.first.text
  ```
</CodeGroup>

<Tip>
  The Pod spec already sets `ANTHROPIC_IDENTITY_TOKEN_FILE`, `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, and `ANTHROPIC_WORKSPACE_ID`, so you can construct the client with no arguments and the SDK reads the federation environment variables automatically.
</Tip>

### Verify the setup

From inside the pod, exchange the projected token directly and inspect the response:

```bash cURL
JWT=$(cat "$ANTHROPIC_IDENTITY_TOKEN_FILE")

curl -sS https://api.anthropic.com/v1/oauth/token \
  -H "content-type: application/json" \
  -d "{
    \"grant_type\": \"urn:ietf:params:oauth:grant-type:jwt-bearer\",
    \"assertion\": \"$JWT\",
    \"federation_rule_id\": \"$ANTHROPIC_FEDERATION_RULE_ID\",
    \"organization_id\": \"$ANTHROPIC_ORGANIZATION_ID\",
    \"service_account_id\": \"$ANTHROPIC_SERVICE_ACCOUNT_ID\",
    \"workspace_id\": \"$ANTHROPIC_WORKSPACE_ID\"
  }" | jq
```

A successful exchange returns an `access_token` beginning with `sk-ant-oat01-` and an `expires_in` value in seconds. On `400 invalid_grant`, see [Troubleshoot a failed exchange](/docs/en/manage-claude/wif-reference#troubleshoot-a-failed-exchange); the most common EKS-side cause is the projected token's `aud` not matching the rule (project a token with `audience: https://api.anthropic.com`, not the IRSA default `sts.amazonaws.com`).

## Scope your rule

<Warning>
  A `subject_prefix` of `arn:aws:iam::123456789012:role/*` matches every IAM role in the account. Any principal that can assume any matching role can obtain a federated Anthropic token.
</Warning>

Lock the rule's `match` block to the narrowest scope that fits your use case:

* **Pin the full role ARN:** Use `subject_prefix: "arn:aws:iam::<account>:role/<role-name>"` with no trailing `*` so other roles in the account do not match.
* **Pin the account ID:** Match the `aws_account` field of the token's `https://sts.amazonaws.com/` claim with the `claims` map or a CEL `condition` as a defense-in-depth check against a misconfigured prefix.
* **Pin namespace and service account on EKS:** Use the exact `system:serviceaccount:<namespace>:<name>` value with no `*` after the `system:serviceaccount:` prefix.
* **Use a separate rule per environment:** Create distinct rules for production, staging, and development workloads rather than widening one prefix to cover them all.

## Next steps

* Review the [WIF reference](/docs/en/manage-claude/wif-reference) for the full credential precedence, profile configuration, and rule matching reference.
* For self-managed Kubernetes clusters that aren't on EKS, see [Use WIF with Kubernetes](/docs/en/manage-claude/wif-providers/kubernetes).
