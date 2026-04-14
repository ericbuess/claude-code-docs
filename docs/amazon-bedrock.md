> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code on Amazon Bedrock

> Learn about configuring Claude Code through Amazon Bedrock, including setup, IAM configuration, and troubleshooting.

export const ContactSalesCard = ({surface}) => {
  const utm = content => `utm_source=claude_code&utm_medium=docs&utm_content=${surface}_${content}`;
  const iconArrowRight = (size = 13) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>;
  const STYLES = `
.cc-cs {
  --cs-slate: #141413;
  --cs-clay: #d97757;
  --cs-clay-deep: #c6613f;
  --cs-gray-000: #ffffff;
  --cs-gray-700: #3d3d3a;
  --cs-border-default: rgba(31, 30, 29, 0.15);
  font-family: inherit;
}
.dark .cc-cs {
  --cs-slate: #f0eee6;
  --cs-gray-000: #262624;
  --cs-gray-700: #bfbdb4;
  --cs-border-default: rgba(240, 238, 230, 0.14);
}
.cc-cs-card {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; padding: 14px 16px; margin: 0;
  background: var(--cs-gray-000); border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; flex-wrap: wrap;
}
.cc-cs-text { font-size: 13px; color: var(--cs-gray-700); line-height: 1.5; flex: 1; min-width: 240px; }
.cc-cs-text strong { font-weight: 550; color: var(--cs-slate); }
.cc-cs-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.cc-cs-btn-clay {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--cs-clay-deep); color: #fff; border: none;
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
  transition: background-color 0.15s; white-space: nowrap;
}
.cc-cs-btn-clay:hover { background: var(--cs-clay); }
.cc-cs-btn-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; color: var(--cs-gray-700);
  border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
}
.cc-cs-btn-ghost:hover { background: rgba(0, 0, 0, 0.04); }
.dark .cc-cs-btn-ghost:hover { background: rgba(255, 255, 255, 0.04); }
@media (max-width: 720px) {
  .cc-cs-actions { width: 100%; }
}
`;
  return <div className="cc-cs not-prose">
      <style>{STYLES}</style>
      <div className="cc-cs-card">
        <div className="cc-cs-text">
          <strong>Deploying Claude Code across your organization?</strong> Talk to sales about enterprise plans, SSO, and centralized billing.
        </div>
        <div className="cc-cs-actions">
          <a href={`https://claude.com/pricing?${utm('view_plans')}#plans-business`} className="cc-cs-btn-ghost">
            View plans
          </a>
          <a href={`https://www.anthropic.com/contact-sales?${utm('contact_sales')}`} className="cc-cs-btn-clay">
            Contact sales {iconArrowRight()}
          </a>
        </div>
      </div>
    </div>;
};

