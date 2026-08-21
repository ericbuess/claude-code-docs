---
title: Python SDK
url: https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python
description: Install and configure the Anthropic Python SDK with sync and async client support
---

The Anthropic Python SDK provides convenient access to the Claude API from Python applications. It supports both synchronous and asynchronous operations, streaming, and integrations with Amazon Bedrock, Claude Platform on AWS, Google Cloud, and Microsoft Foundry.

<Info>
  For API feature documentation with code examples, see the [API reference](https://platform.claude.com/docs/en/api/overview). This page covers Python-specific SDK features and configuration.
</Info>

## Installation

```bash
pip install anthropic
```

For platform-specific integrations or improved async performance, install with extras:

```bash
# For Amazon Bedrock support
pip install "anthropic[bedrock]"

# For Google Cloud support
pip install "anthropic[vertex]"

# For Claude Platform on AWS support
pip install "anthropic[aws]"

# Microsoft Foundry support is included in the base package

# For improved async performance with aiohttp
pip install "anthropic[aiohttp]"
```

## Requirements

Python 3.9 or later is required.

## Usage

```python
import os
from anthropic import Anthropic

client = Anthropic(
    # This is the default and can be omitted
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-opus-5",
)

for block in message.content:
    if block.type == "text":
        print(block.text)
```

<Tip>
  Consider using [python-dotenv](https://pypi.org/project/python-dotenv/) to add `ANTHROPIC_API_KEY="my-anthropic-api-key"` to your `.env` file so that your API key isn't stored in source control.
</Tip>

For authentication options including Workload Identity Federation, see [Authentication](https://platform.claude.com/docs/en/manage-claude/authentication).

## Async usage

```python
import os
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)


async def main() -> None:
    message = await client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude",
            }
        ],
        model="claude-opus-5",
    )
    print(message.content)


asyncio.run(main())
```

### Using aiohttp for better concurrency

For improved async performance, you can use the `aiohttp` HTTP backend instead of the default `httpx`:

```python
import os
import asyncio
from anthropic import AsyncAnthropic, DefaultAioHttpClient


async def main() -> None:
    async with AsyncAnthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
        http_client=DefaultAioHttpClient(),
    ) as client:
        message = await client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, Claude",
                }
            ],
            model="claude-opus-5",
        )
        print(message.content)


asyncio.run(main())
```

## Streaming responses

The SDK provides support for streaming responses using Server-Sent Events (SSE).

```python
client = Anthropic()

stream = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-opus-5",
    stream=True,
)
for event in stream:
    print(event.type)
```

The async client uses the exact same interface:

```python
client = AsyncAnthropic()

stream = await client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-opus-5",
    stream=True,
)
async for event in stream:
    print(event.type)
```

### Streaming helpers

The SDK also provides streaming helpers that use context managers and provide access to the accumulated text and the final message:

```python
async def main() -> None:
    async with client.messages.stream(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Say hello there!",
            }
        ],
        model="claude-opus-5",
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
        print()

        message = await stream.get_final_message()
        print(message.to_json())


asyncio.run(main())
```

Streaming with `client.messages.stream(...)` exposes various helpers including accumulation and SDK-specific events.

Alternatively, you can use `client.messages.create(..., stream=True)` which only returns an iterable of the events in the stream and uses less memory (it doesn't build up a final message object for you).

## Token counting

You can see the exact usage for a given request through the `usage` response property:

```python
message = client.messages.create(...)
print(message.usage)
# Usage(input_tokens=25, output_tokens=13)
```

You can also count tokens before making a request:

```python
count = client.messages.count_tokens(
    model="claude-opus-5", messages=[{"role": "user", "content": "Hello, world"}]
)
print(count.input_tokens)  # 10
```

## Tool use

This SDK provides support for tool use, also known as function calling. For more details, see [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

### Tool helpers

The SDK provides helpers for defining and running tools as pure Python functions. The `@beta_tool` decorator generates the tool schema from the function signature and docstring:

```python
import json
from anthropic import Anthropic, beta_tool

client = Anthropic()


@beta_tool
def get_weather(location: str) -> str:
    """Get the weather for a given location.

    Args:
        location: The city and state, for example, San Francisco, CA
    Returns:
        A JSON-encoded string with the location, temperature, and weather condition.
    """
    return json.dumps(
        {
            "location": location,
            "temperature": "68°F",
            "condition": "Sunny",
        }
    )


# Use the tool_runner to automatically handle tool calls
runner = client.beta.messages.tool_runner(
    max_tokens=1024,
    model="claude-opus-5",
    tools=[get_weather],
    messages=[
        {"role": "user", "content": "What is the weather in SF?"},
    ],
)
for message in runner:
    print(message)
```

On every iteration, an API request is made. If the response includes a call to one of the given tools, the tool is automatically called, and the result is returned directly to the model in the next iteration.

## Message batches

This SDK provides support for [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing) under `client.messages.batches`.

### Creating a batch

Message Batches takes an array of requests, where each object has a `custom_id` identifier and the same request `params` as the standard Messages API:

```python
client.messages.batches.create(
    requests=[
        {
            "custom_id": "my-first-request",
            "params": {
                "model": "claude-opus-5",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Hello, world"}],
            },
        },
        {
            "custom_id": "my-second-request",
            "params": {
                "model": "claude-opus-5",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Hi again, friend"}],
            },
        },
    ]
)
```

### Getting results from a batch

Once a Message Batch has been processed, indicated by `.processing_status == 'ended'`, you can access the results with `.batches.results()`:

```python
client = anthropic.Anthropic()
batch_id = "batch_abc123"
result_stream = client.messages.batches.results(batch_id)
for entry in result_stream:
    if entry.result.type == "succeeded":
        print(entry.result.message.content)
```

## File uploads

Request parameters that correspond to file uploads can be passed in many different forms:

* A `PathLike` object (for example, `pathlib.Path`)
* A tuple of `(filename, content, content_type)`
* A `BinaryIO` file-like object

```python
from pathlib import Path
from anthropic import Anthropic

client = Anthropic()

# Upload using a file path
client.files.upload(
    file=Path("/path/to/file"),
)

# Upload using bytes
client.files.upload(
    file=("file.txt", b"my bytes", "text/plain"),
)
```

The async client uses the exact same interface. If you pass a `PathLike` instance, the file contents are read asynchronously automatically.

## Handling errors

When the library is unable to connect to the API, or if the API returns a non-success status code (that is, 4xx or 5xx response), a subclass of `APIError` is raised:

```python
import anthropic
# ...
try:
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude",
            }
        ],
        model="claude-opus-5",
    )
except anthropic.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx
except anthropic.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except anthropic.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
```

Error codes are as follows:

| Status code | Error type                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 409         | `ConflictError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |

## Request IDs

> For more information on debugging requests, see [Request ID](https://platform.claude.com/docs/en/api/errors#request-id).

All object responses in the SDK provide a `_request_id` property which is added from the `request-id` response header so that you can quickly log failing requests and report them back to Anthropic.

```python
message = client.messages.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-5",
)
print(message._request_id)  # e.g., req_018EeWyXxfu5pfWkrYcMdjWG
```

<Note>
  Unlike other properties that use an `_` prefix, the `_request_id` property is public. Unless documented otherwise, all other `_` prefix properties, methods, and modules are private.
</Note>

## Retries

Certain errors are automatically retried 2 times by default, with a short exponential backoff. Connection errors (for example, because of a network connectivity problem), 408 Request Timeout, 409 Conflict, 429 Rate Limit, and >=500 Internal errors are all retried by default.

You can use the `max_retries` option to configure or disable this:

```python
# Configure the default for all requests:
client = Anthropic(
    max_retries=0,  # default is 2
)

# Or, configure per-request:
client.with_options(max_retries=5).messages.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-5",
)
```

## Timeouts

By default requests time out after 10 minutes. You can configure this with a `timeout` option, which accepts a float or an `httpx.Timeout` object:

```python
import httpx
from anthropic import Anthropic

# Configure the default for all requests:
client = Anthropic(
    timeout=20.0,  # 20 seconds (default is 10 minutes)
)

# More granular control:
client = Anthropic(
    timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
)

# Override per-request:
client.with_options(timeout=5.0).messages.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-5",
)
```

On timeout, the SDK throws an `APITimeoutError`.

Note that requests that time out are [retried twice by default](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python#retries).

## Long requests

<Warning>
  Consider using the streaming [Messages API](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python#streaming-responses) for longer running requests.
</Warning>

Avoid setting a large `max_tokens` value without using streaming. Some networks may drop idle connections after a certain period of time, which can cause the request to fail or [timeout](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python#timeouts) without receiving a response from Anthropic.

The SDK will throw a `ValueError` if a non-streaming request is expected to take longer than approximately 10 minutes. Passing `stream=True` or overriding the `timeout` option at the client or request level disables this error.

An expected request latency longer than the [timeout](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python#timeouts) for a non-streaming request will result in the client terminating the connection and retrying without receiving a response.

The SDK sets a [TCP socket keep-alive](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/overview.html) option to reduce the impact of idle connection timeouts on some networks. This can be overridden by passing a custom `http_client` option to the client.

## Auto-pagination

List methods in the Claude API are paginated. You can use the `for` syntax to iterate through items across all pages:

```python
client = Anthropic()

all_batches = []
# Automatically fetches more pages as needed.
for batch in client.messages.batches.list(limit=20):
    all_batches.append(batch)
print(all_batches)
```

For async iteration:

```python
async def main() -> None:
    all_batches = []
    async for batch in client.messages.batches.list(limit=20):
        all_batches.append(batch)
    print(all_batches)


asyncio.run(main())
```

Alternatively, you can use the `.has_next_page()`, `.next_page_info()`, or `.get_next_page()` methods for more granular control working with pages:

```python
first_page = await client.messages.batches.list(limit=20)

if first_page.has_next_page():
    print(f"will fetch next page using these details: {first_page.next_page_info()}")
    next_page = await first_page.get_next_page()
    print(f"number of items we just fetched: {len(next_page.data)}")

# Remove `await` for non-async usage.
```

Or work directly with the returned data:

```python
first_page = await client.messages.batches.list(limit=20)

print(f"next page cursor: {first_page.last_id}")
for batch in first_page.data:
    print(batch.id)

# Remove `await` for non-async usage.
```

## Default headers

The SDK automatically sends the `anthropic-version` header set to `2023-06-01`.

If you need to, you can override it by setting default headers on the client object or per-request.

<Warning>
  Overriding default headers may result in incorrect types and other unexpected or undefined behavior in the SDK.
</Warning>

```python
# Set default headers for all requests on the client
client = Anthropic(
    default_headers={"anthropic-version": "My-Custom-Value"},
)

# Or override per-request
client.messages.with_raw_response.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-5",
    extra_headers={"anthropic-version": "My-Custom-Value"},
)
```

## Type system

### Request parameters

Nested request parameters are [TypedDicts](https://docs.python.org/3/library/typing.html#typing.TypedDict). Responses are [Pydantic models](https://docs.pydantic.dev) which also have helper methods for things like serializing back into JSON ([`v1`](https://docs.pydantic.dev/1.10/usage/models/), [`v2`](https://docs.pydantic.dev/latest/concepts/serialization/)).

Typed requests and responses provide autocomplete and documentation within your editor. If you'd like to see type errors in VS Code to help catch bugs earlier, set `python.analysis.typeCheckingMode` to `basic`.

### Response models

To convert a Pydantic model to a dictionary, use the helper methods:

```python
message = client.messages.create(...)

# Convert to JSON string
json_str = message.to_json()

# Convert to dictionary
data = message.to_dict()
```

### Handling null vs missing fields

In responses, you can distinguish between fields that are explicitly `null` versus fields that were not returned (missing):

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)
if response.my_field is None:
    if "my_field" not in response.model_fields_set:
        print("field was not in the response")
    else:
        print("field was null")
```

## Advanced usage

### Accessing raw response data (for example, headers)

The "raw" `Response` returned by `httpx` can be accessed through the `.with_raw_response` property on the client. This is useful for accessing response headers or other metadata:

```python
client = Anthropic()

response = client.messages.with_raw_response.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-5",
)

print(response.headers.get("request-id"))
message = (
    response.parse()
)  # get the object that `messages.create()` would have returned
print(message.content)
```

These methods return an `APIResponse` object.

### Streaming response body

The `.with_raw_response` approach eagerly reads the full response body when you make the request. To stream the response body instead, use `.with_streaming_response`, which requires a context manager and only reads the response body once you call `.read()`, `.text()`, `.json()`, `.iter_bytes()`, `.iter_text()`, `.iter_lines()`, or `.parse()`. In the async client, these are async methods.

```python
with client.messages.with_streaming_response.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    model="claude-opus-5",
) as response:
    print(response.headers.get("request-id"))

    for line in response.iter_lines():
        print(line)
```

The context manager is required so that the response will reliably be closed.

### Logging

The SDK uses the standard library `logging` module.

You can enable logging by setting the environment variable `ANTHROPIC_LOG` to `debug` or `info`:

```bash
export ANTHROPIC_LOG=debug
```

### Making custom/undocumented requests

This library is typed for convenient access to the documented API. If you need to access undocumented endpoints, params, or response properties, the library can still be used.

#### Undocumented endpoints

To make requests to undocumented endpoints, you can use `client.get`, `client.post`, and other HTTP verbs. Options on the client, such as retries, are respected when making these requests.

```python
import httpx

response = client.post(
    "/foo",
    cast_to=httpx.Response,
    body={"my_param": True},
)

print(response.json())
```

#### Undocumented request params

If you want to explicitly send an extra parameter, you can do so with the `extra_query`, `extra_body`, and `extra_headers` request options.

<Warning>
  The `extra_` parameters override documented parameters of the same name. For security reasons, ensure these methods are only used with trusted input data.
</Warning>

#### Undocumented response properties

To access undocumented response properties, you can access the extra fields like `response.unknown_prop`. You can also get all extra fields on the Pydantic model as a dict with `response.model_extra`.

### Configuring the HTTP client

You can directly override the [httpx client](https://www.python-httpx.org/api/#client) to customize it for your use case, including support for proxies and transports:

```python
import httpx
from anthropic import Anthropic, DefaultHttpxClient

client = Anthropic(
    # Or use the `ANTHROPIC_BASE_URL` env var
    base_url="http://my.test.server.example.com:8083",
    http_client=DefaultHttpxClient(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

You can also customize the client on a per-request basis by using `with_options()`:

```python
client.with_options(http_client=DefaultHttpxClient(...))
```

<Note>
  Use `DefaultHttpxClient` and `DefaultAsyncHttpxClient` instead of raw `httpx.Client` and `httpx.AsyncClient` to ensure the SDK's default configuration (such as timeouts and connection limits) is preserved.
</Note>

### Managing HTTP resources

By default the library closes underlying HTTP connections whenever the client is [garbage collected](https://docs.python.org/3/reference/datamodel.html#object.__del__). You can manually close the client using the `.close()` method if desired, or with a context manager that closes when exiting.

```python
with Anthropic() as client:
    message = client.messages.create(...)

# HTTP client is automatically closed
```

## Beta features

Beta features are available before general release to get early feedback and test new functionality. You can check the availability of all of Claude's capabilities and tools in the [build with Claude overview](https://platform.claude.com/docs/en/build-with-claude/overview).

You can access most beta API features through the `beta` property of the client. To enable a particular beta feature, you need to add the appropriate [beta header](https://platform.claude.com/docs/en/api/beta-headers) to the `betas` field when creating a message.

For example, to enable [context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing):

```python
client = Anthropic()

response = client.beta.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    betas=["context-management-2025-06-27"],
)
```

## Platform integrations

<Note>
  For detailed platform setup guides with code examples, see:

  * [Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (Opus 4.6 and earlier)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws)
  * [Google Cloud](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai)
  * [Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry)
</Note>

All five client classes are included in the base `anthropic` package:

| Provider                         | Client                                         | Extra dependencies                 |
| -------------------------------- | ---------------------------------------------- | ---------------------------------- |
| Agent Platform                   | `from anthropic import AnthropicVertex`        | `pip install "anthropic[vertex]"`  |
| Bedrock                          | `from anthropic import AnthropicBedrockMantle` | `pip install "anthropic[bedrock]"` |
| Bedrock (`bedrock-runtime` path) | `from anthropic import AnthropicBedrock`       | `pip install "anthropic[bedrock]"` |
| Claude Platform on AWS           | `from anthropic import AnthropicAWS`           | `pip install "anthropic[aws]"`     |
| Foundry                          | `from anthropic import AnthropicFoundry`       | None                               |

The `AnthropicAWS` client is in beta. Pass `workspace_id` to the constructor or set the `ANTHROPIC_AWS_WORKSPACE_ID` environment variable.

Use `AnthropicBedrockMantle` for new projects; `AnthropicBedrock` remains for existing applications using the Bedrock `InvokeModel` API.

## Semantic versioning

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions, though certain backward-incompatible changes may be released as minor versions:

1. Changes that only affect static types, without breaking runtime behavior.
2. Changes to library internals which are technically public but not intended or documented for external use.
3. Changes that aren't expected to impact the vast majority of users in practice.

### Determining the installed version

If you've upgraded to the latest version but aren't seeing new features you were expecting, your Python environment is likely still using an older version. You can determine the version being used at runtime with:

```python
print(anthropic.__version__)
```

## Additional resources

* [GitHub repository](https://github.com/anthropics/anthropic-sdk-python)
* [API reference](https://platform.claude.com/docs/en/api/overview)
* [Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming)
* [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
