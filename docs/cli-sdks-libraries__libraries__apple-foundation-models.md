---
title: Apple Foundation Models
url: https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/apple-foundation-models
description: Use Claude on Apple platforms through the Foundation Models framework with the Claude for Foundation Models Swift package.
---

[Claude for Foundation Models](https://github.com/anthropics/ClaudeForFoundationModels) is a Swift package that makes Claude available as a server-side language model in Apple's [Foundation Models](https://developer.apple.com/documentation/foundationmodels) framework. The package conforms Claude to the framework's `LanguageModel` protocol, so you drive it with the same `LanguageModelSession` API you use for Apple's on-device model: `respond(to:)`, streaming, guided generation, and tool calling all work the same way.

Requests go directly from your app to the Claude API; Apple is not in the request path and does not see prompts or responses. Usage is billed to your Anthropic account at [standard API pricing](https://platform.claude.com/docs/en/about-claude/pricing), so your organization needs an available credit balance or an active billing method. Your app decides when to use Claude and when to use Apple's on-device model: pass whichever model you want to each session.

<Note>
  **Beta.** This package targets the Foundation Models server-side language model API introduced in the OS 27 betas. APIs might change before general availability.
</Note>

<Info>
  Claude for Foundation Models is **not** a general-purpose Messages API client. Its public surface is the Foundation Models provider conformance plus the configuration types that reach it (`ClaudeLanguageModel`, `ClaudeModel`, `AuthMode`, `ClaudeServerTool`). For direct access to the Messages API in another language, see the [Client SDKs](https://platform.claude.com/docs/en/cli-sdks-libraries/overview#client-sdks).
</Info>

## Requirements

* iOS 27, macOS 27, visionOS 27, or watchOS 27 (all in beta): the OS releases whose Foundation Models framework supports server-side language models
* Xcode 27 (beta)
* A Claude API key from the [Claude Console](https://platform.claude.com/) for development. See [Authentication](https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/apple-foundation-models#authentication) for production options.

## Install the package

Add the package to your `Package.swift`:

```swift
dependencies: [
  .package(url: "https://github.com/anthropics/ClaudeForFoundationModels.git", from: "0.1.0")
]
```

Or in Xcode: **File** > **Add Package Dependencies…** and enter the repository URL.

Then add `ClaudeForFoundationModels` to your target's dependencies and import it alongside `FoundationModels`:

```swift
import FoundationModels
import ClaudeForFoundationModels
```

## Quick start

`ClaudeLanguageModel` is the entry point. Pass it to `LanguageModelSession` and use the session exactly as you would with any Foundation Models provider:

```swift
import FoundationModels
import ClaudeForFoundationModels

let model = ClaudeLanguageModel(
  name: .sonnet5,
  auth: .apiKey(ProcessInfo.processInfo.environment["ANTHROPIC_API_KEY"] ?? "")
)

let session = LanguageModelSession(model: model)
let response = try await session.respond(to: "Plan a 4-day trip to Buenos Aires.")
print(response.content)
```

The initializer also accepts `baseURL` (default `https://api.anthropic.com`), `timeout`, and `serverTools` (see [Server-side tools](https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/apple-foundation-models#server-side-tools)).

For a complete working program, the repository includes [`Examples/ClaudeExample`](https://github.com/anthropics/ClaudeForFoundationModels/tree/main/Examples/ClaudeExample), a runnable command-line target that streams a chat turn to the terminal, with a `--search` flag that enables server-side web search for the turn. Running it requires a macOS 27 host.

## Choosing a model

Model identifiers are values of `ClaudeModel`. Use a compiled-in constant, or construct one with explicit capabilities for an ID that isn't compiled in yet (see [Capabilities](https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/apple-foundation-models#capabilities)):

```swift
ClaudeLanguageModel(name: .opus5, auth: auth)
```

Constants mirror API model IDs (`.opus5` is `claude-opus-5`) and carry each model's capabilities. New models ship as new constants in package releases; check `ClaudeModel` in Xcode for the current list, and the [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) to compare models.

### Capabilities

Each `ClaudeModel` declares what it accepts: sampling parameters, effort levels, adaptive thinking, structured output, and image input. The package uses this to determine which request fields to send, because sending a field a model rejects is a hard error. The constants carry the right capabilities. For an ID that isn't compiled in, declare what the model accepts (there is deliberately no shorthand that guesses):

```swift
let model = ClaudeModel(
  id: "claude-experimental-x",
  capabilities: .init(samplingParams: false, effortLevels: [.low, .high])
)
ClaudeLanguageModel(name: model, auth: auth)
```

### Effort

Pin a Claude [effort level](https://platform.claude.com/docs/en/build-with-claude/effort) for every request with `fixedEffort:`. It takes precedence over the framework's per-request reasoning hints. The framework's named reasoning levels stop at high; to request more effort for a single request instead, pass a custom reasoning level naming the Claude effort (`.custom("xhigh")` or `.custom("max")`), which maps directly. The API defaults to `high` when no effort is sent:

```swift
ClaudeLanguageModel(name: .opus5, auth: auth, fixedEffort: .xhigh)
```

The level must be one the model accepts. Each `ClaudeModel` declares which of the five levels (`low`, `medium`, `high`, `xhigh`, `max`) its model takes, if any: some models don't accept effort at all.

### When to use Claude versus the on-device model

Apple's on-device model is fast, private, and available offline, but it is sized for lightweight tasks. Escalate to Claude when you need larger context, frontier reasoning, or server-side tools such as web search and code execution. Because both use the same `LanguageModelSession` API, you can switch by swapping the `model:` argument.

## Authentication

Set the credential with the `auth:` parameter. Use `.appAttest` to ship without a back end, `.proxied` to route requests through your own back end, or `.apiKey` to iterate during development.

### App Attest

Each installation of your app uses Apple's [App Attest](https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity) service to prove that it is a genuine, unmodified build of the app you registered. Anthropic then issues the device a short-lived access token that bills usage to your workspace. The app ships no API key, and there is no proxy for you to operate.

App Attest authentication is available only when your app calls the Claude API directly. It is not available through Amazon Bedrock, Google Cloud, or Microsoft Foundry.

To ship without running a back end, use `.appAttest`:

```swift
ClaudeLanguageModel(
  name: .sonnet5,
  auth: .appAttest(clientID: "clid_...")
)
```

<Note>
  App Attest requires a physical device. The Simulator, and hardware without a Secure Enclave, cannot perform App Attest. Use `.apiKey` while iterating in the Simulator, and `.appAttest` when running on a device.
</Note>

To set up App Attest, you need your Apple Developer Team ID and the admin, owner, or primary owner role in your organization. Configure your Xcode project and register your app in the [Claude Console](https://platform.claude.com/):

1. In Xcode, add the **App Attest** capability to your app target under **Signing & Capabilities**.
2. In your workspace's settings in the Claude Console, open **App integrations**.
3. Click **Create app integration** and enter a name, your Apple Developer Team ID, and one or more bundle IDs (up to 32).
4. Copy the client ID (`clid_...`) from the integration's **Overview** tab and pass it to your app's Claude configuration.

The first time your app uses Claude on a device, the app requests a challenge from Anthropic, attests the device with Apple's `DCAppAttestService`, and exchanges the verified attestation for an access token. The Claude for Foundation Models package runs this flow automatically and requests new tokens as they expire; there is no attestation code for you to write.

Tokens are scoped to your workspace, expire after one hour, and authorize only [Messages API](https://platform.claude.com/docs/en/api/messages/create) calls. They carry no end-user identity: App Attest identifies your app, not the person using it, so handle any per-user logic in your app.

To stop a compromised or retired app, revoke its integration: in your workspace's settings in the Claude Console, open **App integrations**, select the integration, and click **Revoke**, then confirm. Revoking an integration revokes its outstanding tokens, and its registered devices can no longer request new ones. Revocation is permanent, so create a new app integration to restore access.

### Proxy (production)

For production, route requests through your own back end with `.proxied`. The relay at `baseURL` adds the Claude API credential server-side, so the app ships no key. The `headers` you provide are sent on every request so your proxy can authorize the caller. Pass `[:]` if it needs none:

```swift
ClaudeLanguageModel(
  name: .sonnet5,
  auth: .proxied(headers: ["X-App-Token": "..."]),
  baseURL: URL(string: "https://api.yourapp.com/claude")!
)
```

Your proxy receives standard [Messages API](https://platform.claude.com/docs/en/api/messages/create) requests, attaches the `x-api-key` header, and forwards them to `https://api.anthropic.com`.

### API key (development)

Pass an API key directly while developing:

```swift
ClaudeLanguageModel(name: .sonnet5, auth: .apiKey("YOUR_API_KEY"))
```

<Warning>
  A key bundled into an app is extractable from the shipping binary, and anyone who extracts it can make requests billed to your account. Use `.apiKey` for development only, and switch to App Attest or a proxy before release.
</Warning>

## Streaming

`streamResponse(to:)` returns the response incrementally. Each element is a cumulative snapshot of the response so far, not a delta:

```swift
let stream = session.streamResponse(to: "Summarize today's top science stories.")
for try await partial in stream {
  print(partial.content)
}
```

## Structured output

Annotate a type with `@Generable` and request it with `generating:`. The model returns a value of that type through [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs):

```swift
@Generable
struct Trip {
  @Guide(description: "Destination city") var destination: String
  @Guide(description: "Length in days") var days: Int
}

let response = try await session.respond(to: "Plan a trip to Tokyo.", generating: Trip.self)
print(response.content.destination)
```

Structured output requires a model whose capabilities include it (all compiled-in constants do). If the chosen model does not, the package throws `LanguageModelError.unsupportedGenerationGuide` rather than silently degrading.

## Tool use

### Client-side tools

The framework's `tools:` array works unchanged. Conform your types to `Tool`, pass them to `LanguageModelSession`, and the framework invokes them on the device when Claude calls them. See [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

```swift
let session = LanguageModelSession(model: model, tools: [FindRestaurantsTool()])
```

### Server-side tools

[Server tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools) (web search, web fetch, and code execution) run on Anthropic's infrastructure within a single round trip, with nothing for the framework to invoke on the device. Configure them for each model with `serverTools:`:

```swift
let model = ClaudeLanguageModel(
  name: .sonnet5,
  auth: auth,
  serverTools: [
    .webSearch(maxUses: 5),
    .codeExecution,
  ]
)
```

`.webSearch` and `.webFetch` accept optional `allowedDomains`, `blockedDomains`, and `maxUses`. Server tool activity surfaces in the transcript as `ClaudeServerToolSegment` custom segments.

<Note>
  `serverTools` is configured on `ClaudeLanguageModel` rather than on `LanguageModelSession` because the session type is Apple's. To use different server-tool sets for each conversation, construct multiple `ClaudeLanguageModel` instances.
</Note>

## Images

Models whose capabilities include image input declare the framework's vision capability. Pass image content through the framework's standard session API; the package converts it to the Claude API's image format. See [Vision](https://platform.claude.com/docs/en/build-with-claude/vision) for image requirements.

## Error handling

The package maps Claude API errors onto Apple's `LanguageModelError` cases where one fits: context-window overflow surfaces as `.contextSizeExceeded`, HTTP 429 as `.rateLimited`, a request past the configured timeout as `.timeout`. Provider errors with no framework equivalent surface as `ClaudeError`. Pattern-match to drive product flows:

```swift
do {
  let response = try await session.respond(to: prompt)
  print(response.content)
} catch ClaudeError.missingCredential {
  // Prompt for an API key.
} catch let error as LanguageModelError {
  // Framework-shaped errors (rate limits, guardrails, context length, decoding).
} catch {
  // Transport errors.
}
```

A common pattern is to catch `.rateLimited` and fall back to `SystemLanguageModel` for that turn, queue the request, or surface a retry affordance.

## Feature support

The package surfaces the Messages API capabilities that the Foundation Models provider protocol can express. Features with no representation in Apple's protocol are not available through it, including:

* Prompt caching controls (the package applies prompt caching automatically; cache TTL and breakpoint placement are not configurable)
* Stop sequences
* Batch processing
* Files API
* Token counting
* Beta headers

## Additional resources

| Reference                                                                                           | Covers                                                                                            |
| --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| [Apple Foundation Models documentation](https://developer.apple.com/documentation/foundationmodels) | `LanguageModelSession`, `@Generable`, `Transcript`, `Tool`, and the rest of the framework surface |
| [`ClaudeForFoundationModels` on GitHub](https://github.com/anthropics/ClaudeForFoundationModels)    | Source, the runnable example, and the issue tracker                                               |
| [Claude API reference](https://platform.claude.com/docs/en/api/overview)                            | The underlying Messages API                                                                       |

The package is licensed under Apache 2.0. Bug reports are welcome through GitHub issues. External pull requests are not being accepted during the beta period.
