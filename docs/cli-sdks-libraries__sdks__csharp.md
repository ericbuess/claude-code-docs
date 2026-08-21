---
title: C# SDK
url: https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/csharp
description: Install and configure the Anthropic C# SDK for .NET applications with IChatClient integration
---

The Anthropic C# SDK provides convenient access to the Claude API from applications written in C#.

<Info>
  The C# SDK is currently in beta. APIs may change between versions.
</Info>

<Info>
  For API feature documentation with code examples, see the [API reference](https://platform.claude.com/docs/en/api/overview). This page covers C#-specific SDK features and configuration.
</Info>

<Warning>
  As of version 10+, the `Anthropic` package is now the official Anthropic SDK for C#. Package versions 3.X and below were previously used for the tryAGI community-built SDK, which has moved to [`tryAGI.Anthropic`](https://www.nuget.org/packages/tryagi.Anthropic/). If you need to continue using the former client in your project, update your package reference to `tryAGI.Anthropic`.
</Warning>

## Installation

Install the package from [NuGet](https://www.nuget.org/packages/Anthropic):

```bash
dotnet add package Anthropic
```

## Requirements

This library requires .NET Standard 2.0 or later.

## Usage

```csharp
using System;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new();

MessageCreateParams parameters = new()
{
    MaxTokens = 1024,
    Messages =
    [
        new()
        {
            Role = Role.User,
            Content = "Hello, Claude",
        },
    ],
    Model = Model.ClaudeOpus5,
};

var message = await client.Messages.Create(parameters);

foreach (var block in message.Content)
{
    if (block.TryPickText(out var textBlock))
    {
        Console.WriteLine(textBlock.Text);
    }
}
```

For authentication options including Workload Identity Federation, see [Authentication](https://platform.claude.com/docs/en/manage-claude/authentication).

## Client configuration

Configure the client using environment variables:

```csharp
using Anthropic;

// Configured using the ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN and ANTHROPIC_BASE_URL environment variables
AnthropicClient client = new();
```

Or manually:

```csharp
using Anthropic;

AnthropicClient client = new() { ApiKey = "my-anthropic-api-key" };
```

Or using a combination of the two approaches.

See this table for the available options:

| Property    | Environment variable   | Required | Default value                 |
| ----------- | ---------------------- | -------- | ----------------------------- |
| `ApiKey`    | `ANTHROPIC_API_KEY`    | false    | -                             |
| `AuthToken` | `ANTHROPIC_AUTH_TOKEN` | false    | -                             |
| `BaseUrl`   | `ANTHROPIC_BASE_URL`   | true     | `"https://api.anthropic.com"` |

### Modifying configuration

To temporarily use a modified client configuration, while reusing the same connection and thread pools, call `WithOptions` on any client or service:

```csharp
using System;

var message = await client
    .WithOptions(options =>
        options with
        {
            BaseUrl = "https://example.com",
            Timeout = TimeSpan.FromSeconds(42),
        }
    )
    .Messages.Create(parameters);

Console.WriteLine(message);
```

Using a [`with` expression](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/with-expression) makes it easy to construct the modified options.

The `WithOptions` method does not affect the original client or service.

## Streaming

The SDK defines methods that return response "chunk" streams, where each chunk can be individually processed as soon as it arrives instead of waiting on the full response. Streaming methods generally correspond to [SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) or [JSONL](https://jsonlines.org) responses.

A streaming method always has a `Streaming` suffix in its name, even if it doesn't have a non-streaming variant.

These streaming methods return [`IAsyncEnumerable`](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.iasyncenumerable-1):

```csharp
using System;
using Anthropic.Models.Messages;

MessageCreateParams parameters = new()
{
    MaxTokens = 1024,
    Messages =
    [
        new()
        {
            Role = Role.User,
            Content = "Hello, Claude",
        },
    ],
    Model = Model.ClaudeOpus5,
};

await foreach (var message in client.Messages.CreateStreaming(parameters))
{
    Console.WriteLine(message);
}
```

## Error handling

The SDK throws custom unchecked exception types:

* `AnthropicApiException`: Base class for API errors. See this table for which exception subclass is thrown for each HTTP status code:

| Status | Exception                                |
| ------ | ---------------------------------------- |
| 400    | `AnthropicBadRequestException`           |
| 401    | `AnthropicUnauthorizedException`         |
| 403    | `AnthropicForbiddenException`            |
| 404    | `AnthropicNotFoundException`             |
| 422    | `AnthropicUnprocessableEntityException`  |
| 429    | `AnthropicRateLimitException`            |
| 5xx    | `Anthropic5xxException`                  |
| others | `AnthropicUnexpectedStatusCodeException` |

Additionally, all 4xx errors inherit from `Anthropic4xxException`.

* `AnthropicSseException`: thrown for errors encountered during SSE streaming after a successful initial HTTP response.

* `AnthropicIOException`: I/O networking errors.

* `AnthropicInvalidDataException`: Failure to interpret successfully parsed data. For example, when accessing a property that's supposed to be required, but the API unexpectedly omitted it from the response.

* `AnthropicException`: Base class for all exceptions.

## Retries

The SDK automatically retries 2 times by default, with a short exponential backoff between requests.

Only the following error types are retried:

* Connection errors (for example, because of a network connectivity problem)
* 408 Request Timeout
* 409 Conflict
* 429 Rate Limit
* 5xx Internal

The API may also explicitly instruct the SDK to retry or not retry a request.

To set a custom number of retries, configure the client using the `MaxRetries` property:

```csharp
using Anthropic;

AnthropicClient client = new() { MaxRetries = 3 };
```

Or configure a single method call using `WithOptions`:

```csharp
using System;

var message = await client
    .WithOptions(options =>
        options with { MaxRetries = 3 }
    )
    .Messages.Create(parameters);

Console.WriteLine(message);
```

## Timeouts

Requests time out after 10 minutes by default.

To set a custom timeout, configure the client using the `Timeout` option:

```csharp
using System;
using Anthropic;

AnthropicClient client = new() { Timeout = TimeSpan.FromSeconds(42) };
```

Or configure a single method call using `WithOptions`:

```csharp
using System;

var message = await client
    .WithOptions(options =>
        options with { Timeout = TimeSpan.FromSeconds(42) }
    )
    .Messages.Create(parameters);

Console.WriteLine(message);
```

## Pagination

The SDK defines methods that return paginated lists of results. It provides convenient ways to access the results either one page at a time or item-by-item across all pages.

### Auto-pagination

To iterate through all results across all pages, use the `Paginate` method, which automatically fetches more pages as needed. The method returns an [`IAsyncEnumerable`](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.iasyncenumerable-1):

```csharp
using System;

var page = await client.Messages.Batches.List(parameters);
await foreach (var item in page.Paginate())
{
    Console.WriteLine(item);
}
```

### Manual pagination

To access individual page items and manually request the next page, use the `Items` property, and `HasNext` and `Next` methods:

```csharp
var page = await client.Messages.Batches.List();
while (true)
{
    foreach (var item in page.Items)
    {
        Console.WriteLine(item);
    }
    if (!page.HasNext())
    {
        break;
    }
    page = await page.Next();
}
```

## Response validation

In rare cases, the API may return a response that doesn't match the expected type. By default, the SDK does not throw an exception in this case. It throws `AnthropicInvalidDataException` only if you directly access the property.

If you would prefer to check that the response is completely well-typed upfront, then either call `Validate`:

```csharp
var message = await client.Messages.Create(parameters);
message.Validate();
```

Or configure the client using the `ResponseValidation` option:

```csharp
using Anthropic;

AnthropicClient client = new() { ResponseValidation = true };
```

Or configure a single method call using `WithOptions`:

```csharp
using System;

var message = await client
    .WithOptions(options =>
        options with { ResponseValidation = true }
    )
    .Messages.Create(parameters);

Console.WriteLine(message);
```

## IChatClient integration

The SDK provides an implementation of the `IChatClient` interface from the `Microsoft.Extensions.AI.Abstractions` library. This enables `AnthropicClient` (and `Anthropic.Services.IBetaService`) to be used with other libraries that integrate with these core abstractions. For example, tools in the MCP C# SDK (`ModelContextProtocol`) library can be used directly with an `AnthropicClient` exposed through `IChatClient`.

```csharp
using Anthropic;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;

// Configured using the ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN and ANTHROPIC_BASE_URL environment variables
AnthropicClient client = new();

IChatClient chatClient = client.AsIChatClient("claude-opus-5")
    .AsBuilder()
    .UseFunctionInvocation()
    .Build();

// Using McpClient from the MCP C# SDK
McpClient learningServer = await McpClient.CreateAsync(
    new HttpClientTransport(new() { Endpoint = new("https://learn.microsoft.com/api/mcp") }));

ChatOptions options = new() { Tools = [.. await learningServer.ListToolsAsync()] };

Console.WriteLine(await chatClient.GetResponseAsync("Tell me about IChatClient", options));
```

## Requests and responses

To send a request to the Claude API, build an instance of a `Params` class and pass it to the corresponding client method. When the response is received, it's deserialized into an instance of a C# class.

For example, `client.Messages.Create` should be called with an instance of `MessageCreateParams`, and it will return an instance of `Task<Message>`.

## Advanced usage

### Binary responses

The SDK defines methods that return binary responses, which are used for API responses that shouldn't necessarily be parsed, like non-JSON data.

These methods return `HttpResponse`:

```csharp
using System;
using Anthropic.Models.Files;

FileDownloadParams parameters = new() { FileID = "file_id" };

var response = await client.Files.Download(parameters);

Console.WriteLine(response);
```

To save the response content to a file, or any [`Stream`](https://learn.microsoft.com/en-us/dotnet/api/system.io.stream), use the [`CopyToAsync`](https://learn.microsoft.com/en-us/dotnet/api/system.io.stream.copytoasync) method:

```csharp
using System.IO;

using var response = await client.Files.Download(parameters);
using var contentStream = await response.ReadAsStream();
using var fileStream = File.Open(path, FileMode.OpenOrCreate);
await contentStream.CopyToAsync(fileStream); // Or any other Stream
```

### Raw responses

The SDK defines methods that deserialize responses into instances of C# classes. To access response headers, status code, or the raw response body, prefix any HTTP method call on a client or service with `WithRawResponse`:

```csharp
var response = await client.WithRawResponse.Messages.Create(parameters);
var statusCode = response.StatusCode;
var headers = response.Headers;
```

The raw `HttpResponseMessage` can also be accessed through the `RawMessage` property.

For non-streaming responses, you can deserialize the response into an instance of a C# class if needed:

```csharp
using System;
using Anthropic.Models.Messages;

var response = await client.WithRawResponse.Messages.Create(parameters);
Message deserialized = await response.Deserialize();
Console.WriteLine(deserialized);
```

For streaming responses, you can deserialize the response to an `IAsyncEnumerable` if needed:

```csharp
using System;

var response = await client.WithRawResponse.Messages.CreateStreaming(parameters);
await foreach (var item in response.Enumerate())
{
    Console.WriteLine(item);
}
```

### Logging

<Warning>
  All log messages are intended for debugging only. The format and content of log messages may change between releases.
</Warning>

Enable debug logging by setting an environment variable:

```bash
export ANTHROPIC_LOG=debug
```

### Undocumented API functionality

The SDK is typed for convenient usage of the documented API. However, it also supports working with undocumented or not yet supported parts of the API.

## Platform integrations

<Note>
  For detailed platform setup guides with code examples, see:

  * [Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (Opus 4.6 and earlier)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws)
  * [Google Cloud](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai)
  * [Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry)
</Note>

The C# SDK supports the following platforms through separate NuGet packages:

* **Agent Platform:** `Anthropic.Vertex`. See [Claude on Google Cloud](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai) for client setup.
* **Bedrock:** `Anthropic.Bedrock`. Use `AnthropicBedrockMantleClient` for the Messages-API Bedrock endpoint, or `AnthropicBedrockClient` (`bedrock-runtime` path). `AnthropicBedrockMantleClient` takes an optional `MantleAwsClientOptions` config object; `AnthropicBedrockClient` accepts `AnthropicBedrockCredentialsHelper.FromEnv()` or explicit credentials.
* **Claude Platform on AWS:** `Anthropic.Aws`. Use `AnthropicAwsClient`; set `WorkspaceId` on the client or the `ANTHROPIC_AWS_WORKSPACE_ID` environment variable (see [Workspaces](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws#workspaces)). Available in beta.
* **Foundry:** `Anthropic.Foundry`. Use `AnthropicFoundryClient` with `DefaultAnthropicFoundryCredentials.FromEnv()` or explicit credentials.

Use `AnthropicBedrockMantleClient` for new projects; `AnthropicBedrockClient` remains for existing applications using the Bedrock `InvokeModel` API.

## Semantic versioning

<Warning>
  Although this package is versioned as 10+, it's currently in beta. During the beta period, breaking changes may occur in minor or patch releases. Once the library reaches stable release, SemVer conventions will be followed more strictly. Share feedback by [filing an issue](https://github.com/anthropics/anthropic-sdk-csharp/issues/new).
</Warning>

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions, though certain backward-incompatible changes may be released as minor versions:

1. Changes to library internals that are technically public but not intended or documented for external use.
2. Changes that aren't expected to impact the vast majority of users in practice.

Backward-compatibility is taken seriously to ensure you can rely on a smooth upgrade experience.

## Additional resources

* [GitHub repository](https://github.com/anthropics/anthropic-sdk-csharp)
* [NuGet package](https://www.nuget.org/packages/Anthropic)
* [API reference](https://platform.claude.com/docs/en/api/overview)
* [Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming)