export const Experiment = ({flag, treatment, children}) => {
  const VID_KEY = 'exp_vid';
  const CONSENT_COUNTRIES = new Set(['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'RE', 'GP', 'MQ', 'GF', 'YT', 'BL', 'MF', 'PM', 'WF', 'PF', 'NC', 'AW', 'CW', 'SX', 'FO', 'GL', 'AX', 'GB', 'UK', 'AI', 'BM', 'IO', 'VG', 'KY', 'FK', 'GI', 'MS', 'PN', 'SH', 'TC', 'GG', 'JE', 'IM', 'CA', 'BR', 'IN']);
  const fnv1a = s => {
    let h = 0x811c9dc5;
    for (let i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h += (h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24);
    }
    return h >>> 0;
  };
  const bucket = (seed, vid) => fnv1a(fnv1a(seed + vid) + '') % 10000 < 5000 ? 'control' : 'treatment';
  const [decision] = useState(() => {
    const params = new URLSearchParams(location.search);
    const force = params.get('gb-force');
    if (force) {
      for (const p of force.split(',')) {
        const [k, v] = p.split(':');
        if (k === flag) return {
          variant: v || 'treatment',
          track: false
        };
      }
    }
    if (navigator.globalPrivacyControl) {
      return {
        variant: 'control',
        track: false
      };
    }
    const prefsMatch = document.cookie.match(/(?:^|; )anthropic-consent-preferences=([^;]+)/);
    if (prefsMatch) {
      try {
        if (JSON.parse(decodeURIComponent(prefsMatch[1])).analytics !== true) {
          return {
            variant: 'control',
            track: false
          };
        }
      } catch {
        return {
          variant: 'control',
          track: false
        };
      }
    } else {
      const country = params.get('country')?.toUpperCase() || (document.cookie.match(/(?:^|; )cf_geo=([A-Z]{2})/) || [])[1];
      if (!country || CONSENT_COUNTRIES.has(country)) {
        return {
          variant: 'control',
          track: false
        };
      }
    }
    let vid;
    try {
      const ajsMatch = document.cookie.match(/(?:^|; )ajs_anonymous_id=([^;]+)/);
      if (ajsMatch) {
        vid = decodeURIComponent(ajsMatch[1]).replace(/^"|"$/g, '');
      } else {
        vid = localStorage.getItem(VID_KEY);
        if (!vid) {
          vid = crypto.randomUUID();
        }
        document.cookie = `ajs_anonymous_id=${vid}; domain=.claude.com; path=/; Secure; SameSite=Lax; max-age=31536000`;
      }
      try {
        localStorage.setItem(VID_KEY, vid);
      } catch {}
    } catch {
      return {
        variant: 'control',
        track: false
      };
    }
    return {
      variant: bucket(flag, vid),
      track: true,
      vid
    };
  });
  useEffect(() => {
    if (!decision.track) return;
    fetch('https://api.anthropic.com/api/event_logging/v2/batch', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-service-name': 'claude_code_docs'
      },
      body: JSON.stringify({
        events: [{
          event_type: 'GrowthbookExperimentEvent',
          event_data: {
            device_id: decision.vid,
            anonymous_id: decision.vid,
            timestamp: new Date().toISOString(),
            experiment_id: flag,
            variation_id: decision.variant === 'treatment' ? 1 : 0,
            environment: 'production'
          }
        }]
      }),
      keepalive: true
    }).catch(() => {});
  }, []);
  return decision.variant === 'treatment' ? treatment : children;
};

<Experiment flag="docs-contact-sales-cta" treatment={<ContactSalesCard surface="bedrock" />} />

## Prerequisites

Before configuring Claude Code with Bedrock, ensure you have:

