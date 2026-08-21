---
title: Ruby SDK
url: https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/ruby
description: Install and configure the Anthropic Ruby SDK with Sorbet types, streaming helpers, and connection pooling
---

The Anthropic Ruby library provides convenient access to the Claude API from any Ruby 3.2.0+ application. It ships with comprehensive types and docstrings in Yard, RBS, and RBI. The standard library's `net/http` is used as the HTTP transport, with connection pooling through the `connection_pool` gem.

<Info>
  For API feature documentation with code examples, see the [API reference](https://platform.claude.com/docs/en/api/overview). This page covers Ruby-specific SDK features and configuration.
</Info>

## Installation

Add the gem to your application's `Gemfile` with Bundler:

```bash
bundle add anthropic
```

## Requirements

Ruby 3.2.0 or higher.

## Usage

```ruby
anthropic = Anthropic::Client.new(
  api_key: ENV["ANTHROPIC_API_KEY"] # This is the default and can be omitted
)

message = anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-5"
)

message.content.each do |block|
  puts block.text if block.type == :text
end
```

For authentication options including Workload Identity Federation, see [Authentication](https://platform.claude.com/docs/en/manage-claude/authentication).

## Streaming

The SDK provides support for streaming responses using Server-Sent Events (SSE).

```ruby
anthropic = Anthropic::Client.new
stream = anthropic.messages.stream(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-5"
)

stream.each do |message|
  puts(message.type)
end
```

### Streaming helpers

This library provides several conveniences for streaming messages, for example:

```ruby
anthropic = Anthropic::Client.new
stream = anthropic.messages.stream(
  max_tokens: 1024,
  messages: [{role: :user, content: "Say hello there!"}],
  model: :"claude-opus-5"
)

stream.text.each do |text|
  print(text)
end
```

Streaming with `anthropic.messages.stream(...)` exposes various helpers including accumulation and SDK-specific events.

## Input schema and tool calling

The SDK provides helper mechanisms to define structured data classes for tools and let Claude automatically execute them. For detailed documentation on tool use patterns including the tool runner, see [Tool Runner (SDK)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner).

```ruby
anthropic = Anthropic::Client.new
class CalculatorInput < Anthropic::BaseModel
  required :lhs, Float
  required :rhs, Float
  required :operator, Anthropic::InputSchema::EnumOf[:+, :-, :*, :/]
end

class Calculator < Anthropic::BaseTool
  input_schema CalculatorInput

  def call(expr)
    expr.lhs.public_send(expr.operator, expr.rhs)
  end
end

# Automatically handles tool execution loop
anthropic.beta.messages.tool_runner(
  model: "claude-opus-5",
  max_tokens: 1024,
  messages: [{role: "user", content: "What's 15 * 7?"}],
  tools: [Calculator.new]
).each_message { |message| puts message.content }
```

## Structured outputs

For complete structured outputs documentation including Ruby examples, see [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs).

## Handling errors

When the library is unable to connect to the API, or if the API returns a non-success status code (that is, 4xx or 5xx response), a subclass of `Anthropic::Errors::APIError` is raised:

```ruby
anthropic = Anthropic::Client.new
begin
  message = anthropic.messages.create(
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    model: :"claude-opus-5"
  )
rescue Anthropic::Errors::APIConnectionError => e
  puts("The server could not be reached")
  puts(e.cause)  # an underlying Exception, likely raised within `net/http`
rescue Anthropic::Errors::RateLimitError => e
  puts("A 429 status code was received; we should back off a bit.")
rescue Anthropic::Errors::APIStatusError => e
  puts("Another non-200-range status code was received")
  puts(e.status)
end
```

Error codes are as follows:

| Cause            | Error Type                 |
| ---------------- | -------------------------- |
| HTTP 400         | `BadRequestError`          |
| HTTP 401         | `AuthenticationError`      |
| HTTP 403         | `PermissionDeniedError`    |
| HTTP 404         | `NotFoundError`            |
| HTTP 409         | `ConflictError`            |
| HTTP 422         | `UnprocessableEntityError` |
| HTTP 429         | `RateLimitError`           |
| HTTP >= 500      | `InternalServerError`      |
| Other HTTP error | `APIStatusError`           |
| Timeout          | `APITimeoutError`          |
| Network error    | `APIConnectionError`       |

## Retries

Certain errors will be automatically retried 2 times by default, with a short exponential backoff.

Connection errors (for example, because of a network connectivity problem), 408 Request Timeout, 409 Conflict, 429 Rate Limit, >=500 Internal errors, and timeouts are all retried by default.

You can use the `max_retries` option to configure or disable this:

```ruby
# Configure the default for all requests:
anthropic = Anthropic::Client.new(
  max_retries: 0 # default is 2
)

# Or, configure per-request:
anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-5",
  request_options: {max_retries: 5}
)
```

## Timeouts

By default, requests time out after 10 minutes. You can use the `timeout` option to configure this:

```ruby
# Configure the default for all requests:
anthropic = Anthropic::Client.new(
  timeout: 20 # 20 seconds (default is 10 minutes)
)

# Or, configure per-request:
anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-5",
  request_options: {timeout: 5}
)
```

On timeout, `Anthropic::Errors::APITimeoutError` is raised.

Note that requests that time out are retried by default.

## Pagination

List methods in the Claude API are paginated.

This library provides auto-paginating iterators with each list response, so you do not have to request successive pages manually:

```ruby
anthropic = Anthropic::Client.new
page = anthropic.messages.batches.list(limit: 20)

# Fetch single item from page.
batch = page.data[0]
puts(batch.id)

# Automatically fetches more pages as needed.
page.auto_paging_each do |batch|
  puts(batch.id)
end
```

Alternatively, you can use the `#next_page?` and `#next_page` methods for more granular control working with pages.

```ruby
anthropic = Anthropic::Client.new
page = anthropic.messages.batches.list(limit: 20)
loop do
  page.data&.each { |batch| puts(batch.id) }
  break unless page.next_page?
  page = page.next_page
end
```

## File uploads

Request parameters that correspond to file uploads can be passed as raw contents, a [`Pathname`](https://rubyapi.org/3.2/o/pathname) instance, [`StringIO`](https://rubyapi.org/3.2/o/stringio), or more.

```ruby
anthropic = Anthropic::Client.new
require "pathname"

# Use `Pathname` to send the filename and/or avoid paging a large file into memory:
file_metadata = anthropic.files.upload(file: Pathname("/path/to/file"))

# Alternatively, pass file contents or a `StringIO` directly:
file_metadata = anthropic.files.upload(file: File.read("/path/to/file"))

# Or, to control the filename and/or content type:
file = Anthropic::FilePart.new(File.read("/path/to/file"), filename: "/path/to/file", content_type: "...")
file_metadata = anthropic.files.upload(file: file)

puts(file_metadata.id)
```

Note that you can also pass a raw `IO` descriptor, but this disables retries, as the library can't be sure if the descriptor is a file or pipe (which cannot be rewound).

## Sorbet

This library provides comprehensive [RBI](https://sorbet.org/docs/rbi) definitions, and has no dependency on sorbet-runtime.

You can provide typesafe request parameters like so:

```ruby
anthropic = Anthropic::Client.new
anthropic.messages.create(
  max_tokens: 1024,
  messages: [Anthropic::MessageParam.new(role: "user", content: "Hello, Claude")],
  model: :"claude-opus-5"
)
```

Or, equivalently:

```ruby
anthropic = Anthropic::Client.new
# Hashes work, but are not typesafe:
anthropic.messages.create(
  max_tokens: 1024,
  messages: [{role: "user", content: "Hello, Claude"}],
  model: :"claude-opus-5"
)

# You can also splat a full Params class:
params = Anthropic::MessageCreateParams.new(
  max_tokens: 1024,
  messages: [Anthropic::MessageParam.new(role: "user", content: "Hello, Claude")],
  model: :"claude-opus-5"
)
anthropic.messages.create(**params)
```

### Enums

Since this library does not depend on `sorbet-runtime`, it cannot provide [`T::Enum`](https://sorbet.org/docs/tenum) instances. Instead, the SDK provides "tagged symbols", which is always a primitive at runtime:

```ruby
# :auto
puts(Anthropic::MessageCreateParams::ServiceTier::AUTO)

# Revealed type: `T.all(Anthropic::MessageCreateParams::ServiceTier, Symbol)`
T.reveal_type(Anthropic::MessageCreateParams::ServiceTier::AUTO)
```

Enum parameters have a "relaxed" type, so you can either pass in enum constants or their literal value:

```ruby
# Using the enum constants preserves the tagged type information:
anthropic.messages.create(
  service_tier: Anthropic::MessageCreateParams::ServiceTier::AUTO,
  # ...
)

# Literal values are also permissible:
anthropic.messages.create(
  service_tier: :auto,
  # ...
)
```

## BaseModel

All parameter and response objects inherit from `Anthropic::Internal::Type::BaseModel`, which provides several conveniences, including:

1. All fields, including unknown ones, are accessible with `obj[:prop]` syntax, and can be destructured with `obj => {prop: prop}` or pattern-matching syntax.

2. Structural equivalence for equality; if two API calls return the same values, comparing the responses with == will return true.

3. Both instances and the classes themselves can be pretty-printed.

4. Helpers such as `#to_h`, `#deep_to_h`, `#to_json`, and `#to_yaml`.

## Concurrency and connection pooling

The `Anthropic::Client` instances are threadsafe, but are only fork-safe when there are no in-flight HTTP requests.

Each instance of `Anthropic::Client` has its own HTTP connection pool with a default size of 99. As such, the recommendation is to create the client once per application in most settings.

When all available connections from the pool are checked out, requests wait for a new connection to become available, with queue time counting toward the request timeout.

Unless otherwise specified, other classes in the SDK do not have locks protecting their underlying data structure.

## Making custom or undocumented requests

### Undocumented properties

You can send undocumented parameters to any endpoint, and read undocumented response properties, like so:

<Warning>
  The `extra_` parameters of the same name override the documented parameters. For security reasons, ensure these methods are only used with trusted input data.
</Warning>

```ruby
anthropic = Anthropic::Client.new
value = "example"
message =
  anthropic.messages.create(
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    model: :"claude-opus-5",
    request_options: {
      extra_query: {my_query_parameter: value},
      extra_body: {my_body_parameter: value},
      extra_headers: {"my-header": value}
    }
  )

puts(message[:my_undocumented_property])
```

### Undocumented request params

If you want to explicitly send an extra param, you can do so with the `extra_query`, `extra_body`, and `extra_headers` under the `request_options:` parameter when making a request, as seen in the examples above.

### Undocumented endpoints

To make requests to undocumented endpoints while retaining the benefit of auth, retries, and so on, you can make requests using `anthropic.request`, like so:

```ruby
response = anthropic.request(
  method: :post,
  path: '/undocumented/endpoint',
  query: {"dog": "woof"},
  headers: {"useful-header": "interesting-value"},
  body: {"hello": "world"}
)
```

## Platform integrations

<Note>
  For detailed platform setup guides with code examples, see:

  * [Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (Opus 4.6 and earlier)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws)
  * [Google Cloud](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai)
</Note>

The Ruby SDK supports the following platforms:

* **Agent Platform:** `Anthropic::VertexClient`. Requires the `googleauth` gem.
* **Bedrock:** `Anthropic::BedrockMantleClient`, or `Anthropic::BedrockClient` for the `bedrock-runtime` path. `Anthropic::BedrockMantleClient` requires the `aws-sdk-core` gem; `Anthropic::BedrockClient` requires the `aws-sdk-bedrockruntime` gem.
* **Claude Platform on AWS:** Part of the main `anthropic` gem (requires the `aws-sdk-core` gem). Provides `Anthropic::AWSClient`. Pass `workspace_id:` to the constructor or set the `ANTHROPIC_AWS_WORKSPACE_ID` environment variable (see [Workspaces](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws#workspaces)). Available in beta.
* **Foundry:** Not currently supported in the Ruby SDK. See [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry) for supported SDKs.

Use `Anthropic::BedrockMantleClient` for new projects; `Anthropic::BedrockClient` remains for existing applications using the Bedrock `InvokeModel` API.

## Semantic versioning

This package follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions.

This package considers improvements to the (non-runtime) `*.rbi` and `*.rbs` type definitions to be non-breaking changes.

## Additional resources

* [GitHub repository](https://github.com/anthropics/anthropic-sdk-ruby)
* [YARD documentation](https://gemdocs.org/gems/anthropic)
* [API reference](https://platform.claude.com/docs/en/api/overview)
* [Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming)
