---
title: PHP SDK
url: https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/php
description: Install and configure the Anthropic PHP SDK with value objects and builder patterns
---

The Anthropic PHP library provides convenient access to the Claude API from any PHP 8.1.0+ application.

<Info>
  The PHP SDK is currently in beta. APIs might change between versions.
</Info>

<Info>
  For API feature documentation with code examples, see the [API reference](https://platform.claude.com/docs/en/api/overview). This page covers PHP-specific SDK features and configuration.
</Info>

## Installation

The SDK uses [PSR-18](https://www.php-fig.org/psr/psr-18/) for HTTP and discovers any installed PSR-18 client automatically. [Guzzle](https://docs.guzzlephp.org/) is recommended because the SDK configures it for streaming with no additional setup:

```bash
composer require "anthropic-ai/sdk" "guzzlehttp/guzzle:^7"
```

## Requirements

PHP 8.1.0 or higher.

## Usage

This library uses named parameters to specify optional arguments. Parameters with a default value must be set by name.

```php
$client = new Client();

$message = $client->messages->create(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-5',
);

$textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
echo $textBlock->text;
```

For authentication options including Workload Identity Federation, see [Authentication](https://platform.claude.com/docs/en/manage-claude/authentication).

## Value objects

It is recommended to use the static `with` constructor `Base64ImageSource::with(data: "U3RhaW5sZXNzIHJvY2tz", ...)` and named parameters to initialize value objects.

However, builders are also provided `(new Base64ImageSource)->withData("U3RhaW5sZXNzIHJvY2tz")`.

## Streaming

The SDK provides support for streaming responses using Server-Sent Events (SSE).

```php
$client = new Client();

$stream = $client->messages->createStream(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-5',
);

foreach ($stream as $event) {
  echo $event->type . PHP_EOL;
}
```

Streaming requires an HTTP client that returns the response body incrementally. When Guzzle is the discovered PSR-18 client, the SDK configures it for streaming automatically. With a buffering client, the `foreach` loop yields every event at once when the response completes instead of incrementally; if you observe that symptom, install Guzzle or supply a streaming-capable PSR-18 client through the `streamingTransporter` request option:

```php
$client = new Anthropic\Client(
  requestOptions: Anthropic\RequestOptions::with(streamingTransporter: $myStreamingClient),
);
```

## Error handling

When the library is unable to connect to the API, or if the API returns a non-success status code (that is, a 4xx or 5xx response), a subclass of `Anthropic\Core\Exceptions\APIException` is thrown:

```php
<?php
// ...
use Anthropic\Core\Exceptions\APIConnectionException;
use Anthropic\Core\Exceptions\APIStatusException;
use Anthropic\Core\Exceptions\RateLimitException;
// ...
try {
  $message = $client->messages->create(
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello, Claude']],
    model: 'claude-opus-5',
  );
} catch (APIConnectionException $e) {
  echo "The server could not be reached", PHP_EOL;
  echo $e->getPrevious()?->getMessage(), PHP_EOL;
} catch (RateLimitException $_) {
  echo "A 429 status code was received; we should back off a bit.", PHP_EOL;
} catch (APIStatusException $e) {
  echo "Another non-200-range status code was received", PHP_EOL;
  echo $e->getMessage();
}
```

Error codes are as follows:

| Cause            | Error Type                     |
| ---------------- | ------------------------------ |
| HTTP 400         | `BadRequestException`          |
| HTTP 401         | `AuthenticationException`      |
| HTTP 403         | `PermissionDeniedException`    |
| HTTP 404         | `NotFoundException`            |
| HTTP 409         | `ConflictException`            |
| HTTP 422         | `UnprocessableEntityException` |
| HTTP 429         | `RateLimitException`           |
| HTTP >= 500      | `InternalServerException`      |
| Other HTTP error | `APIStatusException`           |
| Timeout          | `APITimeoutException`          |
| Network error    | `APIConnectionException`       |

## Retries

Certain errors are automatically retried two times by default, with a short exponential backoff.

Connection errors (for example, because of a network connectivity problem), 408 Request Timeout, 409 Conflict, 429 Rate Limit, >=500 Internal errors, and timeouts are all retried by default.

You can use the `maxRetries` option to configure or disable this:

```php
use Anthropic\RequestOptions;
// ...
// Configure the default for all requests:
$client = new Client(requestOptions: RequestOptions::with(maxRetries: 0));

// Or, configure per-request:
$result = $client->messages->create(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-5',
  requestOptions: RequestOptions::with(maxRetries: 5),
);
```

## Pagination

List methods in the Claude API are paginated.

This library provides auto-paginating iterators with each list response, so you do not have to request successive pages manually:

```php
$client = new Client();

$page = $client->beta->messages->batches->list(limit: 20);

// fetch items from the current page
foreach ($page->getItems() as $item) {
  echo $item->id, PHP_EOL;
}
// make additional network requests to fetch items from all pages, including and after the current page
foreach ($page->pagingEachItem() as $item) {
  echo $item->id, PHP_EOL;
}
```

## Advanced usage

### Undocumented properties

You can send undocumented parameters to any endpoint, and read undocumented response properties, as follows:

<Note>
  The `extra*` parameters of the same name override the documented parameters.
</Note>

```php
<?php
// ...
use Anthropic\RequestOptions;
// ...
$message = $client->messages->create(
  maxTokens: 1024,
  messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  model: 'claude-opus-5',
  requestOptions: RequestOptions::with(
    extraQueryParams: ['my_query_parameter' => 'value'],
    extraBodyParams: ['my_body_parameter' => 'value'],
    extraHeaders: ['my-header' => 'value'],
  ),
);
```

### Undocumented request parameters

If you want to explicitly send an extra parameter, you can do so with the `extraQueryParams`, `extraBodyParams`, and `extraHeaders` options under `RequestOptions::with()` when making a request, as seen in the preceding example.

### Undocumented endpoints

To make requests to undocumented endpoints while retaining the benefit of authentication, retries, and other client features, you can make requests using `client->request`, as follows:

```php
$client = new Client();

$response = $client->request(
  method: "post",
  path: '/undocumented/endpoint',
  query: ['dog' => 'woof'],
  headers: ['useful-header' => 'interesting-value'],
  body: ['hello' => 'world']
);
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

The PHP SDK supports the following platforms:

* **Agent Platform:** `Anthropic\Vertex\Client`. Use `::fromEnvironment()`.
* **Bedrock:** `Anthropic\Bedrock\MantleClient`. Use `new MantleClient(awsRegion: ...)`.
* **Bedrock (legacy):** `Anthropic\Bedrock\Client`. Use `::fromEnvironment()` or `::withCredentials()`.
* **Claude Platform on AWS:** `Anthropic\Aws\Client` (requires `aws/aws-sdk-php` as a soft dependency). Use `new Anthropic\Aws\Client(workspaceId: ...)` or set `ANTHROPIC_AWS_WORKSPACE_ID`. Available in beta.
* **Foundry:** `Anthropic\Foundry\Client`. Use `::withCredentials()`.

Use `MantleClient` for new projects; `Anthropic\Bedrock\Client` remains for existing applications using the Bedrock `InvokeModel` API.

## Semantic versioning

This package follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions. As the library is in initial development and has a major version of `0`, APIs might change at any time.

This package considers improvements to the (non-runtime) PHPDoc type definitions to be non-breaking changes.

## Additional resources

* [GitHub repository](https://github.com/anthropics/anthropic-sdk-php)
* [Packagist](https://packagist.org/packages/anthropic-ai/sdk)
* [API reference](https://platform.claude.com/docs/en/api/overview)
* [Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming)