* An AWS account with Bedrock access enabled
* Access to desired Claude models (for example, Claude Sonnet 4.6) in Bedrock
* AWS CLI installed and configured (optional - only needed if you don't have another mechanism for getting credentials)
* Appropriate IAM permissions

To sign in with your own Bedrock credentials, follow [Sign in with Bedrock](#sign-in-with-bedrock) below. To deploy Claude Code across a team, use the [manual setup](#set-up-manually) steps and [pin your model versions](#4-pin-model-versions) before rolling out.

## Sign in with Bedrock

If you have AWS credentials and want to start using Claude Code through Bedrock, the login wizard walks you through it. You complete the AWS-side prerequisites once per account; the wizard handles the Claude Code side.

<Steps>
  <Step title="Enable Anthropic models in your AWS account">
    In the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/), open the Model catalog, select an Anthropic model, and submit the use case form. Access is granted immediately after submission. See [Submit use case details](#1-submit-use-case-details) for AWS Organizations and [IAM configuration](#iam-configuration) for the permissions your role needs.
  </Step>

  <Step title="Start Claude Code and choose Bedrock">
    Run `claude`. At the login prompt, select **3rd-party platform**, then **Amazon Bedrock**.
  </Step>

  <Step title="Follow the wizard prompts">
    Choose how you authenticate to AWS: an AWS profile detected from your `~/.aws` directory, a Bedrock API key, an access key and secret, or credentials already in your environment. The wizard picks up your region, verifies which Claude models your account can invoke, and lets you pin them. It saves the result to the `env` block of your [user settings file](/en/settings), so you don't need to export environment variables yourself.
  </Step>
</Steps>

After you've signed in, run `/setup-bedrock` any time to reopen the wizard and change your credentials, region, or model pins.

## Set up manually

To configure Bedrock through environment variables instead of the wizard, for example in CI or a scripted enterprise rollout, follow the steps below.

### 1. Submit use case details

First-time users of Anthropic models are required to submit use case details before invoking a model. This is done once per AWS account.

1. Ensure you have the right IAM permissions described below
2. Navigate to the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/)
3. Select an Anthropic model from the **Model catalog**
4. Complete the use case form. Access is granted immediately after submission.

If you use AWS Organizations, you can submit the form once from the management account using the [`PutUseCaseForModelAccess` API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html). This call requires the `bedrock:PutUseCaseForModelAccess` IAM permission. Approval extends to child accounts automatically.

### 2. Configure AWS credentials

Claude Code uses the default AWS SDK credential chain. Set up your credentials using one of these methods:

**Option A: AWS CLI configuration**

```bash  theme={null}
aws configure
```

**Option B: Environment variables (access key)**

```bash  theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**Option C: Environment variables (SSO profile)**

```bash  theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**Option D: AWS Management Console credentials**

```bash  theme={null}
aws login
```

[Learn more](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) about `aws login`.

**Option E: Bedrock API keys**

```bash  theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Bedrock API keys provide a simpler authentication method without needing full AWS credentials. [Learn more about Bedrock API keys](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### Advanced credential configuration

Claude Code supports automatic credential refresh for AWS SSO and corporate identity providers. Add these settings to your Claude Code settings file (see [Settings](/en/settings) for file locations).

When Claude Code detects that your AWS credentials are expired (either locally based on their timestamp or when Bedrock returns a credential error), it will automatically run your configured `awsAuthRefresh` and/or `awsCredentialExport` commands to obtain new credentials before retrying the request.

##### Example configuration

```json  theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### Configuration settings explained

**`awsAuthRefresh`**: Use this for commands that modify the `.aws` directory, such as updating credentials, SSO cache, or config files. The command's output is displayed to the user, but interactive input isn't supported. This works well for browser-based SSO flows where the CLI displays a URL or code and you complete authentication in the browser.

**`awsCredentialExport`**: Only use this if you can't modify `.aws` and must directly return credentials. Output is captured silently and not shown to the user. The command must output JSON in this format:

```json  theme={null}
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. Configure Claude Code

Set the following environment variables to enable Bedrock:

```bash  theme={null}
# Enable Bedrock integration
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # or your preferred region

# Optional: Override the region for the small/fast model (Haiku).
# Also applies to Bedrock Mantle.
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2

# Optional: Override the Bedrock endpoint URL for custom endpoints or gateways
# export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

When enabling Bedrock for Claude Code, keep the following in mind:

* `AWS_REGION` is a required environment variable. Claude Code does not read from the `.aws` config file for this setting.
* When using Bedrock, the `/login` and `/logout` commands are disabled since authentication is handled through AWS credentials.
* You can use settings files for environment variables like `AWS_PROFILE` that you don't want to leak to other processes. See [Settings](/en/settings) for more information.

### 4. Pin model versions

<Warning>
  Pin specific model versions when deploying to multiple users. Without pinning, model aliases such as `sonnet` and `opus` resolve to the latest version, which may not yet be available in your Bedrock account when Anthropic releases an update. Claude Code [falls back](#startup-model-checks) to the previous version at startup when the latest is unavailable, but pinning lets you control when your users move to a new model.
</Warning>

Set these environment variables to specific Bedrock model IDs:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

These variables use cross-region inference profile IDs (with the `us.` prefix). If you use a different region prefix or application inference profiles, adjust accordingly. For current and legacy model IDs, see [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). See [Model configuration](/en/model-config#pin-models-for-third-party-deployments) for the full list of environment variables.

Claude Code uses these default models when no pinning variables are set:

| Model type       | Default value                                  |
| :--------------- | :--------------------------------------------- |
| Primary model    | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Small/fast model | `us.anthropic.claude-haiku-4-5-20251001-v1:0`  |

To customize models further, use one of these methods:

```bash  theme={null}
# Using inference profile ID
export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Using application inference profile ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1
```

<Note>[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) may not be available in all regions.</Note>

#### Map each model version to an inference profile

The `ANTHROPIC_DEFAULT_*_MODEL` environment variables configure one inference profile per model family. If your organization needs to expose several versions of the same family in the `/model` picker, each routed to its own application inference profile ARN, use the `modelOverrides` setting in your [settings file](/en/settings#settings-files) instead.

This example maps three Opus versions to distinct ARNs so users can switch between them without bypassing your organization's inference profiles:

```json  theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

When a user selects one of these versions in `/model`, Claude Code calls Bedrock with the mapped ARN. Versions without an override fall back to the built-in Bedrock model ID or any matching inference profile discovered at startup. See [Override model IDs per version](/en/model-config#override-model-ids-per-version) for details on how overrides interact with `availableModels` and other model settings.

## Startup model checks

When Claude Code starts with Bedrock configured, it verifies that the models it intends to use are accessible in your account. This check requires Claude Code v2.1.94 or later.

If you have pinned a model version that is older than the current Claude Code default, and your account can invoke the newer version, Claude Code prompts you to update the pin. Accepting writes the new model ID to your [user settings file](/en/settings) and restarts Claude Code. Declining is remembered until the next default version change. Pins that point to an [application inference profile ARN](#map-each-model-version-to-an-inference-profile) are skipped, since those are managed by your administrator.

If you have not pinned a model and the current default is unavailable in your account, Claude Code falls back to the previous version for the current session and shows a notice. The fallback is not persisted. Enable the newer model in your Bedrock account or [pin a version](#4-pin-model-versions) to make the choice permanent.

## IAM configuration

Create an IAM policy with the required permissions for Claude Code:

```json  theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelAndInferenceProfileAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*",
        "arn:aws:bedrock:*:*:foundation-model/*"
      ]
    },
    {
      "Sid": "AllowMarketplaceSubscription",
      "Effect": "Allow",
      "Action": [
        "aws-marketplace:ViewSubscriptions",
        "aws-marketplace:Subscribe"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:CalledViaLast": "bedrock.amazonaws.com"
        }
      }
    }
  ]
}
```

For more restrictive permissions, you can limit the Resource to specific inference profile ARNs.

For details, see [Bedrock IAM documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

<Note>
  Create a dedicated AWS account for Claude Code to simplify cost tracking and access control.
</Note>

## 1M token context window

Claude Opus 4.6 and Sonnet 4.6 support the [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) on Amazon Bedrock. Claude Code automatically enables the extended context window when you select a 1M model variant.

To enable the 1M context window for your pinned model, append `[1m]` to the model ID. See [Pin models for third-party deployments](/en/model-config#pin-models-for-third-party-deployments) for details.

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) let you implement content filtering for Claude Code. Create a Guardrail in the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/), publish a version, then add the Guardrail headers to your [settings file](/en/settings). Enable Cross-Region inference on your Guardrail if you're using cross-region inference profiles.

Example configuration:

```json  theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

