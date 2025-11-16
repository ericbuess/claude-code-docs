# Claude on Amazon Bedrock

> Anthropic's Claude models are now generally available through Amazon Bedrock.

export const ModelId = ({children, style = {}}) => {
  const copiedNotice = 'Copied!';
  const handleClick = e => {
    const element = e.currentTarget;
    const textSpan = element.querySelector('.model-id-text');
    const copiedSpan = element.querySelector('.model-id-copied');
    navigator.clipboard.writeText(children).then(() => {
      textSpan.style.opacity = '0';
      copiedSpan.style.opacity = '1';
      element.style.backgroundColor = '#d4edda';
      element.style.borderColor = '#c3e6cb';
      setTimeout(() => {
        textSpan.style.opacity = '1';
        copiedSpan.style.opacity = '0';
        element.style.backgroundColor = '#f5f5f5';
        element.style.borderColor = 'transparent';
      }, 2000);
    }).catch(error => {
      console.error('Failed to copy:', error);
    });
  };
  const handleMouseEnter = e => {
    const element = e.currentTarget;
    const copiedSpan = element.querySelector('.model-id-copied');
    const tooltip = element.querySelector('.copy-tooltip');
    if (tooltip && copiedSpan.style.opacity !== '1') {
      tooltip.style.opacity = '1';
    }
    element.style.backgroundColor = '#e8e8e8';
    element.style.borderColor = '#d0d0d0';
  };
  const handleMouseLeave = e => {
    const element = e.currentTarget;
    const copiedSpan = element.querySelector('.model-id-copied');
    const tooltip = element.querySelector('.copy-tooltip');
    if (tooltip) {
      tooltip.style.opacity = '0';
    }
    if (copiedSpan.style.opacity !== '1') {
      element.style.backgroundColor = '#f5f5f5';
      element.style.borderColor = 'transparent';
    }
  };
  const defaultStyle = {
    cursor: 'pointer',
    position: 'relative',
    transition: 'all 0.2s ease',
    display: 'inline-block',
    userSelect: 'none',
    backgroundColor: '#f5f5f5',
    padding: '2px 4px',
    borderRadius: '4px',
    fontFamily: 'Monaco, Consolas, "Courier New", monospace',
    fontSize: '0.75em',
    border: '1px solid transparent',
    ...style
  };
  return <span onClick={handleClick} onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave} style={defaultStyle}>
      <span className="model-id-text" style={{
    transition: 'opacity 0.1s ease'
  }}>
        {children}
      </span>
      <span className="model-id-copied" style={{
    position: 'absolute',
    top: '2px',
    left: '4px',
    right: '4px',
    opacity: '0',
    transition: 'opacity 0.1s ease',
    color: '#155724'
  }}>
        {copiedNotice}
      </span>
    </span>;
};

Calling Claude through Bedrock slightly differs from how you would call Claude when using Anthropic's client SDK's. This guide will walk you through the process of completing an API call to Claude on Bedrock in either Python or TypeScript.

