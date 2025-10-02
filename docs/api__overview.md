# Overview

## Accessing the API

The API is made available via our web [Console](https://console.anthropic.com/). You can use the [Workbench](https://console.anthropic.com/workbench) to try out the API in the browser and then generate API keys in [Account Settings](https://console.anthropic.com/account/keys). Use [workspaces](https://console.anthropic.com/settings/workspaces) to segment your API keys and [control spend](/en/api/rate-limits) by use case.

## Authentication

All requests to the Claude API must include an `x-api-key` header with your API key. If you are using the Client SDKs, you will set the API when constructing a client, and then the SDK will send the header on your behalf with every request. If integrating directly with the API, you'll need to send this header yourself.

## Content types

The Claude API always accepts JSON in request bodies and returns JSON in response bodies. You will need to send the `content-type: application/json` header in requests. If you are using the Client SDKs, this will be taken care of automatically.

## Request size limits

The API has a maximum request size of 32 MB for standard endpoints, including the Messages API and Token Counting API. If you exceed this limit, you'll receive a 413 `request_too_large` error from Cloudflare. Specific endpoints have different limits:

* **Standard endpoints** (Messages, Token Counting): 32 MB
* **[Batch API](/en/docs/build-with-claude/batch-processing)**: 256 MB
* **[Files API](/en/docs/build-with-claude/files)**: 500 MB

## Response Headers

The Claude API includes the following headers in every response:

* `request-id`: A globally unique identifier for the request.

* `anthropic-organization-id`: The organization ID associated with the API key used in the request.

## Examples

<Tabs>
  <Tab title="curl">
    ```bash Shell
    curl https://api.anthropic.com/v1/messages \
         --header "x-api-key: $ANTHROPIC_API_KEY" \
         --header "anthropic-version: 2023-06-01" \
         --header "content-type: application/json" \
         --data \
    '{
        "model": "claude-sonnet-4-5",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "Hello, world"}
        ]
    }'
    ```
  </Tab>

  <Tab title="Python">
    Install via PyPI:

    ```bash
    pip install anthropic
    ```

    ```Python Python
    import anthropic

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key="my_api_key",
    )
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello, Claude"}
        ]
    )
    print(message.content)
    ```
  </Tab>

  <Tab title="TypeScript">
    Install via npm:

    ```bash
    npm install @anthropic-ai/sdk
    ```

    ```TypeScript TypeScript
    import Anthropic from '@anthropic-ai/sdk';

    const anthropic = new Anthropic({
      apiKey: 'my_api_key', // defaults to process.env["ANTHROPIC_API_KEY"]
    });

    const msg = await anthropic.messages.create({
      model: "claude-sonnet-4-5",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }],
    });
    console.log(msg);
    ```
  </Tab>
</Tabs>