## Use the Mantle endpoint

Mantle is an Amazon Bedrock endpoint that serves Claude models through the native Anthropic API shape rather than the Bedrock Invoke API. It uses the same AWS credentials, IAM permissions, and `awsAuthRefresh` configuration described earlier on this page.

<Note>
  Mantle requires Claude Code v2.1.94 or later. Run `claude --version` to check.
</Note>

### Enable Mantle

With AWS credentials already configured, set `CLAUDE_CODE_USE_MANTLE` to route requests to the Mantle endpoint:

```bash  theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export AWS_REGION=us-east-1
```

Claude Code constructs the endpoint URL from `AWS_REGION`. To override it for a custom endpoint or gateway, set `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`.

Run `/status` inside Claude Code to confirm. The provider line shows `Amazon Bedrock (Mantle)` when Mantle is active.

### Select a Mantle model

Mantle uses model IDs prefixed with `anthropic.` and without a version suffix, for example `anthropic.claude-haiku-4-5`. The models available to your account depend on what your organization has been granted; additional model IDs are listed in your onboarding materials from AWS. Contact your AWS account team to request access to allowlisted models.

Set the model with the `--model` flag or with `/model` inside Claude Code:

```bash  theme={null}
claude --model anthropic.claude-haiku-4-5
```

### Run Mantle alongside the Invoke API