Note that this guide assumes you have already signed up for an [AWS account](https://portal.aws.amazon.com/billing/signup) and configured programmatic access.

## Install and configure the AWS CLI

1. [Install a version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) at or newer than version `2.13.23`
2. Configure your AWS credentials using the AWS configure command (see [Configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)) or find your credentials by navigating to "Command line or programmatic access" within your AWS dashboard and following the directions in the popup modal.
3. Verify that your credentials are working:

```bash Shell theme={null}
aws sts get-caller-identity
```

## Install an SDK for accessing Bedrock

Anthropic's [client SDKs](/en/api/client-sdks) support Bedrock. You can also use an AWS SDK like `boto3` directly.

<CodeGroup>
  ```Python Python theme={null}
  pip install -U "anthropic[bedrock]"
  ```

  ```TypeScript TypeScript theme={null}
  npm install @anthropic-ai/bedrock-sdk
  ```

  ```Python Boto3 (Python) theme={null}
  pip install boto3>=1.28.59
  ```
</CodeGroup>

## Accessing Bedrock

### Subscribe to Anthropic models

Go to the [AWS Console > Bedrock > Model Access](https://console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess) and request access to Anthropic models. Note that Anthropic model availability varies by region. See [AWS documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) for latest information.

#### API model IDs

| Model                                                                            | Base Bedrock model ID                                        | `global` | `us` | `eu` | `jp` | `apac` |
| :------------------------------------------------------------------------------- | :----------------------------------------------------------- | :------- | :--- | :--- | :--- | :----- |
| Claude Sonnet 4.5                                                                | <ModelId>anthropic.claude-sonnet-4-5-20250929-v1:0</ModelId> | Yes      | Yes  | Yes  | Yes  | No     |
| Claude Sonnet 4                                                                  | <ModelId>anthropic.claude-sonnet-4-20250514-v1:0</ModelId>   | Yes      | Yes  | Yes  | No   | Yes    |
| Claude Sonnet 3.7 <Tooltip tip="Deprecated as of October 28, 2025.">⚠️</Tooltip> | <ModelId>anthropic.claude-3-7-sonnet-20250219-v1:0</ModelId> | No       | Yes  | Yes  | No   | Yes    |
| Claude Opus 4.1                                                                  | <ModelId>anthropic.claude-opus-4-1-20250805-v1:0</ModelId>   | No       | Yes  | No   | No   | No     |
| Claude Opus 4                                                                    | <ModelId>anthropic.claude-opus-4-20250514-v1:0</ModelId>     | No       | Yes  | No   | No   | No     |
| Claude Opus 3 <Tooltip tip="Deprecated as of June 30, 2025.">⚠️</Tooltip>        | <ModelId>anthropic.claude-3-opus-20240229-v1:0</ModelId>     | No       | Yes  | No   | No   | No     |
| Claude Haiku 4.5                                                                 | <ModelId>anthropic.claude-haiku-4-5-20251001-v1:0</ModelId>  | Yes      | Yes  | Yes  | No   | No     |
| Claude Haiku 3.5                                                                 | <ModelId>anthropic.claude-3-5-haiku-20241022-v1:0</ModelId>  | No       | Yes  | No   | No   | No     |
| Claude Haiku 3                                                                   | <ModelId>anthropic.claude-3-haiku-20240307-v1:0</ModelId>    | No       | Yes  | Yes  | No   | Yes    |

For more information about regional vs global model IDs, see the [Global vs regional endpoints](#global-vs-regional-endpoints) section below.

### List available models

The following examples show how to print a list of all the Claude models available through Bedrock:

<CodeGroup>
  ```bash AWS CLI theme={null}
  aws bedrock list-foundation-models --region=us-west-2 --by-provider anthropic --query "modelSummaries[*].modelId"
  ```

  ```python Boto3 (Python) theme={null}
  import boto3

  bedrock = boto3.client(service_name="bedrock")
  response = bedrock.list_foundation_models(byProvider="anthropic")

  for summary in response["modelSummaries"]:
      print(summary["modelId"])
  ```
</CodeGroup>

### Making requests

The following examples show how to generate text from Claude on Bedrock:

<CodeGroup>
  ```Python Python theme={null}
  from anthropic import AnthropicBedrock

  client = AnthropicBedrock(
      # Authenticate by either providing the keys below or use the default AWS credential providers, such as
      # using ~/.aws/credentials or the "AWS_SECRET_ACCESS_KEY" and "AWS_ACCESS_KEY_ID" environment variables.
      aws_access_key="<access key>",
      aws_secret_key="<secret key>",
      # Temporary credentials can be used with aws_session_token.
      # Read more at https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html.
      aws_session_token="<session_token>",
      # aws_region changes the aws region to which the request is made. By default, we read AWS_REGION,
      # and if that's not present, we default to us-east-1. Note that we do not read ~/.aws/config for the region.
      aws_region="us-west-2",
  )

  message = client.messages.create(
      model="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
      max_tokens=256,
      messages=[{"role": "user", "content": "Hello, world"}]
  )
  print(message.content)
  ```

  ```TypeScript TypeScript theme={null}
  import AnthropicBedrock from '@anthropic-ai/bedrock-sdk';

  const client = new AnthropicBedrock({
    // Authenticate by either providing the keys below or use the default AWS credential providers, such as
    // using ~/.aws/credentials or the "AWS_SECRET_ACCESS_KEY" and "AWS_ACCESS_KEY_ID" environment variables.
    awsAccessKey: '<access key>',
    awsSecretKey: '<secret key>',

    // Temporary credentials can be used with awsSessionToken.
    // Read more at https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html.
    awsSessionToken: '<session_token>',

    // awsRegion changes the aws region to which the request is made. By default, we read AWS_REGION,
    // and if that's not present, we default to us-east-1. Note that we do not read ~/.aws/config for the region.
    awsRegion: 'us-west-2',
  });

  async function main() {
    const message = await client.messages.create({
      model: 'global.anthropic.claude-sonnet-4-5-20250929-v1:0',
      max_tokens: 256,
      messages: [{"role": "user", "content": "Hello, world"}]
    });
    console.log(message);
  }
  main().catch(console.error);
  ```

  ```python Boto3 (Python) theme={null}
  import boto3
  import json

  bedrock = boto3.client(service_name="bedrock-runtime")
  body = json.dumps({
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "Hello, world"}],
    "anthropic_version": "bedrock-2023-05-31"
  })

  response = bedrock.invoke_model(body=body, modelId="global.anthropic.claude-sonnet-4-5-20250929-v1:0")

  response_body = json.loads(response.get("body").read())
  print(response_body.get("content"))
  ```
</CodeGroup>

See our [client SDKs](/en/api/client-sdks) for more details, and the official Bedrock docs [here](https://docs.aws.amazon.com/bedrock/).

## Activity logging

Bedrock provides an [invocation logging service](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) that allows customers to log the prompts and completions associated with your usage.

Anthropic recommends that you log your activity on at least a 30-day rolling basis in order to understand your activity and investigate any potential misuse.

<Note>
  Turning on this service does not give AWS or Anthropic any access to your content.
</Note>

## Feature support

You can find all the features currently supported on Bedrock [here](/en/api/overview).

### PDF Support on Bedrock

PDF support is available on Amazon Bedrock through both the Converse API and InvokeModel API. For detailed information about PDF processing capabilities and limitations, see the [PDF support documentation](/en/docs/build-with-claude/pdf-support#amazon-bedrock-pdf-support).

**Important considerations for Converse API users:**

* Visual PDF analysis (charts, images, layouts) requires citations to be enabled
* Without citations, only basic text extraction is available
* For full control without forced citations, use the InvokeModel API

For more details on the two document processing modes and their limitations, refer to the [PDF support guide](/en/docs/build-with-claude/pdf-support#amazon-bedrock-pdf-support).

### 1M token context window

Claude Sonnet 4 and 4.5 support the [1M token context window](/en/docs/build-with-claude/context-windows#1m-token-context-window) on Amazon Bedrock.

<Note>
  The 1M token context window is currently in beta. To use the extended context window, include the `context-1m-2025-08-07` beta header in your [Bedrock API requests](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages-request-response.html).
</Note>

## Global vs regional endpoints

Starting with **Claude Sonnet 4.5 and all future models**, Amazon Bedrock offers two endpoint types:

* **Global endpoints**: Dynamic routing for maximum availability
* **Regional endpoints**: Guaranteed data routing through specific geographic regions

Regional endpoints include a 10% pricing premium over global endpoints.

<Note>
  This applies to Claude Sonnet 4.5 and future models only. Older models (Claude Sonnet 4, Opus 4, and earlier) maintain their existing pricing structures.
</Note>

### When to use each option

**Global endpoints (recommended):**

* Provide maximum availability and uptime
* Dynamically route requests to regions with available capacity
* No pricing premium
* Best for applications where data residency is flexible

**Regional endpoints (CRIS):**

* Route traffic through specific geographic regions
* Required for data residency and compliance requirements
* Available for US, EU, Japan, and Australia
* 10% pricing premium reflects infrastructure costs for dedicated regional capacity

### Implementation

**Using global endpoints (default for Sonnet 4.5 and 4):**

The model IDs for Claude Sonnet 4.5 and 4 already include the `global.` prefix:

<CodeGroup>
  ```python Python theme={null}
  from anthropic import AnthropicBedrock

  client = AnthropicBedrock(aws_region="us-west-2")

  message = client.messages.create(
      model="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
      max_tokens=256,
      messages=[{"role": "user", "content": "Hello, world"}]
  )
  ```

  ```typescript TypeScript theme={null}
  import AnthropicBedrock from '@anthropic-ai/bedrock-sdk';

  const client = new AnthropicBedrock({
    awsRegion: 'us-west-2',
  });

  const message = await client.messages.create({
    model: 'global.anthropic.claude-sonnet-4-5-20250929-v1:0',
    max_tokens: 256,
    messages: [{role: "user", content: "Hello, world"}]
  });
  ```
</CodeGroup>

**Using regional endpoints (CRIS):**

To use regional endpoints, remove the `global.` prefix from the model ID:

<CodeGroup>
  ```python Python theme={null}
  from anthropic import AnthropicBedrock

  client = AnthropicBedrock(aws_region="us-west-2")

  # Using US regional endpoint (CRIS)
  message = client.messages.create(
      model="anthropic.claude-sonnet-4-5-20250929-v1:0",  # No global. prefix
      max_tokens=256,
      messages=[{"role": "user", "content": "Hello, world"}]
  )
  ```

  ```typescript TypeScript theme={null}
  import AnthropicBedrock from '@anthropic-ai/bedrock-sdk';

  const client = new AnthropicBedrock({
    awsRegion: 'us-west-2',
  });

  // Using US regional endpoint (CRIS)
  const message = await client.messages.create({
    model: 'anthropic.claude-sonnet-4-5-20250929-v1:0',  // No global. prefix
    max_tokens: 256,
    messages: [{role: "user", content: "Hello, world"}]
  });
  ```
</CodeGroup>

### Additional resources

* **AWS Bedrock pricing:** [aws.amazon.com/bedrock/pricing](https://aws.amazon.com/bedrock/pricing/)
* **AWS pricing documentation:** [Bedrock pricing guide](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-pricing.html)
* **AWS blog post:** [Introducing Claude Sonnet 4.5 in Amazon Bedrock](https://aws.amazon.com/blogs/aws/introducing-claude-sonnet-4-5-in-amazon-bedrock-anthropics-most-intelligent-model-best-for-coding-and-complex-agents/)
* **Anthropic pricing details:** [Pricing documentation](/en/docs/about-claude/pricing#third-party-platform-pricing)