The models available to you on Mantle may not include every model you use today. Setting both `CLAUDE_CODE_USE_BEDROCK` and `CLAUDE_CODE_USE_MANTLE` lets Claude Code call both endpoints from the same session. Model IDs that match the Mantle format are routed to Mantle, and all other model IDs go to the Bedrock Invoke API.

```bash  theme={null}
export CLAUDE_CODE_USE_BEDROCK=1
export CLAUDE_CODE_USE_MANTLE=1
```

To surface a Mantle model in the `/model` picker, list its ID in `availableModels` in your [settings file](/en/settings). This setting also restricts the picker to the listed entries, so include every alias you want to keep available:

```json  theme={null}
{
  "availableModels": ["opus", "sonnet", "haiku", "anthropic.claude-haiku-4-5"]
}
```

Entries with the `anthropic.` prefix are added as custom picker options and routed to Mantle. Replace `anthropic.claude-haiku-4-5` with the model ID your account has been granted. See [Restrict model selection](/en/model-config#restrict-model-selection) for how `availableModels` interacts with other model settings.

When both providers are active, `/status` shows `Amazon Bedrock + Amazon Bedrock (Mantle)`.

### Route Mantle through a gateway

If your organization routes model traffic through a centralized [LLM gateway](/en/llm-gateway) that injects AWS credentials server-side, disable client-side authentication so Claude Code sends requests without SigV4 signatures or `x-api-key` headers:

```bash  theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export CLAUDE_CODE_SKIP_MANTLE_AUTH=1
export ANTHROPIC_BEDROCK_MANTLE_BASE_URL=https://your-gateway.example.com
```

### Mantle environment variables

These variables are specific to the Mantle endpoint. See [Environment variables](/en/env-vars) for the full list.

| Variable                                | Purpose                                                             |
| :-------------------------------------- | :------------------------------------------------------------------ |
| `CLAUDE_CODE_USE_MANTLE`                | Enable the Mantle endpoint. Set to `1` or `true`.                   |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`     | Override the default Mantle endpoint URL                            |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH`          | Skip client-side authentication for proxy setups                    |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | Override AWS region for the Haiku-class model (shared with Bedrock) |

## Troubleshooting

### Authentication loop with SSO and corporate proxies

If browser tabs spawn repeatedly when using AWS SSO, remove the `awsAuthRefresh` setting from your [settings file](/en/settings). This can occur when corporate VPNs or TLS inspection proxies interrupt the SSO browser flow. Claude Code treats the interrupted connection as an authentication failure, re-runs `awsAuthRefresh`, and loops indefinitely.

If your network environment interferes with automatic browser-based SSO flows, use `aws sso login` manually before starting Claude Code instead of relying on `awsAuthRefresh`.

### Region issues

If you encounter region issues:

* Check model availability: `aws bedrock list-inference-profiles --region your-region`
* Switch to a supported region: `export AWS_REGION=us-east-1`
* Consider using inference profiles for cross-region access

If you receive an error "on-demand throughput isn’t supported":

* Specify the model as an [inference profile](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) ID

Claude Code uses the Bedrock [Invoke API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) and does not support the Converse API.

### Mantle endpoint errors

If `/status` does not show `Amazon Bedrock (Mantle)` after you set `CLAUDE_CODE_USE_MANTLE`, the variable is not reaching the process. Confirm it is exported in the shell where you launched `claude`, or set it in the `env` block of your [settings file](/en/settings).

A `403` from the Mantle endpoint with valid credentials means your AWS account has not been granted access to the model you requested. Contact your AWS account team to request access.

A `400` that names the model ID means that model is not served on Mantle. Mantle has its own model lineup separate from the standard Bedrock catalog, so inference profile IDs such as `us.anthropic.claude-sonnet-4-6` will not work. Use a Mantle-format ID, or enable [both endpoints](#run-mantle-alongside-the-invoke-api) so Claude Code routes each request to the endpoint where the model is available.

## Additional resources

* [Bedrock documentation](https://docs.aws.amazon.com/bedrock/)
* [Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)
* [Bedrock inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Bedrock token burndown and quotas](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-token-burndown.html)
* [Claude Code on Amazon Bedrock: Quick Setup Guide](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Claude Code Monitoring Implementation (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
